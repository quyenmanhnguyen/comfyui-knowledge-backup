# Z-Image playbook

Use this reference for Z-Image, ZIT, MoodyPro, Beyond Reality, Diving, CyberRealistic, Z-Image LoRAs, samplers, speed, crashes, and image-quality work on this machine.

## Canonical graph

Use these components unless an exact author workflow requires otherwise:

- `UNETLoader`, `weight_dtype=default`
- `CLIPLoader`: `qwen_3_4b.safetensors`, type `lumina2`, device `cpu`
- `VAELoader`: `ae.safetensors`
- Native canvas: 576x800 for the established portrait benchmark
- Standard quality path: `ModelSamplingAuraFlow`, shift 3; KSampler CFG 1, denoise 1
- Negative conditioning: `ConditioningZeroOut` when matching the established Z workflow
- No upscale during comparison

Do not substitute a generic SDXL/Flux loader or encoder. Do not assume the filename precision equals compute precision; read model dtype and loaded size from logs.

## Reproduced leaders

### Overall natural realism: Beyond Reality v3 BF16

- Model: `china_community\beyondREALITY_V30_CIVITAI_BF16.safetensors`
- Quality: `res_2s`, `beta57`, 12 steps, CFG 1, AuraFlow shift 3, 576x800.
- Measured isolated pair: about 87 s BASIC / 54.4 s adult NSFW.
- Strength: most natural mature skin, asymmetry, hands, feet, and anatomy; avoid calling its less doll-like face “worse.”
- Practical fast path: `ZSamplerTurboX21 //ZImagePowerNodes`, 8 steps, `alternative_refiner=true`, `spectral_tilt=stage3_H`, `old_scheduler=false`, `turbo_creativity=false`, `disable_ibias=false`, `ibias=0`.
- X21 measured: about 68.5 / 40.9 s. It is cleaner/smoother and slightly less detailed than res_2s.

### Youthful beauty: MoodyPro v13.2

- Model family: `moodyProMix_zitV13.safetensors`; prefer the installed v13.2 file when its exact filename differs.
- Quality: `res_2s`, `beta57`, 10-12 steps, CFG 1, shift 3, 576x800.
- Strength: attractive youthful face, good skin, hair, and fashion material.
- Runtime can vary sharply because model/Qwen/VAE reload dominates. Do not judge sampler speed from total cold time.
- Fast portrait draft: `RandomNoise` + `BasicGuider` + `KSamplerSelect(euler_flow)` + `ZImageTurboScheduler(8)` + `SamplerCustomAdvanced`.
- EulerFlow/ZIT8 measured about 43.7 / 37.2 s. Keep for simple portraits; reject for complex full-body scenes after the reproduced merged stool/bag/leg artifact.

### Youthful clean alternative: Diving v7 FP16

- Model: `divingZImageTurbo_v70Fp16.safetensors`
- Preferred visual direction: native `res_2s`, `beta57`, about 10 steps, CFG 1, shift 3.
- Strength: clean young beauty without obvious blur when the native graph behaves normally.
- Weakness: FP16 reload/offload can dominate and long paired tests can become unstable.
- Do not use Detail Daemon 0.30 or 0.12 as default: both caused digital edges, oversharpening, and fake text without a quality win.

### Documentary texture: CyberRealistic v6

- Model: `cyberrealisticZImage_v60.safetensors`
- Recipe: `res_2s`, `beta57`, 10 steps, CFG 1, shift 3, 576x800.
- Measured about 80.4 / 51.5 s in the final pair report.
- Strength: pores, tonal variation, anatomy.
- Bias: older, darker, more angular faces. Use only when documentary/mature texture is wanted; do not try to force it into the youthful beauty default with prompt hype.

## Prompt grammar for the requested aesthetic

Use natural-language photographic prose, not tag soup. Order:

1. Premium editorial/candid/fine-art photograph and composition.
2. One clearly adult subject with explicit age and ethnicity.
3. Youthful soft oval face, natural expression, hair, and pose.
4. Exact hands, feet, clothing, or adult figure-study constraints.
5. Bright diffused key light plus clean white bounce/fill.
6. 85 mm lens and shallow depth of field when portrait mood is desired.
7. Luminous neutral-warm skin, fine pores, peach fuzz, subtle blush and tonal variation.
8. Realistic hair, silk/fabric, wet pavement, glass, or other scene materials.

