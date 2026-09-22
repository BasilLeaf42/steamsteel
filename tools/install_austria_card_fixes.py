from collections import deque
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CARD_DIR = ROOT / "data/ui/units/hungary"
SOURCE_DIR = ROOT / "tools/card_generation_sources"
CANONICAL = (184, 173, 143, 255)

def is_background(pixel):
    r, g, b, _ = pixel
    return r >= 140 and g >= 125 and b >= 90 and r >= g >= b and r - b <= 95

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
        point = queue.popleft()
        if point in seen:
            continue
        seen.add(point)
        x, y = point
        if not is_background(pixels[x, y]):
            continue
        pixels[x, y] = CANONICAL
        if x: queue.append((x - 1, y))
        if x + 1 < width: queue.append((x + 1, y))
        if y: queue.append((x, y - 1))
        if y + 1 < height: queue.append((x, y + 1))
    return image

def install_generated(source, crop_box, members):
    image = Image.open(SOURCE_DIR / source).convert("RGBA").crop(crop_box)
    image = normalize_background(image)
    image = image.resize((48, 64), Image.Resampling.LANCZOS)
    image = normalize_background(image)
    for member in members:
        image.save(CARD_DIR / f"#{member}.tga", format="TGA")

def normalize_existing(member):
    path = CARD_DIR / f"#{member}.tga"
    normalize_background(Image.open(path)).save(path, format="TGA")

install_generated("aus_matrosen_master.png", (90, 0, 990, 1200), ["aus_matrosen_early", "aus_matrosen_mid", "aus_matrosen_high"])
install_generated("aus_dragoner_master.png", (360, 0, 960, 800), ["aus_dragoner_early", "aus_dragoner_mid", "aus_dragoner_high"])
install_generated("aus_general_staff_master.png", (80, 0, 880, 1067), ["aus_general_staff"])
for unit in ["aus_bosniak_mid", "aus_bosniak_high"]:
    normalize_existing(unit)
print("Installed Austrian marine, dragoon and general replacements and normalized the affected card backgrounds.")
