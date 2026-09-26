from collections import deque
from pathlib import Path
import json
import math
import shutil

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = (184, 173, 143, 255)
BACKUP = ROOT / "tools/backup_before_final_reported_card_repairs_20260925"


def distance(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def strict_background_cutout(image, reference_limit=None, local_only=False):
    """Remove only border-connected pixels belonging to the corner background.

    The reference-colour bound prevents a flood from walking gradually through pale
    uniforms or skin; the neighbour bound permits only the small variation present
    inside the original card background.
    """
    image = image.convert("RGBA")
    px = image.load()
    width, height = image.size
    corners = [px[0, 0], px[width - 1, 0], px[0, height - 1], px[width - 1, height - 1]]
    reference = tuple(round(sum(c[i] for c in corners) / 4) for i in range(4))
    if reference_limit is None:
        reference_limit = 18 if width <= 48 else 48
    neighbour_limit = 14 if width <= 48 else 18
    queue = deque()
    seen = set()
    for x in range(width):
        queue.extend(((x, 0), (x, height - 1)))
    for y in range(height):
        queue.extend(((0, y), (width - 1, y)))
    background = set()
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        current = px[x, y]
        if current[3] < 16:
            background.add((x, y))
        elif local_only or distance(current, reference) <= reference_limit:
            background.add((x, y))
        else:
            continue
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in seen:
                neighbour = px[nx, ny]
                if neighbour[3] < 16 or (
                    (local_only or distance(neighbour, reference) <= reference_limit)
                    and distance(neighbour, current) <= neighbour_limit
                ):
                    queue.append((nx, ny))
    cutout = image.copy()
    out = cutout.load()
    for x, y in background:
        out[x, y] = (0, 0, 0, 0)
    return cutout, len(background)


def prepare(source, crop=None, reference_limit=None, local_only=False):
    image = Image.open(ROOT / source).convert("RGBA")
    if crop:
        image = image.crop(crop)
    if image.getchannel("A").getextrema()[0] == 255:
        image, removed = strict_background_cutout(image, reference_limit, local_only)
    else:
        removed = sum(1 for alpha in image.getchannel("A").getdata() if alpha == 0)
    if image.size != (48, 64):
        image = image.resize((48, 64), Image.Resampling.LANCZOS)
    background = Image.new("RGBA", (48, 64), CANONICAL)
    background.alpha_composite(image)
    return background, removed


jobs = [
    {
        "source": "tools/backup_before_remaining_mercenary_standardization_20260922/cards/mercs/#merc_pol_hussars.tga",
        "targets": [
            "data/ui/units/mercs/#merc_pol_hussars.tga",
            "data/ui/units/slave/#merc_pol_hussars.tga",
            "data/ui/units/hre/#merc_pol_hussars.tga",
            "data/ui/units/russia/#merc_pol_hussars.tga",
        ],
    },
    {
        "source": "tools/card_source_archive/all_cards_before_systemic_background_20260923/poland/#bra_marines_mid.tga",
        "targets": ["data/ui/units/poland/#bra_marines_mid.tga"],
    },
    {
        "source": "tools/backup_before_brazil_followup_20260915/cards/#bra_cacadores_early.tga",
        "targets": ["data/ui/units/poland/#bra_cacadores_early.tga"],
    },
    {
        "source": "tools/backup_before_brazil_followup_20260915/cards/#bra_cacadores_mid.tga",
        "targets": ["data/ui/units/poland/#bra_cacadores_mid.tga"],
    },
    {
        "source": "tools/backup_before_brazil_followup_20260915/cards/#bra_atiradores_high.tga",
        "targets": ["data/ui/units/poland/#bra_atiradores_high.tga"],
    },
    {
        "source": "tools/card_generation_sources/aus_general_staff_master.png",
        "crop": (80, 0, 880, 1067),
        "targets": ["data/ui/units/hungary/#aus_general_staff.tga"],
    },
    {
        "source": "tools/backup_before_remaining_mercenary_standardization_20260922/cards/mercs/#merc_kok_royal_cav.tga",
        "targets": [
            "data/ui/units/mercs/#merc_kok_royal_cav.tga",
            "data/ui/units/slave/#merc_kok_royal_cav.tga",
            "data/ui/units/byzantium/#merc_kok_royal_cav.tga",
            "data/ui/units/russia/#merc_kok_royal_cav.tga",
            "data/ui/units/timurids/#merc_kok_royal_cav.tga",
        ],
    },
    {
        "source": "tools/backup_before_qing_followup_repair_20260919/cards/#byz_armstrong.tga",
        "local_only": True,
        "targets": [
            "data/ui/units/byzantium/#byz_armstrong.tga",
            "data/ui/units/cru/#byz_armstrong.tga",
            "data/ui/units/slave/#byz_armstrong.tga",
        ],
    },
    {
        "source": "tools/card_source_archive/indian_princely_before_balance_20260917/#ind_5lb.tga",
        "targets": [
            "data/ui/units/bulga/#ind_5lb.tga",
            "data/ui/units/egypt/#ind_5lb.tga",
            "data/ui/units/timurids/#ind_5lb.tga",
            "data/ui/units/slave/#ind_5lb.tga",
        ],
    },
]

report = []
for job in jobs:
    output, removed = prepare(
        job["source"], job.get("crop"), job.get("reference_limit"), job.get("local_only", False)
    )
    for relative in job["targets"]:
        target = ROOT / relative
        if target.exists():
            backup = BACKUP / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                shutil.copy2(target, backup)
        target.parent.mkdir(parents=True, exist_ok=True)
        output.save(target, format="TGA", bits=32, compression="tga_rle")
    report.append({"source": job["source"], "targets": job["targets"], "background_pixels_removed": removed})

(ROOT / "tools/final_reported_card_repairs_20260925.json").write_text(
    json.dumps(report, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps({"compositions": len(jobs), "physical_cards": sum(len(j["targets"]) for j in jobs)}, indent=2))
