"""Create Oman's switchable pistol/sabre rider without modifying its legacy donor."""
from pathlib import Path

R=Path(__file__).resolve().parents[1]
src=R/'data/unit_models/_Units/oma/oma_cav_1g_lod0.mesh'
dst=R/'data/unit_models/_Units/oma/oma_cav_pistol_sabre_lod0.mesh'
data=src.read_bytes(); old=b'priamryactive0'; new=b'primaryactive0'
if len(old)!=len(new) or data.count(old)!=1 or data.count(b'secondaryactive0')!=1:
 raise RuntimeError('Unexpected Omani pistol/sabre donor structure')
dst.write_bytes(data.replace(old,new))
print('Built dedicated Omani pistol/sabre mesh with both weapon groups switchable.')
