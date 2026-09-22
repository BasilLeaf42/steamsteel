from PIL import Image,ImageDraw
from pathlib import Path
p=Path('data/ui/units/moors');n=['mor_makhzen_early','mor_makhzen_mid','mor_makhzen_high','mor_abid_early','mor_abid_mid','mor_rif_early','mor_rif_mid','mor_rif_high','mor_hajjana'];o=Image.new('RGB',(432,288),'#504b3e');d=ImageDraw.Draw(o)
for i,x in enumerate(n):
 im=Image.open(p/f'#{x}.tga').convert('RGBA').resize((96,128));xx=(i%3)*144+24;yy=(i//3)*96;o.paste(im,(xx,yy),im);d.text((i%3*144+2,yy+78),x.replace('mor_',''),fill='white')
o.resize((324,216)).save('tools/_inspect_morocco_common_corrections.jpg',quality=82)