"""Build a Boer-compatible bearer atlas with a two-sided Transvaal Vierkleur."""
from pathlib import Path
import io
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ATTACH = ROOT / "data/unit_models/_Units/attachments/textures"
TEXTURES = ROOT / "data/unit_models/_Units/bnw/textures"
WORK = ROOT / "tools/mesh_work/boer_bearer"

def open_texture(path: Path) -> Image.Image:
    raw = path.read_bytes()
    if raw[48:52] != b"DDS ":
        raise ValueError(f"invalid texture container: {path}")
    return Image.open(io.BytesIO(raw[48:])).convert("RGBA")

def main() -> None:
    # The transplanted French bearer UVs place the cloth in the bottom-right
    # 512x512 square of france_flag.texture.  Starting from an unrelated atlas
    # made the cloth sample fragments of several materials/banners.
    image = open_texture(TEXTURES / "france_flag.texture")
    draw = ImageDraw.Draw(image)
    x0, y0, x1, y1 = 512, 512, 1023, 1023
    green, red, white, blue = (0, 98, 51, 255), (190, 25, 35, 255), (245, 241, 222, 255), (25, 48, 100, 255)
    stripe = (y1 - y0 + 1) // 3
    draw.rectangle((x0, y0, x1, y0 + stripe - 1), fill=red)
    draw.rectangle((x0, y0 + stripe, x1, y0 + stripe * 2 - 1), fill=white)
    draw.rectangle((x0, y0 + stripe * 2, x1, y1), fill=blue)
    draw.rectangle((x0, y0, x0 + 127, y1), fill=green)
    out = WORK / "tga"
    out.mkdir(parents=True, exist_ok=True)
    image.save(out / "boer_standard_flag.tga")
    open_texture(TEXTURES / "france_flag_n.texture").save(out / "boer_standard_flag_n.tga")
    mesh_out = ROOT / "data/unit_models/_Units/off/boer_standard_bearer_lod0.mesh"
    mesh_out.write_bytes((ROOT / "data/unit_models/_Units/off/csa_standard_bearer_lod0.mesh").read_bytes())
    print("Built Boer bearer mesh clone and Vierkleur atlas source.")

if __name__ == "__main__":
    main()
