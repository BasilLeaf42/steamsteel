"""Restore and locally recolour the native Omani face UV islands."""

from __future__ import annotations

import io
import re
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
TEXTURES = ROOT / "data" / "unit_models" / "_Units"
ARCHIVE_DIR = ROOT / "tools" / "texture_source_archive" / "oman_before_face_fix"
OUT_DIR = ROOT / "tools" / "mesh_work" / "oman_faces" / "tga"
INF_TARGET = TEXTURES / "oma" / "textures" / "oma_inf_2g.texture"
INF_DONOR = TEXTURES / "ott" / "textures" / "ott_inf_2g.texture"
BEARER_DUMP = ROOT / "tools/mesh_work/oman_bearer/audit/oma_standard_bearer_lod0.txt"
CAV_TARGET = TEXTURES / "oma" / "textures" / "oma_cav_1g.texture"
CAV_BOXES = ((696, 510, 768, 686), (720, 714, 832, 856),
             (8, 816, 142, 886), (74, 890, 572, 1024))
BALUSH_SOURCE = TEXTURES / "nej" / "textures" / "nej_inf_1g.texture"
BALUSH_DUMP = ROOT / "tools/mesh_work/oman_faces/balush/nej_inf_1g_lod0.txt"
NIZAMIYE_SOURCE = TEXTURES / "nej" / "textures" / "nej_inf_2g.texture"
NIZAMIYE_DUMP = ROOT / "tools/mesh_work/oman_faces/nizamiye/nej_inf_2g_lod0.txt"
ATTACHMENTS = TEXTURES / "attachments" / "textures"
BALUSH_FACE_SOURCE = ATTACHMENTS / "per_tribal.texture"
NIZAMIYE_FACE_SOURCE = ATTACHMENTS / "per_rugbxx.texture"


def open_texture(path: Path) -> Image.Image:
    raw = path.read_bytes()
    if raw[48:52] != b"DDS ":
        raise ValueError(f"Not a Medieval II texture container: {path}")
    return Image.open(io.BytesIO(raw[48:])).convert("RGBA")


def group_mask(dump: Path, size: tuple[int, int], group_names: set[str], uv_set: int = 0,
               u_scale: float = 1.0) -> np.ndarray:
    """Rasterise selected mesh groups, including double-atlas U offsets."""
    lines = dump.read_text(encoding="utf-8", errors="replace").splitlines()
    uv_start = next(i for i, line in enumerate(lines) if f"start of pair data {uv_set}" in line)
    uv_end = next(i for i in range(uv_start + 1, len(lines)) if f"end of pair data {uv_set}" in lines[i])
    uv = {}
    pair = re.compile(r"\s*([-0-9.]+)\s+([-0-9.]+)\s+# mesh pair data values\s+(\d+)")
    for line in lines[uv_start:uv_end]:
        match = pair.match(line)
        if match:
            uv[int(match.group(3))] = (float(match.group(1)), float(match.group(2)))

    triangles = []
    starts = [i for i, line in enumerate(lines) if "start triangle group" in line]
    tri_pattern = re.compile(r"\s*(\d+)\s+(\d+)\s+(\d+)\s+# mesh vertex triangle indexes")
    name_pattern = re.compile(r"\s*\d+\s+(\S+)\s+# name size and mesh name1")
    for start in starts:
        end = next(i for i in range(start + 1, len(lines)) if "end   triangle group" in lines[i])
        segment = lines[start:end]
        match = next((name_pattern.match(line) for line in segment if "mesh name1" in line), None)
        if not match or match.group(1) not in group_names:
            continue
        for line in segment:
            match = tri_pattern.match(line)
            if match:
                triangles.append(tuple(map(int, match.groups())))
    if not triangles:
        raise ValueError(f"No {sorted(group_names)} triangles found in {dump}")

    width, height = size
    canvas = Image.new("L", size, 0)
    draw = ImageDraw.Draw(canvas)
    for triangle in triangles:
        coords = [(uv[index][0] * u_scale, uv[index][1]) for index in triangle]
        # Unwrap each small triangle locally, then rasterise periodic copies.
        unwrapped = [coords[0]]
        for u, v in coords[1:]:
            ref_u, ref_v = unwrapped[0]
            while u - ref_u > 0.5:
                u -= 1.0
            while u - ref_u < -0.5:
                u += 1.0
            while v - ref_v > 0.5:
                v -= 1.0
            while v - ref_v < -0.5:
                v += 1.0
            unwrapped.append((u, v))
        for shift_u in range(-3, 4):
            for shift_v in range(-1, 2):
                shifted = [(u + shift_u, v + shift_v) for u, v in unwrapped]
                if max(u for u, _ in shifted) < 0 or min(u for u, _ in shifted) > 1:
                    continue
                if max(v for _, v in shifted) < 0 or min(v for _, v in shifted) > 1:
                    continue
                points = [(round(u * (width - 1)), round(v * (height - 1)))
                          for u, v in shifted]
                draw.polygon(points, fill=255)
    return np.asarray(canvas.filter(ImageFilter.MaxFilter(5))) > 0


