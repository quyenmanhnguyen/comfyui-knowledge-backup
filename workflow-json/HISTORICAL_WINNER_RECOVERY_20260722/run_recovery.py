import csv
import json
import subprocess
import time
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(r"C:\AI")
OUT = ROOT / r"workflows\HISTORICAL_WINNER_RECOVERY_20260722"
PY = ROOT / r"python_embeded\python.exe"
CTL = ROOT / r"workflows\BENCH_CONTROLLED_20260719\bench_matrix.py"
SERVER = "http://127.0.0.1:8188"

CASES = [
    ("SDXL_INTO_AUTHOR", ROOT / r"workflows\DISCOVERY20_PAIR_20260721\S11_INTO_AUTHOR_NSFW.json"),
    ("SDXL_INTO_NATIVE", ROOT / r"workflows\REBAlANCE_SDXL_Z_20260721\R01_INTO_NATIVE_NSFW.json"),
    ("SDXL_INTO_FIXED", ROOT / r"workflows\KEEP_MAIN_SDXL_REBUILD_20260721\05_INTOREALISM_FIXED_NSFW.json"),
    ("SDXL_REALVIS_SDE", ROOT / r"workflows\DISCOVERY20_PAIR_20260721\S13_REALVIS_SDE_NSFW.json"),
    ("Z_MOODY_RES2S", ROOT / r"workflows\COMMUNITY_TEST_20260717\FINAL_TOP10_PAIR_20260719\01_MOODY_RES2S_NSFW.json"),
    ("Z_DIVING_RES2S", ROOT / r"workflows\FINAL_SFW_NSFW_20260722\Z03_DIVING_NSFW.json"),
    ("Z_BEYOND_RES2S", ROOT / r"workflows\FINAL_SFW_NSFW_20260722\Z01_BEYOND_NSFW.json"),
]


def request(path, payload=None, timeout=30):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(SERVER + path, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
        return json.loads(raw) if raw else {}


def stop():
    subprocess.run([str(PY), str(CTL), "stop"], check=False)


def start():
    subprocess.run([str(PY), str(CTL), "start", "--mode", "pytorch"], check=True)


def run_case(name, source):
    graph = json.loads(source.read_text(encoding="utf-8-sig"))
    for node in graph.values():
        if node.get("class_type") == "SaveImage":
            node["inputs"]["filename_prefix"] = "RECOVER-" + name
    saved = OUT / f"{name}.json"
    saved.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    started = time.time()
    queued = request("/prompt", {"prompt": graph, "client_id": str(uuid.uuid4())})
    if queued.get("node_errors"):
        return "node_error", 0, "", json.dumps(queued["node_errors"])[:800]
    prompt_id = queued["prompt_id"]
    while time.time() - started < 240:
        entry = request("/history/" + prompt_id, timeout=10).get(prompt_id)
        if entry and entry.get("status", {}).get("completed"):
            images = [i["filename"] for o in entry.get("outputs", {}).values() for i in o.get("images", [])]
            return "ok", round(time.time() - started, 1), images[0] if images else "", ""
        if entry and entry.get("status", {}).get("status_str") == "error":
            return "error", round(time.time() - started, 1), "", json.dumps(entry["status"])[:800]
        time.sleep(2)
    try:
        request("/interrupt", {}, timeout=5)
    except Exception:
        pass
    return "timeout", 240, "", "four-minute limit"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    current_family = None
    for name, source in CASES:
        family = name.split("_", 1)[0]
        if family != current_family:
            stop()
            start()
            current_family = family
        try:
            state, seconds, image, note = run_case(name, source)
        except Exception as exc:
            state, seconds, image, note = "exception", 0, "", repr(exc)
        row = {"candidate": name, "state": state, "elapsed_s": seconds, "image": image,
               "source_workflow": str(source), "recovery_workflow": str(OUT / f"{name}.json"), "note": note}
        rows.append(row)
        print(row, flush=True)
        with (OUT / "results.csv").open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=row.keys())
            writer.writeheader()
            writer.writerows(rows)
    stop()


if __name__ == "__main__":
    main()
