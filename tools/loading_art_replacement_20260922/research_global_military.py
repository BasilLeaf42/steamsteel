import json,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'tools/loading_art_replacement_20260922');import urllib.request,urllib.parse
def api(params):
 params.update(format='json',formatversion=2)
 params['gsrsearch']=params['gsrsearch'].replace(' filetype:bitmap','')
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as resp:r=json.load(resp)
 if 'query' in r:r['query']['pages']={str(i):p for i,p in enumerate(r['query'].get('pages',[]))}
 return r

B=Path('tools/loading_art_replacement_20260922/global_expansion')
qs={93:'Pedro Americo Avai',94:'Patricio Ramos Puebla',95:'Somerscales Angamos',96:'Fripp Isandlwana',97:'Simpson Magdala',98:'Raden Saleh Diponegoro',99:'Palikao painting',100:'Lundgren Lucknow',101:'Somerscales Iquique',102:'Cenni Adwa',103:'Blanes Rancagua',104:'Battle Tamanieh Wollen',105:'Battle Omdurman Sutherland'}
def run(item):
 i,q=item;f=B/f'{i}.json'
 if f.exists():return
 r=api(dict(action='query',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=4,prop='imageinfo',iiprop='url|size|extmetadata'));f.write_text(json.dumps(dict(query=q,pages=list(r.get('query',{}).get('pages',{}).values())),indent=2),encoding='utf-8');print(i,flush=True)
with ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(run,qs.items()))
