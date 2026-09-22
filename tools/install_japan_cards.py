from pathlib import Path
from collections import deque
import math, re, shutil
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
CARDS=ROOT/'data/ui/units/saxons'
GEN=Path(r'C:\Users\kwoks\.codex\generated_images\01a09417-2b02-79c1-ac26-19f8f616b95f')
CAN=(184,173,143,255)

exact={
'korean_archers':('slave','korean_archers'),'Korean_Byeolgigun':('mercs','Korean_Byeolgigun'),'Korean_Gimagungsu':('mercs','Korean_Gimagungsu'),
'Japan_Ainu_Geberu':('mercs','Japan_Ainu_Geberu'),'Japan_Ainu_Minieru':('mercs','Japan_Ainu_Minieru'),'Japan_Ainu_Teppo':('mercs','Japan_Ainu_Teppo'),
'Japan_Heimin_Partisans_Geberu':('mercs','Japan_Heimin_Partisans_Geberu'),'Japan_Heimin_Partisans_Minieru':('mercs','Japan_Heimin_Partisans_Minieru'),
'Japan_Shizoku':('mercs','Japan_Shizoku'),'Japan_Teppotai_Merc':('mercs','Japan_Teppotai_Merc'),
'korean_rifles_mercs':('mercs','korean_rifles_mercs'),'korean_cav_mercs':('mercs','korean_cav_mercs')}
generated={
'Japan_Hijikata_Toshizo':'exec-306060dc-2b3b-418c-9d0d-217861e2026d.png','Japan_Itagaki_Taisuke':'exec-8b6224b3-9eee-4c86-afef-de3a259ab075.png',
'Japan_Kondo_Isami':'exec-b5a05d63-87e2-4dd5-a45b-0a6a7d6f1fee.png','Japan_Matsudaira_Katamori':'exec-8e9ee400-a53f-4d9e-a8f7-5edd48e1b311.png',
'Japan_Saigo_Takamori_1860':'exec-e368fc6f-d26f-478c-8842-17bd390a9bef.png','Japan_Sakamoto_Ryoma':'exec-c64b834d-bd6d-47cc-8d2b-7c503d032616.png',
'Japan_Tokugawa_Yoshinobu':'exec-ab62ac57-db08-4d65-8bf4-839f2fe303f8.png','Japan_Enomoto_Takeaki':'exec-8c9b4e11-fe7c-4f36-b318-29b6cba38d6b.png',
'Japan_Jules_Brunet':'exec-e6928f41-7da2-4c11-af65-dcd273b94dbd.png','Japan_Takeda_Ayasaburo':'exec-7291e34c-ed34-4771-8ae9-5d517735a191.png',
'Japan_Bodyguard_Retainers':'exec-fc5fc2d9-7f4d-4653-8a00-483dbfd45e47.png','Korean_Musketeers':'exec-998a503d-03db-40aa-b717-cdcb2edfbf51.png',
'Korean_Pikemen':'exec-3bb92b2c-56a3-41ba-a0aa-e2e92c985d93.png','Japan_Ezo_Rikuguntai_1900':'exec-5005a976-3339-4f88-a827-c8752b77bdd3.png',
'Japan_Ezo_Rikuguntai_1905':'exec-9812f098-29c2-42d3-b7f4-32914c91e1b9.png','Japan_Goshimpei_Hohei_1880':'exec-7c21ef4c-181f-4f06-86d6-fe0068ee8cde.png',
'Japan_Goshimpei_Kihei_1880':'exec-83c70947-bdb2-4f00-a664-f3b27ded9533.png','Japan_Goshimpei_Kihei_1900':'exec-e466abf3-e293-4a0c-903b-ae89dd7227c0.png',
'Japan_Goshimpei_Kihei_1905':'exec-9d6dfcd4-c38d-44d8-9385-34f2d6a8fc64.png','Japan_Hokuchin_Butai_1890':'exec-bb6e51ac-54e3-43f6-b89d-20cc3c7c5b2d.png',
'Japan_Hokuchin_Butai_1900':'exec-a1a18d03-ded6-4f62-85e2-4b5ca76623ac.png','Japan_Ronin':'exec-83484194-0ed5-4060-879d-0a510ebc2ce7.png',
'Japan_Kaga_Hoheitai':'exec-0adfba99-c1da-451b-a873-ce4f207c825c.png','Japan_Kenyotai':'exec-e1baf702-cbce-4ca1-aec2-0b01b3379056.png',
'Japan_Kijutai':'exec-d7fc5879-b46b-4917-85d1-ee3ee4eb4d90.png','Japan_Matsushiro_Hoheitai':'exec-1a31b109-510b-4d40-b8de-cc9c435ccaa1.png',
'Japan_Rikusentai_1880':'exec-fb0ff4aa-9564-4de3-896e-6c89c3fba38b.png','Japan_Rikusentai_1900':'exec-e074ef78-39b9-4187-88a3-3b5d26ebda68.png',
'Japan_Ryukihei_1880':'exec-98e55660-2e67-4c7b-b811-326fd6eaa9d2.png','Japan_Ryukihei_1900':'exec-785ac1d6-aaaf-4e3e-87ed-0ce3d7d0b4e0.png',
'Japan_Ryukihei_1905':'exec-c6b80aa5-dd68-45bc-8a69-dbb02f2269e0.png','Japan_Tondenhei_1880':'exec-5b642709-07b8-479f-8a37-52ca4710830f.png',
'Japan_Yukantai':'exec-4ee12ea2-4b98-4876-a38f-70237865a7e1.png'}
shared={'Japan_Ezo_Rikuguntai_1890':'Japan_Ezo_Rikuguntai_1880','Japan_Goshimpei_Kihei_1890':'Japan_Goshimpei_Kihei_1880',
'Japan_Hokuchin_Butai_1905':'Japan_Hokuchin_Butai_1900','Japan_Ishin_Shishi':'Japan_Ronin','Japan_Rikusentai_1890':'Japan_Rikusentai_1900','Japan_Ryukihei_1890':'Japan_Ryukihei_1880'}

