"""Safely place an existing alpha-cutout tactical card over the canonical background.

This tool deliberately refuses fully opaque inputs. Opaque cards require a reviewed,
unit-specific foreground mask; broad colour keying is not permitted here.
"""
from pathlib import Path
import argparse, json, shutil
from PIL import Image

CANONICAL = (184, 173, 143, 255)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', type=Path)
    ap.add_argument('targets', nargs='+', type=Path)
    ap.add_argument('--backup-dir', required=True, type=Path)
    ap.add_argument('--report', required=True, type=Path)
    args = ap.parse_args()

    source = Image.open(args.source).convert('RGBA')
    if source.size != (48, 64):
        raise SystemExit(f'Expected 48x64 source, got {source.size}')
    alpha = source.getchannel('A')
    amin, amax = alpha.getextrema()
    if amin == 255:
        raise SystemExit('Refusing opaque input: a reviewed unit-specific mask is required')

    background = Image.new('RGBA', source.size, CANONICAL)
    output = Image.alpha_composite(background, source)
    src = source.load(); out = output.load()
    opaque_checked = 0
    for y in range(64):
        for x in range(48):
            if src[x, y][3] == 255:
                opaque_checked += 1
                if out[x, y][:3] != src[x, y][:3]:
                    raise SystemExit(f'Opaque foreground changed at {(x,y)}')
            if src[x, y][3] == 0 and out[x, y] != CANONICAL:
                raise SystemExit(f'Transparent background failed at {(x,y)}')

    args.backup_dir.mkdir(parents=True, exist_ok=True)
    installed=[]
    for target in args.targets:
        target = target.resolve()
        if target.exists():
            backup = args.backup_dir / f'{target.parent.name}-{target.name}'
            if not backup.exists(): shutil.copy2(target, backup)
        target.parent.mkdir(parents=True, exist_ok=True)
        output.save(target, format='TGA', bits=32, compression='tga_rle')
        installed.append(str(target))

    report = {
        'source': str(args.source.resolve()), 'targets': installed,
        'canonical_background': '#B8AD8F', 'source_alpha_range': [amin, amax],
        'opaque_foreground_pixels_verified_unchanged': opaque_checked,
        'method': 'alpha_composite_only', 'opaque_colour_keying_used': False,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__': main()
