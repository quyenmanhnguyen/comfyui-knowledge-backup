# Benchmark protocol

## Before running

1. Run `scripts/collect_state.ps1`.
2. Confirm no unrelated queue or user-started ComfyUI process is active.
3. Read recent CSV, logs, HTML reports, and selected output PNG metadata.
4. Build a shortlist by different model, loader, sampler structure, or material LoRA change. Reject seed-only duplicates.
5. Preserve originals and write to a new dated directory.

## Test design

- Start at 576×800 for Z-Image.
- Use the same prompt and seed within a comparison round.
- For broad realism validation, use:
  - BASIC: one clearly adult subject, visible hands, clothing materials, movement or object interaction, mixed lighting.
  - NSFW when requested: one clearly adult subject age 29+, solo, nonsexual fine-art studio, visible hands/feet, natural anatomy and skin.
- Run BASIC and NSFW for a final candidate; a single flattering portrait is insufficient.
- Record cold start and warm run separately.
- Use a four-minute per-image timeout unless the user explicitly authorizes research-slow paths.
- Interrupt a repeated 30+ s/step patch loop; restart ComfyUI before testing another candidate.

## Process isolation

- Start API-only with a hidden window and explicit port 8188.
- Prefer one process per model family for ordinary comparisons.
- Use a fresh process per LoRA when prior patch/unpatch behavior is unstable.
- Never kill generic Python processes. Match `ComfyUI\main.py`, inspect PID and command line, then stop only that PID.
- Stop ComfyUI at task completion unless the user asked to leave it open.

## Log interpretation

Capture:

- `model weight dtype` and `loaded completely` size.
- Sampler seconds per iteration.
- `Unloaded partially` lines before VAE decode.
- Prompt execution time.
- OOM, NaN, black image, node errors, unsupported quantization, or interruption.

Do not call a sampler slow when diffusion is fast but model/VAE transfer dominates.

## Visual scoring

Score each image from 0–5 on:

- Face/age/ethnicity.
- Skin clarity and natural texture.
- Hands/feet/anatomy.
- Prompt and object-contact compliance.
- Lighting/color/materials.
- Artifacts: fake text, duplication, merging, blur, wax, oversharpen, color bleed.

Reject a workflow with a severe anatomy or merged-object failure even if its average appearance is attractive.
