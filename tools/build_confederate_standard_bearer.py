"""Build a native Confederate standard bearer and its two-sided battle-flag atlas."""

from __future__ import annotations

import io
import math
import re
import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tools" / "mesh_work" / "confederate_bearer"


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
    arrays: list[tuple[int, int]]
    primary: Group


POSITION = re.compile(r"at position =\s*(\d+)")


def position(line: str) -> int:
    match = POSITION.search(line)
    if not match:
        raise ValueError(f"Missing byte position: {line}")
    return int(match.group(1))


def read_dump(path: Path) -> Dump:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    counts = []
    for line in lines:
        match = re.match(r"\s*(\d+)\s+# number of vertices", line)
        if match:
            counts.append((int(match.group(1)), position(line)))
    if len(counts) != 8:
        raise ValueError(f"{path}: expected top count plus seven vertex arrays")
    primary_line = next(i for i, line in enumerate(lines) if re.match(r"\s*14\s+primaryactive0\s+#", line))
    start_line = next(i for i in range(primary_line - 1, -1, -1) if "start triangle group" in lines[i])
    name2_line = primary_line + 1
    count_line = next(i for i in range(name2_line + 1, len(lines)) if "# number of triangles" in lines[i])
    end_line = next(i for i in range(count_line + 1, len(lines)) if "end   triangle group" in lines[i])
    count = int(re.match(r"\s*(\d+)\s+# number of triangles", lines[count_line]).group(1))
    return Dump(counts[0][0], counts[1:], Group(
        position(lines[start_line]), position(lines[primary_line]), position(lines[name2_line]),
        position(lines[count_line]), count, position(lines[end_line])
    ))


def build_mesh() -> None:
    source_path = ROOT / "data/unit_models/_Units/bnw/csa_officer_lod0.mesh"
    donor_path = ROOT / "data/unit_models/_Units/bnw/fra_qishou_lod0.mesh"
    output_path = ROOT / "data/unit_models/_Units/off/csa_standard_bearer_lod0.mesh"
    source_dump = WORK / "officer/csa_officer_lod0.txt"
    donor_dump = Path(r"C:\Users\kwoks\.codex\visualizations\2026\09\12\01a09417-2b02-79c1-ac26-19f8f616b95f\bearer_check\fra_qishou\fra_qishou_lod0.txt")
    target, donor = bytearray(source_path.read_bytes()), donor_path.read_bytes()
    td, dd = read_dump(source_dump), read_dump(donor_dump)

    donor_indices = list(struct.unpack_from(f"<{dd.primary.count * 3}H", donor, dd.primary.count_end))
    donor_first, donor_last = min(donor_indices), max(donor_indices)
    donor_vertices = donor_last - donor_first + 1
    target_indices = list(struct.unpack_from(f"<{td.primary.count * 3}H", target, td.primary.count_end))
    target_first, target_last = min(target_indices), max(target_indices)
    if donor_vertices != 221 or target_last - target_first + 1 < donor_vertices:
        raise ValueError("Unexpected flag or Confederate officer-prop vertex span")

    adjusted = [target_first + index - donor_first for index in donor_indices]
    strides = [8, 8, 12, 4, 4, 4, 4]
    # Preserve the verified donor UVs.  Its cloth occupies the lower-left
    # flag rectangle used by build_texture; redirecting the group elsewhere
    # made the pole/cloth sample unrelated attachment pixels.
    for array_index, stride in enumerate(strides):
        target_count, target_start = td.arrays[array_index]
        donor_count, donor_start = dd.arrays[array_index]
        if target_count != td.vertex_count or donor_count != dd.vertex_count:
            raise ValueError("Inconsistent mesh vertex array count")
        chunk = bytearray(donor[donor_start + donor_first * stride:donor_start + (donor_last + 1) * stride])
        # Both meshes use the same Western skeleton and identical hand-chain indices.
        write_at = target_start + target_first * stride
        target[write_at:write_at + len(chunk)] = chunk

    group = td.primary
    old_triangle_end = group.count_end + group.count * 6
    replacement = bytearray(target[group.start:group.name1_end])
    name = b"big_flag"
    replacement += struct.pack("<I", len(name)) + name
    replacement += target[group.name2_end:group.count_end - 4]
    replacement += struct.pack("<I", dd.primary.count)
    replacement += struct.pack(f"<{len(adjusted)}H", *adjusted)
    replacement += target[old_triangle_end:group.end]
    target[group.start:group.end] = replacement
    if struct.unpack_from("<I", target, 0)[0] != 22:
        raise ValueError("Corrupt source serialization header")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(target)


def open_texture(path: Path) -> Image.Image:
    raw = path.read_bytes()
    if raw[48:52] != b"DDS ":
        raise ValueError(f"Not a Medieval II texture container: {path}")
    return Image.open(io.BytesIO(raw[48:])).convert("RGBA")


def build_texture() -> None:
    attachments = ROOT / "data/unit_models/_Units/attachments/textures"
    image = open_texture(attachments / "whi_spusxx.texture")
    pixels = np.asarray(image).copy()
    pixels[:, 8:504] = (132, 8, 12, 255)
    image = Image.fromarray(pixels, "RGBA")
    draw = ImageDraw.Draw(image)
    # Cloth footprint established from the verified French pole-and-flag donor.
    box = (193, 711, 502, 1013)
    red, white, blue = (132, 8, 12, 255), (235, 233, 218, 255), (20, 31, 65, 255)
    draw.rectangle(box, fill=red)
    draw.line((198, 716, 497, 1008), fill=white, width=43)
    draw.line((497, 716, 198, 1008), fill=white, width=43)
    draw.line((198, 716, 497, 1008), fill=blue, width=28)
    draw.line((497, 716, 198, 1008), fill=blue, width=28)
    stars = [(220,738),(266,783),(312,828),(358,873),(404,918),(450,963),
             (475,738),(429,783),(383,828),(337,873),(291,918),(245,963),(347,862)]
    for cx, cy in stars:
        points = []
        for i in range(10):
            radius = 9 if i % 2 == 0 else 4
            angle = -math.pi / 2 + i * math.pi / 5
            points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
        draw.polygon(points, fill=white)
    out = WORK / "tga"
    out.mkdir(parents=True, exist_ok=True)
    image.save(out / "csa_standard_flag.tga")
    open_texture(attachments / "blank_norm.texture").save(out / "csa_standard_flag_n.tga")


def main() -> None:
    build_mesh()
    build_texture()
    print("Built Confederate officer-based bearer mesh and battle-flag atlas while preserving the original CSA face material.")


if __name__ == "__main__":
    main()

