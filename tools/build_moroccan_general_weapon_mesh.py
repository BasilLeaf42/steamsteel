"""Clone the Omani rider and correct its misspelled switchable pistol group."""
from pathlib import Path
import shutil

R=Path(__file__).resolve().parents[1]
src=R/'data/unit_models/_Units/oma/oma_cav_1g_lod0.mesh'
dst=R/'data/unit_models/_Units/oma/mor_general_staff_lod0.mesh'
data=src.read_bytes(); old=b'priamryactive0'; new=b'primaryactive0'
if len(old)!=len(new) or data.count(old)!=1 or data.count(b'secondaryactive0')!=1:
 raise RuntimeError('Unexpected Omani pistol/sabre group structure')
dst.write_bytes(data.replace(old,new))
print('Built dedicated Moroccan general mesh with switchable pistol and sabre groups.')
