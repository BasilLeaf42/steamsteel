"""Report texture-coordinate bounds used by face and headwear mesh groups."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> None:
    lines = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace").splitlines()
    uv_set = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    uv_start = next(i for i, line in enumerate(lines) if f"start of pair data {uv_set}" in line)
    uv_end = next(i for i in range(uv_start + 1, len(lines)) if f"end of pair data {uv_set}" in lines[i])
    uv: dict[int, tuple[float, float]] = {}
    pattern = re.compile(r"\s*([-0-9.]+)\s+([-0-9.]+)\s+# mesh pair data values\s+(\d+)")
    for line in lines[uv_start:uv_end]:
        match = pattern.match(line)
        if match:
            uv[int(match.group(3))] = (float(match.group(1)), float(match.group(2)))

    starts = [i for i, line in enumerate(lines) if "start triangle group" in line]
    for start in starts:
        end = next(i for i in range(start + 1, len(lines)) if "end   triangle group" in lines[i])
        segment = lines[start:end]
        names = []
        for label in ("name1", "name2"):
            match = next((re.match(r"\s*\d+\s+(\S+)\s+# name size and mesh " + label, line) for line in segment if "mesh " + label in line), None)
            names.append(match.group(1) if match else "")
        if names[0] not in {"head", "heads", "beard", "fez", "turban"}:
            continue
        indices = []
        for line in segment:
            match = re.match(r"\s*(\d+)\s+(\d+)\s+(\d+)\s+# mesh vertex triangle indexes", line)
            if match:
                indices.extend(map(int, match.groups()))
        coords = [uv[index] for index in set(indices) if index in uv]
        bounds = min(x for x, _ in coords), min(y for _, y in coords), max(x for x, _ in coords), max(y for _, y in coords)
        print(names[0], names[1], len(set(indices)), *(f"{value:.4f}" for value in bounds))


if __name__ == "__main__":
    main()
