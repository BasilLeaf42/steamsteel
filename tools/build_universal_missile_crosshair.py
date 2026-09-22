from pathlib import Path
from collections import Counter
import hashlib
import shutil

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "data" / "ui" / "icons" / "missiles.tga"
ARCHIVE = ROOT / "tools" / "ui_icon_archive" / "before_universal_crosshair" / "missiles.tga"
SHARED_ROOT = ROOT / "data" / "ui"
SHARED_ARCHIVE = ROOT / "tools" / "ui_icon_archive" / "before_card_attacking_crosshair"
CARD_ATTACKING_BOX = (365, 1, 381, 17)
VERIFIED_DONOR = SHARED_ARCHIVE / "northern_european" / "interface" / "sharedpage_01.tga"


def main():
    if not ICON.exists():
        raise FileNotFoundError(ICON)

    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    if not ARCHIVE.exists():
        shutil.copy2(ICON, ARCHIVE)

    # missiles.tga was changed during the original misdiagnosis. It is not the
    # firing-state overlay, so restore it exactly and leave it alone.
    if not ARCHIVE.exists():
        raise FileNotFoundError(ARCHIVE)
    shutil.copy2(ARCHIVE, ICON)

    # The symbol drawn over an actively firing unit card is not missiles.tga.
    # It is CARD_ATTACKING_MISSILE on page 0 of shared.sd, stored at this same
    # rectangle in every culture's sharedpage_01 atlas.
    archived_atlases = sorted(SHARED_ARCHIVE.rglob("sharedpage_01.tga"))
    if len(archived_atlases) != 10:
        raise RuntimeError(f"expected 10 preserved atlases, found {len(archived_atlases)}")
    preserved_tiles = [Image.open(path).convert("RGBA").crop(CARD_ATTACKING_BOX)
                       for path in archived_atlases]
    hashes = [hashlib.sha256(item.tobytes()).digest() for item in preserved_tiles]
    majority_hash, majority_count = Counter(hashes).most_common(1)[0]
    if majority_count != 7:
        raise RuntimeError(f"expected verified crosshair in 7 preserved atlases, found {majority_count}")
    tile = Image.open(VERIFIED_DONOR).convert("RGBA").crop(CARD_ATTACKING_BOX)
    if hashlib.sha256(tile.tobytes()).digest() != majority_hash:
        raise RuntimeError("verified donor is not the preserved majority firing crosshair")

    atlases = sorted(SHARED_ROOT.glob("*/interface/sharedpage_01.tga"))
    atlases += sorted((SHARED_ROOT / "southern_european" / "interface").glob("*/sharedpage_01.tga"))
    if len(atlases) != 10:
        raise RuntimeError(f"expected 10 culture/interface atlases, found {len(atlases)}")
    for atlas in atlases:
        relative = atlas.relative_to(SHARED_ROOT)
        archived = SHARED_ARCHIVE / relative
        archived.parent.mkdir(parents=True, exist_ok=True)
        if not archived.exists():
            shutil.copy2(atlas, archived)
        page = Image.open(atlas).convert("RGBA")
        page.paste((0, 0, 0, 0), CARD_ATTACKING_BOX)
        page.paste(tile, CARD_ATTACKING_BOX[:2])
        page.save(atlas, format="TGA", bits=32, compression="tga_rle")

    if ICON.read_bytes() != ARCHIVE.read_bytes():
        raise RuntimeError("missiles.tga was not restored exactly")
    expected = tile.tobytes()
    for atlas in atlases:
        page = Image.open(atlas).convert("RGBA")
        if page.crop(CARD_ATTACKING_BOX).tobytes() != expected:
            raise RuntimeError(f"crosshair mismatch in {atlas}")

    print("Restored the unrelated missiles.tga exactly.")
    print(f"Installed the preserved 7-of-10 majority CARD_ATTACKING_MISSILE tile in {len(atlases)} atlases.")


if __name__ == "__main__":
    main()
