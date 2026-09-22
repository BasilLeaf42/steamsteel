from collections import Counter, deque
from pathlib import Path
import json
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
MASTER=ROOT/'tools/card_generation_sources/brazil_20260915'
CARD=ROOT/'data/ui/units/poland'
REG=ROOT/'tools/historical_card_sources.json'
CAN=(184,173,143,255)
records=[
 dict(id='bra_general_staff',unit_type='bra_general_staff',card_file='data/ui/units/poland/#bra_general_staff.tga',faction='poland',name='General e Estado-Maior',role='mounted general and staff',weapon='no weapon held; sidearm holstered',source_url='https://commons.wikimedia.org/wiki/File:Brazilian_officer_and_Paraguayan_soldier.jpg',source_file='tools/historical_card_refs/bra_cavalry_officer_1866.jpg',source_title='Brazilian cavalry officer and Paraguayan prisoner',creator='Photographer unidentified',source_date='circa 1866',licence='Public Domain Mark',depicted_subject='Mounted Brazilian officer during the Paraguayan War',pose_source_id='',mapping_note='The period photograph controls national officer appearance. The card follows the universal mounted-command rule: horse and tack visible, passive posture, folded dispatch and binoculars, and no weapon held.',status='card-approved',generated_file='tools/card_generation_sources/brazil_20260915/bra_general_staff_master.png',crop_box=[4,8,1084,1448]),
 dict(id='bra_cavalry_early',unit_type='bra_cavalry_early',card_file='data/ui/units/poland/#bra_cavalry_early.tga',faction='poland',name='Cavalaria de Linha',role='mounted carbine cavalry',weapon='Pattern 1853 Enfield percussion cavalry carbine',source_url='https://commons.wikimedia.org/wiki/File:Brazilian_officer_and_Paraguayan_soldier.jpg',source_file='tools/historical_card_refs/bra_cavalry_officer_1866.jpg',source_title='Brazilian cavalry officer and Paraguayan prisoner',creator='Photographer unidentified',source_date='circa 1866',licence='Public Domain Mark',depicted_subject='Brazilian cavalry officer during the Paraguayan War',pose_source_id='',mapping_note='The Brazilian photograph controls national period appearance. Library of Congress mounted cavalry source https://www.loc.gov/pictures/item/2012648975/ controls rider, horse and tack relationship. Card visibly presents the named Enfield cavalry carbine.',status='card-approved',generated_file='tools/card_generation_sources/brazil_20260915/bra_cavalry_early_master.png',crop_box=[4,8,1084,1448]),
 dict(id='bra_dragoons_mid',unit_type='bra_dragoons_mid',card_file='data/ui/units/poland/#bra_dragoons_mid.tga',faction='poland',name='Dragões (Mid)',role='mounted carbine cavalry',weapon='Spencer Model 1865 repeating carbine',source_url='https://commons.wikimedia.org/wiki/File:Brazilian_officer_and_Paraguayan_soldier.jpg',source_file='tools/historical_card_refs/bra_cavalry_officer_1866.jpg',source_title='Brazilian cavalry officer and Paraguayan prisoner',creator='Photographer unidentified',source_date='circa 1866',licence='Public Domain Mark',depicted_subject='Brazilian cavalry officer during the Paraguayan War',pose_source_id='',mapping_note='Brazilian uniform reference plus the approved Library of Congress mounted-cavalry pose source. Distinct low-ready composition visibly presents the Spencer carbine and horse.',status='card-approved',generated_file='tools/card_generation_sources/brazil_20260915/bra_dragoons_mid_master.png',crop_box=[4,8,1084,1448]),
 dict(id='bra_dragoons_high',unit_type='bra_dragoons_high',card_file='data/ui/units/poland/#bra_dragoons_high.tga',faction='poland',name='Dragões (Late)',role='mounted carbine cavalry',weapon='Mannlicher M1888-90 cavalry carbine',source_url='https://commons.wikimedia.org/wiki/File:Brazilian_officer_and_Paraguayan_soldier.jpg',source_file='tools/historical_card_refs/bra_cavalry_officer_1866.jpg',source_title='Brazilian cavalry officer and Paraguayan prisoner',creator='Photographer unidentified',source_date='circa 1866',licence='Public Domain Mark',depicted_subject='Brazilian cavalry officer; late equipment is an explicit period extension',pose_source_id='',mapping_note='National appearance is extended conservatively to the late slot. Distinct shoulder-ready composition visibly presents a bolt-action cavalry carbine and mounted tack.',status='card-approved',generated_file='tools/card_generation_sources/brazil_20260915/bra_dragoons_high_master.png',crop_box=[4,8,1084,1448]),
]
for uid,name,weapon,master in [
 ('bra_cacadores_early','Caçadores (Early)','Pattern 1856 Enfield short rifle','bra_cacadores_early_master.png'),
 ('bra_cacadores_mid','Caçadores (Mid)','Brazilian Comblain M1873 rifle','bra_cacadores_mid_master.png'),
 ('bra_atiradores_high','Atiradores (Late)','Mauser M1894 magazine rifle','bra_atiradores_high_master.png')]:
 records.append(dict(id=uid,unit_type=uid,card_file=f'data/ui/units/poland/#{uid}.tga',faction='poland',name=name,role='infantry skirmisher',weapon=weapon,source_url='https://bndigital.bn.gov.br/dossies/guerra-do-paraguai/artigos/uniformes-da-guerra-do-paraguai/',source_file='tools/historical_card_refs/bra_cacadores_1866_1870_plate.jpg',source_title='Exército Brasileiro – Infantaria Ligeira – Caçadores, 1866-1870',creator='José Wasth Rodrigues',source_date='historical uniform plate; published collection',licence='Reference use; BNDigital provides public-domain or authorized collection material',depicted_subject='Brazilian Caçadores uniforms and equipment',pose_source_id='kneel_aim_photo_1871',mapping_note='The Brazilian plate controls national uniform and equipment; the approved pool master controls the one-knee anatomy and two-handed rifle handling. The traced bra_lgt model controls the broad pale campaign hat and dark-blue/red-trim field appearance.',status='card-approved',generated_file=f'tools/card_generation_sources/brazil_20260915/{master}',crop_box=[188,0,1088,1200]))
