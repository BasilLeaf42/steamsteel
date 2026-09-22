"""Build a plain-red Muscat and Oman flag for the verified bearer mesh."""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENTS = ROOT / "data" / "unit_models" / "_Units" / "attachments" / "textures"
OUT = ROOT / "tools" / "mesh_work" / "oman_bearer" / "tga"


def open_texture(path: Path) -> Image.Image:
    raw = path.read_bytes()
    if raw[48:52] != b"DDS ":
        raise ValueError(f"Not a Medieval II texture container: {path}")
    return Image.open(io.BytesIO(raw[48:])).convert("RGBA")


def main() -> None:
    # The Omani bearer reuses the proven Ottoman bearer mesh. Preserve its
    # donor face atlas exactly and change only the isolated flag region.
    image = open_texture(ATTACHMENTS / "per_rugbxx.texture")
    pixels = np.asarray(image).copy()
    pixels[:, 8:504, 0] = 132
    pixels[:, 8:504, 1] = 0
    pixels[:, 8:504, 2] = 8
    pixels[:, 8:504, 3] = 255
    OUT.mkdir(parents=True, exist_ok=True)
    Image.fromarray(pixels, "RGBA").save(OUT / "oma_standard_flag.tga")
    open_texture(ATTACHMENTS / "blank_norm.texture").save(OUT / "oma_standard_flag_n.tga")
    print(f"Built plain-red Omani bearer flag with donor faces preserved in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
