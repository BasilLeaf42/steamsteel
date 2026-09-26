from pathlib import Path
import re,json,struct,shutil,hashlib,html
B=Path('tools/quote_full_audit_20260925');B.mkdir(exist_ok=False)
p=Path('data/text/quotes.txt');bp=Path('data/text/quotes.txt.strings.bin');lp=Path('data/descr_quotes_lookup.txt');R=Path('tools/quote_revision_20260925');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in [p,bp,lp,R/'retained.html',R/'CHANGES.md',R/'manifest.json']:shutil.copy2(f,B/f.name)
s=p.read_text(encoding='utf-16');old=dict(re.findall(r'^\{([^}]+)\}(.*)$',s,re.M));new=dict(old)
A={1:'Porfirio Díaz, President of Mexico',4:'Henry Hope Crealock, Lieutenant-Colonel; at Isandlwana',6:'Wilhelm I, German Emperor and King of Prussia; on Bismarck',7:'Patrice de MacMahon, Marshal of France',8:'Patrice de MacMahon, Marshal of France; attributed remark at Malakoff, 1855',9:'Patrice de MacMahon, Marshal of France',11:'William McKinley, President of the United States; the Philippines, 1898',20:'Porfirio Díaz, President of Mexico',22:'Charles Robert Darwin, English scientist',23:'Alfred Thayer Mahan, American admiral and historian',32:'Karl Marx, German socialist philosopher; on Napoleon III’s coup (paraphrased)',34:'Karl Marx and Friedrich Engels, "The Communist Manifesto"',36:'Paul Doumer, Governor-General of French Indochina',62:'Henri Duval, French colonial official; rubber production in Indochina',72:'Charles George Gordon, British general',73:'Charles George Gordon, British general',74:'Charles George Gordon, British general; besieged at Khartoum',75:'Charles George Gordon, British officer; burning the Summer Palace, 1860',76:'Henry Morton Stanley, Welsh-American explorer',77:'Henry Morton Stanley, Welsh-American explorer',78:'Henry Morton Stanley, Welsh-American explorer',79:'Shaka kaSenzangakhona, King of the Zulu Kingdom',81:'Rudyard Kipling, English writer and poet, "Land and Sea Tales" (1923)',82:'Rudyard Kipling, English writer and poet, "The White Man’s Burden"',83:'Rudyard Kipling, English writer and poet, "Tommy"',101:'Le Bien Public, Belgian newspaper; the Second Mexican Empire',102:'United States Congress; the Second Mexican Empire'}
for n in [24,25,27]:A[n]='Henry John Temple, Viscount Palmerston, British Prime Minister'
for n in range(47,54):A[n]='Benjamin Disraeli, Earl of Beaconsfield, British Prime Minister'
for n in range(54,57):A[n]='William Ewart Gladstone, British Prime Minister'
for n in range(97,101):A[n]='Franz Joseph I, Emperor of Austria and King of Hungary'
for n in range(104,107):A[n]='Robert E. Lee, Confederate general'
for n in range(84,88):A[n]=old[f'Author_{n}'].replace('Joseph Rudyard Kipling','Rudyard Kipling')
for k,v in new.items():
 if k.startswith('Author_'):new[k]=re.sub(r'[ \t]+',' ',v).strip()
for n,v in A.items():new[f'Author_{n}']=v
for n in range(1,123):
 k=f'Quote_{n}';v=new[k];v=re.sub(r'\.{3,4}','…',v);v=v.replace('….','…');v=re.sub(r'…(?=[A-Za-z])','… ',v);v=re.sub(r' {2,}',' ',v);new[k]=v
