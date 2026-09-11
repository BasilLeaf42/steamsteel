from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


REQUIRED_FIELDS = (
    "source_url", "source_file", "source_title", "creator", "source_date", "licence",
    "depicted_subject", "mapping_note",
)
SOURCED = {"source-approved", "card-approved", "pilot-approved"}
CARD_APPROVED = {"card-approved", "pilot-approved"}
POSE_REGISTER = "tools/historical_skirmisher_pose_sources.json"


def is_skirmisher(record: dict) -> bool:
    role = str(record.get("role", "")).lower()
    return "skirmisher" in role or "sharpshooter" in role


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "tools/balanced_card_generation_manifest.json").read_text(encoding="utf-8"))
    register = json.loads((root / "tools/historical_card_sources.json").read_text(encoding="utf-8"))
    pose_register = json.loads((root / POSE_REGISTER).read_text(encoding="utf-8"))
    poses = {record["id"]: record for record in pose_register}
    expected = {
        Path(target).stem.lstrip("#")
        for group in manifest
        for target in group["members"]
    }
    by_unit = {record["unit_type"]: record for record in register}
    failures: list[str] = []
    sourced_by_faction: Counter[str] = Counter()
    approved_by_faction: Counter[str] = Counter()
    total_by_faction: Counter[str] = Counter()

    for unit_type in sorted(expected):
        record = by_unit.get(unit_type)
        if record is None:
            failures.append(f"{unit_type}: missing register record")
            continue
        total_by_faction[record["faction"]] += 1
        missing = [field for field in REQUIRED_FIELDS if not str(record.get(field, "")).strip()]
        source_file = root / str(record.get("source_file", ""))
        if missing:
            failures.append(f"{unit_type}: missing {', '.join(missing)}")
        if record.get("status") not in SOURCED:
            failures.append(f"{unit_type}: source status is {record.get('status', 'missing')}")
        elif not missing and source_file.is_file():
            sourced_by_faction[record["faction"]] += 1
            if record.get("status") in CARD_APPROVED:
                approved_by_faction[record["faction"]] += 1
        if record.get("source_file") and not source_file.is_file():
            failures.append(f"{unit_type}: source file not found: {source_file}")
        pose_id = str(record.get("pose_source_id", "")).strip()
        if is_skirmisher(record):
            if not pose_id:
                failures.append(f"{unit_type}: missing approved kneeling pose_source_id")
            elif pose_id not in poses:
                failures.append(f"{unit_type}: unknown pose_source_id {pose_id}")
            else:
                pose = poses[pose_id]
                pose_missing = [field for field in REQUIRED_FIELDS if not str(pose.get(field, "")).strip()]
                if pose_missing:
                    failures.append(f"pose {pose_id}: missing {', '.join(pose_missing)}")
                if pose.get("status") != "approved":
                    failures.append(f"{unit_type}: pose {pose_id} is not approved")
                pose_file = root / str(pose.get("source_file", ""))
                if not pose_file.is_file():
                    failures.append(f"pose {pose_id}: source file not found: {pose_file}")
        elif pose_id:
            failures.append(f"{unit_type}: pose_source_id is only permitted for skirmishers/sharpshooters")

    failures.extend(f"{unit_type}: stale register record" for unit_type in sorted(set(by_unit) - expected))
    for field in ("source_url", "source_file"):
        duplicates = Counter(
            str(record.get(field, "")).strip()
            for record in register
            if str(record.get(field, "")).strip()
        )
        for value, count in duplicates.items():
            if count > 1:
                failures.append(f"{field} reused by {count} units: {value}")

    for pose_id, pose in poses.items():
        if not is_skirmisher(pose):
            failures.append(f"pose {pose_id}: role must identify a skirmisher or sharpshooter pose")
        base_file = str(pose.get("base_file", "")).strip()
        if base_file:
            if pose.get("base_status") != "approved":
                failures.append(f"pose {pose_id}: generated base is not approved")
            if not (root / base_file).is_file():
                failures.append(f"pose {pose_id}: generated base file not found: {base_file}")

    for faction in sorted(total_by_faction):
        print(
            f"{faction}: {sourced_by_faction[faction]}/{total_by_faction[faction]} sourced; "
            f"{approved_by_faction[faction]}/{total_by_faction[faction]} cards approved"
        )
    print(
        f"total: {sum(sourced_by_faction.values())}/{len(expected)} sourced; "
        f"{sum(approved_by_faction.values())}/{len(expected)} cards approved"
    )
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
