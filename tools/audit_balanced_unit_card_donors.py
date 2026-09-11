from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path


ROSTER_BLOCKS = {
    "england": (6318, 7253),
    "spain": (7893, 8609),
    "france": (8610, 9639),
    "hre": (10144, 11131),
    "portugal": (11637, 12360),
    "sicily": (12689, 13235),
    "normans": (13251, 13975),
    "mongols": (14286, 14832),
}


def edu_records(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for block in re.split(r"(?=^type\s+)", text, flags=re.MULTILINE):
        unit_type = re.search(r"^type\s+(.+?)\s*$", block, flags=re.MULTILINE)
        soldier = re.search(r"^soldier\s+([^,;\s]+)", block, flags=re.MULTILINE)
        ownership = re.search(r"^ownership\s+(.+?)\s*$", block, flags=re.MULTILINE)
        if unit_type and soldier:
            records.append(
                {
                    "type": unit_type.group(1).split(";", 1)[0].strip(),
                    "soldier": soldier.group(1).strip(),
                    "ownership": ownership.group(1).strip() if ownership else "",
                }
            )
    return records


def model_visual_signatures(text: str) -> dict[str, tuple[str, ...]]:
    header = re.compile(r"^(\d+) ([^\s;]+);?\s*\n\d+ \d+;?\s*$", re.MULTILINE)
    matches = [match for match in header.finditer(text) if int(match.group(1)) == len(match.group(2))]
    signatures: dict[str, tuple[str, ...]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        entry = text[match.start() : end]
        visual_lines = []
        for line in entry.splitlines()[1:]:
            lower = line.lower()
            if ".mesh" in lower or ".texture" in lower or ".spr" in lower:
                visual_lines.append(re.sub(r"^\d+\s+", "", line.strip()))
        if visual_lines:
            signatures[match.group(2)] = tuple(visual_lines)
    return signatures


def target_types(edu_lines: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for faction, (start, end) in ROSTER_BLOCKS.items():
        result[faction] = [
            line.split(None, 1)[1].split(";", 1)[0].strip()
            for line in edu_lines[start - 1 : end]
            if line.startswith("type")
        ]
    return result


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    edu_path = root / "data/tow_steamsteel/export_descr_unit.txt"
    edu_text = edu_path.read_text(encoding="utf-8", errors="replace").replace("\r", "")
    model_text = (root / "data/unit_models/battle_models.modeldb").read_text(
        encoding="utf-8", errors="replace"
    ).replace("\r", "")
    records = edu_records(edu_text)
    by_type = {record["type"]: record for record in records}
    signatures = model_visual_signatures(model_text)
    models_by_signature: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for model, signature in signatures.items():
        models_by_signature[signature].append(model)
    records_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in records:
        records_by_model[record["soldier"]].append(record)

    targets = target_types(edu_text.splitlines())
    exact = 0
    unresolved = 0
    for faction, types in targets.items():
        for unit_type in types:
            record = by_type[unit_type]
            signature = signatures.get(record["soldier"])
            equivalent_models = models_by_signature.get(signature, []) if signature else []
            candidates: list[str] = []
            for model in equivalent_models:
                model_card = root / f"data/ui/units/{faction}/#{model}.tga"
                if model != unit_type and model_card.is_file():
                    candidates.append(f"@{model}")
            for model in equivalent_models:
                for candidate in records_by_model.get(model, []):
                    candidate_card = root / f"data/ui/units/{faction}/#{candidate['type']}.tga"
                    if candidate["type"] != unit_type and candidate_card.is_file():
                        candidates.append(candidate["type"])
            candidates = list(dict.fromkeys(candidates))
            if candidates:
                exact += 1
            else:
                unresolved += 1
            print(
                "\t".join(
                    [
                        faction,
                        unit_type,
                        record["soldier"],
                        ",".join(equivalent_models),
                        ",".join(candidates),
                    ]
                )
            )
    print(f"SUMMARY\texact={exact}\tunresolved={unresolved}")


if __name__ == "__main__":
    main()
