from pathlib import Path
from collections import deque,Counter
import shutil, json, math
from PIL import Image
R=Path(__file__).resolve().parents[1]; C=R/'data/ui/units/byzantium'; A=R/'tools/card_source_archive/qing_before_background_normalization_20260919'
A.mkdir(parents=True,exist_ok=True)
units=['qing_green_banner_spears','qing_green_banner_gunmen','qing_green_banner_archers','qing_green_banner_regulars','qing_new_army','qing_green_banner_late','qing_xiang_huai_early','qing_xiang_huai_mid','qing_beiyang_infantry','qing_baqi_gunmen','qing_green_banner_horse','qing_eight_banner_cavalry','qing_village_braves','oirat_royal']
BG=(184,173,143,255); report=[]
for u in units:
 p=C/f'#{u}.tga'; assert p.exists(),p; shutil.copy2(p,A/p.name); im=Image.open(p).convert('RGBA'); assert im.size==(48,64),(u,im.size)
 px=im.load(); border=[px[x,y] for x in range(48) for y in range(64) if x in (0,47) or y in (0,63)]
 seedcol=Counter(border).most_common(1)[0][0]; q=deque(); seen=set()
 for x in range(48): q.extend(((x,0),(x,63)))
 for y in range(64): q.extend(((0,y),(47,y)))
 while q:
  x,y=q.popleft()
  if (x,y) in seen: continue
  c=px[x,y]; d=sum((c[i]-seedcol[i])**2 for i in range(3))**.5
  if d>12: continue
  seen.add((x,y));
  for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=nx<48 and 0<=ny<64 and (nx,ny) not in seen:
    nc=px[nx,ny]; step=sum((nc[i]-c[i])**2 for i in range(3))**.5
    if step<=8: q.append((nx,ny))
 for x,y in seen: px[x,y]=BG
 im.save(p); report.append({'unit':u,'source_background':seedcol,'pixels_normalized':len(seen)})
(R/'tools/qing_card_background_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
