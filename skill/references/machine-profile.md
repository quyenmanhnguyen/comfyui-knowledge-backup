# Verified machine profile

Last verified: 2026-07-19.

## Hardware and runtime

- GPU: AMD Radeon RX 7800 XT, 16 GB VRAM.
- Actual architecture: `gfx1101`. Do not call this GPU `gfx1103`.
- RAM: 32 GB.
- CPU: Intel Core i7-14700KF.
- OS/runtime: Windows native ROCm/TheRock path.
- Python: 3.12.10 embedded runtime at `C:\AI\python_embeded\python.exe`.
- Torch: `2.9.1+rocm7.2.1`.
- ComfyUI: `C:\AI\ComfyUI`, git tag `v0.28.0` with local modifications.
- Custom-node packs: 46 directories at last count.

## Model paths

- Diffusion models: `C:\AI\ComfyUI\models\diffusion_models`.
- Checkpoints: `C:\AI\ComfyUI\models\checkpoints`.
- LoRAs: `C:\AI\ComfyUI\models\loras`.
- Text encoders: `C:\AI\ComfyUI\models\text_encoders`.
- VAE: `C:\AI\ComfyUI\models\vae`.
- Outputs: `C:\AI\ComfyUI\output`.
- Workflows and reports: `C:\AI\workflows`.

## Verified startup

`C:\AI\START_COMFYUI.ps1` currently:

- Detects API availability and port 8188 conflicts.
- Stops stale matching ComfyUI processes.
- Writes stdout/stderr logs under `C:\AI\logs`.
- Sets `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1`.
- Launches with `--use-pytorch-cross-attention` and no automatic browser launch.

The PyTorch cross-attention choice is locally stable and is also consistent with a Windows ROCm performance report. Do not replace it without A/B testing.

## Benign and actionable warnings

- `[WARNING] offload-arch failed`: currently benign; Torch still detects RX 7800 XT and `gfx1101`.
- TIPO-KGen may repeatedly attempt `llama-cpp-python` installation and add startup delay. Disable only if confirmed unused.
- Forty-six node packs increase startup time and upgrade risk. Prune only after dependency mapping; do not bulk-delete.
- Z-Image model files around 6–12 GB may log BF16 compute and about 11.7 GB loaded. File quantization does not guarantee low compute VRAM.
