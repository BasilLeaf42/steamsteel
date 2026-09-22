from collections import Counter, deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "data/ui/units/portugala"
CANONICAL = (184, 173, 143, 255)
SOURCES = [
    "us_inf", "us_militia", "us_front_inf", "us_late_inf", "us_blacks",
    "us_colo_inf", "us_zouave", "berdan_inf", "union_irish_brigade",
    "us_scout_cav", "ap_front_cav", "us_front_cav", "apache_inf",
]
TARGETS = [
    "uni_regulars_early", "uni_regulars_mid", "uni_regulars_high",
    "uni_national_guard_mid", "uni_national_guard_high",
    "uni_colored_troops_early", "uni_irish_brigade_early",
    "uni_zouaves_early", "uni_marines_early", "uni_marines_mid",
    "uni_marines_high", "uni_sharpshooters_early", "uni_indian_scouts",
    "uni_volunteer_cavalry_early", "uni_dragoons_early",
    "uni_dragoons_mid", "uni_dragoons_high",
    "uni_indian_scout_cavalry", "uni_general_staff",
]


def distance(left, right):
    return sum((left[index] - right[index]) ** 2 for index in range(3)) ** 0.5


def normalize(path):
    image = Image.open(path).convert("RGBA")
    width, height = image.size
    pixels = image.load()
    border = []
    for x in range(width):
        border.extend([pixels[x, 0], pixels[x, height - 1]])
    for y in range(height):
        border.extend([pixels[0, y], pixels[width - 1, y]])
    opaque = [pixel[:3] for pixel in border if pixel[3] > 200 and max(pixel[:3]) - min(pixel[:3]) < 85]
    palette = [colour for colour, _ in Counter(opaque).most_common(12)]
    queue = deque()
    seen = set()
    for x in range(width):
        queue.extend([(x, 0), (x, height - 1)])
    for y in range(height):
        queue.extend([(0, y), (width - 1, y)])
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen:
            continue
        pixel = pixels[x, y]
        candidate = pixel[3] < 128 or (palette and min(distance(pixel[:3], colour) for colour in palette) <= 38)
        if not candidate:
            continue
        seen.add((x, y))
        pixels[x, y] = CANONICAL
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in seen:
                queue.append((nx, ny))
    for y in range(height):
        for x in range(width):
            if pixels[x, y][3] < 128:
                pixels[x, y] = CANONICAL
    image.save(path, format="TGA")


for name in dict.fromkeys(SOURCES + TARGETS):
    normalize(FOLDER / f"#{name}.tga")
print(f"Normalized {len(set(SOURCES + TARGETS))} preserved and standardized Union cards.")
