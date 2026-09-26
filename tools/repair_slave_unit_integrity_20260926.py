from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EDU = DATA / "tow_steamsteel/export_descr_unit.txt"
EDU_MIRROR = DATA / "export_descr_unit.txt"
MODELDB = DATA / "unit_models/battle_models.modeldb"
REBEL_DB = DATA / "descr_rebel_factions.txt"
CAMPAIGNS = [
    DATA / "world/maps/campaign/camp_steamsteel/descr_strat.txt",
    DATA / "world/maps/campaign/imperial_campaign/descr_strat.txt",
]
BACKUP = ROOT / "tools/backup_before_slave_integrity_repair_20260926"
BACKUP.mkdir(parents=True, exist_ok=True)

for path in [EDU, EDU_MIRROR, MODELDB, REBEL_DB, *CAMPAIGNS]:
    target = BACKUP / str(path.relative_to(ROOT)).replace("/", "__").replace("\\", "__")
    if not target.exists():
        shutil.copy2(path, target)


def unit_blocks(text):
    return list(re.finditer(r"(?ms)^type\s+(.+?)\s*$.*?(?=^type\s+|\Z)", text))


ownership_units = {
    "merc_aceh_marines", "merc_aceh_noble", "merc_aceh_reg",
    "merc_aceh_gold", "merc_aceh_warband", "merc_aceh_inf",
    "cog", "dhow", "dragon boat", "grande carrack", "pirate ship",
    "ship_sail_corvette", "ship_sail_sotl", "ship_steam_corvette", "turtle ship",
}

edu = EDU.read_text(encoding="utf-8", errors="strict").replace("\r\n", "\n")
changed = 0
for match in reversed(unit_blocks(edu)):
    unit = match.group(1).strip()
    if unit not in ownership_units:
        continue
    block = match.group(0)
    own = re.search(r"(?m)^ownership[ \t]+([^\r\n]+?)[ \t]*$", block)
    if not own:
        raise RuntimeError(f"Missing ownership row: {unit}")
    factions = [x.strip() for x in own.group(1).split(",") if x.strip()]
    if "slave" not in factions:
        factions.append("slave")
        replacement = "ownership        " + ", ".join(factions)
        block = block[:own.start()] + replacement + block[own.end():]
        edu = edu[:match.start()] + block + edu[match.end():]
        changed += 1
if changed != 15:
    raise RuntimeError(f"Expected 15 EDU ownership repairs, got {changed}")
EDU.write_text(edu.replace("\n", "\r\n"), encoding="utf-8", newline="")
shutil.copy2(EDU, EDU_MIRROR)


replacements = {
    "mex_bers": "mex_cazadores_early",
    "mex_foot": "mex_provincial_levies",
    "qing_vets": "qing_green_banner_gunmen",
    "qing_archers": "qing_green_banner_archers",
    "qing_swords": "qing_village_braves",
    "german_asia": "merc_aceh_reg",
    "us_militia_te": "boer_kommando_early",
    "us_farmer_cav": "merc_us_farmer_cav",
}
rebel = REBEL_DB.read_text(encoding="utf-8", errors="strict")
for old, new in replacements.items():
    pattern = rf"(?m)^(\s*unit\s+){re.escape(old)}(\s*)$"
    rebel, count = re.subn(pattern, rf"\g<1>{new}\g<2>", rebel)
    if count == 0:
        raise RuntimeError(f"Obsolete rebel unit not found: {old}")
REBEL_DB.write_text(rebel, encoding="utf-8", newline="")

for path in CAMPAIGNS:
    text = path.read_text(encoding="utf-8", errors="strict")
    text, infantry_count = re.subn(r"(?m)^(\s*unit\s+)us_militia_te(\s+exp\b)", r"\1boer_kommando_early\2", text)
    text, cavalry_count = re.subn(r"(?m)^(\s*unit\s+)us_farmer_cav(\s+exp\b)", r"\1boer_mounted_kommando_early\2", text)
    if infantry_count != 2 or cavalry_count != 1:
        raise RuntimeError(f"Unexpected Boer replacements in {path}: {infantry_count}/{cavalry_count}")
    path.write_text(text, encoding="utf-8", newline="")


