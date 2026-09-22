from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1]
j=json.loads((R/'tools/all_tactical_card_background_audit_20260923.json').read_text())
rows=[r for r in j['rows'] if '/#' in r['path'].replace('\\','/')]
rows.sort(key=lambda r:r['foreign_border'],reverse=True); rows=rows[:160]
sheet=Image.new('RGB',(10*150,16*92),(38,34,29));d=ImageDraw.Draw(sheet)
for i,r in enumerate(rows):
 p=R/r['path']; im=Image.open(p).convert('RGB');x=i%10*150;y=i//10*92
 sheet.paste(im,(x,y));d.text((x+50,y+2),p.parent.name[:11],fill='white');d.text((x+50,y+13),p.stem[1:18],fill='white')
sheet.save(R/'tools/tactical_card_background_outliers_20260923.png')
