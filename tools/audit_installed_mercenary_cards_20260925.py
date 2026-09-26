from pathlib import Path
import re, json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EDU = (ROOT/'data/tow_steamsteel/export_descr_unit.txt').read_text(encoding='utf-8', errors='replace').replace('\r','')
units=[]
for block in re.split(r'\n(?=type\s+)', EDU):
    m=re.search(r'^type\s+(.+)$',block,re.M)
    if not m or not re.search(r'^attributes\s+.*\bmercenary_unit\b',block,re.M): continue
    unit=m.group(1).strip()
    if re.search(r'^category\s+ship\s*$',block,re.M): continue
    units.append(unit)

folder=ROOT/'data/ui/units/mercs'
rows=[]
for unit in units:
    candidates=[folder/f'#{unit}.tga',folder/f"#{unit.replace(' ','_')}.tga"]
    p=next((x for x in candidates if x.is_file()),candidates[0])
    if not p.is_file():
        rows.append({'unit':unit,'missing':True}); continue
    with Image.open(p) as im:
        rgba=im.convert('RGBA')
        rows.append({'unit':unit,'missing':False,'size':list(rgba.size),'mode':rgba.mode,'path':str(p.relative_to(ROOT))})

cols=6; cell_w=205; cell_h=150
sheet=Image.new('RGB',(cols*cell_w,((len(rows)+cols-1)//cols)*cell_h),(46,42,36))
d=ImageDraw.Draw(sheet); font=ImageFont.load_default()
for i,row in enumerate(rows):
    x=(i%cols)*cell_w; y=(i//cols)*cell_h
    if not row['missing']:
        with Image.open(ROOT/row['path']) as im:
            sheet.paste(im.convert('RGB').resize((96,128),Image.Resampling.NEAREST),(x+4,y+4))
    d.text((x+104,y+6),row['unit'][:27],fill='white',font=font)
out=ROOT/'tools/installed_mercenary_cards_contact_sheet_20260925.png'
sheet.save(out)
(ROOT/'tools/installed_mercenary_cards_audit_20260925.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'units':len(rows),'missing':sum(r['missing'] for r in rows),'contact_sheet':str(out)},indent=2))
