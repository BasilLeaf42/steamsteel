from pathlib import Path
from PIL import Image
from collections import deque
import io,json,shutil
R=Path(__file__).resolve().parents[1];B=R/'data/unit_models/_Units/bnw/textures';C=R/'data/ui/units/moors';M=R/'tools/card_generation_sources/morocco_20260915';A=R/'tools/card_source_archive/morocco_before_standardization';A.mkdir(parents=True,exist_ok=True)
for p in C.glob('*.tga'):
 q=A/p.name
 if not q.exists():shutil.copy2(p,q)
# Compatible bearer body; separate flag atlas is plain red before the 1915 pentagram decree.
(B/'mor_standard_bearer.texture').write_bytes((R/'data/unit_models/_Units/ott/textures/ott_inf_1g.texture').read_bytes())
raw=(B/'ott_standard_flag.texture').read_bytes();im=Image.open(io.BytesIO(raw[48:])).convert('RGBA');im.paste((174,20,32,255),(0,0,im.width,im.height));o=io.BytesIO();im.save(o,format='DDS',pixel_format='DXT5');(B/'mor_standard_flag.texture').write_bytes(raw[:48]+o.getvalue());(B/'mor_standard_flag_n.texture').write_bytes((B/'ott_standard_flag_n.texture').read_bytes())
BG=(184,173,143,255)
def flat(im):
 im=im.convert('RGBA').resize((48,64),Image.Resampling.LANCZOS);p=im.load();q=deque([(x,0) for x in range(48)]+[(x,63) for x in range(48)]+[(0,y) for y in range(64)]+[(47,y) for y in range(64)]);seen=set()
 while q:
  x,y=q.popleft()
  if (x,y) in seen:continue
  r,g,b,a=p[x,y];neutral=a<170 or (r>125 and g>105 and b>65 and abs(r-g)<65 and g-b<90 and r>=g-15)
  if not neutral:continue
  seen.add((x,y));p[x,y]=BG
  for z in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=z[0]<48 and 0<=z[1]<64:q.append(z)
 return im
def save(im,n):flat(im).save(C/f'#{n}.tga',format='TGA')
def donor(src,names):
 im=Image.open(C/f'#{src}.tga')
 for n in names:save(im,n)
donor('d_fra_for_cav',['mor_askar_early','mor_askar_mid','mor_askar_high']);donor('skif_inf',['mor_makhzen_early','mor_makhzen_mid','mor_makhzen_high']);donor('black_guard',['mor_abid_early','mor_abid_mid']);donor('skif_inf1',['mor_rif_early','mor_rif_mid','mor_rif_high']);donor('african_warband',['mor_tribal_levy']);donor('moroccan_camel_gunner_moors',['mor_hajjana'])
gens=['mor_guich_cavalry','mor_general_staff','mor_makhzen_cav_early','mor_makhzen_cav_mid','mor_makhzen_cav_high']
for n in gens:save(Image.open(M/f'{n}_master.png').crop((4,8,1084,1448)),n)
reg=R/'tools/historical_card_sources.json';data=json.loads(reg.read_text(encoding='utf-8'));data=[x for x in data if x.get('id') not in gens]
weapons={'mor_guich_cavalry':'Western military lance and sabre','mor_general_staff':'no weapon held; Lefaucheux Model 1858 holstered','mor_makhzen_cav_early':'percussion cavalry musketoon','mor_makhzen_cav_mid':'Snider-Enfield cavalry carbine','mor_makhzen_cav_high':'Turkish Mauser Model 1890 cavalry carbine'}
for n in gens:data.append(dict(id=n,unit_type=n,card_file=f'data/ui/units/moors/#{n}.tga',faction='moors',name=n,role='mounted general and staff' if n=='mor_general_staff' else ('mounted lancer' if 'guich' in n else 'mounted carbine cavalry'),weapon=weapons[n],source_url='https://www.heritage-print.com/war-morocco-arab-moorish-cavalry-1844-20369303.html',source_file='tools/historical_card_refs/moroccan_cavalry_1844.webp',source_title='War in Morocco: Arab and Moorish cavalry, 1844',creator='Illustrated London News artist, 1844',source_date='1844',licence='Historical reference reproduction',depicted_subject='Moroccan cavalry in the Franco-Moroccan War',pose_source_id='',mapping_note='Contemporary Moroccan cavalry reference controls mounted relationship, dress and tack; exact role equipment and passive command rule applied.',status='card-approved',generated_file=f'tools/card_generation_sources/morocco_20260915/{n}_master.png',crop_box=[4,8,1084,1448]))
reg.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Built Moroccan bearer textures and installed 18 cards.')