For the preferred “đẹp, nét, sáng, trẻ” direction, favor `luminous healthy neutral-warm skin`, `bright diffused light`, `clean face fill`, `subtle natural blush`, `fine pores`, and `peach fuzz`. Avoid `weathered`, `aged`, `blemished`, harsh microcontrast, grey skin, low-key lighting across the face, or long exclusion-heavy prompts.

Use restrained teal/gold blue-hour mood when matching the previously selected street portrait. The rejected TOP10 reference-style round flattened this into bright 50 mm daylight and became visually worse.

## Runtime and stability rules

- Z diffusion itself is often around 1-2 s/step. Total 80-185 s commonly comes from Qwen load, UNet load/unload, LoRA patching, and UNet-to-VAE transfer.
- A roughly 12 GB BF16/FP16 model plus Qwen and VAE cannot remain fully resident in 16 GB VRAM. Some transfer is unavoidable.
- Group prompts under one unchanged model. Restart the process before changing checkpoint families and after suspicious LoRA/offload behavior.
- Use one cold plus warm paired run for speed claims. Report sampler time separately when logs expose it.
- Enforce 150-240 s prompt timeouts. Interrupt, stop the targeted API process, and record timeout; do not let a poisoned process contaminate the next model.
- Browser/video GPU use can reduce available VRAM and slow transfers. Benchmark with the browser closed or idle, but do not modify Chrome without user authorization.
- Keep `--use-pytorch-cross-attention`: local A/B measured SageAttention about 15% slower at the established sequence length. Triton may remain installed but is not the cause of the later 2x report speedup; resident model/cache state was.

## LoRA policy and known failures

Treat every Z LoRA as a VRAM/patch risk. Start with native checkpoint and add one low-strength LoRA only for a specific defect.

Do not retry these as defaults without a relevant runtime change:

- Moody + FDPO 0.30: roughly 34-39 s/step and timeout.
- Moody + Professional Photographer or Radiant Realism: roughly 40-80 s/step patch/offload and timeout.
- Cyber + skin-texture v4.5 at 0.35: reference image was attractive, but clean retest reached about 81.9 s/step and timed out.
- SDA 0.55, skin-texture v4.5 0.22, Smooth Booster 0.18: isolated SFW outputs existed, but paired adult NSFW runs timed out at 150-240 s; not stable winners.
- Cyber + Kook: made the face younger but failed paired stability.
- Aesthetic Turbo 20-step LoRA: exceeded 586 s without output.
- RedCraft quant paths: local server crash/unsupported behavior.
- Krea2 on this machine: roughly 340-512 s; not a practical default.

Never promote a LoRA from one attractive image. Require the paired test, visual inspection, and acceptable warm behavior.

## Visual acceptance

Score face/age, skin texture, hands/fingers, feet, pose, object contact, prompt adherence, material realism, fake text, and color bleed.

Reject:

- smooth wax/plastic skin presented as “clean”;
- dark/grey/old face when youthful bright beauty was requested;
- merged stool, bag, chair, limb, or other contact artifacts;
- fake lettering introduced by aggressive detail nodes;
- a valid SFW image paired with timeout, crash, or malformed adult NSFW output when broad stability was requested;
- a workflow that only changes seed, minor wording, or node count.

## Baseline artifacts

- Final pair report: `C:\AI\workflows\COMMUNITY_TEST_20260717\FINAL_TOP10_PAIR_20260719\REPORT.html`
- Diving/Cyber regrade: `C:\AI\workflows\COMMUNITY_TEST_20260717\DIVING_CYBER_REGRADE_20260719\REPORT.html`
- Aesthetic round: `C:\AI\workflows\COMMUNITY_TEST_20260717\AESTHETIC_ROUND_20260719\REPORT.html`
- Rebalance report: `C:\AI\workflows\REBAlANCE_SDXL_Z_20260721\REPORT.html`
- Rejected reference-style round: `C:\AI\workflows\TOP10_REFERENCE_STYLE_20260721\REPORT.html`

Before generating, inspect the embedded PNG prompt metadata of user-selected winners rather than reconstructing them from report captions.
