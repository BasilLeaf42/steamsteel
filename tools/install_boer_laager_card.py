from pathlib import Path
from collections import deque
from PIL import Image
import json, shutil, struct

ROOT=Path(__file__).resolve().parents[1]
card=ROOT/'data/ui/units/teu/#boer_wagon.tga'
archive=ROOT/'tools/card_source_archive/boers_before_laager_card_replacement_20260916'
archive.mkdir(parents=True,exist_ok=True)
if not (archive/card.name).exists(): shutil.copy2(card,archive/card.name)
(archive/'original_members.json').write_text(json.dumps({'archived_from':'data/ui/units/teu','members':['boer_wagon']},indent=2),encoding='utf-8')

master=ROOT/'tools/card_generation_sources/boer_laager_20260916_master.png'
im=Image.open(master).convert('RGBA'); w,h=im.size
cw=min(w,(h*3)//4); ch=(cw*4)//3
if ch>h: ch=h; cw=(ch*3)//4
x=(w-cw)//2; y=(h-ch)//2; crop=(x,y,x+cw,y+ch); im=im.crop(crop)
px=im.load(); W,H=im.size; q=deque(); seen=set()
for xx in range(W): q.extend(((xx,0),(xx,H-1)))
for yy in range(H): q.extend(((0,yy),(W-1,yy)))
def bg(c):
 r,g,b,a=c
 return a>0 and r>=145 and g>=135 and b>=105 and max(r,g,b)-min(r,g,b)<=95
while q:
 xx,yy=q.popleft()
 if (xx,yy) in seen: continue
 seen.add((xx,yy))
 if not bg(px[xx,yy]): continue
 px[xx,yy]=(184,173,143,255)
 if xx:q.append((xx-1,yy))
 if xx+1<W:q.append((xx+1,yy))
 if yy:q.append((xx,yy-1))
 if yy+1<H:q.append((xx,yy+1))
final=im.resize((48,64),Image.Resampling.LANCZOS).convert('RGBA')
fp=final.load()
for p in ((0,0),(47,0),(0,63),(47,63)): fp[p]=(184,173,143,255)
card_win=Path('\\\\?\\'+str(card))
final.save(card_win,format='TGA')

reg_path=ROOT/'tools/historical_card_sources.json'; reg=json.loads(reg_path.read_text(encoding='utf-8'))
reg=[e for e in reg if e.get('id')!='boer_wagon']
reg.append({
 'id':'boer_wagon','group_id':'boer_laager_20260916','unit_type':'boer_wagon',
 'card_file':'data/ui/units/teu/#boer_wagon.tga','faction':'teu','name':'Laer',
 'role':'defensive wagon fort','weapon':'Pattern 1853 Enfield rifle-musket',
 'source_url':'https://commons.wikimedia.org/wiki/File:Draught_Bullocks_just_captured_by_Mounted_Infantry_from_a_Boer_Laager_on_the_Modder_(Feb._19),_S._Africa,_RP-F-F09169.jpg',
 'source_file':'tools/historical_card_refs/boer_laager_modder_1901.jpg',
 'source_title':'Draught Bullocks just captured by Mounted Infantry from a Boer Laager on the Modder',
 'creator':'Underwood & Underwood; Rijksmuseum','source_date':'1901','licence':'CC0 / public domain',
 'depicted_subject':'Boer Laager transport and draught-wagon context on the Modder River',
 'mapping_note':'Historical Boer laager wagon controls the wagon form; generated composition matches the loaded pale covered-wagon model and shows riflemen clearly above the wagon bed with complete rifles and no underground clipping.',
 'pose_source_id':'','status':'card-approved',
 'generated_file':'tools/card_generation_sources/boer_laager_20260916_master.png','crop_box':list(crop)})
reg_path.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

d=card_win.read_bytes()
assert struct.unpack_from('<HH',d,12)==(48,64) and d[16]==32
assert all(final.getpixel(p)==(184,173,143,255) for p in ((0,0),(47,0),(0,63),(47,63)))
print('Installed and registered new 48x64 RGBA Boer Laager tactical card.')
