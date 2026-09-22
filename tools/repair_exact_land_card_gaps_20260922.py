from pathlib import Path
import re, json, shutil
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
edu=(ROOT/'data/tow_steamsteel/export_descr_unit.txt').read_text(encoding='utf-8',errors='replace').replace('\r','')
factions={'portugala','milan','scotland','denmark','poland','aztecs','england','france','hre','spain','portugal','sicily','normans','mongols','venice','russia','hungary','moors','teu','lith','turks','golden','egypt','timurids','cuman','bulga','cru','byzantium','papal_states','saxons'}
rows=[]
for b in re.split(r'(?=^type\s+)',edu,flags=re.M):
    tm=re.search(r'^type\s+(.+?)\s*$',b,re.M); sm=re.search(r'^soldier\s+([^,]+)',b,re.M); cm=re.search(r'^category\s+(\S+)',b,re.M)
    if not(tm and sm and cm) or cm.group(1) in {'ship','siege'}: continue
    owners=set()
    for m in re.finditer(r'^(?:ownership|era [012])\s+(.+)$',b,re.M): owners.update(x.strip() for x in m.group(1).split(',') if x.strip() in factions)
    dm=re.search(r'^dictionary\s+([^\s;]+)',b,re.M)
    rows.append({'type':tm.group(1).strip(),'dict':dm.group(1) if dm else tm.group(1).strip(),'soldier':sm.group(1).strip(),'mount':(re.search(r'^mount\s+(\S+)',b,re.M)or['','foot'])[1],'owners':owners})

copied=[]; converted=[]; missing=[]; bad=[]
for r in rows:
    for faction in sorted(r['owners']):
        dest=ROOT/'data/ui/units'/faction/f"#{r['dict']}.tga"
        if not dest.exists():
            donor=next((ROOT/'data/ui/units'/folder/f"#{r['dict']}.tga" for folder in ('mercs','slave') if (ROOT/'data/ui/units'/folder/f"#{r['dict']}.tga").exists()),None)
            for d in rows:
                if donor: break
                if d is r or d['soldier']!=r['soldier'] or d['mount']!=r['mount'] or faction not in d['owners']: continue
                p=ROOT/'data/ui/units'/faction/f"#{d['dict']}.tga"
                if p.exists(): donor=p;break
            if donor:
                dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(donor,dest);copied.append({'to':str(dest.relative_to(ROOT)),'from':str(donor.relative_to(ROOT))})
            else: missing.append(str(dest.relative_to(ROOT)));continue
        with Image.open(dest) as im:
            if im.size!=(48,64): bad.append({'path':str(dest.relative_to(ROOT)),'size':im.size});continue
            if im.mode!='RGBA':
                rgba=im.convert('RGBA');rgba.save(dest,format='TGA',bits=32,compression='tga_rle');converted.append(str(dest.relative_to(ROOT)))

report={'copied':copied,'converted':converted,'missing':sorted(set(missing)),'bad_dimensions':bad}
(ROOT/'tools/exact_land_card_gap_report_20260922.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:len(v) for k,v in report.items()}))
