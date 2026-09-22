"""Build the Moroccan bearer attachment atlas without recolouring face or pole."""
from pathlib import Path
from PIL import Image, ImageDraw
import io, math, shutil

R=Path(__file__).resolve().parents[1]
T=R/'data/unit_models/_Units'; B=T/'bnw/textures'; A=R/'tools/texture_source_archive/morocco_before_bearer_atlas_fix_20260915'
A.mkdir(parents=True,exist_ok=True)
target=B/'mor_standard_flag.texture'; normal=B/'mor_standard_flag_n.texture'
for p in (target,normal):
 if not (A/p.name).exists(): shutil.copy2(p,A/p.name)

def load(p):
 raw=p.read_bytes(); return raw[:48],Image.open(io.BytesIO(raw[48:])).convert('RGBA')
def save(header,im,p):
 out=io.BytesIO(); im.save(out,format='DDS',pixel_format='DXT5'); p.write_bytes(header+out.getvalue())

header,base=load(T/'attachments/textures/per_rugbxx.texture')
_,donor=load(B/'france_flag.texture')
# The transplanted donor group was normalised into renderer UV x=.02..49,
# y=.40..99. Transfer the complete donor atlas there so its face/pole/cloth
# sub-islands remain distinct. The Moroccan source face stays on the native
# per_rugbxx atlas outside this rectangle.
box=(20,410,502,1014); donor=donor.resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
# The donor cloth occupies its lower-right quadrant. Replace only that cloth.
d=ImageDraw.Draw(donor); l,t,r,b=donor.width//2,donor.height//2,donor.width-1,donor.height-1
d.rectangle((l,t,r,b),fill=(174,20,32,255))
cx,cy=(l+r)//2,(t+b)//2; radius=min(r-l,b-t)*.28
pts=[]
for i in range(5):
 a=-math.pi/2+i*4*math.pi/5; pts.append((cx+math.cos(a)*radius,cy+math.sin(a)*radius))
d.line(pts+[pts[0]],fill=(0,100,55,255),width=max(5,donor.width//45),joint='curve')
base.paste(donor,(box[0],box[1])); save(header,base,target)

nh,nbase=load(T/'attachments/textures/blank_norm.texture')
_,ndonor=load(B/'france_flag_n.texture'); ndonor=ndonor.resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
nbase.paste(ndonor,(box[0],box[1])); save(nh,nbase,normal)
print('Built Moroccan bearer atlas: native face/gear, donor pole, red cloth with green pentagram.')
