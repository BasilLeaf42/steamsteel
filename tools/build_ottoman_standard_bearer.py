"""Build Ottoman-specific textures for the verified French standard-bearer mesh."""

from __future__ import annotations

import io
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "unit_models" / "_Units" / "attachments" / "textures"
OUT = ROOT / "tools" / "mesh_work" / "ottoman_bearer" / "tga"
def open_texture(path: Path) -> Image.Image:
    raw = path.read_bytes()
    if raw[48:52] != b"DDS ":
        raise ValueError(f"Not a Medieval II texture container: {path}")
    return Image.open(io.BytesIO(raw[48:])).convert("RGBA")


def star_points(cx: float, cy: float, outer: float, inner: float) -> list[tuple[float, float]]:
    points = []
    for i in range(10):
        radius = outer if i % 2 == 0 else inner
        angle = -math.pi / 2 + i * math.pi / 5
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return points


def ottoman_flag() -> Image.Image:
    # Preserve the mesh donor's original faces. Only the isolated flag region
    # may be changed on transplanted units.
    image = open_texture(SOURCE / "per_rugbxx.texture")
    pixels = np.asarray(image).copy()
    # The remapped flag occupies the left quarter; the face atlas is on the
    # right. Use a deep, uniform red field to resist battlefield bleaching.
    pixels[:, 8:504, 0] = 132
    pixels[:, 8:504, 1] = 0
    pixels[:, 8:504, 2] = 8
    pixels[:, 8:504, 3] = 255
    image = Image.fromarray(pixels, "RGBA")

    symbol = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(symbol)
    # Low texture U is the fly edge and high U is the pole edge. Draw the
    # crescent opening toward the fly and counter-map it to the flag's
    # proportionally preserved lower-left UV footprint.
    # The actual cloth is the 264-triangle component at x=193..502 and
    # y=711..1013. Keep the complete device inside that component.
    draw.ellipse((305, 765, 465, 925), fill=255)
    draw.ellipse((275, 765, 435, 925), fill=0)
    draw.polygon(star_points(230, 845, 32, 13), fill=255)

    # Use a clean white device so it remains legible at battlefield distance.
    arr = np.asarray(image).copy()
    mask = np.asarray(symbol) > 0
    for channel in range(3):
        arr[:, :, channel][mask] = 242
    return Image.fromarray(arr, "RGBA")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ottoman_flag().save(OUT / "ott_standard_flag.tga")
    open_texture(SOURCE / "blank_norm.texture").save(OUT / "ott_standard_flag_n.tga")
    print(f"Built Ottoman bearer flag atlas with donor faces preserved in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
