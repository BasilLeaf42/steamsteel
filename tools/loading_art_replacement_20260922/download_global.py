import json,urllib.request,time
from pathlib import Path
from PIL import Image,ImageDraw
B=Path(__file__).resolve().parent/'global_expansion';choices=json.loads((B/'choices.json').read_text());records=[]
for q,j,region,country in choices:
 p=json.loads((B/f'{q}.json').read_text(encoding='utf-8'))['pages'][j];ii=p['imageinfo'][0];dest=B/'sources'/f'{q}_{j}.image';base=ii['url'].split('?')[0]
 tail=base.split('/wikipedia/commons/')[1];fn=tail.rsplit('/',1)[1];u='https://upload.wikimedia.org/wikipedia/commons/thumb/'+tail+'/1280px-'+fn if ii['width']>1280 else base
 if not dest.exists():
  for attempt in range(3):
   try:dest.write_bytes(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'SteamSteelHistoricalArt/1.0'}),timeout=30).read());break
   except Exception as e:print(q,str(e),flush=True);time.sleep(12)
  time.sleep(2)
 if dest.exists():
  im=Image.open(dest);records.append(dict(query=q,index=j,region=region,country=country,source=p,local=str(dest),download_url=u,download_size=im.size));print(q,j,im.size,flush=True)
(B/'downloaded.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
for start in range(0,len(records),8):
 sheet=Image.new('RGB',(1200,1200),'#222222');d=ImageDraw.Draw(sheet)
 for k,r in enumerate(records[start:start+8]):
  im=Image.open(r['local']).convert('RGB');im.thumbnail((590,260));x=k%2*600;y=k//2*300;sheet.paste(im,(x,y+30));d.text((x,y),str(r['query'])+'_'+str(r['index'])+' '+r['country'],fill='white')
 sheet.save(B/f'sources_review_{start//8}.jpg',quality=94)
