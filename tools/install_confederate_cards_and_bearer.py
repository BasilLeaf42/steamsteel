"""Install restored Confederate tactical cards and the native standard bearer."""

from __future__ import annotations

import re
import shutil
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ATTACH = DATA / "unit_models/_Units/attachments/textures"
WORK = ROOT / "tools/mesh_work/confederate_bearer"


def install_flag_texture() -> None:
    donor = (ATTACH / "whi_spusxx.texture").read_bytes()
    generated = (WORK / "dds/csa_standard_flag.dds").read_bytes()
    donor_dds = bytearray(donor[48:])
    if donor_dds[:4] != generated[:4] or generated[:4] != b"DDS ":
        raise ValueError("Invalid DDS payload")
    height, width = struct.unpack_from("<II", donor_dds, 12)
    gen_height, gen_width = struct.unpack_from("<II", generated, 12)
    mip_count = struct.unpack_from("<I", donor_dds, 28)[0]
    if (width, height) != (gen_width, gen_height) or (width, height) != (1024, 1024):
        raise ValueError("Unexpected flag atlas dimensions")
    if donor_dds[84:88] != b"DXT5" or generated[84:88] != b"DXT5":
        raise ValueError("Flag atlas must be DXT5")
    donor_offset = generated_offset = 128
    for level in range(mip_count):
        mip_width, mip_height = max(1, width >> level), max(1, height >> level)
        blocks_w = max(1, (mip_width + 3) // 4)
        blocks_h = max(1, (mip_height + 3) // 4)
        x0, x1 = 8 // (1 << level), (504 + (1 << level) - 1) // (1 << level)
        block0, block1 = max(0, x0 // 4), min(blocks_w, (x1 + 3) // 4)
        row_size = blocks_w * 16
        for row in range(blocks_h):
            start, end = row * row_size + block0 * 16, row * row_size + block1 * 16
            donor_dds[donor_offset + start:donor_offset + end] = generated[generated_offset + start:generated_offset + end]
        size = blocks_h * row_size
        donor_offset += size
        generated_offset += size
    if donor_offset != len(donor_dds) or generated_offset != len(generated):
        raise ValueError("Incomplete mip-chain copy")
    out = DATA / "unit_models/_Units/bnw/textures"
    out.mkdir(parents=True, exist_ok=True)
    (out / "csa_standard_flag.texture").write_bytes(donor[:48] + donor_dds)
    (out / "csa_standard_flag_n.texture").write_bytes((ATTACH / "blank_norm.texture").read_bytes())


def counted(value: str) -> str:
    return f"{len(value)} {value}"


def bearer_entry() -> str:
    mesh = "unit_models/_Units/off/csa_standard_bearer_lod0.mesh"
    body = "unit_models/_Units/csa/textures/csa_grd_1g.texture"
    normal = "unit_models/_Units/attachments/textures/blank_norm.texture"
    flag = "unit_models/_Units/bnw/textures/csa_standard_flag.texture"
    flag_normal = "unit_models/_Units/bnw/textures/csa_standard_flag_n.texture"
    sprite = "unit_sprites/milan_Italian_MAA_sprite.spr"
    lines = [
        counted("csa_standard_bearer"), "1 1", f"{counted(mesh)} 20000", "1", counted("milan"),
        counted(body), counted(normal), counted(sprite), "1", counted("milan"), counted(flag),
        f"{counted(flag_normal)} 0", "4", counted("None"), "9 MTW2_Pike 0", "1",
        counted("MTW2_Pike_primary"), "0", counted("horse"), "18 MTW2_HR_Non_Shield 0", "1",
        counted("MTW2_Sword_Primary"), "0", counted("elephant"), "18 MTW2_Elephant_Crew 0", "1",
        counted("MTW2_Sword_Primary"), "0", counted("camel"), "18 MTW2_HR_Non_Shield 0", "1",
        counted("MTW2_Sword_Primary"), "0", "16 -0.090000004 0 0 -0.34999999 0.80000001 0.60000002",
    ]
    return "\n".join(lines) + "\n"


def install_modeldb() -> None:
    path = DATA / "unit_models/battle_models.modeldb"
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.startswith("22 serialization::archive 3 0 0 0 0 "):
        raise ValueError("Unexpected modeldb header")
    marker = re.compile(r"^19 csa_standard_bearer\s*$", re.M)
    if marker.search(text):
        start = marker.search(text).start()
        end_match = re.search(r"^16 -0\.090000004 0 0\s*$", text[start:], re.M)
        if not end_match:
            raise ValueError("Malformed existing Confederate bearer entry")
        end = start + end_match.end()
        text = text[:start] + bearer_entry().rstrip("\n") + text[end:]
    else:
        header = re.match(r"^(22 serialization::archive 3 0 0 0 0 )(\d+)( 0 0\s*)$", text.split("\n", 1)[0])
        if not header:
            raise ValueError("Could not parse modeldb entry count")
        first, rest = text.split("\n", 1)
        first = f"{header.group(1)}{int(header.group(2)) + 1}{header.group(3)}"
        text = first + "\n" + rest.rstrip("\n") + "\n" + bearer_entry()
    path.write_text(text.replace("\n", "\r\n"), encoding="utf-8", newline="")


BEARER_UNITS = {
    "csa_state_volunteers_early", "csa_state_guard_mid",
    "csa_regulars_early", "csa_regulars_mid",
    "csa_louisiana_tigers", "csa_marines", "csa_sharpshooters",
}


def install_edu_officers() -> None:
    canonical = DATA / "tow_steamsteel/export_descr_unit.txt"
    text = canonical.read_text(encoding="utf-8").replace("\r\n", "\n")
    blocks = re.split(r"(?=^type\s+)", text, flags=re.M)
    found = set()
    for i, block in enumerate(blocks):
        match = re.match(r"^type\s+(\S+)", block)
        if not match or match.group(1) not in BEARER_UNITS:
            continue
        unit = match.group(1)
        found.add(unit)
        block = re.sub(r"^officer\s+csa_standard_bearer\s*\n", "", block, flags=re.M)
        officer = re.search(r"^officer\s+csa_officer\s*$", block, flags=re.M)
        if not officer:
            raise ValueError(f"Missing primary Confederate officer in {unit}")
        block = block[:officer.end()] + "\nofficer          csa_standard_bearer" + block[officer.end():]
        blocks[i] = block
    if found != BEARER_UNITS:
        raise ValueError(f"Missing bearer unit blocks: {sorted(BEARER_UNITS - found)}")
    output = "".join(blocks).replace("\n", "\r\n")
    canonical.write_text(output, encoding="utf-8", newline="")
    (DATA / "export_descr_unit.txt").write_text(output, encoding="utf-8", newline="")


def restore_cards() -> None:
    archive = ROOT / "tools/card_source_archive/confederates_before_standardization"
    target = DATA / "ui/units/milan"
    assignments = {
        "#csa_state_volunteers_early.tga": "#csa_inf.tga",
        "#csa_state_guard_mid.tga": "#csa_militia.tga",
        "#csa_state_guard_high.tga": "#csa_militia.tga",
        "#csa_regulars_early.tga": "#csa_guard.tga",
        "#csa_regulars_mid.tga": "#csa_guard.tga",
        "#csa_regulars_high.tga": "#csa_guard.tga",
        "#csa_louisiana_tigers.tga": "#csa_zouave.tga",
        "#csa_marines.tga": "#gr_inf_mi.tga",
        "#csa_sharpshooters.tga": "#berdan_inf_milan.tga",
        "#csa_state_cavalry.tga": "#us_farmer_cav.tga",
        "#csa_virginia_cavalry.tga": "#csa_cav.tga",
    }
    for destination, source in assignments.items():
        shutil.copy2(archive / source, target / destination)


def update_agents() -> None:
    path = ROOT / "agents.md"
    text = path.read_text(encoding="utf-8")
    old = "No compatible Confederate standard-bearer mesh and flag mapping has yet been verified, so do not substitute a Union or foreign bearer."
    new = ("The verified Confederate foot bearer is `csa_standard_bearer`: it preserves the native `csa_grd_1g` body, faces, and faction texture, "
           "and replaces only the embedded rifle group with the verified `fra_qishou` pole-and-flag geometry mapped to the dedicated two-sided Confederate battle-flag atlas. "
           "Use it as the second officer for Confederate early and mid infantry; late infantry retains only `csa_officer`.")
    if old not in text and new not in text:
        raise ValueError("Confederate bearer policy sentence not found")
    path.write_text(text.replace(old, new), encoding="utf-8", newline="")


def main() -> None:
    install_flag_texture()
    install_modeldb()
    install_edu_officers()
    restore_cards()
    update_agents()
    print("Installed restored Confederate tactical cards and native Confederate standard bearer.")


if __name__ == "__main__":
    main()

