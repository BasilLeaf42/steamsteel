import json,shutil
from PIL import Image,ImageDraw
from compact_labels_bakufu import BASE,ROOT,WORK,TITLE,BODY,wrap,sha,export
B=BASE/'global_expansion';src=B/'sources/31_0.image';p=json.loads((B/'31.json').read_text())['pages'][0];ii=p['imageinfo'][0]
rev=BASE/'revision11_before_colour_replacement';rev.mkdir(exist_ok=False)
for f in ['source_register.json','installation_manifest.json','ARTWORK_CREDITS.md','README.md','aspect_ratio_audit.json']:shutil.copy2(BASE/f,rev/f)
for folder,name in [('sources','100.image'),('sources','100.download.json'),('staged','Loading_screen_100.tga'),('unlabelled_current','Loading_screen_100.tga')]:
 (rev/folder).mkdir(exist_ok=True);shutil.copy2(BASE/folder/name,rev/folder/name)
for folder in ['display','display_clean']:
 (rev/folder).mkdir();shutil.copy2(WORK/folder/'100.png',rev/folder/'100.png')
rows=json.loads((BASE/'source_register.json').read_text(encoding='utf-8'));old=rows[99];r=dict(old)
r.update(title='Hong Kong Harbour',artist='Unknown Chinese artist',date='Late 1850s',theme='Strategic harbour and maritime trade',medium='Oil on canvas; licensed museum photograph',medium_verified=True,approximation='Period Chinese harbour painting replaces the rejected monochrome Palikiao engraving. Depicts shipping and the Hong Kong waterfront.',commons_file=p['title'],source_url=ii['descriptionurl'],download_url=src.with_suffix('.url').read_text(),source_sha256=sha(src),source_pixel_size=[1920,1119],licence='CC BY-SA 4.0',licence_url='https://creativecommons.org/licenses/by-sa/4.0/',rights_basis='Photograph explicitly licensed CC BY-SA 4.0 on Wikimedia Commons.',credit='Painting: unknown Chinese artist, late 1850s; Asian Civilisations Museum, Singapore. Photograph: Bjoertvedt, 10 November 2018, Wikimedia Commons, CC BY-SA 4.0. Cropped/resized and captioned adaptations are also licensed CC BY-SA 4.0.',changes='Cropped, resized and captioned. This image adaptation is distributed under CC BY-SA 4.0; the collection as a whole is not relicensed.',crop_box=[12,350,1902,1106],crop_reason='Remove excess sky and narrow photographed edges; retain the principal ships, complete sails, mountain skyline and waterfront.',date_note='Painting date follows the museum photograph’s file identification (late 1850s), not the 2018 photograph date.',research_file='global_expansion/31.json',research_index=0,local_source='global_expansion/sources/31_0.image',final_visual_review='pending')
im=Image.open(src).convert('RGBA');display=im.resize((1250,500),Image.Resampling.LANCZOS,box=tuple(r['crop_box']));display.save(rev/'candidate_clean.png')
ts=wrap(r['title'],TITLE,272);ds=wrap(r['artist']+' · '+r['date'],BODY,272);w=max(160,int(max([TITLE.getlength(s) for s in ts]+[BODY.getlength(s) for s in ds]))+17);h=16*len(ts)+14*len(ds)+17;x=y=10
layer=Image.new('RGBA',display.size);d=ImageDraw.Draw(layer);d.rectangle((x,y,x+w-1,y+h-1),fill=(28,31,29,102),outline=(139,129,105,60));out=Image.alpha_composite(display,layer);d=ImageDraw.Draw(out);ty=y+7
for s in ts:d.text((x+8,ty),s,font=TITLE,fill=(241,233,213,255),anchor='lt');ty+=16
ty+=3
for s in ds:d.text((x+8,ty),s,font=BODY,fill=(222,218,206,255),anchor='lt');ty+=14
out.save(rev/'candidate.png');r['museum_label']=dict(old['museum_label'],title=r['title'],artist=r['artist'],date=r['date'],box=[x,y,x+w,y+h],corner='top-left',visual_review='pending')
(rev/'candidate.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print('Colour replacement staged for review')
