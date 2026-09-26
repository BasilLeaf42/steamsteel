from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / "general_portrait_medieval_audit_20260925"
POOLS = (
    "northern_european",
    "southern_european",
    "middle_eastern",
    "chinese",
    "mesoamerican",
    "slavic",
)

OUT.mkdir(parents=True, exist_ok=True)
font = ImageFont.load_default()

for pool in POOLS:
  for role in ("generals", "pagan_generals", "civilians", "rogues"):
    folder = ROOT / "data" / "ui" / pool / "portraits" / "portraits" / "young" / role
    files = sorted(folder.glob("*.tga"), key=lambda p: (int(p.stem.split()[0]), p.name))
    if not files:
        continue
    cols, cell_w, cell_h = 10, 86, 120
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h + 24), "#28241f")
    draw = ImageDraw.Draw(sheet)
    draw.text((6, 6), f"{pool}: every young {role} portrait ({len(files)})", fill="white", font=font)
    for i, path in enumerate(files):
        x = (i % cols) * cell_w
        y = 24 + (i // cols) * cell_h
        with Image.open(path) as source:
            image = source.convert("RGBA")
            backdrop = Image.new("RGBA", image.size, "#B8AD8F")
            backdrop.alpha_composite(image)
            thumb = backdrop.convert("RGB").resize((69, 96), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x + 8, y + 16))
        draw.text((x + 8, y + 2), path.stem, fill="white", font=font)
    sheet.save(OUT / f"{pool}_all_young_{role}.png")

print(OUT)

family_sheet = Image.new("RGB", (6 * 110, 3 * 130 + 24), "#28241f")
family_draw = ImageDraw.Draw(family_sheet)
family_draw.text((6, 6), "Living family portraits by pool: wife, daughter, son", fill="white", font=font)
for col, pool in enumerate(POOLS):
    for row, filename in enumerate(("wife.tga", "daughter.tga", "son.tga")):
        path = ROOT / "data" / "ui" / pool / "portraits" / "family" / filename
        if not path.exists():
            continue
        with Image.open(path) as source:
            image = source.convert("RGBA")
            backdrop = Image.new("RGBA", image.size, "#B8AD8F")
            backdrop.alpha_composite(image)
            thumb = backdrop.convert("RGB").resize((69, 96), Image.Resampling.LANCZOS)
        x, y = col * 110 + 20, row * 130 + 40
        family_sheet.paste(thumb, (x, y))
        family_draw.text((col * 110 + 4, y - 14), f"{pool[:8]} {filename[:-4]}", fill="white", font=font)
family_sheet.save(OUT / "all_family_portraits.png")
