import re,struct,json,shutil,hashlib,html
from pathlib import Path
B=Path('tools/quote_aizu_context_20260925');B.mkdir(exist_ok=False)
p=Path('data/text/quotes.txt');bp=Path('data/text/quotes.txt.strings.bin');R=Path('tools/quote_revision_20260925');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in [p,bp,R/'retained.html',R/'CHANGES.md',R/'manifest.json']:shutil.copy2(f,B/f.name)
s=p.read_text(encoding='utf-16');old=dict(re.findall(r'^\{([^}]+)\}(.*)$',s,re.M));v='Matsudaira Katamori, Daimyō of Aizu; defeated at the Battle of Aizu, 1868';s=s.replace('{Author_111}'+old['Author_111'],'{Author_111}'+v);new=dict(re.findall(r'^\{([^}]+)\}(.*)$',s,re.M));assert [k for k in old if old[k]!=new[k]]==['Author_111']
b=bp.read_bytes();pos=8;records=[]
def read():
 global pos
 n=struct.unpack_from('<H',b,pos)[0];pos+=2;t=b[pos:pos+2*n].decode('utf-16le');pos+=2*n;return t
for _ in range(struct.unpack_from('<I',b,4)[0]):k=read();records.append((k,read()))
assert dict(records)==old;trailer=b[pos:]
def field(s):q=s.encode('utf-16le');return struct.pack('<H',len(q)//2)+q
out=b[:8]+b''.join(field(k)+field(new[k]) for k,val in records)+trailer
p.write_bytes(b'\xff\xfe'+s.replace('\n','\r\n').encode('utf-16le'));bp.write_bytes(out)
b=bp.read_bytes();pos=8;check={}
for _ in range(struct.unpack_from('<I',b,4)[0]):k=read();check[k]=read()
assert check==new and b[pos:]==trailer
for f in [R/'retained.html',R/'CHANGES.md']:
 t=f.read_text(encoding='utf-8');t=t.replace(html.escape(old['Author_111']),html.escape(v)) if f.suffix=='.html' else t.replace(old['Author_111'],v);f.write_text(t,encoding='utf-8')
m=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
for f in m['files']:f['after_sha256']=sha(Path(f['path']))
m['aizu_context_revision']='tools/quote_aizu_context_20260925/manifest.json';(R/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'manifest.json').write_text(json.dumps(dict(id=111,before=old['Author_111'],after=v,source='https://www.ndl.go.jp/en/landmarks/column/aizuwar',timing_note='The defeat is documented; the quotation date remains unverified. No before or spoken-at claim added.',validation='Only Author_111 changed; quotation wording, other attributions and lookup sections unchanged; binary round-trip verified.'),ensure_ascii=False,indent=2),encoding='utf-8')
print('Aizu attribution updated in game text, binary and review page; single-entry change verified.')
