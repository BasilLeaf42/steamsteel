from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "tools/card_source_archive/union_before_standardization/#ap_front_cav.tga"
SOURCE = ROOT / "data/ui/units/portugala/#ap_front_cav.tga"
TARGET = ROOT / "data/ui/units/portugala/#uni_indian_scout_cavalry.tga"
shutil.copy2(ARCHIVE, SOURCE)
shutil.copy2(ARCHIVE, TARGET)
print("Restored the preserved Indian Scout Cavalry card without altering the rider artwork.")
