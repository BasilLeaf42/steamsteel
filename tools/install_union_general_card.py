import json
from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / 'tools' / 'historical_card_sources.json'
UNIT = 'uni_general_staff'
CANON = (184, 173, 143)

records = json.loads(REGISTRY.read_text(encoding='utf-8'))
record = next((x for x in records if x.get('id') == UNIT), None)
if not record or record.get('status') != 'approved':
    raise SystemExit('Refusing installation: Union General and Staff source mapping is not approved')
for field in ('source_url', 'source_file', 'source_title', 'creator', 'source_date',
              'licence', 'depicted_subject', 'mapping_note', 'generated_file'):
    if not record.get(field):
        raise SystemExit(f'Refusing installation: missing source field {field}')

source = ROOT / record['generated_file']
if not source.is_file() or not (ROOT / record['source_file']).is_file():
    raise SystemExit('Refusing installation: registered source files are missing')

image = Image.open(source).convert('RGB')
crop = tuple(record.get('crop_box', ()))
if len(crop) != 4 or crop[2] <= crop[0] or crop[3] <= crop[1]:
    raise SystemExit('Refusing installation: invalid crop box')
image = image.crop(crop)
if image.width * 4 != image.height * 3:
    raise SystemExit('Refusing installation: crop is not 3:4')

# The generated figure is correct, but the generator added a gentle parchment
# vignette. Flood only the smooth connected background from the image edges and
# replace it with the project's exact canonical colour, leaving the figure intact.
px = image.load()
w, h = image.size
seen = bytearray(w * h)
queue = deque()

def plausible_background(rgb):
    r, g, b = rgb
    return 145 <= r <= 215 and 135 <= g <= 205 and 105 <= b <= 180 and 3 <= r-g <= 28 and 12 <= g-b <= 48

for x in range(w):
    for y in (0, h - 1):
        if plausible_background(px[x, y]):
            queue.append((x, y)); seen[y*w+x] = 1
for y in range(h):
    for x in (0, w - 1):
        if plausible_background(px[x, y]) and not seen[y*w+x]:
            queue.append((x, y)); seen[y*w+x] = 1

while queue:
    x, y = queue.popleft()
    base = px[x, y]
    for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
        if nx < 0 or ny < 0 or nx >= w or ny >= h:
            continue
        idx = ny*w+nx
        if seen[idx]:
            continue
        value = px[nx, ny]
        if plausible_background(value) and max(abs(value[i]-base[i]) for i in range(3)) <= 7:
            seen[idx] = 1
            queue.append((nx, ny))

flat = Image.new('RGB', image.size, CANON)
flat_px = flat.load()
for y in range(h):
    for x in range(w):
        if not seen[y*w+x]:
            flat_px[x, y] = px[x, y]

card = flat.resize((48, 64), Image.Resampling.LANCZOS).convert('RGBA')
card.putalpha(255)
# Collapse one-pixel resampling drift in connected background pixels back to
# the exact canonical colour without touching the dark figure or equipment.
cp = card.load()
cw, ch = card.size
edge = deque()
marked = bytearray(cw * ch)
for x in range(cw):
    for y in (0, ch - 1):
        if sum((cp[x, y][i] - CANON[i]) ** 2 for i in range(3)) <= 100:
            edge.append((x, y)); marked[y*cw+x] = 1
for y in range(ch):
    for x in (0, cw - 1):
        if not marked[y*cw+x] and sum((cp[x, y][i] - CANON[i]) ** 2 for i in range(3)) <= 100:
            edge.append((x, y)); marked[y*cw+x] = 1
while edge:
    x, y = edge.popleft()
    cp[x, y] = (*CANON, 255)
    for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
        if 0 <= nx < cw and 0 <= ny < ch and not marked[ny*cw+nx] and sum((cp[nx, ny][i] - CANON[i]) ** 2 for i in range(3)) <= 100:
            marked[ny*cw+nx] = 1
            edge.append((nx, ny))
target = ROOT / record['card_file']
target.parent.mkdir(parents=True, exist_ok=True)
card.save(target, format='TGA')

check = Image.open(target)
if check.size != (48, 64) or check.mode != 'RGBA':
    raise SystemExit('Installed card failed format validation')
print(f'Installed {target.relative_to(ROOT)} from approved historical source mapping.')
