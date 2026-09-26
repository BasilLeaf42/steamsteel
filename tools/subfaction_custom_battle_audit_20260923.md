# Custom-battle subfaction audit

Definition: a subfaction is a coherent mercenary roster that can be played from
its mother faction's custom-battle panel in every period. It supplies its own
foot roster and any characteristic cavalry, while borrowing the mother roster's
general and artillery. Every subfaction unit must retain `mercenary_unit`.

| Subfaction | Mother roster | Agreed balance | Early foot/cavalry | Mid foot/cavalry | Late foot/cavalry | Result |
|---|---|---|---:|---:|---:|---|
| Portugal | Spain | C tier, no bonus | 5 missile / 1 cavalry | 5 missile / 1 cavalry | 5 missile / 1 cavalry | Pass |
| Aceh | Netherlands | Weak regional subfaction; one of each distinct unit | 2 missile + 2 melee / 0 | 4 missile + 2 melee / 0 | 4 missile + 2 melee / 0 | Pass |
| Taiping | Qing | D tier, no cost reduction; intentionally early-only | 3 missile + 6 melee / 0 | none | none | Pass (early-only by design) |
| Tibet | Qing | Qing D-tier rules, no cost reduction | 4 missile + 5 melee / 3 cavalry | 4 missile + 5 melee / 2 cavalry | 4 missile + 5 melee / 2 cavalry | Pass |
| Korea | Qing and Japan | Qing D-tier rules, no cost reduction | 3 missile + 1 melee / 1 cavalry | 3 missile + 1 melee / 1 cavalry | 3 missile / 1 cavalry | Pass |
| Mahdist/Sudanese | Ethiopia | D tier with Zulu morale/melee bonus; Mahdists mid/late only | 3 Sudanese melee / 0 cavalry | 2 missile + 6 melee / 2 cavalry | 2 missile + 6 melee / 2 cavalry | Pass |
| Ainu/Japanese irregulars | Japan | D-tier rules | 4 missile + 4 melee / 0 | 4 missile + 4 melee / 0 | 4 missile + 3 melee / 0 | Pass |

Portugal has one genuine infantry and one genuine cavalry lineage with distinct
early, mid, and late equipment records. The deleted `merc_port_inf` and
`merc_port_lancer` records were exact compatibility duplicates of the early
records. Rebel templates now reference the surviving early records.

Spain, the Netherlands, Qing, Japan, and Ethiopia each provide at least one
general and one artillery record in all three periods, so every listed mother
roster can supply the deliberately borrowed command and artillery arms.

Aceh deliberately remains smaller than a national roster: every distinct unit
has availability one. Taiping is intentionally an early-only subfaction and does
not require mid/late exposure. Maori and Zulu-themed mercenaries remain standard
auxiliaries rather than subfactions because each has only two records and does
not form a standalone roster.
