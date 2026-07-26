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
OUT = ROOT / r"workflows\TG_CIVITAI_ADV_CINEMATIC_20260724"
IMAGES = ROOT / r"ComfyUI\output"
PY = ROOT / r"python_embeded\python.exe"
CTL = ROOT / r"workflows\BENCH_CONTROLLED_20260719\bench_matrix.py"
GATE = Path(
    r"C:\Users\Admin\.codex\skills\optimize-comfyui-rx7800xt\scripts\visual_gate.py"
)
SERVER = "http://127.0.0.1:8188"

SOURCE_ANIMA = (
    ROOT
    / r"workflows\TG_CIVITAI_6_20260724\A1_MOODY_ANIMA_AUTHOR_NATIVE.json"
)
SOURCE_RIMIX = (
    ROOT / r"workflows\TG_CIVITAI_6_20260724\S1_AMIX_RIMIX065_FULL.json"
)
SOURCE_ONEOBS = (
    ROOT / r"workflows\TG_CIVITAI_6_20260724\S2_ONEOBSESSION_FULL.json"
)

spec = importlib.util.spec_from_file_location("visual_gate", GATE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


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
        raise RuntimeError(json.dumps(queued["node_errors"], ensure_ascii=False)[:2400])
    prompt_id = queued["prompt_id"]
    while time.time() - started < 480:
        entry = api("/history/" + prompt_id, timeout=10).get(prompt_id)
        if entry and entry.get("status", {}).get("completed"):
            files = [
                image["filename"]
                for output in entry.get("outputs", {}).values()
                for image in output.get("images", [])
            ]
            return round(time.time() - started, 1), files[0]
        if entry and entry.get("status", {}).get("status_str") == "error":
            raise RuntimeError(json.dumps(entry["status"], ensure_ascii=False)[:2400])
        time.sleep(2)
    raise TimeoutError("eight-minute cap")


def save_graph(name, graph):
    path = OUT / f"{name}.json"
    path.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return path


def set_seed(graph, seed):
    for node in graph.values():
        inputs = node.get("inputs", {})
        if node.get("class_type") == "KSampler" and "seed" in inputs:
            inputs["seed"] = seed
        if node.get("class_type") == "RandomNoise" and "noise_seed" in inputs:
            inputs["noise_seed"] = seed


ANIMA_SFW = (
    "masterpiece, best quality, very aesthetic, smooth cinematic anime film still, "
    "one clearly adult East Asian woman age 27, solo, elegant long black hair moving in "
    "the rain, youthful adult oval face, warm brown eyes, walking slowly through a quiet "
    "old-city alley at blue hour, fitted black blazer over a deep-red silk dress, both arms "
    "relaxed separately at her sides, exactly two complete hands visible, foreground rain "
    "streaks and wet stone reflections, subject in the midground, layered amber lantern "
    "bokeh and misty architecture in the background, soft motivated amber shop-window key "
    "light, cool moonlit rim, broad neutral face fill, smooth highlight roll-off, gentle "
    "halation, subtle 35mm film grain, controlled teal-and-amber palette, 50mm lens, shallow "
    "depth of field, cinematic vertical composition, clean line art, refined eyes, detailed "
    "silk and wet hair, no text, no watermark, no child, no teen, no loli"
)

ANIMA_NSFW = (
    "masterpiece, best quality, very aesthetic, sensual smooth cinematic anime film still, "
    "one clearly adult East Asian woman age 28, solo, completely nude adult figure, seated "
    "sideways on a white silk chaise beside a tall rain-streaked window, youthful adult oval "
    "face, long glossy black hair, voluptuous soft curvy adult body, large natural breasts "
    "and adult pubic anatomy visible, torso gently turned toward camera, both arms separated, "
    "exactly two complete hands resting visibly on different parts of the chaise, foreground "
    "sheer curtain edge, subject in the midground, warm practical lamps and rainy city bokeh "
    "in the background, soft amber motivated key from one side, cool blue window rim, broad "
    "pearl-white fill on the face, smooth tonal roll-off, gentle halation, subtle 35mm film "
    "grain, restrained highlights, cinematic vertical composition, coherent adult anatomy, "
    "clean line art, no text, no watermark, no child, no teen, no loli"
)

ILLUST_SFW = (
    "masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, smooth "
    "cinematic anime film still, layered depth of field, adult, aged up, 1woman, solo, clearly "
    "adult East Asian woman age 27, youthful oval adult face, warm brown eyes, long black hair "
    "moving in rain, fitted black blazer, deep-red silk dress, walking through a quiet old-city "
    "alley at blue hour, both arms relaxed separately, exactly two complete hands visible, "
    "foreground rain streaks and wet pavement reflections, centered midground subject, layered "
    "amber lantern bokeh and misty architecture, motivated amber shop-window key light, cool "
    "moon rim light, broad soft face fill, smooth highlight roll-off, gentle halation, subtle "
    "35mm film grain, controlled teal and amber color grade, 50mm lens, cinematic vertical "
    "frame, detailed silk and wet hair, refined eyes"
)

ILLUST_NSFW = (
    "masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, sensual "
    "smooth cinematic anime film still, layered depth of field, adult, aged up, 1woman, solo, "
    "clearly adult East Asian woman age 28, completely nude adult figure, seated sideways on "
    "a white silk chaise beside a tall rain-streaked window, youthful oval adult face, long "
    "glossy black hair, voluptuous soft curvy adult body, large natural breasts and adult "
    "vulva visible, torso gently turned toward camera, both arms separated, exactly two "
    "complete hands resting visibly on different parts of the chaise, foreground sheer "
    "curtain edge, midground subject, warm practical lamps and rainy city bokeh in background, "
    "motivated amber side key, cool blue window rim, broad pearl-white face fill, smooth tonal "
    "roll-off, gentle halation, subtle 35mm film grain, controlled contrast, coherent adult "
    "anatomy, cinematic vertical frame"
)

NEGATIVE = (
    "lowres, worst quality, low quality, bad anatomy, bad hands, extra hands, extra fingers, "
    "fused fingers, missing fingers, extra limbs, duplicate person, malformed feet, cropped "
    "hands, text, logo, watermark, fake lettering, child, teen, loli, flat "
    "lighting, crushed blacks, blown highlights, neon eyes, oversaturated skin, waxy skin, "
    "plastic skin, heavy sharpening, color bleed"
)


def build_moody_anima(prompt, seed, prefix):
    g = read(SOURCE_ANIMA)
    g["7"]["inputs"]["text"] = prompt
    g["8"]["inputs"].update({"width": 832, "height": 1216})
    set_seed(g, seed)
    g["15"]["inputs"]["filename_prefix"] = prefix
    return g


def build_anima_rimix(prompt, seed, prefix):
    g = read(SOURCE_ANIMA)
    g["1"]["inputs"]["unet_name"] = "anima_baseV10.safetensors"
    g["2"] = {
        "class_type": "LoraLoaderModelOnly",
        "inputs": {
            "model": ["1", 0],
            "lora_name": "rimixao5050.safetensors",
            "strength_model": 0.70,
        },
    }
    g["7"]["inputs"]["text"] = prompt
    g["8"]["inputs"].update({"width": 768, "height": 1152})
    g["16"] = {
        "class_type": "ConditioningZeroOut",
        "inputs": {"conditioning": ["7", 0]},
    }
    g["17"] = {
        "class_type": "KSampler",
        "inputs": {
            "model": ["2", 0],
            "positive": ["7", 0],
            "negative": ["16", 0],
            "latent_image": ["8", 0],
            "seed": seed,
            "steps": 32,
            "cfg": 3,
            "sampler_name": "er_sde",
            "scheduler": "simple",
            "denoise": 1,
        },
    }
    g["14"]["inputs"]["samples"] = ["17", 0]
    for node_id in ("9", "10", "11", "12", "13"):
        g.pop(node_id, None)
    g["15"]["inputs"]["filename_prefix"] = prefix
    return g


def build_illustrious(source, prompt, seed, prefix):
    g = read(source)
    g["2"]["inputs"]["text"] = prompt
    g["3"]["inputs"]["text"] = NEGATIVE
    set_seed(g, seed)
    g["8"]["inputs"]["filename_prefix"] = prefix
    return g


def jobs():
    seed_sfw = 72428011
    seed_nsfw = 72428022
    return [
        (
            "A1_MOODY_ANIMA_CINEMATIC_SFW",
            "Anima",
            "Civitai author model/workflow + Telegram cinematic grammar",
            build_moody_anima(
                ANIMA_SFW, seed_sfw, "ADV8-A1_MOODY_ANIMA_CINEMATIC_SFW"
            ),
        ),
        (
            "A2_MOODY_ANIMA_CINEMATIC_NSFW",
            "Anima",
            "Civitai author model/workflow + Telegram cinematic grammar",
            build_moody_anima(
                ANIMA_NSFW, seed_nsfw, "ADV8-A2_MOODY_ANIMA_CINEMATIC_NSFW"
            ),
        ),
        (
            "A3_ANIMA_RIMIX_ALPHA_SFW",
            "Anima",
            "Ri-mix alpha Anima author settings",
            build_anima_rimix(
                ANIMA_SFW, seed_sfw, "ADV8-A3_ANIMA_RIMIX_ALPHA_SFW"
            ),
        ),
        (
            "A4_ANIMA_RIMIX_ALPHA_NSFW",
            "Anima",
            "Ri-mix alpha Anima author settings",
            build_anima_rimix(
                ANIMA_NSFW, seed_nsfw, "ADV8-A4_ANIMA_RIMIX_ALPHA_NSFW"
            ),
        ),
        (
            "S1_AMIX_RIMIX_CINEMATIC_SFW",
            "SDXL/Illustrious",
            "Ri-mix Omega author settings + Telegram cinematic grammar",
            build_illustrious(
                SOURCE_RIMIX,
                ILLUST_SFW,
                seed_sfw,
                "ADV8-S1_AMIX_RIMIX_CINEMATIC_SFW",
            ),
        ),
        (
            "S2_AMIX_RIMIX_CINEMATIC_NSFW",
            "SDXL/Illustrious",
            "Ri-mix Omega author settings + Telegram cinematic grammar",
            build_illustrious(
                SOURCE_RIMIX,
                ILLUST_NSFW,
                seed_nsfw,
                "ADV8-S2_AMIX_RIMIX_CINEMATIC_NSFW",
            ),
        ),
        (
            "S3_ONEOBSESSION_CINEMATIC_SFW",
            "SDXL/Illustrious",
            "OneObsession v23 high-contrast author direction",
            build_illustrious(
                SOURCE_ONEOBS,
                ILLUST_SFW,
                seed_sfw,
                "ADV8-S3_ONEOBSESSION_CINEMATIC_SFW",
            ),
        ),
        (
            "S4_ONEOBSESSION_CINEMATIC_NSFW",
            "SDXL/Illustrious",
            "OneObsession v23 high-contrast author direction",
            build_illustrious(
                SOURCE_ONEOBS,
                ILLUST_NSFW,
                seed_nsfw,
                "ADV8-S4_ONEOBSESSION_CINEMATIC_NSFW",
            ),
        ),
    ]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    try:
        for index, (name, family, evidence, graph) in enumerate(jobs(), 1):
            workflow = save_graph(name, graph)
            print(
                json.dumps(
                    {"event": "starting", "index": index, "name": name},
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
