from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
AUTHORITATIVE = ROOT / "data/tow_steamsteel/export_descr_unit.txt"
MIRROR = ROOT / "data/export_descr_unit.txt"

text = AUTHORITATIVE.read_text(encoding="utf-8", errors="strict")
newline = "\r\n" if "\r\n" in text else "\n"
normalized = text.replace("\r\n", "\n")
changed = []


def update(block):
    if not re.search(r"^attributes\s+.*\bfree_upkeep_unit\b", block, re.M):
        return block
    unit = re.search(r"^type\s+(.+)$", block, re.M).group(1).strip()
    match = re.search(r"^(stat_cost\s+)(.+)$", block, re.M)
    if not match:
        raise RuntimeError(f"Militia record lacks stat_cost: {unit}")
    fields = [x.strip() for x in match.group(2).split(",")]
    if len(fields) != 8:
        raise RuntimeError(f"Unexpected stat_cost field count for {unit}: {len(fields)}")
    purchase = int(fields[1])
    quarter = int(purchase / 4 + 0.5)
    before = (int(fields[2]), int(fields[7]))
    fields[2] = str(quarter)
    fields[7] = str(quarter)
    after = (quarter, quarter)
    if before != after:
        changed.append({"unit": unit, "before": before, "after": after})
    replacement = match.group(1) + ", ".join(fields)
    return block[:match.start()] + replacement + block[match.end():]


parts = re.split(r"(\n(?=type\s+))", normalized)
for index in range(0, len(parts), 2):
    if re.search(r"^type\s+", parts[index], re.M):
        parts[index] = update(parts[index])
result = "".join(parts).replace("\n", newline)

AUTHORITATIVE.write_text(result, encoding="utf-8", newline="")
MIRROR.write_text(result, encoding="utf-8", newline="")
print(f"Updated {len(changed)} militia/reserve records to quarter-cost upkeep and excess penalty.")
for item in changed:
    print(f"{item['unit']}: {item['before']} -> {item['after']}")
