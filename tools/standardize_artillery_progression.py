from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EDU_FILES = [ROOT / "data/tow_steamsteel/export_descr_unit.txt", ROOT / "data/export_descr_unit.txt"]
EDB_FILES = [ROOT / "data/tow_steamsteel/export_descr_buildings.txt", ROOT / "data/export_descr_buildings.txt"]

D = {"moors", "golden", "egypt", "timurids", "cuman", "bulga", "cru", "byzantium", "papal_states", "lith"}
MORTAR_ALLOWED = {
    "england", "france", "hre", "normans", "portugala", "milan", "spain",
    "scotland", "denmark", "poland", "aztecs", "russia", "mongols", "turks",
    "portugal", "sicily", "venice", "hungary", "teu", "saxons",
}

# Exact custom-battle eras. Automatic weapons are deliberately absent: their
# already-established historical dates are outside this conventional-gun pass.
ERA_MAP = {
    "fra_12lb": {0: ["france", "spain", "sicily", "poland", "scotland", "aztecs"], 1: ["france", "spain", "sicily", "poland", "scotland", "aztecs"]},
    "fra_armstrong": {1: ["france", "spain", "sicily", "poland", "scotland", "aztecs"], 2: ["france", "spain", "sicily", "poland", "scotland", "aztecs"]},
    "fra_150mm": {2: ["france", "spain", "sicily", "poland", "scotland", "aztecs"]},
    "fra_5lb": {2: ["france", "spain", "sicily", "poland", "scotland", "aztecs"]},
    "rus_12lb": {0: ["russia", "mongols", "normans", "hungary", "hre"], 1: ["russia", "mongols", "normans", "hungary"]},
    "rus_armstrong": {0: ["hre"], 1: ["russia", "mongols", "normans", "hungary", "hre"], 2: ["russia", "mongols", "normans", "hungary", "hre"]},
    "rus_150mm": {1: ["hre"], 2: ["russia", "mongols", "normans", "hungary", "hre"]},
    "rus_5lb": {2: ["russia", "mongols", "normans", "hungary", "hre"]},
    "eng_12lb": {0: ["england", "venice", "portugal"], 1: ["venice", "portugal"]},
    "eng_armstrong": {0: ["england"], 1: ["england", "venice", "portugal"], 2: ["england", "venice", "portugal"]},
    "eng_150mm": {1: ["england"], 2: ["england", "venice", "portugal"]},
    "eng_5lb": {2: ["england", "venice", "portugal"]},
    "usa_12lb": {0: ["portugala", "denmark"], 1: ["portugala", "denmark"]},
    "usa_armstrong": {1: ["portugala", "denmark"], 2: ["portugala", "denmark"]},
    "usa_150mm": {2: ["portugala", "denmark"]},
    "usa_5lb": {2: ["portugala", "denmark"]},
    "csa_12lb": {0: ["milan", "teu"], 1: ["milan", "teu"]},
    "csa_armstrong": {1: ["milan", "teu"], 2: ["milan", "teu"]},
    "csa_150mm": {2: ["milan", "teu"]},
    "csa_5lb": {2: ["milan", "teu"]},
    # The colonial piece remains the safe generic gun for unsupported rosters.
    # Western owners use it as the early muzzle-loader; D-tier owners retain it
    # because no compatible traditional crew/engine clone exists for all three.
    "col_12lb": {0: ["england", "france", "portugal", "egypt", "timurids", "lith"], 1: ["england", "france", "portugal", "egypt", "timurids", "lith"], 2: ["egypt", "timurids", "lith"]},
    "ind_armstrong": {0: ["bulga"], 1: ["bulga"]},
    "ind_12lb": {1: ["bulga"], 2: ["bulga"]},
    "ind_5lb": {},
    "ind_150mm": {},
    "kok_armstrong": {0: ["cuman"], 1: ["cuman"]},
    "kok_12lb": {1: ["cuman"], 2: ["cuman"]},
    "kok_5lb": {},
    "kok_150mm": {},
    "siam_armstrong": {0: ["cru"], 1: ["cru"]},
    "siam_12lb": {1: ["cru"], 2: ["cru"]},
    "siam_5lb": {},
    "byz_armstrong": {0: ["byzantium"], 1: ["byzantium"]},
    "byz_12lb": {1: ["byzantium"], 2: ["byzantium"]},
    "byz_150mm": {2: ["byzantium"]},
    "byz_5lb": {},
    "mus_armstrong": {0: ["moors", "golden"], 1: ["moors", "golden"]},
    "mus_12lb": {0: ["turks"], 1: ["moors", "turks", "golden"], 2: ["moors", "turks", "golden"]},
    "mus_150mm": {2: ["turks"]},
    "mus_5lb": {2: ["turks"]},
    "eth_field_gun": {0: ["papal_states"], 1: ["papal_states"]},
    "eth_rifled_gun": {1: ["papal_states"], 2: ["papal_states"]},
    "jap_armstrong": {0: ["saxons"]},
    "sho_armstrong": {0: ["saxons"]},
    "jap_12lb": {0: ["saxons"], 1: ["saxons"]},
    "sho_12lb": {0: ["saxons"], 1: ["saxons"]},
    "Japan Armstrong": {1: ["saxons"], 2: ["saxons"]},
    "Japan Armstrong Han": {1: ["saxons"], 2: ["saxons"]},
    "jap_150mm": {2: ["saxons"]},
    "sho_150mm": {2: ["saxons"]},
    "jap_5lb": {2: ["saxons"]},
    "sho_5lb": {2: ["saxons"]},
}


