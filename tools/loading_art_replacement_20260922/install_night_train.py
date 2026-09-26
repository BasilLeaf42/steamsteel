from pathlib import Path
import json,shutil
from datetime import datetime,timezone
from PIL import Image
from compact_labels_bakufu import BASE,ROOT,WORK,sha,export
p=BASE/'night_train_preview';meta=json.loads((p/'preview_metadata.json').read_text())
rows=json.loads((BASE/'source_register.json').read_text(encoding='utf-8'))
man=json.loads((BASE/'installation_manifest.json').read_text())
assert len(rows)==63 and not any(r['slot']==64 for r in rows)
for op in man['operations']:assert sha(ROOT/op['path'])==op['after_sha256'],op['path']
folders=['data/loading_screen','data/loading_screen/load_steamsteel','data/loading_screen/load_althis']
name='Loading_screen_64.tga'
for f in folders:assert not (ROOT/f/name).exists()
backup=BASE/'revision7_before_night_train';backup.mkdir(exist_ok=False)
for f in ['source_register.json','installation_manifest.json','ARTWORK_CREDITS.md','README.md','gallery.html','aspect_ratio_audit.json']:shutil.copy2(BASE/f,backup/f)
source=p/'Loading_screen_64_preview.tga';im=Image.open(source);assert im.size==(1024,768) and im.mode=='RGBA'
approved=Image.open(p/'Night_Train_loading_preview.png').convert('RGBA')
assert im.crop((0,0,1024,490)).tobytes()==approved.resize((1024,490),Image.Resampling.LANCZOS).tobytes()
clean=Image.new('RGBA',(1024,768),(16,18,17,255));clean.paste(Image.open(p/'crop_without_overlay.png').resize((1024,490),Image.Resampling.LANCZOS),(0,0))
clean.save(BASE/'unlabelled_current'/name,compression='tga_rle')
shutil.copy2(p/'source.jpg',BASE/'sources/64.image')
shutil.copy2(source,BASE/'staged'/name);shutil.copy2(source,WORK/'staged'/name)
shutil.copy2(BASE/'unlabelled_current'/name,WORK/'clean'/name)
shutil.copy2(p/'Night_Train_loading_preview.png',WORK/'display/64.png');shutil.copy2(p/'crop_without_overlay.png',WORK/'display_clean/64.png')
im.convert('RGB').save(BASE/'previews/64.jpg',quality=95);approved.convert('RGB').save(BASE/'previews/64_art.jpg',quality=95)
r=dict(slot=64,title=meta['title'],artist=meta['artist'],date=meta['date'],theme='Japanese railway passengers',approximation='Additional painting explicitly supplied and crop approved by the user.',medium='Oil on canvas',medium_verified=True,medium_evidence=dict(url=meta['metadata_source'],basis='Museum catalogue identifies oil on canvas, 1901.'),source_url=meta['source_url'],metadata_source=meta['metadata_source'],download_url=meta['source_url'],source_sha256=meta['source_sha256'],source_pixel_size=meta['source_size'],licence=meta['rights_status'],licence_url=None,credit='User-supplied reproduction; artist and date verified against Tokyo University of the Arts catalogue.',crop_box=meta['crop_box'],crop_reason='User-approved full-width crop preserving passengers faces; retains 50.659% of source height.',display_crop_ratio=2.5,staged_file=name,output_size=[1024,768],output_mode='RGBA',staged_sha256=sha(source),unlabelled_sha256=sha(BASE/'unlabelled_current'/name),unlabelled_file='unlabelled_current/'+name,formatting='Approved 1250x500 display panel precompensated into 1024x490 game artwork area; dark footer.',final_visual_review='User approved preview 2026-09-24',museum_label=dict(corner='top-left',title=meta['title'],artist=meta['artist'],date=meta['date'],box=[10,10,198,57],coordinate_space='1250x500 display panel',title_font='Georgia Bold 13px',details_font='Arial 11px',background_opacity=.4,text_opacity=1,visual_review='User approved'))
rows.append(r)
for f in folders:
 target=ROOT/f/name;shutil.copy2(source,target);assert sha(target)==r['staged_sha256']
 man['operations'].append(dict(path=f+'/'+name,before_sha256=None,archive=None,after_sha256=r['staged_sha256']))
man.update(installed_at=datetime.now(timezone.utc).isoformat(),screens=64,copies_verified=192,museum_labels=64,new_oil_paintings=62)
(BASE/'source_register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'installation_manifest.json').write_text(json.dumps(man,indent=2),encoding='utf-8')
(BASE/'sources/64.download.json').write_text(json.dumps(dict(title=meta['title'],url=meta['source_url'],sha256=meta['source_sha256']),indent=2))
export(rows)
readme=BASE/'README.md';readme.write_text(readme.read_text(encoding='utf-8')+'\nScreen 64: Night Train, Akamatsu Rinsaku, 1901. Approved crop installed unchanged. Source is the user-supplied retailer reproduction; no open licence asserted for that file.\n',encoding='utf-8')
audit=json.loads((BASE/'aspect_ratio_audit.json').read_text());audit['items'].append(dict(slot=64,scale_x=1250/922,scale_y=500/(513.8-145),ratio_error_percent=0.0,user_approved=True));(BASE/'aspect_ratio_audit.json').write_text(json.dumps(audit,indent=2))
meta['installed']=True;meta['installed_slot']=64;(p/'preview_metadata.json').write_text(json.dumps(meta,indent=2))
for op in man['operations']:assert sha(ROOT/op['path'])==op['after_sha256']
print('Installed approved screen 64 in all three sets. Verified 192 installed textures. Updated both galleries and ZIP packs.')
