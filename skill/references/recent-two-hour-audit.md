# Recent two-hour audit — 2026-07-22

Use this audit with `historical-winners.md` before further Z-Image/SDXL exploration. Scope: workflow rounds modified roughly 18:30–20:30 Asia/Saigon on 2026-07-22 plus the immediately following five-pair Z close test.

## Keep as primary evidence

- `FINAL_SFW_NSFW_20260722`: IntoRealism overall photoreal leader; Beyond stable full-body; Diving youthful bright Z leader. Moody res_2s is visually good but its 210.6 s paired outlier prevents default promotion.
- `OLD_WINNER_SLOW_20260722`: H4 Moody EulerFlow/ZIT8 remains the preferred bright youthful aesthetic. Longer samplers made faces harder/older; do not equate more steps with more beauty.
- `HISTORICAL_WINNER_RECOVERY_20260722`: exact old graphs reproduced 7/7. This is the locked recovery baseline proving later regressions were caused by input/graph changes, not lack of capable models.
- `Z_CLOSE_CURVY_5PAIR_20260722`: 10/10 final isolated runs completed. Use its close, fuller-figure findings below.

## Keep only for a distinct role

- `EXPANSION8_PAIR_20260722`: keep RealVis SDE for sharp fashion/close skin and OneObsession for high-contrast anime. Cyber Z v2 is documentary/anatomy-only because it biases older/darker. Anima full stack is a fast generic anime option.
- `MODEL_LORA_AUDIT_20260722`: keep Animayume and Anima+Niji as optional anime styles. Keep 748cm only for SFW style; adult validation had glossy skin and overlapping feet.
- `YOUTHFUL_CLEAN_NSFW_20260722`: keep Diving H2 and Moody H4 results. RealVis/Into close crops were valid for close studies but failed the then-required full-body framing; do not label the checkpoints bad.

## Reject or avoid repeating

- `QUALITY_TOURNAMENT_20260722` and the rejected one-size prompt direction: changing prompt, seed and framing together erased model-native strengths. Positive `youthful adult` plus negative `young-looking` was contradictory.
- Slow extensions from `OLD_WINNER_SLOW_20260722`: Moody res_2s 14, Moody DPM++ SDE 16, Diving res_2s 14 and Beyond res_2s 14 did not improve the requested youthful beauty; several made faces older/harder.
- Flux UltraReal v4 and FluxedUp: blurred/soft, slow and below Z/SDXL quality.
- PhotoAnima: wrong identity bias, harsh/over-rendered skin and poor crop.
- Z LoRA patch bucket: PhotoBOX, Realistic Fantasy, FDPO, Professional Photographer, Radiant Realism, aggressive skin/detail LoRAs. Repeated patch/offload stalls or timeouts; do not retry without a runtime-relevant change.
- Detail Daemon 0.12/0.30 and gratuitous full-node stacks: digital edges, fake text or oversharpening without a quality win.

## Five-pair close/full-figure Z result

All final measurements below used a fresh API-only ComfyUI process for every image, same SFW/NSFW prompt grammar and shared seeds, no LoRA/detail/upscale.

| Recipe | SFW / NSFW | Visual decision |
|---|---:|---|
| Moody EulerFlow H4 | 64.2 / 64.5 s | Best youthful fuller appearance and fastest balanced pair; skin is smooth/doll-like. Keep for beauty-first close images. |
| Moody res_2s | 78.2 / 82.3 s | Best compromise between youthful face, fuller shape and visible skin texture. Promote as close quality default. |
| Beyond res_2s | 80.1 / 82.3 s | Most natural mature texture; face appears older than requested. Keep for naturalism, not youth-first. |
| Diving res_2s | 78.2 / 78.4 s | Bright attractive SFW and useful texture; NSFW right-hand fingers stretched. Keep, but reject that NSFW seed. |
| Beyond X21 | 66.4 / 72.2 s | Clean, fuller and practical; smoother texture and more mature SFW face than Moody. Keep as fast natural alternative. |

Initial paired runs placed SFW then NSFW in one process. Diving and Beyond NSFW both timed out at 240 s. Re-running the identical NSFW workflows in fresh processes completed in 78.4 and 82.3 s. Therefore classify those initial timeouts as warm model/VAE/Qwen offload contamination, not prompt or model failure. For Z paired validation on this machine, use a fresh process per image when correctness matters.

## Next-use rules

1. For a close youthful fuller target, start from Moody res_2s; compare Moody Euler H4 when beauty/speed matters more than pores.
2. Use Beyond res_2s only when natural texture outweighs the youthful-face target.
3. Keep Diving but change only its failed NSFW seed/hand pose in the next A/B.
4. Do not add `young-looking` to the negative when positive asks for a youthful adult face.
5. Use a fresh process per Z image for final paired validation; warm sequential execution can create false timeout conclusions.
