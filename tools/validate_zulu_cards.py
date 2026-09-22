from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CARD_DIR = ROOT / "data" / "ui" / "units" / "lith"
NAMES = ("zulu_spearmen", "zulu_guard", "zulu_royals", "zulu_rifles", "zulu_elite")
PARCHMENT = (184, 173, 143, 255)

for name in NAMES:
    path = CARD_DIR / f"#{name}.tga"
    image = Image.open(path).convert("RGBA")
    assert image.size == (48, 64), f"{name}: wrong dimensions"
    assert image.mode == "RGBA", f"{name}: not RGBA"
    assert image.getpixel((0, 0)) == PARCHMENT, f"{name}: wrong top-left background"
    assert image.getpixel((47, 0)) == PARCHMENT, f"{name}: wrong top-right background"
    parchment_pixels = sum(pixel == PARCHMENT for pixel in image.getdata())
    assert parchment_pixels >= 500, f"{name}: canonical background is not established"
    assert image.getchannel("A").getextrema() == (255, 255), f"{name}: background remains translucent"

print(f"Zulu card validation passed: {len(NAMES)} cards are 48x64 RGBA on #B8AD8F.")
