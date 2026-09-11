from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path

from PIL import Image

import audit_balanced_unit_card_donors as audit
import standardize_card_backgrounds as backgrounds


def donor_map(root: Path) -> tuple[dict[Path, Path], list[Path]]:
    edu_path = root / "data/tow_steamsteel/export_descr_unit.txt"
    edu_text = edu_path.read_text(encoding="utf-8", errors="replace").replace("\r", "")
    model_text = (root / "data/unit_models/battle_models.modeldb").read_text(
        encoding="utf-8", errors="replace"
    ).replace("\r", "")
    records = audit.edu_records(edu_text)
    by_type = {record["type"]: record for record in records}
    signatures = audit.model_visual_signatures(model_text)
    models_by_signature: dict[tuple[str, ...], list[str]] = defaultdict(list)
    records_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for model, signature in signatures.items():
        models_by_signature[signature].append(model)
    for record in records:
        records_by_model[record["soldier"]].append(record)

    targets = audit.target_types(edu_text.splitlines())
    all_targets = {unit_type for types in targets.values() for unit_type in types}
    resolved: dict[Path, Path] = {}
    unresolved: list[Path] = []
    for faction, types in targets.items():
        for unit_type in types:
            target = root / f"data/ui/units/{faction}/#{unit_type}.tga"
            record = by_type[unit_type]
            signature = signatures.get(record["soldier"])
            equivalent_models = models_by_signature.get(signature, []) if signature else []
            candidates: list[tuple[int, str, Path]] = []
            for model in equivalent_models:
                card = root / f"data/ui/units/{faction}/#{model}.tga"
                if model not in all_targets and card.is_file():
                    candidates.append((0, model, card))
            for model in equivalent_models:
                for candidate in records_by_model.get(model, []):
                    card = root / f"data/ui/units/{faction}/#{candidate['type']}.tga"
                    if candidate["type"] not in all_targets and card.is_file():
                        candidates.append((1, candidate["type"], card))
            if candidates:
                candidates.sort(key=lambda item: (item[0], item[1]))
                resolved[target] = candidates[0][2]
            else:
                unresolved.append(target)
    return resolved, unresolved


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.apply == bool(args.output_root):
        parser.error("choose exactly one of --apply or --output-root")

    resolved, unresolved = donor_map(args.root)
    changed = 0
    for target, donor in resolved.items():
        original_hash = hashlib.sha256(target.read_bytes()).digest()
        image = Image.open(donor).convert("RGBA")
        if image.size != (48, 64):
            raise SystemExit(f"unexpected donor dimensions for {donor}: {image.size}")
        image, _ = backgrounds.replace_connected_background(image)
        if args.apply:
            destination = target
        else:
            destination = args.output_root / target.relative_to(args.root)
            destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination, format="TGA", bits=32, compression="tga_rle")
        if original_hash != hashlib.sha256(destination.read_bytes()).digest():
            changed += 1

    # Preserve manually verified cards for unique models, but run the same
    # canonical-background pass over them in preview and apply modes.
    for target in unresolved:
        image = Image.open(target).convert("RGBA")
        image, _ = backgrounds.replace_connected_background(image)
        if args.apply:
            destination = target
        else:
            destination = args.output_root / target.relative_to(args.root)
            destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination, format="TGA", bits=32, compression="tga_rle")

    print(f"exact model donors={len(resolved)}; changed={changed}; unique/manual={len(unresolved)}")
    for target in unresolved:
        print(f"manual\t{target.relative_to(args.root)}")


if __name__ == "__main__":
    main()
