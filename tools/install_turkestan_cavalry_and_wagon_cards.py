from collections import deque
from pathlib import Path
from PIL import Image
import io, json, shutil, struct, subprocess

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'data/ui/units/cuman'
ARCH=ROOT/'tools/card_source_archive/turkestan_cavalry_wagon_20260917'; ARCH.mkdir(parents=True,exist_ok=True)
for name in ('kok_royal_cav','camel_wagon'):
 card=OUT/f'#{name}.tga'
 if not (ARCH/card.name).exists(): shutil.copy2(card,ARCH/card.name)
raw=subprocess.check_output(['git','show','HEAD:data/ui/units/cuman/#camel_wagon.tga'],cwd=ROOT)
wagon=Image.open(io.BytesIO(raw)).convert('RGBA'); assert wagon.size==(48,64)
wagon.save(Path('\\\\?\\'+str(OUT/'#camel_wagon.tga')),format='TGA')
master=Image.open(ROOT/'tools/card_generation_sources/turkestan_turkman_carbine_cavalry_20260917.png').convert('RGBA')
px=master.load(); w,h=master.size; q=deque([(0,0),(w-1,0)]); seen=set()
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
card=master.resize((48,64),Image.Resampling.LANCZOS).convert('RGBA')
for xy in ((0,0),(47,0),(0,63),(47,63)): card.putpixel(xy,(184,173,143,255))
card.save(Path('\\\\?\\'+str(OUT/'#kok_royal_cav.tga')),format='TGA')
regp=ROOT/'tools/historical_card_sources.json'; reg=json.loads(regp.read_text(encoding='utf-8')); reg=[x for x in reg if x.get('id')!='kok_royal_cav']
reg.append({'id':'kok_royal_cav','group_id':'turkestan_turkman_carbine_20260917','unit_type':'kok_royal_cav','card_file':'data/ui/units/cuman/#kok_royal_cav.tga','faction':'cuman','name':'Turkman Otliqlari','role':'carbine cavalry','weapon':'visible matchlock carbine and sheathed curved sword','source_url':'https://commons.wikimedia.org/wiki/File:A_Persian_Cavalier_smoking_(Letters_from_the_Caucasus_and_Georgia).jpg','source_file':'tools/historical_card_refs/qaj_persian_cavalier_1812.jpg','source_title':'A Persian Cavalier smoking','creator':'Fredrika and Wilhelm von Freygang','source_date':'Observed 1812; published 1823','licence':'Public domain via Wikimedia Commons','depicted_subject':'Qajar-era regional cavalrymen mounted on campaign','mapping_note':'Regional source controls upright mounted balance and rider-horse relationship; loaded Turkman mesh controls local dress, horse tack, matchlock carbine and sheathed sword. Card visibly shows the complete carbine and no lance.','pose_source_id':'','status':'card-approved','generated_file':'tools/card_generation_sources/turkestan_turkman_carbine_cavalry_20260917.png','crop_box':[0,0,1536,2048]})
regp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('kok_royal_cav','camel_wagon'):
 d=Path('\\\\?\\'+str(OUT/f'#{name}.tga')).read_bytes(); assert struct.unpack_from('<HH',d,12)==(48,64) and d[16]==32
(ARCH/'original_members.json').write_text(json.dumps({'archived_from':'data/ui/units/cuman','members':['kok_royal_cav','camel_wagon']},indent=2),encoding='utf-8')
print('Installed visible-carbine Turkman cavalry card and restored intact camel-fort card.')
