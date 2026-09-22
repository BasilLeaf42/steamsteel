"""Install only reviewed paintings, with archived originals and exact verification."""
import json
import hashlib
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

rows = json.loads((BASE / 'source_register.json').read_text(encoding='utf-8'))
originals = json.loads((BASE / 'archive/original_members.json').read_text())
baseline = {r['path']: r for r in originals}
assert len(rows) == 62 and {r['slot'] for r in rows} == set(range(1, 63))
assert len({r['staged_sha256'] for r in rows}) == 62
assert Counter(r['licence'] for r in rows) == {'Public domain': 58, 'CC0': 4}
assert len(originals) == 184
for r in originals:
    assert digest(ROOT / r['path']) == r['sha256'], f"Changed since archive: {r['path']}"
    assert digest(BASE / 'archive' / r['archive']) == r['sha256']

# All eight formatted contact sheets were visually inspected before installation.
review = 'All 62 images inspected in formatted_01.jpg through formatted_08.jpg; proportions, framing and readability accepted. Portraits retain side margins.'
targets = ['data/loading_screen', 'data/loading_screen/load_steamsteel', 'data/loading_screen/load_althis']
operations = []
for r in rows:
    assert r['medium_verified'] and r['source_visual_review'] == 'passed'
    source = BASE / 'staged' / r['staged_file']
    assert digest(source) == r['staged_sha256']
    assert digest(BASE / 'sources' / f"{r['slot']:02}.image") == r['source_sha256']
    with Image.open(source) as im:
        assert im.size == (1024, 768) and im.mode == 'RGBA'
        with Image.open(BASE / 'archive' / (r['original_runtime_sha256'] + '.tga')) as old:
            assert im.crop((0, 490, 1024, 768)).tobytes() == old.convert('RGBA').crop((0, 490, 1024, 768)).tobytes()
    r['final_visual_review'] = 'passed'
    r['final_visual_review_notes'] = review
    for folder in targets:
        relative = folder + '/' + r['staged_file']
        previous = baseline.get(relative)
        if previous is None:
            assert r['slot'] == 19 and folder != targets[0]
            assert not (ROOT / relative).exists()
        operations.append(dict(path=relative, before_sha256=previous['sha256'] if previous else None,
                               archive=previous['archive'] if previous else None, after_sha256=r['staged_sha256']))

(BASE / 'source_register.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
for op in operations:
    shutil.copy2(BASE / 'staged' / Path(op['path']).name, ROOT / op['path'])
for op in operations:
    assert digest(ROOT / op['path']) == op['after_sha256']
    with Image.open(ROOT / op['path']) as im:
        assert im.size == (1024, 768) and im.mode == 'RGBA'
        im.load()
for folder in targets:
    shutil.copy2(BASE / 'ARTWORK_CREDITS.md', ROOT / folder / 'ARTWORK_CREDITS.md')
manifest = dict(installed_at=datetime.now(timezone.utc).isoformat(), screens=62, copies_verified=186,
                visual_review=review, engine_launch_tested=False, operations=operations)
(BASE / 'installation_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
gallery = BASE / 'gallery.html'
page = gallery.read_text(encoding='utf-8')
page = page.replace('<h1>Period oil paintings</h1>', '<h1>Period oil paintings</h1><p><strong>Installed: all 62 screens.</strong> Runtime, Steam &amp; Steel and alternate-history source sets are synchronized. All 186 textures verified; in-game launch not tested.</p>')
gallery.write_text(page, encoding='utf-8')
(BASE / 'README.md').write_text('''# Installed loading-screen paintings

All 62 numbered screens now use distinct, sourced period oil paintings (1807–1908).
Commons file-specific rights records: 58 public domain, 4 CC0.

- Review `gallery.html` for before/after comparisons and subject substitutions.
- `ARTWORK_CREDITS.md` records artists, dates, sources, rights and medium evidence.
- `source_register.json` records source and output hashes, crop boxes and visual review.
- Installed in runtime, `load_steamsteel`, and `load_althis`: 186 verified TGA files.
- 1024×768, 32-bit RGBA, RLE TGA. Original lower 278 rows preserved exactly.
- Paintings retain their aspect ratio and complete composition, with neutral margins.
- All 62 formatted paintings visually reviewed. File decode, hashes and mirror equality passed.
- The game has not been launched for an engine-level check.

## Originals and rollback

`archive/original_members.json` maps 184 original file paths to 62 archived originals.
`installation_manifest.json` records every installed path and before/after hash.
For rollback, first verify installed hashes against that manifest; restore archived bytes to
their original paths. The two source-set screen 19 files had no previous file and should be
removed on rollback. Do not overwrite later user edits without reviewing them.
''', encoding='utf-8')
print('Installed 62 paintings across 3 sets; all 186 textures verified. Original lower text area preserved. 184 originals archived. Game launch not tested.')
