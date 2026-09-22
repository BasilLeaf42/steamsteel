from pathlib import Path
from collections import deque,Counter
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,shutil,math

R=Path(__file__).resolve().parents[1]
OLD=R/'tools/backup_before_remaining_mercenary_standardization_20260922/cards/mercs/#merc_arab_sailors.tga'
REF=R/'data/ui/units/hungary/#aus_landwehr_mid.tga'
OUT=R/'tools/khedival_lowpoly_trial_20260923'; OUT.mkdir(parents=True,exist_ok=True)
BACK=R/'tools/card_source_archive/khedival_before_background_repair_20260923';BACK.mkdir(parents=True,exist_ok=True)
CAN=(184,173,143,255)

def cd(a,b):return sum((a[i]-b[i])**2 for i in range(3))**0.5
def border_cutout(im):
    im=im.convert('RGBA'); w,h=im.size; px=im.load(); q=deque(); seen=set()
    corners=[(0,0),(w-1,0),(0,h-1),(w-1,h-1)]
    refs=[px[x,y] for x,y in corners]
    for x,y in corners:q.append((x,y,px[x,y]))
    while q:
        x,y,parent=q.popleft()
        if (x,y) in seen:continue
        cur=px[x,y]
        if cd(cur,parent)>9 or min(cd(cur,r) for r in refs)>55:continue
        seen.add((x,y))
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=nx<w and 0<=ny<h and (nx,ny) not in seen:q.append((nx,ny,cur))
    out=im.copy(); op=out.load()
    for x,y in seen:op[x,y]=CAN
    return out,seen

def quant(im,colors):
    return im.convert('RGB').quantize(colors=colors,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGBA')

old=Image.open(OLD).convert('RGBA'); repaired,mask=border_cutout(old)
repaired.save(OUT/'khedival_background_repaired.tga',format='TGA',bits=32,compression='tga_rle')

# Install only the conservative background repair; preserve all three originals.
installed=[]
for target in (R/'data/ui/units').glob('*/#merc_arab_sailors.tga'):
    backup=BACK/target.parent.name/target.name;backup.parent.mkdir(parents=True,exist_ok=True)
    if not backup.exists():shutil.copy2(target,backup)
    repaired.save(target,format='TGA',bits=32,compression='tga_rle');installed.append(str(target.relative_to(R)))

ref=Image.open(REF).convert('RGBA')
ref_fg=[p for p in ref.getdata() if p!=CAN]
src_fg=[p for p in repaired.getdata() if p!=CAN]
ref_unique=len(set(ref_fg)); src_unique=len(set(src_fg))
palette=max(24,min(64,round(ref_unique/max(1,len(ref_fg))*len(src_fg))))

v1=quant(repaired,palette)
# Restore the exact canonical background after any global palette operation.
for v in (v1,):
    vp=v.load()
    for x,y in mask:vp[x,y]=CAN

small=repaired.resize((32,43),Image.Resampling.BOX).resize((48,64),Image.Resampling.NEAREST)
v2=quant(small,palette)
v2p=v2.load()
for x,y in mask:v2p[x,y]=CAN

# A restrained line-art treatment: darken only strong local luminance edges.
base=quant(repaired,palette); gray=repaired.convert('L'); edges=gray.filter(ImageFilter.FIND_EDGES)
bp=base.load(); ep=edges.load()
for y in range(64):
    for x in range(48):
        if (x,y) in mask: bp[x,y]=CAN
        elif ep[x,y]>95:
            r,g,b,a=bp[x,y]; bp[x,y]=(max(0,int(r*.68)),max(0,int(g*.68)),max(0,int(b*.68)),a)
v3=base

variants=[('k.k. Landwehr reference',ref),('Khedival repaired',repaired),('Palette matched',v1),('Coarse low-poly',v2),('Palette + hard edges',v3)]
sheet=Image.new('RGB',(5*240,360),(42,38,32));d=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(variants):
    sheet.paste(im.resize((192,256),Image.Resampling.NEAREST).convert('RGB'),(i*240+20,20));d.text((i*240+20,286),name,fill='white')
    im.save(OUT/(name.lower().replace(' ','_').replace('+','plus')+'.png'))
sheet.save(OUT/'comparison.png')
report={'installed_background_repair':installed,'backup':str(BACK.relative_to(R)),'trial_installed':False,
        'reference_unique_foreground_colours':ref_unique,'source_unique_foreground_colours':src_unique,
        'trial_palette_colours':palette,'background_pixels_rebuilt':len(mask)}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
