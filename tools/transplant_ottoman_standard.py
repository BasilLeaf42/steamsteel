"""Put a verified flag and pole onto the Ottoman Nizamiye infantry mesh."""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass
from pathlib import Path


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
    name2_line, count_line = primary_line + 1, primary_line + 2
    end_line = next(i for i in range(count_line + 1, len(lines)) if "end   triangle group" in lines[i])
    count = int(re.match(r"\s*(\d+)\s+# number of triangles", lines[count_line]).group(1))
    return Dump(counts[0][0], counts[1:], Group(
        position(lines[start_line]), position(lines[primary_line]), position(lines[name2_line]),
        position(lines[count_line]), count, position(lines[end_line])
    ))


def main() -> None:
    source_path = ROOT / "data" / "unit_models" / "_Units" / "ott" / "ott_inf_1g_lod0.mesh"
    donor_path = ROOT / "data" / "unit_models" / "_Units" / "bnw" / "fra_qishou_lod0.mesh"
    output_path = ROOT / "data" / "unit_models" / "_Units" / "off" / "ott_standard_bearer_lod0.mesh"
    source_dump = WORK / "ottoman_bearer" / "nizamiye" / "ott_inf_1g_lod0.txt"
    donor_dump = Path(r"C:\Users\kwoks\.codex\visualizations\2026\09\12\01a09417-2b02-79c1-ac26-19f8f616b95f\bearer_check\fra_qishou\fra_qishou_lod0.txt")
    target, donor = bytearray(source_path.read_bytes()), donor_path.read_bytes()
    td, dd = read_dump(source_dump), read_dump(donor_dump)

    donor_at = dd.primary.count_end
    donor_indices = list(struct.unpack_from(f"<{dd.primary.count * 3}H", donor, donor_at))
    donor_first, donor_last = min(donor_indices), max(donor_indices)
    donor_vertices = donor_last - donor_first + 1
    target_at = td.primary.count_end
    target_indices = list(struct.unpack_from(f"<{td.primary.count * 3}H", target, target_at))
    target_first, target_last = min(target_indices), max(target_indices)
    if donor_vertices != 221 or target_last - target_first + 1 < donor_vertices:
        raise ValueError("Unexpected verified flag or Ottoman sabre vertex span")

    adjusted = [target_first + index - donor_first for index in donor_indices]
    strides = [8, 8, 12, 4, 4, 4, 4]
    joint_map = {20: 22, 21: 23, 22: 24}
    donor_uvs = [struct.unpack_from("<ff", donor, dd.arrays[0][1] + i * 8)
                 for i in range(donor_first, donor_last + 1)]
    u_min, u_max = min(u for u, _ in donor_uvs), max(u for u, _ in donor_uvs)
    v_min, v_max = min(v for _, v in donor_uvs), max(v for _, v in donor_uvs)
    for array_index, stride in enumerate(strides):
        target_count, target_start = td.arrays[array_index]
        donor_count, donor_start = dd.arrays[array_index]
        if target_count != td.vertex_count or donor_count != dd.vertex_count:
            raise ValueError("Inconsistent mesh vertex array count")
        chunk = bytearray(donor[donor_start + donor_first * stride:donor_start + (donor_last + 1) * stride])
        if array_index == 0:
            # Head geometry occupies the right half of the attachment atlas.
            # Preserve the donor flag's renderer-space aspect ratio in the
            # lower-left region. Raw U is doubled by the mesh format.
            for i, (u, v) in enumerate(donor_uvs):
                # Raw U is doubled by the mesh format. Keep the result above
                # 1.0 so IWTE/the game retains the attachment material, while
                # its wrapped local coordinate occupies 0.02..0.49. The
                # 0.47:0.59 renderer-space ratio matches the donor's 0.77
                # ratio after accounting for double-atlas U coordinates.
                new_u = 0.51 + ((u - u_min) / (u_max - u_min)) * 0.235
                new_v = 0.40 + ((v - v_min) / (v_max - v_min)) * 0.59
                struct.pack_into("<ff", chunk, i * stride, new_u, new_v)
        if array_index == 3:
            for i in range(donor_vertices):
                at = i * stride
                chunk[at] = joint_map.get(chunk[at], chunk[at])
                chunk[at + 2] = joint_map.get(chunk[at + 2], chunk[at + 2])
        write_at = target_start + target_first * stride
        target[write_at:write_at + len(chunk)] = chunk

    group = td.primary
    old_triangle_end = group.count_end + group.count * 6
    replacement = bytearray(target[group.start:group.name1_end])
    name = b"big_flag"
    replacement += struct.pack("<I", len(name)) + name
    replacement += struct.pack("<I", dd.primary.count)
    replacement += struct.pack(f"<{len(adjusted)}H", *adjusted)
    replacement += target[old_triangle_end:group.end]
    target[group.start:group.end] = replacement

    # The first integer is the archive-name length and must remain 22.
    if struct.unpack_from("<I", target, 0)[0] != 22:
        raise ValueError("Corrupt source serialization header")
    output_path.write_bytes(target)
    print(f"Built {output_path.relative_to(ROOT)} from the Nizamiye body and face set with verified flag geometry")


if __name__ == "__main__":
    main()
