import csv
import importlib.util
import json
import subprocess
import time
import urllib.request
import uuid
from copy import deepcopy
from pathlib import Path

ROOT = Path(r"C:\AI")
OUT = ROOT / r"workflows\TG_CIVITAI_6_20260724"
IMAGES = ROOT / r"ComfyUI\output"
PY = ROOT / r"python_embeded\python.exe"
CTL = ROOT / r"workflows\BENCH_CONTROLLED_20260719\bench_matrix.py"
GATE = Path(
    r"C:\Users\Admin\.codex\skills\optimize-comfyui-rx7800xt\scripts\visual_gate.py"
)
SERVER = "http://127.0.0.1:8188"

SOURCES = {
    "A1": ROOT
    / r"workflows\TELEGRAM_Z_SDXL_ANIMA_8_20260723\ANIMA_YUME_NSFW.json",
    "A2": ROOT
    / r"workflows\SOFTWHITE_EXPANSION6_20260722\A5_ANIMA_NIJI_NSFW.json",
    "Z1": ROOT
    / r"workflows\Z_CLOSE_CURVY_5PAIR_20260722\Z3_MOODY_RES2S_NSFW.json",
    "Z2": ROOT
    / r"workflows\Z_CLOSE_CURVY_5PAIR_20260722\Z1_DIVING_RES2S_NSFW.json",
    "S1": ROOT
    / r"workflows\YOUTHFUL_CLEAN_NSFW_20260722\I1_RIMIX_FULL.json",
    "S2": ROOT
    / r"workflows\YOUTHFUL_CLEAN_NSFW_20260722\I2_OBSESSION_FULL.json",
}

