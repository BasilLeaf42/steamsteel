from pathlib import Path
import shutil

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "data/ui/units/portugala"
SOURCE = FOLDER / "#ap_front_cav.tga"
TARGET = FOLDER / "#uni_indian_scout_cavalry.tga"
ARCHIVE = ROOT / "tools/card_source_archive/union_before_standardization/#ap_front_cav.tga"
CANONICAL = (184, 173, 143, 255)

shutil.copy2(ARCHIVE, SOURCE)
image = Image.open(SOURCE).convert("RGBA")
width, height = image.size
pixels = image.load()


def background(pixel):
    return pixel[3] < 128 or max(pixel[:3]) < 52


for y in range(height):
    for x in range(width):
        if not background(pixels[x, y]):
            break
        pixels[x, y] = CANONICAL
    for x in range(width - 1, -1, -1):
        if not background(pixels[x, y]):
            break
        pixels[x, y] = CANONICAL
for x in range(width):
    for y in range(height):
        if not background(pixels[x, y]):
            break
        pixels[x, y] = CANONICAL
    for y in range(height - 1, -1, -1):
        if not background(pixels[x, y]):
            break
        pixels[x, y] = CANONICAL
for y in range(height):
    for x in range(width):
        if pixels[x, y][3] == 0:
            pixels[x, y] = CANONICAL
image.save(SOURCE, format="TGA")
shutil.copy2(SOURCE, TARGET)
print("Repaired only edge-connected dark background runs on the cavalry card.")
