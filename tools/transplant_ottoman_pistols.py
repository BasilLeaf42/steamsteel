"""Transplant only pistol geometry into the original Ottoman rider mesh binaries.

IWTE full dumps provide verified byte boundaries. The original rider's body, face,
skeleton, and existing vertex records remain byte-for-byte intact; the donor pistol
vertices overwrite the start of the carbine's existing private vertex range and only
the primary weapon triangle group is replaced. The global vertex count and ordering
therefore remain unchanged.
"""

from __future__ import annotations

import io
import math
import re
import struct
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tools" / "mesh_work"


@dataclass
class Group:
    start: int
    name1_end: int
    name2_end: int
    count_end: int
    count: int
    end: int


@dataclass
class Dump:
    vertex_count: int
    top_count_end: int
    arrays: list[tuple[int, int]]  # (count, count_end/data_start)
    primary: Group


POS = re.compile(r"at position =\s*(\d+)")


def pos(line: str) -> int:
    match = POS.search(line)
    if not match:
        raise ValueError(f"No byte position in: {line}")
    return int(match.group(1))


def read_dump(path: Path) -> Dump:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    counts = []
    for line in lines:
        match = re.match(r"\s*(\d+)\s+# number of vertices", line)
        if match:
            counts.append((int(match.group(1)), pos(line)))
    if len(counts) != 8:
        raise ValueError(f"{path}: expected top count plus seven vertex arrays, found {len(counts)}")

    primary_line = next(i for i, line in enumerate(lines) if re.match(r"\s*14\s+primaryactive0\s+#", line))
    start_line = next(i for i in range(primary_line - 1, -1, -1) if "start triangle group" in lines[i])
    name2_line = primary_line + 1
    count_line = primary_line + 2
    end_line = next(i for i in range(count_line + 1, len(lines)) if "end   triangle group" in lines[i])
    count_match = re.match(r"\s*(\d+)\s+# number of triangles", lines[count_line])
    if not count_match:
        raise ValueError(f"{path}: cannot read primary triangle count")
    group = Group(
        pos(lines[start_line]), pos(lines[primary_line]), pos(lines[name2_line]),
        pos(lines[count_line]), int(count_match.group(1)), pos(lines[end_line])
    )
    return Dump(counts[0][0], counts[0][1], counts[1:], group)


def pistol_uv_bounds(donor: bytes, dump: Dump, first: int, last: int):
    _, start = dump.arrays[0]
    values = [struct.unpack_from("<2f", donor, start + i * 8) for i in range(first, last + 1)]
    us = [u - math.floor(u) for u, _ in values]
    vs = [v - math.floor(v) for _, v in values]
    return min(us), max(us), min(vs), max(vs)


def transplant(source_mesh: Path, source_dump: Path, output_mesh: Path,
               donor_mesh: Path, donor_dump: Path, texture_box: tuple[int, int, int, int],
               joint_map: dict[int, int]):
    target = bytearray(source_mesh.read_bytes())
    donor = donor_mesh.read_bytes()
    td = read_dump(source_dump)
    dd = read_dump(donor_dump)
    strides = [8, 8, 12, 4, 4, 4, 4]

    donor_triangle_start = dd.primary.count_end
    donor_indices = list(struct.unpack_from(f"<{dd.primary.count * 3}H", donor, donor_triangle_start))
    first, last = min(donor_indices), max(donor_indices)
    pistol_vertices = last - first + 1
    if pistol_vertices != 487:
        raise ValueError(f"Unexpected pistol vertex span {first}..{last}")
    target_triangle_start = td.primary.count_end
    target_indices = list(struct.unpack_from(f"<{td.primary.count * 3}H", target, target_triangle_start))
    target_first, target_last = min(target_indices), max(target_indices)
    target_span = target_last - target_first + 1
    if target_span < pistol_vertices:
        raise ValueError(f"Target weapon range {target_first}..{target_last} is too small")
    adjusted_indices = [target_first + index - first for index in donor_indices]

    u0, u1, v0, v1 = pistol_uv_bounds(donor, dd, first, last)
    box_x, box_y, box_w, box_h = texture_box

    # Overwrite only carbine-owned slots; no array is resized or reordered.
    for array_index in range(7):
        stride = strides[array_index]
        target_count, target_start = td.arrays[array_index]
        donor_count, donor_start = dd.arrays[array_index]
        if target_count != td.vertex_count or donor_count != dd.vertex_count:
            raise ValueError("Inconsistent mesh vertex array count")
        chunk = bytearray(donor[donor_start + first * stride : donor_start + (last + 1) * stride])

        if array_index == 0:  # UVs: map pistol into an unused patch of the original attachment texture.
            for i in range(pistol_vertices):
                u, v = struct.unpack_from("<2f", chunk, i * stride)
                u, v = u - math.floor(u), v - math.floor(v)
                mapped_u = (box_x + ((u - u0) / (u1 - u0)) * (box_w - 1) + 0.5) / 1024
                mapped_v = (box_y + ((v - v0) / (v1 - v0)) * (box_h - 1) + 0.5) / 1024
                struct.pack_into("<2f", chunk, i * stride, mapped_u, mapped_v)
        elif array_index == 3 and joint_map:  # compressed (bone, weight, bone, weight)
            for i in range(pistol_vertices):
                at = i * stride
                chunk[at] = joint_map.get(chunk[at], chunk[at])
                chunk[at + 2] = joint_map.get(chunk[at + 2], chunk[at + 2])

        target_at = target_start + target_first * stride
        target[target_at : target_at + len(chunk)] = chunk

    # Keep the target group's serialization header/footer, changing only its second
    # name, triangle count, and triangle indices.
    tg = td.primary
    target_triangle_end = tg.count_end + tg.count * 6
    group = bytearray(target[tg.start : tg.name1_end])
    weapon_name = b"swrevolver_01"
    group += struct.pack("<I", len(weapon_name)) + weapon_name
    group += struct.pack("<I", dd.primary.count)
    group += struct.pack(f"<{len(adjusted_indices)}H", *adjusted_indices)
    group += target[target_triangle_end : tg.end]
    target[tg.start : tg.end] = group

    # Byte 0 is the serialized archive-name length (22), not a file-size field.
    # Preserve it from the original mesh; overwriting it produces a file IWTE can
    # inspect but Medieval II crashes on when the battle model is instantiated.
    output_mesh.parent.mkdir(parents=True, exist_ok=True)
    output_mesh.write_bytes(target)
    print(f"Built {output_mesh.relative_to(ROOT)}: original rider/count/order preserved; pistol occupies carbine slots {target_first}..{target_first + pistol_vertices - 1} of {target_first}..{target_last}")
    return (u0, u1, v0, v1)


