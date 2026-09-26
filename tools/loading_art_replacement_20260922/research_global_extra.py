import json,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'tools/loading_art_replacement_20260922');from research import api
B=Path('tools/loading_art_replacement_20260922/global_expansion')
qs={44:'Pueyrredon alto campo',45:'Blanes gauchos',46:'Reza Abbasi Qajar',47:'Kamal ol molk',48:'Osman Hamdi mosque',49:'Raden Saleh Javanese landscape',50:'Payen Buitenzorg',51:'Juan Luna paseo',52:'Lorenzo Guerrero river',53:'Rattray Kandahar',54:'Hildebrandt Siam',55:'Louis Choris Hawaii',56:'Ernest Griset Abyssinia',57:'Frederick Goodall Nubia',58:'Eugene Fromentin falconers',59:'Baines Gold Fields',60:'Gustave Guillaumet Laghouat',61:'Louis Mouchot Tangier',62:'Charton Guayaquil',63:'Church Cotopaxi',64:'Agustin Arrieta market',65:'Pancho Fierro market',66:'Nicanor Plaza Valparaiso',67:'Pedro Subercaseaux plaza',68:'Hugo Pratt Ceylon',69:'Marianne North Ceylon',70:'Marianne North Borneo',71:'Marianne North Chile',72:'Edwin Weeks Ahmedabad',73:'Vasily Vereshchagin Taj Mahal',74:'Charles Landelle Algeria'}
def run(item):
 i,q=item;f=B/f'{i}.json'
 if f.exists():return
 r=api(dict(action='query',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=4,prop='imageinfo',iiprop='url|size|extmetadata'));f.write_text(json.dumps(dict(query=q,pages=list(r.get('query',{}).get('pages',{}).values())),indent=2),encoding='utf-8');print(i,flush=True)
with ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(run,qs.items()))