new['Quote_3']=new['Quote_3'].replace('Somsteu must','Somsteu [Theophilus Shepstone] must')
new['Quote_9']=new['Quote_9'].replace("I'm taking about","I'm talking about")
new['Quote_20']=new['Quote_20'].replace('from god','from God')
new['Quote_87']=new['Quote_87'].replace('Pharaoh, "I','Pharaoh, ‘I').replace('to do,"','to do,’')
new['Quote_117']=new['Quote_117'].replace('["Gansu Braves"]','[Gansu Braves]')
# No entries removed or renumbered, and the user-approved Aizu attribution is preserved.
assert new['Author_111']==old['Author_111'];assert set(new)==set(old)
for k,v in new.items():s=re.sub(r'^\{'+re.escape(k)+r'\}.*$',lambda m:'{'+k+'}'+v,s,flags=re.M)
b=bp.read_bytes();pos=8;records=[]
def read():
 global pos
 n=struct.unpack_from('<H',b,pos)[0];pos+=2;v=b[pos:pos+2*n].decode('utf-16le');pos+=2*n;return v
for _ in range(struct.unpack_from('<I',b,4)[0]):k=read();records.append((k,read()))
assert dict(records)==old;tail=b[pos:]
def field(v):d=v.encode('utf-16le');return struct.pack('<H',len(d)//2)+d
out=b[:8]+b''.join(field(k)+field(new[k]) for k,v in records)+tail
p.write_bytes(b'\xff\xfe'+s.replace('\n','\r\n').encode('utf-16le'));bp.write_bytes(out)
b=bp.read_bytes();pos=8;check={}
for _ in range(struct.unpack_from('<I',b,4)[0]):k=read();check[k]=read()
assert check==new and b[pos:]==tail and lp.read_bytes()==(B/lp.name).read_bytes()
changes=[dict(key=k,before=old[k],after=v) for k,v in new.items() if v!=old[k]]
notes='''1|Bloodshed justification is self-contained; remove the distracting and potentially misleading presidential term count.
2|Peace expectation has historical irony, but the statement’s date and British annexation context should be traced before a date is added.
3|Somsteu is opaque to most readers; identify Theophilus Shepstone in square brackets, without rewriting the statement.
4|Fix the broken rank abbreviation; Isandlwana supplies useful context. Exact speaker and occasion still need a stronger source than quotation aggregators.
5|Mahan is unexplained; identify the naval-strategy occasion from a source before adding a topic label. Ellipsis spacing corrected.
6|Correct Bismark to Bismarck and separate the topic from the title with a semicolon.
7|Trim the biography. Which appearance of the Legion prompted the remark needs verification; do not assume Camerone or Magenta.
8|Supply Malakoff, 1855; the French Academy treats this as an attributed remark, so do not imply a verified transcript.
9|Correct taking to talking; the anecdote’s historical attribution remains unverified.
10|The territorial comparison is self-contained; no extra explanatory phrase needed.
11|The omitted object of benevolent assimilation matters: add the Philippines, 1898. The original proclamation supports it.
12|The existing telegram and war clarification is useful and short; leave it.
13|The last-battle referent and exact source should be verified; avoid assigning Cerro Cora merely from inference.
14|Sincere heroic-death maxim, not automatically ironic. Exact attribution needs tracing; no silent removal in a formatting pass.
15|The paradox is intelligible. Do not invent which assassination attempt occasioned it.
16|Govt and Ld are source-style abbreviations. Prefer a checked transcription before expanding them; punctuation of the omission is inconsistent.
17|The comparison is clear and the author role sufficient; no addition needed.
18|The technology/values distinction is self-contained; no additional framing needed.
19|The linguistic comparison is understandable without a dated event label.
20|Capitalize God and remove the presidential term count. Familiar attribution is not proof of authenticity.
21|The political cynicism is self-contained.
22|Standardize role capitalization; the monkey/man comparison is clear.
23|Standardize role capitalization; the deterrence point is clear.
24|Shorten the attribution. The quotation itself explains the diplomatic confusion, though its exact wording remains unverified.
25|Shorten the attribution and normalize the trailing ellipsis; the Russian-policy topic is already explicit.
26|Attacks and capitulation could be military or sexual metaphor. The occasion/source must establish the intended topic before adding a label.
27|Shorten the attribution. The distinction between interests and alliances needs no explanation.
28|Keep the brief smoking clarification: otherwise this vice has no referent.
29|Remove trailing whitespace. Recipient and diplomatic occasion remain unidentified; do not guess Britain merely from Egypt.
30|The imperial order is intelligible as written; a campaign label is not essential.
31|Morny, Persigny and the political labels make this dense, but the final contrast still works. Do not add a paragraph of family history.
32|The installed sentence condenses Marx rather than reproducing the checked opening of The Eighteenth Brumaire. Mark paraphrased in the attribution; the wording is not silently replaced.
33|Trim trailing whitespace; the stated contrast is clear.
34|Credit the jointly authored Communist Manifesto rather than Marx alone.
35|Trim trailing whitespace; add an edition/source only after checking the exact translation.
36|Use the familiar name Paul Doumer and the role relevant to the quotation, rather than stacking a later presidency onto it. Exact quote still unverified.
37|The passage explicitly quotes Franklin within Marx; retain that distinction instead of silently reassigning the whole line.
38|Clear argument, but verify the exact Marx source before treating it as a fully authenticated quotation.
39|Generic motivational maxim: attribution and tonal fit deserve review rather than a new context phrase.
40|The apparent prophecy depends on when it was recorded. An exact source/date is essential to distinguish prediction from retrospective anecdote.
41|Self-contained sardonic remark; source verification is still outstanding.
42|Self-contained analogy; no topic label required.
43|Clear, but the attribution and generic aphoristic character require review.
44|The referent is explicit; no added explanation needed.
45|The rhetoric is understandable. Source checking should distinguish the original 1862 speech from polished later formulations.
46|Self-contained cynicism; do not promote a familiar attribution into a verified one without evidence.
47|Shorten the biography; the Gladstone joke works without explaining their rivalry at length.
48|Shorten the biography. Check whether this is literary dialogue rather than autobiographical testimony.
49|Shorten the biography; the flattery metaphor is clear.
50|Shorten the biography; the opposition argument is clear.
51|Shorten the biography. The apparently paradoxical use of colony needs its source before interpretation or editing.
52|Shorten the biography; the prejudice is expressed plainly enough without explanatory gloss.
53|Shorten the biography; the Ireland argument is self-contained.
54|Shorten the biography; the place and moral comparison are already explicit. Earnest rather than intrinsically ironic.
55|Shorten the biography. A slogan rather than irony, but no clarity repair is needed.
56|Shorten the biography; the foreign/domestic contrast is readily understood.
57|Source title is supplied and the blunder is explicit; strong stand-alone excerpt.
58|Flattened verse produces thundered Stormed without a boundary. Recheck against a chosen edition before repunctuating poetry wholesale.
59|Source title is clear, but the excerpt loses the blunder context and reads as uncomplicated celebration.
60|Source title is clear. Part of the same five-entry poem cluster; review weighting rather than repeat explanatory labels.
61|A sincere exhortation to honour the charge. The poem title may supply historical irony, but the passage alone does not; review alongside 57–60.
62|Exact quote, speaker identity and date were not established. Highest-priority provenance check: do not invent a date for rubber production. Clarification shortened to the actual topic.
63|Terminal question mark does not match the sentence’s declarative syntax; check the original translation before choosing punctuation.
64|The state and claim are explicit; no additional label is needed for the self-exposure.
65|The coercive labour/civilisation juxtaposition is already present.
66|The secrecy/ownership contradiction is self-contained.
67|The defeated paying their conquerors is explicit; no extra explanation needed.
68|Shreds at even the shadow appears corrupt or mistranslated. The same wording occurs on a quotation site, which does not resolve it. Do not guess shrinks or shudders.
69|Clear aspiration, with irony depending on broader knowledge of Leopold’s conduct. His Congo title supplies compact context.
70|It has no identifiable referent. Needs a sourced noun or occasion; otherwise this is a strong removal candidate.
71|The proposed attack and target are explicit. Date and documentary status need checking before labelling it an actual operational order.
72|Replace nickname-only attribution with a role; Sudan is already clarified in the text. Normalize malformed ellipsis.
73|Use the speaker’s role, not only a nickname; the place is explicit.
74|Add besieged at Khartoum: town otherwise lacks a referent. Preserve capitals as apparent source emphasis until transcription is checked.
75|Identify the Summer Palace, 1860, and use British officer rather than a later general’s rank for the event; remove doubled space.
76|Standardize Welsh-American and explorer. Familiar anecdote, not automatically verified or ironic.
77|Normalize malformed ellipsis and attribution; do not expand expedition/date without evidence.
78|Standardize attribution. The campaign behind the numerical claim must be traced before adding context.
79|Fix doubled space and title capitalization. Do not manufacture an immediately-before-assassination date to make the boast ironic.
80|Source title is present; verse punctuation and line flattening should be checked against an edition if revised.
81|Identify Land and Sea Tales (1923). The source continues with mental/physical fitness, including disabled readers: the isolated stanza and its period suitability need review.
82|Add the poem title The White Man’s Burden; this identifies literary imperial rhetoric without explaining away its meaning.
83|Add Tommy as the poem title; the soldier/civilian contradiction is clear in the excerpt.
84|Standardize the author’s name; source title is present. Firearm vocabulary may be acceptable for this game, but this is a long excerpt.
85|Standardize the author’s name. Jingal and Jemadar may impede general readers; avoid packing a glossary into the attribution.
86|Standardize the author’s name. The reprisals are intelligible, but three extracts from one poem create repetition.
87|Standardize the author name and make nested speech punctuation unambiguous. The existing poem title is sufficient.
88|Admission of unpreparedness is clear; exact occasion should be verified before adding an accession date.
89|The scope of all around me depends on a dated source, probably a diary context. Do not infer the abdication occasion without checking.
90|The day has no referent. Identify the celebration from the source or remove; do not guess May Day.
91|The bureaucracy joke is self-contained; exact attribution remains unchecked.
92|His late father is understandable in context; no family-tree explanation needed.
93|The existing recruits clarification is useful. The threat is otherwise self-contained; normalize ellipsis spacing only.
94|Attila is intelligible, but the expedition being addressed is omitted. A verified Hun Speech/China 1900 label would help; leave pending source check.
95|The Tsar is understandable but not named. Verify the correspondence/date before identifying a particular recipient or ruler.
96|The demand is clear; the source/date is needed to establish whether this was a private marginal note or a public order.
97|Shorten the royal title list. This war needs an occasion/date before the quote can stand alone reliably.
98|Shorten the royal title list; the statement is self-contained.
99|Shorten the royal title list. Peace rhetoric is clear, but a particular before-war reversal must not be invented.
100|Shorten the royal title list. The prediction is comprehensible; dating/provenance is needed before calling it prescient.
101|Standardize newspaper capitalization and shorten the repeated topic label; Mexico and monarchy are already explicit.
102|Remove redundant The and on from attribution. Exact resolution/source should establish which chamber acted before the attribution is made more specific.
103|The impending execution is explicit. If adding a date/place, verify the reported final words rather than assume verbatim accuracy.
104|Shorten the rank biography. The paradox works on its own; a battle label is optional, not necessary.
105|Shorten the rank biography. Self-denial is clear; quote-site repetition does not authenticate the attribution.
106|Shorten the rank biography; the constitutional prediction is self-contained.
107|The Civil War is strongly implied by speaker and text; a redundant topic clause is not needed.
108|The rebellion’s referent is readily understood from Lincoln and slavery; no additional explanation necessary.
109|Cuba and independence are explicit; no repeated topic label needed.
110|The foreign attack and defensive demand are clear; chronology should be checked before adding the 1847 bombardment as an occasion.
111|Preserve the user-approved before-defeat wording. The Aizu defeat is sourced; the quotation’s precise date remains unverified.
112|Human Bullets supplies adequate source context. Passage checked in the earlier audit; no additional on clause needed.
113|The contrast is understandable from French Foreign Legion and Annamite; avoid repeating colonial service in the attribution.
114|The bracketed westerners supplies the missing subject. Do not label Boxer-era speech until its source is established.
115|The bracketed Russians supplies the missing referent. No redundant on confronting Russia clause needed.
116|French is clarified within the quotation. The threat stands alone; source check in the earlier pass connects it to 1883.
117|Remove unnecessary quotation marks inside the Gansu Braves bracket. Long operational prose remains a readability concern, not a licence to rewrite the testimony.
118|Keep urging surrender at Hakodate: it turns a vague death remark into intelligible pragmatic advice.
119|The comparison and social hierarchy are explicit; another clause explaining that he is comparing peoples is redundant.
120|Keep Mentana, 1867: it identifies the otherwise unspecified use of the rifles and supplies the intended setting.
121|The imperial/religious self-image is plain; no on neighbours clause needed.
122|The contrast between ethics and science is self-contained; no on modernisation clause needed.'''
N={int(line.split('|',1)[0]):line.split('|',1)[1] for line in notes.splitlines()};assert set(N)==set(range(1,123))
flags={2,4,5,7,9,13,14,15,16,20,24,26,29,31,32,35,36,38,39,40,41,43,45,46,48,51,58,59,60,61,62,63,68,70,71,74,76,78,79,80,81,84,85,86,88,89,90,94,95,96,97,99,100,102,103,105,110,111,114,117}
priority={26,32,62,68,70,81,90,97}
sources={3:'https://emandulo.apc.uct.ac.za/collection/KCAL/1_VOL1/KCAL_JSAVol1_1976_edited_notes_Gxubu_ka_Luduzo_026_p158_p160.pdf',8:'https://www.dictionnaire-academie.fr/article/A9Y0002',11:'https://www.presidency.ucsb.edu/documents/executive-order-132',32:'https://www.marxists.org/archive/marx/works/1852/18th-brumaire/ch01.htm',34:'https://www.marxists.org/archive/marx/works/1848/communist-manifesto/ch01.htm',68:'https://www.goodreads.com/quotes/10753943-a-people-which-is-content-with-its-homeland-and-which',75:'https://www.laphamsquarterly.org/foreigners/wild-plunder',81:'https://www.kiplingsociety.co.uk/children_landsea.htm'}
rows=[]
for n in range(1,123):
 rows.append(dict(id=n,quote=new[f'Quote_{n}'],author=new[f'Author_{n}'],before_quote=old[f'Quote_{n}'],before_author=old[f'Author_{n}'],changed=any(c['key'] in [f'Quote_{n}',f'Author_{n}'] for c in changes),needs_review=n in flags,priority=n in priority,note=N[n],source=sources.get(n),provenance='Targeted checks only; presentation acceptance is not historical authentication.'))
manifest=dict(count=122,changed_authors=sum(c['key'].startswith('Author') for c in changes),changed_quote_strings=sum(c['key'].startswith('Quote') for c in changes),changes=changes,files=[dict(path=str(f),after_sha256=sha(f),backup=str(B/f.name)) for f in [p,bp,lp]],validation='All 122 entries reviewed; text and compiled values agree; binary lookup tail and external lookup unchanged; no removal or renumbering; Aizu wording preserved.')
(B/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');(B/'audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
report=['# Full loading-quote presentation audit','All 122 installed entries reviewed individually. This is a complete formatting and clarity pass, with targeted historical checks—not a claim that every quotation has been authenticated.',f'Applied {manifest["changed_authors"]} attribution edits and {manifest["changed_quote_strings"]} quote-string edits. No deletions or renumbering. Quote-string edits are punctuation/spacing, the taking/talking typo, God capitalization, and the explicit Shepstone clarification. The user-approved Aizu wording is unchanged.','Attributions use name and relevant role, followed by a semicolon only for needed context; literary works use a quoted title. Career summaries, term counts and redundant topic explanations have been shortened. Source-like capitalization and historical vocabulary inside quotations were not globally modernized.','## Highest-priority unresolved items','26: metaphor’s subject unclear; 32: paraphrase, now labelled; 62: rubber quotation/speaker/date unresolved; 68: apparently corrupt shreds wording; 70: it lacks a referent; 81: 1923 source and omitted wider meaning; 90: the day unspecified; 97: this war unspecified. These remain installed pending source-backed decisions.','## All entries','| ID | Action | Finding |','|---:|---|---|']
for r in rows:report.append(f'| {r["id"]} | '+('Presentation edited' if r['changed'] else 'Unchanged')+(' / review' if r['needs_review'] else '')+f' | {r["note"]} |')
report+=['','## Validation',manifest['validation'],'Original files and preceding review page are preserved in this directory. Full before/after values are in manifest.json; all entry assessments are in audit.json. Engine rendering has not been tested.','## Targeted sources']
for n,u in sources.items():report.append(f'- [{n}: checked source]({u})')
(B/'audit.md').write_text('\n\n'.join(report),encoding='utf-8')
parts=['<!doctype html><meta charset="utf-8"><title>All 122 loading quotes — audit</title><style>body{background:#191d20;color:#eee8db;font:17px/1.55 system-ui;max-width:1050px;margin:35px auto;padding:20px}article{border-top:1px solid #555;padding:18px 0}blockquote{font:22px/1.5 Georgia;margin:12px 0}.note{color:#c9d2d7}.flag{color:#f3c28d}a{color:#acd5ef}input,select{padding:10px;background:#30363b;color:white;border:1px solid #777}</style><h1>All 122 loading quotes</h1><p>Complete formatting and clarity audit. Routine corrections installed; unresolved historical or editorial questions are flagged. No quotes removed.</p><p><a href="audit.md">Full findings and sources</a></p><input id="q" placeholder="Search" oninput="f()"><select id="v" onchange="f()"><option value="all">All 122</option><option value="review">Needs review</option><option value="priority">Priority findings</option><option value="edited">Edited entries</option></select>']
for r in rows:
 parts.append(f'<article data-review="{int(r["needs_review"])}" data-priority="{int(r["priority"])}" data-edited="{int(r["changed"])}"><h2>{r["id"]}'+(' · <span class="flag">Needs review</span>' if r['needs_review'] else '')+f'</h2><blockquote>{html.escape(r["quote"])}</blockquote><p>{html.escape(r["author"])}</p><p class="note">{html.escape(r["note"])}</p>')
 if r['changed']:parts.append('<details><summary>Previous text</summary><p>'+html.escape(r['before_quote'])+'</p><p>'+html.escape(r['before_author'])+'</p></details>')
 if r['source']:parts.append('<a href="'+r['source']+'">Checked source</a>')
 parts.append('</article>')
parts.append('<script>function f(){let q=document.getElementById("q").value.toLowerCase(),v=document.getElementById("v").value;document.querySelectorAll("article").forEach(e=>e.hidden=!(e.textContent.toLowerCase().includes(q)&&(v==="all"||e.dataset[v]==="1")))}</script>');(B/'audit.html').write_text(''.join(parts),encoding='utf-8')
# Keep the existing later-quotes review current and link the full audit.
f=R/'retained.html';page=f.read_text(encoding='utf-8')
for n in range(111,123):
 for kind in ['Author','Quote']:page=page.replace(html.escape(old[f'{kind}_{n}']),html.escape(new[f'{kind}_{n}']))
page=page.replace('<h1>Revised loading quotes</h1>','<h1>Revised loading quotes</h1><p><a href="../quote_full_audit_20260925/audit.html">Full audit of all 122 quotes</a></p>');f.write_text(page,encoding='utf-8')
m=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
for x in m['files']:x['after_sha256']=sha(Path(x['path']))
m['full_audit_revision']=str(B/'manifest.json');(R/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:manifest[k] for k in ['count','changed_authors','changed_quote_strings','validation']}))
