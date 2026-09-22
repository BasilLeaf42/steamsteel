from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import re, json, shutil

ROOT=Path(__file__).resolve().parents[1]
UI=ROOT/'data/ui/units'
OUT=ROOT/'tools/all_small_unit_cards_20260923'
ARCH=ROOT/'tools/card_source_archive/missing_faction_combinations_20260923'
OUT.mkdir(parents=True,exist_ok=True); ARCH.mkdir(parents=True,exist_ok=True)
FACTIONS=['portugala','milan','scotland','denmark','poland','aztecs','england','france','hre','spain','portugal','sicily','normans','mongols','venice','russia','hungary','moors','teu','lith','turks','golden','egypt','timurids','cuman','bulga','cru','byzantium','papal_states','saxons']
NAMES={'portugala':'Union','milan':'Confederates','scotland':'Mexico','denmark':'Peru','poland':'Brazil','aztecs':'Argentina','england':'Britain','france':'France','hre':'Prussia','spain':'Spain','portugal':'Netherlands','sicily':'Denmark','normans':'Sweden–Norway','mongols':'Greece','venice':'Italy','russia':'Russia','hungary':'Austria–Hungary','moors':'Morocco','teu':'Boers','lith':'Zulu','turks':'Ottoman Empire','golden':'Oman','egypt':'Qajar Persia','timurids':'Afghanistan','cuman':'Turkestan','bulga':'Indian Princely States','cru':'Siam','byzantium':'Qing','papal_states':'Ethiopia','saxons':'Japan'}

def read(path):
    b=path.read_bytes()
    if b[:2]==b'\xff\xfe': return b[2:].decode('utf-16le',errors='replace')
    return b.decode('utf-8-sig',errors='replace')

loc={m.group(1):m.group(2).strip() for m in re.finditer(r'^\{([^}\r\n]+)\}([^\r\n]*)',read(ROOT/'data/text/export_units.txt'),re.M)}
edu=read(ROOT/'data/tow_steamsteel/export_descr_unit.txt').replace('\r','')
units=[]
for block in re.split(r'(?=^type\s+)',edu,flags=re.M):
    tm=re.search(r'^type\s+(.+?)\s*$',block,re.M); dm=re.search(r'^dictionary\s+([^\s;]+)',block,re.M)
    if not (tm and dm): continue
    owners=set()
    for m in re.finditer(r'^(?:ownership|era [012])\s+(.+)$',block,re.M):
        owners.update(x.strip() for x in m.group(1).split(',') if x.strip() in FACTIONS)
    units.append({'type':tm.group(1).strip(),'key':dm.group(1),'owners':owners,
                  'category':(re.search(r'^category\s+(\S+)',block,re.M)or['',''])[1],
                  'name':loc.get(dm.group(1),dm.group(1).replace('_',' '))})

# Exact dictionary-key donors are the same card, not merely similar artwork.
by_key={}
for p in UI.glob('*/#*.tga'): by_key.setdefault(p.stem[1:].lower(),[]).append(p)
copied=[]; missing=[]
for u in units:
    for faction in sorted(u['owners']):
        target=UI/faction/f"#{u['key']}.tga"
        if target.exists(): continue
        donors=by_key.get(u['key'].lower(),[])
        donor=next((p for p in donors if p.parent.name in ('mercs','slave')),donors[0] if donors else None)
        if donor:
            target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(donor,target)
            copied.append({'target':str(target.relative_to(ROOT)),'donor':str(donor.relative_to(ROOT))})
            by_key.setdefault(u['key'].lower(),[]).append(target)
        else: missing.append({'faction':faction,'type':u['type'],'key':u['key'],'category':u['category']})

def label_lines(text,n=23):
    words=text.split(); lines=[]; cur=''
    for w in words:
        if len(cur)+len(w)+1<=n: cur=(cur+' '+w).strip()
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines[:3]

def render(title,entries,path,cols=8):
    entries=sorted(entries,key=lambda x:(x['name'].casefold(),x['key'].casefold()))
    cw,ch=190,166; head=48; rows=max(1,(len(entries)+cols-1)//cols)
    sheet=Image.new('RGB',(cols*cw,head+rows*ch),(48,44,37)); d=ImageDraw.Draw(sheet); font=ImageFont.load_default()
    d.text((12,10),f'{title} — {len(entries)} tactical cards',fill=(255,245,220),font=font)
    for i,e in enumerate(entries):
        x=(i%cols)*cw; y=head+(i//cols)*ch; p=e['path']
        try:
            im=Image.open(p).convert('RGBA')
            if im.size==(48,64): im=im.resize((96,128),Image.Resampling.NEAREST)
            else: im.thumbnail((96,128),Image.Resampling.NEAREST)
            canvas=Image.new('RGBA',(96,128),(184,173,143,255)); canvas.alpha_composite(im,(0,0))
            sheet.paste(canvas.convert('RGB'),(x+4,y+4))
        except Exception:
            d.rectangle((x+4,y+4,x+99,y+131),outline='red')
        for j,line in enumerate(label_lines(e['name'])): d.text((x+104,y+6+j*12),line,fill='white',font=font)
        d.text((x+104,y+46),e['key'][:24],fill=(190,185,174),font=font)
        d.text((x+104,y+59),e.get('category','')[:18],fill=(160,190,205),font=font)
    sheet.save(path)

pages=[]
for faction in FACTIONS:
    seen=set(); entries=[]
    for u in units:
        if faction not in u['owners'] or u['key'].lower() in seen: continue
        seen.add(u['key'].lower()); p=UI/faction/f"#{u['key']}.tga"
        if p.exists(): entries.append({**u,'path':p})
    path=OUT/f'{faction}.png'; render(NAMES[faction],entries,path)
    pages.append({'faction':faction,'title':NAMES[faction],'count':len(entries),'path':str(path.relative_to(ROOT))})

# Physical mercenary and rebel/slave catalogs deliberately remain separate.
for folder,title in [('mercs','Mercenaries'),('slave','Slave/Rebel')]:
    entries=[]
    for p in sorted((UI/folder).glob('#*.tga')):
        key=p.stem[1:]; entries.append({'key':key,'name':loc.get(key,key.replace('_',' ')),'category':'catalog','path':p})
    path=OUT/f'{folder}.png'; render(title,entries,path,cols=10)
    pages.append({'faction':folder,'title':title,'count':len(entries),'path':str(path.relative_to(ROOT))})

report={'copied':copied,'missing':missing,'pages':pages}
(ROOT/'tools/complete_faction_card_atlas_report_20260923.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'copied':len(copied),'missing':len(missing),'pages':len(pages),'cards':sum(x['count'] for x in pages)}))
