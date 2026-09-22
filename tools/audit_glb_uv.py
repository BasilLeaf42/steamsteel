"""Report renderer-ready GLB UV bounds and material assignments."""

from __future__ import annotations

import json
import struct
import sys
from pathlib import Path


def main() -> None:
    data = Path(sys.argv[1]).read_bytes()
    json_length, json_type = struct.unpack_from("<II", data, 12)
    if json_type != 0x4E4F534A:
        raise ValueError("Missing GLB JSON chunk")
    document = json.loads(data[20:20 + json_length].decode("utf-8").rstrip(" \0"))
    binary_at = 20 + json_length
    binary_length, binary_type = struct.unpack_from("<II", data, binary_at)
    if binary_type != 0x004E4942:
        raise ValueError("Missing GLB binary chunk")
    binary = data[binary_at + 8:binary_at + 8 + binary_length]
    materials = document.get("materials", [])

    for mesh in document.get("meshes", []):
        name = mesh.get("name", "")
        if len(sys.argv) > 2 and sys.argv[2].lower() not in name.lower():
            continue
        for primitive in mesh.get("primitives", []):
            accessor = document["accessors"][primitive["attributes"]["TEXCOORD_0"]]
            if accessor["componentType"] != 5126 or accessor["type"] != "VEC2":
                raise ValueError(f"Unsupported UV accessor in {name}")
            view = document["bufferViews"][accessor["bufferView"]]
            start = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
            stride = view.get("byteStride", 8)
            values = [struct.unpack_from("<ff", binary, start + i * stride)
                      for i in range(accessor["count"])]
            us, vs = zip(*values)
            material_index = primitive.get("material")
            material = materials[material_index].get("name") if material_index is not None else None
            print(name, material, accessor["count"],
                  f"{min(us):.6f}", f"{min(vs):.6f}", f"{max(us):.6f}", f"{max(vs):.6f}")


if __name__ == "__main__":
    main()
