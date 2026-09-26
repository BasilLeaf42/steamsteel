import re,json,hashlib,struct,html
from pathlib import Path
from collections import Counter
B=Path('tools/quote_audit_20260925');B.mkdir(exist_ok=True)
p=Path('data/text/quotes.txt');text=p.read_text(encoding='utf-16');d=dict(re.findall(r'^\{([^}]+)\}(.*)$',text,re.M));lines={m.group(1):text[:m.start()].count('\n')+1 for m in re.finditer(r'^\{([^}]+)\}',text,re.M)}
# Editorial judgement is separate from attribution. Retain candidates still require sources.
notes={
111:('Remove','A bare prediction of war. No irony, contradiction or revealing detail.'),
112:('Remove','Earnest advice about worthy living and dying; reads as inspirational warrior philosophy.'),
113:('Context','Useful criticism of obsolete methods, but straightforward practical wisdom rather than irony.'),
114:('Remove','Sincere celebration of national sacrifice and shame at surviving. The loading screen supplies no counterpoint.'),
115:('Remove','Manly death aphorism; presents the warrior ideal at face value.'),
116:('Remove','Commemorative elegy. Sorrow and remembrance are not themselves irony.'),
117:('Retain','Absolute confidence in Aizu victory is a strong dramatic-irony candidate when identified as a boast before defeat; verify wording and occasion.'),
118:('Context','Firearms overturning a social hierarchy fits the game well. Exact historical wording and attribution were not established by targeted searches.'),
119:('Remove','Provocative sword-boast, but its targets and reversal need specialist context. Duplicates the martial bravado theme.'),
120:('Context','Civilian suffering supplies a serious counterweight to glorious-war rhetoric, but the excerpt alone is reportage. Retain at most one Aizu hospital passage with source/date.'),
121:('Context','Rules protecting civilians are not hypocritical merely because they are rules. Needs a documented contradiction to work as irony; do not invent one.'),
122:('Remove','Explicit noble defeat and loyal death. Currently reads as endorsement, not exposure, of the ideal.'),
123:('Remove','Long memento mori; generic earnest life advice, weak strategic relevance and no visible ironic turn. Attribution unresolved.'),
124:('Remove','Consecutive with 125 in Human Bullets; weaker of the pair for this brief. Mostly gruesome description.'),
125:('Retain','The contrast between gallantry and machine-gun destruction captures the game’s industrial-war irony. Verified in the 1907 English edition, pp. 231–232; shorten only with faithful ellipsis.'),
126:('Retain','The doubled burden of colonial identity is revealing and concise. Verify the exact quotation and date; the speaker’s First World War context may require an era exception.'),
127:('Remove','Modest but brave warrior self-portrait; straightforward admiration without an ironic mechanism.'),
128:('Retain','Dynastic face and ancestral legitimacy placed above survival: suitable self-exposing political rhetoric. Verify document and translation.'),
129:('Context','Diplomatic resistance is relevant but not clearly ironic in isolation. Correct county/country only after checking the source.'),
130:('Context','Diplomacy backed by force fits strategy, but a threat is not automatically a failed boast. Needs occasion and outcome.'),
131:('Context','A vivid threat can fit the collection, but do not imply a military reverse without checking the event. Choose this or 135, not both.'),
132:('Context','Accusation of treason by a faction later defeated has potential dramatic irony; too dependent on untranslated domain politics as presented.'),
133:('Context','Modern Chinese firepower could puncture imperial assumptions, but this excerpt is a long operational report. Needs a sharper self-contained selection.'),
134:('Remove','Straightforward heroic battle narrative. No irony on the loading screen.'),
135:('Remove','Second long Liu Yongfu proclamation; repetitive militaristic threat rather than a distinctive ironic observation.'),
136:('Remove','A sincere loyalty/death poem. Romanticises precisely the ideal the intended editorial voice should interrogate.'),
137:('Retain','Dry rejection of futile heroic death. Excellent tonal fit; a secondary source places it in the surrender discussion at Hakodate, 1869. Original wording still needs tracing.'),
138:('Context','Factions denouncing their rivals as usurpers can be revealing, but this passage requires too much Boshin-specific explanation.'),
139:('Context','Good dry humour, but the reported remark belongs to the speaker’s deathbed in 1941, not 1868. Exclude from a strict period-quotation pool or explicitly label the exception.'),
140:('Context','A famous liberal slogan, mainly inspirational on its own. Official Japanese tourism text cautiously says he is said to have shouted it during the 1882 attack.'),
141:('Retain','Diplomatic praise reveals a hierarchy among Asian peoples; useful imperial self-exposure. Verify dispatch/date and keep enough context to preserve that meaning.'),
142:('Retain','Cheerful praise of rifle efficiency is a strong example of military euphemism. Add the Mentana, 1867 context in attribution after source verification.'),
143:('Context','Christian-island rhetoric could reveal imperial self-justification, but the contradiction requires context about Ethiopian expansion. Not an automatic rejection.'),
144:('Remove','Straightforward assertion of sovereignty; little irony or distinctive insight.'),
145:('Context','Peace after annexation can carry historical irony, but the exact English wording is documented here in Clinton’s 2000 speech, not a checked nineteenth-century original. Attribute cautiously.'),
146:('Remove','Earnest hereditary loyalty and obedience. Repeats 122 and 136 without a self-contained reversal.'),
147:('Context','Concise modernisation formula with a useful tension between ethics and technology; not inherently ironic. Verify wording and avoid labelling sincere reform thought hypocrisy.'),
148:('Remove','Filial farewell before death. Elegiac, not ironic.'),
149:('Context','Treating an entire region as enemies can expose political logic, but this long internal report needs context and a checked source.'),
150:('Remove','Factional strategic assessment requires detailed court-politics knowledge; neither punchy nor ironic as presented.'),
151:('Remove','Second Aizu hospital-horror passage; duplicates 120. At most keep one, sourced and shortened.'),
152:('Remove','Earnest patriotic last-stand text; the death alone does not make the sentiment ironic. Claimed diary provenance needs verification.'),
153:('Context','Potential anti-glory counterweight, but graphic injury is not itself irony. Keep at most one of 153/154 and verify the edition, page and translation.'),
154:('Remove','A second clinical mutilation anecdote; redundant with 153 and poorly suited to a short ironic loading quote.'),
155:('Context','A credible modernisation problem, but earnest policy advice. Keep only if the broader editorial brief includes sober strategic observations.'),
156:('Remove','Generic motivational maxim; the weakest fit for a distinctive period-ironic collection.'),
157:('Remove','Blood-as-proof-of-sincerity rhetoric reads as romanticised self-destruction without context. Exact source not established.'),
}
J=set(range(111,126))|{127,132,134,136,137,138,139,140,146,147,148,149,150,151,155,156,157}
sources={
 'human_bullets':dict(url='https://www.gutenberg.org/files/47548/47548-h/47548-h.htm',ids=[124,125],status='Exact passages located in 1907 translation, pp. 231–232. They are consecutive.'),
 'otori':dict(url='https://en.wikipedia.org/wiki/%C5%8Ctori_Keisuke',ids=[137],status='Secondary corroboration and 1869 surrender context, not primary-source authentication.'),
 'hayashi':dict(url='https://en.wikipedia.org/wiki/Hayashi_Tadataka',ids=[139],status='Secondary report of a deathbed remark in 1941. The quote’s mention of 1868 is not its utterance date.'),
 'itagaki':dict(url='https://www.mlit.go.jp/kankocho/jirei_shien/content/001473855.pdf',ids=[140],status='Official interpretation panel describes an attributed remark, using said to have.'),
 'sho_tai':dict(url='https://www.govinfo.gov/content/pkg/WCPD-2000-07-24/pdf/WCPD-2000-07-24.pdf',ids=[145],status='Official record of Clinton quoting the wording in July 2000, p. 1658. Does not authenticate the original attribution to Sho Tai.'),
 'aizu_rules':dict(url='https://en.wikipedia.org/wiki/Aizu_Domain',ids=[121],status='Secondary corroboration of the rules; traces their origin to the 1790s. No evidence of a violation supplied.'),
 'mentana':dict(url='https://en.wikipedia.org/wiki/Chassepot',ids=[142],status='Secondary corroboration of the phrase and Mentana 1867 context; original dispatch not inspected.')
}
rows=[]
for n in range(1,158):
 action,reason=notes.get(n,('Baseline screened','Read for editorial comparison; no individual attribution authentication in this pass.'))
 evidence=[s for s in sources.values() if n in s['ids']]
 rows.append(dict(id=n,quote=d[f'Quote_{n}'],author=d[f'Author_{n}'],quote_line=lines[f'Quote_{n}'],author_line=lines[f'Author_{n}'],word_count=len(d[f'Quote_{n}'].split()),japanese=n in J,ryukyuan=n==145,recommendation=action,editorial_reason=reason,attribution_status=evidence or 'Not authenticated in this pass; not a finding of fabrication.'))
