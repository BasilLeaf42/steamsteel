"""Build a Qajar military banner atlas while preserving Persian face textures."""

from __future__ import annotations

import io
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ATTACH = ROOT / "data" / "unit_models" / "_Units" / "attachments" / "textures"
OUT = ROOT / "tools" / "mesh_work" / "qajar_bearer" / "tga"


def open_texture(path: Path) -> Image.Image:
    raw = path.read_bytes()
    if raw[48:52] != b"DDS ":
        raise ValueError(f"Not a Medieval II texture container: {path}")
    return Image.open(io.BytesIO(raw[48:])).convert("RGBA")


def main() -> None:
    # The right half is the native Persian face attachment atlas; the flag is
    # isolated on the left, so none of the Qajar faces are repainted.
    image = open_texture(ATTACH / "per_rugbxx.texture")
    pixels = np.asarray(image).copy()
    pixels[:, 8:504] = (132, 0, 8, 255)
    image = Image.fromarray(pixels, "RGBA")
    draw = ImageDraw.Draw(image)
    # Early-Qajar army banners were red and bore the Lion and Sun. The simple
    # gold silhouette is deliberately bold enough to survive mipmapping.
    sun = (330, 778, 430, 878)
    draw.ellipse(sun, fill=(236, 190, 42, 255))
    cx, cy = 380, 828
    for i in range(16):
        angle = i * math.pi / 8
        inner = (cx + math.cos(angle) * 58, cy + math.sin(angle) * 58)
        outer = (cx + math.cos(angle) * 82, cy + math.sin(angle) * 82)
        draw.line((inner, outer), fill=(236, 190, 42, 255), width=9)
    gold = (236, 190, 42, 255)
    draw.ellipse((245, 838, 383, 925), fill=gold)
    draw.ellipse((215, 850, 280, 905), fill=gold)
    draw.polygon(((355, 885), (440, 904), (436, 929), (335, 915)), fill=gold)
    draw.polygon(((255, 904), (225, 963), (252, 963), (285, 910)), fill=gold)
    draw.polygon(((330, 910), (340, 970), (367, 970), (367, 904)), fill=gold)
    draw.line((260, 865, 210, 790), fill=gold, width=10)
    draw.line((208, 790, 192, 772), fill=gold, width=8)
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / "qaj_standard_flag.tga")
    open_texture(ATTACH / "blank_norm.texture").save(OUT / "qaj_standard_flag_n.tga")
    print("Built red Qajar Lion-and-Sun military banner atlas with Persian faces preserved.")


if __name__ == "__main__":
    main()
