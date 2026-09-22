"""Clone the mixed civilian rider and disable only its Colt weapon group."""
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/unit_models/_Units/usa/usa_cow_1g_lod0.mesh"
TARGET = ROOT / "data/unit_models/_Units/usa/boer_cow_carbine_only_lod0.mesh"

def main() -> None:
    data = bytearray(SOURCE.read_bytes())
    active = b"primaryactive0"
    disabled = b"primarydummy00"
    hits = []
    at = 0
    while True:
        at = data.find(active, at)
        if at < 0:
            break
        name2_at = at + len(active)
        name2_len = struct.unpack_from("<I", data, name2_at)[0]
        name2 = bytes(data[name2_at + 4:name2_at + 4 + name2_len])
        hits.append((at, name2))
        at += len(active)
    if [name for _, name in hits] != [b"winchester_01", b"colt_01"]:
        raise ValueError(f"Unexpected mixed-rider weapon groups: {hits}")
    pistol_at = hits[1][0]
    data[pistol_at:pistol_at + len(active)] = disabled
    if data.count(active) != 1 or data.count(disabled) != 1:
        raise ValueError("Failed to isolate the Winchester group")
    TARGET.write_bytes(data)
    print("Built civilian Boer rider with Winchester active and Colt disabled.")

if __name__ == "__main__":
    main()
