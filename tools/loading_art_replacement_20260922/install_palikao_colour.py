import json,shutil,zipfile
from datetime import datetime,timezone
from PIL import Image
from compact_labels_bakufu import BASE,ROOT,WORK,sha,export
rev=BASE/'revision11_before_colour_replacement';r=json.loads((rev/'candidate.json').read_text(encoding='utf-8'));rows=json.loads((BASE/'source_register.json').read_text(encoding='utf-8'));m=json.loads((BASE/'installation_manifest.json').read_text())
for op in m['operations']:assert sha(ROOT/op['path'])==op['after_sha256']
r['final_visual_review']='passed';r['museum_label']['visual_review']='passed: full-size wide crop inspected; principal sails and waterfront preserved'
for labelled,folder in [(False,'display_clean'),(True,'display')]:
 image=Image.open(rev/('candidate.png' if labelled else 'candidate_clean.png')).convert('RGBA');shutil.copy2(rev/('candidate.png' if labelled else 'candidate_clean.png'),WORK/folder/'100.png')
 base=Image.open(rev/'unlabelled_current'/'Loading_screen_100.tga').convert('RGBA');base.paste(image.resize((1024,490),Image.Resampling.LANCZOS),(0,0));outfolder='staged' if labelled else 'unlabelled_current';dest=BASE/outfolder/r['staged_file'];base.save(dest,compression='tga_rle',orientation=-1);shutil.copy2(dest,WORK/('staged' if labelled else 'clean')/r['staged_file'])
 if labelled:base.convert('RGB').save(BASE/'previews/100.jpg',quality=95);image.convert('RGB').save(BASE/'previews/100_art.jpg',quality=95)
r['staged_sha256']=sha(BASE/'staged'/r['staged_file']);r['unlabelled_sha256']=sha(BASE/'unlabelled_current'/r['staged_file'])
shutil.copy2(BASE/r['local_source'],BASE/'sources/100.image');shutil.copy2(BASE/r['research_file'],BASE/'sources/100.download.json')
for op in m['operations']:
 if op['path'].endswith('/Loading_screen_100.tga'):
  op['previous_install_sha256']=op['after_sha256'];op['previous_install_archive']='revision11_before_colour_replacement/staged/Loading_screen_100.tga';shutil.copy2(BASE/'staged'/r['staged_file'],ROOT/op['path']);op['after_sha256']=r['staged_sha256']
rows[99]=r;(BASE/'source_register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');m['installed_at']=datetime.now(timezone.utc).isoformat();(BASE/'installation_manifest.json').write_text(json.dumps(m,indent=2))
a=json.loads((BASE/'aspect_ratio_audit.json').read_text());a['items']=[x for x in a['items'] if x['slot']!=100]+[dict(slot=100,crop_box=r['crop_box'],scale_x=1250/1890,scale_y=500/756,ratio_error_percent=0)];(BASE/'aspect_ratio_audit.json').write_text(json.dumps(a,indent=2))
export(rows)
(BASE/'README.md').write_text((rev/'README.md').read_text(encoding='utf-8')+'\n\nScreen 100 now uses the colour oil painting Hong Kong Harbour (late 1850s). Photograph by Bjoertvedt; its cropped and captioned versions are CC BY-SA 4.0. The rejected monochrome Palikiao engraving is archived in revision11_before_colour_replacement.\n',encoding='utf-8')
for op in m['operations']:assert sha(ROOT/op['path'])==op['after_sha256']
for name in ['Steam_and_Steel_Full_Resolution_Cropped_With_Overlays.zip','Steam_and_Steel_Paintings_No_Overlays.zip']:
 with zipfile.ZipFile(BASE/'discord_share'/name) as z:
  s=z.read('ARTWORK_CREDITS.md').decode();assert len(z.namelist())==101 and 'Bjoertvedt' in s and 'https://creativecommons.org/licenses/by-sa/4.0/' in s
print('Screen 100 replaced in all three game folders. 300 hashes verified; galleries and ZIPs refreshed with ShareAlike attribution.')
