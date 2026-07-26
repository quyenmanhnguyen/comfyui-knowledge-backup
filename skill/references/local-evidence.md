# Local workflow evidence

## MAIN10 NSFW workflow pack -- 2026-07-26

- Curated pack: `C:\AI\workflows\MAIN10_NSFW_WORKFLOWS_20260726`. It contains 10 copied workflow JSONs under `workflows\`, 10 reference images under `reference_images\`, `main10_manifest.json`, `README.md`, `REPORT.html`, and `CONTACT_SHEET.jpg`.
- Selection principle: workflows must be materially different by model family, loader, sampler/style role, or visual target. Seed-only or tiny prompt/strength variations were not allowed.
- Main rank order:
  1. `01_ONEOBSESSION_HIGH_IMPACT_SOFA` — SDXL/Illustrious OneObsession v23, strongest high-impact glossy curvy adult-anime NSFW; start here for "hở/căng/ấn tượng".
  2. `02_ANIMA_RIMIX_WINDOW_CHAISE` — Ri-mix alpha Anima + exposure lighting; cinematic rain/window chaise.
  3. `03_ANIMA_RIMIX_MIRROR_STAND` — same Anima family but distinct standing/mirror-room premium pose.
  4. `04_AMIX_RIMIX_BALANCED_SILK` — aMix + rimixxO2 0.65, clean balanced semi-real anime.
  5. `05_HASSAKU_BRIGHT_CURVY_LOUNGE` — Hassaku v3.4 bright curvy anime secondary.
  6. `06_ANIMA_RIMIX_EXPOSURE_TELEGRAM` — earlier Telegram/model-expansion Ri-mix alpha Anima baseline.
  7. `07_ANIMA_MOODY_MYTH_PORTRAIT` — Moody Anima + Myth Portrait; faster/brighter Anima portrait branch.
  8. `08_INTOREALISM_PHOTOREAL_ADULT_STUDY` — IntoRealism Author SDXL photoreal adult figure-study branch.
  9. `09_ZIMAGE_MOODY_RES2S_PHOTOREAL` — MoodyPro v13.2 Z-Image res_2s/beta57 photoreal branch; no Z LoRA/detail/upscale.
  10. `10_WAI_CLEAN_MIRROR_ANIME` — WAI v17 clean mirror anime; useful lightweight distinct style, but weaker than rank 1–9.
- For future work, treat ranks 1–4 as the first-call main anime/Anima choices. Use rank 8/9 only when the user specifically asks for real-person/photoreal. Rank 10 is optional/filler, not a visual leader.

## Civitai/Telegram adult Anima + SDXL pose batch -- 2026-07-26

- Evidence/report: `C:\AI\workflows\CIVITAI_ANIMA_NSFW_POSES_20260726\REPORT.html`; selected outputs copied to `C:\AI\workflows\CIVITAI_ANIMA_NSFW_POSES_20260726\SELECTED`.
- Eight native-resolution adult NSFW candidates were generated with no upscale: four Ri-mix alpha Anima ER-SDE/simple workflows and four SDXL/Illustrious workflows based on locked OneObsession, aMix+Ri-mix, Hassaku and WAI presets. All completed without node error or crash.
- Best current high-impact adult-anime continuation: `CANP-05_ONEOBS_LOCKED_SOFA` (OneObsession v23, 832x1216, DPM++ 2M/Karras, 32 steps, CFG 5.5, CLIP skip 2, 32.1 s). It best matches the approved S4 direction: glossy luminous skin, strong curvy body design, ornate sofa, rainy blue window and warm lamp. Continue this branch for "hở/căng/ấn tượng" close compositions.
- Strong Anima cinematic variants: `CANP-01_ANIMA_WINDOW_CHAISE` and `CANP-03_ANIMA_MIRROR_STAND` (Ri-mix alpha Anima + exposure lighting LoRA 0.45, ER-SDE/simple, 32 steps, CFG 3). They preserve the Telegram-style rain/window/lamp grammar with better cinematic depth than generic SDXL, but remain more illustrated than photoreal.
- Balanced clean SDXL/Illustrious variant: `CANP-06_AMIX_RIMIX_SILK_SOFA` (aMix + rimixxO2 0.65, Euler A/normal, 30 steps, CFG 7) is cleaner and less extreme than OneObsession; use when the user wants elegant rather than maximal.
- Secondary: `CANP-07_HASSAKU_BRIGHT_LOUNGE` is bright and curvy but simpler/flatter. `CANP-08_WAI_CLEAN_MIRROR` is clean but less premium. `CANP-02_ANIMA_KNEEL_WINDOW` is acceptable but too mild. `CANP-04_ANIMA_EDGE_BED` is visually strong but more game-like/plastic and should not be the main recommendation unless the user asks for harder anime rendering.
- Community/Civitai triage for this pass found no small newly-downloadable LoRA with stronger reproducible settings than the already-installed Ri-mix/OneObsession/Hassaku/WAI/Anima stack. Do not download random character LoRAs merely because they rank in Civitai search; prefer model-author settings and local winners.

## Moody realtime Telegram learning -- 2026-07-26

- Realtime read-only Telethon scan succeeded for `Moody小圆脸同好会`: 6 forum topics and 338 recent messages were scanned. Output: `C:\AI\telegram_client\moody_realtime_scan.json`; working synthesis: `C:\AI\workflows\MOODY_REALTIME_LEARNING_20260726.md`.
- Telegram forum-topic message views frequently returned `0`, so rank Moody posts by reactions, attached media/files, recency, topic, reproducible settings, and whether the prompt/model data maps to local files. Do not treat unread/topic counters as view counts.
- The useful Moody prompt lesson is structured scene prose, not more nodes: subject/composition, clearly adult age, face/hair/expression, silhouette/pose, exact left/right hand placement, fabric/adult figure-study constraints, layered room/window/sofa/rain/lamp materials, lighting/color grade, lens, compact exclusions.
- Convert extreme/private Telegram prompts into non-graphic adult glamour/fine-art constraints. Preserve the visual grammar: rain-blue window, warm lamp, pale sofa/bed, translucent fabric, pearls/jewelry, glossy but not plastic skin, direct emotional gaze.
- Local Downloads contains `workflowRAWDetailer_v10ZITEDITION.json`. It includes Z nodes plus LoRA stack, `ImageUpscaleWithModel`, `DetailDaemonSamplerNode`, tiled VAE decode, and extra KSampler. Treat as research-only. If tested, disable/remove upscale first and A/B only one detail/sampler component against the locked Moody native baseline; do not promote as default from file presence.
- Current best next-test shortlist from this synthesis: MoodyPro v13.2 native res_2s for Z photoreal, Diving/Beyond res_2s as natural alternatives, aMix + Ri-mix 0.65 for balanced semi-real anime, OneObsession S4/T2 for close high-impact adult anime, and Ri-mix alpha Anima ER-SDE/CFG3/32 for HQ cinematic depth.
- Do not retry `realism-anima-v2`, gothic/neon/dark/dappled branches, full-image 2x upscale, or unstable Z LoRA stacks for the user's current bright youthful detailed-skin target.

## Telegram photo-direction reconstruction — 2026-07-26

- Source audit covered `C:\Users\Admin\Downloads\Telegram Desktop\ChatExport_2026-07-23\photos`: 5,358 image files, about 2,668 originals after excluding `_thumb`, spanning July 10–23. Fourteen date-stratified contact sheets and an all-days overview are saved under `C:\AI\workflows\TELEGRAM_PHOTO_DIRECTION_20260726\CONTACTS`.
- The useful recurring visual grammar was bright window portraiture, separated hands, clean warm face fill, restrained rim light, clear fabric/hair, and layered foreground/midground/background. Rejected motifs include enlarged/glassy eyes, painterly smearing, harsh orange skin, intertwined hands, dark gothic bias and whole-image hires resampling.
- SDXL reconstruction retained the proven aMix + `rimixxO2` 0.65 graph and changed only the composition/material/light prompt block: Euler A/normal, 30 steps, CFG 7, Clip Skip 2, 768x1152. Output `TGPHOTO-SDXL-RIMIX065-WINDOW_00001_.png` passed the technical gate and full-size review: clean eyes, coherent separated hands, crisp satin, no paint smear. It is the stable clean option.
- Anima reconstruction retained the author-proven Ri-mix alpha graph: ER-SDE/simple, 32 steps, CFG 3, 768x1152. Output `TGPHOTO-ANIMA-RIMIXA-LAYERED_00001_.png` completed in 65.59 s and passed technical/full-size review. It has better cinematic layering and warm/cool separation than SDXL while keeping simple coherent hands; skin is glossier but not plastic or painterly.
- Reusable workflows/report: `C:\AI\workflows\TELEGRAM_PHOTO_DIRECTION_20260726\TG_SDXL_RIMIX065_WINDOW_CINEMATIC.json`, `TG_ANIMA_RIMIX_ALPHA_LAYERED_CINEMATIC.json`, and `REPORT.html`. No upscale, FaceDetailer, FreeU or Detail Daemon was used.

## Ri-mix Style LoRA correction and author-strength validation — 2026-07-25

- User correction: the requested resource is `Ri-mix - Style LORA [Illustrious + Anima]`, 663.98 MiB, not the separate 3.89 GB Ri-mix alpha Anima checkpoint. Preserve both resources but never conflate their loaders or settings.
- Local `rimixxO2.safetensors` is exact-identical in Downloads and `models\loras`; SHA256 `E612482B4DD8ED43466BD12C0E4DB33F469B88F4FF85D83A154B7AEAC458F624`. It has 2,250 `lora_unet_*` tensors, no text-encoder tensors, and metadata architecture `stable-diffusion-xl-v1-base/lora`. This proves it is an SDXL/Illustrious UNet LoRA and cannot be loaded directly into an Anima diffusion graph.
- Correct author-style Illustrious validation: aMix Illustrious base, LoRA model strength 1.2, Clip Skip 2, Euler ancestral/normal, 30 steps, CFG 6, 768x1152, no upscale/detailer. It completed in 34.16 s and passed the technical gate. Output `RIMIXSTYLE-AUTHOR12-NATIVE_00001_.png` has a clean face and hands, strong satin/light rendering, and a noticeably stronger/glossier style than the locally preferred 0.65 preset.
- Keep two intentionally different presets: author-faithful 1.2 for strong Ri-mix styling; locally balanced 0.65 for cleaner face/style restraint. Do not silently replace one with the other.
- Corrected workflow/report: `C:\AI\workflows\RIMIX_STYLE_LORA_AUTHOR_20260725\RIMIX_STYLE_AUTHOR12_NATIVE.json` and `REPORT.html`. The earlier `RIMIX_ALPHA_AUTHOR_20260725` graph remains valid only for the separate full Anima checkpoint.

## Ri-mix α Anima author-native install and validation — 2026-07-25

- Source: Civitai/civitai.red model 996495, version 3020951, updated June 2026. The downloaded 3.89 GB checkpoint merge was moved to `C:\AI\ComfyUI\models\diffusion_models\riMixIllustriousAnima_riMixAnima.safetensors`; SHA256 begins `91CF056496`, exactly matching the author version.
- Safetensors metadata confirms this is a full Anima diffusion-model merge from `anima_baseV10` + `rimixao5050`, not a LoRA. Keep the separate `rimixxO2` file as the Illustrious Ω branch; do not stack it on Ri-mix α.
- Required components were already installed and exact-hash matched: `qwen_3_06b_base.safetensors` (`CD2A512003`) and `qwen_image_vae.safetensors` (`A70580F021`). No duplicate downloads were needed.
- Author's Anima settings were followed without mixing the Illustrious section: ER-SDE, CFG 3, 30–40 steps. Local validation used 32 steps, simple scheduler, native 768x1152, no upscale/detailer. It completed successfully in 58.56 s backend / 68.2 s API wall time; model loaded as float16, output passed the technical gate.
- Output `RIMIXA-AUTHOR32-SFW_00001_.png` showed strong face, hair, satin and warm-window rendering. The visible right hand was coherent; the left hand was cropped by composition. Reusable workflow/report: `C:\AI\workflows\RIMIX_ALPHA_AUTHOR_20260725\RIMIX_ALPHA_ANIMA_AUTHOR32.json` and `REPORT.html`.
- Do not apply Clip Skip 2, Euler A/CFG 6–7, or the Forge hires settings to this Anima graph merely because they appear elsewhere on the same page; those instructions belong to the Illustrious branch. The page does not provide a reproducible Anima-specific hires denoise/upscale recipe.

## Z-Image final 10 main-workflow validation — 2026-07-25

- Report: `C:\AI\workflows\ZIMAGE_FINAL10_MAIN_20260725\REPORT.html`. Five proven Z recipes were each rerun as exact SFW/clearly-adult NSFW pairs in ten isolated API processes. All 10/10 completed and passed the technical gate; no upscale, detailer or LoRA was used.
- Main winner: MoodyPro v13.2, native `res_2s`/`beta57`, 10 steps, CFG 1, shift 3, 576x800. It gave the best pair-level balance of youthful face, visible but restrained skin texture, clean light, coherent hands and anatomy. Measured 82.3 s SFW / 86.3 s NSFW. Canonical workflow: `C:\AI\workflows\ZIMAGE_FINAL10_MAIN_20260725\MAIN_ZIMAGE_MOODY_RES2S.json`.
- Fast secondary: Moody EulerFlow H4/ZIT8, 68.2/66.4 s. It is brighter and younger-looking but visibly smoother and more beauty-filtered. Use it for fast beauty drafts, not as the final texture default.
- Diving res_2s measured 80.3/84.3 s and remained strong, but its NSFW right hand was elongated; rank third. Beyond res_2s measured 87.8/84.4 s with the most natural texture but an older SFW face; rank fourth. Beyond X21 measured 72.3/70.3 s and is practical but smoother/more mature; rank fifth.
- Fresh-process isolation again prevented false warm-run timeouts. ComfyUI was stopped after completion.

## User correction and eye-only SDXL repair — 2026-07-24

- The user explicitly approved `XHSCREEN-04_SEED72429784`, `XHSCREEN-01_SEED72429781`, and `XHNSFW-03_FACEV8_HANDV9` for eyes, nose, body shape and hands. This supersedes the earlier automatic rejection of those prefixes. Their remaining weakness is finish: not yet premium/smooth/voluptuous enough. Do not discard or regenerate these as anatomy failures.
- Later seed-screen/body-detail images have useful body shapes but inconsistent or glassy gaze. Preserve their pixels and repair eyes regionally; do not rerun the whole image or whole face.
- Controlled repair used `Eyeful_v2-Paired.pt` + IntoRealism Ultra on the original PNG, 384 guide, 14 steps, DPM++ SDE/Karras, CFG 4.0, feather 14. Denoise 0.12–0.17 was too subtle. Denoise 0.22–0.28 is the useful range for distant frontal eyes; 0.24 is useful for the seated/profile case.
- Pixel-difference validation proved the repair stayed inside the detected eye box: only 0.45–0.62% of image pixels changed. Best current frontal candidate is `XHEYE-SEED83_EYE028_00001_.png`; conservative alternative is `XHEYE-SEED83_EYE022_00001_.png`. `XHEYE-SEATED_EYE024_00001_.png` improves local coherence but the profile gaze remains the harder case and is secondary.
- Eye-only passes took 6–16 s after API startup/model residency, with no upscale and no body/hand resampling. Report and reusable graphs: `C:\AI\workflows\SDXL_EYE_REPAIR_20260724\REPORT.html`.
- Subsequent explicit user review rejected every `XHEYE-*` result: the eyes remained poor and the whole face was unattractive. This supersedes the provisional winner above. Block the full `XHEYE-` prefix. Root cause: an eye-only crop cannot repair weak global facial proportions, nose, jaw and expression. Future rescue must use a controlled whole-face crop or regenerate from an approved face baseline.
- Whole-face corrective A/B then used face_yolov8m on the same Seed83 body at denoise 0.32/0.40/0.48, guide 640, 20 steps. Only the face bbox changed (about 2.23% of pixels); body, breasts, hands, legs and pose stayed pixel-identical. Internal review prefers D32 for the softest youthful face, D40 for stronger definition, and rejects D48 as starting to look hard. These remain provisional until user review. Report: `C:\AI\workflows\SDXL_FACE_REPAIR_20260724\REPORT.html`.

## SDXL adult hand-detail corrective validation — 2026-07-24

- Evidence/report: `C:\AI\workflows\SDXL_NSFW_HAND_DETAIL_20260724\REPORT.html`. IntoRealism Ultra was tested with a clearly adult nude figure-study prompt, Face YOLOv8 and Hand YOLOv8/YOLOv9c, no upscale.
- First reclining A/B: native 56.3 s, Face v8 + Hand v8 88.4 s, Face v8 + Hand v9c 74.4 s. Both detectors improved the near hand only slightly; the far hand remained blurred because it was outside the focal plane. Hand v9c was faster and at least as clean as v8, so use v9c when a hand pass is justified.
- The corrective seated pose failed prompt compliance by hiding one hand. Native 52.3 s and v9 detail 68.3 s confirmed that a detailer cannot create a missing hand. These outputs are rejected.
- Four-seed native screening was therefore run before detailing. Seeds 72429781, 72429782 and 72429784 hid/crossed/cropped hands and are rejected. Seed 72429783 was the only candidate with two complete hands in one focal plane.
- The winning seed 72429783 with Face v8 + Hand v9c completed in 78.3 s. Both hands remained complete with coherent finger counts, no extra limbs, and face/skin stayed natural. The model drifted from hands-at-sides to symmetric hands-on-chest, so it wins anatomy but not exact pose compliance.
- New rule: for SDXL hands, screen native seeds/pose first, then run one Hand v9c pass only on an image where every required hand already exists and is visible. Detector/detailer cannot add missing hands or recover deliberate depth-of-field blur.

## Targeted full-detail A/B across SDXL, Anima and Z — 2026-07-24

- Evidence/report: `C:\AI\workflows\TG_ADV_FULL_DETAIL_20260724\REPORT.html`. Six planned isolated tests compared native and targeted Face+Hand YOLOv8 passes. No upscale and no whole-person SAM were used. Face settings: guide 512, 14 steps, denoise 0.18, feather 10. Hand settings: guide 384, 16 steps, denoise 0.24, feather 12.
- SDXL IntoRealism native completed in 54.4 s and was the best convincing-human image: natural skin tone variation, hair/fabric material, coherent seated pose and clean hand. The same-seed Face+Hand result took 74.3 s, changed eyes/lips slightly and did not materially improve already-good hands. Keep native as default; detailer is rescue-only.
- Anima + Ri-mix alpha native completed in 66.3 s with strong rain/lamp depth and satin/hair, but the table-side hand was ambiguous. The targeted detail result completed in 110.4 s and produced a more refined face and more coherent table-side hand. This is the only full-detail branch in this round worth retaining as an optional HQ preset.
- Diving v7 Z native completed in 168.6 s cold and produced credible human skin/light with a slightly long right hand. Z FaceDetailer was stopped: after base generation, the first face crop fell to 44.56 s per detail step due UNET/Qwen/VAE memory movement, before the hand pass. Do not run Impact FaceDetailer directly with this FP16 Z path on 16 GB VRAM.
- Telegram export supports explicit spatial hand ownership and layered lighting grammar, but its generic “full workflow” claims are not proof that every detector/refiner helps. Local A/B supersedes them.
- Current full-detail rule: SDXL native first and selective face/hand rescue only; Anima targeted Face+Hand is a valid HQ option; Z remains native and should be corrected by prompt/seed or a separate lightweight SDXL inpaint, not direct Z regional resampling.

## User correction — reject the entire Anima Realism v2 branch — 2026-07-24

- Explicitly reject the original `STYLEX2-B2_ANIMA_REALISM_V2` and every `ARUP6-*` prompt-upgrade output. The user judged all of them artificial, mannequin-like and plastic rather than convincingly human.
- This correction supersedes the earlier note that ARUP6 01/05/06 might be retained as pose references. Do not use those images, prompts, poses or this LoRA as visual references.
- `realism-anima-v2.safetensors` is disqualified for human realism on this machine. Do not retry it by lowering strength, changing prompt, adding skin/detail nodes, face detailers or upscale.
- For the next genuinely human branch, recover an approved photoreal baseline first: IntoRealism Author/Fixed, RealVis SDE, Diving res_2s, Beyond res_2s or Moody res_2s. Reject any output with waxy uniform skin before presenting it.

## User correction to five-style expansion — 2026-07-24

- Explicitly reject `STYLEX-A1_GOTHIC_NEON`, `STYLEX-A2_DARK_ART`, and `STYLEX-A4_DRAMATIC_DAPPLED`. They are now blocked by the technical pre-filter and must not appear in future selected galleries.
- The rejection is aesthetic, not a runtime failure: Gothic Neon is too flat and color-aggressive; Dark Art is too dark with unattractive eyes/face; Dramatic Dappled makes the face/skin too dark and orange. Do not retry adjacent gothic/neon/dark/dappled variants.
- Continue from the brighter approved branches only: Mythic ColorLines and WAI v17, while exploring genuinely different bright/clean checkpoints or portrait styles.

## Civitai/Telegram five-style expansion — 2026-07-24

- Report: `C:\AI\workflows\STYLE_EXPANSION_CIVITAI_TG_20260724\REPORT.html`. Five materially different style paths were run in isolated API processes at native resolution with no upscale/detailer; all five passed the technical gate and were visually reviewed.
- Newly downloaded and SHA256-verified: WAI Illustrious SDXL v17 (`waiIllustriousSDXL_v170.safetensors`, Civitai model 827184/version 2883731, SHA256 `F116B0C78FF441467B0CDC8F1936E1ED18EA31E9997C7B132B1B8DB533F0BD04`) and S1 Dramatic Lighting Anima V2 (`S1_Dramatic Lighting Anima_V2.safetensors`, model 661736/version 3126711, SHA256 `D27D2C74BF32222FB3DF4515E14A45AB996A59CFF3D53E4ABFA0F8ED5922399A`).
- Best new distinct style: Anima + Mythic ColorLines 0.78 at 768x1152, ER-SDE/simple 32, CFG 3, 64.1 s. It produced the strongest bright turquoise/gold fantasy composition, coherent face and hands, and opens a genuinely different illustrated category.
- Best clean practical new checkpoint: WAI v17 at 896x1216, Euler A/normal 28, CFG 6, 26.1 s. It produced clean mature anime, bright youthful face and coherent lounge composition. Use compact author-style prompts; WAI's author warns that excessive quality tags and long negatives make images blurry.
- S1 Dramatic Anima V2 0.82 produced strong dappled tropical light in 62.2 s. Keep as a lighting/style preset, not the default, because the tested face/skin became darker and warmer than the user's main preference.
- Gothic Neon Anima 0.82 produced a valid high-impact cyan/magenta poster style in 66.2 s, but was flatter and colder than the user-locked OneObsession S4. Keep only as a distinct comic/poster branch.
- Dark Art Anima 1.0 produced a valid dark manga/gothic image in 64.1 s, but the face and skin were too dark and the eyes less attractive for the bright youthful target. Reject from the main selection; retain workflow for audit only.
- Local Telegram export contributed the raw CCD/neon/high-contrast lighting grammar; it was not treated as proof of model settings. Civitai author/version data determined the exact base compatibility, trigger words and strengths.

## Latest user-locked correction: OneObsession S4 — 2026-07-24

- User review supersedes the earlier ADV8 ranking: only `ADV8-S4_ONEOBSESSION_CINEMATIC_NSFW_00001_.png` is approved. All other `ADV8-A1/A2/A3/A4/A4B/S1/S2/S3/S3B` outputs are rejected references and are blocked by `scripts/visual_gate.py`.
- Locked target: OneObsession v23; close three-quarter seated/reclined adult solo; very full soft-curvy proportions; black hair and bangs; glossy luminous skin; white ornate sofa; rainy blue bokeh; warm lamp/cool rim; sheer pale fabric and pearls; high contrast and direct gaze.
- Exact graph: `C:\AI\workflows\TG_CIVITAI_ADV_CINEMATIC_20260724\S4_ONEOBSESSION_CINEMATIC_NSFW.json`; seed 72428022; 832x1216; DPM++ 2M/Karras; 32 steps; CFG 5.5; CLIP skip 2; no upscale/detailer.
- `OBSLOCK5-T1B_EXACT_S4_PIXEL_RECOVERY_00001_.png` is pixel-identical to the approved S4. The earlier T1 attempt changed the negative prompt and is audit-only, not an exact recovery.
- Telegram evidence is from the local export `C:\Users\Admin\Downloads\Telegram Desktop\ChatExport_2026-07-23`, not live Telegram: `messages8.html` message 68168 (2026-07-20 20:57: semi-real 3D/anime, glossy fair skin, black hair, blue sheer silk, pearls/gold) and message 68659 (2026-07-21 14:02: full curvy proportions, pale sofa, lace/blue jewelry).
- Focused report: `C:\AI\workflows\ONEOBS_TELEGRAM_LOCK5_20260724\REPORT.html`. T2 blue-sheer/pearl chaise is the closest new S4 continuation; T5 is a strong warmer close-up; T3 is secondary due bridal drift; T4 is rejected for an unwanted second background person.
- Future work must begin from exact S4/T2, keep model/sampler fixed, and change one major scene/material block only. Do not broaden back to generic cinematic Anima/SDXL or let technical sharpness override the user's visual preference.

Last consolidated: 2026-07-21. Evidence grade: `Local` unless noted.

## Current leaders

| Category | Workflow | Proven result |
|---|---|---|
| Natural mature realism | Beyond Reality v3 BF16, res_2s/beta57, 12 steps | Best natural adult skin, age, hands, and anatomy; about 87 s BASIC / 54 s NSFW in isolated high-VRAM pair test. |
| Practical fast Beyond | Beyond Reality v3, X21 8 | Good quality/speed balance; about 68.5 s BASIC / 40.9 s NSFW isolated. Skin is cleaner and less detailed than res_2s. |
| Youthful clean beauty | Diving v7 FP16, res_2s/beta57, 10 steps | Best locally validated young, bright, clean skin without blur; about 132/127 s because FP16 reload dominates. |
| Young beauty alternative | MoodyPro v13.2, res_2s/beta57, 10–12 steps | Attractive youthful face and good skin; slower and less natural than Beyond in final pair test. |
| Fast portrait draft | MoodyPro v13.2, EulerFlow + ZImageTurboScheduler, 8 steps | About 44/37 s in final pair test; BASIC good, but complex full-body NSFW produced a merged stool/object artifact. |
| Mature documentary texture | CyberRealistic v6, res_2s/beta57, 10 steps | Strong pores/anatomy, but checkpoint biases faces older, darker, and more angular. Do not use for youthful beauty. |
| SDXL full-quality native | RealVisXL V5 FP16, DPM++ SDE/Karras, 36 steps, CFG 4, FreeU, 832x1216 | 62.3 s cold on 2026-07-21. Best local SDXL photoreal material/light quality, but face is more mature and outfit adherence is weaker than Moody Z-Image. A same-resolution 0.15 skin pass made too little difference; do not keep it by default. |
| SDXL natural youthful winner | IntoRealism Ultra SDXL V1 no-lightning, DPM++ SDE/Karras, 35 steps, CFG 4.5, 768x1024 | Reproduced 2026-07-21 at 42.3 s SFW cold / 30.1 s NSFW warm. Best current balance of youthful face, natural skin, anatomy and stability. FreeU is a commercial-polished alternative but can change pose/perspective. |
| Fast SDXL quality draft | RealVisXL V5 FP16, DPM++ 2M/Karras, 42 steps, CFG 4.5, 768x1024 | Reproduced 2026-07-21 at 24.2 s SFW cold / 18.1 s NSFW warm. Lower naturalness than IntoRealism but the best quality/speed discovery in the 20-pair round. |
| Anime SFW winner | OneObsession v2.3, DPM++ 2M/Karras, 32 steps, CFG 5.5, clip skip 2, 768x1024 | Reproduced 2026-07-21 at 24.1/14.1 s. Most impressive SFW anime composition/color in the round; NSFW tends to add clothing. |
| Clean anime pair | aMix Illustrious + Ri-mix Omega v2 at 0.85, Euler a/normal, 30 steps, CFG 7, clip skip 2, 768x1152 | Rebalanced prompt reproduced 2026-07-21 at 30.0/18.1 s. Daylight/brown-eye prompt removes the prior neon-eye artifact; best balanced clean anime pair. |
| Fast clean anime pair | FabricatedXL v7, Euler a/normal, 28 steps, CFG 6.5, clip skip 2, 768x1152 | Reproduced 2026-07-21 at 26.1/16.1 s. Clean flat illustration and good NSFW compliance; SFW overlapping hands remain imperfect. |

## Rejected or demoted

- Correction from explicit user review on 2026-07-22: the top four images in `TOP10_REFERENCE_STYLE_20260721` are approved visual references, especially H4 Moody EulerFlow/ZIT8. Preserve their exact bright-overcast 50 mm street prompt, crop, seed and sampler. The later blue-hour/85 mm tournament prompts were visually worse and must not replace this reference direction.

- MoodyPro X21: removed by user; soft/blurred, anatomy weaker, and slow after reload.
- Diving Detail Daemon 0.30: oversharpened/digital, fake text, no quality win.
- Diving Detail Daemon 0.12: still produced fake text/digital edges; res_2s is better.
- Cyber G2: brighter/cleaner but loses microtexture and does not overcome mature-face bias.
- Cyber + `skin texture Photorealistic style v4.5` at 0.35: reference image quality is real, but current retest reached about 81.9 s/step and timed out due LoRA patch/offload.
- Moody + FDPO 0.30: about 34–39 s/step and timeout.
- Moody + Professional Photographer and Radiant Realism LoRAs: severe 40–80 s/step patch/offload in clean retests; not stable defaults.
- PhotoAnima v2.1: fast but ignored ethnicity/style and looked over-rendered.
- Flux UltraReal v4 and FluxedUp NSFW: lower skin/face quality for this target than Z-Image.
- Cyber Catalyst v2 BF16: good texture/anatomy but hard/older face and 145/105 s.
- Krea2 paths: 340–512 s locally; not a default on this machine.
- RedCraft quant paths: known local server crash/unsupported behavior; do not retry without a relevant runtime fix.
- Aesthetic Turbo 20-step LoRA: exceeded 586 s without output.
- 2026-07-21 20-pair discovery: Z LoRA variants SDA 0.55, skin-texture v4.5 0.22 and Smooth Booster 0.18 produced valid SFW images but timed out on the paired NSFW warm run (150-240 s). Do not promote from a single successful image.
- Cyber res_2s and Cyber+Kook produced valid SFW but timed out on the paired NSFW run; Kook made the face visibly younger but did not meet stability requirements.
- Illustrious Ri-mix, Fabricated and OneObsession often added a dress/cloth to the adult nude prompt. aMix+Hand Focus complied better, but its SFW hands still had finger defects; the LoRA is not a reliable hand repair.
- Rebalance correction: the earlier glowing anime eyes were prompt-induced by explicit violet/blue/neon eye and hair terms, not a checkpoint defect. Brown-eye/daylight model-specific prompts removed the artifact across OneObsession, Ri-mix and Fabricated.
- Moody and Diving without LoRA, with their proven 85 mm mood prompt, produced valid SFW images at 80.7/82.2 s but both paired NSFW runs timed out at 180 s. Long-run Z instability persists independently of the flat prompt and LoRA stacks.

## Measured bottleneck

- Z-Image diffusion commonly runs around 1–2 s/step.
- Perceived 80–185 s runtime is often dominated by Qwen text encoder load, UNet load/unload, LoRA patching, and UNet-to-VAE memory transfer.
- A 12 GB BF16/FP16 model plus Qwen and VAE cannot remain fully resident together in 16 GB VRAM.
- `--highvram` helps some cold runs but cannot remove unavoidable reloads.
- Grouping prompts under one unchanged model helps. Switching LoRAs can poison performance and should trigger a clean process restart before subsequent measurements.

## Key reports

- `C:\AI\workflows\COMMUNITY_TEST_20260717\FINAL_TOP10_PAIR_20260719\REPORT.html`
- `C:\AI\workflows\COMMUNITY_TEST_20260717\DIVING_CYBER_REGRADE_20260719\REPORT.html`
- `C:\AI\workflows\COMMUNITY_TEST_20260717\CROSS_MODEL_DEEP_20260719\REPORT.html`
- `C:\AI\workflows\COMMUNITY_TEST_20260717\AESTHETIC_ROUND_20260719\REPORT.html`
- `C:\AI\workflows\TOP10_REFERENCE_STYLE_20260721\REPORT.html`
- `C:\AI\workflows\SDXL_REALVIS_FULL_20260721\REPORT.html`
- `C:\AI\workflows\DISCOVERY20_PAIR_20260721\REPORT.html`
- `C:\AI\workflows\REBAlANCE_SDXL_Z_20260721\REPORT.html`
- `C:\AI\workflows\KEEP_MAIN_SDXL_REBUILD_20260721\REPORT.html`
- `C:\AI\workflows\MODEL_LORA_AUDIT_20260722\REPORT.html`

## KEEP_MAIN SDXL rebuild (2026-07-21)

- Revalidated 5 SDXL/Illustrious recipes as 10 SFW/adult-NSFW images, without upscale and with a clean process per checkpoint.
- Best photoreal recipe remains IntoRealism Ultra No-Lightning: DPM++ SDE Karras, 35 steps, CFG 4.5, 896x1152, checkpoint CLIP connected directly; 56.6 s cold / 48.3 s warm. Adding `CLIPSetLastLayer(-1)` silently produced all-black decoded PNGs and must not be used with this checkpoint.
- Best semi-real anime recipe: aMix Illustrious + `rimixxO2` at 0.65, Euler ancestral/normal, 30 steps, CFG 7, CLIP skip 2, 768x1152; 26.1/18.0 s. Lower strength preserved the face/style better than historical 1.2 and was visually cleaner than native aMix.
- Best stable clean anime recipe: Fabricated XL v7 native, Euler ancestral/normal, 28 steps, CFG 6, CLIP skip 2, 768x1152; 26.1/16.1 s.
- OneObsession v23 gives the strongest detail/contrast, but complex hands near the face remain risky. Use separated simple hand poses.
- Author/Civitai data and local Telegram evidence agree that Illustrious LoRAs can alter face and base style; validate low strengths with paired A/B tests rather than stacking nodes.

Inspect embedded PNG `prompt` metadata for user-selected reference images before designing replacements.

## Model/LoRA inventory audit (2026-07-22)

- Inventory: 12 diffusion models (~104.97 GB), 5 checkpoints (~32.62 GB), and 61 LoRAs (~16.08 GB before cleanup). Workflow-reference count can produce false negatives when old JSON was moved or deleted; inspect reports and output PNGs before deleting an unreferenced file.
- Z-Image Turbo style LoRA screening on Beyond v3: PhotoBOX Aperture timed out at 180 s during patch/load with no image; ZiT Realistic Fantasy entered the same uninterruptible patch state. Stop that bucket rather than retrying similar Z LoRAs sequentially.
- Illustrious screening on aMix: PHM 26.1 s, Niji/Midjourney 22.1 s, Ouyenm 22.1 s, and 748cm 22.1 s all produced valid images. None beat Ri-mix 0.65/Fabricated v7 as a default. 748cm was best for SFW but its adult validation had overly glossy skin and overlapping feet; keep only as an optional SFW style.
- AnimaYume retest: 18.1 s, clean anime and improved hands with separated pose. Keep `animayume_v10.safetensors`; its zero-reference inventory status was misleading.
- Anima base + `Niji_semi_realism_v5` 0.60: 16.1 s, useful distinct semi-real style; keep as optional. Edge-contact hands still need simple poses.
- Base-model compatibility matters for cleanup: `ZIB-Aesthetic-Ultra`, `Hands zib`, and `yoki-zib` are Z-Image Base LoRAs while no Z-Image Base diffusion model is installed. Archive/delete only if the user does not plan to install Z-Image Base.

## Final paired selection (2026-07-22)

- Final validation used 8 retained recipes, each with one SFW and one clearly-adult nonsexual nude prompt, no upscale, clean process per model family; 16/16 images completed. Evidence: `C:\AI\workflows\FINAL_SFW_NSFW_20260722\REPORT.html` and `results.csv`.
- Best photoreal overall: IntoRealism Ultra (50.1 s SFW / 42.1 s NSFW). Best balance of face, skin texture, fabric, lighting, anatomy and speed.
- Best stable full-body/anatomy: Beyond Reality v3 res_2s (80.5 / 76.2 s). Slightly more mature-looking than the preferred youthful target, but the most dependable hands/feet and skin texture.
- Best youthful bright Z-Image choice: Diving v7 res_2s (74.2 / 70.1 s). Cleaner/younger than Beyond, with slightly smoother skin.
- MoodyPro v13.2 res_2s produced a strong youthful SFW image but the paired NSFW run took 210.6 s, so it is not a default despite good appearance.
- Best semireal illustration remains aMix + Ri-mix 0.65 (28.0 / 16.0 s). Fabricated v7 is the clean anime fallback (24.1 / 16.0 s). Animayume and Anima+Niji were faster but too plastic/stylized for the user's photoreal preference.
- Default retained shortlist: IntoRealism for general photoreal, Beyond for dependable full body, Diving for youthful/bright portraits, Ri-mix 0.65 for semireal anime. Do not rank solely by speed.

## Eight-branch expansion pair test (2026-07-22)

- Tested 8 workflows excluded from the preceding final round, each as SFW/adult-NSFW, no upscale and clean process per model: 16/16 API completions. Report: `C:\AI\workflows\EXPANSION8_PAIR_20260722\REPORT.html`.
- RealVisXL V5 DPM++ SDE/Karras 36 was the only new photoreal candidate promoted: 54.2/42.1 s. It adds a sharp, visually striking fashion/material category, but IntoRealism remains the balanced default and Beyond remains better for explicit visible-hand/full-body compliance.
- OneObsession v2.3 reproduced as the high-impact anime winner at 30.1/20.1 s. Keep for contrast, lighting and detailed hair; Ri-mix 0.65 remains the balanced semireal default.
- CyberRealistic Z v2 NSFW completed at 62.2/94.3 s with clean anatomy, but its older/darker face bias loses to Diving for the user's youthful bright target.
- PhotoAnima v2.1 was fast (22.1/14.0 s) but ignored Vietnamese/Asian identity, over-rendered skin, and cropped the adult full-body prompt. Do not promote.
- Flux UltraReal v4 produced a severely blurred NSFW output after 176.4 s; FluxedUp took 112.1/176.2 s and remained soft/low-detail. Both are rejected for the present still-image target even though API execution completed.
- Anima full stack was valid and fast (20.1/10.1 s) but generic; aMix+PHM 0.6 (26.2/16.1 s) had overlapping hands and glossy NSFW skin. Neither beats OneObsession or Ri-mix.

## Old-winner slow validation (2026-07-22)

- Reproduced approved originals with exact prompt/seed: H4 Moody EulerFlow/ZIT8 70.2 s, H2 Diving res_2s 10 88.2 s, C3 Moody Euler ancestral/Beta 14 78.2 s, H5 Diving EulerFlow/ZIT8 72.2 s. H4 remains the youthful bright aesthetic leader.
- Slow extensions did not automatically improve beauty: Moody res_2s 14 (92.2 s) and DPM++ SDE/Beta 16 (98.2 s) increased hardness/maturity; Beyond res_2s 14 (92.4 s) was the oldest-looking. Diving res_2s 14 (94.9 s) was sharper/confident but still more mature than H4.
- Evidence: `C:\AI\workflows\OLD_WINNER_SLOW_20260722\REPORT.html`. Future quality work should preserve the H4 composition and prompt grammar, screen nearby seeds, and change only one small variable at a time.

## Youthful clean adult-NSFW validation (2026-07-22)

- Six adult-NSFW workflows completed without upscale or detail nodes. Report: `C:\AI\workflows\YOUTHFUL_CLEAN_NSFW_20260722\REPORT.html`.
- Best photoreal full-body: Diving H2 res_2s, 84.4 s. It delivered the best balance of youthful face, clean natural skin texture, full-body framing and anatomy.
- Best youthful/clean alternative: Moody H4 EulerFlow/ZIT8, 70.3 s. Brighter and younger-looking than Diving but smoother and more doll-like.
- RealVisXL full SDE36 (58.2 s) and IntoRealism full (54.3 s) had useful photographic texture but cropped the requested full body; use them for closer figure/portrait studies rather than the default full-body preset.
- Ri-mix (28.1 s) and OneObsession (30.1 s) remain illustration-only alternatives; glossy skin and hand placement prevent promotion for clean realistic anatomy.

## Historical winner recovery (2026-07-22)

- Re-ran seven exact historical adult figure-study workflows with original prompt, seed, canvas, sampler and graph; only the SaveImage prefix changed. All 7/7 completed without upscale, timeout or crash. Evidence: `C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\REPORT.html` and `results.csv`.
- SDXL recovered cleanly: IntoRealism Author 40.2 s, IntoRealism Native 42.2 s, IntoRealism Fixed 42.2 s, RealVis SDE 42.2 s. Visual quality matched their historical outputs, proving the poor later SDXL round came from the replacement prompt/seed/framing rather than the checkpoints.
- Z-Image recovered cleanly: Moody res_2s 80.3 s, Diving res_2s 68.3 s, Beyond res_2s 56.9 s. Diving remains the youthful bright Z full-body choice; Beyond has more natural/full tonal texture; Moody is attractive but smoother and slower.
- Critical prompt correction: do not combine positive `youthful adult` with negative `young-looking`; that contradiction was present in the rejected one-size-fits-all round and can push faces older or less coherent.

## Z close/full-figure five-pair validation (2026-07-22)

- Five established Z graphs were tested as SFW/adult-NSFW close three-quarter pairs with fuller healthy proportions, shared prompt grammar/seeds, no LoRA/detail/upscale. All final isolated runs completed. Evidence: `C:\AI\workflows\Z_CLOSE_CURVY_5PAIR_20260722\REPORT.html` and `results.csv`.
- Moody res_2s (78.2/82.3 s) is the close quality default: best balance of youthful face, fuller shape and visible texture. Moody Euler H4 (64.2/64.5 s) is the beauty/speed winner but has smoother, more doll-like skin.
- Beyond res_2s (80.1/82.3 s) retained the most natural mature texture but looked older than the requested target. Beyond X21 (66.4/72.2 s) was a clean practical alternative with smoother texture.
- Diving res_2s (78.2/78.4 s) produced an attractive SFW image, but the tested NSFW seed stretched right-hand fingers; reject that seed rather than the graph.
- Critical runtime correction: sequential warm SFW→NSFW caused false 240 s timeouts for Diving and Beyond. Identical NSFW JSON completed in 78.4/82.3 s after a fresh process per image. Use fresh-process isolation for final Z pair validation.

## SDXL + anime soft-white validation (2026-07-22)

- Four retained SDXL/anime graphs were tested as isolated SFW/adult-NSFW pairs with soft white diffused light, no upscale: 8/8 API completions. Evidence: `C:\AI\workflows\SDXL_ANIMA_SOFTWHITE_4PAIR_20260722\REPORT.html` and `results.csv`.
- IntoRealism (60.3/54.5 s) was the best real-photo soft-white direction. SFW had natural exposure, fabric and skin; NSFW skin remained good but the crop was too close and omitted hands.
- RealVis SDE (68.4/60.3 s) produced the strongest SFW fabric/window-light image, but its NSFW output added a lace slip and failed the nude constraint. Keep as SFW/editorial only for this prompt/seed.
- Ri-mix 0.65 (42.2/34.1 s) was the best soft-white semi-real anime pair. It retained glossy skin, overlapping hands and changed the requested ivory dress toward dark brown; improve with separated hand pose and restrained highlights.
- Animayume (26.1/20.1 s) was fastest and visually clean, but cropped SFW hands at the edges and moved NSFW hands near the face. Keep as a fast anime draft, not the anatomy/compliance leader.

## Soft-white expansion six (2026-07-22)

- Six additional distinct SDXL/anime graphs produced 12/12 API-success images using clean per-image processes and no upscale. Evidence: `C:\AI\workflows\SOFTWHITE_EXPANSION6_20260722\REPORT.html` and `results.csv`.
- IntoRealism + FreeU (52.3/44.1 s) was the visual winner of the expansion: polished soft-white real-photo beauty. It is smoother/more commercial than native Into and its NSFW crossed-arm pose hid hands; keep as a beauty preset, not a native replacement.
- RealVis 2M (34.2/28.1 s) was the fastest good photoreal SFW option. Its NSFW output added a lace dress and failed compliance, repeating RealVis's clothing bias under this prompt.
- Fabricated (30.1/26.1 s) produced a clean SFW anime image but added a white sweater to NSFW; keep only as clean SFW for this direction.
- OneObsession (42.3/36.1 s) created the most expressive close anime images, but retained glossy skin, hands-near-face risk and very tight framing. Keep as a close emotional portrait style, not anatomy validation.
- Anima+Niji (26.2/20.1 s) gave an attractive semi-real SFW image, but cut hands at the edges and reduced NSFW to a face close-up. Anima full (20.1/22.2 s) was fast and clean SFW but introduced wrist rope in NSFW despite a nonsexual/no-props prompt; reject that NSFW output.

## SDXL full detailer A/B (2026-07-22)

- Controlled IntoRealism Ultra test: native, Face YOLOv8, Hand YOLOv8, sequential Face+Hand v8, and Face+Hand v9; each ran as isolated SFW/adult figure-study pairs at 896x1152, same seeds, no upscale. Evidence: `C:\AI\workflows\SDXL_FULL_DETAILER_20260722\REPORT.html` and `results.csv`.
- Native remained the default (68.3/66.3 s): best preservation of identity, natural skin and torso. Face v8 cost about 14-18 s (82.3/84.3 s) and is a rescue pass for genuinely weak/small faces, not an always-on quality improvement; it subtly changes eyes/identity.
- Hand v8 is conditional. The SFW pose hid the hands, so the detector effectively had nothing useful to refine; adding the node did not satisfy a missing-hand composition. On the adult validation it changed the visible lower hand slightly at 74.3 s. Generate a hand-visible pose first; detail afterward only when detection succeeds.
- Sequential Face+Hand v8 (80.6/92.4 s) is the retained optional full preset when both regions are visibly defective. V9 (80.4/126.6 s) changed the face more and was much slower on NSFW, so do not use it by default.
- No reliable local breast/chest detector was installed. Preserve torso/breast quality through the native checkpoint, coherent adult-anatomy prompt and seed selection; do not misuse unrelated NSFW detectors or claim a magic regional detail node. Detailer nodes cannot repair composition that hides hands, and more nodes are not proof of better quality.

## SDXL person segmentation + SAM A/B (2026-07-22)

- Installed the Impact Subpack-recommended `person_yolov8m-seg.pt` from Bingsu/adetailer into `models/ultralytics/segm` (54,827,683 bytes; SHA256 `C8AB26F517173B1FE8342D336A09F443EB61CB08DCBFC78D53FFF4C2547AE81E`). Reused the already-installed official SAM ViT-B checkpoint; no custom-node or runtime package change.
- IntoRealism same-seed A/B at 896x1152, no upscale: person segmentation 90.5/70.3 s; person segmentation plus SAM on CPU 132.4/128.5 s. Evidence: `C:\AI\workflows\SDXL_PERSON_SAM_20260722\REPORT.html` and `results.csv`.
- Both masks correctly isolated the person silhouette. SAM produced slightly more contour detail, but did not improve the final image relative to the segmentation-only mask enough to justify roughly another minute.
- A whole-person 16-step detail pass at denoise 0.14 still changed face/body shape and smoothed skin. Native IntoRealism retained better identity and natural texture. Keep person YOLO/SAM as targeted repair tools for a selected defective image; never enable whole-person regional detail by default.
- Aggressive follow-up at person-detail denoise 0.28, 24 steps, CFG 4.2 completed at 76.3 s SFW / 74.3 s adult figure-study. It made the face harder/more mature and skin smoother without producing a clearly fuller or more impressive body. Reject as a default; increasing regional denoise did not reverse the 0.14 weakness. Evidence: `C:\AI\workflows\SDXL_PERSON_HARD_20260722\REPORT.html`.
## Telegram export validation — 2026-07-23

- Source: complete Telegram Desktop export `ChatExport_2026-07-23` (10 HTML pages, 1,067 Comfy/model/workflow-related records indexed).
- Six clean-process SFW validations at native workflow resolution, no upscale:
  - Moody H4 Editorial: 56.2 s — best overall for youthful, bright, softly full street/editorial portrait.
  - Diving res_2s Candid: 70.5 s — strongest real skin texture, but explicit pink-blush wording over-reddens cheeks and ages the face.
  - Beyond res_2s Beauty: 78.2 s — best clean youthful close portrait; slightly beauty-retouched skin.
  - Cyber Bright Clean: 64.2 s — clean lighting/hands/clothes, but face remains more mature than target.
  - SDXL IntoRealism Native: 50.1 s — best SDXL portrait and strong speed/quality compromise.
  - SDXL RealVis SDE: 42.1 s — fastest, but literal colorful arcade background dominates and misses the reference aesthetic.
- Reproduced prompt lesson: `cool luminous fair skin`, restrained blush, broad white fill and low contrast are useful; do not combine strong pink-blush wording with Diving.
- Reproduced composition lesson: explicit action plus both complete hands visible improved pose/hand reliability in the tested set.
- Telegram Krea2 graphs frequently stack multiple LoRAs, use latent scaling, and require 4–8 GB text encoders. Do not promote these graphs without isolated A/B proof. Krea2-YM and Flux2 Klein True V3 remain heavy/deferred downloads.
- Evidence/report: `C:\AI\workflows\TELEGRAM_EXPORT_6_20260723\REPORT.html`.

## Telegram Z/SDXL/Anima paired follow-up — 2026-07-23

- Eight isolated SFW/adult-NSFW images completed, no upscale/detail/refiner:
  - CyberRealistic Z v2 CN: 62.2/62.1 s. SFW remains mature/flat; NSFW is youthful, bright and anatomically clean but has a cool-blue window cast. Keep only as a distinct Z NSFW option.
  - IntoRealism Author: 38.0/36.1 s. Best real-photo pair in this round: youthful, bright, natural skin, strong fabric and coherent anatomy. NSFW changed hands-at-sides to a valid hand-window contact.
  - AnimaYume: 20.1/16.0 s. Reject for this prompt: both variants cropped too tightly; NSFW had glossy plastic skin and exaggerated breasts; adult age was insufficiently clear in SFW.
  - aMix + Ri-mix 0.65: 28.1/24.1 s. Best anime/semi-real pair: coherent framing, clearly adult proportions and cleaner hands than AnimaYume; still glossy and exaggerated in NSFW.
- Prompt lesson: Telegram-style soft-white/cool-fair wording helps photoreal models, but cannot override a checkpoint's crop/style bias. Model-native framing remains more important than adjective density.
- Evidence/report: `C:\AI\workflows\TELEGRAM_Z_SDXL_ANIMA_8_20260723\REPORT.html`.

## Curated operating set — 2026-07-23

- Audited outputs/reports from 2026-07-22 through 2026-07-23 and copied a non-destructive operating set to `C:\AI\workflows\CURATED_MAIN12_AUX6_20260723`.
- Main 12 roles: Moody H4, Moody res_2s, Diving res_2s, Beyond res_2s, Beyond X21, IntoRealism Author, Into+FreeU, RealVis SDE36, RealVis 2M, aMix+Ri-mix 0.65, FabricatedXL v7, OneObsession v2.3.
- Secondary 6 roles: Cyber v2 CN, Cyber v6 Bright, IntoRealism Fixed, Moody C3 Euler/Beta14, Anima+Niji, Anima Full Stack.
- Default selection order: Into Author for general photoreal; Moody H4 for youthful bright Z beauty; Moody res_2s for closer Z skin/shape; Beyond res_2s for full-body anatomy; Ri-mix 0.65 for semi-real anime; FabricatedXL for fast clean anime.
- Report: `C:\AI\workflows\CURATED_MAIN12_AUX6_20260723\REPORT.html`.

## Final curated Top-6 exact rerun — 2026-07-23

- Re-ran 12 exact SFW/adult-NSFW workflows in fresh per-image processes, changing only SaveImage prefix. All 12/12 completed, no upscale or runtime error.
- Into Author 36.3/36.1 s; Moody H4 58.2/62.2 s; Moody res_2s 78.4/80.3 s; Beyond res_2s 80.3/72.5 s; Ri-mix 0.65 28.1/24.1 s; FabricatedXL 24.0/22.1 s.
- Pixel comparison against the selected leader outputs: 11/12 pixel-identical. Fabricated NSFW was visually equivalent with only a tiny background-shadow pixel variation.
- This confirms the practical defaults are reproducible on the current stack, not cache/seed luck.
- Evidence/report: `C:\AI\workflows\FINAL_CURATED_TOP6_20260723\REPORT.html`.

### Visual-ranking correction after user review

- The exact rerun proves reproducibility only; it does **not** prove that all six are the user's best-looking directions.
- Do not use recency or paired stability as a proxy for visual rank.
- Specific corrections: ZC5 Diving NSFW has an elongated/deformed right hand; Cyber Bright remains visibly mature; AnimaYume NSFW is over-cropped, plastic/glossy and anatomically exaggerated; Beyond NSFW is natural but older than the preferred beauty target.
- Older visual references must be included before rebuilding the main set, especially `QUALITY-BASE-ZIT-MOODY-V13`, `QUALITY-LORA-ZIT-SKIN-TEXTURE-V45`, the approved AESTH Euler/ZIT8 direction, and selected IntoRealism outputs.
- Treat `CURATED_MAIN12_AUX6_20260723` and `FINAL_CURATED_TOP6_20260723` as reproducibility/stability collections, not the final visual-best ranking.

## SDXL real 5 + anime 5 corrective retest — 2026-07-23

- Retested five real-photo and five anime/semi-real outputs from the retained historical graphs, changing only seeds and SaveImage prefixes, using isolated processes and no upscale. Evidence: `C:\AI\workflows\SDXL_REAL5_ANIME5_RETEST_20260723\REPORT.html`.
- Critical failure reproduced: `KEEP_MAIN_SDXL_REBUILD_20260721\05_INTOREALISM_ULTRA_SFW/NSFW.json` can complete successfully through the API yet produce all-black images. Do not use these graphs; their `CLIPSetLastLayer(-1)` path is unsafe for this checkpoint/runtime.
- Correct replacement: `DISCOVERY20_PAIR_20260721\S11_INTO_AUTHOR_SFW/NSFW.json`. Same replacement seeds produced valid, visually strong images in about 36 s, with natural skin and coherent anatomy.
- Into Fixed remained good but slower (~48 s): youthful/bright SFW with an edge-cropped hand; coherent NSFW with a slightly more mature face. RealVis SDE was sharp at 44 s but introduced fake storefront text, so keep it secondary and avoid signage prompts.
- Anime ranking from this retest: Fabricated v7 for the cleanest fast anime pair (26.1/22.1 s); Ri-mix 0.65 for stronger semi-real adult form (28.2/24.2 s, slightly glossy); OneObsession for highest hair/clothing detail (34.1 s, softer near hand).
- Operational rule reinforced: API completion is not image validation. Always run pixel-range/non-black checks and visually inspect face, hands, anatomy, crop, skin texture and lighting before promoting a workflow.

## User-locked visual direction library — 2026-07-23

- Created a non-destructive visual library at `C:\AI\workflows\VISUAL_DIRECTION_LIBRARY_20260723`: 17 approved references, 8 explicit rejected references, and 25 embedded prompt/workflow JSON files extracted from the PNG metadata. Use its `REPORT.html`, `README.md` and `manifest.json` before future generation or visual ranking.
- The user explicitly rejected these outputs as soft/blurred/unattractive direction and they must never be promoted as baselines: `SDXL10-04_REAL04_INTO_FIXED_NSFW`, `SDXL10-05_REAL05_REALVIS_SDE_SFW`, `VF35-29_S3_REALVIS_C1_SFW`, `VF35-30_S3_REALVIS_C2_SFW`, `VF35-31_S3_REALVIS_C2_NSFW`, `VF35-17_Z5_B_X21_C1_SFW`, `VF35-18_Z5_B_X21_C1_NSFW`, and `VF35-21_S1_INTO_AUTHOR_C1_SFW`.
- Important model-versus-image distinction: rejection applies to these exact prompt/seed/framing outputs, not automatically to the whole IntoRealism, RealVis, or Beyond checkpoint. Their locked historical recovery graphs remain useful, but a new result must visibly match or beat the approved reference at full resolution.
- New negative visual standard: reject beauty-filter softness, waxy/flat skin, weak eye/hair/fabric separation, window light that washes away skin detail, generic lifeless faces, or images that are merely clean without being visually striking.
- Mandatory next-run procedure: recover the closest PNG-embedded approved workflow exactly, compare at full size beside both an approved and a rejected reference, change one material variable only, and exclude failed images from the main result gallery.

## Active visual gate + filtered random five — 2026-07-23

- Installed the reusable technical pre-filter at `scripts/visual_gate.py` and made it mandatory in `SKILL.md`. It blocks explicit user-rejected prefixes and checks black/near-black pixels, very low contrast and technical softness. It never replaces full-size visual review.
- Validation run: `C:\AI\workflows\FILTERED_RANDOM5_20260723\REPORT.html`. Five graph-native random-seed outputs were retained after technical and visual review: Moody res_2s, Into Author SFW, Ri-mix 0.65 NSFW, Fabricated v7 NSFW and OneObsession SFW.
- Important filter calibration: Moody H4 seed `579845207` passed technical metrics but was manually rejected from the selected five because the face/skin remained too mild and smooth for the “best, sharp, striking” target. This confirms that edge/contrast metrics cannot judge beauty or skin character.
- Retained outputs are copied to `C:\AI\workflows\FILTERED_RANDOM5_20260723\SELECTED`; the visually rejected H4 output remains outside that folder for audit only.
- User correction: `FILTER5-04_FABRICATED_NSFW_A1` is visually rejected despite strong edge metrics. Its side-profile face, pose and body design were unattractive for the requested voluptuous adult-anime target. Remove it from the selected set and blacklist the exact seed/output; do not treat high edge score as aesthetic quality.

## Adult-anime curvy corrective five — 2026-07-23

- Corrective report: `C:\AI\workflows\ANIME_CURVY_RETEST5_20260723\REPORT.html`. Five isolated native-resolution outputs completed and passed the technical gate.
- For the explicit voluptuous adult-anime target, OneObsession seeds `1528486701`, `5858247`, and `535833129` visually beat the rejected Fabricated seed on face impact, body design, lighting and composition. Seed `1528486701` was the strongest overall, though its foreground foot is enlarged by perspective.
- Ri-mix seed `1751227198` is the balanced alternative with the best seated pose and coherent visible limbs. Seed `397693804` is secondary because the hands overlap and skin is glossier.
- Updated selection rule: for this exact target, start with OneObsession native NSFW or Ri-mix 0.65. Do not default to Fabricated merely because it is technically clean/fast; aesthetic face and pose quality take priority.

## Telegram + Civitai Anima/Z/SDXL validation — 2026-07-24

- Evidence/report: `C:\AI\workflows\TG_CIVITAI_6_20260724\REPORT.html`. Six main graphs plus one corrective Z rerun were generated in fresh per-image processes, native resolution, PyTorch cross-attention, no upscale. All outputs passed the technical gate and were visually inspected.
- Installed and SHA256-verified Civitai model `Moody Anima Mix v1.0` (`moodyAnimaMix_v10.safetensors`, 3.90 GB; SHA256 `5368C9B1318C783D7215492002CD1BCA94895D1DCA8C780EF24F75536FD341F8`) plus the author's minimal Anima and Z-Image workflow archives. Telegram export links and the Civitai API independently matched model/workflow IDs 2700077, 2700120, and 2253524.
- Moody Anima author-native adaptation at 832x1216, ER-SDE/simple, 4 steps, no LoRA/upscale completed in 14.1 s after API readiness. It produced the strongest clean Anima face/body style in this round, but ignored the requested standing/full-body composition and chose a closer kneeling crop. Keep as a fast high-impact anime preset, not a strict composition preset.
- Anima base + Turbo + Niji 0.60 at 768x1152, 16 steps completed in 22.1 s. It produced richer semi-real rendering than Moody Anima but the front fingers remained slightly stiff/fused. Keep as a secondary detail-rich branch.
- Moody Z v13 adapted to the current author core (SDA 0.49, shift 3, DPM++ 2M SDE/beta, 9 steps, 640x960) is pose-sensitive. A seated torso-twist seed completed in 70.2 s but generated an extra hand and is rejected. A simplified standing pose with explicit exactly-two-hands constraints completed in 81.0 s and was clean, bright and anatomically coherent. SDA is not an anatomy repair tool; use simple poses and seed selection.
- Diving v7 res_2s/beta57, shift 3, 10 steps at 576x800 completed in 78.3 s and produced the most natural bright photoreal skin in this round. The exact seed `72426044` is clean and replaces the previously rejected elongated-hand Diving seed for this prompt direction.
- aMix + Ri-mix 0.65 at 768x1152, Euler A/normal, 30 steps completed in 28.1 s and was the best balanced full adult-anime result: clean pose, coherent hands, strong face and restrained stylization. Retain as the default adult-anime graph.
- OneObsession v2.3 at 832x1216, DPM++ 2M/Karras, 32 steps completed in 28.2 s. It was the most exaggerated/glossy and visually forceful result; retain as the stylized/curvy branch, not the anatomy-neutral default.
- Current selection order for this target: aMix + Ri-mix 0.65 for balanced anime; Moody Anima 4-step for fast high-impact anime; OneObsession for exaggerated stylized anime; Moody Z + SDA only with simple pose; Diving res_2s for natural photoreal skin.

## Advanced Telegram/Civitai cinematic validation — 2026-07-24

- Evidence/report: `C:\AI\workflows\TG_CIVITAI_ADV_CINEMATIC_20260724\REPORT.html`. Eight primary SFW/adult-NSFW images plus two controlled prompt corrections ran in fresh per-image processes, native resolution, no upscale/detailer. The six retained outputs are copied non-destructively to `SELECTED`.
- Installed and SHA256-verified Civitai `Ri-mix α (Anima)` version 3011920 as `rimixao5050.safetensors` (504.2 MB; SHA256 `03EE210C6F390080B16A142A142C0848BB856877A7422D1B3637635F2E4FD8C6`). The author recommends Anima ER-SDE, CFG 3 and 30–40 steps; local validation used Anima base + LoRA 0.70, ER-SDE/simple, 32 steps, CFG 3, 768x1152.
- Anima + Ri-mix α was the strongest HQ cinematic direction. SFW/clean-corrected NSFW completed in 66.1/66.2 s. It produced true foreground/midground/background depth, wet reflections, controlled cyan/amber separation and richer hair/fabric than Moody Anima. Its initial NSFW output added wrist rope; explicitly assigning the woman's left and right hands to different cushions and excluding rope/restraint/bondage removed it without changing the seed.
- Moody Anima 4-step remained the speed leader at 16.1/12.0 s for cinematic SFW/NSFW. Scene grammar and bokeh were valid, but the SFW face/materials were flatter than Ri-mix α. Use Moody Anima for drafts and Ri-mix α for HQ cinematic.
- aMix + Ri-mix Ω 0.65 remained the most balanced SDXL/Illustrious cinematic pair at 32.1/26.1 s. Its SFW rain/alley scene had strong layered depth, silk, wet pavement, moon/lantern separation and a plausible hand/bag adaptation. NSFW was clean and smooth but partially hid hands at the chaise edges.
- OneObsession v23 failed the wide walking cinematic composition twice with the same seed. The first output added disembodied POV hands; a controlled prompt correction banning POV/foreground hands changed the artifact into disembodied POV legs. Stop this branch rather than seed-grinding. Keep OneObsession for its proven close/high-contrast stylized role, not as the default wide cinematic model. Its NSFW output remained visually forceful but added cloth-in-mouth, jewelry and overlapping hands, so it is conditional only.
- Reusable cinematic prompt structure: environmental foreground only; clearly identified subject in the midground; layered background bokeh/architecture; motivated warm practical key; cool rim; broad neutral face fill; smooth highlight roll-off; gentle halation; restrained 35mm grain; controlled complementary color grade; lens and camera distance. Merely adding the word `cinematic` is insufficient.
- Anatomy/composition correction: `exactly two hands visible` can still provoke extra viewer limbs. Prefer possessive, spatial constraints such as `her left hand on the left cushion; her right hand on the right cushion`, explicitly exclude POV/disembodied human parts, and avoid mentioning generic human foreground elements.
- Current cinematic selection order: aMix + Ri-mix Ω 0.65 for balanced/default pair; Anima + Ri-mix α for best HQ depth/detail; Moody Anima 4-step for fast draft; OneObsession only for close stylized scenes.

## Civitai/Telegram style expansion round 2 — 2026-07-24

- Evidence/report: `C:\AI\workflows\STYLE_EXPANSION_CIVITAI_TG_20260724\REPORT_ROUND2.html`. Five genuinely different model/LoRA branches were run in isolated processes at native resolution with no upscale or detailer. The four retained outputs are in `SELECTED_ROUND2`.
- The user explicitly rejected the earlier `STYLEX-A1_GOTHIC_NEON`, `STYLEX-A2_DARK_ART`, and `STYLEX-A4_DRAMATIC_DAPPLED` outputs. They are blacklisted in `visual_gate.py` and must not be reused as visual targets.
- Hassaku XL Illustrious v3.4 was the best match to the desired bright, glossy, voluptuous adult-anime direction. It completed in 30.1 s and kept a clean face, readable body design, warm/cool lounge lighting and usable hands. Use it as the first new style branch.
- Anima Myth Portrait produced the richest semi-real fantasy rendering and scene depth. It completed in 68.2 s. Retain for luxurious/fantasy portrait work; inspect nails and hands because they were slightly less precise than the face and fabric.
- CoMix b3 completed in 28.1 s and established a useful separate comic/superhero branch: clean full-body composition, bright color, coherent city depth and readable hands. Do not mix its graphic look into photoreal or soft-anime comparisons.
- BunnySlop v404 completed in 64.2 s and was technically clean, bright and curvy, but flatter and simpler than Hassaku/Myth Portrait. Keep as a secondary candidate rather than a leader.
- `STYLEX2-B2_ANIMA_REALISM_V2` is rejected despite an attractive face: the crop is too close and the beauty-filter skin is overly smooth/waxy. It is now blacklisted. Do not promote results solely because they are bright and clean.

## Anima Realism v2 prompt-upgrade stress test — 2026-07-24

- Evidence/report: `C:\AI\workflows\STYLE_EXPANSION_CIVITAI_TG_20260724\REPORT_ANIMA_REALISM_UPGRADE6.html`. Six isolated 768x1152 images used the author's Anima ER-SDE/simple 32-step path, LoRA reduced from 0.72 to 0.50, no upscale or detailer, and prompts explicitly controlling face/chest/waist/hips/buttocks, framing and hand placement.
- All six completed in 64.1–66.2 s and passed the simple pixel/edge gate, but full-size review showed that the LoRA's waxy beauty-filter skin persists even at 0.50. Prompt wording improved composition but did not repair the material character of skin.
- `01_SEATED_THREEQUARTER` is the best front three-quarter prompt composition and `05_KNEELING_SIDE` is the cleanest curvy side composition. `06_CLOSE_CURVE_BALANCED` has clean symmetric hands but remains mannequin-like. Keep these only as pose/prompt references, not visual leaders.
- Explicitly reject and blacklist `02_STANDING_BODYCON` for a duplicated arm/hand plus fake text, `03_REAR_THREEQUARTER` for fake text and unreliable contact anatomy, and `04_RECLINED_DIAGONAL` for three visible hands.
- Final model decision: stop iterating `realism-anima-v2` for the bright detailed-skin target. Transfer the successful spatial prompt grammar to Hassaku v3.4, Anima Myth Portrait, aMix + Ri-mix 0.65, or OneObsession instead.
## Moody realtime + node-discovery corrective batch — 2026-07-26

- Evidence/report: `C:\AI\workflows\NODE_DISCOVERY_20260726\REPORT.html` and `C:\AI\workflows\DIVERSE_PROMPT_BATCH10_20260726\REPORT.html`.
- User explicitly rejected the main Node Discovery Z outputs `NDISC-01_Z_RAW_EULER_BETA9_SHIFT5`, `NDISC-03_Z_EULERFLOW_DD012`, `NDISC-04_Z_REALSNAP_LORA012`, and `NDISC-05_Z_RENDERDETAIL_LORA010`: skin looked dark/smudged/soft, face was not clearly beautiful enough, and the visual direction repeated the same sofa/rain nude close-up too much. Do not promote these as baselines.
- Specific avoid rules from this failure: do not default Z-Image to `shift 5 + beta9` for this target; do not add DetailDaemon or rendering/detail LoRA to Z as a generic quality fix; do not use `RealisticSnapshot` LoRA around 0.12 for this soft indoor glamour look; do not assume more nodes means better output.
- Better corrective direction from `DIVERSE_PROMPT_BATCH10_20260726`: diversify prompts first. Test high-key white studio, clean street flash, morning-window portrait, clean studio, bright SDXL window portrait, Ri-mix daylight, OneObsession pink studio, Ri-mix/Anima gold window, and Hassaku clean anime. No upscale was used.
- Visual read of DP10 contact sheet: `DP10-01_Z_MOODY_HIGHKEY_WHITE` is the best Z corrective photo direction so far: brighter, cleaner, less muddy than NDISC. `DP10-05_SDXL_INTO_BRIGHT_PORTRAIT` and `DP10-06_SDXL_REALVIS_SKIN` are clean bright photo alternatives, but still need full-size face/skin review. `DP10-07_RIMIX_DAYLIGHT_CHARM`, `DP10-08_ONEOBS_PINK_STUDIO`, `DP10-09_ANIMA_RIMIX_GOLD_WINDOW`, and `DP10-10_HASSAKU_CLEAN_ANIME` are stronger anime/semi-real directions than the rejected gothic/dark/dappled experiments.
- Current prompt lesson: for the user's preferred result, avoid a single repetitive couch/rain/glamour prompt. Use varied scene grammar with bright high-key or soft daylight, clear face lighting, exact hand placement, controlled camera distance, clean hair/eye/fabric detail, and compact negatives for muddy skin, waxy skin, oil-paint smear, dark underexposure, extra fingers, and asymmetry.

## Telegram/model expansion with Z LoRA loader — 2026-07-26

- Evidence/report: `C:\AI\workflows\TELEGRAM_MODEL_EXPAND_20260726\REPORT.html`.
- Installed `Comfyui-ZiT-Lora-loader` from GitHub to test architecture-aware Z-Image Turbo LoRA loading. The node solves the fused-QKV mismatch problem described by its README, but local visual/runtime results do not justify making Z LoRA stacks the default.
- Downloaded Hugging Face `diobrando0/realstagram-zimg` file `REALSTAGRAM_ZIMG.safetensors` (~325 MiB) to `C:\AI\ComfyUI\models\loras\huggingface_20260726`. It loaded only after restarting ComfyUI because the Z LoRA node's dropdown is populated at startup.
- Z tests with the new loader completed but were slow: `TME-01_Z_MOODY_SPECIAL_HANDS_ZIB` 219.2 s, `TME-02_Z_MOODY_GIRLSLIKE_LIGHT` 210.0 s, `TME-03_Z_DIVING_MYTH_REALISTICF` 123.2 s, `TME-07_Z_REALSTAGRAM_018` 189.1 s. `TME-08_Z_REALSTAGRAM_028` timed out with no output. These did not beat Moody native `res_2s`/Euler H4 for the user's bright youthful skin target.
- Important path rule: this node validates `lora_name` against ComfyUI's Windows-style dropdown entries. Use backslashes for subfolders, e.g. `zimage\\girlslike_zi_mzy.safetensors`; files downloaded after ComfyUI startup require a restart before the node sees them.
- Best visual direction from this round: `TME-05_ANIMA_RIMIXA_EXPOSURE_LIGHT` (Ri-mix alpha Anima + exposure lighting LoRA, 68.4 s) for polished rainy-window cinematic anime; secondary `TME-04_ANIMA_MOODY_PLUS_MYTHPORTRAIT` (56.2 s) for brighter Moody/portrait anime. Keep these as Telegram-style candidates.
- Rejected/secondary: `TME-06_SDXL_HASSAKU_RIMIX_AUTHORISH` is too misty/soft; do not promote. The Z LoRA loader remains a research tool for specific LoRA compatibility, not a quality default.
