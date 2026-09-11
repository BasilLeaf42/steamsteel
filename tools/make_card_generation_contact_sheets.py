from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools" / "balanced_card_generation_manifest.json"
OUTPUT = Path(
    r"C:\Users\kwoks\.codex\visualizations\2026\08\25\01a0389f-e7b4-7a23-8350-e89948489774"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path)
    parser.add_argument("--large", action="store_true")
    args = parser.parse_args()
    groups = json.loads(MANIFEST.read_text(encoding="utf-8"))
    per_sheet = 12 if args.large else 24
    columns = 4 if args.large else 6
    cell_w, cell_h = (256, 278) if args.large else (160, 150)
    for sheet_index, start in enumerate(range(0, len(groups), per_sheet), 1):
        batch = groups[start : start + per_sheet]
        rows = (len(batch) + columns - 1) // columns
        sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), (40, 40, 40))
        draw = ImageDraw.Draw(sheet)
        for index, group in enumerate(batch):
            x = (index % columns) * cell_w
            y = (index // columns) * cell_h
            source = group["reference"]
            if args.sources:
                candidate = args.sources / f'{group["id"]}.png'
                if not candidate.is_file():
                    continue
                source = candidate
            card = Image.open(source).convert("RGBA")
            if args.sources and not args.large:
                card = card.resize((48, 64), Image.Resampling.LANCZOS)
            display_size = (192, 256) if args.large else (96, 128)
            card = card.resize(display_size, Image.Resampling.LANCZOS if args.large else Image.Resampling.NEAREST)
            sheet.paste(card.convert("RGB"), (x + (cell_w - display_size[0]) // 2, y), card)
            label_y = y + display_size[1] + 2
            draw.text((x + 3, label_y), f'{group["id"][:8]} {group["representative"][:22]}', fill="white")
        stem = "balanced_card_generated_large" if args.large else ("balanced_card_generated" if args.sources else "balanced_card_references")
        path = OUTPUT / f"{stem}_{sheet_index}.png"
        sheet.save(path)
        print(path)


if __name__ == "__main__":
    main()
