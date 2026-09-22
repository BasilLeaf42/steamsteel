import json, urllib.request, urllib.parse, time, hashlib, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageOps,ImageDraw
from research import BASE,UA,api,clean

def fetch(row):
    n=row['slot']; ii=row['page']['imageinfo'][0]
    d=BASE/'sources';d.mkdir(exist_ok=True)
    path=d/f'{n:02}.image'
    side=d/f'{n:02}.download.json'
    url=ii.get('thumburl',ii['url']).split('?')[0]
    if '/thumb/' not in url:
        rel=ii['url'].split('/wikipedia/commons/')[1].split('?')[0]
        filename=rel.rsplit('/',1)[1]
        width=960 if ii['width']>960 else 330
        url='https://thumb.wikimedia.org/wikipedia/commons/thumb/'+rel+'/'+str(width)+'px-'+filename
    if path.exists() and side.exists():
        old=json.loads(side.read_text(encoding='utf-8'))
        if old['title']!=row['page']['title']:
            path.rename(d/f"{n:02}_superseded_{hashlib.sha256(path.read_bytes()).hexdigest()[:10]}.image")
        else: url=old['url']
    elif path.exists():
        with Image.open(path) as prior:
            if prior.width==ii['width']:url=ii['url'].split('?')[0]
    if not path.exists():
        for attempt in range(3):
            try:
                req=urllib.request.Request(url,headers={'User-Agent':UA})
                with urllib.request.urlopen(req,timeout=25) as response: data=response.read()
                path.write_bytes(data)
                break
            except Exception as exc:
                print('Download retry',n,str(exc)[:100],flush=True)
                if attempt==2: raise
                time.sleep(10+attempt*10)
        time.sleep(2)
    with Image.open(path) as im:
        im=ImageOps.exif_transpose(im).convert('RGB')
        im.thumbnail((1800,1400))
        im.save(d/f'{n:02}.jpg',quality=95)
    row['download_url']=url
    row['download_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    side.write_text(json.dumps({'title':row['page']['title'],'url':url,'sha256':row['download_sha256']},indent=2),encoding='utf-8')
    print('Downloaded',n,flush=True)
    return row

def run():
    selection=json.loads((BASE/'selection.json').read_text(encoding='utf-8'))
    rows=[]
    for r in selection:
        pages=json.loads((BASE/'search'/f"{r['search']:02}.json").read_text(encoding='utf-8'))['pages']
        row=dict(r,page=pages[r['index']]);rows.append(row)
    with ThreadPoolExecutor(max_workers=2) as pool: rows=list(pool.map(fetch,rows))
    (BASE/'selected_metadata.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
    for start in range(0,len(rows),12):
        sheet=Image.new('RGB',(1500,1100),'#20242a');d=ImageDraw.Draw(sheet)
        for j,r in enumerate(rows[start:start+12]):
            im=Image.open(BASE/'sources'/f"{r['slot']:02}.jpg");im.thumbnail((490,240));x=j%3*500;y=j//3*275
            sheet.paste(im,(x+(490-im.width)//2,y+28));d.text((x+8,y+5),f"Slot {r['slot']}: "+r['page']['title'][5:65],fill='white')
        sheet.save(BASE/f'candidates_{start//12+1:02}.jpg',quality=93)
    print('Prepared',len(rows),'paintings')

if __name__=='__main__':run()
