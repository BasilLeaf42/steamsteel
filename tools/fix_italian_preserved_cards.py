from pathlib import Path
from PIL import Image
from standardize_card_backgrounds import CANONICAL

ROOT = Path(__file__).resolve().parents[1]
assignments = {
    ROOT / 'data/ui/units/venice/#ita_arditi_high.tga': ROOT / 'data/ui/units/mercs/#merc_it_arditi.tga',
    ROOT / 'data/ui/units/venice/#ita_libici_high.tga': ROOT / 'data/ui/units/slave/#libya_inf.tga',
}
for destination, source in assignments.items():
    foreground = Image.open(source).convert('RGBA')
    image = Image.alpha_composite(Image.new('RGBA', foreground.size, CANONICAL), foreground)
    image.save(destination, format='TGA', bits=32, compression='tga_rle')
print('Installed and normalized preserved Arditi and Libyan infantry cards.')
