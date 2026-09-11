from pathlib import Path
import hashlib
import json
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
canonical = ROOT / 'data/tow_steamsteel/export_descr_unit.txt'
runtime = ROOT / 'data/export_descr_unit.txt'
assert canonical.read_bytes() == runtime.read_bytes(), 'EDU mirrors differ'
edu = canonical.read_text(encoding='utf-8', errors='replace').replace('\r', '')
blocks = {}
for block in re.split(r'(?=^type\s+)', edu, flags=re.M):
    match = re.search(r'^type\s+(\S+)', block, flags=re.M)
    if match:
        blocks[match.group(1)] = block

bearers = {
    'ita_line_early','ita_line_mid','ita_milizia_early','ita_milizia_mid',
    'ita_granatieri_early','ita_granatieri_mid','ita_bersaglieri_early','ita_bersaglieri_mid',
    'ita_alpini_mid','ita_marina_early','ita_marina_mid','ita_zappatori_early',
    'ita_zappatori_mid','ita_garibaldini_early'
}
for name in bearers:
    assert len(re.findall(r'^officer\s+russia_qi$', blocks[name], flags=re.M)) == 1, f'{name}: missing/duplicate bearer'
for name, block in blocks.items():
    if name.startswith('ita_') and ('_high' in name or name in {'ita_arditi_high','ita_ascari_high','ita_libici_high'}):
        assert 'officer          russia_qi' not in block, f'{name}: late bearer retained'

for name, block in blocks.items():
    if re.search(r'^attributes\s+.*\bgeneral_unit\b', block, flags=re.M) and re.search(r'^soldier\s+\S+,\s*4,', block, flags=re.M):
        assert re.search(r'^category\s+cavalry$', block, flags=re.M), f'{name}: general not cavalry'
        assert re.search(r'^class\s+light$', block, flags=re.M), f'{name}: general not light cavalry'

model = (ROOT / 'data/unit_models/battle_models.modeldb').read_text(encoding='utf-8', errors='replace').replace('\r', '')
declared = int(re.match(r'^22 serialization::archive 3 0 0 0 0 (\d+) 0 0', model).group(1))
headers = [m for m in re.finditer(r'^(\d+) ([^\s;]+)\s*\n\d+ \d+\s*$', model, flags=re.M) if int(m.group(1)) == len(m.group(2))]
# The committed 932-entry baseline contains one legacy header shape this conservative
# detector does not recognize; Italy must preserve that exact one-entry delta.
assert declared - len(headers) == 1, f'unexpected modeldb header delta: {declared} declared, {len(headers)} detected'
entries = {}
for index, match in enumerate(headers):
    end = headers[index + 1].start() if index + 1 < len(headers) else len(model)
    entries[match.group(2)] = model[match.start():end]
assert 'koi_pis_1g_lod0.mesh' in entries['ita_cavalleggeri']
assert 'MTW2_HR_Pistol' in entries['ita_cavalleggeri'] and 'MTW2_HR_Pistol_Primary' in entries['ita_cavalleggeri']
assert 'unit_sprites/tmp_cavalry_sprite.spr' in entries['ita_cavalleggeri'], 'ita_cavalleggeri: standard mounted distant sprite missing'
for name in ('ita_carabinieri_early','ita_carabinieri_mid','ita_carabinieri_high'):
    assert 'koi_crb_1g_lod0.mesh' in entries[name], f'{name}: wrong visible rider mesh'
    assert 'MTW2_CR_Arquebus' in entries[name] and 'MTW2_HR_Arquebus_Primary' in entries[name], f'{name}: wrong carbine slots'
    assert 'unit_sprites/tmp_cavalry_sprite.spr' in entries[name], f'{name}: standard mounted distant sprite missing'
for name in ('ita_cavalleggeri','ita_carabinieri_early','ita_carabinieri_mid','ita_carabinieri_high'):
    for line in entries[name].splitlines():
        line = line.strip()
        if not any(suffix in line for suffix in ('.mesh ', '.texture ', '.spr ')):
            continue
        count, rest = line.split(' ', 1)
        asset = rest.rsplit(' ', 1)[0] if rest.rsplit(' ', 1)[-1] in {'0','20000'} else rest
        assert int(count) == len(asset), f'{name}: bad string checksum: {line}'

cards = ['ita_milizia_early','ita_milizia_mid','ita_milizia_high','ita_cavalleggeri','ita_lancieri','ita_carabinieri_early','ita_carabinieri_mid','ita_carabinieri_high','ita_general_staff']
hashes = {}
for name in cards:
    path = ROOT / f'data/ui/units/venice/#{name}.tga'
    image = Image.open(path).convert('RGBA')
    assert image.size == (48,64), f'{name}: wrong card size'
    assert image.getchannel('A').getextrema() == (255,255), f'{name}: wrong alpha'
    hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
assert len({hashes[n] for n in ('ita_milizia_early','ita_milizia_mid','ita_milizia_high')}) == 1
assert len({hashes[n] for n in ('ita_carabinieri_early','ita_carabinieri_mid','ita_carabinieri_high')}) == 1
assert len({hashes[n] for n in ('ita_milizia_early','ita_cavalleggeri','ita_lancieri','ita_carabinieri_early','ita_general_staff')}) == 5
json.loads((ROOT / 'tools/historical_card_sources.json').read_text(encoding='utf-8'))
print(f'PASS: {len(bearers)} Italian bearer records, all four-man generals light cavalry, modeldb {declared} entries, {len(cards)} cards validated.')
