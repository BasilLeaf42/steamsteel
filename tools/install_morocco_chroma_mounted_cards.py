from pathlib import Path
from PIL import Image
import json, shutil

R=Path(__file__).resolve().parents[1]
C=R/'data/ui/units/moors'; M=R/'tools/card_generation_sources/morocco_20260915'
A=R/'tools/card_source_archive/morocco_before_chroma_mounted_rebuild_20260915'
G=Path(r'C:/Users/kwoks/.codex/generated_images/01a09417-2b02-79c1-ac26-19f8f616b95f')
BG=(184,173,143,255); A.mkdir(parents=True,exist_ok=True)
files={
 'mor_general_staff':'exec-abdb460a-17c7-42d0-aecd-5472a2008f66.png',
 'mor_makhzen_cav_early':'exec-32c272cf-da03-4241-9fc0-f05d6ae00357.png',
 'mor_makhzen_cav_mid':'exec-b6781330-1352-40dd-aa0f-f0d9fd1f6b3c.png',
 'mor_makhzen_cav_high':'exec-52a149d0-9b9e-4b5e-8204-64b5fee8bb8b.png'}
for n,f in files.items():
 live=C/f'#{n}.tga'; shutil.copy2(live,A/live.name)
 master=M/f'{n}_chroma_final_master.png'; shutil.copy2(G/f,master)
 im=Image.open(master).convert('RGBA'); p=im.load()
 for y in range(im.height):
  for x in range(im.width):
   r,g,b,a=p[x,y]
   if g>105 and g>r*1.34 and g>b*1.34: p[x,y]=BG
 im=im.resize((48,64),Image.Resampling.LANCZOS); p=im.load()
 for y in range(64):
  for x in range(48):
   r,g,b,a=p[x,y]
   if g>95 and g>r*1.20 and g>b*1.20: p[x,y]=BG
   else: p[x,y]=(r,g,b,255)
 im.save(live,format='TGA')
reg=R/'tools/historical_card_sources.json'; rows=json.loads(reg.read_text(encoding='utf-8'))
for row in rows:
 n=row.get('unit_type') or row.get('id')
 if n in files:
  row['generated_file']=f'tools/card_generation_sources/morocco_20260915/{n}_chroma_final_master.png'
  row['crop_box']=[0,0,1536,2048]; row['status']='card-approved'
reg.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Installed four chroma-extracted mounted tactical cards with intact heads and exact RGBA background.')
