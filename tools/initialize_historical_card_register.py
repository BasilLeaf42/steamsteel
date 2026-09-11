from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import prepare_balanced_card_generation as cards


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools/balanced_card_generation_manifest.json"
REGISTER = ROOT / "tools/historical_card_sources.json"
EDU = ROOT / "data/tow_steamsteel/export_descr_unit.txt"
DEFAULT_SKIRMISHER_POSES = (
    "kneel_aim_waud_1860_65",
    "kneel_aim_photo_1871",
    "kneel_drill_plate_xvi_1862",
)


def default_pose(unit_type: str, role: str) -> str:
    if "skirmisher" not in role.lower() and "sharpshooter" not in role.lower():
        return ""
    return DEFAULT_SKIRMISHER_POSES[sum(unit_type.encode("utf-8")) % len(DEFAULT_SKIRMISHER_POSES)]


def edu_records() -> dict[str, dict[str, str]]:
    text = EDU.read_text(encoding="utf-8", errors="replace").replace("\r", "")
    result = {}
    for block in re.split(r"(?=^type\s+)", text, flags=re.MULTILINE):
        record = cards.fields(block)
        if "type" not in record:
            continue
        record["type"] = record["type"].split(";", 1)[0].strip()
        result[record["type"]] = record
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--migrate", action="store_true")
    args = parser.parse_args()
    if REGISTER.exists() and not args.migrate:
        raise SystemExit(f"refusing to overwrite {REGISTER}; pass --migrate explicitly")

    groups = json.loads(MANIFEST.read_text(encoding="utf-8"))
    units = edu_records()
    previous = json.loads(REGISTER.read_text(encoding="utf-8")) if REGISTER.exists() else []
    previous_by_unit = {
        record.get("unit_type", record.get("representative", "")): record for record in previous
    }
    records = []
    for group in groups:
        for member in group["members"]:
            target = Path(member)
            unit_type = target.stem.lstrip("#")
            record = units[unit_type]
            display = record.get("dictionary", unit_type).split(";", 1)[-1].strip()
            prior = previous_by_unit.get(unit_type, {})
            role = cards.role(record)
            records.append(
                {
                    "id": unit_type,
                    "group_id": group["id"],
                    "unit_type": unit_type,
                    "card_file": str(target.relative_to(ROOT)).replace("\\", "/"),
                    "faction": target.parent.name,
                    "name": display,
                    "role": role,
                    "weapon": cards.weapon(record),
                    "source_url": prior.get("source_url", ""),
                    "source_file": prior.get("source_file", ""),
                    "source_title": prior.get("source_title", ""),
                    "creator": prior.get("creator", ""),
                    "source_date": prior.get("source_date", ""),
                    "licence": prior.get("licence", ""),
                    "depicted_subject": prior.get("depicted_subject", ""),
                    "mapping_note": prior.get("mapping_note", ""),
                    "pose_source_id": prior.get("pose_source_id") or default_pose(unit_type, role),
                    "status": prior.get("status", "pending"),
                    "generated_file": prior.get("generated_file", prior.get("pilot_file", "")),
                    "crop_box": prior.get("crop_box", []),
                }
            )
    REGISTER.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"created {REGISTER} with {len(records)} unit records")


if __name__ == "__main__":
    main()
