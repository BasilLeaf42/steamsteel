from PIL import Image,ImageDraw
from pathlib import Path
p=Path('data/ui/units/aztecs');names=['arg_line_early','arg_line_mid','arg_line_high','arg_national_guard_early','arg_national_guard_mid','arg_national_guard_high','arg_cavalry_early','arg_cavalry_mid','arg_cavalry_high'];out=Image.new('RGB',(432,288),'#504b3e');d=ImageDraw.Draw(out)
for i,n in enumerate(names):
 im=Image.open(p/f'#{n}.tga').convert('RGBA').resize((96,128));x=(i%3)*144+24;y=(i//3)*96;out.paste(im,(x,y),im);d.text((i%3*144+2,y+78),n,fill='white')
out.resize((324,216)).save('tools/_inspect_argentina_regenerated.jpg',quality=82)