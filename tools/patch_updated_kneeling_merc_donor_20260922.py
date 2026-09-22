from pathlib import Path
p=Path(__file__).with_name('install_updated_kneeling_merc_cards_20260922.py')
s=p.read_text(encoding='utf-8')
old="'merc_apache_inf':('data/ui/units/france/#fra_chasseurs_early.tga','fra_chasseurs_early','Closest approved kneeling match for the loaded blue-uniform rifleman model.')"
new="'merc_apache_inf':('data/ui/units/aztecs/#arg_cazadores_early.tga','arg_cazadores_early','Closest approved kneeling match for the loaded blue-uniform rifleman model.')"
if old not in s:raise SystemExit('Apache donor target missing')
p.write_text(s.replace(old,new),encoding='utf-8')
