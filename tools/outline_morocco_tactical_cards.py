from pathlib import Path
from PIL import Image
import shutil,math
R=Path(__file__).resolve().parents[1];C=R/'data/ui/units/moors';A=R/'tools/card_source_archive/morocco_before_silhouette_edges_20260915';A.mkdir(parents=True,exist_ok=True)
BG=(184,173,143,255); EDGE=(91,76,57,255)
names=['mor_askar_early','mor_askar_mid','mor_askar_high','mor_makhzen_early','mor_makhzen_mid','mor_makhzen_high','mor_abid_early','mor_abid_mid','mor_rif_early','mor_rif_mid','mor_rif_high','mor_makhzen_cav_early','mor_makhzen_cav_mid','mor_makhzen_cav_high','mor_tribal_levy','mor_guich_cavalry','mor_hajjana','mor_general_staff']
def dist(c):return sum((c[i]-BG[i])**2 for i in range(3))**.5
for n in names:
 p=C/f'#{n}.tga';q=A/p.name
 if not q.exists():shutil.copy2(p,q)
 im=Image.open(p).convert('RGBA');px=im.load();fg={(x,y) for y in range(1,63) for x in range(1,47) if px[x,y][3]>180 and dist(px[x,y])>32};outline=set()
 for x,y in fg:
  for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)):
   nx,ny=x+dx,y+dy
   if 1<=nx<47 and 1<=ny<63 and (nx,ny) not in fg and dist(px[nx,ny])<24:outline.add((nx,ny))
 for x,y in outline:px[x,y]=EDGE
 im.save(p,format='TGA')
print(f'Added non-destructive painted silhouette edges to {len(names)} Moroccan tactical cards.')