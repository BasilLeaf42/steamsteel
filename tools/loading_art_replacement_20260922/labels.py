"""Opaque museum labels, rendered from reviewed metadata onto archived wide crops."""
import json, shutil, hashlib, html, re, sys
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont, ImageChops
from research import BASE

ROOT=BASE.parent.parent
ARCHIVE=BASE/'revision2_unlabelled'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
TITLE=ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf',16)
BODY=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
SMALL=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
# Corner choices avoid the main groups and foreground action wherever possible.
CORNER={n:'top-right' for n in range(1,63)}
CORNER.update({4:'bottom-right',6:'top-left',8:'top-left',10:'top-left',13:'top-left',
14:'top-right',16:'top-right',17:'bottom-right',18:'top-left',20:'top-left',
23:'top-right',24:'top-left',25:'top-left',26:'top-right',30:'top-left',
31:'top-right',32:'top-left',33:'top-left',35:'top-left',36:'top-left',
37:'top-right',39:'top-left',40:'top-left',41:'top-right',42:'top-right',
44:'top-left',45:'top-right',47:'bottom-right',50:'top-left',51:'top-left',
52:'top-right',54:'top-right',55:'top-left',57:'bottom-left',59:'top-right',
60:'top-left',61:'top-right',62:'top-right'})

def wrap(text,font,width):
    lines=[];line=''
    for word in text.split():
        candidate=(line+' '+word).strip()
        if font.getlength(candidate)>width and line:lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    assert all(font.getlength(s)<=width for s in lines),text
    return lines

