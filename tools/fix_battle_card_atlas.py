from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


CANONICAL = (184, 173, 143, 255)  # #B8AD8F
SPRITES = ((194, 432, 241, 511), (243, 432, 290, 511))
CULTURES = (
    "asian",
    "chinese",
    "mesoamerican",
    "middle_eastern",
    "northern_european",
    "slavic",
    "southern_european",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    changed = 0
    for culture in CULTURES:
        path = args.root / f"data/ui/{culture}/interface/battlepage_01.tga"
        image = Image.open(path).convert("RGBA")
        if image.size != (512, 512):
            raise SystemExit(f"unexpected atlas dimensions: {path}: {image.size}")

        pixels = image.load()
        atlas_changed = False
        for left, top, right, bottom in SPRITES:
            for y in range(top, bottom + 1):
                for x in range(left, right + 1):
                    if pixels[x, y] != CANONICAL:
                        pixels[x, y] = CANONICAL
                        atlas_changed = True

        if atlas_changed:
            changed += 1
            if args.apply:
                image.save(path, format="TGA", bits=32, compression="tga_rle")

    if not args.apply:
        print(f"atlases requiring correction={changed}")
        return

    failures = []
    for culture in CULTURES:
        path = args.root / f"data/ui/{culture}/interface/battlepage_01.tga"
        raw = path.read_bytes()
        image = Image.open(path).convert("RGBA")
        if raw[16] != 32:
            failures.append(f"{culture}: not 32-bit")
        for left, top, right, bottom in SPRITES:
            for y in range(top, bottom + 1):
                for x in range(left, right + 1):
                    if image.getpixel((x, y)) != CANONICAL:
                        failures.append(f"{culture}: battle-card sprite mismatch")
                        break
                if failures and failures[-1].startswith(culture):
                    break
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"corrected={changed}; validated={len(CULTURES)} culture atlases")


if __name__ == "__main__":
    main()
