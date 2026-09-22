from research import BASE,api,clean
import json,re,time

selection=json.loads((BASE/'selection.json').read_text())
pages=[]
dest=BASE/'evidence';dest.mkdir(exist_ok=True)
for r in selection:
    p=json.loads((BASE/'search'/f"{r['search']:02}.json").read_text())['pages'][r['index']]
    pages.append((r['slot'],p))
missing=[(n,p) for n,p in pages if not (dest/f"{p['pageid']}.json").exists()]
for start in range(0,len(missing),20):
    batch=missing[start:start+20]
    result=api(dict(action='query',pageids='|'.join(str(p['pageid']) for n,p in batch),prop='revisions',rvprop='content|timestamp|ids',rvslots='main'))
    for p in result['query']['pages'].values():
        (dest/f"{p['pageid']}.json").write_text(json.dumps(p,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Evidence batch',start//20+1,flush=True);time.sleep(3)
lines=[]
for n,p in pages:
    r=json.loads((dest/f"{p['pageid']}.json").read_text(encoding='utf-8'))
    wt=r['revisions'][0]['slots']['main']['*']
    evidence=[line.strip() for line in wt.splitlines() if re.search(r'medium\s*=|technique\s*=|oil|huile|óleo|öl|масло|olieverf|canvas|wikidata\s*=',line,re.I)]
    lines.append(f"{n}: {p['title']}\n"+'\n'.join(evidence)[:1000])
(BASE/'medium_evidence.txt').write_text('\n\n'.join(lines),encoding='utf-8')
print('Saved evidence for',len(pages))
