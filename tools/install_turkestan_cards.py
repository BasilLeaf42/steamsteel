from pathlib import Path
from collections import deque
from PIL import Image
import json, shutil, struct

ROOT=Path(__file__).resolve().parents[1]
master=Image.open(ROOT/'tools/card_generation_sources/turkestan_skirmishers_command_20260916.png').convert('RGBA')
out=ROOT/'data/ui/units/cuman'; archive=ROOT/'tools/card_source_archive/turkestan_before_role_card_replacement_20260916'
archive.mkdir(parents=True,exist_ok=True)
specs={
 'ghulja_inf':((0,15,625,848),'kokand_palace_soldiers_1860s.png','Kokand palace soldiers','Aleksandr L. Kun','1865-1872','https://commons.wikimedia.org/wiki/File:Kokand_Khanate._City_of_Kokand._Palace_of_Said_Khudoyar_Khan,_with_Soldiers_of_the_Kokand_Khan%27s_Army_Standing_Outside_the_Entrance,_and_a_Russian_Officer_Standing_in_the_Center_WDL10726.png','Ghulja frontier arquebus skirmisher'),
 'buk_guard':((628,15,1253,848),'kokand_soldier_vereshchagin.jpg','Kokand soldier','Vasily Vereshchagin','1873','https://commons.wikimedia.org/wiki/File:%D0%9A%D0%BE%D0%BA%D0%B0%D0%BD%D0%B4%D1%81%D0%BA%D0%B8%D0%B9_%D1%81%D0%BE%D0%BB%D0%B4%D0%B0%D1%82.jpg','Darkhan long-gun skirmisher'),
 'kok_rcav':((1256,15,1881,848),'khudayar_khan_and_sons.png','Kokand Khan and his sons','Aleksandr L. Kun','1865-1872','https://commons.wikimedia.org/wiki/File:Kokand_Khan_and_His_Sons._Seid_Mukhamed_Khudayar_Khan,_Kokand_Khan_WDL10718.png','mounted Qorboshi and staff')}
regp=ROOT/'tools/historical_card_sources.json'; reg=json.loads(regp.read_text(encoding='utf-8'))
for name,(box,src,title,creator,date,url,subject) in specs.items():
 card=out/f'#{name}.tga'
 if not (archive/card.name).exists(): shutil.copy2(card,archive/card.name)
 im=master.crop(box); px=im.load(); w,h=im.size; q=deque(); seen=set()
 for x in range(w): q.extend(((x,0),(x,h-1)))
 for y in range(h): q.extend(((0,y),(w-1,y)))
 def bg(c):
  r,g,b,a=c; return a and 110<r<235 and 95<g<220 and 65<b<190 and r>=g>=b and r-b<100
 while q:
  x,y=q.popleft()
  if (x,y) in seen: continue
  seen.add((x,y))
  if not bg(px[x,y]): continue
  px[x,y]=(184,173,143,255)
  if x:q.append((x-1,y))
  if x+1<w:q.append((x+1,y))
  if y:q.append((x,y-1))
  if y+1<h:q.append((x,y+1))
 im=im.resize((48,64),Image.Resampling.LANCZOS).convert('RGBA'); p=im.load()
 for c in ((0,0),(47,0),(0,63),(47,63)): p[c]=(184,173,143,255)
 im.save(Path('\\\\?\\'+str(card)),format='TGA')
 reg=[x for x in reg if x.get('id')!=name]
 reg.append({'id':name,'group_id':'turkestan_role_cards_20260916','unit_type':name,'card_file':f'data/ui/units/cuman/#{name}.tga','faction':'cuman','name':subject,'role':'skirmisher' if name!='kok_rcav' else 'general and staff','source_url':url,'source_file':f'tools/historical_card_refs/{src}','source_title':title,'creator':creator,'source_date':date,'licence':'Public domain','depicted_subject':subject,'mapping_note':'Historical reference controls period dress and role; generated composition follows the loaded card uniform and required kneeling or passive mounted command posture.','pose_source_id':'kneel_aim_photo_1871' if name!='kok_rcav' else '','status':'card-approved','generated_file':'tools/card_generation_sources/turkestan_skirmishers_command_20260916.png','crop_box':list(box)})
 d=Path('\\\\?\\'+str(card)).read_bytes(); assert struct.unpack_from('<HH',d,12)==(48,64) and d[16]==32
regp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(archive/'original_members.json').write_text(json.dumps({'archived_from':'data/ui/units/cuman','members':list(specs)},indent=2),encoding='utf-8')
# Normalize the exposed background of every retained tactical card without
# crossing the figure silhouette.
all_cards=['kok_spears','turkmen_inf','ghulja_inf','buk_guard','kok_ww1','kashgar_inf','kok_inf','kok_cav','kok_royal_cav','kaz_cav','uyghur_camel_cav','kok_rcav','camel_wagon']
for name in all_cards:
 card=out/f'#{name}.tga'; im=Image.open(card).convert('RGBA'); px=im.load(); w,h=im.size
 border=[px[x,y] for x,y in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]]; q=deque((x,y) for x in range(w) for y in (0,h-1)); q.extend((x,y) for y in range(h) for x in (0,w-1)); seen=set()
 def near(c): return any(sum((c[i]-s[i])**2 for i in range(3))<=38**2 for s in border)
 while q:
  x,y=q.popleft()
  if (x,y) in seen: continue
  seen.add((x,y))
  if not near(px[x,y]): continue
  px[x,y]=(184,173,143,255)
  if x:q.append((x-1,y))
  if x+1<w:q.append((x+1,y))
  if y:q.append((x,y-1))
  if y+1<h:q.append((x,y+1))
 im.save(Path('\\\\?\\'+str(card)),format='TGA')
print('Installed three sourced Turkestan role-correct tactical cards.')
