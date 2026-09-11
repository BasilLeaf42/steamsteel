from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from PIL import Image

import standardize_card_backgrounds as backgrounds


REQUIRED_SOURCE_FIELDS = (
    "source_url",
    "source_file",
    "source_title",
    "creator",
    "source_date",
    "licence",
    "depicted_subject",
    "mapping_note",
)
APPROVED_SOURCE_STATUSES = {"card-approved", "pilot-approved"}
POSE_REGISTER = "tools/historical_skirmisher_pose_sources.json"


def is_skirmisher(record: dict) -> bool:
    role = str(record.get("role", "")).lower()
    return "skirmisher" in role or "sharpshooter" in role


def crop_to_card_aspect(image: Image.Image) -> Image.Image:
    """Crop without distortion to the tactical card's 3:4 aspect ratio."""
    width, height = image.size
    target_ratio = 3 / 4
    if width / height > target_ratio:
        crop_width = round(height * target_ratio)
        left = (width - crop_width) // 2
        return image.crop((left, 0, left + crop_width, height))
    if width / height < target_ratio:
        crop_height = round(width / target_ratio)
        # Preserve the head and upper torso; remove excess lower-body space.
        return image.crop((0, 0, width, crop_height))
    return image


def validate_historical_sources(root: Path, manifest: list[dict]) -> dict[str, dict]:
    register_path = root / "tools/historical_card_sources.json"
    register = json.loads(register_path.read_text(encoding="utf-8"))
    pose_register = json.loads((root / POSE_REGISTER).read_text(encoding="utf-8"))
    poses = {record["id"]: record for record in pose_register}
    by_id = {record["unit_type"]: record for record in register}
    failures = []
    for group in manifest:
        for target_name in group["members"]:
            unit_type = Path(target_name).stem.lstrip("#")
            record = by_id.get(unit_type)
            if record is None:
                failures.append(f"missing source record: {unit_type}")
                continue
            missing = [field for field in REQUIRED_SOURCE_FIELDS if not str(record.get(field, "")).strip()]
            if missing:
                failures.append(f"incomplete source record {unit_type}: {', '.join(missing)}")
            source_file = root / str(record.get("source_file", ""))
            if not source_file.is_file():
                failures.append(f"missing historical source file {unit_type}: {source_file}")
            if record.get("status") not in APPROVED_SOURCE_STATUSES:
                failures.append(
                    f"unapproved historical source {unit_type}: {record.get('status', 'missing')}"
                )
            pose_id = str(record.get("pose_source_id", "")).strip()
            if is_skirmisher(record):
                pose = poses.get(pose_id)
                if not pose_id:
                    failures.append(f"missing kneeling pose source: {unit_type}")
                elif pose is None:
                    failures.append(f"unknown kneeling pose source {pose_id}: {unit_type}")
                else:
                    pose_missing = [field for field in REQUIRED_SOURCE_FIELDS if not str(pose.get(field, "")).strip()]
                    if pose_missing:
                        failures.append(f"incomplete pose source {pose_id}: {', '.join(pose_missing)}")
                    pose_file = root / str(pose.get("source_file", ""))
                    if not pose_file.is_file():
                        failures.append(f"missing pose source file {pose_id}: {pose_file}")
                    if pose.get("status") != "approved":
                        failures.append(f"unapproved pose source {pose_id}: {unit_type}")
            elif pose_id:
                failures.append(f"pose source assigned to non-skirmisher {unit_type}: {pose_id}")
    for field in ("source_url", "source_file"):
        counts = Counter(
            str(record.get(field, "")).strip()
            for record in register
            if str(record.get(field, "")).strip()
        )
        for value, count in counts.items():
            if count > 1:
                failures.append(f"historical {field} reused by {count} units: {value}")
    for pose_id, pose in poses.items():
        base_file = str(pose.get("base_file", "")).strip()
        if base_file and (pose.get("base_status") != "approved" or not (root / base_file).is_file()):
            failures.append(f"invalid approved generated base for pose {pose_id}: {base_file}")
    if failures:
        raise SystemExit("historical-source gate failed:\n" + "\n".join(failures))
    return by_id


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sources", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "tools/balanced_card_generation_manifest.json").read_text(encoding="utf-8"))
    source_register = validate_historical_sources(root, manifest)

    installed = 0
    missing = []
    for group in manifest:
        for target_name in group["members"]:
            target = Path(target_name)
            unit_type = target.stem.lstrip("#")
            generated = str(source_register[unit_type].get("generated_file", "")).strip()
            source = root / generated if generated else args.sources / f"{unit_type}.png"
            if not source.is_file():
                missing.append(source)
                continue
            image = Image.open(source).convert("RGBA")
            crop_box = source_register[unit_type].get("crop_box", [])
            if crop_box:
                if len(crop_box) != 4:
                    raise SystemExit(f"invalid crop_box for {unit_type}: {crop_box}")
                image = image.crop(tuple(int(value) for value in crop_box))
            image = crop_to_card_aspect(image)
            image = image.resize((48, 64), Image.Resampling.LANCZOS)
            image, _ = backgrounds.replace_connected_background(image)
            temporary = target.with_name(f"codex_card_{target.stem.lstrip('#')}.tmp.tga")
            image.save(temporary, format="TGA", bits=32, compression="tga_rle")
            temporary.replace(target)
            installed += 1

    if missing:
        raise SystemExit("missing generated sources:\n" + "\n".join(str(path) for path in missing))

    failures = []
    validated = 0
    for group in manifest:
        for target_name in group["members"]:
            target = Path(target_name)
            raw = target.read_bytes()
            image = Image.open(target).convert("RGBA")
            if image.size != (48, 64) or raw[16] != 32:
                failures.append(str(target))
            # A hand, weapon, horse, or cast shadow may naturally leave the frame
            # through a corner.  Validate the connected parchment field over the
            # upper/side border instead of requiring all four corner pixels to be
            # empty background.
            border = [
                (x, y)
                for y in range(48)
                for x in range(48)
                if x < 2 or x >= 46 or y < 2
            ]
            canonical_fraction = sum(
                image.getpixel(point) == backgrounds.CANONICAL for point in border
            ) / len(border)
            if canonical_fraction < 0.5:
                failures.append(f"insufficient canonical card background: {target}")
            if image.getchannel("A").getextrema() != (255, 255):
                failures.append(f"nonopaque alpha: {target}")
            validated += 1
    if failures:
        raise SystemExit("invalid installed cards:\n" + "\n".join(failures))
    print(f"installed={installed}; validated={validated}; historical unit sources={len(source_register)}")


if __name__ == "__main__":
    main()
