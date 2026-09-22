from pathlib import Path
import json,re,struct
ROOT=Path(__file__).resolve().parents[1]
def glb_doc(p):
 d=p.read_bytes(); n=struct.unpack_from('<I',d,12)[0]; return json.loads(d[20:20+n].decode())
work=ROOT/'tools/mesh_work/boer_general_carbine'
base=glb_doc(work/'csa_gen_1g.glb'); out=glb_doc(work/'audit/boer_mounted_kommando.glb')
names=lambda d:{x.get('name') for x in d.get('meshes',[])}
bn,on=names(base),names(out)
assert 'primaryactive0__colt_01' not in on
assert 'primaryactive0__winchester_01' in on
assert 'secondaryactive0__saber_01' in on
assert (bn-{'primaryactive0__colt_01'}) <= on
model=(ROOT/'data/unit_models/battle_models.modeldb').read_text(encoding='utf-8')
for n in ('boer_mounted_kommando_early','boer_mounted_kommando_mid','boer_mounted_kommando_high'):
 i=model.index(f'{len(n)} {n}'); e=model.index('16 -0.090000004',i); b=model[i:e]
 assert b.count('unit_models/_Units/bnw/boer_mounted_kommando_lod0.mesh')==4
 assert 'MTW2_CR_Arquebus' in b and 'MTW2_HR_Arquebus_Primary' in b and 'MTW2_HR_Pistol' not in b
mount=(ROOT/'data/descr_mount.txt').read_text(encoding='utf-8')
b=re.search(r'^type\s+boer_wagon\s*$[\s\S]*?(?=^type\s+|\Z)',mount,re.M).group(0)
rows=re.findall(r'^rider_offset\s+([-0-9.]+),\s*([-0-9.]+),\s*([-0-9.]+)',b,re.M)
assert len(rows)==6 and all(y=='0.5' for x,y,z in rows)
for era in ('early','mid','high'):
 d=(ROOT/f'data/ui/units/teu/#boer_mounted_kommando_{era}.tga').read_bytes()
 assert struct.unpack_from('<HH',d,12)==(48,64) and d[16]==32
print('Boer general-body carbine mesh, Colt removal, sabre secondary, Laager Y=0.5, mappings, and cards validated.')
