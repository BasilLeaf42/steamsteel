from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGNS = [
    ROOT / "data/world/maps/campaign/camp_steamsteel/descr_strat.txt",
    ROOT / "data/world/maps/campaign/imperial_campaign/descr_strat.txt",
]

# Legacy start-army aliases left behind by faction roster conversions.  These
# are faction-scoped so similarly named donor records elsewhere are untouched.
MAP = {
    "scotland": {"us_scout_cav": "mex_carbineers_early"},
    "teu": {"us_farmers": "boer_kommando_early"},
    "normans": {"rus_imp_cav_no": "swe_general_staff", "rus_sib_cossacks_no": "swe_lifeguard_horse", "swe_guard": "swe_jagare_early", "swed_inf2": "swe_line_early", "swed_roy": "nor_line_early"},
    "hre": {"balk_cav_gr": "pru_general_staff", "gr_lancer": "pru_husaren", "otto_sipahi": "pru_general_staff", "siam_riflemen_gr": "pru_fusiliere_early"},
    "denmark": {"bol_hussar": "per_husares_junin", "peru_early_inf": "per_line_early", "peru_hussars": "per_general_staff", "tzar_inf": "per_guard_mid"},
    "france": {"fra_blacks_fr": "fra_senegalais_early", "fra_carbs": "fra_chasseurs_cheval", "fra_chass": "fra_chasseurs_mid", "fra_hus_2": "fra_cuirassiers", "fra_hussar": "fra_general_staff", "fra_inf_fr": "fra_legion_mid", "fra_line_inf": "fra_fusiliers_early", "fra_rec": "fra_garde_mobile_early", "us_zouave": "fra_zouaves_early"},
    "hungary": {"aus_lancers": "aus_ulanen", "aus_ulhans": "aus_general_staff", "balk_cav": "aus_husaren", "dan_dragoon_early": "aus_dragoner_early", "dutch_militia": "aus_line_early", "kaiserjager": "aus_grenz_early", "rom_guard": "aus_bosniak_mid"},
    "venice": {"it_pistoleer": "ita_general_staff", "rus_cos_guard_ve": "ita_line_early"},
    "spain": {"fra_hus_2": "spa_cuirassiers_early"},
    "papal_states": {"sho_mod_cav": "aby_grd_2g"},
    "russia": {"rus_conscript": "rus_siberian_early", "rus_conscript_ru": "rus_pekhota_early", "rus_cos_guard_ru": "rus_leib_guard_early", "rus_imp_cav": "rus_general_staff", "rus_roy_cav_ru": "rus_draguny_early", "rus_roy_inf_ru": "rus_strelki_early", "russ_inf": "rus_sapery_mid"},
    "timurids": {"ind_armstrong": "col_12lb"},
    "turks": {"arab_brigade": "ott_mustahfiz_early", "arab_sailors": "ott_nizamiye_early", "moroccan_camel_gunner": "ott_suvari_early", "moroccan_gunner": "ott_redif_early", "otto_cav_tu": "ott_suvari_mid", "turk_lt": "ott_ertugrul_suvari"},
    "egypt": {"ind_armstrong": "col_12lb"},
    "golden": {"moroccan_camel_gunner": "oma_bedouin_camelry", "moroccan_gunner": "oma_baluchi_musketeers", "omani_roy": "oma_palace_guard_early", "otto_cav": "oma_horse_guard_early", "us_zouave_go": "oma_regular_early"},
    "portugal": {"balk_cav_nl": "net_general_staff", "dutch_askari2": "net_knil_early", "dutch_inf": "net_line_early", "nl_carbs": "net_huzaren", "nl_roy": "net_grenadiers_early"},
    "sicily": {"fra_hussar": "dan_general"},
    "byzantium": {"mongol_inf": "qing_village_braves", "mongols_archer": "qing_green_banner_archers"},
    "milan": {"berdan_inf": "csa_sharpshooters"},
    "mongols": {"fra_hussar": "gre_general_staff", "greek_early_inf": "gre_line_early", "greek_guard_cav": "gre_carbineers_mid"},
    "cru": {"byz_armstrong": "siam_armstrong"},
    "slave": {"eng_12lb": "col_12lb"},
}

FACTION_RE = re.compile(r"(?m)^faction\s+([a-z_]+)\b")
UNIT_RE = re.compile(r"(?m)^(\s*unit\s+)(\S+)(\s+exp\s+)")

for path in CAMPAIGNS:
    text = path.read_text(encoding="utf-8")
    matches = list(FACTION_RE.finditer(text))
    out, cursor, changed = [], 0, [0]
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out.append(text[cursor:start])
        block = text[start:end]
        mapping = MAP.get(match.group(1), {})
        def replace_unit(unit_match):
            old = unit_match.group(2)
            new = mapping.get(old)
            if not new:
                return unit_match.group(0)
            changed[0] += 1
            return unit_match.group(1) + new + unit_match.group(3)
        out.append(UNIT_RE.sub(replace_unit, block))
        cursor = end
    out.append(text[cursor:])
    path.write_text("".join(out), encoding="utf-8", newline="\r\n")
    print(f"{path.relative_to(ROOT)}: replaced {changed[0]} obsolete starting units")