def open_texture(path: Path) -> Image.Image:
    raw = path.read_bytes()
    if raw[48:52] != b"DDS ":
        raise ValueError(f"Not an M2 texture container: {path}")
    return Image.open(io.BytesIO(raw[48:])).convert("RGBA")


def patched_texture(original: Path, donor: Path, output: Path,
                    box: tuple[int, int, int, int], uv_bounds: tuple[float, float, float, float]):
    image = open_texture(original)
    donor_image = open_texture(donor)
    u0, u1, v0, v1 = uv_bounds
    crop = (
        max(0, math.floor(u0 * 1024)), max(0, math.floor(v0 * 1024)),
        min(1024, math.ceil(u1 * 1024) + 1), min(1024, math.ceil(v1 * 1024) + 1),
    )
    x, y, width, height = box
    if image.getchannel("A").crop((x, y, x + width, y + height)).getbbox() is not None:
        raise ValueError(f"Chosen destination patch is not transparent: {original}")
    image.paste(donor_image.crop(crop).resize((width, height), Image.Resampling.LANCZOS), (x, y))
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    print(f"Built {output.relative_to(ROOT)} from original texture plus pistol-only patch")


donor_mesh = ROOT / "data" / "unit_models" / "_units" / "japan" / "revolver_cavalry_lod0.mesh"
donor_dump = WORK / "pistol_donor" / "revolver_cavalry_lod0.txt"
hassa_box = (300, 4, 152, 72)
general_box = (780, 4, 88, 42)

hassa_uv = transplant(
    ROOT / "data" / "unit_models" / "_Units" / "otto" / "otto_reg_lod0.mesh",
    WORK / "hassa" / "otto_reg_lod0.txt",
    ROOT / "data" / "unit_models" / "_Units" / "otto" / "ott_hassa_suvarisi_lod0.mesh",
    donor_mesh, donor_dump, hassa_box, {},
)
general_uv = transplant(
    ROOT / "data" / "unit_models" / "_Units" / "ott" / "ott_cav_1g_lod0.mesh",
    WORK / "general" / "ott_cav_1g_lod0.txt",
    ROOT / "data" / "unit_models" / "_Units" / "ott" / "ott_general_staff_lod0.mesh",
    donor_mesh, donor_dump, general_box, {20: 22, 21: 23, 22: 24, 23: 25},
)

shared = ROOT / "data" / "unit_models" / "_Units" / "attachments" / "textures"
portugal = ROOT / "data" / "unit_models" / "_Units" / "portugal" / "textures"
japan = ROOT / "data" / "unit_models" / "_units" / "japan" / "attachments"
png = WORK / "pistol_texture_png"
patched_texture(portugal / "port_inf_3.texture", japan / "revolver_cavalry_gear.texture", png / "ott_hassa_pistol_gear.png", hassa_box, hassa_uv)
patched_texture(portugal / "yingguowuqi_n.texture", japan / "revolver_cavalry_gear_norm.texture", png / "ott_hassa_pistol_gear_norm.png", hassa_box, hassa_uv)
patched_texture(shared / "per_rugbxx.texture", japan / "revolver_cavalry_gear.texture", png / "ott_general_pistol_gear.png", general_box, general_uv)
patched_texture(shared / "blank_norm.texture", japan / "revolver_cavalry_gear_norm.texture", png / "ott_general_pistol_gear_norm.png", general_box, general_uv)
