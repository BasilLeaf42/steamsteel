import json,time,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw
B=Path('tools/loading_art_replacement_20260922/global_expansion');(B/'sources').mkdir(exist_ok=True)
choices=[(0,1),(2,1),(44,0),(45,3),(9,3),(10,0),(11,3),(11,4),(16,0),(49,1),(49,3)]
for q,j in choices:
 p=json.loads((B/f'{q}.json').read_text(encoding='utf-8'))['pages'][j];ii=p['imageinfo'][0];dest=B/'sources'/f'{q}_{j}.image'
 if not dest.exists():
  for attempt in range(4):
   try:
    u=ii['url']+('&download=1' if attempt else '');dest.write_bytes(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read());break
   except Exception as e:print(q,str(e),flush=True);time.sleep(8)
 if dest.exists():print(q,j,Image.open(dest).size,flush=True)
for start in range(0,len(choices),8):
 sheet=Image.new('RGB',(1200,1200),'#222222');d=ImageDraw.Draw(sheet)
 for k,(q,j) in enumerate(choices[start:start+8]):
  im=Image.open(B/'sources'/f'{q}_{j}.image');im.thumbnail((590,260));x=k%2*600;y=k//2*300;sheet.paste(im,(x,y+30));d.text((x,y),f'{q}_{j}',fill='white')
 sheet.save(B/f'candidates_{start}.jpg')
