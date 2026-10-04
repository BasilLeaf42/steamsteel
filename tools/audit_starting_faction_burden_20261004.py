from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EDU = ROOT / "data/tow_steamsteel/export_descr_unit.txt"
CAMPAIGN = ROOT / "data/world/maps/campaign/camp_steamsteel/descr_strat.txt"
OUT = ROOT / "tools/starting_faction_burden_20261004.json"


def clean(line):
    return line.split(";", 1)[0].strip()


records = {}
for block in re.split(r"\n(?=type\s+)", EDU.read_text(encoding="utf-8", errors="replace").replace("\r", "")):
    unit = re.search(r"^type\s+(.+)$", block, re.M)
    cost = re.search(r"^stat_cost\s+(.+)$", block, re.M)
    category = re.search(r"^category\s+(\S+)", block, re.M)
    if not unit or not cost:
        continue
    fields = [x.strip() for x in cost.group(1).split(",")]
    records[unit.group(1).strip()] = {
        "upkeep": int(fields[2]),
        "category": category.group(1) if category else "unknown",
        "militia": bool(re.search(r"^attributes\s+.*\bfree_upkeep_unit\b", block, re.M)),
    }

types = tuple(records)


def resolve(body):
    body = re.sub(r"^unit\s+", "", body).strip()
    candidates = [u for u in types if body == u or body.startswith(u + " ") or body.startswith(u + "\t")]
    return max(candidates, key=len) if candidates else None


level_weight = {
    "village": 1,
    "town": 2,
    "large_town": 3,
    "city": 4,
    "large_city": 5,
    "huge_city": 6,
}
factions = {}
current = None
for number, raw in enumerate(CAMPAIGN.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
    line = clean(raw)
    m = re.match(r"^faction\s+([^,\s]+)", line)
    if m:
        current = m.group(1)
        factions[current] = {"denari": 0, "settlements": [], "units": [], "unknown": []}
        continue
    if not current:
        continue
    m = re.match(r"^denari\s+(\d+)", line)
    if m:
        factions[current]["denari"] = int(m.group(1))
        continue
    m = re.match(r"^level\s+(\S+)", line)
    if m:
        factions[current]["settlements"].append(m.group(1))
        continue
    if re.match(r"^unit\s+", line):
        unit = resolve(line)
        if unit:
            factions[current]["units"].append(unit)
        else:
            factions[current]["unknown"].append({"line": number, "text": line})

report = []
for faction, data in factions.items():
    units = data["units"]
    land = [u for u in units if records[u]["category"] != "ship"]
    ships = [u for u in units if records[u]["category"] == "ship"]
    capacity = sum(level_weight.get(level, 0) for level in data["settlements"])
    report.append({
        "faction": faction,
        "denari": data["denari"],
        "settlement_count": len(data["settlements"]),
        "settlement_size_points": capacity,
        "land_units": len(land),
        "ships": len(ships),
        "land_upkeep": sum(records[u]["upkeep"] for u in land),
        "ship_upkeep": sum(records[u]["upkeep"] for u in ships),
        "militia_land_units": sum(records[u]["militia"] for u in land),
        "unknown": data["unknown"],
    })

OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
