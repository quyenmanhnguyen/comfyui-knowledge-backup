# NSFW native-detail workflows — 2026-07-26

Target: RX 7800 XT 16 GB, native resolution, no 2x upscale.

## 1. ZIMAGE_MOODY_ADV_NSFW.json

- MoodyPro ZIT v13, `res_2s` / `beta57`
- 576x800, 10 steps, CFG 1, shift 3
- Structured adult editorial prompt with explicit hand ownership, layered light,
  skin texture and compact exclusions
- No LoRA stacking and no regional Z detailer because local testing showed severe
  UNET/Qwen/VAE movement on 16 GB VRAM
- Tested output: `ADVNSFW-Z-MOODY-NATIVE_00001_.png`
- Cold/API elapsed: 91.0 s

## 2. SDXL_INTO_FACE_HAND_NSFW.json

- IntoRealism Ultra SDXL
- 896x1152, DPM++ SDE/Karras, 35 steps, CFG 4.5
- Native image is saved before correction
- Face YOLOv8m: 512 guide, 14 steps, denoise 0.20
- Hand YOLOv9c: 384 guide, 16 steps, denoise 0.24
- Only detected regions are resampled; the full image is never upscaled
- Tested detail output: `ADVNSFW-SDXL-INTO-FACEHAND_00001_.png`
- Cold/API elapsed: 74.3 s

The detail branch can correct an existing visible face or hand. It cannot create
a hand that the base composition hides, so compare the saved BASE and FACEHAND
outputs before keeping the result.
