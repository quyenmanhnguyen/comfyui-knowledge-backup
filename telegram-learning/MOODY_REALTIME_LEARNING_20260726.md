# Moody Realtime Learning - 2026-07-26

Scope: realtime read-only Telegram scan of `Moody小圆脸同好会`, local Downloads, installed ComfyUI models/LoRAs, and prior local evidence. This is a working note for future workflow selection, not a final model ranking.

## Telegram Moody Scan

- Source: `C:\AI\telegram_client\moody_realtime_scan.json`.
- Group found: `Moody小圆脸同好会`.
- Topics scanned: `model releases`, `Sharing`, `Prompts`, `Q&A`, `English`, and one Chinese prompt-sharing topic.
- Recent messages scanned: 338.
- Useful signal: `Prompts 提示词分享` is the best practical source. It contains long structured prompts, sample media, and reaction signal.
- Limitation: forum-topic message views often return `0` through Telethon. Use reactions, attached files, message recency, topic, and reproducibility instead of treating Telegram view counts as authoritative.

## What To Learn From Moody Prompts

- Use structured scene prose instead of short keyword piles for Z-Image and photoreal SDXL.
- The strongest recurring grammar is:
  1. subject and composition;
  2. clearly adult age and face type;
  3. hair, expression and eye contact;
  4. body silhouette and pose;
  5. exact hand placement;
  6. clothing/fabric or adult fine-art constraints;
  7. scene layers, window, sofa/bed, rain, lamp, reflective materials;
  8. lighting/color grade;
  9. lens/camera distance;
  10. compact exclusions.
- Keep the emotional direction: direct gaze, relaxed confidence, soft inviting expression, rain-blue/cool window plus warm lamp, pale sofa/bed, pearls/jewelry, translucent fabric.
- For anatomy, avoid generic `hands visible`; use spatial ownership: `her left hand rests on the left cushion; her right hand rests on her thigh`, and exclude foreground/POV/disembodied hands.
- Avoid importing the most extreme Telegram prompt details directly. They increase anatomy/crop risk. Convert them into non-graphic adult glamour/fine-art constraints.

## Local Downloads And Model Inventory

- New download: `C:\Users\Admin\Downloads\workflowRAWDetailer_v10ZITEDITION.json`.
  - Contains Z-Image nodes plus `Lora Loader Stack`, `ImageUpscaleWithModel`, `DetailDaemonSamplerNode`, `KSampler`, tiled VAE decode.
  - Treat as research-only. It conflicts with local evidence that full upscale/detail stacks often cause lag, oversharpening, fake texture, or model transfer stalls.
  - If tested, isolate it, disable/remove upscale first, then A/B only the detail/sampler component against `MAIN_ZIMAGE_MOODY_RES2S.json`.
- New/confirmed LoRA: `rimixxO2.safetensors`.
  - This is SDXL/Illustrious Ri-mix Style LoRA, not an Anima diffusion model.
  - Use with `aMixIllustrious_aMix.safetensors`; author-faithful strength 1.2 is strong/glossy, local balanced strength 0.65 is cleaner.
- Installed strong candidates:
  - Z-Image: MoodyPro v13.2, Diving v7, Beyond Reality v3, CyberRealistic v6/v2.
  - SDXL/Illustrious: aMix, OneObsession v23, Hassaku XL Illustrious v3.4, WAI v17, FabricatedXL v7, IntoRealism, RealVisXL.
  - Anima: Ri-mix alpha Anima full diffusion, Moody Anima Mix, Anima base, AnimaYume.
  - Useful LoRAs: Ri-mix alpha LoRA, Anima Myth Portrait/ColorLines, BunnySlop, S1 Dramatic Lighting.

## Recommended Test Shortlist

Do not start from scratch. Use these branches, in this order:

1. Z-Image main photoreal: `ZIMAGE_FINAL10_MAIN_20260725\MAIN_ZIMAGE_MOODY_RES2S.json`.
   - Apply Moody realtime prompt grammar only.
   - Keep 576x800, res_2s/beta57, 10 steps, CFG 1, shift 3.
   - No Z FaceDetailer or Z upscale.
2. Z-Image natural alternative: Beyond/Diving res_2s.
   - Use only if Moody becomes too smooth or too idealized.
   - Prefer simple poses with separated hands.
3. SDXL/Illustrious semi-real anime: aMix + Ri-mix 0.65.
   - Best balanced anime/semi-real default.
   - Use author 1.2 only for stronger glossy style tests.
4. High-impact adult anime: OneObsession v23 locked S4/T2 direction.
   - Use close seated/reclined scenes only.
   - Do not use for wide walking cinematic scenes.
5. Anima HQ cinematic: Ri-mix alpha Anima, ER-SDE/simple, 32 steps, CFG 3.
   - Strong depth and warm/cool cinematic scene layering.
   - Optional targeted face/hand detail is allowed only if native output is already good.

## Avoid

- Do not retry `realism-anima-v2`; user rejected it as plastic/mannequin-like.
- Do not revive gothic/neon/dark/dappled branches as main visual targets.
- Do not use full-image 2x upscale for this goal.
- Do not treat `workflowRAWDetailer_v10ZITEDITION` as a new default until its upscale/detail components beat native Moody in an isolated A/B.
- Do not stack Z LoRAs just because Telegram posts include heavy stacks; local Z LoRA patch/offload failures are already well documented.

## Current External Check

- ComfyUI official Z-Image example describes Z-Image as photoreal-capable and prompt-enhancer friendly; this supports structured prompt improvement, not random node stacking.
- Reddit Z-Image discussions still emphasize simple/native workflows, good divisible-by-16 resolutions, and style prompting. Multi-stage/upscale workflows exist but are intentionally not default here because local user preference currently rejects laggy scale-up paths.

## Next Action

For the next generation batch, create five controlled tests:

- 2x Z-Image Moody native prompt-grammar variants.
- 1x Beyond or Diving native natural-skin variant.
- 1x aMix + Ri-mix 0.65 semi-real anime variant.
- 1x Ri-mix alpha Anima HQ cinematic variant.

Only change the prompt block from the locked baselines. Keep model, sampler, steps, resolution, and node graph stable unless a single A/B explicitly asks otherwise.
