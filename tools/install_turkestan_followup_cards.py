from collections import deque
from pathlib import Path
from PIL import Image
import json, shutil, struct

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/ui/units/cuman'
ARCH=ROOT/'tools/card_source_archive/turkestan_followup_20260917'
ARCH.mkdir(parents=True,exist_ok=True)
specs={
 'kok_spears': dict(master='turkestan_spear_levy_20260917.png', role='spear-and-shield levy', weapon='long spear and round shield', source_file='tools/historical_card_refs/kokand_palace_soldiers_1860s.png', source_url='https://commons.wikimedia.org/wiki/File:Kokand_Khanate._City_of_Kokand._Palace_of_Said_Khudoyar_Khan,_with_Soldiers_of_the_Kokand_Khan%27s_Army_Standing_Outside_the_Entrance,_and_a_Russian_Officer_Standing_in_the_Center_WDL10726.png', source_title='Kokand palace soldiers', creator='Aleksandr L. Kun', date='1865-1872', subject='Kokand soldiers outside the palace'),
 'turkmen_inf': dict(master='turkestan_matchlock_sword_20260917.png', role='matchlock infantry with sword', weapon='matchlock musket and sheathed curved sword; no shield or bayonet', source_file='tools/historical_card_refs/kokand_soldier_vereshchagin.jpg', source_url='https://commons.wikimedia.org/wiki/File:%D0%9A%D0%BE%D0%BA%D0%B0%D0%BD%D0%B4%D1%81%D0%BA%D0%B8%D0%B9_%D1%81%D0%BE%D0%BB%D0%B4%D0%B0%D1%82.jpg', source_title='Kokand soldier', creator='Vasily Vereshchagin', date='1873', subject='Kokand soldier in local dress'),
 'uyghur_camel_cav': dict(master='turkestan_uyghur_camelry_20260917.png', role='mounted arquebus camelry', weapon='matchlock arquebus', source_file='tools/historical_card_refs/afg_camel_drivers_1870.jpg', source_url='https://commons.wikimedia.org/wiki/File:Afghan_camel_drivers_1870.jpg', source_title='Afghan camel drivers 1870', creator='Photographer unidentified', date='1870', subject='Central Asian camel drivers mounted with their camels')}

reg_path=ROOT/'tools/historical_card_sources.json'; reg=json.loads(reg_path.read_text(encoding='utf-8'))
for name,s in specs.items():
 reg=[x for x in reg if x.get('id')!=name]
 reg.append({'id':name,'group_id':'turkestan_followup_20260917','unit_type':name,'card_file':f'data/ui/units/cuman/#{name}.tga','faction':'cuman','name':name,'role':s['role'],'weapon':s['weapon'],'source_url':s['source_url'],'source_file':s['source_file'],'source_title':s['source_title'],'creator':s['creator'],'source_date':s['date'],'licence':'Public domain','depicted_subject':s['subject'],'mapping_note':'The historical source controls period dress and mounted or foot relationship; the loaded mesh controls role and visible equipment. Generated composition explicitly distinguishes spear-and-shield, matchlock-and-sword, and camel-mounted arquebus roles.','pose_source_id':'','status':'card-approved','generated_file':f"tools/card_generation_sources/{s['master']}",'crop_box':[0,0,1536,2048]})
reg_path.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
approved={x['id']:x for x in reg if x.get('status')=='card-approved'}
for name,s in specs.items():
 assert name in approved and all(approved[name].get(k) for k in ('source_url','source_file','source_title','creator','source_date','licence','generated_file'))
 card=OUT/f'#{name}.tga'
 if not (ARCH/card.name).exists(): shutil.copy2(card,ARCH/card.name)
 im=Image.open(ROOT/'tools/card_generation_sources'/s['master']).convert('RGBA')
 px=im.load(); w,h=im.size; q=deque([(0,0),(w-1,0)]); seen=set()
 while q:
  x,y=q.popleft()
  if (x,y) in seen: continue
  seen.add((x,y)); c=px[x,y]
  if max(c[:3])-min(c[:3])>48: continue
  px[x,y]=(184,173,143,255)
  for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=nx<w and 0<=ny<h and (nx,ny) not in seen:
    n=px[nx,ny]
    if sum((n[i]-c[i])**2 for i in range(3))<=12*12:q.append((nx,ny))
 im=im.resize((48,64),Image.Resampling.LANCZOS).convert('RGBA')
 for xy in ((0,0),(47,0),(0,63),(47,63)): im.putpixel(xy,(184,173,143,255))
 im.save(Path('\\\\?\\'+str(card)),format='TGA')
 raw=Path('\\\\?\\'+str(card)).read_bytes(); assert struct.unpack_from('<HH',raw,12)==(48,64) and raw[16]==32
(ARCH/'original_members.json').write_text(json.dumps({'archived_from':'data/ui/units/cuman','members':list(specs)},indent=2),encoding='utf-8')
print('Installed sourced, role-correct Turkestan spear, matchlock-sword and camelry cards.')
