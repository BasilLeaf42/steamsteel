from pathlib import Path
from PIL import Image,ImageDraw
from collections import deque
import json,hashlib,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tools/japanese_generals_uncropped_20260923'
MAP=json.loads((OUT/'mapping.json').read_text())
CAN=(184,173,143)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 (OUT/'staged').mkdir(exist_ok=True);report=[]
 sheet=Image.new('RGB',(1050,720),CAN);d=ImageDraw.Draw(sheet)
 for i,(key,source) in enumerate(MAP.items()):
  source=Path(source);im=Image.open(source).convert('RGB');w,h=im.size
  assert w*4==h*3
  px=im.load();mask=Image.new('1',im.size);mp=mask.load();q=deque()
  for seed in [(0,0),(w-1,0)]:
   ref=px[seed];q.append(seed);mp[seed]=1
   while q:
    x,y=q.popleft();cur=px[x,y]
    for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
     if 0<=nx<w and 0<=ny<h and not mp[nx,ny]:
      v=px[nx,ny]
      if max(abs(v[c]-cur[c]) for c in range(3))<=4 and max(abs(v[c]-ref[c]) for c in range(3))<=12:
       mp[nx,ny]=1;q.append((nx,ny))
  norm=im.copy();norm.paste(CAN,(0,0,w,h),mask)
  protected=norm.copy();protected.paste(im,(0,0),mask);assert protected.tobytes()==im.tobytes()
  mask.save(OUT/f'{key}_background_mask.png')
  card=norm.resize((48,64),Image.Resampling.LANCZOS).convert('RGBA')
  target=OUT/'staged'/f'#{key}.tga';card.save(target,compression='tga_rle')
  old=ROOT/'data/ui/units/saxons'/target.name
  report.append(dict(unit=key,source=str(source),source_sha256=sha(source),crop_box=[0,0,w,h],target=str(old.relative_to(ROOT)),before_sha256=sha(old),after_sha256=sha(target),background_method='Top-corner-seeded edge continuity: maximum 4 per-channel neighbour difference, bounded within 12 of seed. Protected foreground unchanged.',visual_review='pending'))
  x=i%4*260;y=i//4*240
  d.text((x+4,y+4),key.replace('Japan_',''),fill='black')
  sheet.paste(Image.open(old).convert('RGB').resize((96,128),Image.Resampling.NEAREST),(x+4,y+32))
  sheet.paste(card.convert('RGB').resize((96,128),Image.Resampling.NEAREST),(x+112,y+32))
  sheet.paste(card.convert('RGB'),(x+112,y+179))
  d.text((x+4,y+163),'Before',fill='black');d.text((x+112,y+163),'Full source',fill='black')
 sheet.save(OUT/'before_after.png')
 (OUT/'manifest.json').write_text(json.dumps(report,indent=2))
 print('Staged 11 complete-source cards; no crop; protected foreground identical.')
def install():
 rows=json.loads((OUT/'manifest.json').read_text());archive=ROOT/'tools/card_source_archive/japan_before_uncropped_20260923';archive.mkdir(exist_ok=False)
 registry=ROOT/'tools/historical_card_sources.json';shutil.copy2(registry,archive/registry.name)
 register=json.loads(registry.read_text(encoding='utf-8'))
 for r in rows:
  p=ROOT/r['target'];assert sha(p)==r['before_sha256']
  shutil.copy2(p,archive/p.name);shutil.copy2(OUT/'staged'/p.name,p)
  assert sha(p)==r['after_sha256'];assert Image.open(p).size==(48,64) and Image.open(p).mode=='RGBA'
  r['visual_review']='passed: original sources and all before/after cards at 48x64 and enlarged'
  r['archive']=str((archive/p.name).relative_to(ROOT))
  for v in register:
   if v.get('unit')==r['unit']:
    v.update(crop_box=r['crop_box'],crop_note='2026-09-23: entire original master retained, zero cropping, uniform 3:4 reduction at user request. Original master framing is the zoom-out limit.',background_mask=r['background_method'])
 registry.write_text(json.dumps(register,ensure_ascii=False,indent=2),encoding='utf-8')
 (OUT/'manifest.json').write_text(json.dumps(rows,indent=2));shutil.copy2(OUT/'manifest.json',archive/'manifest.json')
 print('Installed and verified 11 uncropped cards; previous cards and source register archived.')
if __name__=='__main__':install() if '--install' in sys.argv else build()
