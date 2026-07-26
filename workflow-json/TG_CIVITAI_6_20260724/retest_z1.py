import json
import importlib.util
from pathlib import Path

module_path = Path(__file__).with_name("run_6.py")
spec = importlib.util.spec_from_file_location("run_6", module_path)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

graph = r.load("Z1")
graph["11"] = {
    "class_type": "LoraLoaderModelOnly",
    "inputs": {
        "model": ["1", 0],
        "lora_name": "zit_sda_v1.safetensors",
        "strength_model": 0.49,
    },
}
graph["7"]["inputs"].update({"model": ["11", 0], "shift": 3})
graph["6"]["inputs"].update({"width": 640, "height": 960})
graph["8"]["inputs"].update(
    {
        "steps": 9,
        "cfg": 1,
        "sampler_name": "dpmpp_2m_sde",
        "scheduler": "beta",
    }
)
graph["4"]["inputs"]["text"] = (
    "Premium bright full-length editorial nude photograph, one clearly adult Vietnamese "
    "woman age 27, solo, completely nude, youthful soft oval adult face, long natural dark "
    "hair, healthy voluptuous curvy adult figure, large natural breasts and adult pubic "
    "anatomy visible, standing straight in a relaxed slight three-quarter pose, both arms "
    "hanging naturally at her sides, exactly two complete hands separated and fully visible, "
    "all fingers natural, both feet visible, coherent natural adult anatomy, bright diffused "
    "morning window light, clean white bounce fill, luminous neutral-warm skin, fine pores "
    "and peach fuzz, subtle blush, crisp eyes, 70mm lens, uncluttered pale studio, no props, "
    "no writing, no watermark, no child, no teen, no extra hands, no extra limbs"
)
r.set_seed(graph, 72426137)
graph["10"]["inputs"]["filename_prefix"] = "TGCIV6-Z1B_MOODY_SDA49_CLEANPOSE"
workflow = r.save_graph("Z1B_MOODY_SDA49_CLEANPOSE", graph)

try:
    r.server("stop")
    r.server("start")
    elapsed, filename = r.queue(graph)
    result = r.gate.evaluate(r.IMAGES / filename)
    print(
        json.dumps(
            {
                "name": "Z1B_MOODY_SDA49_CLEANPOSE",
                "elapsed_s": elapsed,
                "image": filename,
                "technical_pass": result["pass"],
                "gate": result,
                "workflow": str(workflow),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
finally:
    r.server("stop")
