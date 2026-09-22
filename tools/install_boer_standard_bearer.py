"""Install complete texconv output into verified Medieval II texture containers."""
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
TEXTURES = ROOT / "data/unit_models/_Units/bnw/textures"
WORK = ROOT / "tools/mesh_work/boer_bearer"

def install(name: str, donor_name: str) -> None:
    donor = (TEXTURES / donor_name).read_bytes()
    generated = (WORK / "dds" / f"{name}.dds").read_bytes()
    base = donor[48:]
    if base[:4] != b"DDS " or generated[:4] != b"DDS ":
        raise ValueError("invalid DDS")
    h, w = struct.unpack_from("<II", base, 12)
    gh, gw = struct.unpack_from("<II", generated, 12)
    if (w, h) != (gw, gh) or base[84:88] != b"DXT5" or generated[84:88] != b"DXT5":
        raise ValueError("DDS layout mismatch")
    if struct.unpack_from("<I", base, 28)[0] != struct.unpack_from("<I", generated, 28)[0]:
        raise ValueError("mipmap count mismatch")
    if len(base) != len(generated):
        raise ValueError("DDS payload size mismatch")
    out = TEXTURES
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.texture").write_bytes(donor[:48] + generated)

def main() -> None:
    install("boer_standard_flag", "csa_standard_flag.texture")
    install("boer_standard_flag_n", "csa_standard_flag_n.texture")
    print("Installed Boer Vierkleur texture containers.")

if __name__ == "__main__":
    main()
