from pathlib import Path
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CARD_DIR = ROOT / "data" / "ui" / "units" / "lith"
BACKUP = ROOT / "tools" / "backup_before_zulu_card_backgrounds_20260918"
NAMES = ("zulu_spearmen", "zulu_guard", "zulu_royals", "zulu_rifles", "zulu_elite")
PARCHMENT = (184, 173, 143, 255)

BACKUP.mkdir(parents=True, exist_ok=True)
for name in NAMES:
    source = CARD_DIR / f"#{name}.tga"
    archived = BACKUP / source.name
    if not archived.exists():
        shutil.copy2(source, archived)

    figure = Image.open(source).convert("RGBA")
    if figure.size != (48, 64):
        raise RuntimeError(f"{source.name}: expected 48x64, got {figure.size}")

    background = Image.new("RGBA", figure.size, PARCHMENT)
    installed = Image.alpha_composite(background, figure)
    installed.save(source, format="TGA")

print(f"Normalized {len(NAMES)} Zulu tactical-card backgrounds to #B8AD8F.")
