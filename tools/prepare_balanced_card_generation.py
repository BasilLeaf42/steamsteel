from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

from PIL import Image

import audit_balanced_unit_card_donors as audit
import standardize_card_backgrounds as backgrounds


FACTION_NAMES = {
    "england": "British",
    "spain": "Spanish",
    "france": "French",
    "hre": "Prussian or German",
    "portugal": "Dutch",
    "sicily": "Danish",
    "normans": "Swedish or Norwegian",
    "mongols": "Greek",
}


def fields(block: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for key in ("type", "dictionary", "category", "class", "soldier", "attributes", "formation", "stat_pri", "stat_sec"):
        match = re.search(rf"^{key}\s+(.+?)\s*$", block, flags=re.MULTILINE)
        if match:
            result[key] = match.group(1).strip()
    return result


def role(record: dict[str, str]) -> str:
    category = record.get("category", "")
    attributes = record.get("attributes", "")
    primary = record.get("stat_pri", "")
    formation = record.get("formation", "")
    if "general_unit" in attributes:
        return "general"
    if category == "cavalry" and "carbine_bullet" in primary:
        return "carbine cavalry"
    if category == "cavalry" and "magazine_rifle_bullet_c" in primary:
        return "pistol cavalry"
    if category == "cavalry" and ", melee," in primary and ", spear," in primary:
        return "lancer cavalry"
    if category == "cavalry":
        return "melee cavalry"
    if category == "infantry" and formation.startswith("1.4, 1.8"):
        return "infantry skirmisher"
    return "infantry"


def weapon(record: dict[str, str]) -> str:
    comment = record.get("dictionary", "").split(";", 1)
    if len(comment) == 2:
        details = comment[1].strip()
        match = re.search(r";\s*([^;)]+(?:[)])?)\)$", details)
        if match:
            return match.group(1).strip()
        parenthetical = re.findall(r"\(([^()]*)\)", details)
        if parenthetical:
            return parenthetical[-1].split(";", 1)[-1].strip()
    return "the weapon shown in the reference"


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "tools/card_generation_refs"
    out.mkdir(exist_ok=True)

    edu = (root / "data/tow_steamsteel/export_descr_unit.txt").read_text(
        encoding="utf-8", errors="replace"
    ).replace("\r", "")
    model = (root / "data/unit_models/battle_models.modeldb").read_text(
        encoding="utf-8", errors="replace"
    ).replace("\r", "")
    signatures = audit.model_visual_signatures(model)
    records = {}
    for block in re.split(r"(?=^type\s+)", edu, flags=re.MULTILINE):
        record = fields(block)
        if "type" in record:
            record["type"] = record["type"].split(";", 1)[0].strip()
            record["soldier"] = record.get("soldier", "").split(",", 1)[0].strip()
            records[record["type"]] = record

    groups: dict[tuple[tuple[str, ...], str], list[tuple[str, str]]] = defaultdict(list)
    for faction, types in audit.target_types(edu.splitlines()).items():
        for unit_type in types:
            record = records[unit_type]
            signature = signatures.get(record["soldier"], (record["soldier"],))
            groups[(signature, role(record))].append((faction, unit_type))

    manifest = []
    for index, ((signature, unit_role), members) in enumerate(sorted(groups.items(), key=lambda item: item[1][0])):
        faction, representative = members[0]
        record = records[representative]
        digest = hashlib.sha1(("\n".join(signature) + unit_role).encode()).hexdigest()[:10]
        group_id = f"card_{index:03d}_{digest}"
        source = root / f"data/ui/units/{faction}/#{representative}.tga"
        reference = Image.open(source).convert("RGBA")
        reference, _ = backgrounds.replace_connected_background(reference)
        reference.resize((768, 1024), Image.Resampling.NEAREST).save(out / f"{group_id}.png")
        display = record.get("dictionary", representative).split(";", 1)[-1].strip()
        manifest.append(
            {
                "id": group_id,
                "representative": representative,
                "faction": faction,
                "nation": FACTION_NAMES[faction],
                "name": display,
                "role": unit_role,
                "weapon": weapon(record),
                "reference": str((out / f"{group_id}.png").resolve()),
                "members": [
                    str((root / f"data/ui/units/{member_faction}/#{member_type}.tga").resolve())
                    for member_faction, member_type in members
                ],
            }
        )

    manifest_path = root / "tools/balanced_card_generation_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"prepared={len(manifest)} visual-role groups; cards={sum(len(x['members']) for x in manifest)}")


if __name__ == "__main__":
    main()
