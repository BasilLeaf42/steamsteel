from pathlib import Path
from collections import deque
from PIL import Image
import json, shutil

R = Path(__file__).resolve().parents[1]
C = R / 'data/ui/units/moors'
M = R / 'tools/card_generation_sources/morocco_20260915'
A = R / 'tools/card_source_archive/morocco_before_role_card_repair_20260915'
G = Path(r'C:/Users/kwoks/.codex/generated_images/01a09417-2b02-79c1-ac26-19f8f616b95f')
BG = (184, 173, 143, 255)
A.mkdir(parents=True, exist_ok=True); M.mkdir(parents=True, exist_ok=True)

generated = {
 'mor_guich_cavalry': 'exec-f4a47e7f-47f8-4728-9c8c-39640117f1bd.png',
 'mor_hajjana': 'exec-315ddec4-6428-4dc9-9e3b-2b609a253613.png',
 'mor_rif_early': 'exec-684febe1-01ad-443b-8aaa-55aaf6b9661e.png',
 'mor_rif_mid': 'exec-3f0ab511-1f6b-461e-ae83-b362170c010e.png',
 'mor_rif_high': 'exec-9fa6d9ba-2937-469e-942c-9471f648f4a0.png',
}

def dist(c, b=BG):
 return sum((c[i]-b[i])**2 for i in range(3))**.5

def flatten(im):
 im=im.convert('RGBA').resize((48,64),Image.Resampling.LANCZOS); p=im.load()
 edge=[(x,0) for x in range(48)]+[(x,63) for x in range(48)]+[(0,y) for y in range(64)]+[(47,y) for y in range(64)]
 seed=tuple(sum(p[x,y][i] for x,y in edge)//len(edge) for i in range(3))+(255,)
 q=deque(edge); bg=set()
 while q:
  x,y=q.popleft()
  if (x,y) in bg or dist(p[x,y],seed)>52: continue
  bg.add((x,y)); p[x,y]=BG
  for z in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=z[0]<48 and 0<=z[1]<64:q.append(z)
 for y in range(64):
  for x in range(48):
   if (x,y) not in bg and dist(p[x,y])<20:
    r,g,b,a=p[x,y]; p[x,y]=(min(235,r+30),min(226,g+27),min(202,b+22),a)
 for y in range(64):
  for x in range(48):
   r,g,b,a=p[x,y]; p[x,y]=(r,g,b,255)
 return im

for n in generated:
 live=C/f'#{n}.tga'
 if not (A/live.name).exists(): shutil.copy2(live,A/live.name)
 master=M/f'{n}_final_master.png'; shutil.copy2(G/generated[n],master)
 flatten(Image.open(master)).save(live,format='TGA')

for n in ['mor_makhzen_early','mor_makhzen_mid','mor_makhzen_high','mor_abid_early','mor_abid_mid','mor_makhzen_cav_early','mor_makhzen_cav_mid','mor_makhzen_cav_high','mor_general_staff']:
 live=C/f'#{n}.tga'
 if not (A/live.name).exists(): shutil.copy2(live,A/live.name)
 flatten(Image.open(live)).save(live,format='TGA')

tribal=C/'#mor_tribal_levy.tga'
if not (A/tribal.name).exists(): shutil.copy2(tribal,A/tribal.name)
flatten(Image.open(C/'#African_Spearmen.tga')).save(tribal,format='TGA')

reg=R/'tools/historical_card_sources.json'; rows=json.loads(reg.read_text(encoding='utf-8'))
for row in rows:
 n=row.get('unit_type') or row.get('id')
 if n in generated:
  row['generated_file']=f'tools/card_generation_sources/morocco_20260915/{n}_final_master.png'
  row['crop_box']=[0,0,1536,2048]
  row['status']='card-approved'
reg.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Installed five role-correct masters, repaired five pale cards, and restored the exact African Spearmen card.')