spec = importlib.util.spec_from_file_location("visual_gate", GATE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def load(name):
    return json.loads(SOURCES[name].read_text(encoding="utf-8-sig"))


def save_graph(name, graph):
    path = OUT / f"{name}.json"
    path.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return path


def api(path, payload=None, timeout=30):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        SERVER + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read()
        return json.loads(body) if body else {}


def server(action):
    command = [str(PY), str(CTL), action]
    if action == "start":
        command += ["--mode", "pytorch"]
    subprocess.run(command, check=action == "start")


def queue(graph):
    started = time.time()
    queued = api("/prompt", {"prompt": graph, "client_id": str(uuid.uuid4())})
    if queued.get("node_errors"):
        raise RuntimeError(json.dumps(queued["node_errors"], ensure_ascii=False)[:2000])
    prompt_id = queued["prompt_id"]
    while time.time() - started < 480:
        entry = api("/history/" + prompt_id, timeout=10).get(prompt_id)
        if entry and entry.get("status", {}).get("completed"):
            files = [
                item["filename"]
                for output in entry.get("outputs", {}).values()
                for item in output.get("images", [])
            ]
            return round(time.time() - started, 1), files[0]
        if entry and entry.get("status", {}).get("status_str") == "error":
            raise RuntimeError(json.dumps(entry["status"], ensure_ascii=False)[:2000])
        time.sleep(2)
    raise TimeoutError("eight-minute cap")


def set_seed(graph, seed):
    for node in graph.values():
        inputs = node.get("inputs", {})
        if node.get("class_type") == "KSampler" and "seed" in inputs:
            inputs["seed"] = seed
        if node.get("class_type") == "RandomNoise" and "noise_seed" in inputs:
            inputs["noise_seed"] = seed


def build():
    jobs = []

    # Current Telegram/Civitai author direction: Moody Anima Mix at native size,
    # direct ER-SDE 4-step sampling. Author's 2.5x upscale is intentionally removed.
    g = load("A1")
    g["1"]["inputs"]["unet_name"] = "moodyAnimaMix_v10.safetensors"
    del g["2"]
    g["10"]["inputs"]["model"] = ["1", 0]
    g["11"] = {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "er_sde"}}
    g["12"]["inputs"].update({"model": ["1", 0], "scheduler": "simple", "steps": 4})
    g["8"]["inputs"].update({"width": 832, "height": 1216})
    g["7"]["inputs"]["text"] = (
        "masterpiece, best quality, very aesthetic, crisp detailed anime illustration, "
        "one clearly adult woman age 26, solo, completely nude, full body, voluptuous "
        "soft curvy adult figure, large natural breasts and adult pubic anatomy visible, "
        "long glossy dark hair, youthful adult oval face, warm brown eyes, gentle teasing "
        "smile, standing in a bright white bedroom, slight three-quarter pose, both hands "
        "relaxed and fully visible, both feet visible, coherent adult anatomy, soft diffused "
        "window light, delicate fair skin, subtle blush, clean line art, restrained highlights, "
        "no text, no watermark, no child, no teen, no loli"
    )
    set_seed(g, 72426011)
    g["15"]["inputs"]["filename_prefix"] = "TGCIV6-A1_MOODY_ANIMA_AUTHOR_NATIVE"
    jobs.append(("A1_MOODY_ANIMA_AUTHOR_NATIVE", g, "Anima", "Telegram+Civitai author"))

    # Locally proven Anima full-quality path: base + Turbo + Niji semi-realism 0.60.
    g = load("A2")
    g["8"]["inputs"].update({"width": 768, "height": 1152})
    g["7"]["inputs"]["text"] = (
        "masterwork, masterpiece, best quality, detailed, very aesthetic, soft high-key "
        "semi-real anime illustration, one clearly adult Vietnamese woman age 28, solo, "
        "completely nude, kneeling upright on a white bed, voluptuous soft curvy adult body, "
        "large natural breasts and adult vulva visible, hands resting separately on her thighs, "
        "all fingers visible, youthful gentle adult face, long dark hair, warm brown eyes, "
        "bright sheer-curtain daylight, airy white room, luminous neutral fair skin, subtle "
        "natural blush, clean linework, refined eyes, coherent adult anatomy, no child, no teen, "
        "no loli, no text, no watermark"
    )
    set_seed(g, 72426022)
    g["15"]["inputs"]["filename_prefix"] = "TGCIV6-A2_ANIMA_NIJI_FULL"
    jobs.append(("A2_ANIMA_NIJI_FULL", g, "Anima", "local proven + Telegram"))

    # Current Moody Z-Image v7 author core: SDA 0.49, shift 3, 9-step DPM++ 2M SDE beta.
    g = load("Z1")
    g["11"] = {
        "class_type": "LoraLoaderModelOnly",
        "inputs": {
            "model": ["1", 0],
            "lora_name": "zit_sda_v1.safetensors",
            "strength_model": 0.49,
        },
    }
    g["7"]["inputs"].update({"model": ["11", 0], "shift": 3})
    g["6"]["inputs"].update({"width": 640, "height": 960})
    g["8"]["inputs"].update(
        {
            "steps": 9,
            "cfg": 1,
            "sampler_name": "dpmpp_2m_sde",
            "scheduler": "beta",
        }
    )
    g["4"]["inputs"]["text"] = (
        "Premium bright close three-quarter editorial nude photograph, one clearly adult "
        "Vietnamese woman age 27, solo, completely nude, youthful soft oval adult face, long "
        "natural dark hair, healthy voluptuous curvy adult figure, large natural breasts and "
        "adult pubic anatomy visible, seated sideways on a white bed with torso turned toward "
        "camera, both complete hands separated and visible, coherent natural adult anatomy, "
        "soft diffused morning window light, clean white bounce fill, luminous neutral-warm "
        "skin, fine pores and peach fuzz, subtle blush, crisp eyes, 70mm lens, shallow depth "
        "of field, bright uncluttered room, no writing, no watermark, no child, no teen"
    )
    set_seed(g, 72426033)
    g["10"]["inputs"]["filename_prefix"] = "TGCIV6-Z1_MOODY_SDA49_AUTHOR"
    jobs.append(("Z1_MOODY_SDA49_AUTHOR", g, "Z-Image", "Civitai author core"))

    # Locally proven Z-Image youth/brightness control.
    g = load("Z2")
    g["4"]["inputs"]["text"] = (
        "Premium luminous close portrait photograph, one clearly adult Vietnamese woman age "
        "26, solo, completely nude, framed head to upper thighs, youthful rounded adult face, "
        "bright clear eyes, long dark hair, soft healthy voluptuous curves, large natural "
        "breasts and adult pubic anatomy visible, gentle confident smile, standing beside a "
        "white-curtained window in a slight three-quarter pose, both hands relaxed and fully "
        "visible, coherent natural adult anatomy, high-key diffused daylight, clean white fill, "
        "fresh neutral fair skin, fine pores, peach fuzz, restrained microcontrast, 70mm lens, "
        "simple pale studio, no text, no watermark, no child, no teen"
    )
    set_seed(g, 72426044)
    g["10"]["inputs"]["filename_prefix"] = "TGCIV6-Z2_DIVING_RES2S_PROVEN"
    jobs.append(("Z2_DIVING_RES2S_PROVEN", g, "Z-Image", "local proven"))

    # Full native SDXL/Illustrious anime path: aMix + Ri-mix 0.65, 30 steps.
    g = load("S1")
    g["2"]["inputs"]["text"] = (
        "masterwork, masterpiece, best quality, ultra detailed, very aesthetic, polished "
        "semi-real anime illustration, one clearly adult woman age 27, solo, completely nude, "
        "full body, voluptuous curvy adult body, large natural breasts and adult vulva visible, "
        "kneeling upright on a pale silk bed, hands resting separately on thighs, fingers "
        "clearly drawn, both feet visible, youthful adult oval face, long dark hair, warm brown "
        "eyes, gentle inviting expression, bright soft window light, clean white room, luminous "
        "fair skin, subtle blush, refined line art, detailed eyes, coherent adult anatomy"
    )
    set_seed(g, 72426055)
    g["8"]["inputs"]["filename_prefix"] = "TGCIV6-S1_AMIX_RIMIX065_FULL"
    jobs.append(("S1_AMIX_RIMIX065_FULL", g, "SDXL/Illustrious", "local proven"))

    # Full native OneObsession adult anime path, 32-step DPM++ 2M Karras.
    g = load("S2")
    g["2"]["inputs"]["text"] = (
        "masterwork, masterpiece, best quality, ultra detailed, premium mature anime "
        "illustration, one clearly adult woman age 28, solo, completely nude, voluptuous soft "
        "curvy adult body, large natural breasts and adult vulva visible, reclining sideways "
        "on a white chaise with one knee raised, torso facing viewer, both hands separated and "
        "fully visible, youthful adult oval face, glossy long dark hair, bright expressive "
        "brown eyes, clean high-key studio daylight, pale warm background, luminous fair skin, "
        "subtle blush, crisp contours, fine hair strands, coherent adult anatomy"
    )
    set_seed(g, 72426066)
    g["8"]["inputs"]["filename_prefix"] = "TGCIV6-S2_ONEOBSESSION_FULL"
    jobs.append(("S2_ONEOBSESSION_FULL", g, "SDXL/Illustrious", "local proven"))

    return jobs


def main():
    rows = []
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        for index, (name, graph, family, evidence) in enumerate(build(), 1):
            workflow = save_graph(name, graph)
            print(
                json.dumps(
                    {"event": "starting", "index": index, "name": name, "family": family},
                    ensure_ascii=False,
                ),
                flush=True,
            )
            server("stop")
            server("start")
            elapsed, filename = queue(graph)
            result = gate.evaluate(IMAGES / filename)
            row = {
                "index": index,
                "name": name,
                "family": family,
                "evidence": evidence,
                "elapsed_s": elapsed,
                "image": filename,
                "technical_pass": result["pass"],
                "gate": json.dumps(result, ensure_ascii=False),
                "workflow": str(workflow),
            }
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    finally:
        server("stop")
        if rows:
            with (OUT / "results.csv").open(
                "w", newline="", encoding="utf-8-sig"
            ) as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)


if __name__ == "__main__":
    main()
