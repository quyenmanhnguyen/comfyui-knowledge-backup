# Locked historical winners

Last verified: 2026-07-22. Read this before creating or rerunning any SDXL or Z-Image candidate.

## Recovery baseline

Seven exact historical adult figure-study workflows were reproduced with original prompt, seed, canvas, sampler, scheduler, steps, CFG and graph. Only `SaveImage.filename_prefix` changed. All completed without upscale, timeout, node error or crash.

| Rank/use | Exact workflow | Reproduced | Visual role |
|---|---|---:|---|
| SDXL overall | `C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\SDXL_INTO_AUTHOR.json` | 40.2 s | Best natural full-body balance, soft daylight, coherent anatomy |
| SDXL full-body baseline | `C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\SDXL_INTO_NATIVE.json` | 42.2 s | Clean full-body framing and stable proportions |
| SDXL close/pose | `C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\SDXL_INTO_FIXED.json` | 42.2 s | Strong close composition and skin; use for difficult seated pose |
| SDXL skin/detail | `C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\SDXL_REALVIS_SDE.json` | 42.2 s | Strongest visible skin texture; best for closer framing |
| Z youthful bright | `C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\Z_DIVING_RES2S.json` | 68.3 s | Best youthful bright Z full-body baseline |
| Z natural/full | `C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\Z_BEYOND_RES2S.json` | 56.9 s | Natural tonal texture and fuller proportions |
| Z studio beauty | `C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\Z_MOODY_RES2S.json` | 80.3 s | Attractive studio look; smoother skin and slower |

Evidence:

- Report: `C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\REPORT.html`
- Timings: `C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\results.csv`
- Outputs: `C:\AI\ComfyUI\output\RECOVER-*.png`

## Mandatory recovery-first procedure

1. Select the closest baseline above by model family and intended framing.
2. Inspect its JSON and reference PNG before editing.
3. Reproduce the locked baseline after any runtime/model/node change.
4. Change exactly one material variable per A/B: prompt block, seed, canvas, sampler, model, or one LoRA/node.
5. Keep the baseline image beside the candidate in the report.
6. Reject the candidate if it loses face age, skin clarity, anatomy, framing or stability even when it is faster.
7. Promote only after SFW and clearly-adult nonsexual figure-study validation when broad stability is requested.

## Known regression cause

The rejected one-size-fits-all round kept model names but replaced model-native prompts, seeds and framing. It also combined positive `youthful adult` with negative `young-looking`. This contradiction can suppress the requested youthful appearance and make faces older or less coherent.

Never:

- normalize photoreal SDXL, Illustrious and Z-Image into one generic prompt;
- call a seed-only result a new workflow;
- add FreeU, Detail Daemon, refiner, face detailer, LoRA or upscale merely to make a graph look full;
- replace a locked winner until the candidate beats it visually under a controlled A/B.

## Preferred selection order

- General photoreal: IntoRealism Author.
- Youthful bright Z full body: Diving res_2s.
- Natural/full-bodied Z: Beyond res_2s.
- Close skin/detail: RealVis SDE or IntoRealism Fixed.
- Moody studio beauty: Moody res_2s only when its smoother skin and slower runtime are acceptable.
