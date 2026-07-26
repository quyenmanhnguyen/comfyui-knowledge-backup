import json
import time
import uuid
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(r"C:\AI\workflows\MOODY_REALTIME_BATCH8_20260726")
OUTDIR = Path(r"C:\AI\ComfyUI\output")
SERVER = "http://127.0.0.1:8188"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_api(data, name):
    ROOT.mkdir(parents=True, exist_ok=True)
    path = ROOT / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def set_first_text(data, text):
    for node in data.values():
        if isinstance(node, dict) and node.get("class_type") == "CLIPTextEncode":
            inp = node.get("inputs", {})
            old = str(inp.get("text", "")).lower()
            if "lowres" not in old and "worst quality" not in old:
                inp["text"] = text
                return
    raise RuntimeError("positive CLIPTextEncode not found")


def set_negative(data, extra):
    for node in data.values():
        if isinstance(node, dict) and node.get("class_type") == "CLIPTextEncode":
            inp = node.get("inputs", {})
            old = str(inp.get("text", ""))
            low = old.lower()
            if "lowres" in low or "worst quality" in low:
                inp["text"] = (old.rstrip() + ", " + extra).strip(", ")
                return


def set_seed_prefix(data, seed, prefix):
    for node in data.values():
        if isinstance(node, dict):
            inp = node.get("inputs", {})
            if node.get("class_type") == "KSampler":
                inp["seed"] = seed
            if node.get("class_type") == "SaveImage":
                inp["filename_prefix"] = prefix


