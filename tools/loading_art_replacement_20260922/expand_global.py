"""Curated regional expansion; build first, inspect contact sheets, then install."""
import json, shutil, sys, html, re
from datetime import datetime, timezone
from PIL import Image, ImageOps, ImageDraw
from compact_labels_bakufu import BASE, ROOT, WORK, TITLE, BODY, wrap, sha, export
B=BASE/'global_expansion'
# Manually chosen vertical anchors within the available crop travel, after border removal.
# title | artist | date | crop anchor | corner | subject
SPEC=[
('The Valley of Mexico','José María Velasco','1875',.72,'top-left','Regional landscape'),
('Study for Lima’s Main Square','Johann Moritz Rugendas','c. 1843',.69,'top-right','Urban centre'),
('A Halt in the Countryside','Prilidiano Pueyrredón','1861',1,'top-right','Overland transport'),
('Horse Breaking','Juan Manuel Blanes','c. 1875',.70,'top-left','Horsemanship'),
('Cotopaxi','Frederic Edwin Church','1862',.33,'top-right','Regional landscape'),
('The Great Tree-Aloe of Damaraland','Thomas Baines','1861',.57,'top-right','Regional landscape'),
('Wagon Crossing a Drift, Natal','Thomas Baines','1874',.91,'top-right','Overland transport'),
('The Rapids of Victoria Falls','Thomas Baines','1864',.67,'top-right','River geography'),
('The Kissar Player','Frederick Goodall','1859–1870',.31,'top-right','Cultural life'),
('Falcon Hunt, Algeria','Eugène Fromentin','1874',.96,'top-left','Mounted life'),
('Café at Biskra, Algeria','Frederick Arthur Bridgman','1884',.83,'top-right','Urban life'),
('Market in Jaffa','Gustav Bauernfeind','1887',.88,'top-left','Trade'),
('Mirror Hall','Kamal-ol-Molk','1890s',.77,'top-left','Political centre'),
('Caravan at the Gates of Constantinople','Alberto Pasini','1881',.62,'top-left','Trade and transport'),
('The Gate of the Umayyad Mosque','Gustav Bauernfeind','1890',.42,'top-left','Urban centre'),
('Jerusalem from the Mount of Olives','Gustav Bauernfeind','c. 1902',.38,'top-left','City panorama'),
('Gunung Merapi and a Horseman','Raden Saleh','c. 1867',.89,'top-right','Regional landscape'),
('Bangkok: Spice Shops','Eduard Hildebrandt','before 1868',.69,'top-left','River trade'),
('Battle Scene with Elephants','Thai Wicharn','Late 19th century',.50,'top-left','Battle'),
('El Cundiman','José Honorato Lozano','1847',.20,'bottom-right','Cultural life'),
('An Elephant at Dusk','Eduard Hildebrandt','after 1863',.90,'top-right','Regional landscape'),
('Khyber Pass and the Fortress of Ali Masjid','James Rattray','1848',.65,'top-left','Strategic pass and fortress'),
('A Street Market Scene, India','Edwin Lord Weeks','1887',.42,'top-left','Trade'),
('Shop of Tingqua, the Painter','Tingqua (Guan Lianchang)','c. 1855',.62,'top-right','Trade and craft'),
('The Battle of Avaí','Pedro Américo','1877',.97,'top-left','Battle'),
('Battle of Angamos','Thomas Somerscales','1889',.60,'top-left','Naval battle'),
('Battle of Puebla, 5 May 1862','Unknown artist','1870',.66,'top-left','Battle'),
('The Battle of Isandlwana','Charles Edwin Fripp','1885',.76,'top-right','Battle'),
('Omdurman: The First Battle, 6.30 a.m.','A. Sutherland','1898 or later',.55,'top-right','Battle'),
('The Arrest of Diponegoro','Raden Saleh','1857',.69,'top-right','War and political history'),
('The Relief of Lucknow, 1857','Thomas Jones Barker','1859',.97,'top-left','Battle'),
('The Bridge after the Battle of Palikiao','Émile Bayard','19th century',.55,'top-left','Battle'),
]
# Border boxes expressed in the downloaded image coordinate space, normalised.
BOUNDS={86:(.158,.190,.848,.79),88:(.09,.14,.874,.872),92:(.025,.01,.985,.985),97:(.012,.024,.981,.921),99:(.164,.289,.831,.773),100:(.006,.005,.993,.931)}
MEDIUM={86:'Colour print after a watercolour',88:'Watercolour',89:'Painting; precise medium not documented',90:'Colour lithograph',92:'Gouache on paper',96:'Colour reproduction of a painting',97:'Chromolithograph',99:'Oil on canvas; licensed museum photograph',100:'Engraving'}
def plain(s):return html.unescape(re.sub('<[^>]+>',' ',str(s))).strip()
def build():
 choices=json.loads((B/'choices.json').read_text());choices[30][1]=4;choices[27][1]=1
 rows=[]
 for folder in ['display','display_clean','staged','clean','previews']:(B/folder).mkdir(exist_ok=True)
 for n,(choice,spec) in enumerate(zip(choices,SPEC),69):
  q,j,region,country=choice;title,artist,date,anchor,corner,theme=spec
  p=json.loads((B/f'{q}.json').read_text(encoding='utf-8'))['pages'][j];ii=p['imageinfo'][0];m=ii['extmetadata']
  licence=plain(m['LicenseShortName']['value']);assert licence in ['Public domain','CC BY 4.0']
  src=B/'sources'/f'{q}_{j}.image';im=ImageOps.exif_transpose(Image.open(src)).convert('RGB');w,h=im.size
  a,b,c,d=BOUNDS.get(n,(0,0,1,1));a*=w;c*=w;b*=h;d*=h
  cw=c-a;ch=cw/2.5;assert ch<=d-b
  y=b+(d-b-ch)*anchor;box=[a,y,c,y+ch]
  assert abs(1250/(c-a)-500/ch)<1e-10
  panel=im.resize((1250,500),Image.Resampling.LANCZOS,box=box).convert('RGBA');panel.save(B/'display_clean'/f'{n:02}.png')
  clean=Image.new('RGBA',(1024,768),(16,18,17,255));clean.paste(panel.resize((1024,490),Image.Resampling.LANCZOS),(0,0));name=f'Loading_screen_{n}.tga';clean.save(B/'clean'/name,compression='tga_rle',orientation=-1)
  ts=wrap(title,TITLE,272);ds=wrap(artist+' · '+date,BODY,272);pw=max(160,int(max([TITLE.getlength(x) for x in ts]+[BODY.getlength(x) for x in ds]))+17);ph=len(ts)*16+len(ds)*14+17
  x=10 if corner.endswith('left') else 1240-pw;y=10 if corner.startswith('top') else 490-ph
  layer=Image.new('RGBA',panel.size);draw=ImageDraw.Draw(layer);draw.rectangle((x,y,x+pw-1,y+ph-1),fill=(28,31,29,102),outline=(139,129,105,60));out=Image.alpha_composite(panel,layer);draw=ImageDraw.Draw(out);ty=y+7
  for t in ts:draw.text((x+8,ty),t,font=TITLE,fill=(241,233,213,255),anchor='lt');ty+=16
  ty+=3
  for t in ds:draw.text((x+8,ty),t,font=BODY,fill=(222,218,206,255),anchor='lt');ty+=14
  out.save(B/'display'/f'{n:02}.png');out.convert('RGB').save(B/'previews'/f'{n:02}_art.jpg',quality=95);clean.paste(out.resize((1024,490),Image.Resampling.LANCZOS),(0,0));clean.save(B/'staged'/name,compression='tga_rle',orientation=-1);clean.convert('RGB').save(B/'previews'/f'{n:02}.jpg',quality=95)
  tail=ii['url'].split('?')[0].split('/wikipedia/commons/')[1];url=ii['url'] if w==ii['width'] else 'https://upload.wikimedia.org/wikipedia/commons/thumb/'+tail+'/1280px-'+tail.rsplit('/',1)[1]
  if (src.with_suffix('.url')).exists():url=src.with_suffix('.url').read_text()
  credit=plain(m.get('Credit',{}).get('value',''))
  if n==97:credit='A. Sutherland / Wellcome Collection. CC BY 4.0.'
  if n==99:credit='Painting: Thomas Jones Barker, 1859. Photograph: APK, 17 May 2026, Wikimedia Commons, CC BY 4.0.'
  rows.append(dict(slot=n,title=title,artist=artist,date=date,region=region,country=country,theme=theme,approximation='Period artwork selected for geographic coverage. A detail is cropped to the wide loading panel.',medium=MEDIUM.get(n,'Painting'),medium_verified=n in MEDIUM,commons_file=p['title'],source_url=ii['descriptionurl'],download_url=url,source_sha256=sha(src),source_pixel_size=[w,h],licence=licence,licence_url=m.get('LicenseUrl',{}).get('value','https://creativecommons.org/publicdomain/mark/1.0/'),rights_basis='Explicit '+licence+' declaration in archived Wikimedia Commons metadata.',credit=credit,changes='Cropped, resized, and captioned for the game; no generated or reconstructed image content.',crop_box=box,crop_reason=f'Manually selected vertical anchor {anchor}, after excluding any paper border or frame; reviewed at 2.50:1.',display_crop_ratio=2.5,staged_file=name,staged_sha256=sha(B/'staged'/name),unlabelled_sha256=sha(B/'clean'/name),unlabelled_file='unlabelled_current/'+name,output_size=[1024,768],output_mode='RGBA',formatting='Uniform 1250x500 display crop, precompensated into 1024x490 game panel. Dark footer retained.',museum_label=dict(corner=corner,title=title,artist=artist,date=date,box=[x,y,x+pw,y+ph],coordinate_space='1250x500 display panel',title_font='Georgia Bold 13px',details_font='Arial 11px',background_opacity=.4,text_opacity=1,opaque=False,visual_review='pending'),source_visual_review='passed',final_visual_review='pending',research_file=f'global_expansion/{q}.json',research_index=j,local_source=str(src.relative_to(BASE))))
  if n==81:rows[-1]['date_note']='Broad 1890s dating used because published dates conflict. Encyclopaedia Iranica, as cited by the Mirror Hall article, places completion in 1896; do not use the reproduction photograph date.'
  if n==86:rows[-1]['date_note']='Watercolour created before the artist’s death in 1868; colour-plate edition published 1871–1874.'
  if n==87:rows[-1]['approximation']='Late nineteenth-century Thai painting of historical elephant combat; not a claim to depict a contemporary battle.'
  if n==96:rows[-1]['approximation']='Replaces the rejected Saving the Colours composition. Wide battle detail preserves the central British and Zulu figures; the summit of the background hill and the lower foreground are cropped.'
  if n==97:rows[-1]['date_note']='Depicts the 1898 battle. Exact print publication date is not stated in the collection record; 1898 is a lower bound, not a verified creation date.'
  if n==100:rows[-1]['date_note']='Depicts the battle of 21 September 1860. Source battle date is not treated as the engraving creation date.'
 (B/'new_register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 for start in range(0,32,8):
  sheet=Image.new('RGB',(1260,1140),'#20242a');draw=ImageDraw.Draw(sheet)
  for k,r in enumerate(rows[start:start+8]):
   im=Image.open(B/'display'/f"{r['slot']:02}.png").convert('RGB');im.thumbnail((620,248));x=k%2*630;y=k//2*285;sheet.paste(im,(x,y+30));draw.text((x,y),str(r['slot'])+' '+r['country'],fill='white')
  sheet.save(B/f'crops_{start//8}.jpg',quality=96)
 print('Built 32 candidates for visual review.')

def install():
 new=json.loads((B/'new_register.json').read_text(encoding='utf-8'));assert all(r['final_visual_review']=='passed' for r in new)
 rows=json.loads((BASE/'source_register.json').read_text(encoding='utf-8'));assert len(rows)==68
 prior=json.loads((BASE/'installation_manifest.json').read_text());assert len(prior['operations'])==204
 for op in prior['operations']:assert sha(ROOT/op['path'])==op['after_sha256'],op['path']
 folders=['data/loading_screen','data/loading_screen/load_steamsteel','data/loading_screen/load_althis']
 for r in new:
  assert sha(B/'staged'/r['staged_file'])==r['staged_sha256']
  for folder in folders:assert not (ROOT/folder/r['staged_file']).exists()
 backup=BASE/'revision10_before_global_expansion';backup.mkdir(exist_ok=False)
 for name in ['source_register.json','installation_manifest.json','ARTWORK_CREDITS.md','README.md','gallery.html','aspect_ratio_audit.json']:shutil.copy2(BASE/name,backup/name)
 groups=json.loads((B/'regional_audit_before.json').read_text())['groups']
 for region,slots in groups.items():
  for r in rows:
   if r['slot'] in slots:r['region']=region
 operations=prior['operations'][:]
 for r in new:
  n=r['slot'];name=r['staged_file'];src=BASE/r['local_source'];shutil.copy2(src,BASE/'sources'/f'{n:02}.image');shutil.copy2(BASE/r['research_file'],BASE/'sources'/f'{n:02}.download.json')
  for folder in folders:
   path=folder+'/'+name;shutil.copy2(B/'staged'/name,ROOT/path);operations.append(dict(path=path,before_sha256=None,archive=None,after_sha256=r['staged_sha256']))
  for a,dest in [('staged',BASE/'staged'),('clean',BASE/'unlabelled_current'),('staged',WORK/'staged'),('clean',WORK/'clean')]:shutil.copy2(B/a/name,dest/name)
  for a in ['display','display_clean']:shutil.copy2(B/a/f'{n:02}.png',WORK/a/f'{n:02}.png')
  for suffix in ['','_art']:shutil.copy2(B/'previews'/f'{n:02}{suffix}.jpg',BASE/'previews'/f'{n:02}{suffix}.jpg')
  groups[r['region']].append(n)
 rows+=new
 (BASE/'source_register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 (BASE/'installation_manifest.json').write_text(json.dumps(dict(prior,installed_at=datetime.now(timezone.utc).isoformat(),screens=100,copies_verified=300,museum_labels=100,operations=operations),indent=2),encoding='utf-8')
 audit=json.loads((BASE/'aspect_ratio_audit.json').read_text());audit['items'] += [dict(slot=r['slot'],crop_box=r['crop_box'],scale_x=1250/(r['crop_box'][2]-r['crop_box'][0]),scale_y=500/(r['crop_box'][3]-r['crop_box'][1]),ratio_error_percent=0) for r in new];(BASE/'aspect_ratio_audit.json').write_text(json.dumps(audit,indent=2))
 export(rows)
 counts={k:len(v) for k,v in groups.items()};(B/'regional_audit_after.json').write_text(json.dumps(dict(basis='Depicted location, not artist nationality. Broad historical-region grouping.',groups=groups,counts=counts),indent=2))
 for op in operations:assert sha(ROOT/op['path'])==op['after_sha256']
 for r in rows:
  im=Image.open(BASE/'staged'/r['staged_file']);assert im.size==(1024,768) and im.mode=='RGBA'
  assert Image.open(WORK/'display'/f"{r['slot']:02}.png").size==(1250,500)
 before=json.loads((B/'regional_audit_before.json').read_text())['counts'];report=['# Global loading artwork: 100 screens','32 additions, selected by depicted geography. Battles and military subjects remain prominent, with trade, transport, strategic passes and political centres providing context. Existing 68 images retained.','| Depicted region | Before | Now |','|---|---:|---:|']+[f'| {k} | {before[k]} | {v} |' for k,v in counts.items()]
 report+=['','New sources are public domain or explicitly CC BY 4.0. Wellcome Collection and APK photograph credits, licence links and modifications are included in every ZIP and installed credits file. A few contemporary watercolours and prints supplement the paintings; media are listed individually.','The previously user-approved Night Train (64) retains its existing unverified reproduction-rights note; this pass does not claim every pre-existing file has newly cleared rights.','Display panels are 1250×500, uniformly scaled from consciously placed 2.50:1 crops. Small labels have 60% transparent backgrounds. Game textures remain 1024×768 with the established stretch compensation and dark footer. Low-resolution sources are identified in the register; export dimensions do not imply additional source detail.','All 300 installed files match the manifest. All 32 new crops were visually inspected. Post-change in-game rendering has not been tested. The preceding metadata is preserved in revision10_before_global_expansion.']
 (BASE/'README.md').write_text('\n\n'.join(report),encoding='utf-8');(B/'REGIONAL_REBALANCE.md').write_text('\n\n'.join(report),encoding='utf-8')
 print('Installed 100 screens; all 300 copies verified. Galleries and both ZIPs regenerated. '+str(counts))

if __name__=='__main__':install() if '--install' in sys.argv else build()
