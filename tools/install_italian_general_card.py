from pathlib import Path
import json
from PIL import Image
from standardize_card_backgrounds import replace_connected_background, CANONICAL

ROOT = Path(__file__).resolve().parents[1]
register = json.loads((ROOT / 'tools/historical_card_sources.json').read_text(encoding='utf-8'))
record = next((item for item in register if item.get('unit_type') == 'ita_general_staff'), None)
required = ('source_url','source_file','source_title','creator','source_date','licence','depicted_subject','mapping_note','generated_file')
if not record or record.get('status') not in {'card-approved','pilot-approved'}:
    raise SystemExit('Italian general source mapping is missing or unapproved')
missing = [field for field in required if not str(record.get(field, '')).strip()]
if missing:
    raise SystemExit('Italian general source mapping is incomplete: ' + ', '.join(missing))
for field in ('source_file','generated_file'):
    if not (ROOT / record[field]).is_file():
        raise SystemExit(f'Missing {field}: {record[field]}')
image = Image.open(ROOT / record['generated_file']).convert('RGBA')
width, height = image.size
target = 3 / 4
if width / height > target:
    crop_width = round(height * target); left = (width - crop_width) // 2
    image = image.crop((left, 0, left + crop_width, height))
elif width / height < target:
    crop_height = round(width / target)
    image = image.crop((0, 0, width, crop_height))
image = image.resize((48, 64), Image.Resampling.LANCZOS)
image, _ = replace_connected_background(image)
destination = ROOT / record['card_file']
image.save(destination, format='TGA', bits=32, compression='tga_rle')
check = Image.open(destination).convert('RGBA')
border = [(x,y) for y in range(48) for x in range(48) if x < 2 or x >= 46 or y < 2]
fraction = sum(check.getpixel(point) == CANONICAL for point in border) / len(border)
if check.size != (48,64) or check.getchannel('A').getextrema() != (255,255) or fraction < .5:
    raise SystemExit(f'Installed Italian general card failed validation; canonical border={fraction:.3f}')
print(f'Installed Italian general card; canonical border={fraction:.3f}.')
