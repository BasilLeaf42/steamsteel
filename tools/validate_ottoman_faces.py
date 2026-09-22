"""Validate the Ottoman bearer flag while preserving donor faces."""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
from PIL import Image

from repair_oman_faces import face_mask, group_mask


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/unit_models/_Units/attachments/textures/per_rugbxx.texture"
BEARER_DUMP = ROOT / "tools/mesh_work/ottoman_bearer/audit/ott_standard_bearer_lod0.txt"
BUILT = ROOT / "tools/mesh_work/ottoman_bearer/tga"


def pixels(path: Path) -> np.ndarray:
    raw = path.read_bytes()
    assert raw[48:52] == b"DDS ", f"{path}: invalid texture container"
    return np.asarray(Image.open(io.BytesIO(raw[48:])).convert("RGBA"), dtype=np.int16)


def main() -> None:
    base = pixels(BASE)
    bearer = pixels(ROOT / "data/unit_models/_Units/bnw/textures/ott_standard_flag.texture")
    bearer_built = np.asarray(Image.open(BUILT / "ott_standard_flag.tga").convert("RGBA"), dtype=np.int16)
    heads = face_mask(BEARER_DUMP, (1024, 1024), u_scale=2.0)
    flag = group_mask(BEARER_DUMP, (1024, 1024), {"primaryactive0"}, u_scale=2.0)
    flag_region = np.zeros((1024, 1024), dtype=bool)
    flag_region[:, 8:504] = True
    assert not np.any(heads & flag), "Ottoman bearer flag overlaps head UVs"
    assert np.abs(bearer[flag, :3] - bearer_built[flag, :3]).mean() < 12, "installed Ottoman flag mismatch"
    red = (bearer[..., 0] > 115) & (bearer[..., 0] < 155) & (bearer[..., 1] < 15) & (bearer[..., 2] < 22)
    white = (bearer[..., 0] > 220) & (bearer[..., 1] > 220) & (bearer[..., 2] > 220)
    assert np.count_nonzero(flag & (red | white)) / np.count_nonzero(flag) > 0.97, "Ottoman flag retains bleached/donor colours"
    cloth_region = np.zeros((1024, 1024), dtype=bool)
    cloth_region[710:1016, 192:504] = True
    cloth = flag & cloth_region
    assert np.count_nonzero(cloth & white) / np.count_nonzero(cloth) > 0.04, "Ottoman crescent and star do not cover the rendered flag cloth"
    assert not np.any(white & flag_region & ~cloth_region), "Ottoman emblem crosses the flag cloth UV seam"
    untouched = ~(heads | flag_region)
    assert np.abs(bearer[untouched, :3] - base[untouched, :3]).mean() < 12, "Ottoman bearer atlas changed outside the flag region"
    assert np.abs(bearer[heads, :3] - base[heads, :3]).mean() < 12, "Ottoman bearer no longer preserves its donor faces"
    print("PASS: Ottoman bearer keeps its donor faces and uses an isolated deep-red flag.")


if __name__ == "__main__":
    main()
