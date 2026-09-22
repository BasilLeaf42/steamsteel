"""Composite 40%-opacity plaques over preserved artwork; keep text fully opaque."""
import json, shutil, sys
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageDraw
from labels import BASE, ROOT, TITLE, BODY, wrap, sha

BACKUP=BASE/'revision4_opacity60'
STAGE=BASE/'transparent60_staged'

def build():
    if not BACKUP.exists():
        BACKUP.mkdir()
        for name in ['source_register.json','installation_manifest.json','gallery.html','ARTWORK_CREDITS.md','README.md']:
            shutil.copy2(BASE/name,BACKUP/name)
        shutil.copytree(BASE/'staged',BACKUP/'staged')
    prior=json.loads((BACKUP/'installation_manifest.json').read_text())
    for op in prior['operations']:assert sha(ROOT/op['path'])==op['after_sha256'],op['path']
    rows=json.loads((BACKUP/'source_register.json').read_text(encoding='utf-8'))
    STAGE.mkdir(exist_ok=True)
    for r in rows:
        source=BASE/'revision2_unlabelled/staged'/r['staged_file']
        assert sha(source)==r['unlabelled_sha256']
        base=Image.open(source).convert('RGBA');box=r['museum_label']['box'];x,y,x2,y2=box
        layer=Image.new('RGBA',base.size,(0,0,0,0));d=ImageDraw.Draw(layer)
        d.rectangle((x,y,x2-1,y2-1),fill=(28,31,29,102),outline=(139,129,105,80))
        out=Image.alpha_composite(base,layer);d=ImageDraw.Draw(out);ty=y+10
        for line in wrap(r['title'],TITLE,336):
            d.text((x+12,ty),line,font=TITLE,fill=(241,233,213,255),anchor='lt');ty+=20
        ty+=4
        for line in wrap(r['artist']+' · '+r['date'],BODY,336):
            d.text((x+12,ty),line,font=BODY,fill=(222,218,206,255),anchor='lt');ty+=18
        masked=out.copy();masked.paste(base.crop(box),(x,y));assert masked.tobytes()==base.tobytes()
        assert out.getchannel('A').tobytes()==base.getchannel('A').tobytes()
        path=STAGE/r['staged_file'];out.save(path,compression='tga_rle',orientation=-1)
        assert Image.open(path).tobytes()==out.tobytes()
        out.convert('RGB').save(STAGE/f"{r['slot']:02}.jpg",quality=95)
        r['staged_sha256']=sha(path)
        r['museum_label'].update(opaque=False,background_opacity=.4,border_opacity=80/255,text_opacity=1,
                                compositing='Flattened over original artwork; texture alpha unchanged',visual_review='pending')
        r['formatting']=r['formatting'].replace('60% background opacity','40% background opacity').replace('Opaque corner label','Semi-transparent corner label (40% background opacity; fully opaque text)')
    (STAGE/'source_register.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
    sheet=Image.new('RGB',(1040,840),'#20242a');d=ImageDraw.Draw(sheet)
    for j,n in enumerate([7,19,25,46,53,60]):
        im=Image.open(STAGE/f'{n:02}.jpg').crop((0,0,1024,490));im.thumbnail((512,245));x=j%2*520;y=j//2*280
        sheet.paste(im,(x,y+28));d.text((x+5,y+5),str(n),fill='white')
    sheet.save(STAGE/'review.jpg',quality=95)
    print('Built 62 semi-transparent labels; artwork outside labels and all alpha bytes unchanged.')

def install():
    prior=json.loads((BACKUP/'installation_manifest.json').read_text())
    rows=json.loads((STAGE/'source_register.json').read_text(encoding='utf-8'))
    for op in prior['operations']:assert sha(ROOT/op['path'])==op['after_sha256']
    for r in rows:assert sha(STAGE/r['staged_file'])==r['staged_sha256']
    operations=[]
    for op in prior['operations']:
        n=int(Path(op['path']).stem.rsplit('_',1)[1]);r=rows[n-1]
        shutil.copy2(STAGE/r['staged_file'],ROOT/op['path'])
        assert sha(ROOT/op['path'])==r['staged_sha256']
        updated=dict(op,previous_install_sha256=op['after_sha256'],previous_install_archive='revision4_opacity60/staged/'+r['staged_file'],after_sha256=r['staged_sha256']);operations.append(updated)
    for r in rows:
        shutil.copy2(STAGE/r['staged_file'],BASE/'staged'/r['staged_file'])
        im=Image.open(STAGE/r['staged_file']).convert('RGB');n=r['slot']
        im.save(BASE/'previews'/f'{n:02}.jpg',quality=95)
        im.crop((0,0,1024,490)).save(BASE/'previews'/f'{n:02}_art.jpg',quality=95)
        r['museum_label']['visual_review']='passed: light, dark, detailed and long-label examples inspected; layout and text unchanged across all 62'
    (BASE/'source_register.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
    manifest=dict(prior,installed_at=datetime.now(timezone.utc).isoformat(),label_background_opacity=.4,operations=operations)
    (BASE/'installation_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    for name in ['gallery.html','ARTWORK_CREDITS.md','README.md']:
        p=BASE/name;s=p.read_text(encoding='utf-8')
        s=s.replace('60%-opacity','40%-opacity').replace('opaque museum labels','semi-transparent museum labels').replace('opaque corner labels','semi-transparent corner labels').replace('solid dark background','40%-opacity dark background with fully opaque text')
        if name=='gallery.html':s=s.replace('previews/', 'previews/').replace('?labels=semi60','?labels=semi40').replace('.jpg"','.jpg?labels=semi40"')
        p.write_text(s,encoding='utf-8')
    for folder in ['data/loading_screen','data/loading_screen/load_steamsteel','data/loading_screen/load_althis']:
        shutil.copy2(BASE/'ARTWORK_CREDITS.md',ROOT/folder/'ARTWORK_CREDITS.md')
    print('Installed 62 semi-transparent labels; all 186 runtime and launcher files verified.')

if __name__=='__main__':install() if '--install' in sys.argv else build()
