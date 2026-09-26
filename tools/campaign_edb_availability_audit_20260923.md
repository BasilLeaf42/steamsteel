# Campaign EDB availability audit (2026-09-23)

Authoritative file: `data/tow_steamsteel/export_descr_buildings.txt`  
Runtime mirror exact: **true**  
Recruitment entries: **4908** across **556** EDU types.

## System reconstructed

Each `recruit_pool` is attached to a building level. Its four numeric fields are initial pool, replenishment rate per turn, maximum pool, and starting experience. The trailing `requires` expression independently gates faction, resources/regions, buildings and event counters. Multiple matching rows stack; a “resupply” row is not merely metadata and can itself make a unit recruitable. EDU ownership and era lists do not create campaign recruitment.

## Global findings

- EDB unit names absent from EDU: **0**.
- EDB faction scopes not repeated in EDU ownership/eras: **1023**. This is a cross-scope difference, not automatically an error: many campaign-only units deliberately have EDU ownership `slave`.
- Period-suffixed rows missing their standard 1870/1890 gate: **493**.
- Exact duplicate row groups: **0**.
- Unit/building/level/faction combinations with multiple pool rows: **2035**. Multiple geography rows can be intentional; exact duplicates are not.
- Rows with no faction restriction: **0**.
- EDU units with no campaign EDB row (excluding no_custom): **489**. This includes hidden, obsolete, mercenary, naval and custom-battle-only records and requires roster classification before correction.

The barracks roster is repeated at all four barracks tiers. Home/colonial availability normally uses a faction gate plus a `hidden_resource`; a second low-cap “resupply” row is commonly added without geography. Because it remains a normal `recruit_pool`, it enables recruitment wherever its building exists. Of 1,462 resupply rows, only 4 retain a hidden-resource restriction. Of the 575 deficient standard period gates, 335 are resupply rows.

Two incompatible time schemes coexist: 1,765 rows use the standardized 1870/1890 counters, 680 use legacy `military_reforms_1`/`military_reforms_2`, and 1,851 use neither. The campaign script currently fires 1870 after turn 1, 1890 after turn 3, legacy reform 1 after turn 2, and legacy reform 2 after turn 4 (`[TESTING]` values), so even correctly gated eras collapse almost immediately.

## Converted-faction summary

| Faction | Code | Units | Rows | Bad gates | Ownership mismatches | Multi-pool groups |
|---|---:|---:|---:|---:|---:|---:|
| Union | portugala | 26 | 207 | 89 | 0 | 87 |
| Confederates | milan | 20 | 166 | 82 | 0 | 67 |
| Mexico | scotland | 18 | 142 | 50 | 0 | 55 |
| Peru | denmark | 23 | 169 | 8 | 0 | 73 |
| Brazil | poland | 33 | 233 | 15 | 55 | 96 |
| Argentina | aztecs | 28 | 210 | 58 | 35 | 83 |
| Britain | england | 45 | 307 | 0 | 2 | 132 |
| France | france | 26 | 169 | 48 | 2 | 70 |
| Prussia | hre | 28 | 188 | 51 | 0 | 78 |
| Spain | spain | 20 | 137 | 21 | 7 | 59 |
| Netherlands | portugal | 17 | 114 | 0 | 67 | 48 |
| Denmark | sicily | 13 | 86 | 14 | 0 | 36 |
| Sweden-Norway | normans | 16 | 128 | 0 | 70 | 46 |
| Greece | mongols | 18 | 119 | 0 | 78 | 49 |
| Italy | venice | 17 | 116 | 0 | 61 | 50 |
| Russia | russia | 22 | 150 | 0 | 94 | 66 |
| Austria-Hungary | hungary | 21 | 165 | 0 | 107 | 63 |
| Morocco | moors | 26 | 180 | 6 | 12 | 80 |
| Boers | teu | 18 | 143 | 40 | 8 | 61 |
| Zulu | lith | 10 | 71 | 0 | 38 | 33 |
| Ottoman | turks | 18 | 127 | 0 | 86 | 55 |
| Oman | golden | 14 | 97 | 0 | 8 | 41 |
| Qajar | egypt | 20 | 139 | 0 | 48 | 59 |
| Afghanistan | timurids | 20 | 137 | 0 | 48 | 59 |
| Turkestan | cuman | 17 | 121 | 0 | 50 | 55 |
| Indian Princely States | bulga | 18 | 119 | 0 | 12 | 49 |
| Siam | cru | 15 | 105 | 0 | 0 | 47 |
| Qing | byzantium | 36 | 264 | 7 | 31 | 120 |
| Ethiopia | papal_states | 5 | 33 | 0 | 20 | 13 |
| Japan | saxons | 52 | 359 | 0 | 0 | 151 |

## Highest-priority examples

