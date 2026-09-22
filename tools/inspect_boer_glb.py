from pathlib import Path
import json, struct

root = Path(__file__).resolve().parents[1] / 'tools/mesh_work/boer_general_carbine'
for fn in ('csa_gen_1g.glb','usa_cav_1g.glb'):
    data=(root/fn).read_bytes(); n=struct.unpack_from('<I',data,12)[0]
    doc=json.loads(data[20:20+n].decode())
    print('\n',fn)
    print('scene',doc.get('scenes'), 'skins',len(doc.get('skins',[])))
    for i,x in enumerate(doc.get('nodes',[])):
        name=x.get('name','')
        if any(k in name.lower() for k in ('primary','secondary','carb','colt','sword','sabre')):
            print('node',i,name,{k:v for k,v in x.items() if k!='name'})
    for i,x in enumerate(doc.get('meshes',[])):
        name=x.get('name','')
        if any(k in name.lower() for k in ('primary','secondary','carb','colt','sword','sabre')):
            print('mesh',i,name,x)
    print('counts',{k:len(doc.get(k,[])) for k in ('nodes','meshes','accessors','bufferViews','materials')})
