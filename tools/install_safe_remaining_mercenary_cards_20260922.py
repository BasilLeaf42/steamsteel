from pathlib import Path
from PIL import Image
import shutil
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'tools/remaining_mercenary_cards_safe_preview'
targets=(ROOT/'data/ui/units/mercs',ROOT/'data/ui/units/slave')
cards=sorted(SRC.glob('#*.tga'))
if len(cards)!=40:raise SystemExit(f'expected 40 preview cards, found {len(cards)}')
for card in cards:
 with Image.open(card) as im:
  if im.size!=(48,64) or im.convert('RGBA').mode!='RGBA':raise SystemExit(f'invalid {card}')
 for folder in targets:shutil.copy2(card,folder/card.name)
print('Installed 40 visually audited safe cards into both mercenary UI folders.')
