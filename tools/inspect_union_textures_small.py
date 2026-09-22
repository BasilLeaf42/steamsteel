from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
sources = [
    root / "data/unit_models/_Units/bnw/textures/fra_qishou_port.texture",
    root / "data/unit_models/_Units/bnw/textures/france_flag_port.texture",
]
canvas = Image.new("RGB", (256, 144), (30, 30, 30))
draw = ImageDraw.Draw(canvas)
for index, source in enumerate(sources):
    dds = root / "tools" / f"_small_{source.stem}.dds"
    dds.write_bytes(source.read_bytes()[48:])
    image = Image.open(dds).convert("RGB")
    image.thumbnail((128, 128))
    canvas.paste(image, (index * 128, 16))
    draw.text((index * 128 + 2, 2), source.stem, fill="white")
canvas.save(root / "tools" / "_inspect_union_small.jpg", quality=65)
