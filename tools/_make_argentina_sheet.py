from PIL import Image,ImageDraw
from pathlib import Path
p=Path('data/ui/units/aztecs'); names=['arg_line_early','arg_line_mid','arg_line_high','arg_national_guard_early','arg_national_guard_mid','arg_national_guard_high','arg_cazadores_early','arg_cazadores_mid','arg_tiradores_high','arg_cavalry_early','arg_cavalry_mid','arg_cavalry_high','arg_lancers_early','arg_lancers_mid','arg_frontier_gauchos','arg_general_staff']
out=Image.new('RGB',(4*160,4*120),'#504b3e');d=ImageDraw.Draw(out)
for i,n in enumerate(names):
 im=Image.open(p/f'#{n}.tga').convert('RGBA').resize((96,128)); x=(i%4)*160+32;y=(i//4)*120;out.paste(im,(x,y),im);d.text((i%4*160+3,y+98),n,fill='white')
out.save('tools/_inspect_argentina_cards.png')