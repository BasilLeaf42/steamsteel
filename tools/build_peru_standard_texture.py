"""Build the Peruvian bearer's two-sided flag texture on the verified Latin-American bearer atlas."""
from __future__ import annotations
import io
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
BNW=ROOT/'data/unit_models/_Units/bnw/textures'
EMBLEM=ROOT/'data/models_strat/textures/#banner_symbol_denmark.tga'

def open_texture(path:Path)->Image.Image:
    raw=path.read_bytes()
    if raw[48:52]!=b'DDS ': raise ValueError(f'Not a wrapped DDS texture: {path}')
    return Image.open(io.BytesIO(raw[48:])).convert('RGBA')

def save_texture(image:Image.Image, source:Path, dest:Path)->None:
    raw=source.read_bytes(); out=io.BytesIO()
    image.save(out,format='DDS',pixel_format='DXT5')
    dest.write_bytes(raw[:48]+out.getvalue())

def main()->None:
    body=BNW/'mex_standard_bearer.texture'
    (BNW/'per_standard_bearer.texture').write_bytes(body.read_bytes())
    source=BNW/'mex_standard_flag.texture'; image=open_texture(source)
    draw=ImageDraw.Draw(image); box=(512,512,1023,1023)
    red=(181,25,36,255); white=(242,239,224,255)
    draw.rectangle(box,fill=white)
    third=(box[2]-box[0]+1)//3
    draw.rectangle((box[0],box[1],box[0]+third-1,box[3]),fill=red)
    draw.rectangle((box[2]-third+1,box[1],box[2],box[3]),fill=red)
    emblem=Image.open(EMBLEM).convert('RGBA')
    alpha=emblem.getchannel('A').getbbox()
    if alpha: emblem=emblem.crop(alpha)
    emblem.thumbnail((105,150),Image.Resampling.LANCZOS)
    x=(box[0]+box[2]-emblem.width)//2; y=(box[1]+box[3]-emblem.height)//2
    image.alpha_composite(emblem,(x,y))
    save_texture(image,source,BNW/'per_standard_flag.texture')
    normal=BNW/'mex_standard_flag_n.texture'
    (BNW/'per_standard_flag_n.texture').write_bytes(normal.read_bytes())
    print('Built two-sided Peruvian red-white-red standard with the existing Peruvian faction emblem.')

if __name__=='__main__': main()
