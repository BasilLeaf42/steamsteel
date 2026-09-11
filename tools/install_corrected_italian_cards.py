from pathlib import Path
import json
import shutil
from PIL import Image
from standardize_card_backgrounds import replace_connected_background, CANONICAL

ROOT = Path(__file__).resolve().parents[1]
REGISTER = json.loads((ROOT / 'tools/historical_card_sources.json').read_text(encoding='utf-8'))
GROUPS = {
    'ita_milizia_shared': ['ita_milizia_early', 'ita_milizia_mid', 'ita_milizia_high'],
    'ita_cavalleggeri': ['ita_cavalleggeri'],
    'ita_carabinieri_shared': ['ita_carabinieri_early', 'ita_carabinieri_mid', 'ita_carabinieri_high'],
    'ita_lancieri': ['ita_lancieri'],
}
archive = ROOT / 'tools/card_source_archive/italy_pre_card_correction'
archive.mkdir(parents=True, exist_ok=True)
for record_id, members in GROUPS.items():
    record = next((item for item in REGISTER if item.get('id') == record_id), None)
    required = ('source_url','source_file','source_title','creator','source_date','licence','depicted_subject','mapping_note','generated_file')
    if not record or record.get('status') != 'card-approved':
        raise SystemExit(f'{record_id}: source mapping is missing or unapproved')
    missing = [field for field in required if not str(record.get(field, '')).strip()]
    if missing:
        raise SystemExit(f'{record_id}: incomplete source mapping: {", ".join(missing)}')
    for field in ('source_file','generated_file'):
        if not (ROOT / record[field]).is_file():
            raise SystemExit(f'{record_id}: missing {field}: {record[field]}')
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
    for member in members:
        destination = ROOT / f'data/ui/units/venice/#{member}.tga'
        archived = archive / destination.name
        if destination.is_file() and not archived.is_file():
            shutil.copy2(destination, archived)
        image.save(destination, format='TGA', bits=32, compression='tga_rle')
        check = Image.open(destination).convert('RGBA')
        border = [(x,y) for y in range(48) for x in range(48) if x < 2 or x >= 46 or y < 2]
        fraction = sum(check.getpixel(point) == CANONICAL for point in border) / len(border)
        if check.size != (48,64) or check.getchannel('A').getextrema() != (255,255) or fraction < .5:
            raise SystemExit(f'{member}: validation failed; canonical border={fraction:.3f}')
        print(f'{member}: installed; canonical border={fraction:.3f}')