- Ownership mismatch: line 759, `uk_knights` gated to `poland`, EDU ownership `slave`.
- Ownership mismatch: line 760, `fra_cav_poland` gated to `poland`, EDU ownership `slave`.
- Ownership mismatch: line 761, `fra_pith_poland` gated to `poland`, EDU ownership `slave`.
- Ownership mismatch: line 762, `merc_uru_inf` gated to `poland`, EDU ownership `slave`.
- Ownership mismatch: line 763, `bra_foot` gated to `poland`, EDU ownership `slave`.
- Ownership mismatch: line 764, `boer_guard_po` gated to `poland`, EDU ownership `slave`.
- Ownership mismatch: line 765, `fra_guard_po` gated to `poland`, EDU ownership `slave`.
- Ownership mismatch: line 766, `fra_inf` gated to `poland`, EDU ownership `slave`.
- Ownership mismatch: line 767, `peru_foot_aztecs` gated to `aztecs`, EDU ownership `slave`.
- Ownership mismatch: line 768, `peru_foot_aztecs` gated to `aztecs`, EDU ownership `slave`.
- Ownership mismatch: line 791, `l_pith_cav_aztecs` gated to `aztecs`, EDU ownership `slave`.
- Ownership mismatch: line 792, `fra_ww1_inf_aztecs` gated to `aztecs`, EDU ownership `slave`.
- Ownership mismatch: line 793, `merc_uru_inf` gated to `aztecs`, EDU ownership `slave`.
- Ownership mismatch: line 875, `merc_fra_blacks` gated to `spain`, EDU ownership `england, venice, france, hre, slave`.
- Ownership mismatch: line 877, `l_pith_cav_portugal` gated to `portugal`, EDU ownership `slave`.
- Ownership mismatch: line 878, `dutch_pith` gated to `portugal`, EDU ownership `slave`.
- Ownership mismatch: line 879, `nl_roy` gated to `portugal`, EDU ownership `slave`.
- Ownership mismatch: line 880, `dutch_ww1` gated to `portugal`, EDU ownership `slave`.
- Ownership mismatch: line 881, `dutch_askari` gated to `portugal`, EDU ownership `slave`.
- Ownership mismatch: line 882, `dutch_askari2` gated to `portugal`, EDU ownership `slave`.
- Period gate: line 650, `uni_state_volunteers_early`, missing -military_reforms_1870.
- Period gate: line 651, `uni_state_volunteers_early`, missing -military_reforms_1870.
- Period gate: line 652, `uni_national_guard_mid`, missing +military_reforms_1870.
- Period gate: line 653, `uni_national_guard_mid`, missing +military_reforms_1870.
- Period gate: line 663, `uni_state_volunteers_early`, missing -military_reforms_1870.
- Period gate: line 664, `uni_regulars_mid`, missing +military_reforms_1870, -military_reforms_1890.
- Period gate: line 665, `uni_regulars_high`, missing +military_reforms_1890.
- Period gate: line 666, `uni_national_guard_mid`, missing +military_reforms_1870.
- Period gate: line 672, `uni_dragoons_early`, missing -military_reforms_1870.
- Period gate: line 673, `uni_dragoons_mid`, missing +military_reforms_1870, -military_reforms_1890.
- Period gate: line 674, `uni_dragoons_high`, missing +military_reforms_1890.
- Period gate: line 679, `csa_state_volunteers_early`, missing -military_reforms_1870.
- Period gate: line 680, `csa_state_volunteers_early`, missing -military_reforms_1870.
- Period gate: line 681, `csa_state_guard_mid`, missing +military_reforms_1870, -military_reforms_1890.
- Period gate: line 682, `csa_state_guard_mid`, missing +military_reforms_1870, -military_reforms_1890.
- Period gate: line 683, `csa_state_guard_high`, missing +military_reforms_1890.
- Period gate: line 684, `csa_state_guard_high`, missing +military_reforms_1890.
- Period gate: line 686, `csa_state_cavalry_early`, missing -military_reforms_1870.
- Period gate: line 687, `csa_state_cavalry_mid`, missing +military_reforms_1870.
- Period gate: line 691, `csa_state_volunteers_early`, missing -military_reforms_1870.
- Period gate: line 692, `csa_state_guard_mid`, missing +military_reforms_1870, -military_reforms_1890.
- Period gate: line 693, `csa_state_guard_high`, missing +military_reforms_1890.
- Period gate: line 694, `csa_regulars_early`, missing -military_reforms_1870.
- Period gate: line 695, `csa_regulars_mid`, missing +military_reforms_1870, -military_reforms_1890.
- Period gate: line 696, `csa_regulars_high`, missing +military_reforms_1890.
- Period gate: line 699, `csa_state_cavalry_early`, missing -military_reforms_1870.
- Period gate: line 700, `csa_state_cavalry_mid`, missing +military_reforms_1870.
- Period gate: line 704, `mex_carbineers_early`, missing -military_reforms_1870.
- Period gate: line 705, `mex_carbineers_mid`, missing +military_reforms_1870, -military_reforms_1890.
- Period gate: line 707, `mex_state_guard_mid`, missing +military_reforms_1870, -military_reforms_1890.

Full row-level evidence is in `tools/campaign_edb_availability_audit_20260923.json`; the flat recruitment matrix is `tools/campaign_edb_recruitment_matrix_20260923.csv`.