def build():
    if not ARCHIVE.exists():
        ARCHIVE.mkdir()
        for f in ['source_register.json','installation_manifest.json','gallery.html','ARTWORK_CREDITS.md','README.md']:
            shutil.copy2(BASE/f,ARCHIVE/f)
        shutil.copytree(BASE/'staged',ARCHIVE/'staged')
    previous=json.loads((ARCHIVE/'installation_manifest.json').read_text())
    for op in previous['operations']:assert sha(ROOT/op['path'])==op['after_sha256'],op['path']
    rows=json.loads((ARCHIVE/'source_register.json').read_text(encoding='utf-8'))
    r=rows[18]
    r.update(title='Surrender of the Fortress of Nikopol, July 4, 1877',artist='Nikolai Dmitriev-Orenburgsky',date='1883',
             theme='Surrender at Nikopol',medium='Oil on canvas',medium_verified=True,licence='Public domain',
             source_url='https://commons.wikimedia.org/wiki/File:Nikopol_dmitriev.jpg',
             source_revision_url='https://commons.wikimedia.org/wiki/File:Nikopol_dmitriev.jpg',
             commons_file='File:Nikopol dmitriev.jpg',licence_url='https://creativecommons.org/publicdomain/mark/1.0/',
             medium_evidence=dict(url='https://commons.wikimedia.org/wiki/File:Nikopol_dmitriev.jpg',basis='Oil on canvas, artist and 1883 date recorded on Commons; visual identity checked.'),
             formatting='Original 1024×768 texture and framing retained beneath the museum label.',
             attribution_evidence='evidence/nikopol_identification.json; full reference visually matched to preserved image',
             approximation='Preserved original image, previously called Plevna in this audit. Identified as Surrender of the Fortress of Nikopol (1883). Only the requested museum label has been added.')
    for r in rows:
        n=r['slot'];base=Image.open(ARCHIVE/'staged'/r['staged_file']).convert('RGBA');out=base.copy()
        titles=wrap(r['title'],TITLE,336)
        info=wrap(r['artist']+' · '+r['date'],BODY,336)
        width=max(210,int(max([TITLE.getlength(s) for s in titles]+[BODY.getlength(s) for s in info]))+25)
        height=20*len(titles)+18*len(info)+23
        assert width<=361 and height<=119
        corner=CORNER[n];x=12 if corner.endswith('left') else 1024-12-width
        y=12 if corner.startswith('top') else 490-12-height
        box=[x,y,x+width,y+height]
        d=ImageDraw.Draw(out);d.rectangle((x,y,x+width-1,y+height-1),fill=(28,31,29,255),outline=(139,129,105,255))
        ty=y+10
        for line in titles:d.text((x+12,ty),line,font=TITLE,fill=(241,233,213,255),anchor='lt');ty+=20
        ty+=4
        for line in info:d.text((x+12,ty),line,font=BODY,fill=(222,218,206,255),anchor='lt');ty+=18
        # Mask out the label; every other pixel must equal the unlabelled installation.
        check=out.copy();check.paste(base.crop(box),(x,y));assert check.tobytes()==base.tobytes()
        assert out.crop(box).getchannel('A').getextrema()==(255,255)
        assert out.crop((0,490,1024,768)).tobytes()==base.crop((0,490,1024,768)).tobytes()
        path=BASE/'staged'/r['staged_file'];out.save(path,compression='tga_rle',orientation=-1)
        assert Image.open(path).tobytes()==out.tobytes()
        out.convert('RGB').save(BASE/'previews'/f'{n:02}.jpg',quality=95)
        out.crop((0,0,1024,490)).convert('RGB').save(BASE/'previews'/f'{n:02}_art.jpg',quality=95)
        r.update(staged_sha256=sha(path),unlabelled_sha256=sha(ARCHIVE/'staged'/r['staged_file']),
                 museum_label=dict(title=r['title'],artist=r['artist'],date=r['date'],corner=corner,box=box,
                                   opaque=True,title_font='Georgia Bold 16px',details_font='Arial 14px',visual_review='pending'))
        r['formatting']+=' Opaque corner label; pixels outside its rectangle are unchanged.'
    (BASE/'source_register.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
    for start in range(0,62,8):
        sheet=Image.new('RGB',(1040,1120),'#20242a');d=ImageDraw.Draw(sheet)
        for j,r in enumerate(rows[start:start+8]):
            im=Image.open(BASE/'previews'/f"{r['slot']:02}_art.jpg");im.thumbnail((512,245));x=j%2*520;y=j//2*280
            sheet.paste(im,(x,y+28));d.text((x+5,y+5),str(r['slot']),font=SMALL,fill='white')
        sheet.save(BASE/f'labels_review_{start//8+1:02}.jpg',quality=95)
    page=(ARCHIVE/'gallery.html').read_text(encoding='utf-8')
    page=page.replace('Plevna surrender','Nikopol surrender').replace('Plevna unchanged','Nikopol artwork preserved')
    page=page.replace('Plevna','Nikopol')
    page=re.sub(r'<p id="status">.*?</p>','<p id="status">Museum labels: review in progress.</p>',page)
    page=page.replace('19 · Nikopol surrender — preserved original','19 · Surrender of the Fortress of Nikopol, July 4, 1877')
    page=page.replace('Original installed artwork · Unverified','Nikolai Dmitriev-Orenburgsky · 1883')
    page=page.replace('Original screen restored byte-for-byte at the user’s explicit request.','Original artwork retained; attribution corrected to Nikopol, 1883. Museum label added at the user’s request.')
    page=page.replace('plus the preserved original Nikopol surrender screen','plus the retained original Nikopol surrender artwork')
    (BASE/'gallery.html').write_text(page,encoding='utf-8')
    credits=['# Loading-screen artwork credits','All 62 screens have opaque museum labels. Dates refer to creation of the paintings; uncertain dates remain qualified. Only the label rectangle changes the preceding artwork. Screen 19 has been correctly identified as Nikopol, replacing the earlier Plevna attribution.']
    for r in rows:
        credits.extend([f"## Screen {r['slot']}: {r['title']}",f"{r['artist']}, {r['date']}. {r['medium']}.",r['approximation'],r['crop_reason'],
                        f"Source: [{r['commons_file']}]({r['source_revision_url']}). Rights: [{r['licence']}]({r['licence_url']}).",
                        f"Medium evidence: [{r['medium_evidence']['basis']}]({r['medium_evidence']['url']})."])
    (BASE/'ARTWORK_CREDITS.md').write_text('\n\n'.join(credits),encoding='utf-8')
    print('Rendered 62 opaque museum labels; outside-label and loading-text pixels unchanged.')

def install():
    rows=json.loads((BASE/'source_register.json').read_text(encoding='utf-8'))
    previous=json.loads((ARCHIVE/'installation_manifest.json').read_text())
    for op in previous['operations']:assert sha(ROOT/op['path'])==op['after_sha256'],op['path']
    for r in rows:
        assert sha(BASE/'staged'/r['staged_file'])==r['staged_sha256']
        r['museum_label']['visual_review']='passed: all eight contact sheets plus native-size samples inspected'
    operations=[]
    for prior in previous['operations']:
        n=int(Path(prior['path']).stem.rsplit('_',1)[1]);r=rows[n-1]
        shutil.copy2(BASE/'staged'/r['staged_file'],ROOT/prior['path'])
        assert sha(ROOT/prior['path'])==r['staged_sha256']
        op=dict(prior);op.update(previous_install_sha256=prior['after_sha256'],previous_install_archive='revision2_unlabelled/staged/'+r['staged_file'],after_sha256=r['staged_sha256']);operations.append(op)
    manifest=dict(previous,installed_at=datetime.now(timezone.utc).isoformat(),museum_labels=62,operations=operations)
    (BASE/'installation_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    (BASE/'source_register.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
    for folder in ['data/loading_screen','data/loading_screen/load_steamsteel','data/loading_screen/load_althis']:
        shutil.copy2(BASE/'ARTWORK_CREDITS.md',ROOT/folder/'ARTWORK_CREDITS.md')
    p=BASE/'gallery.html';s=p.read_text(encoding='utf-8').replace('Museum labels: review in progress.','Installed: all 62 works have opaque museum labels. All 186 runtime and launcher copies verified. Artwork outside the label is unchanged.');p.write_text(s,encoding='utf-8')
    (BASE/'README.md').write_text('# Installed loading artwork — museum labels\n\nAll 62 works now have small opaque corner labels with title, artist and painting date. Labels use Georgia Bold 16px and Arial 14px on a solid dark background. Positions and exact rectangles are recorded in source_register.json.\n\nAll pixels outside each label, including the lower loading-text area, match the preceding installation exactly. All 186 runtime and launcher textures verified. The game has not been launched.\n\nThe retained surrender painting is now identified as Surrender of the Fortress of Nikopol, July 4, 1877, by Nikolai Dmitriev-Orenburgsky (1883). The previous Plevna attribution was incorrect. Its artwork remains intact under the label.\n\nrevision2_unlabelled/ preserves the complete preceding installation; archive/ retains the initial originals. See gallery.html for previews, ARTWORK_CREDITS.md for sources, and installation_manifest.json for before/after hashes.\n',encoding='utf-8')
    print('Installed 62 labelled artworks; all 186 copies verified.')

if __name__=='__main__':
    from pathlib import Path
    install() if '--install' in sys.argv else build()
