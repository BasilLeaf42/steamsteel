from collections import Counter
from pathlib import Path
import shutil

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "data/ui/units/portugala"
ARCHIVE = ROOT / "tools/card_source_archive/union_before_standardization"
CANONICAL = (184, 173, 143, 255)
CARD_MAP = {
    "uni_regulars_early": "us_inf", "uni_regulars_mid": "us_late_inf",
    "uni_regulars_high": "us_militia", "uni_national_guard_mid": "us_late_inf",
    "uni_national_guard_high": "us_late_inf", "uni_colored_troops_early": "us_blacks",
    "uni_irish_brigade_early": "union_irish_brigade", "uni_zouaves_early": "us_zouave",
    "uni_marines_early": "us_colo_inf", "uni_marines_mid": "us_colo_inf",
    "uni_marines_high": "us_colo_inf", "uni_sharpshooters_early": "berdan_inf",
    "uni_indian_scouts": "apache_inf", "uni_volunteer_cavalry_early": "us_front_inf",
    "uni_dragoons_early": "us_scout_cav", "uni_dragoons_mid": "us_scout_cav",
    "uni_dragoons_high": "us_scout_cav", "uni_indian_scout_cavalry": "ap_front_cav",
    "uni_general_staff": "us_front_cav",
}


def neutral(colour):
    red, green, blue = colour
    return 150 <= red <= 225 and 140 <= green <= 210 and 105 <= blue <= 180 and red >= green >= blue


for source in set(CARD_MAP.values()):
    shutil.copy2(ARCHIVE / f"#{source}.tga", FOLDER / f"#{source}.tga")
    path = FOLDER / f"#{source}.tga"
    image = Image.open(path).convert("RGBA")
    pixels = list(image.getdata())
    opaque = Counter(pixel[:3] for pixel in pixels if pixel[3] == 255)
    dominant, count = opaque.most_common(1)[0]
    replace_dominant = count >= 30 and neutral(dominant)
    repaired = []
    for pixel in pixels:
        near_canonical = sum((pixel[index] - CANONICAL[index]) ** 2 for index in range(3)) <= 9
        exact_dominant = replace_dominant and pixel[:3] == dominant
        if pixel[3] == 0 or near_canonical or exact_dominant:
            repaired.append(CANONICAL)
        else:
            repaired.append(pixel)
    image.putdata(repaired)
    image.save(path, format="TGA")

for target, source in CARD_MAP.items():
    shutil.copy2(FOLDER / f"#{source}.tga", FOLDER / f"#{target}.tga")
print("Restored archived Union figures and conservatively normalized exact background pixels.")