model_sources = {
    "arg_standard_bearer": "aztecs",
    "boer_standard_bearer": "teu",
    "bra_general_staff": "poland",
    "csa_standard_bearer": "milan",
    "fra_carabiniers_high": "france",
    "fra_cav": "france",
    "gre_carbineers_high": "mongols",
    "gre_carbineers_mid": "mongols",
    "korean_archers": "merc",
    "mex_standard_bearer": "scotland",
    "mor_standard_bearer": "moors",
    "oma_standard_bearer": "golden",
    "ott_standard_bearer": "turks",
    "per_standard_bearer": "denmark",
    "ssk_qing_soe_beiyang_new_army_ss": "byzantium",
}


def clone_slave_mapping(block, model, source):
    lines = block.splitlines()
    if any(re.fullmatch(r"5 slave\s*", line) for line in lines):
        return block
    lod_count = int(lines[1].split()[1])
    texture_count_index = 2 + lod_count
    texture_count = int(lines[texture_count_index].strip())
    texture_start = texture_count_index + 1
    texture_groups = [lines[texture_start + i * 4:texture_start + (i + 1) * 4] for i in range(texture_count)]
    source_texture = next((g for g in texture_groups if g and g[0].split(maxsplit=1)[-1].strip() == source), None)
    if source_texture is None:
        raise RuntimeError(f"{model}: missing texture source faction {source}")
    slave_texture = ["5 slave", *source_texture[1:]]
    insert_at = texture_start + texture_count * 4
    lines[texture_count_index] = str(texture_count + 1)
    lines[insert_at:insert_at] = slave_texture

    attachment_count_index = insert_at + 4
    attachment_count = int(lines[attachment_count_index].strip())
    attachment_start = attachment_count_index + 1
    if attachment_count:
        groups = [lines[attachment_start + i * 3:attachment_start + (i + 1) * 3] for i in range(attachment_count)]
        source_attachment = next((g for g in groups if g and g[0].split(maxsplit=1)[-1].strip() == source), None)
        if source_attachment is None:
            raise RuntimeError(f"{model}: missing attachment source faction {source}")
        lines[attachment_count_index] = str(attachment_count + 1)
        lines[attachment_start + attachment_count * 3:attachment_start + attachment_count * 3] = ["5 slave", *source_attachment[1:]]
    return "\n".join(lines) + ("\n" if block.endswith("\n") else "")


model = MODELDB.read_text(encoding="utf-8", errors="strict").replace("\r\n", "\n")
heads = [m for m in re.finditer(r"(?m)^(\d+) (\S+)\s*\n\d+ \d+\s*$", model) if int(m.group(1)) == len(m.group(2))]
spans = {}
for i, head in enumerate(heads):
    spans[head.group(2).lower()] = (head.start(), heads[i + 1].start() if i + 1 < len(heads) else len(model), head.group(2))
for requested, source in model_sources.items():
    start, end, actual = spans[requested.lower()]
    block = model[start:end]
    replacement = clone_slave_mapping(block, actual, source)
    model = model[:start] + replacement + model[end:]
    delta = len(replacement) - (end - start)
    if delta:
        for key, (s, e, name) in list(spans.items()):
            if s > start:
                spans[key] = (s + delta, e + delta, name)
        spans[requested.lower()] = (start, start + len(replacement), actual)
MODELDB.write_text(model.replace("\n", "\r\n"), encoding="utf-8", newline="")

print(f"Repaired {changed} ownership rows, 8 obsolete rebel unit names, 3 starting Boer placements, and {len(model_sources)} model mappings.")
