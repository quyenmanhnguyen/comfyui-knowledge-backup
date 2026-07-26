import csv
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("base_runner", HERE / "run_styles.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

ROOT = Path(r"C:\AI")
ANIMA_SOURCE = ROOT / r"workflows\TG_CIVITAI_ADV_CINEMATIC_20260724\A3_ANIMA_RIMIX_ALPHA_SFW.json"
ILLUST_SOURCE = ROOT / r"workflows\TG_CIVITAI_ADV_CINEMATIC_20260724\S4_ONEOBSESSION_CINEMATIC_NSFW.json"

NEG = (
    "lowres, bad quality, worst quality, bad anatomy, bad hands, extra hands, extra fingers, "
    "fused fingers, missing fingers, extra limbs, duplicate person, disembodied limbs, text, "
    "watermark, logo, signature, child, teen, loli, flat lighting, muddy colors, blurry face"
)

ANIMA = [
    {
        "name": "B1_MYTHIC_PORTRAIT",
        "lora": "AnimaMythP0rtr4itStyleV1.safetensors",
        "strength": 0.82,
        "seed": 72429201,
        "sampler": "er_sde",
        "cfg": 3,
        "source": "Civitai model 599757/version 3084665; author trigger mythp0rt, 0.6-1.0",
        "prompt": (
            "masterpiece, best quality, very aesthetic, mythp0rt, high quality semi-real fantasy "
            "portrait of one clearly adult East Asian woman age 28, solo, voluptuous graceful figure, "
            "long flowing black hair, luminous warm fair skin, gentle confident gaze, ivory and "
            "turquoise translucent silk gown, pearl crown and opal necklace, reclining on a pale "
            "marble balcony above a bright enchanted garden, soft rose-gold sunrise, cool sky fill, "
            "delicate painterly skin, rich fabric folds, hands placed separately, close three-quarter "
            "composition, elegant fantasy illustration, no text, no child, no teen, no loli"
        ),
    },
    {
        "name": "B2_ANIMA_REALISM_V2",
        "lora": "realism-anima-v2.safetensors",
        "strength": 0.72,
        "seed": 72429202,
        "sampler": "er_sde",
        "cfg": 3,
        "source": "Civitai model 2643318/version 2995972; realism enhancer v2",
        "prompt": (
            "masterpiece, best quality, very aesthetic, realistic, semi-real anime portrait of one "
            "clearly adult East Asian woman age 29, solo, voluptuous natural adult body, glossy black "
            "hair with soft bangs, luminous neutral-warm skin with subtle pores and blush, elegant "
            "cream silk slip dress, seated sideways on a bright ivory sofa near a large window, "
            "soft natural morning light, clean white bounce fill, pearl earrings, separated relaxed "
            "hands, 85mm close three-quarter framing, realistic hair and silk texture, polished but "
            "natural face, no text, no child, no teen, no loli"
        ),
    },
    {
        "name": "B3_BUNNYSLOP_V404",
        "lora": "BunnySlop_v404.safetensors",
        "strength": 0.72,
        "seed": 72429203,
        "sampler": "euler_ancestral",
        "cfg": 4,
        "source": "Civitai model 2613391/version 3126430; author @sl0p, Euler A/simple 32 CFG4",
        "prompt": (
            "masterpiece, best quality, very aesthetic, @sl0p, one clearly adult East Asian woman "
            "age 28, solo, very voluptuous soft-curvy adult figure, long glossy black hair, warm brown "
            "eyes, playful confident smile, open pale-blue satin robe over black lace lingerie, "
            "lounging on a cream bed in a sunlit modern penthouse, large soft natural breasts, full "
            "thighs, luminous fair skin, both hands clearly separated, bright window light and soft "
            "pearl-white fill, clean detailed adult anime illustration, close diagonal composition, "
            "no text, no child, no teen, no loli"
        ),
    },
]

CHECKPOINTS = [
    {
        "name": "B4_HASSAKU_V34",
        "ckpt": "hassakuXLIllustrious_v34.safetensors",
        "seed": 72429204,
        "steps": 30,
        "cfg": 6,
        "source": "Civitai model 140272/version 2615702; author Euler A CFG6, 832x1216",
        "prompt": (
            "1girl, solo, mature female, aged up, clearly adult East Asian woman age 29, curvy, "
            "voluptuous, long black hair, soft bangs, brown eyes, elegant smile, white pearl earrings, "
            "deep-blue silk evening dress with open neckline, seated on an ivory chaise beside a bright "
            "rainy window, warm lamp, cool blue rim light, glossy hair, luminous skin, detailed eyes, "
            "separated hands, close three-quarter portrait, masterpiece, best quality"
        ),
    },
    {
        "name": "B5_COMIX_B3",
        "ckpt": "comix_b3.safetensors",
        "seed": 72429205,
        "steps": 30,
        "cfg": 5.5,
        "source": "Civitai model 2173364/version 2907004; western comic/cel-shaded Illustrious merge",
        "prompt": (
            "1girl, solo, mature female, aged up, clearly adult East Asian heroine age 29, voluptuous "
            "athletic curvy figure, long black hair, confident direct gaze, fitted white-and-gold "
            "superhero bodysuit with deep neckline, standing on a bright art-deco rooftop at sunrise, "
            "one hand on hip and the other resting separately on a marble rail, warm rim light, blue "
            "city shadows, bold clean outlines, rich cel shading, polished western comic cover, "
            "dynamic low angle, masterpiece, best quality, no text"
        ),
    },
]


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def anima_graph(item):
    graph = read(ANIMA_SOURCE)
    graph["1"]["inputs"]["unet_name"] = "anima_baseV10.safetensors"
    graph["2"]["inputs"].update({"lora_name": item["lora"], "strength_model": item["strength"]})
    graph["7"]["inputs"]["text"] = item["prompt"]
    graph["8"]["inputs"].update({"width": 768, "height": 1152})
    graph["17"]["inputs"].update({
        "seed": item["seed"], "steps": 32, "cfg": item["cfg"],
        "sampler_name": item["sampler"], "scheduler": "simple",
    })
    graph["15"]["inputs"]["filename_prefix"] = "STYLEX2-" + item["name"]
    return graph


def checkpoint_graph(item):
    graph = read(ILLUST_SOURCE)
    graph["1"]["inputs"]["ckpt_name"] = item["ckpt"]
    graph["2"]["inputs"]["text"] = item["prompt"]
    graph["3"]["inputs"]["text"] = NEG
    graph["4"]["inputs"].update({"width": 832, "height": 1216})
    graph["6"]["inputs"].update({
        "seed": item["seed"], "steps": item["steps"], "cfg": item["cfg"],
        "sampler_name": "euler_ancestral", "scheduler": "normal",
    })
    graph["8"]["inputs"]["filename_prefix"] = "STYLEX2-" + item["name"]
    return graph


def jobs():
    return (
        [(x["name"], x["source"], anima_graph(x)) for x in ANIMA]
        + [(x["name"], x["source"], checkpoint_graph(x)) for x in CHECKPOINTS]
    )


def main():
    results = []
    try:
        for index, (name, source, graph) in enumerate(jobs(), 1):
            workflow = HERE / f"{name}.json"
            workflow.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"event": "starting", "index": index, "name": name}), flush=True)
            base.server("stop")
            base.server("start")
            elapsed, filename = base.queue(graph)
            result = base.gate.evaluate(base.IMAGES / filename)
            row = {
                "index": index, "name": name, "source": source, "elapsed_s": elapsed,
                "image": filename, "technical_pass": result["pass"],
                "gate": json.dumps(result, ensure_ascii=False), "workflow": str(workflow),
            }
            results.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    finally:
        base.server("stop")
        if results:
            with (HERE / "results_round2.csv").open("w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.DictWriter(handle, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)


if __name__ == "__main__":
    main()
