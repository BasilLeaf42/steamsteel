from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EDU = ROOT / "data/tow_steamsteel/export_descr_unit.txt"
CAMPAIGNS = [
    ROOT / "data/world/maps/campaign/camp_steamsteel/descr_strat.txt",
    ROOT / "data/world/maps/campaign/imperial_campaign/descr_strat.txt",
]
REPORT = ROOT / "tools/starting_force_rebalance_20261004.json"


def clean(line):
    return line.split(";", 1)[0].strip()


records = {}
for block in re.split(r"\n(?=type\s+)", EDU.read_text(encoding="utf-8", errors="strict").replace("\r", "")):
    name = re.search(r"^type\s+(.+)$", block, re.M)
    category = re.search(r"^category\s+(\S+)", block, re.M)
    cost = re.search(r"^stat_cost\s+(.+)$", block, re.M)
    attributes = re.search(r"^attributes\s+(.+)$", block, re.M)
    if not name or not category or not cost:
        continue
    fields = [x.strip() for x in cost.group(1).split(",")]
    records[name.group(1).strip()] = {
        "category": category.group(1),
        "upkeep": int(fields[2]),
        "general": bool(attributes and "general_unit" in attributes.group(1).split(", ")),
    }

types = tuple(records)


def resolve(line):
    body = re.sub(r"^\s*unit\s+", "", clean(line)).strip()
    matches = [name for name in types if body == name or body.startswith(name + " ") or body.startswith(name + "\t")]
    return max(matches, key=len) if matches else None


weights = {"village": 1, "town": 2, "large_town": 3, "city": 4, "large_city": 5, "huge_city": 6}


def analyse(text):
    lines = text.splitlines(keepends=True)
    factions = {}
    faction = None
    for index, raw in enumerate(lines):
        line = clean(raw)
        match = re.match(r"^faction\s+([^,\s]+)", line)
        if match:
            faction = match.group(1)
            factions[faction] = {"points": 0, "ports": 0, "armies": []}
            continue
        if not faction:
            continue
        match = re.match(r"^level\s+(\S+)", line)
        if match:
            factions[faction]["points"] += weights.get(match.group(1), 0)
            continue
        if re.match(r"^type\s+port\s+", line):
            factions[faction]["ports"] += 1
            continue
        if line != "army":
            continue
        unit_lines = []
        cursor = index + 1
        while cursor < len(lines) and re.match(r"^\s*unit\s+", clean(lines[cursor])):
            unit = resolve(lines[cursor])
            if not unit:
                raise RuntimeError(f"Unknown starting unit at line {cursor + 1}: {clean(lines[cursor])}")
            unit_lines.append({"index": cursor, "unit": unit})
            cursor += 1
        if not unit_lines:
            continue
        owner_line = ""
        back = index - 1
        while back >= 0:
            prior = clean(lines[back])
            if re.match(r"^(character|admiral)\s+", prior):
                owner_line = prior
                break
            if prior in {"army", "settlement"} or re.match(r"^faction\s+", prior):
                break
            back -= 1
        kind = "ship" if all(records[x["unit"]]["category"] == "ship" for x in unit_lines) else "land"
        factions[faction]["armies"].append({
            "start": index,
            "kind": kind,
            "leader": "leader" in owner_line,
            "units": unit_lines,
        })
    return lines, factions


def select_armies(data, kind, target):
    armies = [a for a in data["armies"] if a["kind"] == kind]
    all_units = [u for army in armies for u in army["units"]]
    if len(all_units) <= target:
        return {u["index"] for u in all_units}

    # Keep every existing formation alive. The first record is normally its
    # general/bodyguard or lead ship and is never removed independently.
    chosen = {army["units"][0]["index"] for army in armies}
    if kind == "land":
        # A four-man command element must not be left as the sole defender of
        # a settlement or field stack when that army originally had troops.
        for army in armies:
            first = army["units"][0]
            if records[first["unit"]]["general"]:
                escort = next((u for u in army["units"][1:] if not records[u["unit"]]["general"]), None)
                if escort:
                    chosen.add(escort["index"])
    target = max(target, len(chosen))

    if kind == "land":
        # Preserve one infantry formation and one siege-capable gun if those
        # roles existed but were not already retained.
        for category in ("infantry", "siege"):
            if any(records[u["unit"]]["category"] == category and u["index"] in chosen for u in all_units):
                continue
            candidate = next((u for u in all_units if records[u["unit"]]["category"] == category), None)
            if candidate:
                chosen.add(candidate["index"])
                target = max(target, len(chosen))

    # Give the faction leader's field army first claim on remaining units,
    # then distribute depth-wise so no one stack consumes the entire budget.
    candidates = []
    for army in armies:
        if army["leader"]:
            candidates.extend(army["units"][1:])
    max_depth = max((len(a["units"]) for a in armies), default=0)
    for depth in range(1, max_depth):
        for army in armies:
            if depth < len(army["units"]):
                candidates.append(army["units"][depth])
    for unit in candidates:
        if len(chosen) >= target:
            break
        chosen.add(unit["index"])
    return chosen


def process(path, apply):
    original = path.read_text(encoding="utf-8", errors="strict")
    newline = "\r\n" if "\r\n" in original else "\n"
    lines, factions = analyse(original)
    keep = set()
    rows = []
    for faction, data in factions.items():
        land = [u for a in data["armies"] if a["kind"] == "land" for u in a["units"]]
        ships = [u for a in data["armies"] if a["kind"] == "ship" for u in a["units"]]
        if faction == "slave":
            land_keep = {u["index"] for u in land}
            ship_keep = {u["index"] for u in ships}
        else:
            # Four-man command elements are characters, not field formations.
            # Preserve them and apply the settlement capacity to the actual
            # combat formations that create the economic burden.
            command_units = sum(records[u["unit"]]["general"] for u in land)
            land_keep = select_armies(data, "land", data["points"] + 1 + command_units)
            ship_keep = select_armies(data, "ship", data["ports"] * 2)
        keep.update(land_keep)
        keep.update(ship_keep)
        before_upkeep = sum(records[u["unit"]]["upkeep"] for u in land + ships)
        after_upkeep = sum(records[u["unit"]]["upkeep"] for u in land + ships if u["index"] in keep)
        rows.append({
            "faction": faction,
            "settlement_points": data["points"],
            "ports": data["ports"],
            "land_before": len(land), "land_after": len(land_keep),
            "ships_before": len(ships), "ships_after": len(ship_keep),
            "upkeep_before": before_upkeep, "upkeep_after": after_upkeep,
        })
    unit_indices = {u["index"] for data in factions.values() for a in data["armies"] for u in a["units"]}
    result = "".join(line for i, line in enumerate(lines) if i not in unit_indices or i in keep)
    if apply:
        path.write_text(result.replace("\n", newline) if newline == "\r\n" and "\r\n" not in result else result,
                        encoding="utf-8", newline="")
    return rows, result


parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
args = parser.parse_args()
reports = []
results = []
for path in CAMPAIGNS:
    rows, result = process(path, args.apply)
    reports.append({"file": str(path.relative_to(ROOT)), "factions": rows})
    results.append(result)
if results[0] != results[1]:
    raise RuntimeError("Campaign mirrors would diverge")
REPORT.write_text(json.dumps(reports, indent=2) + "\n", encoding="utf-8")
print(json.dumps(reports[0]["factions"], indent=2))
