from pathlib import Path
import json,shutil
from datetime import datetime,timezone
from PIL import Image,ImageDraw,ImageFont
from compact_labels_bakufu import BASE,ROOT,WORK,sha,export
b=BASE/'artscape_additions';selected=json.loads((b/'selected.json').read_text());inventory=json.loads((b/'inventory.json').read_text())
f=ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf',13);g=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)
for r in selected:
 n=r['slot'];y={65:35,66:120}.get(n,r['crop_box'][1]);r['crop_box']=[3,y,516,y+205.2]
 im=Image.open(b/f"{r['image_id']:02}.jpg").convert('RGB');out=im.resize((1250,500),Image.Resampling.LANCZOS,box=r['crop_box']).convert('RGBA');out.save(b/f'{n}_clean.png')
 layer=Image.new('RGBA',out.size);d=ImageDraw.Draw(layer);x,y,c,e=r['label_box'];d.rectangle((x,y,c-1,e-1),fill=(28,31,29,102),outline=(139,129,105,60));out=Image.alpha_composite(out,layer);d=ImageDraw.Draw(out)
 lines=[r['title']] if n!=66 else ['The Kitchen of the Kikuya Hotel','in Shuzenji, Izu'];ty=17
 for l in lines:d.text((18,ty),l,font=f,fill=(241,233,213,255),anchor='lt');ty+=16
 d.text((18,ty+3),r['artist']+' · '+r['date'],font=g,fill=(222,218,206,255),anchor='lt');out.save(b/f'{n}.png')
(b/'selected.json').write_text(json.dumps(selected,indent=2))
if __name__=='__main__':
 import sys
 if '--install' not in sys.argv:raise SystemExit('Prepared adjusted crops for visual review.')
 rows=json.loads((BASE/'source_register.json').read_text(encoding='utf-8'));man=json.loads((BASE/'installation_manifest.json').read_text());assert len(rows)==64
 for op in man['operations']:assert sha(ROOT/op['path'])==op['after_sha256']
 backup=BASE/'revision8_before_artscape';backup.mkdir(exist_ok=False)
 for name in ['source_register.json','installation_manifest.json','ARTWORK_CREDITS.md','README.md','gallery.html','aspect_ratio_audit.json']:shutil.copy2(BASE/name,backup/name)
 folders=['data/loading_screen','data/loading_screen/load_steamsteel','data/loading_screen/load_althis']
 for r in selected:
  n=r['slot'];name=f'Loading_screen_{n}.tga';src=b/f"{r['image_id']:02}.jpg";info=inventory[r['image_id']]
  for folder in folders:assert not (ROOT/folder/name).exists()
  for clean in [True,False]:
   display=Image.open(b/f'{n}{"_clean" if clean else ""}.png').convert('RGBA');tex=Image.new('RGBA',(1024,768),(16,18,17,255));tex.paste(display.resize((1024,490),Image.Resampling.LANCZOS),(0,0));dest=BASE/('unlabelled_current' if clean else 'staged')/name;tex.save(dest,compression='tga_rle');shutil.copy2(dest,WORK/('clean' if clean else 'staged')/name);display.save(WORK/('display_clean' if clean else 'display')/f'{n:02}.png')
   if not clean:
    tex.convert('RGB').save(BASE/'previews'/f'{n:02}.jpg',quality=95);display.convert('RGB').save(BASE/'previews'/f'{n:02}_art.jpg',quality=95)
  shutil.copy2(src,BASE/'sources'/f'{n:02}.image')
  r.update(theme='Meiji Japan everyday life',approximation='Selected from the user-supplied article; landscape composition visually reviewed for a 2.5:1 loading panel.',source_url='https://artscape.jp/artscape/eng/ht/2207.html',download_url=info['url'],source_sha256=sha(src),source_pixel_size=info['size'],medium_verified=True,licence='Museum-courtesy reproduction on user-supplied page; no open licence stated for the reproduction.',credit='Image courtesy of Fuchu Art Museum, via artscape Japan.',crop_reason='Manually positioned full-width crop preserving main figures; thin reproduction border excluded.',display_crop_ratio=2.5,staged_file=name,output_size=[1024,768],output_mode='RGBA',staged_sha256=sha(BASE/'staged'/name),unlabelled_sha256=sha(BASE/'unlabelled_current'/name),unlabelled_file='unlabelled_current/'+name,formatting='1250x500 display artwork, precompensated into 1024x490 game panel; compact overlay and unchanged dark footer.',final_visual_review='passed',museum_label=dict(corner='top-left',box=r['label_box'],coordinate_space='1250x500 display panel',background_opacity=.4,title_font='Georgia Bold 13px',details_font='Arial 11px',visual_review='passed'))
  rows.append(r)
  for folder in folders:
   target=ROOT/folder/name;shutil.copy2(BASE/'staged'/name,target);man['operations'].append(dict(path=folder+'/'+name,before_sha256=None,archive=None,after_sha256=sha(target)))
  (BASE/'sources'/f'{n:02}.download.json').write_text(json.dumps(dict(url=info['url'],sha256=sha(src)),indent=2))
 man.update(screens=68,copies_verified=204,museum_labels=68,new_oil_paintings=64,installed_at=datetime.now(timezone.utc).isoformat())
 (BASE/'source_register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');(BASE/'installation_manifest.json').write_text(json.dumps(man,indent=2))
 export(rows)
 (BASE/'README.md').write_text((BASE/'README.md').read_text(encoding='utf-8')+'\nScreens 65–68: four manually framed landscape works from the user-supplied artscape article, including two watercolours. Original reproductions are 519px wide and have no stated open licence. Five upright compositions excluded.\n',encoding='utf-8')
 audit=json.loads((BASE/'aspect_ratio_audit.json').read_text());audit['items'] += [dict(slot=r['slot'],scale_x=1250/513,scale_y=500/205.2,ratio_error_percent=0) for r in selected];(BASE/'aspect_ratio_audit.json').write_text(json.dumps(audit,indent=2))
 for op in man['operations']:
  assert sha(ROOT/op['path'])==op['after_sha256'];im=Image.open(ROOT/op['path']);assert im.size==(1024,768) and im.mode=='RGBA'
 print('Added four landscapes, slots 65-68. Verified all 204 textures. Refreshed galleries and archives.')
