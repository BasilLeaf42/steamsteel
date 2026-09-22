from pathlib import Path
import json, shutil
from PIL import Image
from standardize_card_backgrounds import replace_connected_background, CANONICAL

ROOT=Path(__file__).resolve().parents[1]
AUDIT=json.loads((ROOT/'tools/remaining_mercenary_audit.json').read_text(encoding='utf-8'))
TYPES=[r['type'] for r in AUDIT['units'] if r['category']!='ship']
MERC=ROOT/'data/ui/units/mercs'; SLAVE=ROOT/'data/ui/units/slave'

# Only exact same-soldier/model or direct compatibility-lineage donors are used.
DONORS={
 'merc_ap_front_cav':'data/ui/units/portugala/#us_scout_cav.tga',
 'merc_apache_inf':'data/ui/units/portugala/#apache_inf.tga',
 'merc_port_inf':'data/ui/units/mercs/#merc_port_inf_early.tga',
 'merc_port_lancer':'data/ui/units/mercs/#merc_port_cav_early.tga',
 'merc_bhutan_warrior':'data/ui/units/bulga/#ind_bhutan_warrior.tga',
 'merc_burmese_inf':'data/ui/units/cru/#burmese_inf.tga',
 'merc_indian_fanatic':'data/ui/units/bulga/#indian_fanatic.tga',
 'merc_mongol_bows':'data/ui/units/byzantium/#mongol_bows.tga',
 'merc_georgian_inf':'data/ui/units/russia/#georgian_inf.tga',
 'merc_kashgar_inf':'data/ui/units/cuman/#kashgar_inf.tga',
 'merc_rus_georgian_cav':'data/ui/units/russia/#rus_georgian_cav.tga',
 'merc_zulu_spearmen':'data/ui/units/lith/#zulu_spearmen.tga',
 'merc_sikh_warriors':'data/ui/units/bulga/#sikh_warriors.tga',
 'merc_siam_agent':'data/ui/units/cru/#siam_agent.tga',
}

report=[]
for unit in TYPES:
    donor=ROOT/DONORS[unit] if unit in DONORS else MERC/f'#{unit}.tga'
    if not donor.is_file(): raise SystemExit(f'missing source card: {donor}')
    with Image.open(donor) as im:
        source=im.convert('RGBA')
    if source.size!=(48,64): raise SystemExit(f'wrong dimensions: {donor} {source.size}')
    output,replaced=replace_connected_background(source)
    for folder in (MERC,SLAVE):
        target=folder/f'#{unit}.tga'
        output.save(target,format='TGA',bits=32,compression='tga_rle')
    report.append({'type':unit,'source':str(donor.relative_to(ROOT)),'background_pixels_replaced':replaced})

(ROOT/'tools/remaining_mercenary_card_install_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'Installed {len(report)} paired 48x64 RGBA mercenary cards on #{CANONICAL[0]:02X}{CANONICAL[1]:02X}{CANONICAL[2]:02X}.')
