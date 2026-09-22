from pathlib import Path
import re, json
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[1]; D=R/'data'
edu=(D/'tow_steamsteel/export_descr_unit.txt').read_text(encoding='utf-8',errors='replace').replace('\r','')
roster=[]
for b in re.split(r'(?=^type\s+)',edu,flags=re.M):
    t=re.search(r'^type\s+(.+?)\s*$',b,re.M); own=re.search(r'^ownership\s+(.+?)\s*$',b,re.M)
    if not t or not own or 'byzantium' not in own.group(1).split(', '): continue
    d=re.search(r'^dictionary\s+([^\s;]+)',b,re.M); s=re.search(r'^soldier\s+([^,]+),\s*(\d+)',b,re.M); eras=re.findall(r'^era ([012])\s+.*\bbyzantium\b',b,re.M)
    roster.append((t.group(1),d.group(1) if d else t.group(1),s.group(1).strip() if s else '',int(s.group(2)) if s else -1,''.join(eras)))
print('ROSTER')
for t,k,s,n,e in roster: print('|'.join(map(str,(t,s,n,e))))
cards=D/'ui/units/byzantium'; bg=(184,173,143); issues=[]; thumbs=[]
for t,k,s,n,e in roster:
    p=cards/f'#{k}.tga'
    if not p.exists(): issues.append((t,'missing')); continue
    src=Image.open(p)
    if src.size!=(48,64): issues.append((t,f'size={src.size}'))
    if src.mode!='RGBA': issues.append((t,f'mode={src.mode}'))
    im=src.convert('RGBA'); comp=Image.alpha_composite(Image.new('RGBA',(48,64),(*bg,255)),im)
    thumbs.append((t,comp.resize((144,192),Image.Resampling.NEAREST)))
print('CARD_ISSUES',json.dumps(issues))
w=4*220; h=((len(thumbs)+3)//4)*230; sheet=Image.new('RGB',(w,h),(80,72,60)); dr=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(thumbs):
    x=(i%4)*220;y=(i//4)*230;sheet.paste(im,(x,y));dr.text((x,y+194),t,fill='white')
out=R/'tools/qing_card_audit.png';sheet.save(out);print('SHEET',out)