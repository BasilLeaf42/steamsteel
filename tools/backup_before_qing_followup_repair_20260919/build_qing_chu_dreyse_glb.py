"""Replace only the SOE Chu infantry spear group with the verified Qing rifle group."""
from pathlib import Path
import copy,json,struct

TMP=Path(r'C:\Users\kwoks\AppData\Local\Temp\qing_chu_dreyse')
def load(p):
 d=p.read_bytes(); assert d[:4]==b'glTF'; jl,jt=struct.unpack_from('<II',d,12); assert jt==0x4e4f534a
 j=json.loads(d[20:20+jl]); o=20+jl; bl,bt=struct.unpack_from('<II',d,o); assert bt==0x004e4942
 return j,d[o+8:o+8+bl]
b,bb=load(TMP/'chu/chu_spear.glb'); d,db=load(TMP/'dreyse/qin_dreyse.glb')
# Disable the three inherited shield geometry nodes without changing skeleton indices.
for node in b['nodes']:
 if node.get('name','').startswith('shield0__'):
  node.pop('mesh',None)
  node['name']='inactive0__removed_'+node['name']
dn=next(x for x in d['nodes'] if x.get('name')=='primaryactive0__chassepot_01'); dp=d['meshes'][dn['mesh']]['primitives'][0]
used=list(dp['attributes'].values())+[dp['indices']]; am={}; vm={}
for ai in used:
 a=copy.deepcopy(d['accessors'][ai]); vi=a['bufferView']
 if vi not in vm:
  v=copy.deepcopy(d['bufferViews'][vi]); v['byteOffset']=v.get('byteOffset',0)+len(bb); vm[vi]=len(b['bufferViews']); b['bufferViews'].append(v)
 a['bufferView']=vm[vi]; am[ai]=len(b['accessors']); b['accessors'].append(a)
bn=next(x for x in b['nodes'] if x.get('name')=='primaryactive0__sablia_01'); bm=b['meshes'][bn['mesh']]
bn['name']='primaryactive0__dreyse_m1868'; bm['name']=bn['name']; bn['translation']=copy.deepcopy(dn.get('translation',[0,0,0])); bn['rotation']=copy.deepcopy(dn.get('rotation',[0,0,0,1])); bn['scale']=copy.deepcopy(dn.get('scale',[1,1,1]))
bm['primitives']=[{'attributes':{k:am[v] for k,v in dp['attributes'].items()},'indices':am[dp['indices']],'material':1}]
binary=bb+db; b['buffers'][0]['byteLength']=len(binary); enc=json.dumps(b,separators=(',',':')).encode(); enc+=b' '*((-len(enc))%4); binary+=b'\0'*((-len(binary))%4)
total=12+8+len(enc)+8+len(binary); out=b'glTF'+struct.pack('<II',2,total)+struct.pack('<II',len(enc),0x4e4f534a)+enc+struct.pack('<II',len(binary),0x004e4942)+binary
(TMP/'chu_dreyse.glb').write_bytes(out); print('built',len(out))
