# Verdict -- 2026-07-26

Batch goal: adult-only NSFW Anima/SDXL/Illustrious images in the Civitai/Telegram direction, with exposed high-impact posing, no upscale, and no heavy full-image scaling.

## Keep

1. `CANP-05_ONEOBS_LOCKED_SOFA_00001_.png`
   - Best high-impact/curvy/glossy adult anime result.
   - Continue from locked OneObsession S4-style scenes: ornate sofa, rain window, warm lamp, close composition.

2. `CANP-01_ANIMA_WINDOW_CHAISE_00001_.png`
   - Best Anima cinematic window/chaise variant.
   - Good blue rain + warm lamp depth, polished skin/fabric.

3. `CANP-03_ANIMA_MIRROR_STAND_00001_.png`
   - Best standing/mirror-room Anima variant.
   - Good pose diversity and premium room lighting.

4. `CANP-06_AMIX_RIMIX_SILK_SOFA_00001_.png`
   - Clean balanced SDXL/Illustrious option.
   - Less extreme than OneObsession but useful for elegant adult-anime style.

5. `CANP-07_HASSAKU_BRIGHT_LOUNGE_00001_.png`
   - Secondary bright/curvy anime preset.
   - Keep as a variation, not the main winner.

## Reject / secondary

- `CANP-02_ANIMA_KNEEL_WINDOW`: acceptable but too mild.
- `CANP-04_ANIMA_EDGE_BED`: visually strong but more game-like/plastic.
- `CANP-08_WAI_CLEAN_MIRROR`: clean but too simple and less premium.

## Rule for next runs

Do not add random Civitai character LoRAs just because they are popular. For this target, stay with:

- OneObsession v23 close high-impact scenes.
- Ri-mix alpha Anima + exposure lighting LoRA for cinematic Telegram-style depth.
- aMix + Ri-mix 0.65 for clean balanced SDXL/Illustrious.
- Hassaku only as a bright secondary anime branch.

No upscale/detailer by default. Add one node only when it fixes a specific visible defect.
