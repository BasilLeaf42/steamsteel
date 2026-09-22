"""Replace the CSA general rider's Colt group with the verified USA cavalry Winchester group."""
from pathlib import Path
import copy, json, struct

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'tools/mesh_work/boer_general_carbine'

def load(name):
    data=(WORK/name).read_bytes()
    if data[:4]!=b'glTF': raise RuntimeError('bad GLB')
    jlen,jtype=struct.unpack_from('<II',data,12)
    if jtype!=0x4E4F534A: raise RuntimeError('missing JSON chunk')
    doc=json.loads(data[20:20+jlen].decode())
    off=20+jlen
    blen,btype=struct.unpack_from('<II',data,off)
    if btype!=0x004E4942: raise RuntimeError('missing BIN chunk')
    return doc,data[off+8:off+8+blen]

base,bbin=load('csa_gen_1g.glb')
donor,dbin=load('usa_cav_1g.glb')
bn=[base['nodes'][x].get('name') for x in base['skins'][0]['joints']]
dn=[donor['nodes'][x].get('name') for x in donor['skins'][0]['joints']]
if bn!=dn: raise RuntimeError('skeleton mismatch')

dnode=next(x for x in donor['nodes'] if x.get('name')=='primaryactive0__winchester_01')
dmesh=donor['meshes'][dnode['mesh']]
prim=dmesh['primitives'][0]
used_acc=list(prim['attributes'].values())+[prim['indices']]
acc_map={}
view_map={}
for ai in used_acc:
    a=copy.deepcopy(donor['accessors'][ai]); vi=a['bufferView']
    if vi not in view_map:
        v=copy.deepcopy(donor['bufferViews'][vi]); v['byteOffset']=v.get('byteOffset',0)+len(bbin)
        view_map[vi]=len(base['bufferViews']); base['bufferViews'].append(v)
    a['bufferView']=view_map[vi]
    acc_map[ai]=len(base['accessors']); base['accessors'].append(a)

bnode=next(x for x in base['nodes'] if x.get('name')=='primaryactive0__colt_01')
bmesh=base['meshes'][bnode['mesh']]
bnode['name']='primaryactive0__winchester_01'
bnode['translation']=copy.deepcopy(dnode.get('translation',[0,0,0]))
bmesh['name']='primaryactive0__winchester_01'
bmesh['primitives']=[{'attributes':{k:acc_map[v] for k,v in prim['attributes'].items()},
                      'indices':acc_map[prim['indices']], 'material':1}]

binary=bbin+dbin
base['buffers'][0]['byteLength']=len(binary)
encoded=json.dumps(base,separators=(',',':')).encode(); encoded+=b' ' *((4-len(encoded)%4)%4)
binary+=b'\0'*((4-len(binary)%4)%4)
total=12+8+len(encoded)+8+len(binary)
out=b'glTF'+struct.pack('<II',2,total)+struct.pack('<II',len(encoded),0x4E4F534A)+encoded
out+=struct.pack('<II',len(binary),0x004E4942)+binary
(WORK/'boer_mounted_kommando.glb').write_bytes(out)
print('Built general-body GLB with Winchester primary and retained sabre secondary.')
