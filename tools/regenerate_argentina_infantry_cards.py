from pathlib import Path
from PIL import Image
from collections import deque
import json,shutil
R=Path(__file__).resolve().parents[1];C=R/'data/ui/units/aztecs';M=R/'tools/card_generation_sources/argentina_20260915';A=R/'tools/card_source_archive/argentina_before_full_regeneration_20260915';A.mkdir(parents=True,exist_ok=True);BG=(184,173,143,255)
rows=[('arg_line_early','Infantería de Línea (Early)','Pattern 1853 Enfield rifle-musket'),('arg_line_mid','Infantería de Línea (Mid)','Remington Rolling Block Modelo Argentino 1879 rifle'),('arg_line_high','Infantería del Ejército (Late)','Mauser Modelo Argentino 1891 magazine rifle'),('arg_national_guard_early','Guardia Nacional (Early)','assorted percussion infantry musket'),('arg_national_guard_mid','Guardia Nacional (Mid)','Pattern 1853 Enfield rifle-musket'),('arg_national_guard_high','Guardia Nacional (Late)','Remington Rolling Block Modelo Argentino 1879 rifle')]
def flatten(im):
 im=im.convert('RGBA').resize((48,64),Image.Resampling.LANCZOS);p=im.load();q=deque()
 for x in range(48):q.extend(((x,0),(x,63)))
 for y in range(64):q.extend(((0,y),(47,y)))
 seen=set()
 while q:
  x,y=q.popleft()
  if (x,y) in seen:continue
  r,g,b,a=p[x,y]; neutral=a<170 or (r>125 and g>110 and b>70 and abs(r-g)<60 and g-b<85 and r>=g-12)
  if not neutral:continue
  seen.add((x,y));p[x,y]=BG
  for z in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=z[0]<48 and 0<=z[1]<64 and z not in seen:q.append(z)
 return im
for uid,_,_ in rows:
 old=C/f'#{uid}.tga'; arc=A/old.name
 if not arc.exists():shutil.copy2(old,arc)
 im=Image.open(M/f'{uid}_v2_master.png').crop((4,8,1084,1448));flatten(im).save(old,format='TGA')
for uid in ('arg_cavalry_early','arg_cavalry_mid','arg_cavalry_high'):
 p=C/f'#{uid}.tga';arc=A/p.name
 if not arc.exists():shutil.copy2(p,arc)
 flatten(Image.open(p)).save(p,format='TGA')
reg=R/'tools/historical_card_sources.json';data=json.loads(reg.read_text(encoding='utf-8'));ids={x[0] for x in rows};data=[x for x in data if x.get('id') not in ids]
for uid,name,w in rows:data.append(dict(id=uid,unit_type=uid,card_file=f'data/ui/units/aztecs/#{uid}.tga',faction='aztecs',name=name,role='standing firearm infantry',weapon=w,source_url='https://www.memoria.fahce.unlp.edu.ar/tesis/te.1417/te.1417.pdf',source_file='tools/historical_card_refs/argentina_army_1862_1880.pdf',source_title='El proceso de profesionalización del Ejército Argentino (1862-1880)',creator='Argentine military-history thesis repository, Universidad Nacional de La Plata',source_date='historical study covering 1862-1880',licence='Institutional repository reference use',depicted_subject='Argentine Army uniforms, organization and equipment',pose_source_id='',mapping_note='New unit-specific standing composition follows the period slot, exact named firearm, actual loaded Argentine model appearance, and a separated cap/head silhouette.',status='card-approved',generated_file=f'tools/card_generation_sources/argentina_20260915/{uid}_v2_master.png',crop_box=[4,8,1084,1448]))
reg.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Regenerated six infantry cards and canonicalized three cavalry backgrounds.')