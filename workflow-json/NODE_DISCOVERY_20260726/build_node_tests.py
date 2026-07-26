import json
from pathlib import Path

ROOT = Path(r"C:\AI\workflows\NODE_DISCOVERY_20260726")
ROOT.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "Premium adult glamour photograph, one clearly adult Vietnamese woman age 30, close three-quarter seated pose on a pale cream sofa near a rainy blue-hour window, "
    "soft oval youthful face, natural brown eyes, relaxed direct gaze, long black hair with airy strands, voluptuous soft-curvy figure, translucent ivory silk and pearl earrings, "
    "warm lamp glow behind her and cool blue window rim light, clean white bounce fill on the face, luminous neutral-warm skin with fine pores, peach fuzz and subtle tonal variation, "
    "her left hand rests open on the left sofa cushion, her right hand rests relaxed on her thigh, separated natural fingers, no hidden hands, "
    "85mm portrait lens, shallow depth of field, realistic hair, skin and fabric texture"
)

NEG = (
    "child, teen, loli, young-looking, bad face, malformed eyes, crossed eyes, old face, grey skin, waxy skin, oil painting, smeared skin, "
    "bad anatomy, bad hands, extra hands, disembodied hands, pov hands, extra fingers, fused fingers, missing fingers, extra limbs, fake text, watermark"
)


def save(name, graph):
    p = ROOT / f"{name}.json"
    p.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def z_raw_graph(prefix, seed, detail_amount=None, shift=5, scheduler="beta", steps=9, lora=None, lora_strength=0.12):
    graph = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "moodyProMix_zitV13.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "cpu"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": shift}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": PROMPT}},
        "6": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["5", 0]}},
        "7": {"class_type": "EmptyLatentImage", "inputs": {"width": 576, "height": 800, "batch_size": 1}},
        "8": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "9": {"class_type": "BasicGuider", "inputs": {"model": ["4", 0], "conditioning": ["5", 0]}},
        "10": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "11": {"class_type": "BasicScheduler", "inputs": {"model": ["4", 0], "scheduler": scheduler, "steps": steps, "denoise": 1.0}},
        "12": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["8", 0], "guider": ["9", 0], "sampler": ["10", 0], "sigmas": ["11", 0], "latent_image": ["7", 0]}},
        "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["3", 0]}},
        "14": {"class_type": "SaveImage", "inputs": {"images": ["13", 0], "filename_prefix": prefix}},
    }
    if detail_amount is not None:
        graph["15"] = {"class_type": "DetailDaemonSamplerNode", "inputs": {
            "sampler": ["10", 0], "detail_amount": detail_amount, "start": 0.18, "end": 0.72, "bias": 0.45,
            "exponent": 1.0, "start_offset": 0.0, "end_offset": 0.0, "fade": 0.25, "smooth": True, "cfg_scale_override": 0
        }}
        graph["12"]["inputs"]["sampler"] = ["15", 0]
    if lora:
        graph["16"] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": lora, "strength_model": lora_strength}}
        graph["4"]["inputs"]["model"] = ["16", 0]
    return graph


def z_eulerflow_dd(prefix, seed, detail_amount=0.12):
    p = Path(r"C:\AI\workflows\ZIMAGE_FINAL10_MAIN_20260725\FAST_ZIMAGE_MOODY_EULER_H4.json")
    g = json.loads(p.read_text(encoding="utf-8"))
    g["4"]["inputs"]["text"] = PROMPT
    g["12"]["inputs"]["noise_seed"] = seed
    g["10"]["inputs"]["filename_prefix"] = prefix
    # Insert DetailDaemon between KSamplerSelect and SamplerCustomAdvanced.
    g["30"] = {"class_type": "DetailDaemonSamplerNode", "inputs": {
        "sampler": ["14", 0], "detail_amount": detail_amount, "start": 0.20, "end": 0.75, "bias": 0.45,
        "exponent": 1.0, "start_offset": 0.0, "end_offset": 0.0, "fade": 0.25, "smooth": True, "cfg_scale_override": 0
    }}
    g["16"]["inputs"]["sampler"] = ["30", 0]
    return g


def sdxl_lora_variant(prefix, seed):
    p = Path(r"C:\AI\workflows\TELEGRAM_PHOTO_DIRECTION_20260726\TG_SDXL_RIMIX065_WINDOW_CINEMATIC.json")
    g = json.loads(p.read_text(encoding="utf-8"))
    # Add a second LoRA for cinematic/detail style after the existing Ri-mix loader.
    # Existing nodes: 1 checkpoint, 2 lora, 3 clip skip, 4 positive, 5 negative, 7 sampler.
    g["20"] = {"class_type": "LoraLoader", "inputs": {
        "model": ["2", 0], "clip": ["2", 1],
        "lora_name": "cinematic photography detailed illu xl v5.safetensors",
        "strength_model": 0.25, "strength_clip": 0.25
    }}
    g["3"]["inputs"]["clip"] = ["20", 1]
    g["7"]["inputs"]["model"] = ["20", 0]
    g["4"]["inputs"]["text"] = (
        "masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, adult woman age 29, semi-real anime editorial glamour, "
        "soft oval face, brown eyes, direct emotional gaze, long black hair, voluptuous soft-curvy figure, ivory silk, pearls, pale sofa, rainy blue window, warm lamp, "
        "her left hand on sofa cushion, her right hand relaxed on thigh, separated fingers, cinematic blue and gold lighting, rich hair detail, clean fabric texture"
    )
    g["5"]["inputs"]["text"] += ", malformed eyes, waxy skin, oil painting, extra hands, pov hands"
    g["7"]["inputs"]["seed"] = seed
    g["9"]["inputs"]["filename_prefix"] = prefix
    return g


tests = [
    ("NDISC-01_Z_RAW_EULER_BETA9_SHIFT5", z_raw_graph("NDISC-01_Z_RAW_EULER_BETA9_SHIFT5", 72628101)),
    ("NDISC-02_Z_RAW_EULER_DD018", z_raw_graph("NDISC-02_Z_RAW_EULER_DD018", 72628102, detail_amount=0.18)),
    ("NDISC-03_Z_EULERFLOW_DD012", z_eulerflow_dd("NDISC-03_Z_EULERFLOW_DD012", 72628103)),
    ("NDISC-04_Z_REALSNAP_LORA012", z_raw_graph("NDISC-04_Z_REALSNAP_LORA012", 72628104, detail_amount=None, lora="RealisticSnapshot-Zimage-Turbov5.safetensors", lora_strength=0.12)),
    ("NDISC-05_Z_RENDERDETAIL_LORA010", z_raw_graph("NDISC-05_Z_RENDERDETAIL_LORA010", 72628105, detail_amount=None, lora="rendering_detailer_base10-000400.safetensors", lora_strength=0.10)),
    ("NDISC-06_SDXL_RIMIX_CINDETAIL025", sdxl_lora_variant("NDISC-06_SDXL_RIMIX_CINDETAIL025", 72628106)),
]

for name, graph in tests:
    print(save(name, graph))
