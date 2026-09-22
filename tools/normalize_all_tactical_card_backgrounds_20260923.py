from pathlib import Path
from collections import deque
from PIL import Image
import hashlib, json, shutil

ROOT=Path(__file__).resolve().parents[1]
CARD_ROOT=ROOT/'data/ui/units'
ARCHIVE=ROOT/'tools/card_source_archive/all_cards_before_systemic_background_20260923'
CAN=(184,173,143,255)

edu=(ROOT/'data/tow_steamsteel/export_descr_unit.txt').read_text(encoding='utf-8',errors='replace')
SHIP_KEYS=set()
import re
for block in re.split(r'(?=^type\s+)',edu,flags=re.M):
    if re.search(r'^category\s+ship\s*$',block,re.M):
        m=re.search(r'^dictionary\s+([^\s;]+)',block,re.M)
        if m: SHIP_KEYS.add(m.group(1).lower())

def dist(a,b):
    return sum((a[i]-b[i])**2 for i in range(3))**0.5

def strict_border_mask(im):
    """Border-seeded, edge-continuity mask. It never classifies by beige/skin range."""
    w,h=im.size; px=im.load(); seen=set(); q=deque()
    # Top corners are the most reliable background anchors on close-cropped cards.
    seeds=[(0,0),(w-1,0)]
    # Bottom corners are accepted only when locally continuous with their edge.
    for p,n in [((0,h-1),(0,h-2)),((w-1,h-1),(w-1,h-2))]:
        if dist(px[p[0],p[1]],px[n[0],n[1]])<=10: seeds.append(p)
    for seed in seeds:
        q.append((seed[0],seed[1],px[seed[0],seed[1]]))
    while q:
        x,y,parent=q.popleft()
        if (x,y) in seen: continue
        cur=px[x,y]
        if cur[3]<255 or dist(cur,parent)>10: continue
        seen.add((x,y))
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=nx<w and 0<=ny<h and (nx,ny) not in seen:
                q.append((nx,ny,cur))
    return seen

def normalize(im):
    im=im.convert('RGBA')
    original=list(im.getdata())
    method='strict_border'; alpha_count=0
    if any(p[3]<255 for p in original):
        out=Image.new('RGBA',im.size,CAN); out.alpha_composite(im)
        alpha_count=sum(p[3]<255 for p in original)
        im=out
        method='alpha_then_strict_border'
    mask=strict_border_mask(im)
    out=im.copy(); op=out.load()
    for x,y in mask: op[x,y]=CAN
    # Hard protected-foreground gate.
    before_mask=list(im.getdata()); after=list(out.getdata()); w=im.width
    for i,(before,now) in enumerate(zip(before_mask,after)):
        if (i%w,i//w) not in mask and before!=now:
            raise RuntimeError('protected foreground changed')
    return out,method,len(mask)+alpha_count,len(original)-len(mask)

def install_exact(source,target):
    with Image.open(source) as im:
        if im.size!=(48,64): raise RuntimeError(f'bad donor size {source}: {im.size}')
        target.parent.mkdir(parents=True,exist_ok=True)
        payload=im.convert('RGBA').copy()
    temp=target.with_name(target.name+'.tmp.tga')
    payload.save(temp,format='TGA',bits=32,compression='tga_rle')
    temp.replace(target)

# Exact visual donors: the Thai card uses the identical siam_sea soldier, and
# Beiyang uses the selected SOE National Revolutionary Army model/card.
thai= CARD_ROOT/'byzantium/#siam_sea_byzantium.tga'
for target in CARD_ROOT.glob('*/#siam_sea.tga'): install_exact(thai,target)
soe=ROOT.parent/'soe/data/ui/units/byzantium/#Hand_Gunners.tga'
install_exact(soe,CARD_ROOT/'byzantium/#qing_beiyang_infantry.tga')

report=[]; ARCHIVE.mkdir(parents=True,exist_ok=True)
for p in sorted(CARD_ROOT.glob('*/#*.tga')):
    if p.stem[1:].lower() in SHIP_KEYS:
        report.append({'path':str(p.relative_to(ROOT)),'status':'ship_excluded'}); continue
    try:
        with Image.open(p) as src: im=src.convert('RGBA')
    except Exception as exc:
        report.append({'path':str(p.relative_to(ROOT)),'status':'unreadable','error':str(exc)}); continue
    if im.size==(48,62):
        repaired=Image.new('RGBA',(48,64),CAN); repaired.alpha_composite(im,(0,0)); im=repaired
    elif im.size!=(48,64):
        report.append({'path':str(p.relative_to(ROOT)),'status':'other_size','size':list(im.size)}); continue
    out,method,count,protected=normalize(im)
    if out.tobytes()==im.tobytes() and im.mode=='RGBA':
        report.append({'path':str(p.relative_to(ROOT)),'status':'unchanged','method':method}); continue
    rel=p.relative_to(CARD_ROOT); backup=ARCHIVE/rel
    backup.parent.mkdir(parents=True,exist_ok=True)
    if not backup.exists(): shutil.copy2(p,backup)
    temp=p.with_name(p.name+'.tmp.tga')
    out.save(temp,format='TGA',bits=32,compression='tga_rle')
    temp.replace(p)
    report.append({'path':str(p.relative_to(ROOT)),'status':'normalized','method':method,
                   'background_pixels':count,'protected_pixels':protected})

summary={'cards':len(report),'normalized':sum(r['status']=='normalized' for r in report),
         'alpha_composited':sum(r.get('method')=='alpha_then_strict_border' and r['status']=='normalized' for r in report),
         'strict_border':sum(r.get('method')=='strict_border' and r['status']=='normalized' for r in report),
         'unreadable':sum(r['status']=='unreadable' for r in report),
         'other_size':sum(r['status']=='other_size' for r in report)}
(ROOT/'tools/all_tactical_card_background_normalization_20260923.json').write_text(
    json.dumps({'summary':summary,'cards':report},indent=2)+'\n')
print(json.dumps(summary))
