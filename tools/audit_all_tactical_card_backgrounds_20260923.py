from pathlib import Path
from collections import Counter
from PIL import Image
import json

ROOT=Path(__file__).resolve().parents[1]
CAN=(184,173,143,255)
rows=[]
for p in sorted((ROOT/'data/ui/units').glob('*/*.tga')):
    try: im=Image.open(p).convert('RGBA')
    except Exception: continue
    if im.size!=(48,64): continue
    px=list(im.getdata())
    border=[im.getpixel((x,y)) for x in range(48) for y in range(64) if x in (0,47) or y in (0,63)]
    transparent=sum(1 for q in px if q[3]<255)
    canonical=sum(1 for q in border if q==CAN)
    foreign=[q for q in border if q[3]>=250 and q[:3] != CAN[:3]]
    rows.append({'path':str(p.relative_to(ROOT)),'transparent':transparent,
                 'canonical_border':canonical,'border_total':len(border),
                 'foreign_border':len(foreign),
                 'dominant_border':Counter(border).most_common(1)[0]})
out={'cards':len(rows),'transparent':sum(r['transparent']>0 for r in rows),
     'foreign_border':sum(r['foreign_border']>0 for r in rows),'rows':rows}
(ROOT/'tools/all_tactical_card_background_audit_20260923.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
