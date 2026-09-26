import re,json,struct,shutil,hashlib,html
from pathlib import Path
B=Path('tools/quote_attribution_revision_20260925');B.mkdir(exist_ok=False)
p=Path('data/text/quotes.txt');bp=Path('data/text/quotes.txt.strings.bin');look=Path('data/descr_quotes_lookup.txt');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={str(f):sha(f) for f in [p,bp,look]}
for f in [p,bp]:shutil.copy2(f,B/f.name)
R=Path('tools/quote_revision_20260925')
for f in ['retained.html','CHANGES.md','manifest.json']:shutil.copy2(R/f,B/f)
s=p.read_text(encoding='utf-16');old=dict(re.findall(r'^\{([^}]+)\}(.*)$',s,re.M))
a={111:'Matsudaira Katamori, Daimyō of Aizu',112:'Sakurai Tadayoshi, Lieutenant of the Imperial Japanese Army, "Human Bullets"',113:'Đỗ Hữu Vị, Captain of the French Foreign Legion',114:'Cixi, Empress Dowager of the Qing dynasty',115:'Zuo Zongtang, General of the Qing dynasty',116:'Liú Yǒngfú, General of the Black Flag Army',117:'Charles Clive Bigham, British intelligence officer',118:'Ōtori Keisuke, Commander of the Ezo army; urging surrender at Hakodate',119:'Léon Roches, French consul in Japan',120:'Pierre-Louis Charles de Failly, Divisional general of the French Army; after the Battle of Mentana, 1867',121:'Menelik II, Ethiopian King of Kings',122:'Sakuma Shōzan, Japanese scholar'}
for n,v in a.items():s=re.sub(r'^\{Author_'+str(n)+r'\}.*$',lambda m:'{Author_'+str(n)+'}'+v,s,flags=re.M)
new=dict(re.findall(r'^\{([^}]+)\}(.*)$',s,re.M))
b=bp.read_bytes();pos=8;records=[]
def read():
 global pos
 n=struct.unpack_from('<H',b,pos)[0];pos+=2;v=b[pos:pos+2*n].decode('utf-16le');pos+=2*n;return v
for _ in range(struct.unpack_from('<I',b,4)[0]):k=read();v=read();records.append((k,v))
trailer=b[pos:]
def field(v):q=v.encode('utf-16le');return struct.pack('<H',len(q)//2)+q
out=b[:8]+b''.join(field(k)+field(new[k]) for k,v in records)+trailer
assert {k:v for k,v in records}==old
assert all(new[k]==v for k,v in old.items() if k not in {f'Author_{n}' for n in a})
p.write_bytes(b'\xff\xfe'+s.replace('\n','\r\n').encode('utf-16le'));bp.write_bytes(out)
b=bp.read_bytes();pos=8;decoded={}
for _ in range(struct.unpack_from('<I',b,4)[0]):k=read();decoded[k]=read()
assert decoded==new and b[pos:]==trailer and sha(look)==before[str(look)]
changes=[dict(id=n,before=old[f'Author_{n}'],after=v) for n,v in a.items()]
(B/'manifest.json').write_text(json.dumps(dict(changes=changes,files=[dict(path=str(f),before_sha256=before[str(f)],after_sha256=sha(f)) for f in [p,bp,look]],validation='All 122 quote texts and authors 1–110 unchanged; 12 attributions revised; binary round-trip matches text; both lookup lists unchanged.'),ensure_ascii=False,indent=2),encoding='utf-8')
page=(R/'retained.html').read_text(encoding='utf-8');report=(R/'CHANGES.md').read_text(encoding='utf-8')
for c in changes:page=page.replace(html.escape(c['before']),html.escape(c['after']));report=report.replace(c['before'],c['after'])
page=page.replace('with brief context.','with standard attributions and only essential context.');(R/'retained.html').write_text(page,encoding='utf-8');report+='\n\nAttribution revision: redundant topic descriptions removed. Only the source title Human Bullets, the surrender situation at Hakodate, and the Mentana occasion are retained as clarifications. All quotation wording is unchanged.\n';(R/'CHANGES.md').write_text(report,encoding='utf-8')
m=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
for f in m['files']:f['after_sha256']=sha(Path(f['path']))
m['attribution_revision']='tools/quote_attribution_revision_20260925/manifest.json';(R/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('12 attributions revised; all 122 quotation texts unchanged; compiled text verified; lookup files unchanged.')
