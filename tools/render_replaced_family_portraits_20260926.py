from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
archive = root / "tools" / "medieval_portrait_removal_20260925" / "originals"
output = root / "tools" / "general_portrait_medieval_audit_20260925" / "replaced_original_family_portraits.png"
items = [
    ("Northern wife", archive / "northern_european/family/wife.tga"),
    ("Northern daughter", archive / "northern_european/family/daughter.tga"),
    ("Southern wife", archive / "southern_european/family/wife.tga"),
    ("Southern daughter", archive / "southern_european/family/daughter.tga"),
    ("Slavic wife", archive / "slavic/family/wife.tga"),
    ("Slavic daughter", archive / "slavic/family/daughter.tga"),
    ("African wife", archive / "mesoamerican/family/wife.tga"),
    ("African daughter", archive / "mesoamerican/family/daughter.tga"),
    ("African son", archive / "mesoamerican/family/son.tga"),
]

font = ImageFont.load_default()
cell_w, cell_h = 150, 135
sheet = Image.new("RGB", (3 * cell_w, 3 * cell_h + 30), "#28241f")
draw = ImageDraw.Draw(sheet)
draw.text((8, 8), "Original family portraits that were replaced", fill="white", font=font)
for i, (label, path) in enumerate(items):
    x = (i % 3) * cell_w
    y = 30 + (i // 3) * cell_h
    with Image.open(path) as src:
        rgba = src.convert("RGBA")
        backdrop = Image.new("RGBA", rgba.size, "#B8AD8F")
        backdrop.alpha_composite(rgba)
        portrait = backdrop.convert("RGB").resize((69, 96), Image.Resampling.NEAREST)
    sheet.paste(portrait, (x + 40, y + 24))
    draw.text((x + 8, y + 7), label, fill="white", font=font)
sheet.save(output)
print(output)
