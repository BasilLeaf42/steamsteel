from collections import deque
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "tools/card_generation_sources"
TARGET_DIR = ROOT / "data/ui/units/turks"
CANONICAL = (184, 173, 143, 255)
REGISTER = json.loads((ROOT / "tools/historical_card_sources.json").read_text(encoding="utf-8"))
BY_ID = {record["id"]: record for record in REGISTER}
REQUIRED_SOURCE_FIELDS = (
    "source_url", "source_file", "source_title", "creator", "source_date",
    "licence", "depicted_subject", "mapping_note", "generated_file",
)

def is_background(pixel):
    r, g, b, _ = pixel
    if pixel == CANONICAL:
        return True
    return (
        r >= 140
        and g >= 125
        and b >= 90
        and 12 <= r - g <= 40
        and 18 <= g - b <= 60
    )

def normalize_background(image):
    image = image.convert("RGBA")
    pixels = image.load()
    width, height = image.size
    queue = deque()
    seen = set()
    for x in range(width):
        queue.extend(((x, 0), (x, height - 1)))
    for y in range(height):
        queue.extend(((0, y), (width - 1, y)))
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if not is_background(pixels[x, y]):
            continue
        pixels[x, y] = CANONICAL
        if x: queue.append((x - 1, y))
        if x + 1 < width: queue.append((x + 1, y))
        if y: queue.append((x, y - 1))
        if y + 1 < height: queue.append((x, y + 1))
    return image

def approved_record(record_id, source, crop, members):
    record = BY_ID.get(record_id)
    if not record or record.get("status") != "card-approved":
        raise SystemExit(f"{record_id}: source mapping is missing or unapproved")
    missing = [field for field in REQUIRED_SOURCE_FIELDS if not str(record.get(field, "")).strip()]
    if missing:
        raise SystemExit(f'{record_id}: incomplete source mapping: {", ".join(missing)}')
    if record["generated_file"] != f"tools/card_generation_sources/{source}":
        raise SystemExit(f"{record_id}: generated_file does not match installer source")
    if record.get("crop_box") != list(crop):
        raise SystemExit(f"{record_id}: crop_box does not match installer crop")
    if record.get("shared_members", [record.get("unit_type")]) != members:
        raise SystemExit(f"{record_id}: shared_members do not match installer targets")
    for field in ("source_file", "generated_file"):
        if not (ROOT / record[field]).is_file():
            raise SystemExit(f"{record_id}: missing {field}: {record[field]}")


def install(record_id, source, crop, members):
    approved_record(record_id, source, crop, members)
    image = Image.open(SOURCE_DIR / source).convert("RGBA").crop(crop)
    image = normalize_background(image).resize((48, 64), Image.Resampling.LANCZOS)
    image = normalize_background(image)
    for member in members:
        target = TARGET_DIR / f"#{member}.tga"
        image.save(target, format="TGA", bits=32, compression="tga_rle")
        check = Image.open(target).convert("RGBA")
        border = [(x, y) for y in range(48) for x in range(48) if x < 2 or x >= 46 or y < 2]
        background_fraction = sum(check.getpixel(point) == CANONICAL for point in border) / len(border)
        if check.size != (48, 64) or target.read_bytes()[16] != 32:
            raise SystemExit(f"{member}: tactical-card dimensions or colour depth are invalid")
        if check.getchannel("A").getextrema() != (255, 255) or background_fraction < 0.5:
            raise SystemExit(f"{member}: tactical-card alpha or canonical background is invalid")

install("ott_general_staff", "ott_general_staff_master.png", (60, 0, 1026, 1288), ["ott_general_staff"])
install("ott_avci_shared", "ott_avci_master.png", (100, 100, 970, 1260), ["ott_avci_early", "ott_avci_mid", "ott_avci_high"])
install("ott_suvari_shared", "ott_suvari_master.png", (0, 0, 966, 1288), ["ott_suvari_early", "ott_suvari_mid", "ott_suvari_high"])
install("ott_hassa_suvarisi", "ott_hassa_suvarisi_pistol_master.png", (80, 0, 1046, 1288), ["ott_hassa_suvarisi"])
install("ott_mizrakli_suvari", "ott_mizrakli_suvari_lance_master.png", (0, 0, 1086, 1448), ["ott_mizrakli_suvari"])
for card in TARGET_DIR.glob("#ott_*.tga"):
    normalize_background(Image.open(card)).save(card, format="TGA", bits=32, compression="tga_rle")
print("Installed the approved Ottoman general, Avci, Suvari, Hassa Suvarisi and Mizrakli Suvari tactical cards.")
