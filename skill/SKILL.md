---
name: optimize-comfyui-rx7800xt
description: Optimize, benchmark, diagnose, and select ComfyUI still-image workflows on the user's Windows RX 7800 XT machine using accumulated local evidence. Use for Z-Image, MoodyPro, Beyond Reality, Diving, CyberRealistic, Flux, Anima, LoRA, sampler, prompt, VRAM, ROCm, startup, speed, crash, image-quality, BASIC/NSFW comparison, model download, or final-workflow-selection requests on C:\AI.
---

# Optimize ComfyUI RX 7800 XT

## Required context

Read these files before proposing or running changes:

1. `references/machine-profile.md` for verified hardware, runtime, paths, and startup state.
2. `references/local-evidence.md` for current winners, rejected paths, and measured bottlenecks.
3. `references/benchmark-protocol.md` before running any generation benchmark.
4. `references/source-audit.md` before recommending upgrades, Triton, SageAttention, nightly Torch, or launch flags.
5. `references/sdxl-playbook.md` for every SDXL, Illustrious, aMix, FabricatedXL, OneObsession, IntoRealism, or RealVis task.
6. `references/zimage-playbook.md` for every Z-Image, ZIT, MoodyPro, Beyond Reality, Diving, CyberRealistic, or Z-Image LoRA task.
7. `references/historical-winners.md` before generating any new SDXL or Z-Image candidate; treat its exact workflows as locked visual baselines.
8. `references/recent-two-hour-audit.md` for the latest keep/reject distinctions and the fresh-process rule discovered during paired Z validation.

Run `scripts/collect_state.ps1` when runtime, process, version, model inventory, or launch configuration may have changed.

## Operating rules

- Answer in Vietnamese.
- Treat local successful images, embedded PNG prompt metadata, CSV timings, logs, and reports as the strongest evidence for this machine.
- Inspect prior output and workflow history before generating new candidates. Never restart research from zero.
- For SDXL, begin with the reproduced leaders and model-specific prompt grammar in `references/sdxl-playbook.md`; do not normalize anime and photoreal checkpoints into one generic graph.
- For Z-Image, begin with the reproduced leaders and runtime guardrails in `references/zimage-playbook.md`; do not stack LoRAs or replace native sampling merely to create a new candidate.
- Separate model differences from prompt, sampler, scheduler, LoRA, loader, cold-load, warm-run, VAE decode, and browser/GPU contention.
- Compare new work against the current leaders in `references/local-evidence.md`.
- Reject duplicate candidates that only change seed or minor wording.
- Do not re-run known crash, timeout, black-image, unsupported quant, or severe LoRA patch paths unless the user explicitly requests a regression test after a relevant runtime change.
- Never install or upgrade Torch, ROCm, Triton, SageAttention, attention backends, drivers, or ComfyUI automatically. Verify current primary sources, back up the runtime, and obtain explicit user authorization.
- Do not assume an FP8 file remains FP8 in compute. Read the log-reported model dtype and loaded size.
- Do not open ComfyUI or a browser automatically during benchmarks. Start hidden API-only processes, isolate model families when needed, enforce timeouts, and stop only the targeted `ComfyUI\main.py` process at the end.
- Preserve existing workflows. Save new API JSON and reports under a dated directory in `C:\AI\workflows`.
- Use recovery-first testing: reproduce the closest locked historical winner, then change exactly one material variable per A/B. Never replace prompt, seed and canvas together.

## Image-quality standard

Judge every candidate visually, not by runtime alone:

- Face: requested age, ethnicity, natural asymmetry, eyes, hairline.
- Skin: pores and tonal variation without blur, wax, harsh aging, oversharpening, or color bleed.
- Anatomy: hands, fingers, feet, pose, body proportions, object contacts.
- Scene: prompt compliance, materials, lighting, fake text, duplicated or merged objects.
- Stability: both BASIC and clearly adult NSFW prompts must succeed when the user requests broad validation.

Promote a candidate only if it improves a current leader in quality, speed, stability, or a distinct useful category.

Before any new visual-selection batch, load
`C:\AI\workflows\VISUAL_DIRECTION_LIBRARY_20260723\manifest.json` and run
`scripts/visual_gate.py` on each output. The gate is only a technical pre-filter:
full-size visual inspection remains mandatory. Never place a failed or explicitly
user-rejected image in the main gallery.

## Prompt construction

Use a structured, model-readable order:

1. Medium and composition.
2. One clearly adult subject with explicit age and ethnicity when relevant.
3. Pose/action and exact hand-object relationships.
4. Clothing or adult figure-study constraints.
5. Lighting and exposure.
6. Lens/camera.
7. Skin, hair, fabric, and material detail.
8. Compact exclusions.

Avoid hype-token piles. For youthful clean skin, do not overuse `blemishes`, `aged`, `weathered`, or harsh microcontrast. For natural mature skin, use directional light, fine pores, peach fuzz, subtle tonal variation, and restrained microcontrast.

## Benchmark handoff

Report:

- Workflow and output paths.
- Cold and warm runtime separately.
- Sampler time versus model/LoRA/VAE transfer time when logs expose them.
- Success, timeout, interruption, node error, or crash.
- Visual reason for ranking or rejection.
- Whether ComfyUI is still running.

Update `references/local-evidence.md` only after a result is locally reproduced and visually inspected.
