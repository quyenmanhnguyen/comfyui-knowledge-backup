import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(r"C:\AI")
HERE = Path(__file__).parent
SOURCE = ROOT / r"workflows\Z_CLOSE_CURVY_5PAIR_20260722"
RUNNER = ROOT / r"workflows\STYLE_EXPANSION_CIVITAI_TG_20260724\run_styles.py"

spec = importlib.util.spec_from_file_location("base_runner", RUNNER)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

JOBS = [
    "Z1_DIVING_RES2S_SFW",
    "Z1_DIVING_RES2S_NSFW",
    "Z2_BEYOND_RES2S_SFW",
    "Z2_BEYOND_RES2S_NSFW",
    "Z3_MOODY_RES2S_SFW",
    "Z3_MOODY_RES2S_NSFW",
    "Z4_MOODY_EULER_H4_SFW",
    "Z4_MOODY_EULER_H4_NSFW",
    "Z5_BEYOND_X21_SFW",
    "Z5_BEYOND_X21_NSFW",
]


def load_graph(name, index):
    graph = json.loads((SOURCE / f"{name}.json").read_text(encoding="utf-8-sig"))
    for node in graph.values():
        if node.get("class_type") == "SaveImage":
            node["inputs"]["filename_prefix"] = f"ZFINAL10-{index:02d}_{name}"
    return graph


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    rows = []
    try:
        for index, name in enumerate(JOBS, 1):
            graph = load_graph(name, index)
            workflow = HERE / f"{index:02d}_{name}.json"
            workflow.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"event": "starting", "index": index, "name": name}), flush=True)
            base.server("stop")
            base.server("start")
            try:
                elapsed, filename = base.queue(graph)
                gate = base.gate.evaluate(base.IMAGES / filename)
                row = {
                    "index": index, "name": name, "state": "ok", "elapsed_s": elapsed,
                    "image": filename, "technical_pass": gate["pass"],
                    "gate": json.dumps(gate, ensure_ascii=False), "workflow": str(workflow),
                }
            except Exception as exc:
                row = {
                    "index": index, "name": name, "state": "error", "elapsed_s": 0,
                    "image": "", "technical_pass": False, "gate": repr(exc),
                    "workflow": str(workflow),
                }
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
            with (HERE / "results.csv").open("w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
    finally:
        base.server("stop")


if __name__ == "__main__":
    main()
