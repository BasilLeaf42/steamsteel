"""Turn the genuine Siam bodyguard rider into a dedicated sword-only light cavalry mesh."""
from pathlib import Path
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools/mesh_work/siam_sword_cav/siam_sword_cav_source.glb"
OUTPUT = ROOT / "tools/mesh_work/siam_sword_cav/siam_sword_cav.glb"


def main():
    data = SOURCE.read_bytes()
    if data[:4] != b"glTF":
        raise RuntimeError("unexpected GLB header")
    json_len, json_type = struct.unpack_from("<II", data, 12)
    if json_type != 0x4E4F534A:
        raise RuntimeError("first GLB chunk is not JSON")
    start, end = 20, 20 + json_len
    doc = json.loads(data[start:end].decode("utf-8"))
    for collection_name in ("meshes", "nodes"):
        collection = doc.get(collection_name, [])
        pistols = [x for x in collection if x.get("name", "").startswith("primaryactive0")]
        swords = [x for x in collection if x.get("name", "").startswith("secondaryactive0")]
        if len(pistols) != 1 or len(swords) != 1:
            raise RuntimeError(f"{collection_name}: expected one pistol and one sword group")
        pistols[0]["name"] = "inactive0" + pistols[0]["name"][len("primaryactive0"):]
        swords[0]["name"] = "primaryactive0" + swords[0]["name"][len("secondaryactive0"):]
    encoded = json.dumps(doc, separators=(",", ":")).encode("utf-8")
    encoded += b" " * ((4 - len(encoded) % 4) % 4)
    remainder = data[end:]
    total = 12 + 8 + len(encoded) + len(remainder)
    rebuilt = b"glTF" + struct.pack("<II", 2, total)
    rebuilt += struct.pack("<II", len(encoded), 0x4E4F534A) + encoded + remainder
    OUTPUT.write_bytes(rebuilt)
    print("Prepared genuine Siam rider: sabre primary, pistol inactive.")


if __name__ == "__main__":
    main()
