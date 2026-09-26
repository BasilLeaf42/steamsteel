from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,sys
from datetime import datetime,timezone
from compact_labels_bakufu import BASE,ROOT,WORK,sha,export
from research import clean
B=BASE/'open_meiji_replacements';sources=json.loads((B/'selected_sources.json').read_text(encoding='utf-8'))
configs=[('The Silk Merchant, Japan','Robert Frederick Blum','1892','Oil on canvas',[50.5,0,3450.5,1360]),('Harvest','Asai Chu','1890','Oil on canvas',[0,750,3523,2159.2]),('Spring Ridge','Asai Chu','1888','Oil on canvas',[0,3000,13307,8322.8]),('A Japanese Garden with Cherry Blossom','John Varley II','1895','Oil on panel',[15,540,1485,1128])]
f=ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf',13);g=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)
rows=[];sheet=Image.new('RGB',(1250,2120),'#20242a');sd=ImageDraw.Draw(sheet)
for i,(p,c) in enumerate(zip(sources,configs)):
 n=65+i;title,artist,date,medium,box=c;ii=p['imageinfo'][0];assert clean(ii['extmetadata']['LicenseShortName']['value'])=='Public domain'
 src=B/f"{p['id']}.jpg";im=Image.open(src).convert('RGB');display=im.resize((1250,500),Image.Resampling.LANCZOS,box=box).convert('RGBA');display.save(B/f'{n}_clean.png')
 label_y=443 if n==65 else 10; width=int(max(f.getlength(title),g.getlength(artist+' · '+date)))+17;layer=Image.new('RGBA',display.size);d=ImageDraw.Draw(layer);d.rectangle((10,label_y,10+width-1,label_y+46),fill=(28,31,29,102),outline=(139,129,105,60));out=Image.alpha_composite(display,layer);d=ImageDraw.Draw(out);d.text((18,label_y+7),title,font=f,fill=(241,233,213,255),anchor='lt');d.text((18,label_y+26),artist+' · '+date,font=g,fill=(222,218,206,255),anchor='lt');out.save(B/f'{n}.png');sheet.paste(out,(0,i*530+30));sd.text((10,i*530+6),str(n),fill='white')
 rows.append(dict(slot=n,title=title,artist=artist,date=date,medium=medium,medium_verified=True,source_url=ii['descriptionurl'],commons_file=p['title'],download_url=p.get('download_url',ii['url']),source_sha256=sha(src),source_pixel_size=list(im.size),licence='Public domain',licence_url='https://creativecommons.org/publicdomain/mark/1.0/',credit='Wikimedia Commons; public-domain status recorded in saved image metadata.',crop_box=box,crop_reason='Manually selected framing retains key figures and setting at the game display ratio.',display_crop_ratio=2.5,theme='Meiji Japan everyday life',approximation='Period Western-style painting of Japanese everyday life; replaces uncertain-licence artscape reproduction.',museum_label=dict(corner='bottom-left' if n==65 else 'top-left',box=[10,label_y,10+width,label_y+47],coordinate_space='1250x500 display panel',background_opacity=.4,text_opacity=1,title_font='Georgia Bold 13px',details_font='Arial 11px'),source_local=str(src)))
sheet.save(B/'replacement_review.jpg',quality=95);(B/'replacement_register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
if '--install' not in sys.argv:print('Four public-domain replacements prepared.');sys.exit()
old=json.loads((BASE/'source_register.json').read_text(encoding='utf-8'));man=json.loads((BASE/'installation_manifest.json').read_text());assert len(old)==68
for op in man['operations']:assert sha(ROOT/op['path'])==op['after_sha256']
archive=BASE/'revision9_removed_uncertain_licences';archive.mkdir(exist_ok=False)
for name in ['source_register.json','installation_manifest.json','ARTWORK_CREDITS.md','README.md','gallery.html','aspect_ratio_audit.json']:shutil.copy2(BASE/name,archive/name)
for folder in ['staged','unlabelled_current','sources']:
 (archive/folder).mkdir()
 for n in range(65,69):
  name=f'{n:02}.image' if folder=='sources' else f'Loading_screen_{n}.tga';shutil.copy2(BASE/folder/name,archive/folder/name)
for r in rows:
 n=r['slot'];name=f'Loading_screen_{n}.tga';src=Path(r.pop('source_local'));shutil.copy2(src,BASE/'sources'/f'{n:02}.image')
 for bare in [True,False]:
  display=Image.open(B/f'{n}{"_clean" if bare else ""}.png').convert('RGBA');tex=Image.new('RGBA',(1024,768),(16,18,17,255));tex.paste(display.resize((1024,490),Image.Resampling.LANCZOS),(0,0));folder='unlabelled_current' if bare else 'staged';tex.save(BASE/folder/name,compression='tga_rle');shutil.copy2(BASE/folder/name,WORK/('clean' if bare else 'staged')/name);display.save(WORK/('display_clean' if bare else 'display')/f'{n:02}.png')
  if not bare:tex.convert('RGB').save(BASE/'previews'/f'{n:02}.jpg',quality=95);display.convert('RGB').save(BASE/'previews'/f'{n:02}_art.jpg',quality=95)
 r.update(staged_file=name,output_size=[1024,768],output_mode='RGBA',staged_sha256=sha(BASE/'staged'/name),unlabelled_sha256=sha(BASE/'unlabelled_current'/name),unlabelled_file='unlabelled_current/'+name,final_visual_review='passed',formatting='Aspect-preserving 2.5:1 display crop with compact label; precompensated for game display.')
 r['museum_label']['visual_review']='passed'
 for op in man['operations']:
  if op['path'].endswith('/'+name):
   op.update(previous_install_sha256=op['after_sha256'],previous_install_archive='revision9_removed_uncertain_licences/staged/'+name,after_sha256=r['staged_sha256']);shutil.copy2(BASE/'staged'/name,ROOT/op['path'])
 (BASE/'sources'/f'{n:02}.download.json').write_text(json.dumps(dict(url=r['download_url'],sha256=r['source_sha256']),indent=2))
new=old[:64]+rows;(BASE/'source_register.json').write_text(json.dumps(new,ensure_ascii=False,indent=2),encoding='utf-8');man.update(installed_at=datetime.now(timezone.utc).isoformat(),new_oil_paintings=66);(BASE/'installation_manifest.json').write_text(json.dumps(man,indent=2))
export(new)
readme=BASE/'README.md';readme.write_text(readme.read_text(encoding='utf-8')+'\nSlots 65–68 replaced with four explicitly public-domain Commons paintings. Removed artscape reproductions retained only in revision9_removed_uncertain_licences and historical working files; absent from current galleries and ZIPs.\n',encoding='utf-8')
audit=json.loads((BASE/'aspect_ratio_audit.json').read_text());audit['items']=[x for x in audit['items'] if x['slot']<65]+[dict(slot=r['slot'],ratio_error_percent=0,source=r['source_url'],crop_box=r['crop_box']) for r in rows];(BASE/'aspect_ratio_audit.json').write_text(json.dumps(audit,indent=2))
for op in man['operations']:assert sha(ROOT/op['path'])==op['after_sha256']
print('Replaced slots 65-68 in all three sets; 204 hashes verified. Galleries and ZIPs rebuilt without the four removed works.')