counts=Counter(r['recommendation'] for r in rows[110:]);checks={}
for path in ['data/text/quotes.txt','data/text/quotes.txt.strings.bin','data/descr_quotes_lookup.txt']:checks[path]=hashlib.sha256(Path(path).read_bytes()).hexdigest()
(B/'inventory.json').write_text(json.dumps(dict(scope='All 157 read; detailed editorial audit of 111–157; targeted attribution checks only.',japanese_in_later_47=len(J),ryukyu_in_later_47=1,recommendation_counts=counts,files_sha256=checks,sources=sources,quotes=rows),ensure_ascii=False,indent=2),encoding='utf-8')
intro='''# Loading quote audit — 25 September 2026

Audit only: no game text, compiled strings, lookup files or artwork changed.

## Findings

The clear editorial break begins at **111**, not 120–130. There are **157** quote/author pairs. Of the final **47**, **32 are Japanese (68%)**, with **one further Ryukyuan** entry (145) counted separately. This is a content concentration, not proof of their random display frequency.

The earlier pool establishes a voice of imperial self-exposure, political cynicism, foolish confidence and industrial violence: examples include 4, 11, 28, 64–67, 75, 80 and 87. The later block frequently substitutes sincere martial virtue, loyal death, elegy and motivational advice. A speaker need not intend irony: boast versus outcome, euphemism versus reality, and self-exposing contradictions can all serve the brief. Merely being defeated, brave, dead or graphic does not automatically do so. No invented hypocrisy should be supplied to make an otherwise sincere quotation fit.

This is not a recommendation to remove Japanese voices. **137** is one of the strongest tonal fits. **117, 125, 126, 128, 141 and 142** also merit retention consideration, with the sourcing/context qualifications below.

## Concrete source findings

- **124 and 125** are consecutive passages from Sakurai’s *Human Bullets*, 1907 English edition, pp. 231–232. Prefer 125: its contrast of gallantry with machine-gun destruction suits the intended voice. This is evidence of authenticity in that translation, not of authorial satire.
- **139** is reported as a **1941 deathbed remark**. The year 1868 inside the quotation is misleading if read as its date. Witty, but unsuitable for a strict period-only pool.
- **140** is presented cautiously even by an official Japanese interpretation panel: an attributed saying, not a securely recorded verbatim transcript.
- **145** has this English wording in Clinton’s **2000** speech. That corroborates later repetition, not the authenticity of a nineteenth-century Shō Tai original.
- Exact wording/attribution for **118, 123 and 157** was not established by the targeted searches. Do not call them fabricated on that basis; do not mark them verified either.

## Editorial recommendation

Remove the clearly earnest/redundant candidates first; preserve a small, sourced selection of Japanese political and military voices. Do not simply truncate at a numeric threshold: useful non-Japanese entries also occur later. Retain candidates are editorial recommendations, not automatic authenticity approvals. Context candidates should not remain by default if their irony cannot be made legible in a brief attribution.

'''
intro+='**Later-block triage:** '+', '.join(f'{v} {k.lower()}' for k,v in sorted(counts.items()))+'.\n\n'
intro+='## Entry-by-entry review: 111–157\n\n| ID | Speaker | Recommendation | Reason |\n|---:|---|---|---|\n'
for r in rows[110:]:intro+=f"| {r['id']} | {r['author'].split(',')[0]} | {r['recommendation']} | {r['editorial_reason']} |\n"
intro+='''
## Earlier-pool cautions

The first 110 are not uniformly ironic or automatically authentic. Entries 13–14, 54–56, 58–61, 76 and 102–108 include straightforward patriotism, moral observation, poetry or famous sayings. Apply the same standard in any full revision. The isolated celebratory Light Brigade passages, especially 61, lose the blunder context carried by 57. Entries 64–71 are already an eight-entry Leopold II concentration, and 57–61 split one poem into five slots. Rebalancing the late Japanese material should not exempt these earlier repetitions.

Broad editorial screen is complete for the full text; **this report does not claim a source-by-source authentication of all 157 quotations**. A full provenance pass remains separate from this editorial audit.

## Technical findings

- Text contains 157 quotes and 157 corresponding author labels, with no missing numbered pair.
- The binary string-table header declares 314 entries. Decoding those records recovers all 157 quote/author pairs. Their values match the text except trailing whitespace in Author_29; remaining binary data was not interpreted by this audit.
- `data/descr_quotes_lookup.txt` lists only 1–110. It is stale relative to both text and binary. The supplied earlier in-game screenshot shows quote 123, so this mismatch is **not evidence that the late block is inactive**. Actual selection/weighting logic has not been traced.
- No alternative quotes file was found under data. The launcher copies its text_steamsteel directory, but no quotes file was found there in the inventory.
- Any later edit must address the text, compiled string table and lookup coherently, preserve IDs where practical, and verify the engine’s actual quote selection. Do not repair the lookup blindly as part of an editorial removal.
- No working-tree change was reported for these three files. Their hashes are recorded in inventory.json.

## Checked sources

'''
for key,s in sources.items():intro+=f"- [{key.replace('_',' ').title()}]({s['url']}): {s['status']}\n"
(B/'audit.md').write_text(intro,encoding='utf-8')
parts=['<!doctype html><meta charset="utf-8"><title>Loading quote audit</title><style>body{background:#191d20;color:#eee8db;font:16px/1.55 system-ui;max-width:1050px;margin:30px auto;padding:20px}article{border-top:1px solid #596067;padding:20px 0}blockquote{font:21px/1.5 Georgia;margin:12px 0}input,select{padding:10px;background:#30363b;color:white;border:1px solid #666}a{color:#add3f1}.Remove{color:#ffa897}.Retain{color:#a9dfaf}.Context{color:#f3d18a}</style><h1>Loading quote audit</h1><p>157 entries screened; detailed review of 111–157. No game files changed. 32 of the later 47 are Japanese; one further entry is Ryukyuan.</p><p>Judgement: preserve irony, self-exposing rhetoric and pointed contradictions; avoid treating sincere sacrifice or graphic suffering as automatically ironic.</p><p><a href="audit.md">Full report and technical findings</a></p><input id="search" placeholder="Search ID, speaker or words" oninput="filter()"><select id="decision" onchange="filter()"><option value="">All recommendations</option>Remove</option>Retain</option>Context</select>']
for r in rows[110:]:
 parts.append(f'<article data-action="{r["recommendation"]}"><h2>{r["id"]} · <span class="{r["recommendation"]}">{r["recommendation"]}</span></h2><blockquote>{html.escape(r["quote"])}</blockquote><p>{html.escape(r["author"])}</p><p>{html.escape(r["editorial_reason"])}</p>')
 if isinstance(r['attribution_status'],list):
  for s in r['attribution_status']:parts.append(f'<p><a href="{html.escape(s["url"])}">Source check</a> — {html.escape(s["status"])}</p>')
 else:parts.append('<small>Attribution not authenticated in this pass.</small>')
 parts.append('</article>')
parts.append('<script>function filter(){const q=document.getElementById("search").value.toLowerCase(),a=document.getElementById("decision").value;document.querySelectorAll("article").forEach(e=>e.hidden=!(e.textContent.toLowerCase().includes(q)&&(!a||e.dataset.action===a)))}</script>');(B/'audit.html').write_text(''.join(parts),encoding='utf-8')
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in checks.items());print(dict(counts));print('Audit saved; all game-file hashes unchanged.')