def queue(path):
    prompt = json.loads(Path(path).read_text(encoding="utf-8"))
    req = json.dumps({"prompt": prompt, "client_id": str(uuid.uuid4())}).encode("utf-8")
    r = urllib.request.Request(SERVER + "/prompt", data=req, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["prompt_id"]


def wait(prompt_id, timeout=260):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen(SERVER + f"/history/{prompt_id}", timeout=10) as resp:
                hist = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError:
            time.sleep(2)
            continue
        item = hist.get(prompt_id)
        if item:
            status = item.get("status", {})
            images = []
            for out in item.get("outputs", {}).values():
                if isinstance(out, dict):
                    images.extend(out.get("images", []))
            return {
                "state": "complete" if status.get("completed") else status.get("status_str", "done"),
                "elapsed": round(time.time() - t0, 1),
                "images": [img.get("filename") for img in images if img.get("filename")],
                "status": status,
            }
        time.sleep(2)
    return {"state": "timeout", "elapsed": round(time.time() - t0, 1), "images": []}


z_moody = r"C:\AI\workflows\ZIMAGE_FINAL10_MAIN_20260725\MAIN_ZIMAGE_MOODY_RES2S.json"
z_diving = r"C:\AI\workflows\ZIMAGE_FINAL10_MAIN_20260725\01_Z1_DIVING_RES2S_SFW.json"
z_beyond = r"C:\AI\workflows\ZIMAGE_FINAL10_MAIN_20260725\03_Z2_BEYOND_RES2S_SFW.json"
sdxl_rimix = r"C:\AI\workflows\TELEGRAM_PHOTO_DIRECTION_20260726\TG_SDXL_RIMIX065_WINDOW_CINEMATIC.json"
oneobs = r"C:\AI\workflows\TG_CIVITAI_ADV_CINEMATIC_20260724\S4_ONEOBSESSION_CINEMATIC_NSFW.json"
anima = r"C:\AI\workflows\TELEGRAM_PHOTO_DIRECTION_20260726\TG_ANIMA_RIMIX_ALPHA_LAYERED_CINEMATIC.json"

z_prompt_1 = (
    "Premium intimate editorial photograph, waist-up to mid-thigh composition, one clearly adult Vietnamese woman age 29, "
    "soft oval youthful face, natural brown eyes, relaxed confident direct gaze, long black hair with airy strands, "
    "reclining on a pale cream sofa near a tall rainy blue-hour window, warm lamp glow behind her, pearl necklace and translucent ivory silk draped across her shoulders and torso, "
    "voluptuous soft-curvy figure, luminous neutral-warm skin with fine pores and peach fuzz, subtle natural blush, smooth highlight roll-off, "
    "her left hand rests open on the sofa cushion, her right hand rests relaxed on her thigh, separated fingers, no hidden hands, "
    "85mm lens, shallow depth of field, clean white bounce fill, cinematic rain bokeh, realistic hair, fabric and skin texture"
)
z_prompt_2 = (
    "Bright clean studio-window glamour photograph, one clearly adult East Asian woman age 30, close three-quarter seated pose on a white bed, "
    "fresh youthful rounded face, calm inviting expression, glossy black hair falling over one shoulder, full soft figure, "
    "open white satin shirt loosely draped, elegant pearl earrings, warm morning light through sheer curtains, pale walls, soft cream bedding, "
    "both hands visible and separated: left hand lightly holds the bed sheet beside her hip, right hand rests on the pillow, natural fingers, "
    "luminous fair neutral skin, fine pores, tiny peach fuzz, gentle blush, realistic chest/shoulder anatomy, 85mm portrait lens, soft background blur"
)
z_prompt_3 = (
    "Natural fine-art boudoir photograph, one clearly adult Southeast Asian woman age 31, standing near a large rain-streaked window, "
    "youthful but realistic face, slight smile, direct eye contact, dark flowing hair, fuller hips and soft waist, "
    "minimal cream silk wrap, warm lamp and cool blue rim light, pale sofa in background, clean uncluttered room, "
    "her left hand touches the window frame, her right hand rests at her waist, exact two hands visible, separated fingers, "
    "neutral-warm skin with visible pores and tonal variation, no waxy blur, realistic fabric folds, 70mm lens, shallow depth of field"
)

anime_prompt = (
    "masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, depth of field, dynamic angle, adult woman age 28, "
    "semi-real anime glamour illustration, soft oval face, black hair, brown eyes, emotional direct gaze, voluptuous soft-curvy figure, "
    "pale ornate sofa beside a rainy blue window, warm bedside lamp, translucent ivory silk, pearls, glossy luminous skin, "
    "her left hand on the left cushion, her right hand relaxed on her thigh, separated fingers, no foreground hands, cinematic blue and gold lighting"
)
anime_prompt_2 = (
    "masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, adult woman age 29, "
    "bright elegant semi-real anime portrait, full soft-curvy body, youthful mature face, long black hair with bangs, brown expressive eyes, "
    "kneeling sideways on a white chaise lounge, black lace and pale silk fabric, pearl earrings, rain bokeh window, warm lamp, cool rim light, "
    "one hand rests on the chaise arm, the other hand holds a silk edge near her hip, separated fingers, smooth glossy skin, rich hair detail"
)
neg_extra = "child, teen, loli, young-looking, extra hands, disembodied hands, pov hands, extra limbs, fused fingers, malformed eyes, crossed eyes, bad face, waxy skin, oil painting, smeared skin, fake text"

tasks = [
    ("MRB8-01_Z_MOODY_SOFA_BLUE", z_moody, z_prompt_1, 72627101),
    ("MRB8-02_Z_MOODY_WHITE_BED", z_moody, z_prompt_2, 72627102),
    ("MRB8-03_Z_DIVING_WINDOW_WRAP", z_diving, z_prompt_3, 72627103),
    ("MRB8-04_Z_BEYOND_NATURAL_SOFA", z_beyond, z_prompt_1, 72627104),
    ("MRB8-05_SDXL_RIMIX_BLUE_SOFA", sdxl_rimix, anime_prompt, 72627105),
    ("MRB8-06_SDXL_RIMIX_CHAISE", sdxl_rimix, anime_prompt_2, 72627106),
    ("MRB8-07_ONEOBS_LOCKED_VARIANT", oneobs, anime_prompt, 72627107),
    ("MRB8-08_ANIMA_RIMIX_ALPHA", anima, anime_prompt_2, 72627108),
]


def build():
    built = []
    for prefix, src, prompt, seed in tasks:
        data = load(src)
        set_first_text(data, prompt)
        set_negative(data, neg_extra)
        set_seed_prefix(data, seed, prefix)
        built.append(save_api(data, prefix + ".json"))
    return built


def run_all(paths):
    results = []
    for path in paths:
        prefix = path.stem
        print("QUEUE", prefix, flush=True)
        try:
            pid = queue(path)
            res = wait(pid)
            res.update({"workflow": str(path), "prefix": prefix, "prompt_id": pid})
        except Exception as exc:
            res = {"workflow": str(path), "prefix": prefix, "state": "error", "elapsed": 0, "images": [], "error": type(exc).__name__ + ": " + str(exc)}
        results.append(res)
        (ROOT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(res, ensure_ascii=False), flush=True)
    return results


if __name__ == "__main__":
    paths = build()
    run_all(paths)
