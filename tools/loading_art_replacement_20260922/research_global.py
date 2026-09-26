import json,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'tools/loading_art_replacement_20260922');from research import api,clean
B=Path('tools/loading_art_replacement_20260922/global_expansion');B.mkdir(exist_ok=True)
queries=['Velasco valley Mexico','Jose Maria Velasco railway','Rugendas Lima','Ignacio Merino Peru','Prilidiano Pueyrredon countryside','Blanes Paraguay','Pedro Lira founding Santiago','Rugendas Brazil landscape','Thomas Baines South Africa','Thomas Baines Victoria Falls','Thomas Baines Damaraland','Thomas Baines Zulu','Theodore Ethiopia painting','Henry Salt Abyssinia','Louis Gustave Binger painting','Hildebrandt Zanzibar','Gustav Bauernfeind Jaffa','Kamol molk painting','Chlebowski Ottoman','Pasini market Persia','Oman Muscat painting','James Rattray Afghanistan','Daniell India painting','Weeks India market','Senerat Ceylon painting','Raden Saleh landscape','Payen Java painting','Juan Luna Philippines','Felix Resurreccion Hidalgo landscape','Siam painting 19th century','Tonkin painting 19th century','China oil painting harbour','Tingqua painting','Portinari coffee','Ciceri Madagascar','Roberts Nubia painting','Bridgman Algeria painting','Gerome Arnaut','Liotard Istanbul','Dinet market','Baines gold fields','Church Ecuador','Velasco Oaxaca','Reza Abbasi Qajar painting']
def run(q):
 f=B/(str(queries.index(q))+'.json')
 if f.exists():return
 r=api(dict(action='query',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=5,prop='imageinfo',iiprop='url|size|extmetadata'));f.write_text(json.dumps(dict(query=q,pages=list(r.get('query',{}).get('pages',{}).values())),indent=2),encoding='utf-8');print(queries.index(q),q,flush=True)
with ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(run,queries))
lines=[]
for i,q in enumerate(queries):
 r=json.loads((B/f'{i}.json').read_text(encoding='utf-8'));lines.append('\n'+str(i)+' '+q)
 for j,p in enumerate(r['pages']):
  ii=p['imageinfo'][0];m=ii['extmetadata'];lines.append(f"{j}: {p['title']} | {ii['width']}x{ii['height']} | "+clean(m.get('LicenseShortName',{}).get('value',''))+' | '+clean(m.get('DateTimeOriginal',{}).get('value',''))[:80])
(B/'summary.txt').write_text('\n'.join(lines),encoding='utf-8')
