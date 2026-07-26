# Ri-mix Style LoRA — corrected workflow

This folder is for the 663.98 MiB `rimixxO2.safetensors` Style LoRA, not the separate Ri-mix alpha Anima checkpoint.

## Author-native Illustrious preset

- Base: `aMixIllustrious_aMix.safetensors`
- LoRA: `rimixxO2.safetensors`
- LoRA strength: 1.2
- Clip skip: 2
- Sampler: Euler ancestral (`Euler a`)
- Scheduler: normal/automatic
- Steps: 30
- CFG: 6
- Resolution: 768x1152
- No upscale or detailer in the native validation graph

The LoRA contains 2,250 SDXL UNet LoRA tensors and no text-encoder tensors. Its metadata declares `stable-diffusion-xl-v1-base/lora`, so it must not be loaded directly into an Anima diffusion graph.

The separate prior file `riMixIllustriousAnima_riMixAnima.safetensors` is a full Anima checkpoint and remains a different valid resource.
