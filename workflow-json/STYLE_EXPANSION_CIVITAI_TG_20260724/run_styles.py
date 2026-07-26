import csv
import importlib.util
import json
import subprocess
import time
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(r"C:\AI")
OUT = ROOT / r"workflows\STYLE_EXPANSION_CIVITAI_TG_20260724"
IMAGES = ROOT / r"ComfyUI\output"
PY = ROOT / r"python_embeded\python.exe"
CTL = ROOT / r"workflows\BENCH_CONTROLLED_20260719\bench_matrix.py"
ANIMA_SOURCE = ROOT / r"workflows\TG_CIVITAI_ADV_CINEMATIC_20260724\A3_ANIMA_RIMIX_ALPHA_SFW.json"
ONEOBS_SOURCE = ROOT / r"workflows\TG_CIVITAI_ADV_CINEMATIC_20260724\S4_ONEOBSESSION_CINEMATIC_NSFW.json"
GATE_PATH = Path(r"C:\Users\Admin\.codex\skills\optimize-comfyui-rx7800xt\scripts\visual_gate.py")
SERVER = "http://127.0.0.1:8188"

spec = importlib.util.spec_from_file_location("visual_gate", GATE_PATH)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

ANIMA_STYLES = [
    {
        "name": "A1_GOTHIC_NEON",
        "lora": "GothicNeonAnima.safetensors",
        "strength": 0.82,
        "seed": 72429101,
        "source": "Civitai model 888231/version 3022620 + local Telegram neon/CCD lighting grammar",
        "prompt": (
            "masterpiece, best quality, very aesthetic, g0thic n30n, neon lights, glowing, "
            "one clearly adult East Asian woman age 28, solo, voluptuous curvy adult figure, "
            "black lace and glossy midnight-blue silk, seated in an ornate gothic lounge, long "
            "black hair with bangs, direct confident gaze, pearl choker, magenta stained-glass "
            "window, cyan edge light, deep violet shadows, glossy skin highlights, separated "
            "hands resting on different cushions, close three-quarter portrait, crisp anime "
            "line art, intricate gothic metalwork, no text, no child, no teen, no loli"
        ),
    },
    {
        "name": "A2_DARK_ART",
        "lora": "dark_art_style_Anima-step00002750.safetensors",
        "strength": 1.0,
        "seed": 72429102,
        "source": "Civitai model 1380736/version 2817661; author trigger and weight 1.0",
        "prompt": (
            "masterpiece, best quality, very aesthetic, dark_art_style, one clearly adult East "
            "Asian woman age 29, solo, mature voluptuous figure, black translucent ceremonial "
            "veil and dark crimson silk, reclining on a carved ebony chaise in a candlelit occult "
            "library, long black hair, pale luminous skin, enigmatic gaze, antique silver jewelry, "
            "green smoke and floating embers, painterly black-red-gold palette, dramatic rim light, "
            "both hands separated and visible, close diagonal composition, dark fantasy anime, "
            "rich brush texture, no text, no child, no teen, no loli"
        ),
    },
    {
        "name": "A3_MYTHIC_COLORLINES",
        "lora": "AnimaMythC0lorL1nes.safetensors",
        "strength": 0.78,
        "seed": 72429103,
        "source": "Civitai model 599757/version 3016131; author colorful-lines Anima style",
        "prompt": (
            "masterpiece, best quality, very aesthetic, one clearly adult East Asian fantasy woman "
            "age 28, solo, full curvy adult figure, iridescent translucent blue and coral drapery, "
            "reclining on a pearl shell throne above a luminous sea, flowing black hair, warm brown "
            "eyes, opal and gold jewelry, sweeping turquoise-magenta-gold contour lines, prismatic "
            "water reflections, mythic sunrise, elegant separated hands, dynamic three-quarter "
            "composition, vibrant high-detail anime illustration, clean expressive line work, "
            "no text, no child, no teen, no loli"
        ),
    },
    {
        "name": "A4_DRAMATIC_DAPPLED",
        "lora": "S1_Dramatic Lighting Anima_V2.safetensors",
        "strength": 0.82,
        "seed": 72429104,
        "source": "Civitai model 661736/version 3126711 (Anima V2); s1_dram + dappled light",
        "prompt": (
            "masterpiece, best quality, very aesthetic, s1_dram, dappled light, one clearly adult "
            "East Asian woman age 28, solo, voluptuous graceful adult figure, ivory silk gown with "
            "a daring open neckline, seated beside tropical leaves in a glass conservatory, glossy "
            "black hair, pearl earrings, soft direct gaze, broken shafts of late-afternoon sunlight "
            "across face and body, deep leaf shadows, warm gold highlights and cool green ambient "
            "fill, hands placed separately, cinematic close three-quarter anime portrait, refined "
            "skin and fabric rendering, no text, no child, no teen, no loli"
        ),
    },
]

