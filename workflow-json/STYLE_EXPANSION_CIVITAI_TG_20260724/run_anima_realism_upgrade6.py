import csv
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("base_runner", HERE / "run_styles.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

SOURCE = HERE / "B2_ANIMA_REALISM_V2.json"
PREFIX = "ARUP6-"
NEG = (
    "lowres, worst quality, blurry, soft focus, waxy skin, plastic skin, airbrushed skin, "
    "beauty filter, over-smoothed face, flat skin, oily highlights, overexposed skin, "
    "bad anatomy, malformed chest, asymmetrical breasts, deformed hips, malformed buttocks, "
    "bad hands, extra hands, extra fingers, fused fingers, missing fingers, extra limbs, "
    "duplicate person, cropped head, cropped torso, disembodied limbs, text, watermark, logo, "
    "child, teen, underage, loli"
)

COMMON = (
    "masterpiece, best quality, very aesthetic, semi-real anime editorial portrait, one clearly "
    "adult East Asian woman age 29, solo, soft oval adult face, long natural black hair, warm "
    "brown eyes, confident relaxed expression, voluptuous balanced adult proportions, full natural "
    "bust, defined waist, rounded hips and full shapely buttocks, luminous neutral-warm skin with "
    "fine pores, peach fuzz, subtle tonal variation and natural blush, realistic hair strands, "
    "clean bright diffused window key, broad white bounce fill, restrained warm rim light, "
    "smooth highlight roll-off, detailed satin texture, coherent anatomy, exactly two hands"
)

JOBS = [
    {
        "name": "01_SEATED_THREEQUARTER",
        "seed": 72429301,
        "prompt": (
            f"{COMMON}, seated sideways on an ivory chaise, torso gently turned toward camera, "
            "one hand resting on her upper thigh and the other on the sofa back, champagne satin "
            "halter dress with a deep but elegant neckline, fitted waist and draped skirt tracing "
            "the hips, head-to-mid-thigh three-quarter framing, 65mm lens, face chest waist hips "
            "and upper thighs all visible, bright luxury apartment, no text"
        ),
    },
    {
        "name": "02_STANDING_BODYCON",
        "seed": 72429302,
        "prompt": (
            f"{COMMON}, standing in a relaxed contrapposto beside a tall bright window, one hand "
            "on her waist and the other hanging clearly beside her thigh, pearl-white fitted satin "
            "dress with open neckline and body-skimming silhouette, front three-quarter angle, "
            "head-to-knee fashion framing, 70mm lens, clear bust waist hip contour, no text"
        ),
    },
    {
        "name": "03_REAR_THREEQUARTER",
        "seed": 72429303,
        "prompt": (
            f"{COMMON}, standing with her back three-quarter to camera and looking gently over her "
            "shoulder, both hands separately touching a marble balcony rail, backless pale-blue "
            "satin evening dress fitted naturally across the waist and rounded hips, tasteful low "
            "back, head-to-mid-thigh framing, 65mm lens, face profile back waist hips and buttocks "
            "clearly readable, bright skyline bokeh, no text"
        ),
    },
    {
        "name": "04_RECLINED_DIAGONAL",
        "seed": 72429304,
        "prompt": (
            f"{COMMON}, reclining diagonally on a cream sofa with shoulders raised, knees angled "
            "away from camera, left hand on the left cushion and right hand on her right thigh, "
            "ivory silk slip dress with softly draped neckline and fitted hip line, head-to-knee "
            "diagonal composition, 60mm lens, chest waist hips and thighs visible without extreme "
            "foreshortening, airy penthouse morning light, no text"
        ),
    },
    {
        "name": "05_KNEELING_SIDE",
        "seed": 72429305,
        "prompt": (
            f"{COMMON}, elegant side kneeling pose on a wide ivory daybed, upright torso, hips "
            "resting naturally above the heels, both hands separated on her thighs, pale rose "
            "satin wrap dress with open neckline and fitted waist, side three-quarter view, "
            "head-to-knee framing, 70mm lens, clean breast waist hip and buttock silhouette, "
            "soft curtains and pearl-white room, no text"
        ),
    },
    {
        "name": "06_CLOSE_CURVE_BALANCED",
        "seed": 72429306,
        "prompt": (
            f"{COMMON}, seated at the edge of a cream armchair with torso turned and hips angled "
            "opposite, left hand on the left armrest and right hand resting above her knee, black "
            "satin corset-style evening top under an open ivory silk robe with matching fitted "
            "skirt, head-to-upper-thigh framing, 75mm lens, detailed face neckline chest waist "
            "and rounded hip line, high-key editorial studio, no text"
        ),
    },
]


def make_graph(item):
    graph = json.loads(SOURCE.read_text(encoding="utf-8-sig"))
    graph["2"]["inputs"].update({"lora_name": "realism-anima-v2.safetensors", "strength_model": 0.50})
    graph["7"]["inputs"]["text"] = item["prompt"]
    graph["8"]["inputs"].update({"width": 768, "height": 1152})
    graph["17"]["inputs"].update({
        "seed": item["seed"], "steps": 32, "cfg": 3,
        "sampler_name": "er_sde", "scheduler": "simple",
    })
    graph["15"]["inputs"]["filename_prefix"] = PREFIX + item["name"]
    # B2 inherited no dedicated negative encoder, so append exclusions to the
    # positive instruction as a compact natural-language constraint.
    graph["7"]["inputs"]["text"] += ". Exclude: " + NEG
    return graph


def main():
    results = []
    try:
        for index, item in enumerate(JOBS, 1):
            graph = make_graph(item)
            workflow = HERE / f"ARUP6_{item['name']}.json"
            workflow.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"event": "starting", "index": index, "name": item["name"]}), flush=True)
            base.server("stop")
            base.server("start")
            elapsed, filename = base.queue(graph)
            gate = base.gate.evaluate(base.IMAGES / filename)
            row = {
                "index": index, "name": item["name"], "seed": item["seed"],
                "elapsed_s": elapsed, "image": filename, "technical_pass": gate["pass"],
                "gate": json.dumps(gate, ensure_ascii=False), "workflow": str(workflow),
            }
            results.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    finally:
        base.server("stop")
        if results:
            with (HERE / "results_anima_realism_upgrade6.csv").open(
                "w", newline="", encoding="utf-8-sig"
            ) as handle:
                writer = csv.DictWriter(handle, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)


if __name__ == "__main__":
    main()
