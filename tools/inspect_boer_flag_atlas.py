from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / 'data/unit_models/_Units/bnw/textures'
OUT = ROOT / 'tools/mesh_work/boer_bearer/atlas_inspection'
OUT.mkdir(parents=True, exist_ok=True)

names = ['csa_standard_flag', 'boer_standard_flag', 'csa_standard_flag_n', 'boer_standard_standard_flag_n']
names[3] = 'boer_standard_flag_n'
images = {}
for name in names:
    raw = (TEX / f'{name}.texture').read_bytes()
    dds = OUT / f'{name}.dds'
    dds.write_bytes(raw[48:])
    im = Image.open(dds).convert('RGBA')
    im.save(OUT / f'{name}.png')
    images[name] = im

base = images['csa_standard_flag']
boer = images['boer_standard_flag']
diff = ImageChops.difference(base.convert('RGB'), boer.convert('RGB'))
bbox = diff.getbbox()

thumbs = []
for name in ('csa_standard_flag', 'boer_standard_flag'):
    im = images[name].copy()
    if bbox:
        ImageDraw.Draw(im).rectangle(bbox, outline=(255, 0, 255, 255), width=max(1, im.width // 256))
    im.thumbnail((512, 512))
    thumbs.append(im)

sheet = Image.new('RGBA', (sum(i.width for i in thumbs), max(i.height for i in thumbs)), (30, 30, 30, 255))
x = 0
for im in thumbs:
    sheet.alpha_composite(im, (x, 0))
    x += im.width
sheet.save(OUT / 'csa_vs_boer_flag.png')
print(f'size={base.size} difference_bbox={bbox}')
print(OUT / 'csa_vs_boer_flag.png')
