from collections import deque
from pathlib import Path
from PIL import Image
import json
import shutil
import struct

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/ui/units/bulga"
ARCHIVE = ROOT / "tools/card_source_archive/indian_princely_before_balance_20260917"
REGISTRY = ROOT / "tools/historical_card_sources.json"
BG = (184, 173, 143, 255)
ALL_CARDS = ["indian_bow_cav", "indian_spear_cav", "Sikh_heavy_cavalry", "indian_spears", "indian_heavy_banduqchis", "indian_new_musk", "india_sepoy", "sikh_gen", "sikh_warriors", "indian_fanatic", "indian_ele", "india_militia", "ind_bhutan_warrior", "ind_armstrong", "ind_12lb", "ind_5lb", "ind_maxim"]
GENERATED = {
    "indian_bow_cav": {"master": "indian_sowar_carbine_20260917.png", "role": "matchlock carbine cavalry", "weapon": "visible matchlock carbine and sheathed curved sword", "url": "https://commons.wikimedia.org/wiki/File:2nd_Punjab_Cavalry_Sowars,_India,_possibly_by_Felice_Beato,_ca.1858%E2%80%9359_(two).jpg", "source_file": "indian_sowars_1858_59.jpg", "source_title": "2nd Punjab Cavalry Sowars, India", "creator": "Possibly Felice Beato", "date": "ca. 1858-1859", "subject": "Sowars of the 2nd Punjab Cavalry", "pose": ""},
    "indian_spear_cav": {"master": "indian_risala_lancer_20260917.png", "role": "regional lancer cavalry", "weapon": "visible lance and sheathed curved sword", "url": "https://commons.wikimedia.org/wiki/File:Sikh_Lancers,_ca.1845.jpg", "source_file": "sikh_lancers_1845.jpg", "source_title": "Sikh Lancers", "creator": "Illustrated London News staff after Godfrey Vigne", "date": "ca. 1845", "subject": "Sikh lancer cavalry", "pose": ""},
    "indian_heavy_banduqchis": {"master": "indian_rajput_skirmisher_20260917.png", "role": "kneeling long-gun skirmisher", "weapon": "complete long gun and visible two-handed axe", "url": "https://commons.wikimedia.org/wiki/File:Rifle_and_spear_with_the_Rajpoots-_being_the_narrative_of_a_winter%27s_travel_and_sport_in_northern_India_(1895)_(14780337332).jpg", "source_file": "rajput_rifle_spear_1895.jpg", "source_title": "Rifle and spear with the Rajpoots", "creator": "Internet Archive Book Images; book by Nora Beatrice Blyth Gardner", "date": "1895", "subject": "Rajput riflemen in northern India", "pose": "kneel_aim_photo_1871"},
    "india_militia": {"master": "indian_wall_gunner_kneeling_20260917.png", "role": "kneeling wall-gun skirmisher", "weapon": "complete heavy matchlock wall gun and visible two-handed axe", "url": "https://commons.wikimedia.org/wiki/File:Buxerries_or_Native_Matchlock_men.jpg", "source_file": "indian_buxerries_matchlock_men.jpg", "source_title": "Buxerries or Native Matchlock men", "creator": "Anonymous; reproduced in Bengal in 1756-57 by S. C. Hill", "date": "historical subject 1756-1757; published 1905", "subject": "Indian native matchlock men", "pose": "kneel_aim_photo_1871"},
}

def long_path(path): return Path("\\\\?\\" + str(path.resolve()))

def flatten_generated(image):
    image = image.convert("RGBA"); pixels = image.load(); width, height = image.size
    queue = deque((x, y) for x in range(width) for y in (0, height - 1)); queue.extend((x, y) for y in range(height) for x in (0, width - 1)); seen = set()
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen: continue
        seen.add((x, y))
        colour = pixels[x, y]
        if colour[3] == 0 or max(colour[:3]) - min(colour[:3]) > 72: continue
        neighbours = []
        if x: neighbours.append((x - 1, y))
        if x + 1 < width: neighbours.append((x + 1, y))
        if y: neighbours.append((x, y - 1))
        if y + 1 < height: neighbours.append((x, y + 1))
        if (x not in (0, width - 1) and y not in (0, height - 1)) and not any(n in seen and sum((colour[i] - pixels[n][i]) ** 2 for i in range(3)) <= 18 ** 2 for n in neighbours): continue
        pixels[x, y] = BG
        queue.extend(neighbours)
    if image.getextrema()[3][0] < 255: image = Image.alpha_composite(Image.new("RGBA", image.size, BG), image)
    return image

