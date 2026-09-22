from collections import Counter
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "data/ui/units/portugala"
TYPES = [
    "uni_regulars_early", "uni_regulars_mid", "uni_regulars_high",
    "uni_national_guard_mid", "uni_national_guard_high",
    "uni_colored_troops_early", "uni_irish_brigade_early",
    "uni_zouaves_early", "uni_marines_early", "uni_marines_mid",
    "uni_marines_high", "uni_sharpshooters_early", "uni_indian_scouts",
    "uni_volunteer_cavalry_early", "uni_dragoons_early",
    "uni_dragoons_mid", "uni_dragoons_high",
    "uni_indian_scout_cavalry", "uni_general_staff",
]
for unit_type in TYPES:
    image = Image.open(FOLDER / f"#{unit_type}.tga").convert("RGBA")
    assert image.size == (48, 64), (unit_type, image.size)
    assert image.mode == "RGBA", (unit_type, image.mode)
    opaque = Counter(pixel[:3] for pixel in image.getdata() if pixel[3] == 255)
    common, count = opaque.most_common(1)[0]
    print(f"{unit_type}: common=#{common[0]:02X}{common[1]:02X}{common[2]:02X} ({count}) corner={image.getpixel((47,0))}")
