const fs = require('fs');
const p = require('path').join(__dirname, 'install_union_scout_card.py');
let s = fs.readFileSync(p, 'utf8');
const before = "card = flat.resize((48, 64), Image.Resampling.LANCZOS).convert('RGBA')\ncard.putalpha(255)\ntarget = ROOT / record['card_file']";
const after = `card = flat.resize((48, 64), Image.Resampling.LANCZOS).convert('RGBA')
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
target = ROOT / record['card_file']`;
if (!s.includes(before)) throw new Error('Installer insertion point missing');
fs.writeFileSync(p, s.replace(before, after));
console.log('Patched final-size canonical background normalization.');