NEG = (
    "lowres, bad quality, worst quality, bad anatomy, bad hands, extra hands, extra fingers, "
    "fused fingers, missing fingers, extra limbs, duplicate person, disembodied limbs, text, "
    "watermark, logo, child, teen, loli, flat lighting, muddy colors, blurry face"
)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def api(path, payload=None, timeout=30):
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(SERVER + path, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
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
        raise RuntimeError(json.dumps(queued["node_errors"], ensure_ascii=False))
    prompt_id = queued["prompt_id"]
    while time.time() - started < 480:
        entry = api("/history/" + prompt_id, timeout=10).get(prompt_id)
        if entry and entry.get("status", {}).get("completed"):
            files = [im["filename"] for out in entry.get("outputs", {}).values() for im in out.get("images", [])]
            return round(time.time() - started, 1), files[0]
        if entry and entry.get("status", {}).get("status_str") == "error":
            raise RuntimeError(json.dumps(entry["status"], ensure_ascii=False))
        time.sleep(2)
    raise TimeoutError("eight-minute cap")


def anima_graph(item):
    graph = read(ANIMA_SOURCE)
    graph["1"]["inputs"]["unet_name"] = "anima_baseV10.safetensors"
    graph["2"]["inputs"]["lora_name"] = item["lora"]
    graph["2"]["inputs"]["strength_model"] = item["strength"]
    graph["7"]["inputs"]["text"] = item["prompt"]
    graph["8"]["inputs"].update({"width": 768, "height": 1152})
    graph["17"]["inputs"]["seed"] = item["seed"]
    graph["17"]["inputs"].update({"steps": 32, "cfg": 3, "sampler_name": "er_sde", "scheduler": "simple"})
    graph["15"]["inputs"]["filename_prefix"] = "STYLEX-" + item["name"]
    return graph


def wai_graph():
    graph = read(ONEOBS_SOURCE)
    graph["1"]["inputs"]["ckpt_name"] = "waiIllustriousSDXL_v170.safetensors"
    graph["2"]["inputs"]["text"] = (
        "masterpiece, best quality, amazing quality, explicit, aged up, mature female, 1girl, "
        "solo, clearly adult East Asian woman age 29, voluptuous curvy adult body, long black hair "
        "with soft bangs, warm brown eyes, teasing confident smile, sheer black-and-red lace robe "
        "open over her body, reclining sideways on a luxurious red velvet sofa, pearl and ruby "
        "jewelry, left hand resting on her thigh, right hand resting separately on the sofa back, "
        "warm chandelier key light, cool moonlit window rim, detailed eyes and hair, smooth clean "
        "coloring, high-detail adult anime illustration, close three-quarter composition"
    )
    graph["3"]["inputs"]["text"] = NEG + ", sketch, censor"
    graph["4"]["inputs"].update({"width": 896, "height": 1216})
    graph["6"]["inputs"].update({
        "seed": 72429105, "steps": 28, "cfg": 6,
        "sampler_name": "euler_ancestral", "scheduler": "normal"
    })
    graph["8"]["inputs"]["filename_prefix"] = "STYLEX-A5_WAI17_CLEAN_ADULT"
    return graph


def jobs():
    rows = [(x["name"], x["source"], anima_graph(x)) for x in ANIMA_STYLES]
    rows.append(("A5_WAI17_CLEAN_ADULT", "Civitai model 827184/version 2883731; author v17 settings", wai_graph()))
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    try:
        for index, (name, source, graph) in enumerate(jobs(), 1):
            workflow = OUT / f"{name}.json"
            workflow.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"event": "starting", "index": index, "name": name}), flush=True)
            server("stop")
            server("start")
            elapsed, filename = queue(graph)
            result = gate.evaluate(IMAGES / filename)
            row = {
                "index": index, "name": name, "source": source, "elapsed_s": elapsed,
                "image": filename, "technical_pass": result["pass"],
                "gate": json.dumps(result, ensure_ascii=False), "workflow": str(workflow),
            }
            results.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    finally:
        server("stop")
        if results:
            with (OUT / "results.csv").open("w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.DictWriter(handle, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)


if __name__ == "__main__":
    main()
