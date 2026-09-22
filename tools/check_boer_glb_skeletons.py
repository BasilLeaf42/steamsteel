from pathlib import Path
import json, struct
root=Path(__file__).resolve().parents[1]/'tools/mesh_work/boer_general_carbine'
seq=[]
for fn in ('csa_gen_1g.glb','usa_cav_1g.glb'):
 d=(root/fn).read_bytes(); n=struct.unpack_from('<I',d,12)[0]; j=json.loads(d[20:20+n]);
 names=[j['nodes'][x].get('name') for x in j['skins'][0]['joints']]; seq.append(names); print(fn,len(names),names)
print('identical',seq[0]==seq[1])
