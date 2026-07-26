import importlib.util
import json
from pathlib import Path

ROOT = Path(r"C:\AI")
HERE = Path(__file__).parent
RUNNER = ROOT / r"workflows\STYLE_EXPANSION_CIVITAI_TG_20260724\run_styles.py"

spec = importlib.util.spec_from_file_location("base_runner", RUNNER)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

POSITIVE = (
    "masterpiece, best quality, very aesthetic, detailed, high detail, depth of field, "
    "one clearly adult East Asian woman age 28, solo, elegant youthful adult face, warm brown eyes, "
    "long glossy black hair, soft curvy adult proportions, standing at a three-quarter angle beside "
    "a tall apartment window, fitted ivory satin dress beneath a tailored black jacket, her left hand "
    "resting lightly on the window frame, her right hand relaxed separately beside her thigh, exactly "
    "two complete hands visible, warm morning window light, clean neutral face fill, subtle cool rim, "
    "refined skin shading, detailed satin and hair, cinematic vertical anime illustration, clean eyes, "
    "natural fingers, no text, no watermark, aged up, adult"
)

GRAPH = {
    "1": {"class_type": "UNETLoader", "inputs": {
        "unet_name": "riMixIllustriousAnima_riMixAnima.safetensors",
        "weight_dtype": "default"}},
    "2": {"class_type": "CLIPLoader", "inputs": {
        "clip_name": "qwen_3_06b_base.safetensors",
        "type": "stable_diffusion", "device": "default"}},
    "3": {"class_type": "VAELoader", "inputs": {
        "vae_name": "qwen_image_vae.safetensors"}},
    "4": {"class_type": "CLIPTextEncode", "inputs": {
        "clip": ["2", 0], "text": POSITIVE}},
    "5": {"class_type": "ConditioningZeroOut", "inputs": {
        "conditioning": ["4", 0]}},
    "6": {"class_type": "EmptyLatentImage", "inputs": {
        "width": 768, "height": 1152, "batch_size": 1}},
    "7": {"class_type": "KSampler", "inputs": {
        "model": ["1", 0], "positive": ["4", 0], "negative": ["5", 0],
        "latent_image": ["6", 0], "seed": 72525001, "steps": 32, "cfg": 3,
        "sampler_name": "er_sde", "scheduler": "simple", "denoise": 1}},
    "8": {"class_type": "VAEDecode", "inputs": {
        "samples": ["7", 0], "vae": ["3", 0]}},
    "9": {"class_type": "SaveImage", "inputs": {
        "images": ["8", 0], "filename_prefix": "RIMIXA-AUTHOR32-SFW"}},
}


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    workflow = HERE / "RIMIX_ALPHA_ANIMA_AUTHOR32.json"
    workflow.write_text(json.dumps(GRAPH, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        base.server("stop")
        base.server("start")
        elapsed, filename = base.queue(GRAPH)
        gate = base.gate.evaluate(base.IMAGES / filename)
        result = {"elapsed_s": elapsed, "image": filename, "gate": gate,
                  "workflow": str(workflow)}
        (HERE / "result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False), flush=True)
    finally:
        base.server("stop")


if __name__ == "__main__":
    main()