def face_mask(dump: Path, size: tuple[int, int], uv_set: int = 0,
              u_scale: float = 1.0) -> np.ndarray:
    return group_mask(dump, size, {"head", "heads"}, uv_set, u_scale)


def warm_omani_skin(image: Image.Image, regions) -> Image.Image:
    pixels = np.asarray(image).copy()
    if isinstance(regions, np.ndarray):
        region_masks = [regions]
    else:
        region_masks = []
        for left, top, right, bottom in regions:
            mask = np.zeros(pixels.shape[:2], dtype=bool)
            mask[top:bottom, left:right] = True
            region_masks.append(mask)
    for region in region_masks:
        area = pixels[..., :3].astype(np.float32)
        r, g, b = area[..., 0], area[..., 1], area[..., 2]
        # Isolate warm skin pixels while retaining hair, eyes, cloth and black
        # transparent padding. The target palette is a medium Arabian brown;
        # luminance detail is retained so the faces do not become flat masks.
        mask = region & (r > 55) & (g > 32) & (b > 20) & (r > g * 1.015) & (g > b * 1.005)
        luminance = r * 0.299 + g * 0.587 + b * 0.114
        toned = np.stack((luminance * 0.78 + 25,
                          luminance * 0.55 + 18,
                          luminance * 0.40 + 15), axis=-1)
        area[mask] = area[mask] * 0.15 + toned[mask] * 0.85
        pixels[..., :3] = np.clip(area, 0, 255).astype(np.uint8)
    return Image.fromarray(pixels, "RGBA")


def archived(path: Path) -> Path:
    archive = ARCHIVE_DIR / path.name
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    if not archive.exists():
        shutil.copy2(path, archive)
    return archive


def main() -> None:
    infantry = open_texture(archived(INF_TARGET))
    cavalry = open_texture(archived(CAV_TARGET))
    balush = open_texture(BALUSH_SOURCE)
    nizamiye = open_texture(NIZAMIYE_SOURCE)
    balush_faces = open_texture(BALUSH_FACE_SOURCE)
    nizamiye_faces = open_texture(NIZAMIYE_FACE_SOURCE)
    if any(image.size != (1024, 1024) for image in (infantry, cavalry, nizamiye,
                                                     balush_faces, nizamiye_faces)) or balush.size != (2048, 2048):
        raise ValueError("Unexpected native Omani atlas dimensions")

    flag_mask = group_mask(BEARER_DUMP, infantry.size, {"primaryactive0"}, u_scale=2.0)
    # The collapsed flag samples main-atlas UV (0.0625, 0.03125). Pad the
    # exact area for bilinear filtering and mipmaps.
    flag_mask[0:64, 32:96] = True
    infantry_pixels = np.asarray(infantry).copy()
    infantry_pixels[flag_mask] = (132, 0, 8, 255)
    infantry = Image.fromarray(infantry_pixels, "RGBA")
    cavalry = warm_omani_skin(cavalry, CAV_BOXES)
    # Head primitives use the attachment material. IWTE's renderer-ready GLB
    # confirms that its U coordinate is raw U * 2 with normal wrapping.
    balush_faces = warm_omani_skin(balush_faces, face_mask(BALUSH_DUMP, balush_faces.size, u_scale=2.0))
    nizamiye_faces = warm_omani_skin(nizamiye_faces, face_mask(NIZAMIYE_DUMP, nizamiye_faces.size, u_scale=2.0))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    infantry.save(OUT_DIR / "oma_inf_2g.tga")
    cavalry.save(OUT_DIR / "oma_cav_1g.tga")
    balush.save(OUT_DIR / "oma_balush_1g.tga")
    nizamiye.save(OUT_DIR / "oma_nizamiye_2g.tga")
    balush_faces.save(OUT_DIR / "oma_balush_faces.tga")
    nizamiye_faces.save(OUT_DIR / "oma_nizamiye_faces.tga")
    print("Built repaired Omani body and dedicated face-attachment atlases.")


if __name__ == "__main__":
    main()
