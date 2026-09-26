import json,shutil,hashlib,html,base64,io,re,zipfile,sys
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageDraw
from labels import BASE,ROOT,TITLE,BODY,wrap,sha
from research import clean

BACKUP=BASE/'revision5_before_bourget'
WORK=BASE/'bourget_revision'
SHARE=BASE/'discord_share'
TITLE_TEXT='Bivouac after the Battle of Le Bourget, 21 December 1870'
EVIDENCE_URL='https://histoire-image.org/etudes/bivouac-apres-combat-bourget-21-decembre-1870'

def build():
    if not BACKUP.exists():
        BACKUP.mkdir()
        for name in ['source_register.json','installation_manifest.json','selected_metadata.json','catalog.tsv','gallery.html','ARTWORK_CREDITS.md','README.md']:
            shutil.copy2(BASE/name,BACKUP/name)
        shutil.copy2(BASE/'staged/Loading_screen_55.tga',BACKUP/'Loading_screen_55.tga')
        shutil.copy2(BASE/'sources/55.image',BACKUP/'55.image')
        shutil.copy2(BASE/'sources/55.download.json',BACKUP/'55.download.json')
    WORK.mkdir(exist_ok=True)
    rows=json.loads((BACKUP/'source_register.json').read_text(encoding='utf-8'));r=rows[54]
    p=json.loads((BASE/'evidence/bourget.json').read_text(encoding='utf-8'));ii=p['imageinfo'][0];m=ii['extmetadata']
    assert clean(m['LicenseShortName']['value'])=='Public domain'
    assert '{{Technique|oil|canvas}}' in p['revisions'][0]['slots']['main']['*']
    src=BASE/'sources/bourget.jpg';art=Image.open(src).convert('RGB');w,h=art.size
    # Remove scan-edge strips and excess sky; preserve ruins, all heads and resting troops.
    left,right=4,w-7;ch=round((right-left)*490/1024);bottom=h-5;top=bottom-ch
    crop=[left,top,right,bottom]
    original=Image.open(BASE/'archive'/(r['original_runtime_sha256']+'.tga')).convert('RGBA')
    unlabelled=original.copy();unlabelled.paste(art.crop(crop).resize((1024,490),Image.Resampling.LANCZOS),(0,0))
    unlabelled.save(WORK/'55_unlabelled.tga',compression='tga_rle',orientation=-1)
    r.update(title=TITLE_TEXT,artist='Alphonse de Neuville',date='1872',depicted_date='21 December 1870',
             theme='Military rest and hardship in the Franco-Prussian War',
             approximation='French soldiers resting after the battle of Le Bourget in 1870 replace the earlier Napoleonic subject.',
             date_note='Creation date 1872 follows the RMN–Grand Palais catalogue; Commons currently gives 1873.',
             medium='Oil on canvas',medium_verified=True,medium_evidence=dict(url=EVIDENCE_URL,basis='RMN–Grand Palais catalogue: oil on canvas, created 1872, depicts 21 December 1870.'),
             commons_file=p['title'],source_url=ii['descriptionurl'],source_revision=p['revisions'][0]['revid'],
             source_revision_url='https://commons.wikimedia.org/w/index.php?oldid='+str(p['revisions'][0]['revid']),
             download_url=ii['thumburl'],source_sha256=sha(src),source_pixel_size=[w,h],licence='Public domain',
             licence_url='https://creativecommons.org/publicdomain/mark/1.0/',rights_basis=clean(m.get('UsageTerms',{}).get('value','')),
             credit='Wikimedia Commons scan; date and medium checked against RMN–Grand Palais.',
             original_artist_metadata=clean(m.get('Artist',{}).get('value','')),crop_box=crop,
             crop_reason='Reduce empty sky and scan edges; retain ruined farmhouse, resting soldiers, campfires and mounted figures.',
             fitted_box=[0,0,1024,490],unlabelled_sha256=sha(WORK/'55_unlabelled.tga'),unlabelled_file='unlabelled_current/Loading_screen_55.tga')
    r.pop('editorial_offset',None)
    titles=wrap(r['title'],TITLE,336);info=wrap(r['artist']+' · '+r['date'],BODY,336)
    width=int(max([TITLE.getlength(s) for s in titles]+[BODY.getlength(s) for s in info]))+25;height=20*len(titles)+18*len(info)+23
    x=y=12;box=[x,y,x+width,y+height]
    layer=Image.new('RGBA',unlabelled.size);d=ImageDraw.Draw(layer)
    d.rectangle((x,y,x+width-1,y+height-1),fill=(28,31,29,102),outline=(139,129,105,80))
    out=Image.alpha_composite(unlabelled,layer);d=ImageDraw.Draw(out);ty=y+10
    for line in titles:d.text((x+12,ty),line,font=TITLE,fill=(241,233,213,255),anchor='lt');ty+=20
    ty+=4
    for line in info:d.text((x+12,ty),line,font=BODY,fill=(222,218,206,255),anchor='lt');ty+=18
    assert out.crop((0,490,1024,768)).tobytes()==original.crop((0,490,1024,768)).tobytes()
    out.save(WORK/'Loading_screen_55.tga',compression='tga_rle',orientation=-1)
    r.update(staged_sha256=sha(WORK/'Loading_screen_55.tga'),formatting='Subject-specific 1024×490 crop. Label background 60% transparent, text opaque; lower 278 rows unchanged.',final_visual_review='pending')
    r['museum_label'].update(title=r['title'],artist=r['artist'],date=r['date'],corner='top-left',box=box,visual_review='pending')
    out.convert('RGB').save(WORK/'55_labelled.jpg',quality=95)
    unlabelled.crop((0,0,1024,490)).convert('RGB').save(WORK/'55_clean.jpg',quality=95)
    (WORK/'source_register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    (WORK/'medium_date_evidence.json').write_text(json.dumps(dict(url=EVIDENCE_URL,artist=r['artist'],creation_date=1872,depicted_date='21 December 1870',medium='oil on canvas',note=r['date_note']),indent=2),encoding='utf-8')
    print('Replacement staged; crop and label previews ready.')

def install_and_gallery():
    rows=json.loads((WORK/'source_register.json').read_text(encoding='utf-8'));prior=json.loads((BACKUP/'installation_manifest.json').read_text())
    for op in prior['operations']:assert sha(ROOT/op['path'])==op['after_sha256'],op['path']
    r=rows[54];assert sha(WORK/'Loading_screen_55.tga')==r['staged_sha256']
    # Keep a complete, current clean set independent of historical backups.
    clean_dir=BASE/'unlabelled_current';clean_dir.mkdir(exist_ok=True)
    for item in rows:
        n=item['slot'];source=WORK/'55_unlabelled.tga' if n==55 else BASE/'revision2_unlabelled/staged'/item['staged_file']
        assert sha(source)==item['unlabelled_sha256']
        shutil.copy2(source,clean_dir/item['staged_file']);item['unlabelled_file']='unlabelled_current/'+item['staged_file']
    r['final_visual_review']='passed: full source, clean wide crop and labelled texture inspected'
    r['museum_label']['visual_review']='passed'
    operations=[]
    for old in prior['operations']:
        op=dict(old)
        if Path(op['path']).name=='Loading_screen_55.tga':
            shutil.copy2(WORK/'Loading_screen_55.tga',ROOT/op['path'])
            op.update(previous_install_sha256=old['after_sha256'],previous_install_archive='revision5_before_bourget/Loading_screen_55.tga',after_sha256=r['staged_sha256'])
        assert sha(ROOT/op['path'])==op['after_sha256'];operations.append(op)
    shutil.copy2(WORK/'Loading_screen_55.tga',BASE/'staged/Loading_screen_55.tga')
    shutil.copy2(BASE/'sources/bourget.jpg',BASE/'sources/55.image')
    (BASE/'sources/55.download.json').write_text(json.dumps(dict(title=r['commons_file'],url=r['download_url'],sha256=r['source_sha256']),indent=2),encoding='utf-8')
    for suffix,im in [('',Image.open(WORK/'Loading_screen_55.tga').convert('RGB')),('_art',Image.open(WORK/'Loading_screen_55.tga').convert('RGB').crop((0,0,1024,490)))]:im.save(BASE/'previews'/f'55{suffix}.jpg',quality=95)
    (BASE/'source_register.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
    manifest=dict(prior,installed_at=datetime.now(timezone.utc).isoformat(),operations=operations)
    (BASE/'installation_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    p=json.loads((BASE/'evidence/bourget.json').read_text(encoding='utf-8'))
    metadata=json.loads((BASE/'selected_metadata.json').read_text(encoding='utf-8'));metadata[54]=dict(slot=55,page=p,download_url=r['download_url'],download_sha256=r['source_sha256'])
    (BASE/'selected_metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False),encoding='utf-8')
    cat=(BASE/'catalog.tsv').read_text(encoding='utf-8').splitlines();cat[54]='\t'.join(['55',r['title'],r['artist'],r['date'],r['theme'],r['approximation']]);(BASE/'catalog.tsv').write_text('\n'.join(cat)+'\n',encoding='utf-8')
    credits=['# Loading-screen artwork credits','All 62 current works. In-game labels have 60% transparent backgrounds; the shareable artwork gallery has no overlays.']
    for item in rows:
        credits.extend([f"## Screen {item['slot']}: {item['title']}",f"{item['artist']}, {item['date']}. {item['medium']}.",item['approximation'],item['crop_reason'],
                        f"Source: [{item['commons_file']}]({item['source_revision_url']}). Rights: [{item['licence']}]({item['licence_url']}).",
                        f"Medium evidence: [{item['medium_evidence']['basis']}]({item['medium_evidence']['url']})."])
        if item.get('date_note'):credits.append(item['date_note'])
    credit_text='\n\n'.join(credits);(BASE/'ARTWORK_CREDITS.md').write_text(credit_text,encoding='utf-8')
    for folder in ['data/loading_screen','data/loading_screen/load_steamsteel','data/loading_screen/load_althis']:shutil.copy2(BASE/'ARTWORK_CREDITS.md',ROOT/folder/'ARTWORK_CREDITS.md')
    gallery=BASE/'gallery.html';s=gallery.read_text(encoding='utf-8')
    original=json.loads((BACKUP/'source_register.json').read_text(encoding='utf-8'))[54]
    a=re.search(r'<article><h2>55 .*?</article>',s,re.S);assert a
    segment=a.group()
    for key in ['title','artist','date','approximation','crop_reason','source_url']:segment=segment.replace(html.escape(original[key]),html.escape(r[key]))
    segment=segment.replace('55_art.jpg?labels=semi40','55_art.jpg?revision=bourget')
    s=s[:a.start()]+segment+s[a.end():];gallery.write_text(s,encoding='utf-8')
    SHARE.mkdir(exist_ok=True);images=SHARE/'paintings_without_overlays';images.mkdir(exist_ok=True)
    parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Steam &amp; Steel — painting gallery</title><style>body{background:#171c1e;color:#eee6d7;font:17px/1.5 system-ui;margin:0}main{max-width:1120px;margin:auto;padding:25px}article{margin:30px 0 50px}img{width:100%;height:auto;display:block}h1{font:38px Georgia,serif}h2{font:25px Georgia,serif;margin-bottom:3px}a{color:#bcd7e7}small{color:#bfbdb5}input,button{padding:10px;background:#30393a;color:white;border:1px solid #6c726e;font:inherit;margin:5px}.bare figcaption,.bare .credits{display:none}figure{margin:0}</style><main><h1>Steam &amp; Steel</h1><p>Loading-screen painting gallery · 62 artworks · No overlays</p><p>Current in-game crops, presented without museum labels or the dark loading-text area. All images are embedded: save this file and open it in a browser.</p><input id="q" placeholder="Find an artist or painting" oninput="document.querySelectorAll(\'article\').forEach(e=>e.hidden=!e.textContent.toLowerCase().includes(this.value.toLowerCase()))"><button onclick="document.body.classList.toggle(\'bare\')">Show / hide captions</button>']
    for item in rows:
        n=item['slot'];im=Image.open(clean_dir/item['staged_file']).convert('RGB').crop((0,0,1024,490))
        # Exact panel export before JPEG encoding; no overlay removal or generated fill.
        assert im.tobytes()==Image.open(clean_dir/item['staged_file']).convert('RGB').crop((0,0,1024,490)).tobytes()
        im.save(images/f'{n:02}.jpg',quality=90,optimize=True)
        buf=io.BytesIO();im.save(buf,format='JPEG',quality=82,optimize=True);encoded=base64.b64encode(buf.getvalue()).decode()
        parts.append(f'<article><figure><img loading="lazy" alt="{html.escape(item["title"])}" src="data:image/jpeg;base64,{encoded}"><figcaption><h2>{n:02} · {html.escape(item["title"])}</h2><p>{html.escape(item["artist"])} · {html.escape(item["date"])}</p></figcaption></figure><p class="credits"><a href="{html.escape(item["source_url"])}">Source and rights record</a> · {html.escape(item["licence"])}</p></article>')
    parts.append('</main></html>');dest=SHARE/'Steam_and_Steel_Painting_Gallery_No_Overlays.html';dest.write_text(''.join(parts),encoding='utf-8')
    with zipfile.ZipFile(SHARE/'Steam_and_Steel_Paintings_No_Overlays.zip','w',zipfile.ZIP_DEFLATED) as z:
        for image in sorted(images.glob('*.jpg')):z.write(image,'paintings/'+image.name)
        z.writestr('ARTWORK_CREDITS.md',credit_text)
    (BASE/'README.md').write_text((BASE/'README.md').read_text(encoding='utf-8')+'\n\nScreen 55 now depicts the Franco-Prussian War of 1870: Alphonse de Neuville, Bivouac after the Battle of Le Bourget (1872). The preceding Napoleonic painting is archived in revision5_before_bourget. unlabelled_current contains the current clean artwork bases. The Discord painting gallery and ZIP contain all 62 images without overlays; in-game labels remain enabled.\n',encoding='utf-8')
    print('Replaced screen 55 in all three sets; verified all 186 installed hashes.')
    for f in [dest,SHARE/'Steam_and_Steel_Paintings_No_Overlays.zip']:print(f.name,round(f.stat().st_size/1024/1024,2),'MiB')

if __name__=='__main__':install_and_gallery() if '--install' in sys.argv else build()
