"""Technical pre-filter for ComfyUI outputs.

This gate rejects known-bad sources and obvious technical failures. It does not
replace full-size visual inspection for face, skin, anatomy, crop, or aesthetics.
"""
from pathlib import Path
from PIL import Image, ImageFilter, ImageStat

REJECTED_PREFIXES = (
    "SDXL10-04_REAL04_INTO_FIXED_NSFW",
    "SDXL10-05_REAL05_REALVIS_SDE_SFW",
    "VF35-29_S3_REALVIS_C1_SFW",
    "VF35-30_S3_REALVIS_C2_SFW",
    "VF35-31_S3_REALVIS_C2_NSFW",
    "VF35-17_Z5_B_X21_C1_SFW",
    "VF35-18_Z5_B_X21_C1_NSFW",
    "VF35-21_S1_INTO_AUTHOR_C1_SFW",
    "SDXL10-01_REAL01_INTO_ULTRA",
    "SDXL10-02_REAL02_INTO_ULTRA",
    "FILTER5-04_FABRICATED_NSFW_A1",
    "ADV8-A1_MOODY_ANIMA_CINEMATIC_SFW",
    "ADV8-A2_MOODY_ANIMA_CINEMATIC_NSFW",
    "ADV8-A3_ANIMA_RIMIX_ALPHA_SFW",
    "ADV8-A4_ANIMA_RIMIX_ALPHA_NSFW",
    "ADV8-A4B_ANIMA_RIMIX_ALPHA_NSFW_CLEAN",
    "ADV8-S1_AMIX_RIMIX_CINEMATIC_SFW",
    "ADV8-S2_AMIX_RIMIX_CINEMATIC_NSFW",
    "ADV8-S3_ONEOBSESSION_CINEMATIC_SFW",
    "ADV8-S3B_ONEOBSESSION_CINEMATIC_SFW_CLEAN",
    "STYLEX-A1_GOTHIC_NEON",
    "STYLEX-A2_DARK_ART",
    "STYLEX-A4_DRAMATIC_DAPPLED",
    "STYLEX2-B2_ANIMA_REALISM_V2",
    "NDISC-01_Z_RAW_EULER_BETA9_SHIFT5",
    "NDISC-03_Z_EULERFLOW_DD012",
    "NDISC-04_Z_REALSNAP_LORA012",
    "NDISC-05_Z_RENDERDETAIL_LORA010",
    "ARUP6-",
    "ARUP6-02_STANDING_BODYCON",
    "ARUP6-03_REAR_THREEQUARTER",
    "ARUP6-04_RECLINED_DIAGONAL",
    "XHNSFW-01_NATIVE",
    "XHNSFW-02_FACEV8_HANDV8",
    "XHNSFW-FIX",
    "XHSCREEN-02_",
    "XHEYE-",
)


def evaluate(path):
    path = Path(path)
    if path.stem.startswith(REJECTED_PREFIXES):
        return {"pass": False, "reasons": ["explicit_user_reject"]}
    rgb = Image.open(path).convert("RGB")
    gray = rgb.convert("L")
    extrema = gray.getextrema()
    stats = ImageStat.Stat(gray)
    edge = gray.filter(ImageFilter.FIND_EDGES)
    edge_score = ImageStat.Stat(edge).var[0]
    reasons = []
    if extrema[1] <= 8 or stats.mean[0] <= 3:
        reasons.append("black_or_near_black")
    if stats.stddev[0] < 12:
        reasons.append("very_low_contrast")
    if edge_score < 80:
        reasons.append("technically_soft")
    return {
        "pass": not reasons,
        "reasons": reasons,
        "mean_luma": round(stats.mean[0], 2),
        "contrast": round(stats.stddev[0], 2),
        "edge_score": round(edge_score, 2),
        "size": [rgb.width, rgb.height],
    }
