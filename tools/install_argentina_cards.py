from pathlib import Path
from collections import deque
import json, shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
CARD=ROOT/'data/ui/units/aztecs'; MASTER=ROOT/'tools/card_generation_sources/argentina_20260915'
ARCH=ROOT/'tools/card_source_archive/argentina_before_standardization'; ARCH.mkdir(parents=True,exist_ok=True)
for p in CARD.glob('*.tga'):
 q=ARCH/p.name
 if not q.exists(): shutil.copy2(p,q)
CAN=(184,173,143,255)
def normalize(im):
 im=im.convert('RGBA').resize((48,64),Image.Resampling.LANCZOS); px=im.load(); q=deque()
 for x in range(48): q.extend(((x,0),(x,63)))
 for y in range(64): q.extend(((0,y),(47,y)))
 seen=set()
 while q:
  x,y=q.popleft()
  if (x,y) in seen: continue
  r,g,b,a=px[x,y]; bg=a<160 or (145<=r<=245 and 125<=g<=230 and 80<=b<=205 and abs(r-g)<=45 and r>=g-8 and g>=b-12)
  if not bg: continue
  seen.add((x,y)); px[x,y]=CAN
  for z in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=z[0]<48 and 0<=z[1]<64:q.append(z)
 for y in range(64):
  for x in range(48):
   if px[x,y][3]<128:px[x,y]=CAN
 return im
def save(im,name):
 out=CARD/f'#{name}.tga'; normalize(im).save(out,format='TGA'); raw=out.read_bytes()
 if int.from_bytes(raw[12:14],'little')!=48 or int.from_bytes(raw[14:16],'little')!=64 or raw[16]!=32: raise RuntimeError(name)
def donor(src,*names):
 im=Image.open(CARD/f'#{src}.tga')
 for n in names:save(im,n)
def generated(file,crop,*names):
 im=Image.open(MASTER/file).convert('RGBA').crop(crop)
 if im.width*4!=im.height*3: raise RuntimeError(file)
 for n in names:save(im,n)
donor('arg_inf','arg_line_early','arg_line_mid')
donor('argie_pith','arg_line_high')
donor('arg_guard','arg_national_guard_early','arg_national_guard_mid','arg_national_guard_high')
donor('arg_carb','arg_cavalry_early','arg_cavalry_mid','arg_cavalry_high')
donor('gaucho_cav','arg_frontier_gauchos')
generated('arg_general_staff_master.png',(4,8,1084,1448),'arg_general_staff')
generated('arg_cazadores_early_master.png',(4,8,1084,1448),'arg_cazadores_early')
generated('arg_cazadores_mid_master.png',(4,8,1084,1448),'arg_cazadores_mid')
generated('arg_tiradores_high_master.png',(4,8,1084,1448),'arg_tiradores_high')
generated('arg_lancers_master.png',(4,8,1084,1448),'arg_lancers_early','arg_lancers_mid')
REG=ROOT/'tools/historical_card_sources.json'; data=json.loads(REG.read_text(encoding='utf-8'))
base=dict(faction='aztecs',source_url='https://www.memoria.fahce.unlp.edu.ar/tesis/te.1417/te.1417.pdf',source_file='tools/historical_card_refs/argentina_army_1862_1880.pdf',source_title='El proceso de profesionalización del Ejército Argentino (1862-1880)',creator='Argentine military-history thesis repository, Universidad Nacional de La Plata',source_date='historical study covering 1862-1880',licence='Institutional repository reference use',depicted_subject='Argentine Army organization, uniforms and professionalization',status='card-approved')
rows=[
 ('arg_general_staff','General y Estado Mayor','mounted general and staff','no weapon held; sidearm holstered','arg_general_staff_master.png','Mounted passive command composition; horse and tack visible, folded map and no held weapon.'),
 ('arg_cazadores_early','Cazadores (Early)','infantry skirmisher','Pattern 1853 Enfield rifle-musket','arg_cazadores_early_master.png','Argentine period appearance with approved kneeling skirmisher anatomy and coherent muzzle-loading rifle handling.'),
 ('arg_cazadores_mid','Cazadores (Mid)','infantry skirmisher','Remington Rolling Block Modelo Argentino 1879 rifle','arg_cazadores_mid_master.png','Argentine period appearance with approved kneeling skirmisher anatomy and coherent Rolling Block handling.'),
 ('arg_tiradores_high','Tiradores (Late)','infantry skirmisher','Mauser Modelo Argentino 1891 magazine rifle','arg_tiradores_high_master.png','Late Argentine appearance with approved kneeling skirmisher anatomy and coherent bolt-action rifle handling.'),
 ('arg_lancers_early','Lanceros de Frontera','mounted lancer','Western military lance and sabre','arg_lancers_master.png','Mounted Argentine frontier composition with horse, tack and one mechanically coherent Western lance.'),
 ('arg_lancers_mid','Lanceros de Frontera (Mid)','mounted lancer','Western military lance and sabre','arg_lancers_master.png','Approved sharing within the unchanged Lanceros lineage; identical loaded model and equipment.')]
ids={r[0] for r in rows}; data=[r for r in data if r.get('id') not in ids]
for uid,name,role,weapon,file,note in rows:
 rec=dict(base,id=uid,unit_type=uid,card_file=f'data/ui/units/aztecs/#{uid}.tga',name=name,role=role,weapon=weapon,generated_file=f'tools/card_generation_sources/argentina_20260915/{file}',crop_box=[4,8,1084,1448],mapping_note=note,pose_source_id='kneel_aim_photo_1871' if 'skirmisher' in role else '')
 data.append(rec)
REG.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for r in data:
 if r.get('id') in ids and (not (ROOT/r['source_file']).exists() or not (ROOT/r['generated_file']).exists()):raise RuntimeError(r['id'])
print('Installed 16 Argentine tactical cards; 6 generated source mappings approved.')