import re,json,struct,shutil,hashlib,html
from pathlib import Path
B=Path('tools/quote_preservation_revision_20260925');B.mkdir(exist_ok=False);F=Path('tools/quote_full_audit_20260925');R=Path('tools/quote_revision_20260925');p=Path('data/text/quotes.txt');bp=Path('data/text/quotes.txt.strings.bin');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in [p,bp,F/'audit.json',F/'audit.html',F/'audit.md',F/'manifest.json',R/'retained.html']:
 dest=B/('full_'+f.name if f.parent==F else f.name);shutil.copy2(f,dest)
s=p.read_text(encoding='utf-16');old=dict(re.findall(r'^\{([^}]+)\}(.*)$',s,re.M));new=dict(old);m=json.loads((F/'manifest.json').read_text(encoding='utf-8'));restored=[]
for c in m['changes']:
 k=c['key']
 if k.startswith('Author_') and any(w in c['before'] for w in ['Thrice','Twice','Four times']):new[k]=c['before'].rstrip();restored.append(k)
 if k.startswith('Quote_') and k!='Quote_9':new[k]=c['before']
for k,v in new.items():
 if v!=old[k]:s=re.sub(r'^\{'+re.escape(k)+r'\}.*$',lambda _: '{'+k+'}'+v,s,flags=re.M)
b=bp.read_bytes();pos=8;records=[]
def read():
 global pos
 n=struct.unpack_from('<H',b,pos)[0];pos+=2;v=b[pos:pos+2*n].decode('utf-16le');pos+=2*n;return v
for _ in range(struct.unpack_from('<I',b,4)[0]):k=read();records.append((k,read()))
assert dict(records)==old;tail=b[pos:]
def field(v):d=v.encode('utf-16le');return struct.pack('<H',len(d)//2)+d
p.write_bytes(b'\xff\xfe'+s.replace('\n','\r\n').encode('utf-16le'));bp.write_bytes(b[:8]+b''.join(field(k)+field(new[k]) for k,v in records)+tail)
b=bp.read_bytes();pos=8;decoded={}
for _ in range(struct.unpack_from('<I',b,4)[0]):k=read();decoded[k]=read()
assert decoded==new and b[pos:]==tail
baseline=dict(re.findall(r'^\{([^}]+)\}(.*)$',(F/'quotes.txt').read_text(encoding='utf-16'),re.M));assert [i for i in range(1,123) if new[f'Quote_{i}']!=baseline[f'Quote_{i}']]==[9]
rows=json.loads((F/'audit.json').read_text(encoding='utf-8'))
for r in rows:
 n=r['id'];r['quote']=new[f'Quote_{n}'];r['author']=new[f'Author_{n}'];r['changed']=r['quote']!=r['before_quote'] or r['author']!=r['before_author']
 if f'Author_{n}' in restored:r['note']='Term count restored and retained as requested. '+re.sub(r'^(Shorten the attribution\.|Shorten the biography\.)\s*','',r['note'])
 if n in [1,20]:r['note']='Presidential term count retained as requested. Original quotation wording preserved.'
 if n==3:r['note']='Original wording preserved; no explanatory insertion. Somsteu refers to Theophilus Shepstone; identification is recorded in the audit only.'
 if n==26:r['note']='Intentional euphemistic ambiguity: the military language also permits a sexual reading. Keep the original wording without explaining the joke.';r['needs_review']=False;r['priority']=False
 if old[f'Quote_{n}']!=new[f'Quote_{n}'] and n not in [3,20]:r['note']='Original quote text restored; punctuation and typography are preserved. '+r['note']
 if f'Author_{n}' in restored:r['note']=r['note'].replace('Shorten the attribution.','').replace('Shorten the biography.','')
(F/'audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
header=(F/'audit.html').read_text(encoding='utf-8').split('<article ')[0];header=header.replace('Routine corrections installed; unresolved historical or editorial questions are flagged.','Term counts retained. Original quote text preserved except the clear taking/talking typo in 9. Quote 26’s euphemistic ambiguity is intentional. Unresolved historical questions are flagged.')
parts=[header]
for r in rows:
 parts.append(f'<article data-review="{int(r["needs_review"])}" data-priority="{int(r["priority"])}" data-edited="{int(r["changed"])}"><h2>{r["id"]}'+(' · <span class="flag">Needs review</span>' if r['needs_review'] else '')+f'</h2><blockquote>{html.escape(r["quote"])}</blockquote><p>{html.escape(r["author"])}</p><p class="note">{html.escape(r["note"])}</p>')
 if r['changed']:parts.append('<details><summary>Previous text</summary><p>'+html.escape(r['before_quote'])+'</p><p>'+html.escape(r['before_author'])+'</p></details>')
 if r.get('source'):parts.append('<a href="'+r['source']+'">Checked source</a>')
 parts.append('</article>')
parts.append('<script>function f(){let q=document.getElementById("q").value.toLowerCase(),v=document.getElementById("v").value;document.querySelectorAll("article").forEach(e=>e.hidden=!(e.textContent.toLowerCase().includes(q)&&(v==="all"||e.dataset[v]==="1")))}</script>');(F/'audit.html').write_text(''.join(parts),encoding='utf-8')
md=['# Full quote audit — corrected editorial policy','','Term counts retained. Quote 26 deliberately permits a euphemistic reading and requires no clarification. Preserve original quote wording and typography except clear grammatical or typing errors. Of all quote-text edits in the full pass, only taking → talking in 9 remains. Other attribution corrections remain. No deletions or renumbering.','','| ID | Finding |','|---:|---|']
md += [f'| {r["id"]} | {r["note"]} |' for r in rows];md+=['','Historical source checks remain targeted, not exhaustive. Text and compiled values match; lookup sections unchanged. Backups and this policy correction are in tools/quote_preservation_revision_20260925/.'];(F/'audit.md').write_text('\n'.join(md),encoding='utf-8')
f=R/'retained.html';page=f.read_text(encoding='utf-8')
for k,v in new.items():
 if old[k]!=v:page=page.replace(html.escape(old[k]),html.escape(v))
f.write_text(page,encoding='utf-8')
changes=[dict(key=k,before=baseline[k],after=v) for k,v in new.items() if baseline[k]!=v];m.update(changes=changes,changed_authors=sum(c['key'].startswith('Author') for c in changes),changed_quote_strings=1,preservation_revision=str(B),validation='122 pairs verified; original quote text restored except Quote_9 typo; term counts restored; intentional ambiguity of Quote_26 accepted; lookup lists unchanged.')
for x in m['files']:x['after_sha256']=sha(Path(x['path']))
(F/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
f=R/'manifest.json';rm=json.loads(f.read_text(encoding='utf-8'))
for x in rm['files']:x['after_sha256']=sha(Path(x['path']))
rm['preservation_revision']=str(B);f.write_text(json.dumps(rm,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'manifest.json').write_text(json.dumps(dict(restored_term_counts=restored,changes=[dict(key=k,before=old[k],after=v) for k,v in new.items() if v!=old[k]],policy='Preserve original quotations except clear grammatical/typing errors; retain term counts; preserve intentional euphemistic ambiguity.',validation=m['validation']),ensure_ascii=False,indent=2),encoding='utf-8')
print('Restored',len(restored),'term-count attributions. All original quote text restored except clear Quote_9 typo. Game binary and reviews updated and verified.')
