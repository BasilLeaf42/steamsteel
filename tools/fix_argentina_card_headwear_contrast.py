from pathlib import Path
from PIL import Image
import shutil
R=Path(__file__).resolve().parents[1]; C=R/'data/ui/units/aztecs'; A=R/'tools/card_source_archive/argentina_before_headwear_contrast_20260915';A.mkdir(parents=True,exist_ok=True)
names=['arg_line_early','arg_line_mid','arg_line_high','arg_national_guard_early','arg_national_guard_mid','arg_national_guard_high']
BG=(184,173,143,255); SH=(139,127,103,255)
for n in names:
 p=C/f'#{n}.tga'; q=A/p.name
 if not q.exists():shutil.copy2(p,q)
 im=Image.open(p).convert('RGBA'); px=im.load(); subject=set()
 for y in range(1,31):
  for x in range(1,47):
   r,g,b,a=px[x,y]
   if a>180 and sum(abs(px[x,y][i]-BG[i]) for i in range(3))>42:subject.add((x,y))
 shadow=set()
 for x,y in subject:
  for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)):
   z=(x+dx,y+dy)
   if 1<=z[0]<47 and 1<=z[1]<31 and z not in subject and sum(abs(px[z[0],z[1]][i]-BG[i]) for i in range(3))<35:shadow.add(z)
 for z in shadow:px[z[0],z[1]]=SH
 im.save(p,format='TGA')
print('Added a restrained one-pixel headwear silhouette to six Argentine line/Guard cards; originals archived.')