"""Install the Qajar banner while retaining Persian face BC3 blocks."""

from __future__ import annotations

import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DONOR = ROOT / "data/unit_models/_Units/attachments/textures/per_rugbxx.texture"
FLAG_DDS = ROOT / "tools/mesh_work/qajar_bearer/dds/qaj_standard_flag.dds"
OUTPUT = ROOT / "data/unit_models/_Units/bnw/textures/qaj_standard_flag.texture"


def main() -> None:
    donor = DONOR.read_bytes()
    generated = FLAG_DDS.read_bytes()
    donor_dds = bytearray(donor[48:])
    assert donor_dds[:4] == generated[:4] == b"DDS "
    height, width = struct.unpack_from("<II", donor_dds, 12)
    gen_height, gen_width = struct.unpack_from("<II", generated, 12)
    mip_count = struct.unpack_from("<I", donor_dds, 28)[0]
    assert (width, height) == (gen_width, gen_height) == (1024, 1024)
    assert donor_dds[84:88] == generated[84:88] == b"DXT5"
    assert mip_count == struct.unpack_from("<I", generated, 28)[0]
    donor_offset = generated_offset = 128
    for level in range(mip_count):
        mip_width, mip_height = max(1, width >> level), max(1, height >> level)
        blocks_w, blocks_h = max(1, (mip_width + 3) // 4), max(1, (mip_height + 3) // 4)
        x0, x1 = 8 // (1 << level), (504 + (1 << level) - 1) // (1 << level)
        block0, block1 = max(0, x0 // 4), min(blocks_w, (x1 + 3) // 4)
        row_size = blocks_w * 16
        for row in range(blocks_h):
            start, end = row * row_size + block0 * 16, row * row_size + block1 * 16
            donor_dds[donor_offset + start:donor_offset + end] = generated[generated_offset + start:generated_offset + end]
        level_size = blocks_h * row_size
        donor_offset += level_size
        generated_offset += level_size
    assert donor_offset == len(donor_dds) == len(generated)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(donor[:48] + donor_dds)
    (OUTPUT.parent / "qaj_standard_flag_n.texture").write_bytes(
        (ROOT / "data/unit_models/_Units/attachments/textures/blank_norm.texture").read_bytes()
    )
    print("Installed Qajar banner with all non-flag Persian face blocks preserved.")


if __name__ == "__main__":
    main()
