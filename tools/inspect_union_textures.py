from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    "data/unit_models/_Units/bnw/textures/fra_qishou_port.texture",
    "data/unit_models/_Units/bnw/textures/france_flag_port.texture",
    "data/unit_models/_Units/usa/textures/usa_inf_1g.texture",
    "data/unit_models/_Units/off/textures/usa_off_1g.texture",
]

images = []
for relative in SOURCES:
    source = ROOT / relative
    dds = ROOT / "tools" / f"_inspect_{source.stem}.dds"
    dds.write_bytes(source.read_bytes()[48:])
    image = Image.open(dds).convert("RGBA")
    image.thumbnail((512, 512))
    images.append((source.name, image.copy()))

width = max(image.width for _, image in images)
height = max(image.height for _, image in images)
output = Image.new("RGBA", (width * 2, height * 2), (30, 30, 30, 255))
draw = ImageDraw.Draw(output)
for index, (name, image) in enumerate(images):
    x = (index % 2) * width
    y = (index // 2) * height
    output.alpha_composite(image, (x, y))
    draw.text((x + 4, y + 4), name, fill="white")
output.save(ROOT / "tools" / "_inspect_union_textures.png")
