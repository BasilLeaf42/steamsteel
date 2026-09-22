from PIL import Image
from pathlib import Path
d=Path('data/ui/units/cru');bg=(184,173,143,255)
for n in ['siam_sea','siam_sword_cav']:
 im=Image.open(d/f'#{n}.tga').convert('RGBA'); assert im.size==(48,64) and im.mode=='RGBA'; assert im.getpixel((0,0))==bg
out=Image.new('RGB',(768,512),(45,40,32));out.paste(Image.open(d/'#siam_sea.tga').convert('RGB').resize((384,512),Image.Resampling.NEAREST),(0,0));out.paste(Image.open(d/'#siam_sword_cav.tga').convert('RGB').resize((384,512),Image.Resampling.NEAREST),(384,0));out.save('tools/siam_extension_card_audit.jpg',quality=85);print('card format pass')