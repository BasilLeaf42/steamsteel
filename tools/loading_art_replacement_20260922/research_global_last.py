import json,sys
from pathlib import Path
sys.path.insert(0,'tools/loading_art_replacement_20260922');from research import api
B=Path('tools/loading_art_replacement_20260922/global_expansion')
for i,q in {88:'Hildebrandt Hong Kong',89:'China harbour painting 1870',90:'Guerard Tower Hill',91:'Almeida Junior caipira',92:'Kamal goldsmith Baghdad'}.items():
 f=B/f'{i}.json'
 if f.exists():continue
 r=api(dict(action='query',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=4,prop='imageinfo',iiprop='url|size|extmetadata'));f.write_text(json.dumps(dict(query=q,pages=list(r.get('query',{}).get('pages',{}).values())),indent=2),encoding='utf-8');print(i,flush=True)
