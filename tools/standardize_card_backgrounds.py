from __future__ import annotations

import argparse
import math
from collections import Counter
from collections import deque
from pathlib import Path

from PIL import Image


CANONICAL = (184, 173, 143, 255)  # Steam & Steel parchment: #B8AD8F
ROSTER_BLOCKS = {
    "england": (6318, 7253),
    "spain": (7893, 8609),
    "france": (8610, 9639),
    "hre": (10144, 11131),
    "portugal": (11637, 12360),
    "sicily": (12689, 13235),
    "normans": (13251, 13975),
    "mongols": (14286, 14832),
}


def colour_distance(a: tuple[int, ...], b: tuple[int, ...]) -> float:
    return math.sqrt(sum((a[index] - b[index]) ** 2 for index in range(3)))


def background_reference(image: Image.Image) -> tuple[int, int, int, int] | None:
    width, height = image.size
    pixels = image.load()
    scores: Counter[tuple[int, int, int]] = Counter()
    samples: dict[tuple[int, int, int], list[tuple[int, int, int, int]]] = {}
    for y in range(height):
        for x in range(width):
            colour = pixels[x, y]
            if colour[3] < 32:
                continue
            key = tuple(channel // 12 for channel in colour[:3])
            weight = 1
            if y == 0 or (x in (0, width - 1) and y < height * 3 // 4):
                weight += 8
            if y == 0 and x in (0, width - 1):
                weight += 20
            scores[key] += weight
            samples.setdefault(key, []).append(colour)
    if not scores:
        return None
    key = scores.most_common(1)[0][0]
    colours = samples[key]
    return tuple(round(sum(colour[index] for colour in colours) / len(colours)) for index in range(4))


def replace_connected_background(image: Image.Image) -> tuple[Image.Image, int]:
    image = image.convert("RGBA")
    width, height = image.size
    reference = background_reference(image)
    if reference is None:
        return image, 0
    reference_distance = colour_distance(reference, CANONICAL)
    tolerance = 80 if reference_distance > 50 else 42
    pixels = image.load()
    visited: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int]] = deque()

    def eligible(x: int, y: int) -> bool:
        colour = pixels[x, y]
        return colour[3] < 32 or colour_distance(colour, reference) <= tolerance

    for x in range(width):
        if eligible(x, 0):
            queue.append((x, 0))
    for y in range(height * 3 // 4):
        for x in (0, width - 1):
            if eligible(x, y):
                queue.append((x, y))

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited or not eligible(x, y):
            continue
        visited.add((x, y))
        if x:
            queue.append((x - 1, y))
        if x + 1 < width:
            queue.append((x + 1, y))
        if y:
            queue.append((x, y - 1))
        if y + 1 < height:
            queue.append((x, y + 1))

    output = image.copy()
    output_pixels = output.load()
    for x, y in visited:
        output_pixels[x, y] = CANONICAL
    return output, len(visited)


def roster_cards(root: Path) -> list[Path]:
    edu_lines = (root / "data/tow_steamsteel/export_descr_unit.txt").read_text(
        encoding="utf-8", errors="replace"
    ).splitlines()
    cards: list[Path] = []
    for faction, (start, end) in ROSTER_BLOCKS.items():
        for line in edu_lines[start - 1 : end]:
            if line.startswith("type"):
                unit_type = line.split(None, 1)[1].strip()
                cards.append(root / f"data/ui/units/{faction}/#{unit_type}.tga")
    return cards


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.apply == bool(args.output_root):
        parser.error("choose exactly one of --apply or --output-root")

    changed = 0
    missing: list[Path] = []
    for card in roster_cards(args.root):
        if not card.is_file():
            missing.append(card)
            continue
        source = Image.open(card).convert("RGBA")
        if source.size != (48, 64):
            raise SystemExit(f"unexpected dimensions for {card}: {source.size}")
        output, replaced = replace_connected_background(source)
        if not replaced:
            continue
        if args.apply:
            destination = card
        else:
            destination = args.output_root / card.relative_to(args.root)
            destination.parent.mkdir(parents=True, exist_ok=True)
        output.save(destination, format="TGA", bits=32, compression="tga_rle")
        changed += 1

    if missing:
        raise SystemExit("missing cards:\n" + "\n".join(str(path) for path in missing))
    print(f"standardized {changed} cards to #{CANONICAL[0]:02X}{CANONICAL[1]:02X}{CANONICAL[2]:02X}")


if __name__ == "__main__":
    main()
