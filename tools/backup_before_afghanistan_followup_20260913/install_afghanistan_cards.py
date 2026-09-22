from collections import deque
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "tools" / "card_generation_sources"
TARGET_DIR = ROOT / "data" / "ui" / "units" / "timurids"
REGISTER = json.loads((ROOT / "tools" / "historical_card_sources.json").read_text(encoding="utf-8"))
BY_ID = {record["id"]: record for record in REGISTER}
CANONICAL = (184, 173, 143, 255)
REQUIRED = ("source_url", "source_file", "source_title", "creator", "source_date",
            "licence", "depicted_subject", "mapping_note", "generated_file")

def is_background(pixel):
    r, g, b, _ = pixel
    return pixel == CANONICAL or (
        125 <= r <= 240 and 110 <= g <= 225 and 75 <= b <= 205
        and -8 <= r-g <= 50 and -5 <= g-b <= 75
    )

def normalize_background(image):
    image = image.convert("RGBA")
    pixels, width, height = image.load(), image.width, image.height
    queue = deque([(x, y) for x in range(width) for y in (0, height-1)]
                  + [(x, y) for y in range(height) for x in (0, width-1)])
    seen = set()
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if not is_background(pixels[x, y]):
            continue
        pixels[x, y] = CANONICAL
        if x: queue.append((x-1, y))
        if x+1 < width: queue.append((x+1, y))
        if y: queue.append((x, y-1))
        if y+1 < height: queue.append((x, y+1))
    return image

def approved(record_id, source, members):
    record = BY_ID.get(record_id)
    if not record or record.get("status") != "card-approved":
        raise SystemExit(f"{record_id}: source mapping is missing or unapproved")
    missing = [field for field in REQUIRED if not str(record.get(field, "")).strip()]
    if missing:
        raise SystemExit(f"{record_id}: incomplete source mapping: {', '.join(missing)}")
    if (record["generated_file"] != f"tools/card_generation_sources/{source}"
            or record.get("crop_box") != [0, 0, 1086, 1448]
            or record.get("shared_members") != members):
        raise SystemExit(f"{record_id}: generated source, crop, or member mapping mismatch")
    for field in ("source_file", "generated_file"):
        if not (ROOT / record[field]).is_file():
            raise SystemExit(f"{record_id}: missing {field}")

def save_card(image, member):
    image = image.convert("RGBA")
    image.putalpha(255)
    target = TARGET_DIR / f"#{member}.tga"
    image.save(target, format="TGA", bits=32, compression="tga_rle")
    check = Image.open(target).convert("RGBA")
    edge = ([(x, y) for y in range(2) for x in range(48)]
            + [(x, y) for y in range(62, 64) for x in range(48)]
            + [(x, y) for x in (0, 47) for y in range(64)])
    if (check.size != (48, 64) or target.read_bytes()[16] != 32
            or check.getchannel("A").getextrema() != (255, 255)):
        raise SystemExit(f"{member}: invalid card dimensions, depth, or alpha")
    if sum(check.getpixel(point) == CANONICAL for point in edge) / len(edge) < .10:
        raise SystemExit(f"{member}: canonical background not exposed along perimeter")

GENERATED = (
    ("afg_lashkar_qawmi", "afg_lashkar_qawmi_master.png", ["afg_lashkar_qawmi"]),
    ("afg_ghilzai_nobles", "afg_ghilzai_nobles_master.png", ["afg_ghilzai_nobles"]),
    ("afg_sharpshooters_high", "afg_sharpshooters_high_master.png", ["afg_sharpshooters_high"]),
    ("afg_tribal_cavalry", "afg_tribal_cavalry_master.png", ["afg_tribal_cavalry"]),
    ("afg_kabul_guard_high", "afg_kabul_guard_high_master.png", ["afg_kabul_guard_high"]),
    ("afg_general_staff", "afg_general_staff_master.png", ["afg_general_staff"]),
)
archive = ROOT / "tools" / "card_source_archive" / "afghanistan_before_generated_cards"
archive.mkdir(parents=True, exist_ok=True)
for record_id, source, members in GENERATED:
    approved(record_id, source, members)
    card = normalize_background(
        Image.open(SOURCE_DIR/source).crop((0, 0, 1086, 1448))
    ).resize((48, 64), Image.Resampling.LANCZOS)
    card = normalize_background(card)
    for member in members:
        target = TARGET_DIR / f"#{member}.tga"
        if target.exists() and not (archive/target.name).exists():
            shutil.copy2(target, archive/target.name)
        save_card(card, member)
for target in TARGET_DIR.glob("#afg_*.tga"):
    save_card(normalize_background(Image.open(target)), target.stem[1:])
print("Installed and normalized six approved Afghan tactical-card compositions.")