def normalize_legacy(image):
    image = image.convert("RGBA")
    if image.getextrema()[3][0] < 255: return Image.alpha_composite(Image.new("RGBA", image.size, BG), image)
    pixels = image.load(); width, height = image.size
    samples = [pixels[0, 0], pixels[width - 1, 0], pixels[0, height - 1], pixels[width - 1, height - 1]]
    queue = deque((x, y) for x in range(width) for y in (0, height - 1)); queue.extend((x, y) for y in range(height) for x in (0, width - 1)); seen = set()
    def near(c): return any(sum((c[i] - sample[i]) ** 2 for i in range(3)) <= 32 ** 2 for sample in samples)
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen: continue
        seen.add((x, y))
        if not near(pixels[x, y]): continue
        pixels[x, y] = BG
        if x: queue.append((x - 1, y))
        if x + 1 < width: queue.append((x + 1, y))
        if y: queue.append((x, y - 1))
        if y + 1 < height: queue.append((x, y + 1))
    return image

ARCHIVE.mkdir(parents=True, exist_ok=True)
for unit in ALL_CARDS:
    card = OUT / f"#{unit}.tga"
    if unit == "ind_bhutan_warrior" and not card.exists(): shutil.copy2(ROOT / "data/ui/units/mercs/#merc_bhutan_warrior.tga", card)
    if not card.exists(): raise FileNotFoundError(card)
    if not (ARCHIVE / card.name).exists(): shutil.copy2(card, ARCHIVE / card.name)
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
for unit, spec in GENERATED.items():
    source = ROOT / "tools/historical_card_refs" / spec["source_file"]; master = ROOT / "tools/card_generation_sources" / spec["master"]
    if not source.exists() or not master.exists(): raise FileNotFoundError(f"Missing source for {unit}: {source} / {master}")
    registry = [item for item in registry if item.get("id") != unit]
    registry.append({"id": unit, "group_id": "indian_princely_balance_20260917", "unit_type": unit, "card_file": f"data/ui/units/bulga/#{unit}.tga", "faction": "bulga", "name": unit, "role": spec["role"], "weapon": spec["weapon"], "source_url": spec["url"], "source_file": f"tools/historical_card_refs/{spec['source_file']}", "source_title": spec["source_title"], "creator": spec["creator"], "source_date": spec["date"], "licence": "Public domain / no known copyright restrictions", "depicted_subject": spec["subject"], "mapping_note": "Historical source controls pose, anatomy and mounted relationship; the loaded in-game mesh controls regional clothing, equipment and visible weapon. Audited at source size and 48x64.", "pose_source_id": spec["pose"], "status": "card-approved", "generated_file": f"tools/card_generation_sources/{spec['master']}", "crop_box": [0, 0, 1536, 2048]})
REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for unit in ALL_CARDS:
    card = OUT / f"#{unit}.tga"
    if unit in GENERATED: image = flatten_generated(Image.open(ROOT / "tools/card_generation_sources" / GENERATED[unit]["master"]))
    elif unit == "ind_bhutan_warrior": image = normalize_legacy(Image.open(ROOT / "data/ui/units/mercs/#merc_bhutan_warrior.tga"))
    else: image = normalize_legacy(Image.open(ARCHIVE / card.name))
    image = image.resize((48, 64), Image.Resampling.LANCZOS).convert("RGBA"); pixels = image.load()
    for corner in ((0, 0), (47, 0), (0, 63), (47, 63)): pixels[corner] = BG
    image.save(long_path(card), format="TGA"); raw = long_path(card).read_bytes()
    assert struct.unpack_from("<HH", raw, 12) == (48, 64) and raw[16] == 32
(ARCHIVE / "original_members.json").write_text(json.dumps({"archived_from": "data/ui/units/bulga", "members": ALL_CARDS, "generated_replacements": list(GENERATED)}, indent=2) + "\n", encoding="utf-8")
print("Installed Indian Princely States tactical cards and preserved all original members.")
