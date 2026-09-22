from PIL import Image
from pathlib import Path
from collections import deque
C=Path('data/ui/units/moors');BG=(184,173,143,255);names=['mor_guich_cavalry','mor_general_staff','mor_makhzen_cav_early','mor_makhzen_cav_mid','mor_makhzen_cav_high']
for n in names:
 p=C/f'#{n}.tga';im=Image.open(p).convert('RGBA');px=im.load();fg={(x,y) for y in range(64) for x in range(48) if sum(abs(px[x,y][i]-BG[i]) for i in range(3))>35 and px[x,y][3]>160};comps=[]
 while fg:
  seed=fg.pop();q=deque([seed]);co={seed}
  while q:
   x,y=q.popleft()
   for z in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
    if z in fg:fg.remove(z);co.add(z);q.append(z)
  comps.append(co)
 comps.sort(key=len,reverse=True);keep=set().union(*comps[:3]) if comps else set()
 # Retain nearby antialias pixels and erase isolated generated debris.
 near=set(keep)
 for x,y in list(keep):
  for dx in (-1,0,1):
   for dy in (-1,0,1):
    if 0<=x+dx<48 and 0<=y+dy<64:near.add((x+dx,y+dy))
 for y in range(64):
  for x in range(48):
   if (x,y) not in near:px[x,y]=BG
 im.save(p,format='TGA')
print('Cleaned five generated Moroccan mounted-card backgrounds.')