from pathlib import Path
from PIL import Image,ImageDraw

R=Path(__file__).resolve().parents[1]
patterns=['*siam_inf*','*siam_sea*','*fra_spahis*','*merc_fra_for_cav*','*fra_cuirassiers*','*fra_garde*']
paths=[]
for pat in patterns: paths += list((R/'data/ui/units').glob(f'*/#{pat}.tga'))
paths=list(dict.fromkeys(sorted(paths)))
sheet=Image.new('RGB',(800,((len(paths)+7)//8)*110),(40,37,32));d=ImageDraw.Draw(sheet)
for i,p in enumerate(paths):
 im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,(184,173,143,255));bg.alpha_composite(im)
 x=i%8*100;y=i//8*110;sheet.paste(bg.convert('RGB'),(x,y));d.text((x,y+65),p.parent.name[:10],fill='white');d.text((x,y+76),p.stem[1:14],fill='white')
sheet.save(R/'tools/reported_tactical_cards_20260923.png')
print(len(paths))
