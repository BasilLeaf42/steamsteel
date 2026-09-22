from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
folder = root / "data/ui/units/portugala"
names = [
    "us_inf", "us_militia", "us_front_inf", "us_late_inf", "us_blacks",
    "us_colo_inf", "us_zouave", "berdan_inf", "union_irish_brigade",
    "us_scout_cav", "ap_front_cav", "us_front_cav", "apache_inf",
]
cell_w, cell_h = 144, 208
canvas = Image.new("RGB", (cell_w * 4, cell_h * 4), (40, 40, 40))
draw = ImageDraw.Draw(canvas)
for index, name in enumerate(names):
    image = Image.open(folder / f"#{name}.tga").convert("RGBA")
    image = image.resize((144, 192), Image.Resampling.NEAREST)
    x, y = (index % 4) * cell_w, (index // 4) * cell_h
    canvas.paste(image.convert("RGB"), (x, y))
    draw.text((x + 2, y + 193), name, fill="white")
canvas.save(root / "tools" / "_inspect_union_cards.jpg", quality=78)
