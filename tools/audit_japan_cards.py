from pathlib import Path
import re
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
EDU = ROOT / 'data/tow_steamsteel/export_descr_unit.txt'
CARDS = ROOT / 'data/ui/units/saxons'
OUT = ROOT / 'tools/japan_cards_before_contact.png'

text = EDU.read_text(encoding='utf-8', errors='replace')
items = []
for block in re.split(r'(?=^type\s+)', text, flags=re.M):
    if not re.search(r'(?:^ownership|^era [012]).*\bsaxons\b', block, flags=re.M):
        continue
    typ = re.search(r'^type\s+(.+)$', block, flags=re.M)
    key = re.search(r'^dictionary\s+([^;\s]+)', block, flags=re.M)
    if typ and key:
        items.append((typ.group(1).strip(), key.group(1).strip()))

cols, cw, ch = 8, 150, 112
rows = (len(items) + cols - 1) // cols
sheet = Image.new('RGB', (cols*cw, rows*ch), (45, 42, 36))
draw = ImageDraw.Draw(sheet)
for i, (typ, key) in enumerate(items):
    x, y = (i % cols)*cw, (i // cols)*ch
    p = CARDS / f'#{key}.tga'
    if p.exists():
        im = Image.open(p).convert('RGBA')
        if im.size != (48, 64):
            raise SystemExit(f'bad size {p}: {im.size}')
        im = im.resize((72, 96), Image.Resampling.NEAREST)
        sheet.paste(im.convert('RGB'), (x, y), im.getchannel('A'))
    else:
        draw.rectangle((x, y, x+71, y+95), fill=(90, 30, 30), outline=(255, 100, 100))
        draw.text((x+5, y+40), 'MISSING', fill='white')
    draw.text((x+75, y+2), typ[:20], fill='white')
    draw.text((x+75, y+28), key[:20], fill=(210, 200, 175))
sheet.save(OUT)
print(OUT)
