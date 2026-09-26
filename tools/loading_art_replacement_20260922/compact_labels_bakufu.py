import json,shutil,sys,io,base64,html,zipfile,re
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageOps,ImageDraw,ImageFont
from labels import BASE,ROOT,sha,wrap
from research import clean
BACKUP=BASE/'revision6_before_compact'
WORK=BASE/'compact_revision'
TITLE=ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf',13)
BODY=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)

def build():
    if not BACKUP.exists():
        BACKUP.mkdir()
        for name in ['source_register.json','installation_manifest.json','ARTWORK_CREDITS.md','gallery.html']:
            shutil.copy2(BASE/name,BACKUP/name)
        shutil.copytree(BASE/'staged',BACKUP/'staged')
        shutil.copytree(BASE/'unlabelled_current',BACKUP/'unlabelled')
    rows=json.loads((BACKUP/'source_register.json').read_text(encoding='utf-8'))
    prior=json.loads((BACKUP/'installation_manifest.json').read_text())
    for op in prior['operations']:assert sha(ROOT/op['path'])==op['after_sha256'],op['path']
    for folder in ['staged','clean','previews','display','display_clean']:(WORK/folder).mkdir(parents=True,exist_ok=True)
    p=json.loads((BASE/'evidence/bakufu.json').read_text(encoding='utf-8'));ii=p['imageinfo'][0];m=ii['extmetadata']
    assert clean(m['LicenseShortName']['value'])=='Public domain'
    rows.append(dict(slot=63,title='Bakufu Troops near Mount Fuji',artist='Jules Brunet',date='1867',
        theme='Japanese troops in 1867',approximation='Additional artwork explicitly supplied by the user.',
        medium='Painting; exact medium not specified by the source',medium_verified=False,
        medium_evidence=dict(url=ii['descriptionurl'],basis='Commons identifies a painting by Jules Brunet, 1867; specific medium unverified.'),
        commons_file=p['title'],source_url=ii['descriptionurl'],source_revision=p['revisions'][0]['revid'],
        source_revision_url='https://commons.wikimedia.org/w/index.php?oldid='+str(p['revisions'][0]['revid']),
        download_url=ii['url'],source_sha256=sha(BASE/'sources/63.image'),source_pixel_size=[2990,1909],
        licence='Public domain',licence_url='https://creativecommons.org/publicdomain/mark/1.0/',
        rights_basis='PD-Art; PD-old-auto-expired, artist died 1911',credit='User-supplied Commons reproduction.',
        crop_box=[0,700,2990,1896],crop_reason='Focus on the foreground troops, camp and pine branches. The wider game panel crops away the distant mountain peak.',
        museum_label=dict(corner='top-left'),staged_file='Loading_screen_63.tga',output_size=[1024,768],output_mode='RGBA',
        source_visual_review='passed'))
    audit=[]
    for r in rows:
        n=r['slot']
        if n==19:
            base=Image.open(BACKUP/'unlabelled'/r['staged_file']).convert('RGBA')
            art=base.crop((0,0,1024,490)).convert('RGB')
            display=art.resize((1250,500),Image.Resampling.LANCZOS,box=(0,0,1024,409.6)).convert('RGBA')
            audit.append(dict(slot=n,check='Original artwork retained; lower foreground cropped to correct the measured game stretch.',display_ratio=2.5))
        else:
            src=BASE/'sources'/f'{n:02}.image';assert sha(src)==r['source_sha256']
            art=ImageOps.exif_transpose(Image.open(src)).convert('RGB')
            a,b,c,d=r['crop_box'];w=c-a;h=d-b;before_error=abs((w/h)/(1024/490)-1)*100
            if w/h>2.5:
                delta=(w-h*2.5)/2;a+=delta;c-=delta
            else:
                if n in {7,9,14,18,22,23,29,43,44,46,47,57}:
                    d=b+w/2.5
                    r['crop_reason']=r.get('crop_reason','')+' Wider display crop anchored at original top to preserve heads or architecture, following visual review.'
                else:
                    delta=(h-w/2.5)/2;b+=delta;d-=delta
            box=[a,b,c,d];sx=1250/(c-a);sy=500/(d-b)
            assert abs(sx-sy)<1e-12 and 0<=a<c<=art.width and 0<=b<d<=art.height
            base=Image.new('RGBA',(1024,768),(16,18,17,255)) if n==63 else Image.open(BACKUP/'unlabelled'/r['staged_file']).convert('RGBA')
            # Fractional box with one shared scale factor; no integer crop rounding.
            display=art.resize((1250,500),Image.Resampling.LANCZOS,box=tuple(box)).convert('RGBA')
            r['crop_box']=box;r['source_pixel_size']=list(art.size);r['display_crop_ratio']=2.5
            audit.append(dict(slot=n,previous_ratio_error_percent=before_error,scale_x=sx,scale_y=sy,ratio_error_percent=0.0))
        display.save(WORK/'display_clean'/f'{n:02}.png')
        base.paste(display.resize((1024,490),Image.Resampling.LANCZOS),(0,0))
        clean_path=WORK/'clean'/r['staged_file'];base.save(clean_path,compression='tga_rle',orientation=-1)
        titles=wrap(r['title'],TITLE,272);details=wrap(r['artist']+' · '+r['date'],BODY,272)
        width=max(160,int(max([TITLE.getlength(s) for s in titles]+[BODY.getlength(s) for s in details]))+17)
        height=len(titles)*16+len(details)*14+17
        corner=r['museum_label']['corner'];x=10 if corner.endswith('left') else 1240-width;y=10 if corner.startswith('top') else 490-height
        box=[x,y,x+width,y+height];layer=Image.new('RGBA',display.size);draw=ImageDraw.Draw(layer)
        draw.rectangle((x,y,x+width-1,y+height-1),fill=(28,31,29,102),outline=(139,129,105,60))
        out=Image.alpha_composite(display,layer);draw=ImageDraw.Draw(out);ty=y+7
        for line in titles:draw.text((x+8,ty),line,font=TITLE,fill=(241,233,213,255),anchor='lt');ty+=16
        ty+=3
        for line in details:draw.text((x+8,ty),line,font=BODY,fill=(222,218,206,255),anchor='lt');ty+=14
        masked=out.copy();masked.paste(display.crop(box),(x,y));assert masked.tobytes()==display.tobytes()
        out.save(WORK/'display'/f'{n:02}.png')
        base.paste(out.resize((1024,490),Image.Resampling.LANCZOS),(0,0));out=base
        if n!=63:assert out.crop((0,490,1024,768)).tobytes()==Image.open(BACKUP/'unlabelled'/r['staged_file']).convert('RGBA').crop((0,490,1024,768)).tobytes()
        dst=WORK/'staged'/r['staged_file'];out.save(dst,compression='tga_rle',orientation=-1)
        assert Image.open(dst).tobytes()==out.tobytes()
        r.update(staged_sha256=sha(dst),unlabelled_sha256=sha(clean_path),unlabelled_file='unlabelled_current/'+r['staged_file'],
                 formatting='Uniformly scaled 1250×500 display artwork, horizontally precompensated into the 1024×490 game panel for the measured 2.50:1 display area. Compact 40%-opacity label. Footer unchanged.',final_visual_review='pending')
        r['museum_label'].update(title=r['title'],artist=r['artist'],date=r['date'],box=box,title_font='Georgia Bold 13px',details_font='Arial 11px',
             coordinate_space='1250x500 display panel',opaque=False,background_opacity=.4,text_opacity=1,border_opacity=60/255,visual_review='pending')
        out.convert('RGB').save(WORK/'previews'/f'{n:02}.jpg',quality=95)
        Image.open(WORK/'display'/f'{n:02}.png').convert('RGB').save(WORK/'previews'/f'{n:02}_art.jpg',quality=95)
    (WORK/'source_register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    report=dict(display_panel_ratio=2.5,screenshot_panel_ratio=2876/1150,engine_stretch_compensation=2.5/(1024/490),panel_ratio=1024/490,texture_ratio=1024/768,old_max_ratio_error_percent=max(r.get('previous_ratio_error_percent',0) for r in audit),
                method='Fractional source crop; identical horizontal and vertical scale factors.',preserved_original_slot=19,
                saved_game_resolution=[1280,768],saved_widescreen=0,game_display_verified='Measured supplied screenshot; post-change in-game capture not yet verified',
                display_note='A 1024×768 texture expanded to 1280×768 would be 25% wider. This is a conditional calculation, not a measured engine result. User screenshot confirms about 20% horizontal stretch. Textures now compensate for the measured 2.50:1 panel. No display-setting changes made.',items=audit)
    (WORK/'aspect_ratio_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    for start in range(0,63,8):
        sheet=Image.new('RGB',(1040,1120),'#20242a');draw=ImageDraw.Draw(sheet)
        for j,r in enumerate(rows[start:start+8]):
            im=Image.open(WORK/'previews'/f"{r['slot']:02}_art.jpg");im.thumbnail((512,245));x=j%2*520;y=j//2*280;sheet.paste(im,(x,y+28));draw.text((x,y),str(r['slot']),fill='white')
        sheet.save(WORK/f'review_{start//8+1:02}.jpg',quality=94)
    print('Staged 63 screens; compact labels and mathematically uniform scaling. Native/crop review ready.')

def install():
    rows=json.loads((WORK/'source_register.json').read_text(encoding='utf-8'));prior=json.loads((BACKUP/'installation_manifest.json').read_text())
    for op in prior['operations']:assert sha(ROOT/op['path'])==op['after_sha256']
    for folder in ['data/loading_screen','data/loading_screen/load_steamsteel','data/loading_screen/load_althis']:assert not (ROOT/folder/'Loading_screen_63.tga').exists()
    for r in rows:assert sha(WORK/'staged'/r['staged_file'])==r['staged_sha256']
    operations=[];by_path={op['path']:op for op in prior['operations']}
    for r in rows:
        r['final_visual_review']='passed';r['museum_label']['visual_review']='passed: contact sheets and full-size examples inspected'
        for folder in ['data/loading_screen','data/loading_screen/load_steamsteel','data/loading_screen/load_althis']:
            rel=folder+'/'+r['staged_file'];old=by_path.get(rel)
            shutil.copy2(WORK/'staged'/r['staged_file'],ROOT/rel);assert sha(ROOT/rel)==r['staged_sha256']
            op=dict(old) if old else dict(path=rel,before_sha256=None,archive=None)
            op.update(previous_install_sha256=old['after_sha256'] if old else None,previous_install_archive='revision6_before_compact/staged/'+r['staged_file'] if old else None,after_sha256=r['staged_sha256']);operations.append(op)
        shutil.copy2(WORK/'staged'/r['staged_file'],BASE/'staged'/r['staged_file']);shutil.copy2(WORK/'clean'/r['staged_file'],BASE/'unlabelled_current'/r['staged_file'])
        for suffix in ['', '_art']:shutil.copy2(WORK/'previews'/f"{r['slot']:02}{suffix}.jpg",BASE/'previews'/f"{r['slot']:02}{suffix}.jpg")
    (BASE/'source_register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    (BASE/'installation_manifest.json').write_text(json.dumps(dict(prior,installed_at=datetime.now(timezone.utc).isoformat(),screens=63,copies_verified=189,museum_labels=63,operations=operations),indent=2),encoding='utf-8')
    shutil.copy2(WORK/'aspect_ratio_audit.json',BASE/'aspect_ratio_audit.json')
    export(rows)
    print('Installed 63 screens in all three sets: 189 hashes verified. Refreshed galleries and full-resolution export.')

def export(rows):
    share=BASE/'discord_share';pngs=share/'Full_Resolution_Cropped_With_Overlays';pngs.mkdir(exist_ok=True)
    credits=['# Artwork credits',f'{len(rows)} works. Compact labels use 13px titles and 11px details; backgrounds remain 60% transparent. Media and rights are recorded individually. Artwork has been cropped and resized; labelled editions also add a museum caption.']
    for r in rows:
        credits.extend([f"## {r['slot']:02}: {r['title']}",f"{r['artist']}, {r['date']}. {r['medium']}.",r['approximation'],f"[Source]({r['source_url']}) · {r['licence']}."])
        if r.get('credit'):credits.append('Credit: '+r['credit'])
        if r.get('licence_url'):credits.append('[Licence / rights declaration]('+r['licence_url']+').')
        credits.append(r.get('changes','Changes: cropped, resized and captioned for the loading screen. Unlabelled editions omit the caption.'))
        if r.get('date_note'):credits.append(r['date_note'])
    credit='\n\n'.join(credits);(BASE/'ARTWORK_CREDITS.md').write_text(credit,encoding='utf-8')
    for folder in ['data/loading_screen','data/loading_screen/load_steamsteel','data/loading_screen/load_althis']:shutil.copy2(BASE/'ARTWORK_CREDITS.md',ROOT/folder/'ARTWORK_CREDITS.md')
    css='body{background:#171c1e;color:#eee6d7;font:17px/1.5 system-ui;margin:0}main{max-width:1120px;margin:auto;padding:25px}article{margin:30px 0 50px}img{width:100%;height:auto;display:block}h1{font:38px Georgia,serif}h2{font:24px Georgia,serif}a{color:#bcd7e7}input,button{padding:10px;margin:5px}.bare .caption{display:none}'
    index=[]
    for labelled in [False,True]:
        head=f'{len(rows)} artworks · '+('Compact overlays' if labelled else 'No overlays')
        parts=[f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Steam &amp; Steel — Artwork</title><style>{css}</style><main><h1>Steam &amp; Steel</h1><p>{head}. Aspect-preserving 2.50:1 crops, corrected for the game display.</p><input placeholder="Search" oninput="document.querySelectorAll(\'article\').forEach(e=>e.hidden=!e.textContent.toLowerCase().includes(this.value.toLowerCase()))"><button onclick="document.body.classList.toggle(\'bare\')">Show / hide captions</button>']
        for r in rows:
            folder='staged' if labelled else 'unlabelled_current';im=Image.open(WORK/('display' if labelled else 'display_clean')/f"{r['slot']:02}.png").convert('RGB')
            if labelled:
                dest=pngs/f"{r['slot']:02}.png";im.save(dest,optimize=True);assert Image.open(dest).tobytes()==im.tobytes()
                index.append(dict(file=dest.name,title=r['title'],artist=r['artist'],date=r['date'],source=r['source_url']))
            else:im.save(share/'paintings_without_overlays'/f"{r['slot']:02}.jpg",quality=82,optimize=True)
            preview=im.copy();preview.thumbnail((900,431));buf=io.BytesIO();preview.save(buf,format='JPEG',quality=78,optimize=True)
            rights=html.escape(r['licence'])
            if r.get('licence_url'):rights=f'<a href="{html.escape(r["licence_url"])}">{rights}</a>'
            attribution=html.escape(r.get('credit','')) if r['licence'].startswith('CC BY') else ''
            region=html.escape(r.get('region',''))
            parts.append(f'<article><img loading="lazy" alt="{html.escape(r["title"])}" src="data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}"><div class="caption"><h2>{r["slot"]:02} · {html.escape(r["title"])}</h2><p>{html.escape(r["artist"])} · {html.escape(r["date"])} · {region}</p><a href="{html.escape(r["source_url"])}">Source</a> · {rights}<p>{attribution} Cropped and resized'+('; caption added.' if labelled else '.')+'</p></div></article>')
        parts.append('</main></html>');page=''.join(parts)
        name='Steam_and_Steel_Painting_Gallery_Compact_Overlays.html' if labelled else 'Steam_and_Steel_Painting_Gallery_No_Overlays.html'
        (share/name).write_text(page,encoding='utf-8')
        if labelled:(BASE/'gallery.html').write_text(page,encoding='utf-8')
    (pngs/'Artwork_Index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
    (pngs/'README.txt').write_text(f'{len(rows)} 1250 x 500 PNG artwork panels in corrected display proportions, with compact labels and 60% transparent backgrounds. Sources are cropped and resized to this output size; source resolution varies. See ARTWORK_CREDITS.md for attribution and licences.\n',encoding='utf-8')
    (pngs/'ARTWORK_CREDITS.md').write_text(credit,encoding='utf-8')
    (share/'paintings_without_overlays'/'ARTWORK_CREDITS.md').write_text(credit,encoding='utf-8')
    for name,folder,pattern in [('Steam_and_Steel_Full_Resolution_Cropped_With_Overlays.zip',pngs,'*.png'),('Steam_and_Steel_Paintings_No_Overlays.zip',share/'paintings_without_overlays','*.jpg')]:
        with zipfile.ZipFile(share/name,'w',zipfile.ZIP_DEFLATED) as z:
            for f in sorted(folder.glob(pattern)):z.write(f,f.name)
            z.writestr('ARTWORK_CREDITS.md',credit)
        with zipfile.ZipFile(share/name) as z:assert z.testzip() is None and len(z.namelist())==len(rows)+1
    (BASE/'README.md').write_text(f'# Current loading artwork\n\n{len(rows)} screens with compact overlays: 13px Georgia Bold title, 11px Arial details, 40% opacity background. Jules Brunet’s Bakufu Troops near Mount Fuji (1867) is added as screen 63.\n\nAspect audit: the largest previous rounding error was 0.1045%; all generated crop boxes now use equal horizontal and vertical scale factors. The original Nikopol artwork is retained with a wider crop. The saved game resolution is 1280×768 with widescreen=0; the supplied screenshot measures a 2.50:1 artwork area. Textures compensate for this measured stretch; post-change engine rendering has not been verified. No display settings were changed. See aspect_ratio_audit.json.\n\nAll {len(rows)*3} installed copies match. Sources, metadata, prior artwork and manifests are retained. revision6_before_compact preserves the preceding version. Current shareable galleries and full-resolution PNG ZIPs are in discord_share/.\n',encoding='utf-8')

if __name__=='__main__':install() if '--install' in sys.argv else build()
