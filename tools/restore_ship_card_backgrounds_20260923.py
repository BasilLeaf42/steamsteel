from pathlib import Path
import re, shutil, json

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'tools/card_source_archive/all_cards_before_systemic_background_20260923'
CARDS=ROOT/'data/ui/units'
edu=(ROOT/'data/tow_steamsteel/export_descr_unit.txt').read_text(encoding='utf-8',errors='replace')
keys=set()
for block in re.split(r'(?=^type\s+)',edu,flags=re.M):
    if not re.search(r'^category\s+ship\s*$',block,re.M): continue
    m=re.search(r'^dictionary\s+([^\s;]+)',block,re.M)
    if m: keys.add(m.group(1).lower())
restored=[];missing=[]
for target in CARDS.glob('*/#*.tga'):
    if target.stem[1:].lower() not in keys: continue
    source=ARCHIVE/target.relative_to(CARDS)
    if source.exists():
        shutil.copy2(source,target); restored.append(str(target.relative_to(ROOT)))
    else: missing.append(str(target.relative_to(ROOT)))
(ROOT/'tools/ship_card_background_restore_20260923.json').write_text(
    json.dumps({'restored':restored,'missing':missing},indent=2)+'\n')
print(json.dumps({'ship_keys':len(keys),'restored':len(restored),'missing':len(missing)}))
