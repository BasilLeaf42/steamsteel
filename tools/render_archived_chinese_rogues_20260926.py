from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
source = root / "tools" / "medieval_portrait_removal_20260925" / "originals" / "chinese" / "young" / "rogues"
output = root / "tools" / "general_portrait_medieval_audit_20260925" / "chinese_removed_original_rogues.png"
files = sorted(source.glob("*.tga"), key=lambda p: (int(p.stem.split()[0]), p.name))
cols, cell_w, cell_h = 10, 86, 120
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell_w, rows * cell_h + 24), "#28241f")
draw = ImageDraw.Draw(sheet)
font = ImageFont.load_default()
draw.text((6, 6), f"Removed original Chinese young rogue portraits ({len(files)})", fill="white", font=font)
for i, path in enumerate(files):
    x = (i % cols) * cell_w
    y = 24 + (i // cols) * cell_h
    with Image.open(path) as source_image:
        image = source_image.convert("RGBA")
        backdrop = Image.new("RGBA", image.size, "#B8AD8F")
        backdrop.alpha_composite(image)
        thumb = backdrop.convert("RGB").resize((69, 96), Image.Resampling.LANCZOS)
    sheet.paste(thumb, (x + 8, y + 16))
    draw.text((x + 8, y + 2), path.stem, fill="white", font=font)
sheet.save(output)
print(output)
