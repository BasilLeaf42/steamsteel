from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EDU = ROOT / "data/tow_steamsteel/export_descr_unit.txt"
MODELDB = ROOT / "data/unit_models/battle_models.modeldb"
REBEL_DB = ROOT / "data/descr_rebel_factions.txt"
CAMPAIGNS = [
    ROOT / "data/world/maps/campaign/camp_steamsteel/descr_strat.txt",
    ROOT / "data/world/maps/campaign/imperial_campaign/descr_strat.txt",
]
OUT = ROOT / "tools/slave_unit_integrity_audit_20260926.json"


def strip_comment(line):
    return line.split(";", 1)[0].strip()


def parse_edu():
    records = {}
    current = None
    for number, raw in enumerate(EDU.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = strip_comment(raw)
        m = re.match(r"^type\s+(.+)$", line, re.I)
        if m:
            current = m.group(1).strip()
            records[current] = {"line": number, "ownership": set(), "models": []}
            continue
        if not current:
            continue
        m = re.match(r"^ownership\s+(.+)$", line, re.I)
        if m:
            records[current]["ownership"] = {x.strip() for x in m.group(1).split(",") if x.strip()}
        m = re.match(r"^(soldier|officer)\s+([^,]+)", line, re.I)
        if m:
            records[current]["models"].append({"role": m.group(1).lower(), "name": m.group(2).strip()})
    return records


def parse_modeldb():
    text = MODELDB.read_text(encoding="utf-8", errors="replace").replace("\r", "")
    heads = []
    for m in re.finditer(r"^(\d+) (\S+)\s*\n\d+ \d+\s*$", text, re.M):
        if int(m.group(1)) == len(m.group(2)):
            heads.append(m)
    entries = {}
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = text[head.start():end]
        entries[head.group(2)] = {
            "line": text.count("\n", 0, head.start()) + 1,
            "block": block,
            "slave_mapping": bool(re.search(r"^5 slave\s*$", block, re.M)),
            "assets": sorted(set(re.findall(r"(?:unit_models|unit_sprites)[/\\][^\r\n]+?\.(?:mesh|texture|spr)", block, re.I))),
        }
    return entries


def resolve_unit(body, types):
    body = re.sub(r"^\s*unit\s+", "", body, flags=re.I).strip()
    candidates = [u for u in types if body == u or body.startswith(u + " ") or body.startswith(u + "\t")]
    return max(candidates, key=len) if candidates else None


edu = parse_edu()
models = parse_modeldb()
models_ci = {name.lower(): value for name, value in models.items()}
types = tuple(edu)

references = {}


def add_reference(unit, source, line):
    references.setdefault(unit, []).append({"source": source, "line": line})


unknown = []
for number, raw in enumerate(REBEL_DB.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
    line = strip_comment(raw)
    if not re.match(r"^unit\s+", line, re.I):
        continue
    unit = resolve_unit(line, types)
    if unit:
        add_reference(unit, str(REBEL_DB.relative_to(ROOT)), number)
    else:
        unknown.append({"source": str(REBEL_DB.relative_to(ROOT)), "line": number, "text": line})

for path in CAMPAIGNS:
    faction = None
    for number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = strip_comment(raw)
        m = re.match(r"^faction\s+([^,\s]+)", line, re.I)
        if m:
            faction = m.group(1)
            continue
        if faction != "slave" or not re.match(r"^unit\s+", line, re.I):
            continue
        unit = resolve_unit(line, types)
        if unit:
            add_reference(unit, str(path.relative_to(ROOT)), number)
        else:
            unknown.append({"source": str(path.relative_to(ROOT)), "line": number, "text": line})

slave_owned = {u for u, r in edu.items() if "slave" in r["ownership"]}
referenced = set(references)
scope = slave_owned | referenced

issues = []
for unit in sorted(scope):
    record = edu[unit]
    if unit in referenced and "slave" not in record["ownership"]:
        issues.append({"kind": "missing_slave_ownership", "unit": unit, "edu_line": record["line"], "references": references[unit]})
    if not record["models"]:
        issues.append({"kind": "no_soldier_or_officer_model", "unit": unit, "edu_line": record["line"]})
    for item in record["models"]:
        entry = models_ci.get(item["name"].lower())
        if not entry:
            issues.append({"kind": "missing_modeldb_entry", "unit": unit, **item, "edu_line": record["line"]})
        elif not entry["slave_mapping"]:
            issues.append({"kind": "missing_slave_model_mapping", "unit": unit, **item, "modeldb_line": entry["line"]})

report = {
    "scope": {
        "edu_slave_owned_units": len(slave_owned),
        "rebel_referenced_defined_units": len(referenced),
        "audited_union": len(scope),
    },
    "unknown_rebel_references": unknown,
    "issues": issues,
}
OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

counts = {}
for issue in issues:
    counts[issue["kind"]] = counts.get(issue["kind"], 0) + 1
print(json.dumps({
    **report["scope"],
    "unknown_rebel_references": len(unknown),
    "issue_counts": counts,
    "report": str(OUT.relative_to(ROOT)),
}, indent=2))
