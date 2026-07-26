from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import re

SOURCE = Path(r"C:\Users\Admin\Downloads\Telegram Desktop\ChatExport_2026-07-23\photos")
OUT = Path(__file__).parent / "CONTACTS"
OUT.mkdir(parents=True, exist_ok=True)

groups = defaultdict(list)
for path in SOURCE.iterdir():
    if "_thumb" in path.stem.lower() or path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue
    match = re.search(r"@(\d{2}-\d{2}-\d{4})_", path.name)
    if match:
        groups[match.group(1)].append(path)

font = ImageFont.load_default()
for day, files in sorted(groups.items()):
    files.sort()
    count = min(60, len(files))
    indices = [round(i * (len(files) - 1) / max(1, count - 1)) for i in range(count)]
    chosen = [files[i] for i in indices]
    cell_w, cell_h, label_h, cols = 220, 300, 24, 10
    rows = (len(chosen) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * (cell_h + label_h)), "#111")
    draw = ImageDraw.Draw(sheet)
    for position, path in enumerate(chosen):
        with Image.open(path) as source:
            image = source.convert("RGB")
            image.thumbnail((cell_w, cell_h), Image.Resampling.LANCZOS)
        x = (position % cols) * cell_w + (cell_w - image.width) // 2
        y = (position // cols) * (cell_h + label_h) + (cell_h - image.height) // 2
        sheet.paste(image, (x, y))
        short = path.stem.split("@", 1)[0].replace("photo_", "")
        draw.text((position % cols * cell_w + 5, y + image.height + 4), short, fill="white", font=font)
    sheet.save(OUT / f"{day}.jpg", quality=88)
    print(day, len(files), OUT / f"{day}.jpg")

overview_files = sorted(OUT.glob("??-??-2026.jpg"))
overview = Image.new("RGB", (1600, len(overview_files) * 255), "#111")
overview_draw = ImageDraw.Draw(overview)
for row, path in enumerate(overview_files):
    with Image.open(path) as source:
        preview = source.convert("RGB")
        preview.thumbnail((1500, 230), Image.Resampling.LANCZOS)
    overview.paste(preview, (100, row * 255 + 20))
    overview_draw.text((8, row * 255 + 20), path.stem[:5], fill="white", font=font)
overview.save(OUT / "OVERVIEW_ALL_DAYS.jpg", quality=90)
