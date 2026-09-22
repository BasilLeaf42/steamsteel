from PIL import Image, ImageDraw
from pathlib import Path
import json, shutil, math
R=Path.cwd(); d=R/'data/ui/units/cru'; bg=(184,173,143,255)
archive=R/'tools/card_source_archive/siam_before_balance_20260917'; archive.mkdir(parents=True,exist_ok=True)
core=['siam_ele_gunner','fra_vietna','siam_sea','siam_late_inf','siam_late_cav','siam_agent','siam_inf','Siam_bodyguard','Siam_Archers','burmese_inf']
for n in core:
 p=d/f'#{n}.tga'; q=archive/p.name
 if p.exists() and not q.exists(): shutil.copy2(p,q)
(archive/'original_members.json').write_text(json.dumps({'faction':'cru','members':core},indent=2),encoding='utf-8')
def norm(im):
 im=im.convert('RGBA'); px=im.load(); w,h=im.size
 if min(a for *_,a in im.getdata())<255:
  base=Image.new('RGBA',im.size,bg); base.alpha_composite(im); return base
 src=im.copy(); seen=set(); stack=[]
 for x in range(w): stack += [(x,0),(x,h-1)]
 for y in range(h): stack += [(0,y),(w-1,y)]
 def candidate(c): return max(c[:3])-min(c[:3])<=65 and 95<=sum(c[:3])/3<=235
 while stack:
  x,y=stack.pop()
  if (x,y) in seen or not candidate(px[x,y]): continue
  seen.add((x,y)); c=px[x,y]
  for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
   if 0<=nx<w and 0<=ny<h and (nx,ny) not in seen:
    q=px[nx,ny]
    if candidate(q) and sum((q[i]-c[i])**2 for i in range(3))**0.5<=20: stack.append((nx,ny))
 out=src.copy(); op=out.load()
 for xy in seen: op[xy]=bg
 return out
def fit_master(p):
 im=Image.open(p).convert('RGBA'); a=im.getchannel('A'); box=a.getbbox() or (0,0,*im.size); im=im.crop(box)
 # crop to 3:4, preserving head/torso
 w,h=im.size; target=.75
 if w/h>target:
  nw=int(h*target); left=max(0,(w-nw)//2); im=im.crop((left,0,left+nw,h))
 else:
  nh=int(w/target); im=im.crop((0,0,w,min(h,nh)))
 im.thumbnail((48,64),Image.Resampling.LANCZOS)
 out=Image.new('RGBA',(48,64),bg); out.alpha_composite(im,((48-im.width)//2,max(0,64-im.height))); return out
for n in core:
 src=archive/f'#{n}.tga'
 if src.exists(): norm(Image.open(src)).resize((48,64),Image.Resampling.LANCZOS).save(d/f'#{n}.tga')
# The preserved elephant card has an opaque pure-black legacy backdrop; remove only the border-connected near-black field.
ep=d/'#siam_ele_gunner.tga'; im=Image.open(ep).convert('RGBA'); px=im.load(); seen=set(); stack=[(x,0) for x in range(48)]+[(x,63) for x in range(48)]+[(0,y) for y in range(64)]+[(47,y) for y in range(64)]
while stack:
 x,y=stack.pop()
 if (x,y) in seen or max(px[x,y][:3])>18: continue
 seen.add((x,y)); px[x,y]=bg
 for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
  if 0<=nx<48 and 0<=ny<64 and (nx,ny) not in seen: stack.append((nx,ny))
im.save(ep)
masters={'Siam_bodyguard':R/'tools/card_generation_sources/siam_general_staff_20260917.png','siam_late_cav':R/'tools/card_generation_sources/siam_carbine_cavalry_20260917.png'}
for n,p in masters.items(): fit_master(p).save(d/f'#{n}.tga')
for old,new in [('byz_armstrong','siam_armstrong'),('byz_12lb','siam_12lb'),('byz_5lb','siam_5lb'),('byz_maxim','siam_maxim')]:
 src=d/f'#{old}.tga'; norm(Image.open(src)).resize((48,64),Image.Resampling.LANCZOS).save(d/f'#{new}.tga')
# source registry
rp=R/'tools/historical_card_sources.json'; reg=json.loads(rp.read_text(encoding='utf-8-sig')) if rp.exists() else {}
if isinstance(reg,list):
 entries=reg
else:
 entries=reg.setdefault('entries',[])
entries=[e for e in entries if e.get('unit') not in ('Siam_bodyguard','siam_late_cav')]
entries += [
 {'unit':'Siam_bodyguard','faction':'Siam','role':'general and staff','source_url':'https://commons.wikimedia.org/wiki/File:King_Chulalongkorn.jpg','attribution':'Historical portrait of King Chulalongkorn in full dress uniform','date':'late 19th century','license':'public domain','depicted_subject':'King Chulalongkorn in Siamese command uniform','local_reference':'tools/historical_card_refs/king_chulalongkorn_uniform.jpg','generated_master':'tools/card_generation_sources/siam_general_staff_20260917.png','approximation':'Mounted passive command composition; uniform and command paraphernalia follow the national reference.','approved':True,'status':'card-approved'},
 {'unit':'siam_late_cav','faction':'Siam','role':'carbine cavalry','source_url':'https://commons.wikimedia.org/wiki/File:Bangkok_-_mounted_Siamese_cavalryman;_palace_in_background_LCCN2004707846.jpg','attribution':'William Henry Jackson / Library of Congress','date':'1895','license':'no known restrictions on publication','depicted_subject':'Mounted Siamese cavalryman in Bangkok','local_reference':'tools/historical_card_refs/siam_cavalryman_1895.jpg','generated_master':'tools/card_generation_sources/siam_carbine_cavalry_20260917.png','approximation':'Period mounted pose adapted to the loaded dark-blue uniform and visible Snider-Enfield carbine.','approved':True,'status':'card-approved'}]
if isinstance(reg,list): reg=entries
else: reg['entries']=entries
rp.write_text(json.dumps(reg,indent=2,ensure_ascii=False),encoding='utf-8')
# contact sheet at 8x scale
names=core+['siam_armstrong','siam_12lb','siam_5lb','siam_maxim']; scale=8; sheet=Image.new('RGBA',(len(names)*48*scale,64*scale+28),(45,40,32,255))
for i,n in enumerate(names):
 im=Image.open(d/f'#{n}.tga').convert('RGBA').resize((48*scale,64*scale),Image.Resampling.NEAREST); sheet.alpha_composite(im,(i*48*scale,0))
ImageDraw.Draw(sheet).text((4,64*scale+5),' | '.join(names),fill='white')
sheet.save(R/'tools/siam_cards_postbalance.png')
print('Installed Siam cards and contact sheet.')
