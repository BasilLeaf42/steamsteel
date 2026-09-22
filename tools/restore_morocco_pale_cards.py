from PIL import Image
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1];C=R/'data/ui/units/moors';M=R/'tools/card_generation_sources/morocco_20260915';BG=(184,173,143,255)
rows=['mor_makhzen_early','mor_makhzen_mid','mor_makhzen_high','mor_abid_early','mor_abid_mid','mor_rif_early','mor_rif_mid','mor_rif_high','mor_hajjana']
for n in rows:
 im=Image.open(M/f'{n}_v2_master.png').convert('RGBA').crop((4,8,1084,1448)).resize((48,64),Image.Resampling.LANCZOS);p=im.load();corner=p[0,0][:3];q=deque([(x,0) for x in range(48)]+[(x,63) for x in range(48)]+[(0,y) for y in range(64)]+[(47,y) for y in range(64)]);seen=set()
 while q:
  x,y=q.popleft()
  if (x,y) in seen:continue
  c=p[x,y][:3]
  if sum((c[i]-corner[i])**2 for i in range(3))**.5>24:continue
  seen.add((x,y));p[x,y]=BG
  for z in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=z[0]<48 and 0<=z[1]<64:q.append(z)
 im.save(C/f'#{n}.tga',format='TGA')
print('Restored complete pale garments with narrow corner-only background replacement.')