"""Restore the missing transparency in the Asian battle HUD atlas."""
from pathlib import Path
import hashlib
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/ui/asian/interface/battlepage_01.tga"
DONOR = ROOT / "data/ui/middle_eastern/interface/battlepage_01.tga"
ARCHIVE = ROOT / "tools/ui_icon_archive/before_asian_battle_hud_alpha/battlepage_01.tga"

def main():
    target = Image.open(TARGET).convert("RGBA")
    donor = Image.open(DONOR).convert("RGBA")
    if target.size != (512, 512) or donor.size != target.size:
        raise RuntimeError("unexpected battle HUD dimensions")
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    donor_alpha = donor.getchannel("A").tobytes()
    if target.getchannel("A").tobytes() == donor_alpha:
        if not ARCHIVE.exists():
            raise RuntimeError("repaired Asian HUD has no preserved opaque source")
        source = Image.open(ARCHIVE).convert("RGBA")
        if target.convert("RGB").tobytes() != source.convert("RGB").tobytes():
            raise RuntimeError("Asian HUD artwork differs from its preserved source")
        print("Asian battle HUD transparency is already repaired.")
        return
    if target.getchannel("A").getextrema() != (255, 255):
        raise RuntimeError("Asian HUD alpha is neither the verified opaque source nor the repaired mask")
    if not ARCHIVE.exists():
        shutil.copy2(TARGET, ARCHIVE)
    rgb_hash = hashlib.sha256(target.convert("RGB").tobytes()).digest()
    target.putalpha(donor.getchannel("A"))
    target.save(TARGET, format="TGA", bits=32, compression="tga_rle")
    check = Image.open(TARGET).convert("RGBA")
    if hashlib.sha256(check.convert("RGB").tobytes()).digest() != rgb_hash:
        raise RuntimeError("Asian HUD artwork changed while repairing alpha")
    if check.getchannel("A").tobytes() != donor_alpha:
        raise RuntimeError("Asian HUD alpha repair failed")
    print("Restored Asian battle HUD transparency without changing its artwork.")

if __name__ == "__main__":
    main()
