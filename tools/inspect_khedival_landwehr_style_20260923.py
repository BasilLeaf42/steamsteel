from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
paths=[]
for p in (R/'data/ui/units').glob('*/#merc_arab_sailors.tga'): paths.append(p)
for p in (R/'data/ui/units').glob('*/#aus_landwehr_*.tga'): paths.append(p)
sheet=Image.new('RGB',(len(paths)*180,310),(40,36,30)); d=ImageDraw.Draw(sheet)
for i,p in enumerate(paths):
 im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',(48,64),(184,173,143,255));bg.alpha_composite(im)
 sheet.paste(bg.resize((192,256),Image.Resampling.NEAREST).convert('RGB'),(i*180,0))
 d.text((i*180,260),p.parent.name,fill='white'); d.text((i*180,273),p.stem[1:25],fill='white')
sheet.save(R/'tools/khedival_landwehr_style_source_20260923.png')
