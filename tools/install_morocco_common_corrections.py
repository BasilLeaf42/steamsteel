from pathlib import Path
from PIL import Image,ImageDraw
from collections import deque
import io,json,shutil,math,runpy
R=Path(__file__).resolve().parents[1];C=R/'data/ui/units/moors';M=R/'tools/card_generation_sources/morocco_20260915';A=R/'tools/card_source_archive/morocco_before_common_card_corrections';A.mkdir(parents=True,exist_ok=True);BG=(184,173,143,255)
rows=['mor_makhzen_early','mor_makhzen_mid','mor_makhzen_high','mor_abid_early','mor_abid_mid','mor_rif_early','mor_rif_mid','mor_rif_high','mor_hajjana']
def flat(im):
 im=im.convert('RGBA').resize((48,64),Image.Resampling.LANCZOS);p=im.load();q=deque([(x,0) for x in range(48)]+[(x,63) for x in range(48)]+[(0,y) for y in range(64)]+[(47,y) for y in range(64)]);seen=set()
 while q:
  x,y=q.popleft()
  if (x,y) in seen:continue
  r,g,b,a=p[x,y];neutral=a<170 or (r>120 and g>100 and b>60 and abs(r-g)<70 and g-b<95 and r>=g-18)
  if not neutral:continue
  seen.add((x,y));p[x,y]=BG
  for z in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=z[0]<48 and 0<=z[1]<64:q.append(z)
 return im
for n in rows:
 p=C/f'#{n}.tga';q=A/p.name
 if not q.exists():shutil.copy2(p,q)
 flat(Image.open(M/f'{n}_v2_master.png').crop((4,8,1084,1448))).save(p,format='TGA')
# Explicitly requested mesh-compatible complexion correction: darken only skin-range pixels, including hands.
def tex(p):
 raw=p.read_bytes();return Image.open(io.BytesIO(raw[48:])).convert('RGBA'),raw[:48]
def save(im,h,p):
 o=io.BytesIO();im.save(o,format='DDS',pixel_format='DXT5');p.write_bytes(h+o.getvalue())
b=R/'data/unit_models/_Units/bnw/textures';im,h=tex(b/'mor_standard_bearer.texture');px=im.load()
for y in range(im.height):
 for x in range(im.width):
  r,g,bl,a=px[x,y]
  if r>105 and r>g*1.08 and g>bl*1.02 and r-bl>25: px[x,y]=(int(r*.62),int(g*.55),int(bl*.48),a)
save(im,h,b/'mor_standard_bearer.texture')
# The bearer face, pole, and cloth share an attachment atlas. Rebuild its
# distinct UV regions; never paint the complete atlas red.
runpy.run_path(str(R/'tools/repair_moroccan_bearer_atlas.py'),run_name='__main__')
reg=R/'tools/historical_card_sources.json';data=json.loads(reg.read_text(encoding='utf-8'));ids=set(rows);data=[x for x in data if x.get('id') not in ids]
for n in rows:data.append(dict(id=n,unit_type=n,card_file=f'data/ui/units/moors/#{n}.tga',faction='moors',name=n,role='mounted matchlock camelry' if n=='mor_hajjana' else ('infantry skirmisher' if 'rif_' in n else 'non-uniformed firearm infantry'),weapon='period firearm and sword',source_url='https://www.habous.gov.ma/daouat-alhaq/item/8812',source_file='tools/historical_card_refs/moroccan_cavalry_1844.webp',source_title='Moroccan forces, nineteenth-century reference set',creator='Contemporary and institutional Moroccan military-history references',source_date='nineteenth century',licence='Historical reference use',depicted_subject='Moroccan Makhzen, Abid, Rifian, and mounted forces',pose_source_id='kneel_aim_photo_1871' if 'rif_' in n else '',mapping_note='Unit-specific replacement with clear pale-cloak silhouette; Rifiyya use a mechanically correct kneeling pose, Hajjana is visibly camel-mounted, and Makhzen/Abid remain non-uniformed with shield and sword.',status='card-approved',generated_file=f'tools/card_generation_sources/morocco_20260915/{n}_v2_master.png',crop_box=[4,8,1084,1448]))
reg.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Installed nine corrected Moroccan cards, bearer complexion, and green-pentagram flag.')