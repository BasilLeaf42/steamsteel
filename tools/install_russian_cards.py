from pathlib import Path
import json
import shutil
from PIL import Image
from standardize_card_backgrounds import replace_connected_background, CANONICAL

ROOT=Path(__file__).resolve().parents[1]
UNIT=ROOT/'data/ui/units/russia'
core=[]
for lineage in ('pekhota','opolchenie','leib_guard','grenadery','strelki','marines','sapery','siberian','draguny','kazaki'):
    core += [f'rus_{lineage}_{p}' for p in ('early','mid','high')]
core += ['rus_gusary','rus_ulany','rus_guard_cuirassiers','rus_general_staff']
ARCHIVE=ROOT/'tools/card_source_archive/russia_before_standardization'
ARCHIVE.mkdir(parents=True,exist_ok=True)
for unit in core:
    source=UNIT/f'#{unit}.tga'; archived=ARCHIVE/source.name
    if source.is_file() and not archived.exists(): shutil.copy2(source,archived)
REGISTER=json.loads((ROOT/'tools/historical_card_sources.json').read_text(encoding='utf-8'))
BY_ID={r['id']:r for r in REGISTER}
GENERATED=[
    'rus_strelki_shared',
    'rus_marines_shared',
    'rus_draguny_shared',
    'rus_kazaki_shared',
    'rus_gusary',
    'rus_ulany',
    'rus_guard_cuirassiers',
    'rus_general_staff',
]
REQUIRED=('source_url','source_file','source_title','creator','source_date','licence','depicted_subject','mapping_note','generated_file')
for key in GENERATED:
    r=BY_ID[key]
    missing=[f for f in REQUIRED if not str(r.get(f,'')).strip()]
    if missing or r.get('status')!='card-approved':
        raise SystemExit(f'unapproved or incomplete Russian source {key}: {missing}')
    for field in ('source_file','generated_file'):
        if not (ROOT/r[field]).is_file(): raise SystemExit(f'missing {field}: {r[field]}')
    image=Image.open(ROOT/r['generated_file']).convert('RGBA')
    w,h=image.size
    if w/h>3/4:
        nw=round(h*3/4); left=(w-nw)//2; image=image.crop((left,0,left+nw,h))
    elif w/h<3/4:
        nh=round(w/(3/4)); image=image.crop((0,0,w,nh))
    image=image.resize((48,64),Image.Resampling.LANCZOS)
    image,_=replace_connected_background(image)
    for member in r.get('shared_members',[r['unit_type']]):
        image.save(UNIT/f'#{member}.tga',format='TGA',bits=32,compression='tga_rle')

# Preserve distinct original art while assigning it consistently within each unchanged lineage.
donors={
 'rus_pekhota':['rus_conscript_ru'],
 'rus_opolchenie':['rus_roy_inf_ru'],
 'rus_leib_guard':['rus_cos_guard_ru'],
 'rus_grenadery':['rus_guard'],
}
for lineage,source_names in donors.items():
    if len(source_names)==1: source_names*=3
    for period,source in zip(('early','mid','high'),source_names):
        image=Image.open(UNIT/f'#{source}.tga').convert('RGBA')
        image,_=replace_connected_background(image)
        image.save(UNIT/f'#{lineage}_{period}.tga',format='TGA',bits=32,compression='tga_rle')

fail=[]
for unit in core:
    target=UNIT/f'#{unit}.tga'
    image=Image.open(target).convert('RGBA')
    image,_=replace_connected_background(image)
    image.putalpha(255)
    image.save(target,format='TGA',bits=32,compression='tga_rle')
    raw=target.read_bytes(); check=Image.open(target).convert('RGBA')
    border=[(x,y) for y in range(48) for x in range(48) if x<2 or x>=46 or y<2]
    fraction=sum(check.getpixel(p)==CANONICAL for p in border)/len(border)
    if check.size!=(48,64) or raw[16]!=32 or check.getchannel('A').getextrema()!=(255,255) or fraction<.5:
        fail.append(f'{unit}: size={check.size}, bpp={raw[16]}, alpha={check.getchannel("A").getextrema()}, background={fraction:.3f}')
if fail: raise SystemExit('invalid Russian cards:\n'+'\n'.join(fail))
print(f'Installed and validated {len(core)} Russian tactical cards.')
