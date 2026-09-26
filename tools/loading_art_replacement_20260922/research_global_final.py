import json,sys
from pathlib import Path
sys.path.insert(0,'tools/loading_art_replacement_20260922');from research import api
B=Path('tools/loading_art_replacement_20260922/global_expansion')
qs={75:'Kamal Mirror Hall',76:'Lozano Cundiman',77:'Hildebrandt Penang',78:'Bauernfeind Damascus',79:'Pasini caravan',80:'Rattray Kabul',81:'Bauernfeind Jerusalem',82:'Hildebrandt Zanzibar',83:'Willem Hekking Suriname',84:'Church Jamaica',85:'Martin Tovar Caracas',86:'Monvoisin Chile',87:'Pedro Americo Independence death'}
for i,q in qs.items():
 f=B/f'{i}.json'
 if f.exists():continue
 try:r=api(dict(action='query',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=4,prop='imageinfo',iiprop='url|size|extmetadata'));f.write_text(json.dumps(dict(query=q,pages=list(r.get('query',{}).get('pages',{}).values())),indent=2),encoding='utf-8');print(i,flush=True)
 except Exception as e:print(i,type(e).__name__,flush=True)
