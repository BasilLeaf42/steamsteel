from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
cards = sorted((ROOT / 'data/ui/units').glob('#*.tga'))
cards += sorted((ROOT / 'data/ui/units').glob('*/*5lb*.tga'))
cards += sorted((ROOT / 'data/ui/units').glob('*/*12lb*.tga'))
cards += sorted((ROOT / 'data/ui/units').glob('*/*armstrong*.tga'))
cards = list(dict.fromkeys(cards))
sheet = Image.new('RGB', (600, ((len(cards)+5)//6)*100), (55,50,43))
d = ImageDraw.Draw(sheet)
for i,p in enumerate(cards):
    im=Image.open(p).convert('RGBA')
    bg=Image.new('RGBA',im.size,(184,173,143,255)); bg.alpha_composite(im)
    x=(i%6)*100;y=(i//6)*100
    sheet.paste(bg.convert('RGB'),(x,y)); d.text((x,y+65),p.stem[:15],fill='white')
sheet.save(ROOT/'tools/qing_artillery_donor_contact_20260923.png')

soe = ROOT.parent/'soe/data/ui/units/byzantium/#Hand_Gunners.tga'
im=Image.open(soe).convert('RGBA')
bg=Image.new('RGBA',im.size,(184,173,143,255)); bg.alpha_composite(im)
bg.resize((240,320),Image.Resampling.NEAREST).save(ROOT/'tools/qing_beiyang_soe_donor_20260923.png')
