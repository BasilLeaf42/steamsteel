from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
names = [
    "black_death_1.tga", "black_death_2.tga", "black_death_3.tga", "black_death_4.tga", "black_death_hits.tga",
    "earthquake_in_aleppo.tga", "earthquake_in_alexandria.tga", "earthquake_in_alexandria_2.tga", "earthquake_in_naples.tga", "earthquake_in_silicia.tga",
    "first_european_paper.tga", "first_eyeglasses.tga", "first_magnetic_compass.tga", "first_mechanical_clock.tga", "first_oil_painting.tga",
    "first_piano.tga", "first_printing_press.tga", "first_public_clock.tga", "first_sawmill.tga", "first_wheelbarrow.tga", "first_windmill.tga",
    "science_alchemy_book.tga", "science_de_docta_ignorantia.tga", "science_weather_forecast.tga",
    "mongols_invasion_warn.tga", "timurids_invasion_warn.tga", "football_banned.tga", "gunpowder_discovered.tga", "grote_mandenke.tga", "world_is_round.tga",
]
cultures = ["southern_european", "northern_european", "middle_eastern", "slavic", "asian", "chinese", "mesoamerican"]
resolved = []
for name in names:
    match = next((root / "data/ui" / culture / "eventpics" / name for culture in cultures if (root / "data/ui" / culture / "eventpics" / name).exists()), None)
    if match is None:
        raise FileNotFoundError(name)
    resolved.append((name, match))

cols, cell_w, cell_h = 3, 410, 170
rows = (len(resolved) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell_w, rows * cell_h + 34), "#28241f")
draw = ImageDraw.Draw(sheet)
font = ImageFont.load_default()
draw.text((8, 10), "Current inherited medieval event screens proposed for later replacement (no replacements selected)", fill="white", font=font)
for i, (name, path) in enumerate(resolved):
    x = (i % cols) * cell_w
    y = 34 + (i // cols) * cell_h
    with Image.open(path) as src:
        image = src.convert("RGB")
        image.thumbnail((390, 130), Image.Resampling.LANCZOS)
    sheet.paste(image, (x + (cell_w - image.width) // 2, y + 26))
    draw.text((x + 8, y + 7), name, fill="white", font=font)

output = root / "tools" / "medieval_event_replacement_candidates_20260926.png"
sheet.save(output)
print(output)
