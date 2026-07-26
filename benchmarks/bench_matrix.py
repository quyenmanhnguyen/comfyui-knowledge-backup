"""Controlled A/B benchmark harness for the C:\AI ComfyUI setup.

Subcommands:
  start --mode pytorch|sage   start a fresh hidden server (blocks until API ready)
  stop                        stop all ComfyUI servers
  run  --workflow F --prefix P --seed N [--width W --height H] [--timeout T]
       --backend B --phase PH --run-type cold|warm --run-idx I --scenario SC
       --errlog PATH --csv PATH
  pixeldiff A.png B.png       MAE/RMS/max pixel diff (same-size RGB)

Each 'run' samples VRAM (via /system_stats) and server RAM RSS (psutil) every
second, computes SHA-256 of the produced PNG, parses sampler s/it from the
server stderr log tail, and appends one CSV row. No runtime changes are made.
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

import psutil

SERVER = "http://127.0.0.1:8188"
OUTPUT_DIR = Path(r"C:\AI\ComfyUI\output")
BENCH_DIR = Path(r"C:\AI\workflows\BENCH_CONTROLLED_20260719")

CSV_FIELDS = [
    "ts", "phase", "scenario", "backend", "workload", "run_type", "run_idx",
    "seed", "width", "height", "steps", "elapsed_s", "sampler_s_per_it",
    "vram_peak_mb", "ram_peak_mb", "chrome_procs", "sha256", "output_file",
    "state", "notes",
]


def http_json(url, payload=None, timeout=10):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_server_pid():
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cl = " ".join(p.info.get("cmdline") or [])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        if "ComfyUI" in cl and "main.py" in cl and "python" in p.info.get("name", "").lower():
            return p.info["pid"]
    return None


def chrome_count():
    n = 0
    for p in psutil.process_iter(["name"]):
        try:
            if "chrome" in (p.info.get("name") or "").lower():
                n += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return n


class ResourceSampler(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.stop_evt = threading.Event()
        self.vram_peak = 0
        self.ram_peak = 0
        self.chrome_max = 0

    def run(self):
        pid = find_server_pid()
        proc = psutil.Process(pid) if pid else None
        while not self.stop_evt.is_set():
            try:
                stats = http_json(SERVER + "/system_stats", timeout=5)
                for d in stats.get("devices", []):
                    used = d.get("vram_total", 0) - d.get("vram_free", 0)
                    self.vram_peak = max(self.vram_peak, used // (1024 * 1024))
            except Exception:
                pass
            try:
                if proc is None or not proc.is_running():
                    pid = find_server_pid()
                    proc = psutil.Process(pid) if pid else None
                if proc:
                    self.ram_peak = max(self.ram_peak, proc.memory_info().rss // (1024 * 1024))
            except Exception:
                pass
            try:
                self.chrome_max = max(self.chrome_max, chrome_count())
            except Exception:
                pass
            self.stop_evt.wait(1.0)


def load_workflow(path, prefix, seed, width, height):
    with open(path, "r", encoding="utf-8-sig") as f:
        prompt = json.load(f)
    steps = None
    for node in prompt.values():
        ct = node.get("class_type")
        inp = node.get("inputs", {})
        if ct == "SaveImage":
            inp["filename_prefix"] = prefix
        elif ct in ("KSampler",) and seed is not None:
            inp["seed"] = int(seed)
            steps = inp.get("steps")
        elif ct.startswith("ZSamplerTurbo") and seed is not None:
            inp["seed"] = int(seed)
            steps = inp.get("steps")
        elif ct == "EmptyLatentImage" and width and height:
            inp["width"] = int(width)
            inp["height"] = int(height)
    return prompt, steps


def parse_sit(errlog_path):
    """Return (s_per_it or None) from the last tqdm line of the server stderr log."""
    try:
        data = Path(errlog_path).read_bytes()[-200000:].decode("utf-8", "replace")
    except Exception:
        return None
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*s/it", data)
    if matches:
        return float(matches[-1])
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*it/s", data)
    if matches:
        v = float(matches[-1])
        return round(1.0 / v, 3) if v else None
    return None


def wait_completion(prompt_id, timeout):
    t0 = time.time()
    while True:
        elapsed = time.time() - t0
        if elapsed > timeout:
            return "timeout", elapsed, []
        try:
            hist = http_json(f"{SERVER}/history/{prompt_id}", timeout=10)
        except urllib.error.URLError:
            time.sleep(2)
            continue
        entry = hist.get(prompt_id)
        if not entry:
            time.sleep(2)
            continue
        status = entry.get("status", {})
        if status.get("completed"):
            images = []
            for o in entry.get("outputs", {}).values():
                if isinstance(o, dict):
                    for img in o.get("images", []):
                        if "filename" in img:
                            images.append(img["filename"])
            return "completed", time.time() - t0, images
        if status.get("status_str") == "error":
            return "error", time.time() - t0, []
        time.sleep(2)


def cmd_start(mode):
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
         r"C:\AI\workflows\BENCH_SAGE_20260719\bench_start.ps1", "-Mode", mode],
        check=True)


def cmd_stop():
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
         r"C:\AI\workflows\BENCH_SAGE_20260719\bench_stop.ps1"],
        check=True)


def cmd_run(a):
    sampler = ResourceSampler()
    sampler.start()
    state, elapsed, images = "error", 0.0, []
    try:
        prompt, steps = load_workflow(a.workflow, a.prefix, a.seed, a.width, a.height)
    except Exception as exc:
        print("LOAD_FAIL:", exc)
        steps = None
        prompt = None
    if prompt is not None:
        try:
            resp = http_json(SERVER + "/prompt",
                             {"prompt": prompt, "client_id": str(uuid.uuid4())}, timeout=30)
            state, elapsed, images = wait_completion(resp["prompt_id"], a.timeout)
        except Exception as exc:
            print("QUEUE_FAIL:", exc)
    sampler.stop_evt.set()
    sampler.join(timeout=3)

    sha, out_file = "", ""
    if images:
        cand = OUTPUT_DIR / images[0]
        if cand.is_file():
            sha = hashlib.sha256(cand.read_bytes()).hexdigest()[:16]
            out_file = cand.name

    sit = parse_sit(a.errlog)
    row = {
        "ts": time.strftime("%H:%M:%S"),
        "phase": a.phase, "scenario": a.scenario, "backend": a.backend,
        "workload": a.workload or Path(a.workflow).stem,
        "run_type": a.run_type, "run_idx": a.run_idx,
        "seed": a.seed, "width": a.width or "", "height": a.height or "",
        "steps": steps if steps is not None else "",
        "elapsed_s": round(elapsed, 1), "sampler_s_per_it": sit if sit is not None else "",
        "vram_peak_mb": sampler.vram_peak, "ram_peak_mb": sampler.ram_peak,
        "chrome_procs": sampler.chrome_max,
        "sha256": sha, "output_file": out_file, "state": state, "notes": a.notes or "",
    }
    csv_path = Path(a.csv)
    new = not csv_path.is_file()
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    print(json.dumps(row))


def cmd_pixeldiff(a):
    from PIL import Image, ImageChops
    import math
    im1 = Image.open(a.file1).convert("RGB")
    im2 = Image.open(a.file2).convert("RGB")
    if im1.size != im2.size:
        print(json.dumps({"error": "size mismatch", "a": im1.size, "b": im2.size}))
        return
    diff = ImageChops.difference(im1, im2)
    hist = diff.histogram()
    sq = sum(value * ((idx % 256) ** 2) for idx, value in enumerate(hist))
    n = im1.size[0] * im1.size[1] * 3
    rms = math.sqrt(sq / n)
    mae = sum(value * (idx % 256) for idx, value in enumerate(hist)) / n
    mx = max((idx % 256) for idx, value in enumerate(hist) if value)
    print(json.dumps({"file1": Path(a.file1).name, "file2": Path(a.file2).name,
                      "mae": round(mae, 3), "rms": round(rms, 3), "max": mx}))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("start")
    sp.add_argument("--mode", choices=["pytorch", "sage"], required=True)
    sub.add_parser("stop")
    rp = sub.add_parser("run")
    rp.add_argument("--workflow", required=True)
    rp.add_argument("--prefix", required=True)
    rp.add_argument("--seed", type=int, default=None)
    rp.add_argument("--width", type=int, default=None)
    rp.add_argument("--height", type=int, default=None)
    rp.add_argument("--timeout", type=float, default=300.0)
    rp.add_argument("--backend", required=True)
    rp.add_argument("--phase", required=True)
    rp.add_argument("--run-type", dest="run_type", required=True)
    rp.add_argument("--run-idx", dest="run_idx", type=int, required=True)
    rp.add_argument("--scenario", default="clean")
    rp.add_argument("--workload", default="")
    rp.add_argument("--errlog", required=True)
    rp.add_argument("--csv", required=True)
    rp.add_argument("--notes", default="")
    pp = sub.add_parser("pixeldiff")
    pp.add_argument("file1")
    pp.add_argument("file2")
    a = ap.parse_args()
    BENCH_DIR.mkdir(parents=True, exist_ok=True)
    if a.cmd == "start":
        cmd_start(a.mode)
    elif a.cmd == "stop":
        cmd_stop()
    elif a.cmd == "run":
        cmd_run(a)
    elif a.cmd == "pixeldiff":
        cmd_pixeldiff(a)


if __name__ == "__main__":
    main()
