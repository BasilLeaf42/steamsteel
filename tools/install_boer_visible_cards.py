from pathlib import Path
from collections import deque
from PIL import Image
import json, shutil

ROOT=Path(__file__).resolve().parents[1]
CARDS=ROOT/'data/ui/units/teu'
ARCH=ROOT/'tools/card_source_archive/boers_before_visible_gen_carb_replacement_20260916'
ARCH.mkdir(parents=True,exist_ok=True)
members=['csa_lancer_te','boer_mounted_kommando_early','boer_mounted_kommando_mid','boer_mounted_kommando_high']
for n in members:
 p=CARDS/f'#{n}.tga'; q=ARCH/p.name
 if not q.exists(): shutil.copy2(p,q)
(ARCH/'original_members.json').write_text(json.dumps({'archived_from':'data/ui/units/teu','members':members},indent=2),encoding='utf-8')

def install(master_name, targets):
 im=Image.open(ROOT/f'tools/card_generation_sources/{master_name}').convert('RGBA')
 w,h=im.size; cw=min(w,(h*3)//4); ch=(cw*4)//3
 if ch>h: ch=h; cw=(ch*3)//4
 x=(w-cw)//2; y=(h-ch)//2; crop=(x,y,x+cw,y+ch)
 im=im.crop(crop)
 px=im.load(); W,H=im.size; seen=set(); q=deque()
 for xx in range(W): q.extend(((xx,0),(xx,H-1)))
 for yy in range(H): q.extend(((0,yy),(W-1,yy)))
 def bg(c):
  r,g,b,a=c
  return a>0 and r>=145 and g>=135 and b>=105 and max(r,g,b)-min(r,g,b)<=95
 while q:
  p=q.popleft()
  if p in seen: continue
  seen.add(p); xx,yy=p
  if not bg(px[xx,yy]): continue
  px[xx,yy]=(184,173,143,255)
  if xx:q.append((xx-1,yy))
  if xx+1<W:q.append((xx+1,yy))
  if yy:q.append((xx,yy-1))
  if yy+1<H:q.append((xx,yy+1))
 final=im.resize((48,64),Image.Resampling.LANCZOS).convert('RGBA')
 # Exact canonical background at corners and transparent-free RGBA output.
 fp=final.load()
 for xx,yy in ((0,0),(47,0),(0,63),(47,63)): fp[xx,yy]=(184,173,143,255)
 for t in targets: final.save(CARDS/f'#{t}.tga',format='TGA')
 return list(crop)

gen_crop=install('boer_general_staff_20260916_master.png',['csa_lancer_te'])
cav_types=['boer_mounted_kommando_early','boer_mounted_kommando_mid','boer_mounted_kommando_high']
cav_crop=install('boer_mounted_kommando_20260916_master.png',cav_types)

reg_path=ROOT/'tools/historical_card_sources.json'
reg=json.loads(reg_path.read_text(encoding='utf-8'))
reg=[e for e in reg if e.get('id') not in {'csa_lancer_te',*cav_types}]
reg.append({
 'id':'csa_lancer_te','group_id':'boer_general_staff_20260916','unit_type':'csa_lancer_te',
 'card_file':'data/ui/units/teu/#csa_lancer_te.tga','faction':'teu','name':'Generaal en Staf',
 'role':'general and staff','weapon':'none held',
 'source_url':'https://commons.wikimedia.org/wiki/File:Portret_van_generaal_Louis_Botha_te_paard_Generaal_L._Botha_(titel_op_object),_RP-F-F00999-FC.jpg',
 'source_file':'tools/historical_card_refs/boer_general_louis_botha_mounted_1899.jpg',
 'source_title':'Portret van generaal Louis Botha te paard','creator':'Jan van Hoepen',
 'source_date':'1899–1900','licence':'Public domain',
 'depicted_subject':'Commandant-General Louis Botha mounted on horseback',
 'mapping_note':'Historical mounted-command composition; generated card is weapon-free, mounted, and uses a folded field map with visible reins and tack.',
 'pose_source_id':'','status':'card-approved',
 'generated_file':'tools/card_generation_sources/boer_general_staff_20260916_master.png','crop_box':gen_crop})
weapons={'early':'Pattern 1856 Enfield cavalry carbine','mid':'Westley Richards Monkey Tail carbine','high':'Mauser Model 1895 short rifle'}
for era in ('early','mid','high'):
 t=f'boer_mounted_kommando_{era}'
 reg.append({
  'id':t,'group_id':'boer_mounted_kommando_20260916','unit_type':t,
  'card_file':f'data/ui/units/teu/#{t}.tga','faction':'teu','name':f'Berede Boerekommando ({era})',
  'role':'carbine cavalry','weapon':weapons[era],
  'source_url':'https://commons.wikimedia.org/wiki/File:1899_Boer_Commando_-_Pretoria.jpg',
  'source_file':'tools/historical_card_refs/boer_commando_pretoria_1899.jpg',
  'source_title':'1899 Boer Commando - Pretoria','creator':'Anonymous; South African Photo Archives',
  'source_date':'1899','licence':'Public domain',
  'depicted_subject':'Mounted Boer commandos assembled with horses and rifles',
  'mapping_note':'Intentional sharing within one unchanged model lineage; the visible in-game carbine geometry is unchanged across periods. New mounted composition clearly shows complete carbine, two-hand grip, horse, bridle and tack; no pistol.',
  'pose_source_id':'','status':'card-approved',
  'generated_file':'tools/card_generation_sources/boer_mounted_kommando_20260916_master.png','crop_box':cav_crop})
reg_path.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Installed new visible Boer general and carbine tactical cards and registered sources.')
