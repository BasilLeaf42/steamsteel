from PIL import Image,ImageDraw
from pathlib import Path
import json
R=Path.cwd();d=R/'data/ui/units/cru';bg=(184,173,143,255)
def fit(src,dst):
 im=Image.open(src).convert('RGBA'); box=im.getchannel('A').getbbox() or (0,0,*im.size); im=im.crop(box); w,h=im.size
 if w/h>.75:
  nw=int(h*.75); left=max(0,(w-nw)//2); im=im.crop((left,0,left+nw,h))
 else:
  nh=int(w/.75); im=im.crop((0,0,w,min(h,nh)))
 im.thumbnail((48,64),Image.Resampling.LANCZOS); out=Image.new('RGBA',(48,64),bg); out.alpha_composite(im,((48-im.width)//2,max(0,64-im.height))); out.save(dst)
fit(R/'tools/card_generation_sources/siam_naval_skirmisher_20260918.png',d/'#siam_sea.tga')
fit(R/'tools/card_generation_sources/siam_sword_cavalry_20260918.png',d/'#siam_sword_cav.tga')
rp=R/'tools/historical_card_sources.json';reg=json.loads(rp.read_text(encoding='utf-8-sig')); entries=reg if isinstance(reg,list) else reg.setdefault('entries',[]); entries[:]=[x for x in entries if x.get('unit') not in ('siam_sea','siam_sword_cav') and x.get('unit_type') not in ('siam_sea','siam_sword_cav')];entries += [
 {'unit':'siam_sea','faction':'Siam','role':'kneeling rifle skirmisher','weapon':'Remington Rolling Block M1867 rifle','source_url':'https://commons.wikimedia.org/wiki/File:Siamese_Soldiers_in_Chiang_Kham_1885_Haw_Wars.png','attribution':'Historical photograph of Royal Siamese Army soldiers in Chiang Kham','date':'1885','license':'public-domain historical photograph; Commons source page','depicted_subject':'Royal Siamese soldiers during the Haw Wars','local_reference':'tools/historical_card_refs/siamese_soldiers_chiang_kham_1885.png','pose_source_id':'kneel_aim_photo_1871','generated_master':'tools/card_generation_sources/siam_naval_skirmisher_20260918.png','approximation':'The national period source controls ethnicity and Siamese presentation; the loaded white naval uniform controls clothing; approved pool controls kneeling rifle mechanics.','approved':True,'status':'card-approved'},
 {'unit':'siam_sword_cav','faction':'Siam','role':'sword cavalry','weapon':'curved cavalry sabre only','source_url':'https://commons.wikimedia.org/wiki/File:Bangkok_-_mounted_Siamese_cavalryman;_palace_in_background_LCCN2004707846.jpg','attribution':'William Henry Jackson / Library of Congress','date':'1895','license':'no known restrictions on publication','depicted_subject':'Mounted Siamese cavalryman in Bangkok','local_reference':'tools/historical_card_refs/siam_cavalryman_1895.jpg','generated_master':'tools/card_generation_sources/siam_sword_cavalry_20260918.png','approximation':'Mounted pose and national identity follow the period photograph; visible weapon follows the sword-only siam_general mesh.','approved':True,'status':'card-approved'}]
rp.write_text(json.dumps(reg,indent=2,ensure_ascii=False),encoding='utf-8')
print('Installed skirmisher and sword-cavalry tactical cards.')