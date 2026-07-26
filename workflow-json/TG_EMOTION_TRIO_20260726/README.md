# Telegram emotion trio — 2026-07-26

Three model-native adult glamour workflows. No upscale and no whole-image
refiner was used.

## 01 — SDXL OneObsession blue pearl

- Source direction: local Telegram export, messages 68168 and 68659.
- Model-native baseline: approved OneObsession S4.
- 832x1216, DPM++ 2M/Karras, 32 steps, CFG 5.5, CLIP skip 2.
- Runtime: 34.4 s.
- Output: `TGTRIO-01-SDXL-BLUEPEARL_00001_.png`.
- Role: high-impact semi-real anime, rain-blue window, white sofa, veil and
  pearl jewelry, direct intimate gaze.

## 02 — Anima Ri-mix black lace

- Model-native baseline: Ri-mix alpha Anima author settings.
- 768x1152, ER-SDE/simple, 32 steps, CFG 3.
- Runtime: 68.5 s.
- Output: `TGTRIO-02-ANIMA-BLACKLACE_00001_.png`.
- Role: softer semi-real anime, over-shoulder affectionate expression, warm
  lamp/cool window separation, lace and sapphire details.

## 03 — Z-Image Moody rain intimate

- Model-native baseline: MoodyPro ZIT v13.2.
- 576x800, res_2s/beta57, 10 steps, CFG 1, shift 3.
- Runtime: 197.3 s cold outlier; image completed without node error or crash.
- Output: `TGTRIO-03-ZIMAGE-RAININTIMATE_00001_.png`.
- Role: photoreal close portrait, tender breathless expression, rain window,
  warm lamp, visible skin texture and coherent hands.

All three outputs passed the technical visual gate. Full-size human review is
still authoritative for face, eyes, hands, body shape and aesthetic preference.
