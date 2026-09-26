from pathlib import Path
import json,re,struct,hashlib,shutil,html
B=Path('tools/quote_revision_20260925');B.mkdir(exist_ok=True);assert not (B/'manifest.json').exists(), 'Revision already installed; do not overwrite its backups';root=Path('.');paths=['data/text/quotes.txt','data/text/quotes.txt.strings.bin','data/descr_quotes_lookup.txt']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={p:sha(Path(p)) for p in paths}
for p in paths:target=B/'backup'/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
s=Path(paths[0]).read_text(encoding='utf-16');old=dict(re.findall(r'^\{([^}]+)\}(.*)$',s,re.M));kept=[117,125,126,128,130,131,133,137,141,142,143,147];mapping={i:i for i in range(1,111)}|{n:111+k for k,n in enumerate(kept)}
authors={
117:'Matsudaira Katamori, Daimyō of Aizu (defeated, 1868)',
125:'Sakurai Tadayoshi, Japanese lieutenant; on Port Arthur, 1904',
126:'Đỗ Hữu Vị, French Foreign Legion captain; on colonial service',
128:'Cixi, Empress Dowager of the Qing dynasty; on foreign intervention',
130:'Zuo Zongtang, Qing general; on confronting Russia',
131:'Liú Yǒngfú, Black Flag commander; challenging the French, 1883',
133:'Charles Clive Bigham, British officer; on Chinese resistance at Langfang, 1900',
137:'Ōtori Keisuke, Tokugawa commander; on surrender at Hakodate, 1869',
141:'Léon Roches, French diplomat; comparing Japan with other Asian peoples',
142:'Pierre-Louis Charles de Failly, French general; after Mentana, 1867',
143:'Menelik II, Ethiopian King of Kings; on Ethiopia’s neighbours',
147:'Sakuma Shōzan, Japanese scholar; on modernisation',
}
new={}
for kind in ['Author','Quote']:
 for oldid,newid in mapping.items():new[f'{kind}_{newid}']=authors.get(oldid,old[f'Author_{oldid}']) if kind=='Author' else old[f'Quote_{oldid}']
# Preserve the complete earlier lines, including trailing whitespace, and original UTF-16 LE BOM.
output='¬\r\n'+'\r\n'.join('{'+k+'}'+v for k,v in new.items() if k.startswith('Author_'))+'\r\n\r\n'+'\r\n'.join('{'+k+'}'+v for k,v in new.items() if k.startswith('Quote_'))+'\r\n'
keys=[f'{kind}_{i}' for kind in ['Quote','Author'] for i in range(1,123)]
def field(s):
 b=s.encode('utf-16le');return struct.pack('<H',len(b)//2)+b
binary=Path(paths[1]).read_bytes()[:4]+struct.pack('<I',len(new))+b''.join(field(k)+field(v) for k,v in new.items())+struct.pack('<I',len(keys))+b''.join(field(k) for k in keys)
(B/'staged').mkdir(exist_ok=True);(B/'staged/quotes.txt').write_bytes(b'\xff\xfe'+output.encode('utf-16le'));(B/'staged/quotes.txt.strings.bin').write_bytes(binary);(B/'staged/descr_quotes_lookup.txt').write_bytes(('\r\n'.join(keys)+'\r\n').encode('ascii'))
# Independent round-trip of both binary sections and key relationships.
p=8;parsed={}
def read_field():
 global p
 n=struct.unpack_from('<H',binary,p)[0];p+=2;v=binary[p:p+n*2].decode('utf-16le');p+=n*2;return v
for _ in range(struct.unpack_from('<I',binary,4)[0]):k=read_field();parsed[k]=read_field()
n=struct.unpack_from('<I',binary,p)[0];p+=4;trailer=[read_field() for _ in range(n)]
assert p==len(binary) and parsed==new and trailer==keys and len(parsed)==244
staged=dict(re.findall(r'^\{([^}]+)\}(.*)$',(B/'staged/quotes.txt').read_text(encoding='utf-16'),re.M));assert staged==new
for i in range(1,111):
 for kind in ['Quote','Author']:assert new[f'{kind}_{i}']==old[f'{kind}_{i}']
for oldid,newid in mapping.items():assert new[f'Quote_{newid}']==old[f'Quote_{oldid}']
assert all(sha(Path(p))==h for p,h in before.items())
for p in paths:shutil.copy2(B/'staged'/Path(p).name,p)
removed=sorted(set(range(111,158))-set(kept));audit=json.loads(Path('tools/quote_audit_20260925/inventory.json').read_text(encoding='utf-8'));ar={x['id']:x for x in audit['quotes']}
manifest=dict(original_count=157,installed_count=122,removed_original_ids=removed,retained_later_original_ids=kept,id_mapping=mapping,files=[dict(path=p,before_sha256=before[p],after_sha256=sha(Path(p))) for p in paths],validation='Text/binary entries identical; embedded and external lookup lists identical; 122 contiguous quote/author pairs; original 1–110 and all surviving quote wording unchanged. Engine display not tested.',source_audit='tools/quote_audit_20260925/inventory.json')
(B/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
report=['# Applied loading-quote edit','Removed 35 of the 47 later additions; 122 quotes remain. Quotes and author labels 1–110 are unchanged. Every surviving quotation keeps its original wording. Later author labels now provide only short context.','The original audit was advisory: contextual candidates were reconsidered against the earlier collection, which also includes concise realpolitik and revealing imperial assumptions. Brief context rescues 130, 131, 133, 143 and 147. The other contextual candidates and the 22 original removal candidates are excluded.','## Retained later entries','| Original ID | Installed ID | New attribution |','|---:|---:|---|']
for n in kept:report.append(f'| {n} | {mapping[n]} | {authors[n]} |')
report+=['','## Removed original IDs',', '.join(map(str,removed)), '', '## Validation',manifest['validation'],'','All three original files are preserved under backup/. The compiled format was fully decoded: its final section is the lookup list, not unexplained padding. Both lookup copies now list only the 122 survivors. Continuous numbering avoids assuming the game safely handles missing numeric IDs. manifest.json records the old-to-new mapping.','Attribution authentication remains limited to the preceding audit and checked contextual facts; this edit does not claim to authenticate every surviving historical quotation.','Additional source checks: https://www.tandfonline.com/doi/abs/10.1080/1463136042000270614 (Sakuma formulation); https://en.wikipedia.org/wiki/Battle_of_C%E1%BA%A7u_Gi%E1%BA%A5y_%281883%29 (Liu challenge, 1883).']
(B/'CHANGES.md').write_text('\n\n'.join(report),encoding='utf-8')
page=['<!doctype html><meta charset="utf-8"><title>Revised loading quotes</title><style>body{max-width:960px;margin:40px auto;padding:20px;background:#191d20;color:#eee8db;font:17px/1.5 system-ui}article{border-top:1px solid #555;padding:20px 0}blockquote{margin:12px 0;font:22px/1.5 Georgia}a{color:#acd5ef}</style><h1>Revised loading quotes</h1><p>122 installed quotes. The earlier 110 remain unchanged; these 12 survive from the later additions, with brief context.</p><p><a href="CHANGES.md">Changes, removed IDs and verification</a></p>']
for n in kept:page.append(f'<article><h2>{mapping[n]} <small>(formerly {n})</small></h2><blockquote>{html.escape(old[f"Quote_{n}"])}</blockquote><p>{html.escape(authors[n])}</p></article>')
(B/'retained.html').write_text(''.join(page),encoding='utf-8')
print('Installed 122 quotes; removed 35. Text, compiled records, embedded lookup and external lookup verified. Original 1–110 unchanged.')
