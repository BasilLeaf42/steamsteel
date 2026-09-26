import json,sys
from pathlib import Path
sys.path.insert(0,'tools/loading_art_replacement_20260922');from research_global_military import api
B=Path('tools/loading_art_replacement_20260922/global_expansion')
for i,q in {106:'Bataille Palikao',107:'Barker Relief Lucknow',108:'Magdala Simpson',109:'Batalla Puebla painting'}.items():
 r=api(dict(action='query',generator='search',gsrsearch=q,gsrnamespace=6,gsrlimit=5,prop='imageinfo',iiprop='url|size|extmetadata'));(B/f'{i}.json').write_text(json.dumps(dict(query=q,pages=list(r.get('query',{}).get('pages',{}).values())),indent=2),encoding='utf-8');print(i,[(j,p['title']) for j,p in enumerate(r.get('query',{}).get('pages',{}).values())],flush=True)
