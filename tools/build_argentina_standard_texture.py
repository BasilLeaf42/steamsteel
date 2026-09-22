"""Build the Argentine bearer's two-sided flag texture on the verified Latin-American bearer atlas."""
import io
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]; B=ROOT/'data/unit_models/_Units/bnw/textures'
def open_tex(p):
 raw=p.read_bytes(); assert raw[48:52]==b'DDS '; return Image.open(io.BytesIO(raw[48:])).convert('RGBA'),raw[:48]
def save(im,head,p):
 out=io.BytesIO(); im.save(out,format='DDS',pixel_format='DXT5'); p.write_bytes(head+out.getvalue())
body=B/'mex_standard_bearer.texture'; (B/'arg_standard_bearer.texture').write_bytes(body.read_bytes())
im,head=open_tex(B/'mex_standard_flag.texture'); d=ImageDraw.Draw(im); x0,y0,x1,y1=512,512,1023,1023
blue=(105,172,228,255); white=(245,242,224,255); gold=(226,174,39,255); d.rectangle((x0,y0,x1,y1),fill=white); h=(y1-y0+1)//3; d.rectangle((x0,y0,x1,y0+h-1),fill=blue); d.rectangle((x0,y1-h+1,x1,y1),fill=blue)
cx,cy=(x0+x1)//2,(y0+y1)//2; r=42; d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=gold)
for i in range(16):
 import math
 a=math.pi*i/8; r1,r2=48,72; d.line((cx+math.cos(a)*r1,cy+math.sin(a)*r1,cx+math.cos(a)*r2,cy+math.sin(a)*r2),fill=gold,width=8)
save(im,head,B/'arg_standard_flag.texture'); (B/'arg_standard_flag_n.texture').write_bytes((B/'mex_standard_flag_n.texture').read_bytes()); print('Built Argentine standard texture.')
