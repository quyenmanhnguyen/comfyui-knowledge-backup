# MAIN10 NSFW workflow pack -- 2026-07-26

Adult-only selected workflows. Native resolution, no upscale by default.

| Rank | Workflow | Family | Role | Reference |
|---:|---|---|---|---|
| 1 | `01_ONEOBSESSION_HIGH_IMPACT_SOFA.json` | SDXL / Illustrious checkpoint | Main high-impact glossy curvy adult-anime NSFW. Best current hở/căng/ấn tượng branch. | `CANP-05_ONEOBS_LOCKED_SOFA_00001_.png` |
| 2 | `02_ANIMA_RIMIX_WINDOW_CHAISE.json` | Anima / Qwen diffusion | Cinematic Anima chaise/window NSFW. | `CANP-01_ANIMA_WINDOW_CHAISE_00001_.png` |
| 3 | `03_ANIMA_RIMIX_MIRROR_STAND.json` | Anima / Qwen diffusion | Standing/mirror-room premium Anima NSFW. | `CANP-03_ANIMA_MIRROR_STAND_00001_.png` |
| 4 | `04_AMIX_RIMIX_BALANCED_SILK.json` | SDXL / Illustrious checkpoint + Ri-mix LoRA | Balanced clean semi-real anime NSFW. | `CANP-06_AMIX_RIMIX_SILK_SOFA_00001_.png` |
| 5 | `05_HASSAKU_BRIGHT_CURVY_LOUNGE.json` | SDXL / Illustrious checkpoint | Bright clean curvy anime secondary. | `CANP-07_HASSAKU_BRIGHT_LOUNGE_00001_.png` |
| 6 | `06_ANIMA_RIMIX_EXPOSURE_TELEGRAM.json` | Anima / Qwen diffusion | Telegram-style polished rainy-window Anima baseline. | `TME-05_ANIMA_RIMIXA_EXPOSURE_LIGHT_00001_.png` |
| 7 | `07_ANIMA_MOODY_MYTH_PORTRAIT.json` | Anima / Moody Anima + portrait LoRA | Fast brighter Anima portrait/beauty branch. | `TME-04_ANIMA_MOODY_PLUS_MYTHPORTRAIT_00001_.png` |
| 8 | `08_INTOREALISM_PHOTOREAL_ADULT_STUDY.json` | SDXL photoreal checkpoint | Photoreal adult figure-study fallback. | `SDXL10-FIX-01_REAL02_INTO_AUTHOR_NSFW_00001_.png` |
| 9 | `09_ZIMAGE_MOODY_RES2S_PHOTOREAL.json` | Z-Image / MoodyPro diffusion | Z-Image photoreal youthful bright NSFW. | `ZFINAL10-06_Z3_MOODY_RES2S_NSFW_00001_.png` |
| 10 | `10_WAI_CLEAN_MIRROR_ANIME.json` | SDXL / WAI Illustrious checkpoint | Clean simple anime mirror variation. | `CANP-08_WAI_CLEAN_MIRROR_00001_.png` |

## Use rules

- Start with #1 OneObsession for hở/căng/high-impact adult anime.
- Use #2/#3/#6 for Anima cinematic/rain/window/Telegram-style depth.
- Use #4 for clean balanced semi-real anime.
- Use #8 for photoreal SDXL, and #9 for Z-Image photoreal.
- Do not add upscale/detailer by default. Add one repair node only after a visible defect.
- Do not retry rejected branches: realism-anima-v2, gothic/neon/dark/dappled, Z LoRA stacks, DetailDaemon Z, RealisticSnapshot Z for sofa glamour.