from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EDU = ROOT / "data/tow_steamsteel/export_descr_unit.txt"
EDB = ROOT / "data/tow_steamsteel/export_descr_buildings.txt"
CAMPAIGNS = [
    ROOT / "data/world/maps/campaign/camp_steamsteel/descr_strat.txt",
    ROOT / "data/world/maps/campaign/imperial_campaign/descr_strat.txt",
]
MERC_FILES = [
    ROOT / "data/world/maps/campaign/camp_steamsteel/descr_mercenaries.txt",
    ROOT / "data/world/maps/campaign/imperial_campaign/descr_mercenaries.txt",
]
OUT = ROOT / "tools/starting_campaign_unit_audit_20260926.json"


def uncomment(line: str) -> str:
    return line.split(";", 1)[0].strip()


def parse_edu(path: Path):
    records = {}
    current = None
    for number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = uncomment(raw)
        match = re.match(r"^type\s+(.+?)\s*$", line, re.I)
        if match:
            current = match.group(1).strip()
            records[current] = {"ownership": set(), "eras": set(), "line": number}
            continue
        match = re.match(r"^ownership\s+(.+?)\s*$", line, re.I)
        if match and current:
            records[current]["ownership"] = {item.strip() for item in match.group(1).split(",") if item.strip()}
            continue
        match = re.match(r"^era\s+[012]\s+(.+?)\s*$", line, re.I)
        if match and current:
            records[current]["eras"].update(item.strip() for item in match.group(1).split(",") if item.strip())
    return records


def resolve_unit(text: str, types):
    body = re.sub(r"^\s*unit\s+", "", text, flags=re.I).strip()
    candidates = [name for name in types if body == name or body.startswith(name + " ") or body.startswith(name + "\t")]
    return max(candidates, key=len) if candidates else None


edu = parse_edu(EDU)
types = tuple(edu)
edb_factions = {unit: set() for unit in types}
edb_global = set()
for raw in EDB.read_text(encoding="utf-8", errors="replace").splitlines():
    line = uncomment(raw)
    match = re.search(r'recruit_pool\s+"([^"]+)"', line, re.I)
    if not match:
        continue
    unit = match.group(1).strip()
    if unit not in edu:
        continue
    faction_match = re.search(r"requires\s+factions\s*\{([^}]*)\}", line, re.I)
    if faction_match:
        edb_factions[unit].update(item.strip() for item in faction_match.group(1).split(",") if item.strip())
    else:
        edb_global.add(unit)
mercenary_types = set()
merc_unknown = []
for path in MERC_FILES:
    if not path.exists():
        continue
    for number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if re.match(r"^\s*unit\s+", uncomment(raw), re.I):
            unit = resolve_unit(uncomment(raw), types)
            if unit:
                mercenary_types.add(unit)
            else:
                merc_unknown.append({"file": str(path.relative_to(ROOT)), "line": number, "text": raw.strip()})

report = {"edu_records": len(edu), "mercenary_types": len(mercenary_types), "campaigns": [], "merc_unknown": merc_unknown}
for path in CAMPAIGNS:
    faction = None
    units = []
    unknown = []
    mismatches = []
    counts = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = uncomment(raw)
        faction_match = re.match(r"^faction\s+([^,\s]+)", line, re.I)
        if faction_match:
            faction = faction_match.group(1)
            continue
        if not re.match(r"^unit\s+", line, re.I):
            continue
        unit = resolve_unit(line, types)
        if not unit:
            unknown.append({"line": number, "faction": faction, "text": raw.strip()})
            continue
        ownership = sorted(edu[unit]["ownership"])
        era_factions = sorted(edu[unit]["eras"])
        recruitment_factions = sorted(edb_factions[unit])
        is_mercenary = unit in mercenary_types
        valid = (
            faction in edu[unit]["ownership"]
            or "all" in edu[unit]["ownership"]
            or faction in edu[unit]["eras"]
            or faction in edb_factions[unit]
            or unit in edb_global
            or is_mercenary
            or (faction == "slave" and "slave" in edu[unit]["ownership"])
        )
        row = {"line": number, "faction": faction, "unit": unit, "ownership": ownership, "era_factions": era_factions, "recruitment_factions": recruitment_factions, "edb_global": unit in edb_global, "mercenary": is_mercenary, "valid": valid}
        units.append(row)
        counts[faction] = counts.get(faction, 0) + 1
        if not valid:
            mismatches.append(row)
    report["campaigns"].append({
        "file": str(path.relative_to(ROOT)),
        "unit_instances": len(units),
        "distinct_units": len({row["unit"] for row in units}),
        "faction_counts": counts,
        "unknown": unknown,
        "mismatches": mismatches,
    })

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({
    "edu_records": report["edu_records"],
    "mercenary_types": report["mercenary_types"],
    "merc_unknown": len(merc_unknown),
    "campaigns": [
        {"file": item["file"], "units": item["unit_instances"], "distinct": item["distinct_units"], "unknown": len(item["unknown"]), "mismatches": len(item["mismatches"])}
        for item in report["campaigns"]
    ],
}, indent=2))