records.append(dict(id='bra_zuavos_early',unit_type='bra_zuavos_early',card_file='data/ui/units/poland/#bra_zuavos_early.tga',faction='poland',name='Zuavos Baianos',role='infantry skirmisher / light infantry',weapon='Pattern 1853 Enfield rifle-musket',source_url='https://bndigital.bn.gov.br/dossies/rede-da-memoria-virtual-brasileira/personagens-e-persolanidades/dom-oba-ii-dafrica-o-principe-do-povo/',source_file='tools/historical_card_refs/bra_voluntarios_zuavo_1865_1870_plate.jpg',source_title='Exército Brasileiro – Voluntários da Pátria, 1865-1870',creator='José Wasth Rodrigues',source_date='historical uniform plate; published collection',licence='Reference use; BNDigital provides public-domain or authorized collection material',depicted_subject='Voluntários da Pátria including a Zuavo da Bahia',pose_source_id='kneel_aim_photo_1871',mapping_note='The plate controls the distinctive blue-and-yellow jacket, red fez and red trousers. The approved pool pose controls one-knee anatomy; the genuine fra_zou mesh with its original Latin face attachment supplies a compatible in-game Zouave donor.',status='card-approved',generated_file='tools/card_generation_sources/brazil_20260915/bra_zuavos_early_master.png',crop_box=[250,40,970,1000]))

data=json.loads(REG.read_text(encoding='utf-8'))
ids={r['id'] for r in records}
data=[r for r in data if r.get('id') not in ids]+records
REG.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
check={r['id']:r for r in json.loads(REG.read_text(encoding='utf-8'))}
for r in records:
 c=check[r['id']]
 for key in ('source_url','source_file','source_title','creator','source_date','licence','depicted_subject','mapping_note','generated_file','crop_box'):
  if not c.get(key): raise RuntimeError(f'{r["id"]}: incomplete {key}')
 if c.get('status')!='card-approved': raise RuntimeError(f'{r["id"]}: source mapping not approved')
 if not (ROOT/c['source_file']).exists() or not (ROOT/c['generated_file']).exists(): raise RuntimeError(f'{r["id"]}: source asset missing')

def install(r):
 im=Image.open(ROOT/r['generated_file']).convert('RGBA').crop(tuple(r['crop_box']))
 if im.width*4!=im.height*3: raise RuntimeError(f'{r["id"]}: crop not 3:4')
 im=im.resize((48,64),Image.Resampling.LANCZOS)
 px=im.load(); border=[px[x,y] for x in range(48) for y in (0,63)]+[px[x,y] for y in range(64) for x in (0,47)]; palette=[c for c,_ in Counter(q[:3] for q in border if q[3]>180).most_common(20)]
 for y in range(64):
  for x in range(48):
   q=px[x,y]; neutral=q[0]>145 and q[1]>125 and q[2]>80 and q[0]-q[1]<42 and q[1]-q[2]<70
   if neutral and palette and min(sum((q[i]-c[i])**2 for i in range(3))**0.5 for c in palette)<=28:px[x,y]=CAN
 q=deque()
 for x in range(48): q.extend(((x,0),(x,63)))
 for y in range(64): q.extend(((0,y),(47,y)))
 seen=set()
 while q:
  x,y=q.popleft()
  if (x,y) in seen: continue
  red,green,blue,alpha=px[x,y]
  candidate=alpha<160 or (145<=red<=245 and 125<=green<=230 and 80<=blue<=205 and abs(red-green)<=42 and red>=green-5 and green>=blue-10)
  if not candidate: continue
  seen.add((x,y)); px[x,y]=CAN
  for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=nx<48 and 0<=ny<64 and (nx,ny) not in seen:q.append((nx,ny))
 for y in range(64):
  for x in range(48):
   if px[x,y][3]<128:px[x,y]=CAN
 out=ROOT/r['card_file'];im.save(out,format='TGA')
 raw=out.read_bytes()
 if int.from_bytes(raw[12:14],'little')!=48 or int.from_bytes(raw[14:16],'little')!=64 or raw[16]!=32 or raw[17]&15<8: raise RuntimeError(f'{r["id"]}: bad TGA format')
for r in records:install(r)
print(f'Installed and source-approved {len(records)} Brazilian tactical cards.')