def dist(a,b): return math.sqrt(sum((a[i]-b[i])**2 for i in range(3)))
def canonicalize(im, generated=False):
    im=im.convert('RGBA')
    if min(p[3] for p in im.getdata())<255:
        bg=Image.new('RGBA',im.size,CAN); bg.alpha_composite(im); return bg
    if all(dist(im.getpixel(p),CAN)<5 for p in [(0,0),(im.width-1,0)]): return im
    px=im.load(); corners=[px[0,0],px[im.width-1,0],px[0,im.height-1],px[im.width-1,im.height-1]]
    ref=tuple(round(sum(c[i] for c in corners)/4) for i in range(4)); tol=60 if generated else 28
    q=deque(); seen=set()
    for x in range(im.width): q.extend([(x,0),(x,im.height-1)])
    for y in range(im.height): q.extend([(0,y),(im.width-1,y)])
    while q:
        x,y=q.popleft()
        if (x,y) in seen or dist(px[x,y],ref)>tol: continue
        seen.add((x,y))
        for n in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=n[0]<im.width and 0<=n[1]<im.height and n not in seen and dist(px[n[0],n[1]],px[x,y])<45: q.append(n)
    out=im.copy(); op=out.load()
    for p in seen: op[p]=CAN
    return out
def master(path):
    im=Image.open(path).convert('RGBA'); w,h=im.size; target=.75
    if w/h>target:
        nw=round(h*target); x=(w-nw)//2; im=im.crop((x,0,x+nw,h))
    elif w/h<target:
        nh=round(w/target); im=im.crop((0,0,w,nh))
    im=im.resize((48,64),Image.Resampling.LANCZOS)
    return canonicalize(im,True)
def save(key,im): im.convert('RGBA').save(CARDS/f'#{key}.tga',format='TGA',bits=32,compression='tga_rle')

for key,(faction,src) in exact.items(): shutil.copy2(ROOT/f'data/ui/units/{faction}/#{src}.tga',CARDS/f'#{key}.tga')
for key,src in generated.items():
    p=GEN/src
    if not p.is_file(): raise SystemExit(f'missing generated master {p}')
    save(key,master(p))
for key,src in shared.items(): shutil.copy2(CARDS/f'#{src}.tga',CARDS/f'#{key}.tga')

edu=(ROOT/'data/tow_steamsteel/export_descr_unit.txt').read_text(encoding='utf-8',errors='replace')
keys=[]
for block in re.split(r'(?=^type\s+)',edu,flags=re.M):
    if re.search(r'(?:^ownership|^era [012]).*\bsaxons\b',block,flags=re.M):
        m=re.search(r'^dictionary\s+([^;\s]+)',block,flags=re.M)
        if m: keys.append(m.group(1))
for key in keys:
    p=CARDS/f'#{key}.tga'
    if not p.is_file(): raise SystemExit(f'missing roster card {key}')
    im=Image.open(p).convert('RGBA')
    if im.size!=(48,64): raise SystemExit(f'bad dimensions {key}: {im.size}')
    save(key,canonicalize(im))
print(f'Installed and normalized {len(keys)} Japanese roster cards; generated {len(generated)}, exact donors {len(exact)}, shared-model copies {len(shared)}.')
