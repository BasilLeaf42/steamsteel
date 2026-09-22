"""Normalize the Nizamiye tactical-card background without touching the figure."""

from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CARD_DIR = ROOT / "data" / "ui" / "units" / "turks"
CARDS = ["otto_jan_inf", "ott_nizamiye_early", "ott_nizamiye_mid", "ott_nizamiye_high"]
CANONICAL = np.array([0xB8, 0xAD, 0x8F], dtype=np.uint8)


def connected_background(rgb: np.ndarray, tolerance: int = 40) -> np.ndarray:
    height, width = rgb.shape[:2]
    source = rgb[0, 0].astype(np.int16)
    delta = rgb.astype(np.int16) - source
    candidate = np.sum(delta * delta, axis=2) <= tolerance * tolerance
    selected = np.zeros((height, width), dtype=bool)
    queue: deque[tuple[int, int]] = deque()
    for x in range(width):
        for y in (0, height - 1):
            if candidate[y, x] and not selected[y, x]:
                selected[y, x] = True
                queue.append((y, x))
    for y in range(height):
        for x in (0, width - 1):
            if candidate[y, x] and not selected[y, x]:
                selected[y, x] = True
                queue.append((y, x))
    while queue:
        y, x = queue.popleft()
        for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= yy < height and 0 <= xx < width and candidate[yy, xx] and not selected[yy, xx]:
                selected[yy, xx] = True
                queue.append((yy, xx))
    return selected


def main() -> None:
    for name in CARDS:
        path = CARD_DIR / f"#{name}.tga"
        image = Image.open(path).convert("RGBA")
        if image.size != (48, 64):
            raise ValueError(f"{path}: expected 48x64 tactical card")
        pixels = np.asarray(image).copy()
        mask = connected_background(pixels[:, :, :3])
        pixels[:, :, :3][mask] = CANONICAL
        Image.fromarray(pixels, "RGBA").save(path)
        print(f"Normalized {path.relative_to(ROOT)}: {int(mask.sum())} background pixels")


if __name__ == "__main__":
    main()
