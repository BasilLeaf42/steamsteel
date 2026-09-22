"""Build a seated Qajar command rider with shamshir as the primary visible weapon."""
from pathlib import Path
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools/mesh_work/qajar_general/audit/qaj_cav_1g.glb"
OUTPUT = ROOT / "tools/mesh_work/qajar_general/qaj_general_staff.glb"


def main():
    data = SOURCE.read_bytes()
    if data[:4] != b"glTF":
        raise RuntimeError("unexpected GLB header")
    json_len, json_type = struct.unpack_from("<II", data, 12)
    if json_type != 0x4E4F534A:
        raise RuntimeError("first GLB chunk is not JSON")
    start, end = 20, 20 + json_len
    doc = json.loads(data[start:end].decode("utf-8"))
    pistol = "primaryactive0__sm_01"
    sword = "secondaryactive0__p_sabre"
    for collection in (doc.get("meshes", []), doc.get("nodes", [])):
        names = [item.get("name") for item in collection]
        if names.count(pistol) != 1 or names.count(sword) != 1:
            raise RuntimeError("verified Qajar pistol/sabre groups were not found exactly once")
        for item in collection:
            if item.get("name") == pistol:
                item["name"] = "secondaryactive0__sm_01"
            elif item.get("name") == sword:
                item["name"] = "primaryactive0__p_sabre"
    encoded = json.dumps(doc, separators=(",", ":")).encode("utf-8")
    encoded += b" " * ((4 - len(encoded) % 4) % 4)
    remainder = data[end:]
    total = 12 + 8 + len(encoded) + len(remainder)
    rebuilt = b"glTF" + struct.pack("<II", 2, total)
    rebuilt += struct.pack("<II", len(encoded), 0x4E4F534A) + encoded + remainder
    OUTPUT.write_bytes(rebuilt)
    print("Prepared Qajar command rider GLB with shamshir/pistol visibility slots exchanged.")


if __name__ == "__main__":
    main()
