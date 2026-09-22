from collections import deque
from pathlib import Path
import shutil

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "data/ui/units/portugala"
ARCHIVE = ROOT / "tools/card_source_archive/union_before_standardization/#ap_front_cav.tga"
SOURCE = FOLDER / "#ap_front_cav.tga"
TARGET = FOLDER / "#uni_indian_scout_cavalry.tga"
CANONICAL = (184, 173, 143, 255)

shutil.copy2(ARCHIVE, SOURCE)
image = Image.open(SOURCE).convert("RGBA")
width, height = image.size
pixels = image.load()
queue = deque()
for x in range(width):
    queue.extend(((x, 0), (x, height - 1)))
for y in range(height):
    queue.extend(((0, y), (width - 1, y)))
seen = set()
while queue:
    x, y = queue.popleft()
    if (x, y) in seen:
        continue
    pixel = pixels[x, y]
    if not (pixel[3] == 0 or (pixel[3] == 255 and pixel[:3] == (0, 0, 0))):
        continue
    seen.add((x, y))
    pixels[x, y] = CANONICAL
    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if 0 <= nx < width and 0 <= ny < height:
            queue.append((nx, ny))
for y in range(height):
    for x in range(width):
        if pixels[x, y][3] == 0:
            pixels[x, y] = CANONICAL
image.save(SOURCE, format="TGA")
shutil.copy2(SOURCE, TARGET)
print(f"Replaced {len(seen)} connected black/transparent background pixels without recolouring the rider.")
