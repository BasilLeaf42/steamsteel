from pathlib import Path
from PIL import Image
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TEXCONV = ROOT / "tools/IWTE_current_release/IWTE_v26_08_A/texconv.exe"


def extract_dds(texture: Path, dds: Path) -> bytes:
    raw = texture.read_bytes()
    offset = raw.index(b"DDS ")
    dds.write_bytes(raw[offset:])
    return raw[:offset]


def compile_and_install(texture: Path, png: Path, header: bytes, work: Path) -> None:
    subprocess.run(
        [str(TEXCONV), "-f", "R8G8B8A8_UNORM", "-m", "0", "-y", "-o", str(work), str(png)],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    dds = work / (png.stem + ".DDS")
    if not dds.exists():
        dds = work / (png.stem + ".dds")
    payload = dds.read_bytes()
    texture.write_bytes(header + payload)


def recolour_scarlet_to_khaki(image: Image.Image) -> Image.Image:
    out = image.convert("RGBA")
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            # The atlas contains both scarlet and khaki tunics. Restrict this
            # conversion to saturated red cloth; medals, skin and equipment
            # fall outside this mask.
            if r > 45 and r > g * 1.45 and r > b * 1.35 and g < 115:
                # Match the existing khaki half of the atlas while retaining
                # the scarlet cloth's fold shading.
                light = max(0.48, min(1.12, r / 105.0))
                px[x, y] = (
                    int(151 * light),
                    int(126 * light),
                    int(78 * light),
                    a,
                )
    return out


def replace_obstructive_beard(image: Image.Image) -> Image.Image:
    out = image.convert("RGBA")
    # These two 256x224 face slots share the same UV layout. Replace only the
    # mouth-obscuring beard slot with the adjacent clean-shaven donor slot.
    clean = out.crop((0, 274, 256, 498))
    out.paste(clean, (256, 274))
    return out


def main() -> None:
    work = ROOT / "tools/_british_atlas_build"
    work.mkdir(parents=True, exist_ok=True)

    body = ROOT / "data/unit_models/_Units/eng/textures/eng_col_2g.texture"
    body_dds = work / "eng_col_2g_source.dds"
    body_header = extract_dds(body, body_dds)
    subprocess.run([str(TEXCONV), "-ft", "png", "-y", "-o", str(work), str(body_dds)], check=True, stdout=subprocess.DEVNULL)
    body_png = work / "eng_col_2g_source.PNG"
    fixed_body = work / "eng_col_2g_fixed.png"
    recolour_scarlet_to_khaki(Image.open(body_png)).save(fixed_body)
    compile_and_install(body, fixed_body, body_header, work)

    # The Imperial Camel Corps uses a separate mounted atlas with the same
    # unintended scarlet/khaki randomization.
    mounted = ROOT / "data/unit_models/_Units/eng/textures/eng_cav_2g.texture"
    mounted_dds = work / "eng_cav_2g_source.dds"
    mounted_header = extract_dds(mounted, mounted_dds)
    subprocess.run([str(TEXCONV), "-ft", "png", "-y", "-o", str(work), str(mounted_dds)], check=True, stdout=subprocess.DEVNULL)
    mounted_png = work / "eng_cav_2g_source.PNG"
    fixed_mounted = work / "eng_cav_2g_fixed.png"
    recolour_scarlet_to_khaki(Image.open(mounted_png)).save(fixed_mounted)
    compile_and_install(mounted, fixed_mounted, mounted_header, work)

    faces = ROOT / "data/unit_models/_Units/attachments/textures/whi_gbfrxx.texture"
    face_dds = work / "whi_gbfrxx_source.dds"
    face_header = extract_dds(faces, face_dds)
    subprocess.run([str(TEXCONV), "-ft", "png", "-y", "-o", str(work), str(face_dds)], check=True, stdout=subprocess.DEVNULL)
    face_png = work / "whi_gbfrxx_source.PNG"
    fixed_faces = work / "whi_gbfrxx_fixed.png"
    replace_obstructive_beard(Image.open(face_png)).save(fixed_faces)
    compile_and_install(faces, fixed_faces, face_header, work)


if __name__ == "__main__":
    main()
