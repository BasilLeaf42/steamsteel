from PIL import Image,ImageDraw
from pathlib import Path
p=Path('data/ui/units/moors');n=['mor_askar_early','mor_askar_mid','mor_askar_high','mor_makhzen_early','mor_makhzen_mid','mor_makhzen_high','mor_abid_early','mor_abid_mid','mor_rif_early','mor_rif_mid','mor_rif_high','mor_makhzen_cav_early','mor_makhzen_cav_mid','mor_makhzen_cav_high','mor_tribal_levy','mor_guich_cavalry','mor_hajjana','mor_general_staff'];o=Image.new('RGB',(576,384),'#504b3e');d=ImageDraw.Draw(o)
for i,x in enumerate(n):
 im=Image.open(p/f'#{x}.tga').convert('RGBA').resize((72,96));xx=(i%6)*96+12;yy=(i//6)*128;o.paste(im,(xx,yy),im);d.text((i%6*96+2,yy+98),x.replace('mor_','')[:15],fill='white')
o.resize((432,288)).save('tools/_inspect_morocco_cards.jpg',quality=82)