from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'data/unit_models/battle_models.modeldb'
s=P.read_text(encoding='utf-8')
def hs(t):
 return [(m.group(2),m.start()) for m in re.finditer(r'^(\d+) ([^\s;]+)\s*\n\d+ \d+\s*$',t,re.M) if int(m.group(1))==len(m.group(2))]
h=hs(s)
def bounds(name):
 i=next(i for i,x in enumerate(h) if x[0]==name); return h[i][1],(h[i+1][1] if i+1<len(h) else len(s))
a,z=bounds('csa_standard_bearer'); donor=s[a:z]
new=donor.replace('19 csa_standard_bearer','20 boer_standard_bearer',1)
for old,newp in [
 ('unit_models/_Units/off/csa_standard_bearer_lod0.mesh','unit_models/_Units/off/boer_standard_bearer_lod0.mesh'),
 ('unit_models/_Units/bnw/textures/csa_standard_flag.texture','unit_models/_Units/bnw/textures/boer_standard_flag.texture'),
 ('unit_models/_Units/bnw/textures/csa_standard_flag_n.texture','unit_models/_Units/bnw/textures/boer_standard_flag_n.texture')]:
 new=new.replace(f'{len(old)} {old}',f'{len(newp)} {newp}')
new=new.replace('5 milan','3 teu')
a,z=bounds('boer_standard_bearer'); s=s[:a]+new+s[z:]
P.write_text(s,encoding='utf-8',newline='')
print('Finished end-of-file-safe Boer bearer modeldb replacement.')
