# SDXL and Illustrious playbook

Use this reference for SDXL, Illustrious, aMix, FabricatedXL, OneObsession, IntoRealism, and RealVis work on this machine.

## Evidence order

1. Inspect user-selected images and embedded PNG metadata.
2. Read `C:\AI\workflows\KEEP_MAIN_20260713` and the latest relevant report.
3. Compare against the reproduced leaders below with the same prompt and seed.
4. Check the exact Civitai model/version by API or SHA256; use local Telegram exports only as secondary evidence.
5. Change one material variable at a time. Do not call a seed or minor prompt rewrite a new workflow.

## Reproduced leaders

### Photoreal: IntoRealism Ultra No-Lightning

- Checkpoint: `intorealismUltra_sdxlV1NoLightning.safetensors`
- Resolution: 896x1152
- Sampler: DPM++ SDE, Karras
- Steps/CFG: 35 / 4.5
- CLIP: connect checkpoint CLIP directly.
- Measured: 56.6 s cold, 48.3 s warm on 2026-07-21.
- Strength: youthful bright editorial realism, natural skin, good SFW and adult figure study.
- Critical guardrail: do not insert `CLIPSetLastLayer(-1)`. It completed without a node error but decoded all-black PNGs in the reproduced test.

### Semi-real anime: aMix + Ri-mix

- Checkpoint: `aMixIllustrious_aMix.safetensors`
- LoRA: `rimixxO2.safetensors`, strength model/CLIP 0.65
- Resolution: 768x1152
- Sampler: Euler ancestral, normal
- Steps/CFG: 30 / 7
- CLIP skip: 2
- Measured: 26.1 s cold, 18.0 s warm.
- Strength: best balance of clean face, mature proportions, warm daylight, and semireal rendering.
- Do not restore historical Ri-mix 1.2 by default; it changes face/style too strongly. Test 0.50/0.65/0.80 as paired A/B only when justified.

### Clean anime: Fabricated XL v7

- Checkpoint: `fabricatedXL_v70.safetensors`
- Resolution: 768x1152
- Sampler: Euler ancestral, normal
- Steps/CFG: 28 / 6
- CLIP skip: 2
- Measured: 26.1 s cold, 16.1 s warm.
- Strength: fast, clean, stable, balanced full-body composition.
- Character: more clearly anime/flat than aMix + Ri-mix.

### Detail/high contrast: OneObsession v23

- Checkpoint: `oneObsession_v23.safetensors`
- Resolution: 832x1216
- Sampler: DPM++ 2M, Karras
- Steps/CFG: 32 / 5.5
- CLIP skip: 2
- Measured: 32.1 s cold, 22.1 s warm.
- Strength: hair, lighting, contrast, expressive face.
- Risk: complex hands near the face. Prompt separated, simple hands; reject intertwined fingers unless visually valid.

### Fast photoreal draft: RealVisXL V5

- Checkpoint: `RealVisXL_V5.0_fp16.safetensors`
- Proven baseline: DPM++ 2M Karras, 42 steps, CFG 4.5, 768x1024.
- Use for fast clean drafts. IntoRealism remains the quality leader for youthful bright skin.

## Prompt grammar

### Illustrious/anime

Use compact comma-separated tags. Start from the author's aMix quality vocabulary:

`masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, depth of field, dynamic angle, adult, aged up`

Then add subject, pose, clothing/figure-study constraint, lighting, and background. Use a compact negative:

`lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, fused fingers, missing fingers, extra limbs, jpeg artifacts, signature, watermark, text, logo, child, teen, loli`

Avoid applying long photoreal prose to Illustrious. Avoid blue/cyan/violet/neon eye terms unless glowing eyes are wanted; previous “laser eyes” were prompt-induced.

### Photoreal SDXL

Use natural-language photographic prose in this order: medium, clearly adult subject and age, face/ethnicity, pose, hands/feet, clothing or figure study, exposure, lens, skin/hair/materials, background. Use fine pores, peach fuzz, subtle tonal variation, neutral-warm skin, bright diffused light, and white bounce fill for the requested youthful clean look.

Do not apply anime CLIP skip, tag piles, FreeU, or LoRA stacks to photoreal checkpoints without an isolated A/B test.

## Visual acceptance

Reject an image even when the API reports success if it has any of these:

- all-black or near-black decoded pixels;
- wrong apparent age, grey/dull skin, waxy blur, harsh aging, or color bleed;
- malformed fingers/feet, merged contacts, implausible pose, or severe crop against the prompt;
- ignored clothing/figure-study constraints or unwanted censorship;
- only a seed change presented as workflow progress.

Record pixel statistics for suspicious black outputs. Visually inspect every promoted SFW/adult-NSFW pair and record why it wins or loses.

## LoRA and node policy

- Treat every LoRA as a possible face/style change, not a free detail improvement.
- Start with the checkpoint-native graph. Add one LoRA at low strength and A/B it.
- Do not add FreeU, Detail Daemon, refiner, hires fix, face detailer, or upscale merely to make a graph look “full.” Add a node only for a reproduced defect and keep it only after visual improvement.
- Restart the ComfyUI process when changing checkpoint families or after suspicious LoRA/VRAM behavior.

## Key artifacts

- Historical source: `C:\AI\workflows\KEEP_MAIN_20260713`
- Rebuild report: `C:\AI\workflows\KEEP_MAIN_SDXL_REBUILD_20260721\REPORT.html`
- Rebuild workflows: `C:\AI\workflows\KEEP_MAIN_SDXL_REBUILD_20260721`
- Prior rebalance report: `C:\AI\workflows\REBAlANCE_SDXL_Z_20260721\REPORT.html`
