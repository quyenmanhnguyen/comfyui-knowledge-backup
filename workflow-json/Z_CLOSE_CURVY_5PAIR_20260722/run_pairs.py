import csv
import json
import subprocess
import time
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(r"C:\AI")
OUT = ROOT / r"workflows\Z_CLOSE_CURVY_5PAIR_20260722"
PY = ROOT / r"python_embeded\python.exe"
CTL = ROOT / r"workflows\BENCH_CONTROLLED_20260719\bench_matrix.py"
SERVER = "http://127.0.0.1:8188"

RECIPES = [
    ("Z1_DIVING_RES2S", ROOT / r"workflows\FINAL_SFW_NSFW_20260722\Z03_DIVING_SFW.json"),
    ("Z2_BEYOND_RES2S", ROOT / r"workflows\FINAL_SFW_NSFW_20260722\Z01_BEYOND_SFW.json"),
    ("Z3_MOODY_RES2S", ROOT / r"workflows\FINAL_SFW_NSFW_20260722\Z02_MOODY_SFW.json"),
    ("Z4_MOODY_EULER_H4", ROOT / r"workflows\OLD_WINNER_SLOW_20260722\B1_H4_ORIGINAL.json"),
    ("Z5_BEYOND_X21", ROOT / r"workflows\COMMUNITY_TEST_20260717\FINAL_TOP10_PAIR_20260719\08_BEYOND_X21_NSFW.json"),
]

SFW = (
    "Premium close three-quarter editorial photograph, one clearly adult Vietnamese woman age 29, solo, "
    "youthful soft oval adult face, gentle confident expression, long natural dark hair, naturally fuller curvy "
    "figure with soft healthy proportions, framed from head to mid-thigh, standing at a slight three-quarter angle, "
    "both complete hands relaxed and clearly visible, wearing a fitted ivory silk wrap dress beneath a tailored black "
    "jacket, bright diffused window key light and clean white bounce fill, luminous neutral-warm skin, subtle natural "
    "blush, fine pores, peach fuzz and restrained microcontrast, 70mm portrait lens, shallow depth of field, simple "
    "warm-grey studio, realistic fabric and hair, no writing or watermark"
)

NSFW = (
    "Premium close three-quarter fine-art studio photograph, one clearly adult Vietnamese woman age 29, solo, "
    "nonsexual nude adult figure study, youthful soft oval adult face, gentle confident expression, long natural dark "
    "hair, naturally fuller curvy figure with soft healthy adult proportions, framed from head to mid-thigh, standing "
    "at a slight three-quarter angle, both complete hands relaxed, separated and clearly visible, natural adult anatomy, "
    "bright diffused window key light and clean white bounce fill, luminous neutral-warm skin, subtle natural blush, "
    "fine pores, peach fuzz and restrained microcontrast, 70mm portrait lens, shallow depth of field, simple warm-grey "
    "studio, no props, no writing or watermark"
)


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


def make_graph(source, prompt, seed, prefix):
    graph = json.loads(source.read_text(encoding="utf-8-sig"))
    text_nodes = [n for n in graph.values() if n.get("class_type") == "CLIPTextEncode"]
    if not text_nodes:
        raise RuntimeError(f"No CLIPTextEncode in {source}")
    text_nodes[0]["inputs"]["text"] = prompt
    for node in graph.values():
        ctype = node.get("class_type", "")
        inputs = node.get("inputs", {})
        if ctype == "KSampler" and "seed" in inputs:
            inputs["seed"] = seed
        if ctype == "RandomNoise" and "noise_seed" in inputs:
            inputs["noise_seed"] = seed
        if ctype == "SaveImage":
            inputs["filename_prefix"] = prefix
    return graph


def execute(graph):
    started = time.time()
    queued = request("/prompt", {"prompt": graph, "client_id": str(uuid.uuid4())})
    if queued.get("node_errors"):
        return "node_error", 0, "", json.dumps(queued["node_errors"])[:700]
    prompt_id = queued["prompt_id"]
    while time.time() - started < 240:
        entry = request("/history/" + prompt_id, timeout=10).get(prompt_id)
        if entry and entry.get("status", {}).get("completed"):
            images = [i["filename"] for o in entry.get("outputs", {}).values() for i in o.get("images", [])]
            return "ok", round(time.time() - started, 1), images[0] if images else "", ""
        if entry and entry.get("status", {}).get("status_str") == "error":
            return "error", round(time.time() - started, 1), "", json.dumps(entry["status"])[:700]
        time.sleep(2)
    try:
        request("/interrupt", {}, 5)
    except Exception:
        pass
    return "timeout", 240, "", "four-minute limit"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    result_path = OUT / "results.csv"
    rows = []
    if result_path.exists():
        with result_path.open("r", newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
    for index, (name, source) in enumerate(RECIPES, start=1):
        for variant, prompt, seed in (("SFW", SFW, 7229651), ("NSFW", NSFW, 7229652)):
            prior = next((r for r in rows if r["candidate"] == name and r["variant"] == variant), None)
            if prior and prior["state"] == "ok":
                continue
            stop()
            start()
            graph = make_graph(source, prompt, seed, f"ZC5-{index:02d}_{name}-{variant}")
            workflow = OUT / f"{name}_{variant}.json"
            workflow.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
            try:
                state, seconds, image, note = execute(graph)
            except Exception as exc:
                state, seconds, image, note = "exception", 0, "", repr(exc)
            row = {"candidate": name, "variant": variant, "state": state, "elapsed_s": seconds,
                   "image": image, "workflow": str(workflow), "source": str(source), "note": note}
            rows = [r for r in rows if not (r["candidate"] == name and r["variant"] == variant)]
            rows.append(row)
            print(row, flush=True)
            with result_path.open("w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.DictWriter(handle, fieldnames=row.keys())
                writer.writeheader()
                writer.writerows(rows)
    stop()


if __name__ == "__main__":
    main()
