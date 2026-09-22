import json,re,hashlib,html
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
from research import BASE,clean

ROOT=BASE.parent.parent
extra={
7:('https://www.cartermuseum.org/collection/smoke-signal-1961250','Museum catalog: oil on canvas, 1905; public domain.'),
9:('https://en.wikipedia.org/wiki/Blowing_from_Guns_in_British_India','Catalogued medium: oil on canvas. The artwork is a polemical period painting, not an authenticated depiction of one particular revolt.'),
19:('https://my.tretyakov.ru/app/masterpiece/20707','Tretyakov catalog: canvas, oil; 1881; inventory 2106.'),
26:('https://www.wikiart.org/en/edwin-lord-weeks/the-barge-of-the-maharaja-of-benares','Artwork catalog: oil, canvas; c.1883.'),
41:('https://bonndoc.ulb.uni-bonn.de/xmlui/bitstream/handle/20.500.11811/9199/6297.pdf','University of Bonn dissertation, note 503: Camphausen, 1877, oil on canvas, 68 x 115 cm, Deutsches Historisches Museum.'),
46:('https://en.wikipedia.org/wiki/List_of_paintings_of_Vasily_Vereshchagin','Catalog entry: Nomadic Road in the Alatau Mountains, 1869–1870, canvas glued on canvas, oil, 36.5 x 27 cm, Tretyakov Gallery.')
}

