from pathlib import Path
import re, shutil

ROOT=Path(__file__).resolve().parents[1]
STAMP='20260916'
BACK=ROOT/f'tools/backup_before_boer_general_carbine_{STAMP}'
BACK.mkdir(exist_ok=True)
model=ROOT/'data/unit_models/battle_models.modeldb'
mount=ROOT/'data/descr_mount.txt'
cards=ROOT/'data/ui/units/teu'
for p in (model,mount):
    q=BACK/p.name
    if not q.exists(): shutil.copy2(p,q)
for n in ('early','mid','high'):
    p=cards/f'#boer_mounted_kommando_{n}.tga'; q=BACK/p.name
    if not q.exists(): shutil.copy2(p,q)

text=model.read_text(encoding='utf-8')
def heads(s):
    out=[]
    for m in re.finditer(r'^(\d+) ([^\s;]+)\s*\n\d+ \d+\s*$',s,re.M):
        if int(m.group(1))==len(m.group(2)): out.append((m.group(2),m.start()))
    return out

hs=heads(text); gi=next(i for i,x in enumerate(hs) if x[0]=='boer_general_staff')
general=text[hs[gi][1]:hs[gi+1][1]].rstrip()+"\n"
newmesh='unit_models/_Units/bnw/boer_mounted_kommando_lod0.mesh'
oldmesh='unit_models/_Units/csa/csa_gen_1g_lod0.mesh'
for name in ('boer_mounted_kommando_early','boer_mounted_kommando_mid','boer_mounted_kommando_high'):
    block=general.replace('18 boer_general_staff',f'{len(name)} {name}',1)
    block=block.replace(f'{len(oldmesh)} {oldmesh}',f'{len(newmesh)} {newmesh}')
    block=block.replace('14 MTW2_HR_Pistol','16 MTW2_CR_Arquebus')
    block=block.replace('22 MTW2_HR_Pistol_Primary','24 MTW2_HR_Arquebus_Primary')
    hs=heads(text); i=next(i for i,x in enumerate(hs) if x[0]==name); end=hs[i+1][1]
    text=text[:hs[i][1]]+block+text[end:]
model.write_text(text,encoding='utf-8',newline='')

mt=mount.read_text(encoding='utf-8')
start=mt.index('type\t\t\tboer_wagon')
end=mt.find('\ntype\t\t\t',start+1)
if end<0:end=len(mt)
block=mt[start:end]
block=re.sub(r'^(rider_offset\s+[-0-9.]+),\s*[-0-9.]+,',r'\1, 0.5,',block,flags=re.M)
mt=mt[:start]+block+mt[end:]
mount.write_text(mt,encoding='utf-8',newline='')

donor=ROOT/'data/ui/units/milan/#csa_cav.tga'
for n in ('early','mid','high'): shutil.copy2(donor,cards/f'#boer_mounted_kommando_{n}.tga')
print('Installed general-body carbine rider, Laager Y=0.5, and mounted carbine tactical cards.')
