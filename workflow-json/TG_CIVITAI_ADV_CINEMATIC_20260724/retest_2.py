import csv
import importlib.util
import json
from pathlib import Path

module_path = Path(__file__).with_name("run_8.py")
spec = importlib.util.spec_from_file_location("run_8", module_path)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

ANIMA_CLEAN_NSFW = (
    "masterpiece, best quality, very aesthetic, sensual smooth cinematic anime film still, "
    "one clearly adult East Asian woman age 28, solo, completely nude adult figure, seated "
    "upright on a white silk chaise beside a tall rain-streaked window, youthful adult oval "
    "face, long glossy black hair, voluptuous soft curvy adult body, large natural breasts "
    "and adult pubic anatomy visible, torso facing camera with a gentle three-quarter turn, "
    "her left hand open on the left cushion and her right hand open on the right cushion, "
    "wrists separated and unobstructed, natural fingers, no rope, no restraints, no bondage, "
    "no jewelry, no props, foreground sheer curtain edge only, warm practical lamps and rainy "
    "city bokeh in the background, soft amber motivated side key, cool blue window rim, broad "
    "pearl-white face fill, smooth tonal roll-off, gentle halation, subtle 35mm film grain, "
    "restrained highlights, coherent adult anatomy, cinematic vertical composition, no text, "
    "no watermark, no child, no teen, no loli"
)

ONEOBS_CLEAN_SFW = (
    "masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, smooth "
    "cinematic anime film still, layered depth of field, adult, aged up, one clearly adult "
    "East Asian woman age 27, solo, full body, youthful oval adult face, warm brown eyes, "
    "long black hair moving in rain, fitted black blazer, deep-red silk dress, walking toward "
    "the camera through a quiet old-city alley at blue hour, both of her arms hanging naturally "
    "down, her own left hand beside her left thigh and her own right hand beside her right thigh, "
    "no other people near the camera, no POV, no foreground hands, foreground rain streaks and "
    "wet pavement reflections, subject in the midground, layered amber lantern bokeh and misty "
    "architecture behind her, motivated amber shop-window key light, cool moon rim light, broad "
    "soft face fill, smooth highlight roll-off, gentle halation, subtle 35mm film grain, "
    "controlled teal and amber color grade, 50mm lens, cinematic vertical frame, detailed silk "
    "and wet hair, refined eyes"
)

NEGATIVE_EXTRA = (
    r.NEGATIVE
    + ", first-person view, POV, foreground hands, disembodied hands, viewer hands, "
    "rope, wrist rope, restraint, bondage, gag, cloth in mouth"
)

jobs = []

g = r.build_anima_rimix(
    ANIMA_CLEAN_NSFW,
    72428022,
    "ADV8-A4B_ANIMA_RIMIX_ALPHA_NSFW_CLEAN",
)
jobs.append(("A4B_ANIMA_RIMIX_ALPHA_NSFW_CLEAN", "Anima", g))

g = r.build_illustrious(
    r.SOURCE_ONEOBS,
    ONEOBS_CLEAN_SFW,
    72428011,
    "ADV8-S3B_ONEOBSESSION_CINEMATIC_SFW_CLEAN",
)
g["3"]["inputs"]["text"] = NEGATIVE_EXTRA
jobs.append(("S3B_ONEOBSESSION_CINEMATIC_SFW_CLEAN", "SDXL/Illustrious", g))

rows = []
try:
    for index, (name, family, graph) in enumerate(jobs, 1):
        workflow = r.save_graph(name, graph)
        print(json.dumps({"event": "starting", "name": name}), flush=True)
        r.server("stop")
        r.server("start")
        elapsed, filename = r.queue(graph)
        result = r.gate.evaluate(r.IMAGES / filename)
        row = {
            "index": index,
            "name": name,
            "family": family,
            "elapsed_s": elapsed,
            "image": filename,
            "technical_pass": result["pass"],
            "gate": json.dumps(result, ensure_ascii=False),
            "workflow": str(workflow),
        }
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
finally:
    r.server("stop")
    if rows:
        with (r.OUT / "retest_results.csv").open(
            "w", newline="", encoding="utf-8-sig"
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
