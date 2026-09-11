from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

import standardize_card_backgrounds as backgrounds


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(
    r"C:\Users\kwoks\.codex\generated_images\01a0389f-e7b4-7a23-8350-e89948489774"
)


def main() -> None:
    manifest = json.loads(
        (ROOT / "tools/balanced_card_generation_manifest.json").read_text(encoding="utf-8")
    )
    for index in (int(value) for value in sys.argv[1:]):
        group = manifest[index]
        installed = Image.open(group["members"][0]).convert("RGBA")
        candidates: list[tuple[float, Path]] = []
        for path in GENERATED.glob("*.png"):
            image = Image.open(path).convert("RGBA").resize((48, 64), Image.Resampling.LANCZOS)
            image, _ = backgrounds.replace_connected_background(image)
            score = sum(ImageStat.Stat(ImageChops.difference(image, installed)).mean[:3])
            candidates.append((score, path))
        score, source = min(candidates)
        destination = ROOT / "tools/card_generation_sources" / f'{group["id"]}.png'
        shutil.copy2(source, destination)
        print(f"restored {group['id']} from {source.name}; score={score:.4f}")


if __name__ == "__main__":
    main()
