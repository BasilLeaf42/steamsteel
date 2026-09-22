"""Validate restored Omani donor faces and the isolated plain-red flag."""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
from PIL import Image

from repair_oman_faces import face_mask, group_mask


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "tools/texture_source_archive/oman_before_face_fix"
DONOR = ROOT / "data/unit_models/_Units/attachments/textures/per_rugbxx.texture"
BEARER_DUMP = ROOT / "tools/mesh_work/ottoman_bearer/audit/ott_standard_bearer_lod0.txt"


def pixels(path: Path) -> np.ndarray:
    raw = path.read_bytes()
    assert raw[48:52] == b"DDS ", f"{path}: invalid texture container"
    return np.asarray(Image.open(io.BytesIO(raw[48:])).convert("RGBA"), dtype=np.int16)


def main() -> None:
    base = ROOT / "data/unit_models/_Units/oma/textures"
    for name in ("oma_inf_2g.texture", "oma_cav_1g.texture"):
        assert (base / name).read_bytes() == (ARCHIVE / name).read_bytes(), f"{name}: original texture not restored"
    for name in ("oma_balush_1g.texture", "oma_balush_faces.texture",
                 "oma_nizamiye_2g.texture", "oma_nizamiye_faces.texture"):
        assert not (base / name).exists(), f"{name}: obsolete face-remap asset still installed"

    donor = pixels(DONOR)
    flag = pixels(ROOT / "data/unit_models/_Units/bnw/textures/oma_standard_flag.texture")
    flag_uv = group_mask(BEARER_DUMP, (1024, 1024), {"primaryactive0"}, u_scale=2.0)
    heads = face_mask(BEARER_DUMP, (1024, 1024), u_scale=2.0)
    flag_region = np.zeros((1024, 1024), dtype=bool)
    flag_region[:, 8:504] = True
    red = (flag[..., 0] > 115) & (flag[..., 0] < 155) & (flag[..., 1] < 15) & (flag[..., 2] < 22)
    assert np.count_nonzero(flag_uv & red) / np.count_nonzero(flag_uv) > 0.99, "Omani standard is not plain deep red"
    assert np.abs(flag[heads, :3] - donor[heads, :3]).mean() < 1, "Omani bearer donor faces changed"
    assert np.abs(flag[~flag_region, :3] - donor[~flag_region, :3]).mean() < 1, "Omani bearer atlas changed outside flag blocks"
    print("PASS: original Omani textures restored; bearer keeps donor faces and carries a plain-red standard.")


if __name__ == "__main__":
    main()
