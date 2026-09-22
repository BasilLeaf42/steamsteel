from pathlib import Path
from PIL import Image, ImageDraw

names=['indian_bow_cav','indian_spear_cav','Sikh_heavy_cavalry','indian_spears','indian_heavy_banduqchis','indian_new_musk','india_sepoy','sikh_gen','sikh_warriors','indian_fanatic','indian_ele','india_militia']
out=Image.new('RGBA',(96*len(names),148),(40,40,40,255)); d=ImageDraw.Draw(out)
for i,n in enumerate(names):
 p=Path('data/ui/units/bulga')/f'#{n}.tga'; im=Image.open(p).convert('RGBA').resize((96,128));out.paste(im,(i*96,0));d.text((i*96+2,132),n[:15],fill='white')
out.save(r'C:\Users\kwoks\.codex\visualizations\2026\09\12\01a09417-2b02-79c1-ac26-19f8f616b95f\indian_cards_audit.png')
