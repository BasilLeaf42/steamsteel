from pathlib import Path
from collections import Counter, deque
import json, math, shutil
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
BACKUP=ROOT/'tools/backup_before_remaining_mercenary_standardization_20260922/cards/mercs'
OUT=ROOT/'tools/remaining_mercenary_cards_safe_preview'
CANON=(184,173,143,255)
AUDIT=json.loads((ROOT/'tools/remaining_mercenary_audit.json').read_text(encoding='utf-8'))
TYPES=[r['type'] for r in AUDIT['units'] if r['category']!='ship']
DONORS={
 'merc_ap_front_cav':'data/ui/units/portugala/#us_scout_cav.tga','merc_apache_inf':'data/ui/units/portugala/#apache_inf.tga',
 'merc_port_inf':'tools/backup_before_remaining_mercenary_standardization_20260922/cards/mercs/#merc_port_inf_early.tga',
 'merc_port_lancer':'tools/backup_before_remaining_mercenary_standardization_20260922/cards/mercs/#merc_port_cav_early.tga',
 'merc_bhutan_warrior':'data/ui/units/bulga/#ind_bhutan_warrior.tga','merc_burmese_inf':'data/ui/units/cru/#burmese_inf.tga',
 'merc_indian_fanatic':'data/ui/units/bulga/#indian_fanatic.tga','merc_mongol_bows':'data/ui/units/byzantium/#mongol_bows.tga',
 'merc_georgian_inf':'data/ui/units/russia/#georgian_inf.tga','merc_kashgar_inf':'data/ui/units/cuman/#kashgar_inf.tga',
 'merc_rus_georgian_cav':'data/ui/units/russia/#rus_georgian_cav.tga','merc_zulu_spearmen':'data/ui/units/lith/#zulu_spearmen.tga',
 'merc_sikh_warriors':'data/ui/units/bulga/#sikh_warriors.tga','merc_siam_agent':'data/ui/units/cru/#siam_agent.tga'}

def dist(a,b):return math.sqrt(sum((a[i]-b[i])**2 for i in range(3)))
def reference(im):
 p=im.load();w,h=im.size; samples=[]
 for x in range(w):samples.append(p[x,0])
 for y in range(h*3//4):samples.extend((p[0,y],p[w-1,y]))
 bins=Counter(tuple(c//10 for c in px[:3]) for px in samples if px[3]>=32)
 if not bins:return CANON
 key=bins.most_common(1)[0][0]; chosen=[px for px in samples if tuple(c//10 for c in px[:3])==key]
 return tuple(round(sum(px[i] for px in chosen)/len(chosen)) for i in range(4))
def safe_normalize(im):
 im=im.convert('RGBA');p=im.load();w,h=im.size;ref=reference(im);q=deque();seen=set()
 def seed(x,y):return p[x,y][3]<32 or dist(p[x,y],ref)<=24
 for x in range(w):
  if seed(x,0):q.append((x,0))
 for y in range(h*3//4):
  for x in (0,w-1):
   if seed(x,y):q.append((x,y))
 while q:
  x,y=q.popleft()
  if (x,y) in seen:continue
  seen.add((x,y));cur=p[x,y]
  for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if not(0<=nx<w and 0<=ny<h) or (nx,ny) in seen:continue
   nxt=p[nx,ny]
   if nxt[3]<32 or (dist(nxt,ref)<=70 and dist(nxt,cur)<=16):q.append((nx,ny))
 out=im.copy();op=out.load()
 for x,y in seen:op[x,y]=CANON
 return out,len(seen)

OUT.mkdir(parents=True,exist_ok=True); report=[]
for unit in TYPES:
 src=ROOT/DONORS[unit] if unit in DONORS else BACKUP/f'#{unit}.tga'
 if not src.is_file():raise SystemExit(f'missing {src}')
 with Image.open(src) as im: out,n=safe_normalize(im)
 out.save(OUT/f'#{unit}.tga',format='TGA',bits=32,compression='tga_rle');report.append((unit,n,str(src.relative_to(ROOT))))

cols=8;cw,ch=150,96;rows=(len(TYPES)+cols-1)//cols
sheet=Image.new('RGB',(cols*cw,rows*ch),(38,35,30));d=ImageDraw.Draw(sheet);font=ImageFont.load_default()
for i,u in enumerate(TYPES):
 x=(i%cols)*cw;y=(i//cols)*ch
 with Image.open(OUT/f'#{u}.tga') as im:sheet.paste(im.convert('RGB'),(x+4,y+4))
 d.text((x+56,y+5),u.replace('merc_','')[:22],fill='white',font=font)
sheet.save(ROOT/'tools/remaining_mercenary_cards_safe_preview.png')
(ROOT/'tools/remaining_mercenary_cards_safe_preview.json').write_text(json.dumps([{'type':u,'replaced':n,'source':s} for u,n,s in report],indent=2)+'\n')
print(f'Prepared {len(TYPES)} safe previews without changing installed cards.')
