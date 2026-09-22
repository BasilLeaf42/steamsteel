from pathlib import Path
from PIL import Image
import io,re,struct
ROOT=Path(__file__).resolve().parents[1]
model=(ROOT/'data/unit_models/battle_models.modeldb').read_text(encoding='utf-8')
def mb(name):
 m=re.search(rf'^{len(name)} {re.escape(name)}\s*$[\s\S]*?(?=^\d+ [^\s;]+\s*$\n\d+ \d+\s*$|\Z)',model,re.M)
 assert m,name; return m.group(0)
b=mb('boer_standard_bearer')
for p in ('unit_models/_Units/off/boer_standard_bearer_lod0.mesh',
          'unit_models/_Units/bnw/textures/csa_captain.texture',
          'unit_models/_Units/bnw/textures/csa_captain_n.texture',
          'unit_models/_Units/bnw/textures/boer_standard_flag.texture',
          'unit_models/_Units/bnw/textures/boer_standard_flag_n.texture',
          'unit_sprites/milan_Italian_MAA_sprite.spr'):
 assert f'{len(p)} {p}' in b,p
assert '3 teu' in b and 'tra_grd_1g.texture' not in b
assert (ROOT/'data/unit_models/_Units/off/boer_standard_bearer_lod0.mesh').read_bytes()==(ROOT/'data/unit_models/_Units/off/csa_standard_bearer_lod0.mesh').read_bytes()
raw=(ROOT/'data/unit_models/_Units/off/boer_standard_bearer_lod0.mesh').read_bytes()
for g in (b'big_flag',b'primaryactive0',b'head'): assert g in raw
for p in ('data/unit_models/_Units/bnw/textures/boer_standard_flag.texture','data/unit_models/_Units/bnw/textures/boer_standard_flag_n.texture'):
 d=(ROOT/p).read_bytes(); assert d[48:52]==b'DDS '
flag=(ROOT/'data/unit_models/_Units/bnw/textures/boer_standard_flag.texture').read_bytes()
csa=(ROOT/'data/unit_models/_Units/bnw/textures/csa_standard_flag.texture').read_bytes()
assert flag != csa, 'Boer flag has regressed to the Confederate atlas'
assert flag[48:] == (ROOT/'tools/mesh_work/boer_bearer/dds/boer_standard_flag.DDS').read_bytes(), 'active Boer flag mip chain differs from generated DDS'
flag_n=(ROOT/'data/unit_models/_Units/bnw/textures/boer_standard_flag_n.texture').read_bytes()
assert flag_n[48:] == (ROOT/'tools/mesh_work/boer_bearer/dds/boer_standard_flag_n.DDS').read_bytes(), 'active Boer flag normal mip chain differs from generated DDS'
im=Image.open(io.BytesIO(flag[48:])).convert('RGB')
samples=(im.getpixel((560,560)),im.getpixel((760,560)),im.getpixel((760,760)),im.getpixel((760,950)))
assert samples[0][1] > samples[0][0] and samples[0][1] > samples[0][2], samples
assert samples[1][0] > samples[1][1] * 1.5, samples
assert min(samples[2]) > 180, samples
assert samples[3][2] > samples[3][0] and samples[3][2] > samples[3][1], samples
for n in ('csa_lancer_te','boer_mounted_kommando_early','boer_mounted_kommando_mid','boer_mounted_kommando_high'):
 d=(ROOT/f'data/ui/units/teu/#{n}.tga').read_bytes()
 assert struct.unpack_from('<HH',d,12)==(48,64) and d[16]==32,n
laager=(ROOT/'data/ui/units/teu/#boer_wagon.tga').read_bytes()
assert struct.unpack_from('<HH',laager,12)==(48,64) and laager[16]==32
print('Boer bearer package and RGBA general/carbine tactical-card formats validated.')
