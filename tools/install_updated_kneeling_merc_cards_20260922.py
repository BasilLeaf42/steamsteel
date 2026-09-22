from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, shutil

ROOT=Path(__file__).resolve().parents[1]
BACKUP=ROOT/'tools/backup_before_updated_kneeling_merc_cards_20260922'
REGISTER=ROOT/'tools/historical_card_sources.json'
CANON=(184,173,143)
DONORS={
 'merc_apache_inf':('data/ui/units/aztecs/#arg_cazadores_early.tga','arg_cazadores_early','Closest approved kneeling match for the loaded blue-uniform rifleman model.'),
 'merc_us_farmers':('data/ui/units/denmark/#per_montoneros_early.tga','per_montoneros_early','Closest approved kneeling irregular-rifleman composition for Filibusters.'),
 'merc_maori_musketeers':('data/ui/units/moors/#mor_rif_early.tga','mor_rif_early','Closest approved kneeling indigenous irregular-musketeer composition.'),
}

for folder in ('mercs','slave'):
 (BACKUP/folder).mkdir(parents=True,exist_ok=True)
for unit in DONORS:
 for folder in ('mercs','slave'):
  current=ROOT/f'data/ui/units/{folder}/#{unit}.tga'
  if not current.is_file():raise SystemExit(f'missing current card {current}')
  archived=BACKUP/folder/current.name
  if not archived.exists():shutil.copy2(current,archived)

for unit,(rel,_,_) in DONORS.items():
 donor=ROOT/rel
 with Image.open(donor) as im:
  card=im.convert('RGBA')
 if card.size!=(48,64):raise SystemExit(f'wrong donor dimensions {donor}: {card.size}')
 if card.getpixel((0,0))[:3]!=CANON or card.getpixel((47,0))[:3]!=CANON:raise SystemExit(f'noncanonical donor top edge {donor}')
 for folder in ('mercs','slave'):
  card.save(ROOT/f'data/ui/units/{folder}/#{unit}.tga',format='TGA',bits=32,compression='tga_rle')

register=json.loads(REGISTER.read_text(encoding='utf-8'))
by_unit={x.get('unit_type'):x for x in register}
new=[]
for unit,(rel,donor_unit,note) in DONORS.items():
 donor=by_unit.get(donor_unit)
 if not donor:raise SystemExit(f'missing approved donor register {donor_unit}')
 rid=f'{unit}_approved_kneeling_donor_20260922'
 existing=next((x for x in register if x.get('id')==rid),None)
 entry={k:v for k,v in donor.items() if k not in ('id','group_id','unit_type','shared_members','card_file','faction','name','mapping_note','crop_box')}
 entry.update({
  'id':rid,'group_id':'remaining_mercenary_kneeling_cards_20260922','unit_type':unit,
  'card_file':f'data/ui/units/mercs/#{unit}.tga','faction':'mercs / slave',
  'name':unit.replace('merc_','').replace('_',' ').title(),'role':'kneeling firearm skirmisher',
  'mapping_note':note+' Reused at the user’s explicit direction for the non-critical residual mercenary pool; no gameplay or model mapping changed.',
  'donor_unit_type':donor_unit,'donor_card_file':rel,'status':'card-approved','crop_box':[0,0,48,64]
 })
 if existing:register[register.index(existing)]=entry
 else:register.append(entry)
 new.append(entry)
REGISTER.write_text(json.dumps(register,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

sheet=Image.new('RGB',(360,170),(34,31,27));draw=ImageDraw.Draw(sheet);font=ImageFont.load_default()
for i,unit in enumerate(DONORS):
 with Image.open(ROOT/f'data/ui/units/mercs/#{unit}.tga') as im:sheet.paste(im.convert('RGB').resize((96,128)),(i*120,0))
 draw.text((i*120,132),unit.replace('merc_','')[:18],fill='white',font=font)
sheet.save(ROOT/'tools/updated_kneeling_merc_cards_contact_sheet.png')
print('Installed and registered three approved kneeling mercenary cards in both UI folders.')