def replace_edu_eras(text: str) -> str:
    blocks = re.split(r"(?m)(?=^type\s+)", text)
    out = []
    for block in blocks:
        match = re.match(r"type\s+(.+)$", block, re.M)
        if not match or match.group(1).strip() not in ERA_MAP:
            out.append(block)
            continue
        unit = match.group(1).strip()
        block = re.sub(r"(?m)^era\s+[012]\s+.*(?:\r?\n|$)", "", block)
        ownership = re.search(r"(?m)^ownership\s+.*$", block)
        if not ownership:
            raise RuntimeError(f"No ownership row for {unit}")
        rows = "".join(f"era {era}            {', '.join(factions)}\n" for era, factions in sorted(ERA_MAP[unit].items()) if factions)
        insert = ownership.end()
        block = block[:insert] + "\n" + rows.rstrip("\n") + block[insert:]
        out.append(block)
    return "".join(out)


def unit_family(unit: str) -> str | None:
    if unit in {"eth_field_gun"}: return "traditional"
    if unit in {"eth_rifled_gun"}: return "breech"
    if unit.endswith("_12lb"): return "muzzle"
    if unit.endswith("_armstrong") or unit in {"Japan Armstrong", "Japan Armstrong Han"}:
        return "traditional" if unit.startswith(("mus_", "ind_", "kok_", "siam_", "byz_", "jap_", "sho_")) else "breech"
    if unit.endswith("_150mm"): return "howitzer"
    if unit.endswith("_5lb"): return "mortar"
    return None


def gate_for(unit: str, faction: str) -> str | None:
    family = unit_family(unit)
    if not family: return None
    if family == "mortar":
        return "event_counter military_reforms_1890 1" if faction in MORTAR_ALLOWED else "REMOVE"
    if (unit, faction) == ("mus_armstrong", "turks"):
        return "REMOVE"
    if (unit, faction) == ("mus_12lb", "turks"):
        return "ALWAYS"
    if (unit, faction) in {("eng_12lb", "england"), ("rus_12lb", "hre")}:
        return "not event_counter military_reforms_1870 1"
    if (unit, faction) in {("eng_armstrong", "england"), ("rus_armstrong", "hre")}:
        return "ALWAYS"
    if (unit, faction) in {("eng_150mm", "england"), ("rus_150mm", "hre")}:
        return "event_counter military_reforms_1870 1"
    if unit == "eth_field_gun": return "not event_counter military_reforms_1890 1"
    if unit == "eth_rifled_gun": return "event_counter military_reforms_1870 1"
    if family == "traditional": return "not event_counter military_reforms_1890 1"
    if family == "muzzle":
        return "event_counter military_reforms_1870 1" if faction in D and unit != "col_12lb" else "not event_counter military_reforms_1890 1"
    if family == "breech": return "event_counter military_reforms_1870 1"
    if family == "howitzer":
        return "event_counter military_reforms_1890 1" if faction not in D or faction == "byzantium" else "REMOVE"
    return None


def rewrite_edb(text: str) -> str:
    output = []
    for line in text.splitlines(keepends=True):
        m = re.search(r'recruit_pool "([^"]+)".*?requires factions \{\s*([^,}\s]+)', line)
        if not m:
            output.append(line)
            continue
        unit, faction = m.group(1), m.group(2)
        gate = gate_for(unit, faction)
        if gate is None:
            output.append(line)
            continue
        if gate == "REMOVE":
            continue
        newline = "\r\n" if line.endswith("\r\n") else "\n"
        body = line.rstrip("\r\n")
        body = re.sub(r"\s+and\s+(?:not\s+)?event_counter\s+military_reforms_(?:1865|1870|1890)\s+1", "", body)
        if gate != "ALWAYS":
            body += " and " + gate
        output.append(body + newline)
    return "".join(output)


def periods_from_edb_line(line: str) -> set[int]:
    if "military_reforms_1890 1" in line:
        return {0, 1} if "not event_counter military_reforms_1890 1" in line else {2}
    if "military_reforms_1870 1" in line:
        return {0} if "not event_counter military_reforms_1870 1" in line else {1, 2}
    return {0, 1, 2}


def validate() -> None:
    if EDU_FILES[0].read_bytes() != EDU_FILES[1].read_bytes():
        raise RuntimeError("EDU mirrors differ after artillery progression update")
    if EDB_FILES[0].read_bytes() != EDB_FILES[1].read_bytes():
        raise RuntimeError("EDB mirrors differ after artillery progression update")
    edb = EDB_FILES[0].read_text(encoding="utf-8-sig")
    errors = []
    for line in edb.splitlines():
        m = re.search(r'recruit_pool "([^"]+)".*?requires factions \{\s*([^,}\s]+)', line)
        if not m or m.group(1) not in ERA_MAP:
            continue
        unit, faction = m.group(1), m.group(2)
        expected = {era for era, owners in ERA_MAP[unit].items() if faction in owners}
        actual = periods_from_edb_line(line)
        if expected and actual != expected:
            errors.append(f"{unit}/{faction}: campaign {sorted(actual)} != custom {sorted(expected)}")
        if not expected:
            errors.append(f"{unit}/{faction}: campaign row exists but custom availability is empty")
    if errors:
        raise RuntimeError("Artillery progression mismatch:\n" + "\n".join(sorted(set(errors))[:40]))


def main() -> None:
    for path in EDU_FILES:
        path.write_text(replace_edu_eras(path.read_text(encoding="utf-8-sig")), encoding="utf-8")
    for path in EDB_FILES:
        path.write_text(rewrite_edb(path.read_text(encoding="utf-8-sig")), encoding="utf-8")
    validate()


if __name__ == "__main__":
    main()
