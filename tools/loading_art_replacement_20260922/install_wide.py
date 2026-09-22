import json, shutil, hashlib
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageOps
from research import BASE

ROOT=BASE.parent.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.loads((BASE/'source_register.json').read_text(encoding='utf-8'))
previous=json.loads((BASE/'revision1/installation_manifest.json').read_text())
assert len(rows)==62 and {r['slot'] for r in rows}==set(range(1,63))
assert len({r['staged_sha256'] for r in rows})==62
# Detect intervening edits before touching any installed file.
for op in previous['operations']:
    assert sha(ROOT/op['path'])==op['after_sha256'],op['path']
    assert sha(BASE/'revision1/staged'/Path(op['path']).name)==op['after_sha256']
for r in rows:
    staged=BASE/'staged'/r['staged_file'];assert sha(staged)==r['staged_sha256']
    with Image.open(staged) as im:
        assert im.mode=='RGBA' and im.size==(1024,768)
        original=Image.open(BASE/'archive'/(r['original_runtime_sha256']+'.tga')).convert('RGBA')
        assert im.crop((0,490,1024,768)).tobytes()==original.crop((0,490,1024,768)).tobytes()
        if r['slot']==19:
            assert sha(staged)==r['original_runtime_sha256']
        else:
            assert r['medium_verified'] and r['licence'] in ['Public domain','CC0']
            source=BASE/'sources'/f"{r['slot']:02}.image";assert sha(source)==r['source_sha256']
            expected=ImageOps.exif_transpose(Image.open(source)).convert('RGB').crop(r['crop_box']).resize((1024,490),Image.Resampling.LANCZOS)
            assert im.crop((0,0,1024,490)).convert('RGB').tobytes()==expected.tobytes()
    r['final_visual_review']='passed'
    r['final_visual_review_notes']='All eight wide_review sheets inspected; nine crops repositioned and re-inspected in adjusted_review.jpg. Original-resolution upgrades checked separately. No added margins or frames; Plevna unchanged.'
operations=[]
for prior in previous['operations']:
    n=int(Path(prior['path']).stem.rsplit('_',1)[1]);r=rows[n-1]
    shutil.copy2(BASE/'staged'/r['staged_file'],ROOT/prior['path'])
    op=dict(prior);op.update(previous_install_sha256=prior['after_sha256'],previous_install_archive='revision1/staged/'+r['staged_file'],after_sha256=r['staged_sha256']);operations.append(op)
for op in operations:
    assert sha(ROOT/op['path'])==op['after_sha256']
    with Image.open(ROOT/op['path']) as im:im.load();assert im.mode=='RGBA' and im.size==(1024,768)
(BASE/'source_register.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
manifest=dict(installed_at=datetime.now(timezone.utc).isoformat(),screens=62,new_oil_paintings=61,preserved_original_slots=[19],copies_verified=186,engine_launch_tested=False,operations=operations)
(BASE/'installation_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
for folder in ['data/loading_screen','data/loading_screen/load_steamsteel','data/loading_screen/load_althis']:
    shutil.copy2(BASE/'ARTWORK_CREDITS.md',ROOT/folder/'ARTWORK_CREDITS.md')
gallery=BASE/'gallery.html';page=gallery.read_text(encoding='utf-8').replace('Crop review in progress.','Installed and verified: 61 individually composed wide crops plus the unchanged original Plevna surrender screen. All 186 runtime and launcher-source copies match. Game launch not tested.')
gallery.write_text(page,encoding='utf-8')
(BASE/'README.md').write_text('''# Installed loading artwork — wide crop revision

61 oil paintings plus the original Plevna surrender screen (slot 19), restored byte-for-byte at the user's request.

The paintings fill the original 1024×490 artwork panel edge to edge. Each crop has a recorded subject-specific position and has been visually inspected. Eight unsuitable compositions were replaced with other paintings. The original lower 278 rows remain unchanged in each 1024×768 RGBA RLE TGA texture.

- `gallery.html`: current full-width crops, original comparisons, source links and crop reasons.
- `ARTWORK_CREDITS.md`: current artists, dates, licences, subject differences and medium evidence.
- `source_register.json`: final crop boxes, hashes and visual review.
- `installation_manifest.json`: all 186 verified installed files and before/after hashes.
- `archive/original_members.json`: the original pre-replacement assets and their member paths.
- `revision1/`: previous fitted paintings and installation metadata, retained for rollback.

The installation covers runtime, `load_steamsteel` and `load_althis`. Pixel comparisons verified that every artwork panel exactly matches its approved resized crop, with no generated fill, border or mat. All lower text areas match their originals; Plevna matches its entire archived original. The game was not launched for an engine-level check.

For rollback, first compare current files to the installation manifest to protect later edits. The manifest records the prior installation archive for every file; the original archive retains the assets from before either replacement pass.
''',encoding='utf-8')
print('Installed and verified 186 files: 61 wide crops and original Plevna, in all three sets. Exact panel and lower-area pixel comparisons passed.')
