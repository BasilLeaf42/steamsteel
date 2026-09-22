"""Replace the broken Boer bearer mapping with the complete verified CSA bearer package."""
from pathlib import Path
import re, shutil

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/'data/unit_models/battle_models.modeldb'
BACK=ROOT/'tools/backup_before_boer_bearer_repair_20260916'
BACK.mkdir(exist_ok=True)
if not (BACK/'battle_models.modeldb').exists(): shutil.copy2(MODEL,BACK/'battle_models.modeldb')
src_mesh=ROOT/'data/unit_models/_Units/off/csa_standard_bearer_lod0.mesh'
dst_mesh=ROOT/'data/unit_models/_Units/off/boer_standard_bearer_lod0.mesh'
if not (BACK/dst_mesh.name).exists(): shutil.copy2(dst_mesh,BACK/dst_mesh.name)
shutil.copy2(src_mesh,dst_mesh)

text=MODEL.read_text(encoding='utf-8')
def heads(s):
 out=[]
 for m in re.finditer(r'^(\d+) ([^\s;]+)\s*\n\d+ \d+\s*$',s,re.M):
  if int(m.group(1))==len(m.group(2)): out.append((m.group(2),m.start()))
 return out
hs=heads(text)
def block(name):
 i=next(i for i,x in enumerate(hs) if x[0]==name); return text[hs[i][1]:hs[i+1][1]]
donor=block('csa_standard_bearer')
new=donor.replace('19 csa_standard_bearer','20 boer_standard_bearer',1)
old_mesh='unit_models/_Units/off/csa_standard_bearer_lod0.mesh'
new_mesh='unit_models/_Units/off/boer_standard_bearer_lod0.mesh'
new=new.replace(f'{len(old_mesh)} {old_mesh}',f'{len(new_mesh)} {new_mesh}')
new=new.replace('5 milan','3 teu')
old_flag='unit_models/_Units/bnw/textures/csa_standard_flag.texture'
new_flag='unit_models/_Units/bnw/textures/boer_standard_flag.texture'
old_norm='unit_models/_Units/bnw/textures/csa_standard_flag_n.texture'
new_norm='unit_models/_Units/bnw/textures/boer_standard_flag_n.texture'
new=new.replace(f'{len(old_flag)} {old_flag}',f'{len(new_flag)} {new_flag}')
new=new.replace(f'{len(old_norm)} {old_norm}',f'{len(new_norm)} {new_norm}')
hs=heads(text); i=next(i for i,x in enumerate(hs) if x[0]=='boer_standard_bearer')
text=text[:hs[i][1]]+new+text[hs[i+1][1]:]
MODEL.write_text(text,encoding='utf-8',newline='')
print('Installed complete verified bearer mapping with CSA captain body/face and Boer Vierkleur attachment.')
