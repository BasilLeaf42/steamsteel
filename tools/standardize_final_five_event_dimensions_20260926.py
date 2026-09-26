from pathlib import Path
import shutil

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tools" / "event_screen_replacement_20260926"
SMALL_BACKUP = WORK / "legacy_size_replacements"
NAMES = [
    "timurids_invasion_warn.tga",
    "football_banned.tga",
    "gunpowder_discovered.tga",
    "grote_mandenke.tga",
    "world_is_round.tga",
]
INNER = (47, 13, 389, 137)
INNER_SIZE = (INNER[2] - INNER[0], INNER[3] - INNER[1])


def cover_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    width, height = size
    ratio = max(width / image.width, height / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


for name in NAMES:
    source_path = WORK / "sources" / (Path(name).stem + ".img")
    with Image.open(source_path) as opened:
        artwork = cover_crop(opened.convert("RGB"), INNER_SIZE)
    artwork = ImageEnhance.Contrast(artwork).enhance(1.04).convert("RGBA")

    for target in sorted((ROOT / "data" / "ui").glob(f"*/eventpics/{name}")):
        relative = target.relative_to(ROOT)
        backup = SMALL_BACKUP / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copy2(target, backup)

        donor = target.parent / "RAILWAY_BOOM.tga"
        if not donor.exists():
            donor = next((ROOT / "data" / "ui").glob("*/eventpics/RAILWAY_BOOM.tga"))
        with Image.open(donor) as opened:
            framed = opened.convert("RGBA")
        if framed.size != (435, 155):
            raise ValueError(f"Unexpected canonical frame dimensions: {donor} {framed.size}")
        framed.paste(artwork, INNER[:2])
        framed.save(target, format="TGA")

preview = Image.new("RGB", (900, 540), "#28241f")
draw = ImageDraw.Draw(preview)
font = ImageFont.load_default()
draw.text((8, 8), "Final five event screens standardized to 435 x 155", fill="white", font=font)
for index, name in enumerate(NAMES):
    target = next((ROOT / "data" / "ui").glob(f"*/eventpics/{name}"))
    with Image.open(target) as opened:
        rgba = opened.convert("RGBA")
        backdrop = Image.new("RGBA", rgba.size, "#28241f")
        backdrop.alpha_composite(rgba)
        image = backdrop.convert("RGB")
    x = 8 + (index % 2) * 445
    y = 30 + (index // 2) * 168
    preview.paste(image, (x, y + 15))
    draw.text((x, y), name, fill="white", font=font)
preview.save(WORK / "installed_contact_sheet_435x155.png")
print("Standardized five event screens to 435x155 using the exact canonical aperture (47,13)-(389,137).")