def build():
    rows=json.loads((BASE/'selected_metadata.json').read_text(encoding='utf-8'))
    catalog={}
    for line in (BASE/'catalog.tsv').read_text(encoding='utf-8').splitlines():
        n,title,artist,date,theme,approx=line.split('\t');catalog[int(n)]=dict(title=title,artist=artist,date=date,theme=theme,approximation=approx)
    wd=json.loads((BASE/'evidence/wikidata.json').read_text(encoding='utf-8'))
    original=json.loads((BASE/'archive/original_members.json').read_text())
    runtime={int(Path(r['path']).stem.rsplit('_',1)[1]):r for r in original if Path(r['path']).parent.as_posix()=='data/loading_screen'}
    staged=BASE/'staged';staged.mkdir(exist_ok=True)
    preview=BASE/'previews';preview.mkdir(exist_ok=True)
    result=[]
    assert len(rows)==62 and {r['slot'] for r in rows}==set(range(1,63))
    for row in rows:
        n=row['slot'];page=row['page'];ii=page['imageinfo'][0];meta=ii['extmetadata'];lic=clean(meta['LicenseShortName']['value'])
        assert lic in ['Public domain','CC0'],(n,lic)
        ev=json.loads((BASE/'evidence'/f"{page['pageid']}.json").read_text(encoding='utf-8'))
        wt=ev['revisions'][0]['slots']['main']['*']
        q=wd['slot_entities'].get(str(n));entity=wd['entities'].get(q,{})
        materials=[v['mainsnak'].get('datavalue',{}).get('value',{}).get('id') for v in entity.get('claims',{}).get('P186',[])]
        if 'Q296955' in materials:
            medium_evidence={'url':'https://www.wikidata.org/wiki/'+q,'basis':'Material claim P186 = Q296955 (oil paint), archived in evidence/wikidata.json.'}
        elif re.search(r'technique\|[^\n}]*oil|oil on|oil painting|oil paintings|oilpaint|oil\|',wt,re.I):
            medium_evidence={'url':ii['descriptionurl'],'basis':'Oil medium stated in archived Commons description/category/template.'}
        elif n in extra:
            medium_evidence={'url':extra[n][0],'basis':extra[n][1]}
        else: raise ValueError(f'No verified oil medium: {n}')
        src=BASE/'sources'/f'{n:02}.image'
        download=json.loads((BASE/'sources'/f'{n:02}.download.json').read_text(encoding='utf-8'))
        assert download['title']==page['title']
        assert hashlib.sha256(src.read_bytes()).hexdigest()==download['sha256']
        with Image.open(src) as original_image:
            art=ImageOps.exif_transpose(original_image).convert('RGB')
        source_size=list(art.size);crop=[0,0,art.width,art.height]
        crop_reason='Complete available reproduction; no compositional crop.'
        if n==45:
            crop=[round(art.width*116/1280),round(art.height*119/954),round(art.width*1157/1280),round(art.height*832/954)]
            crop_reason='Remove photographed gold frame and surrounding wall; retain painted canvas.'
        art=art.crop(crop)
        before=Image.open(BASE/'archive'/runtime[n]['archive']).convert('RGBA')
        canvas=before.copy()
        canvas.paste((16,18,17,255),(0,0,1024,490))
        fitted=ImageOps.contain(art,(1016,482),Image.Resampling.LANCZOS)
        x=(1024-fitted.width)//2;y=(490-fitted.height)//2
        canvas.paste(fitted,(x,y))
        draw=ImageDraw.Draw(canvas)
        draw.rectangle((x-1,y-1,x+fitted.width,y+fitted.height),outline=(115,103,80,255))
        assert canvas.crop((0,490,1024,768)).tobytes()==before.crop((0,490,1024,768)).tobytes()
        name=f'Loading_screen_{n}.tga';path=staged/name
        canvas.save(path,compression='tga_rle',orientation=-1)
        canvas.convert('RGB').save(preview/f'{n:02}.jpg',quality=95)
        canvas.crop((0,0,1024,490)).convert('RGB').save(preview/f'{n:02}_art.jpg',quality=95)
        reopened=Image.open(path)
        assert reopened.mode=='RGBA' and reopened.size==(1024,768)
        assert reopened.tobytes()==canvas.tobytes()
        r=dict(slot=n,**catalog[n],medium='Oil painting',medium_verified=True,medium_evidence=medium_evidence,
               commons_file=page['title'],source_url=ii['descriptionurl'],source_revision=ev['revisions'][0]['revid'],
               source_revision_url='https://commons.wikimedia.org/w/index.php?oldid='+str(ev['revisions'][0]['revid']),
               download_url=download['url'],source_sha256=download['sha256'],source_pixel_size=source_size,
               licence=lic,licence_url=meta.get('LicenseUrl',{}).get('value','https://creativecommons.org/publicdomain/mark/1.0/'),
               rights_basis=clean(meta.get('UsageTerms',{}).get('value','')),credit=clean(meta.get('Credit',{}).get('value','')),
               original_artist_metadata=clean(meta.get('Artist',{}).get('value','')),crop_box=crop,crop_reason=crop_reason,
               formatting='Aspect-preserving fit in 1024x490 upper art window; thin neutral frame; original lower 278 rows unchanged.',
               fitted_box=[x,y,x+fitted.width,y+fitted.height],original_runtime_sha256=runtime[n]['sha256'],
               staged_file=name,staged_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),output_size=[1024,768],output_mode='RGBA',
               source_visual_review='passed',final_visual_review='pending')
        result.append(r)
    assert len({r['source_sha256'] for r in result})==62
    (BASE/'source_register.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for start in range(0,62,8):
        sheet=Image.new('RGB',(1040,1120),(32,36,42));d=ImageDraw.Draw(sheet)
        for j,r in enumerate(result[start:start+8]):
            im=Image.open(preview/f"{r['slot']:02}_art.jpg");im.thumbnail((512,245));x=j%2*520;y=j//2*280
            sheet.paste(im,(x,y+28));d.text((x+5,y+5),f"{r['slot']:02} · {r['artist']} · {r['date']}",font=font,fill='white')
        sheet.save(BASE/f'formatted_{start//8+1:02}.jpg',quality=95)
    credits=['# Loading-screen artwork credits','', '62 distinct period oil paintings. Files were retrieved from Wikimedia Commons, whose file-specific rights records identify 58 as public domain and 4 as CC0. This does not treat the Commons website-wide text licence as an image licence. Artist, image source and the particular Commons file revision are recorded below.','', 'Reproductions are fitted without stretching or generative edits. The original loading-text area is preserved. Subject substitutions are explicit; these paintings are not asserted to depict the same individuals or events as the removed illustrations.','']
    for r in result:
        credits.extend([f"## Screen {r['slot']}: {r['title']}",f"{r['artist']}, {r['date']}. {r['medium']}.",f"Source: [{r['commons_file']}]({r['source_revision_url']}). Rights: [{r['licence']}]({r['licence_url']}).",f"Medium evidence: [{r['medium_evidence']['basis']}]({r['medium_evidence']['url']})",f"Theme: {r['theme']}. {r['approximation']}",f"Format: {r['formatting']} {r['crop_reason']}",''])
    (BASE/'ARTWORK_CREDITS.md').write_text('\n\n'.join(credits),encoding='utf-8')
    css='body{background:#161b1d;color:#ece5d7;font:17px/1.55 system-ui;max-width:1120px;margin:35px auto;padding:0 20px}a{color:#c5dceb}article{background:#222a2c;padding:22px;margin:24px 0;border:1px solid #5a5347}h1{font:42px Georgia,serif}h2{font:26px Georgia,serif;margin:0}img{width:100%;height:auto}small{color:#b9b4a8}button,input{padding:10px;background:#303a3e;color:white;border:1px solid #897e68;margin:5px}button{cursor:pointer}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}.old{opacity:.9}details{margin:15px 0}'
    page=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Period oil paintings — loading-screen collection</title><style>'+css+'</style><body><h1>Period oil paintings</h1><p>62 individually sourced replacements · 58 public domain · 4 CC0 · 1024 × 768 RGBA TGA</p><p>Period artwork from 1807–1908, with documented thematic substitutions. Click a replacement to inspect its complete game-format texture. This gallery preserves the earlier screen for comparison.</p><p><a href="ARTWORK_CREDITS.md">Full artwork credits</a> · <a href="source_register.json">Source and formatting register</a></p><p><input id="search" placeholder="Find an artist, theme or screen" oninput="filter()" size="42"><button onclick="document.querySelectorAll(\'.old\').forEach(e=>e.hidden=!e.hidden)">Toggle previous artwork</button></p>']
    for r in result:
        n=r['slot'];key=json.loads((ROOT/'tools/loading_art_audit_20260922/findings.json').read_text(encoding='utf-8'))[n-1]['id']
        page.append(f'<article data-search="{html.escape(str(n)+" "+r["title"]+" "+r["artist"]+" "+r["theme"]).lower()}"><h2>{n:02} · {html.escape(r["title"])}</h2><p>{html.escape(r["artist"])} · {html.escape(r["date"])} · {r["licence"]}</p><div class="pair"><div class="old"><small>Previous illustration</small><img loading="lazy" src="../loading_art_audit_20260922/{key}_art.png"></div><div><small>Replacement oil painting</small><a href="previews/{n:02}.jpg"><img loading="lazy" src="previews/{n:02}_art.jpg"></a></div></div><p>{html.escape(r["approximation"])}</p><a href="{html.escape(r["source_url"])}">Painting and rights record on Commons</a><details><summary>Formatting and verification</summary><p>{html.escape(r["formatting"])} {html.escape(r["crop_reason"])}</p><p>Oil medium verified. Complete source metadata and file revision retained in the register.</p></details></article>')
    page.append('<script>function filter(){let q=document.getElementById("search").value.toLowerCase();document.querySelectorAll("article").forEach(e=>e.hidden=!e.dataset.search.includes(q))}</script></body></html>')
    (BASE/'gallery.html').write_text(''.join(page),encoding='utf-8')
    print('Staged and structurally verified 62 distinct oil paintings; visual approval still required.')

if __name__=='__main__':build()
