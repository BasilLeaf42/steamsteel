from collections import deque
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "tools" / "card_generation_sources"
TARGET_DIR = ROOT / "data" / "ui" / "units" / "golden"
REGISTER = json.loads((ROOT / "tools" / "historical_card_sources.json").read_text(encoding="utf-8"))
BY_ID = {record["id"]: record for record in REGISTER}
CANONICAL = (184, 173, 143, 255)
REQUIRED = (
    "source_url", "source_file", "source_title", "creator", "source_date",
    "licence", "depicted_subject", "mapping_note", "generated_file",
)


def is_background(pixel):
    r, g, b, _ = pixel
    if pixel == CANONICAL:
        return True
    return 130 <= r <= 220 and 115 <= g <= 210 and 80 <= b <= 190 and -5 <= r - g <= 45 and 0 <= g - b <= 70


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
        if x:
            queue.append((x - 1, y))
        if x + 1 < width:
            queue.append((x + 1, y))
        if y:
            queue.append((x, y - 1))
        if y + 1 < height:
            queue.append((x, y + 1))
    return image


def approved(record_id, source, crop, members):
    record = BY_ID.get(record_id)
    if not record or record.get("status") != "card-approved":
        raise SystemExit(f"{record_id}: source mapping is missing or unapproved")
    missing = [field for field in REQUIRED if not str(record.get(field, "")).strip()]
    if missing:
        raise SystemExit(f"{record_id}: incomplete source mapping: {', '.join(missing)}")
    if record["generated_file"] != f"tools/card_generation_sources/{source}":
        raise SystemExit(f"{record_id}: generated source mismatch")
    if record.get("crop_box") != list(crop) or record.get("shared_members") != members:
        raise SystemExit(f"{record_id}: crop or member mapping mismatch")
    for field in ("source_file", "generated_file"):
        if not (ROOT / record[field]).is_file():
            raise SystemExit(f"{record_id}: missing {field}")


def save_card(image, member):
    target = TARGET_DIR / f"#{member}.tga"
    image.save(target, format="TGA", bits=32, compression="tga_rle")
    check = Image.open(target).convert("RGBA")
    top_edge = [(x, y) for y in range(2) for x in range(48)]
    fraction = sum(check.getpixel(point) == CANONICAL for point in top_edge) / len(top_edge)
    if check.size != (48, 64) or target.read_bytes()[16] != 32:
        raise SystemExit(f"{member}: invalid card dimensions or depth")
    if check.getchannel("A").getextrema() != (255, 255) or fraction < 0.35:
        raise SystemExit(f"{member}: invalid alpha or canonical background")


ARCHIVE_DIR = ROOT / "tools" / "card_source_archive" / "oman_before_cavalry_card_fix"
GENERATED = (
    ("oma_baluchi_musketeers", "oma_baluchi_musketeers_master.png", (0, 0, 1086, 1448),
     ["oma_baluchi_musketeers"]),
    ("oma_command_retinue", "oma_command_retinue_master.png", (0, 0, 1086, 1448),
     ["oma_command_retinue"]),
    ("oma_horse_guard_shared", "oma_horse_guard_master.png", (0, 0, 1086, 1448),
     ["oma_horse_guard_early", "oma_horse_guard_mid", "oma_horse_guard_high"]),
    ("oma_bedouin_camelry", "oma_bedouin_camelry_master.png", (0, 0, 1086, 1448),
     ["oma_bedouin_camelry"]),
)

ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
for record_id, source, crop, members in GENERATED:
    approved(record_id, source, crop, members)
    master = normalize_background(Image.open(SOURCE_DIR / source).crop(crop))
    card = normalize_background(master.resize((48, 64), Image.Resampling.LANCZOS))
    for member in members:
        target = TARGET_DIR / f"#{member}.tga"
        archive = ARCHIVE_DIR / target.name
        if target.exists() and not archive.exists():
            shutil.copy2(target, archive)
        save_card(card, member)

for target in TARGET_DIR.glob("#oma_*.tga"):
    save_card(normalize_background(Image.open(target)), target.stem[1:])

print("Installed approved Oman Baluchi, command, pistol-guard, and Bedouin-camelry cards; normalized all standardized Oman cards.")
