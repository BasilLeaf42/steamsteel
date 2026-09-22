from pathlib import Path
import re, shutil
ROOT=Path(__file__).resolve().parents[1]
mount=ROOT/'data/descr_mount.txt'
text=mount.read_text(encoding='utf-8')
m=re.search(r'^type\s+boer_wagon\s*$[\s\S]*?(?=^type\s+|\Z)',text,re.M)
if not m: raise RuntimeError('boer_wagon block missing')
block=m.group(0)
block,n=re.subn(r'^(rider_offset\s+[-0-9.]+),\s*[-0-9.]+,',r'\1, 0.5,',block,flags=re.M)
if n!=6: raise RuntimeError(f'expected 6 rider offsets, found {n}')
mount.write_text(text[:m.start()]+block+text[m.end():],encoding='utf-8',newline='')
donor=ROOT/'data/ui/units/milan/#csa_cav.tga'
for era in ('early','mid','high'):
    shutil.copy2(donor,ROOT/f'data/ui/units/teu/#boer_mounted_kommando_{era}.tga')
print('Set six Laager Y offsets to 0.5 and installed mounted carbine cards.')
