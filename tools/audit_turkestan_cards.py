from pathlib import Path
from PIL import Image, ImageDraw
import io, subprocess

names = ['kok_spears', 'turkmen_inf', 'ghulja_inf', 'buk_guard', 'kashgar_inf', 'kok_inf', 'kok_cav', 'kok_royal_cav', 'uyghur_camel_cav', 'camel_wagon']
out = Image.new('RGBA', (96 * len(names), 148), (40, 40, 40, 255))
draw = ImageDraw.Draw(out)
for i, name in enumerate(names):
    card = Image.open(Path('data/ui/units/cuman') / f'#{name}.tga').convert('RGBA').resize((96, 128))
    out.paste(card, (i * 96, 0))
    draw.text((i * 96 + 2, 132), name, fill='white')
out.save(r'C:\Users\kwoks\.codex\visualizations\2026\09\12\01a09417-2b02-79c1-ac26-19f8f616b95f\turkestan_card_audit.png')

compare = Image.new('RGBA', (192, 148), (40, 40, 40, 255))
current = Image.open(Path('data/ui/units/cuman/#turkmen_inf.tga')).convert('RGBA').resize((96, 128))
original = Image.open(io.BytesIO(subprocess.check_output(['git', 'show', 'HEAD:data/ui/units/cuman/#turkmen_inf.tga']))).convert('RGBA').resize((96, 128))
compare.paste(original, (0, 0)); compare.paste(current, (96, 0))
ImageDraw.Draw(compare).text((2, 132), 'HEAD / current', fill='white')
compare.save(r'C:\Users\kwoks\.codex\visualizations\2026\09\12\01a09417-2b02-79c1-ac26-19f8f616b95f\turkestan_card_compare.png')

camel_compare = Image.new('RGBA', (192, 148), (40, 40, 40, 255))
camel_current = Image.open(Path('data/ui/units/cuman/#camel_wagon.tga')).convert('RGBA').resize((96, 128))
camel_original = Image.open(io.BytesIO(subprocess.check_output(['git', 'show', 'HEAD:data/ui/units/cuman/#camel_wagon.tga']))).convert('RGBA').resize((96, 128))
camel_compare.paste(camel_original, (0, 0)); camel_compare.paste(camel_current, (96, 0))
ImageDraw.Draw(camel_compare).text((2, 132), 'HEAD / current', fill='white')
camel_compare.save(r'C:\Users\kwoks\.codex\visualizations\2026\09\12\01a09417-2b02-79c1-ac26-19f8f616b95f\turkestan_camel_wagon_compare.png')
