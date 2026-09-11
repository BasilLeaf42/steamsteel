# Universal Info

## Cautions
The existing systems are a patchwork, consider potential conflicts when making programmatic changes.
Be sparing with tokens and output; excessive context and verbosity can degrade instruction compliance.

## Faction conversion

Union: portugala
Confederates: milan
Mexico: scotland
Peru: denmark
Brazil: poland
Argentina: aztecs
Britain: england
France: france
Prussia: hre
Spain: spain
Netherlands: portugal
Denmark: sicily
Swe-Nor: normans
Greece: mongols
Italy: venice
Russia: russia
Aus-Hun: hungary
Morocco: moors
Boers: teu
Zulu: lith
Ottoman: turks
Oman: golden
Qajar: egypt
Afganistan: timurids
Turkestan: cuman
Indian Princely States: bulga
Siam: cru
Qing: byzantium
Ethiopia: papal_states
Meiji: saxons

## Logging
"Medieval II Total War\system.log.txt"

# Units

## Relevant files
"steamsteel\data\tow_steamsteel\export_descr_unit.txt" - edu, main unit database
"steamsteel\data\tow_steamsteel\export_descr_buildings.txt" - edb, main building database
"steamsteel\data\text\export_units.txt" - name translations
"steamsteel\data\unit_models\battle_models.modeldb" - unit model database
"steamsteel\data\ui\units" - unit gameplay cards
"steamsteel\data\ui\unit_info" - detailed description cards

### Unit cards

Create tactical unit cards as part of balancing each faction, not as a later cleanup. Every internal unit type must have its own correctly named physical card and its own distinct documented historical unit-reference image, including period variants. The only permitted source reuse is an approved kneeling-pose reference from the shared skirmisher pose pool described below.

Before generating or replacing any card, preserve every distinct pre-existing card in the source archive and record its original members. Assign preserved art to the most appropriate unit whose loaded model and visible equipment it genuinely matches; do not discard a valid low-resolution card merely because a new composition exists. If a pre-existing card fails the visual or model-signature audit and cannot be assigned honestly, retain it in the archive as a superseded reference rather than forcing it onto an unsuitable unit or overwriting its only copy.

`data/ui/units/<faction>/#<unit>.tga` is the same 48x64 source card used in battle, in a selected campaign army, and for recruitment. Steam & Steel's custom battle UI provides a 48x80 card background, but the lower 16 pixels belong to the normal or selected `BATTLE_CARD_BACKGROUND` sprite rather than the unit-card texture. Keep tactical cards at 48x64. Replace the complete 48x80 normal and selected battle-card background sprites with the same canonical background used by the cards so no old colour, transparency, or edge treatment remains and the combined battle display appears full-height. Apply this one-time UI-atlas correction consistently to every culture rather than extending or vertically stretching every unit card.

Preserve 32-bit RGBA and alpha. Reuse the established current card style, using the canonical parchment background colour `#B8AD8F` rather than retaining inconsistent donor background colours. Give each period variant its own historically grounded composition even when its in-game model is unchanged. `data/ui/unit_info` contains the separate large information portrait and need not be regenerated unless requested.

Crop approved source artwork to the tactical card's 3:4 aspect ratio before reducing it to 48x64; never change the aspect ratio by stretching. For tall portrait outputs, preserve the head and torso and remove excess lower-body space first. Record a unit-specific crop box in the source register when the automatic top-weighted crop does not produce the close original-card framing.

The card must depict the unit actually loaded by the EDU: trace its `soldier` entry through modeldb and verify the mesh, faction texture, attachments, mount, and visible weapons. A donor card is valid only when its modeldb visual signature matches those assets; similarity of unit names, role, nation, or era is not enough. If no exact visual donor exists, retain or create a card from the actual model rather than substituting a convenient approximate unit.

Base every newly created unit-card composition on a documented period photograph, contemporary engraving, or historically reliable uniform plate for the same unit or the closest defensible national, period, and battlefield-role match. The historical image controls pose, anatomy, hand placement, mount posture, and weapon interaction; the traced in-game model controls the final uniform, equipment, and visible weapon. Record the source URL, attribution, date, licence, depicted subject, and any approximation in the card-source register. Do not install a historically styled card whose source or mapping has not been recorded.

Treat the historical source as a compositional constraint, not a mood reference: preserve its limb arrangement, weight distribution, grip, mount relationship, and weapon orientation unless a documented equipment difference requires a small change. Reject a result that invents a substantially different pose or mechanical action. Before installation, mark the source mapping approved in `tools/historical_card_sources.json`; the card installer must fail closed while any internal unit has an incomplete, missing, reused, or unapproved unit-reference record.

Kneeling skirmisher photographs or plates need not exist for every uniform. Maintain a small, separately documented pool of mechanically correct period kneeling rifle poses in `tools/historical_skirmisher_pose_sources.json`. A skirmisher or sharpshooter may reuse one approved pool pose for anatomy, weight distribution, hand placement, and weapon orientation while retaining its own distinct national, period, and unit-specific historical reference for uniform and equipment. Record the pool ID as `pose_source_id` in the unit register. Do not use the pool for line infantry, cavalry, artillery, or generals, and do not use an unapproved, anachronistic, mirrored, or mechanically implausible pose merely to satisfy the kneeling rule.

When a pool pose has an approved generated master, create further cards as localized uniform/equipment retextures of that master. Preserve the master silhouette, limbs, hands, grip, shoulder contact, and rifle geometry pixel-for-pixel wherever the assigned weapon permits; do not regenerate the whole figure. A materially different weapon action requires another historically sourced and approved pose master rather than forcing a new mechanism or grip into an incompatible composition.

Visually audit every created or generated card individually at both source size and the final 48x64 reduction. Reject duplicated or disconnected limbs, malformed hands or faces, implausible grips, awkward joint cuts, incorrect foot or mounted status, distorted weapon length, missing role-defining equipment, inappropriate general poses or props, mismatched uniforms, and compositions that become unreadable at tactical size; do not rely on a spot check or generation success alone.

Use a reloading pose only when both hands are correctly placed for the depicted weapon and action. Reject mirrored, inverted, or mechanically impossible support/action-hand positions; prefer a natural ready, observing, or aiming pose when the reload cannot be represented reliably.

Do not accept a generated firearm merely because the overall silhouette reads as a rifle. Verify the complete stock, barrel, muzzle, lock or bolt, trigger guard, and every point where a hand contacts the weapon; reject inverted actions, modern or anachronistic grips, broken or duplicated mechanisms, and stocks or barrels merged into hands. Prefer an actual model render or a verified exact visual donor over generative redrawing whenever firearm geometry or a two-handed grip must be shown.

Pose and weapon presentation must also communicate battlefield role. Frame tactical cards at the close torso-level scale used by the original cards; the head, torso, arms, and identifying weapon should fill most of the 48x64 image rather than shrinking a complete figure into the card. Judge the crop for overall naturalness rather than forcing every limb or carried weapon into view: arms, long rifles, lances, and secondary weapons may extend naturally beyond the edge, but avoid awkward joint cuts, distorted anatomy, or shortening a weapon merely to fit it. Only role-defining equipment must be clearly readable; do not force every sidearm or secondary weapon into the same composition. Vary poses between units instead of repeating one template: aiming, ready, observing, bracing, and reloading are all acceptable where appropriate. Infantry skirmishers and sharpshooters are shown kneeling, with enough of the raised knee or crouched body line visible to make the posture clear. General-and-staff cards always show the mount clearly, at least the horse's head or neck and tack, so the unit reads as mounted. The general uses a passive command posture with no weapon held in either hand and visible command paraphernalia such as binoculars, a folded map, dispatch, or map case, varied naturally between factions; hands may otherwise rest on reins, while sidearms remain sheathed or holstered. Carbine-armed cavalry are shown visibly holding or carrying a carbine; a pistol-, lance-, or sabre-only portrait is not acceptable for them. Mounted cards normally show the rider at torso scale together with the horse's head or neck, not the entire horse.

Note that the tow_steamsteel files are copied and overwrite the main directory ones!

## Balancing/Periodization:

1. Reloading animations must be set in "attributes" in conjunction with the entry of the "soldier" in the modeldb, specifically the primary weapon (first entry)*
For Infantry, they are:
Muzzle-loading - gunpowder_unit + 20 MTW2_Fast_Arquebus_3
Rifle/single-shot breechloader (line infantry) - NO gunpowder_unit + 14 MTW2_Musket_SS
Rifle/single-shot breechloader (skirmisher or sharpshooter) - NO gunpowder_unit + 15 MTW2_Musket_SSK.
Magazine Rifle (line infantry) - NO gunpowder_unit + 20 MTW2_Fast_Arquebus_3 (reloading animation is thus disabled)
Magazine Rifle (skirmisher or sharpshooter) - NO gunpowder_unit + 15 MTW2_Musket_SSK. Use the dedicated kneeling set even though its reload timing does not represent a magazine rifle exactly, because its posture is the appropriate skirmisher presentation.

Choose the animation from both weapon action and battlefield role, not era alone. Every non-muzzle-loading skirmisher or sharpshooter uses `MTW2_Musket_SSK`, including late magazine-rifle units. A skirmisher model must have a distinct soldier/modeldb entry whenever a shared line-infantry or different-period record requires another animation. Do not infer correctness from an existing late unit: the surviving Boer sharpshooter uses the generic set, while `moroccan_gunner1` is the verified `MTW2_Musket_SSK` precedent.

All modern line infantry should use 17 MTW2_Pike_primary for bayonets.

Cavalry: as the custom MTW2_Musket_SS breechloading animation cannot be used for them, their logic is much simpler
Muzzle-loading: gunpowder_unit
Breech-loading: NO gunpowder_unit

Changing a cavalry skeleton or EDU weapon does not create the visible weapon: pistol, carbine, lance, and sabre geometry is embedded in the rider mesh. Lancers must use a verified period-appropriate lance mesh with the lance group marked `primaryactive0` and the sabre marked `secondaryactive0`; use a Western/European lance donor for European units and never substitute an Asian bamboo lance. Copy the complete donor modeldb structure and compatible texture mappings with correct string-length checksums.

Artillery animations are set by the engine, just make sure the correct one is assigned.

2. Formations for infantry depend on unit type and period

Regular infantry (Muzzle-loading/early breechloaders/era 0):		1.2, 1.2, 1.2, 1.2, 3, square
Regular infantry (Rifle/era 1):			1.2, 1.2, 2.0, 2.4, 3, square
Regular infantry (Magazine Rifle/era 2): 		1.2, 1.4, 2.4, 2.8, 3, square
Skirmishers (all gunpowder): 				1.4, 1.8, 2.8, 3.6, 3, square
Cavalry:					2, 2, 4, 4, 3, square

3. Morale

EDU syntax is `stat_mental morale, discipline, training`. Valid discipline tokens are `low`, `normal`, `disciplined`, and `impetuous`; `high` is not a valid EDU token. Valid training tokens are `untrained`, `trained`, and `highly_trained`.

Militia: morale 2-5 (default row: `3, low, trained`)
Regular: morale 3-6 (default row: `4, normal, trained`)
Elite: morale 5-8 (default row: `6, disciplined, highly_trained`)

Note that non-line/western units may have `impetuous` discipline.

4. Projectile row:

In short, era 0 is for rifled_muskets/early breechloaders, era 1 is for rifles, and era 2 is for magazine rifles. However obselecence is entirely possible.

Date-gate weapon conversions by their conversion year. A conversion dated after 1862 must not appear in the early/1860s slot; move it to the mid period or later unless the user explicitly sets a different cutoff.

Projectiles: The tiering system uses the designations c, b, a, and s to represent ascending accuracy. Base quality is Militia = c, Regular = b, Elite = a. Apply role modifiers separately: Skirmisher = +1 tier; Sharpshooter = +2 tiers. Skirmishers are not automatically sharpshooters and receive no sharpshooter cost premium.

* arquebus_bullet_c, arquebus_bullet_b, arquebus_bullet_a
* harquebus_bullet_c, harquebus_bullet_b, harquebus_bullet_a
* musket_bullet_c, musket_bullet_b, musket_bullet_a
* musket_carbine_bullet_c, musket_carbine_bullet_b, musket_carbine_bullet_a
* wall_gun_bullet
* long_gun_bullet
* flintlock_rifle_bullet
* rifled_musket_bullet_c, rifled_musket_bullet_b, rifled_musket_bullet_a, rifled_musket_bullet_s
* rifled_musket_carbine_bullet_c, rifled_musket_carbine_bullet_b, rifled_musket_carbine_bullet_a
* rifle_bullet_c, rifle_bullet_b, rifle_bullet_a, rifle_bullet_s
* rifle_carbine_bullet_c, rifle_carbine_bullet_b, rifle_carbine_bullet_a
* magazine_rifle_bullet_c, magazine_rifle_bullet_b, magazine_rifle_bullet_a, magazine_rifle_bullet_s
* magazine_rifle_carbine_bullet_c, magazine_rifle_carbine_bullet_b, magazine_rifle_carbine_bullet_a

Range and smoke:

Infantry (Arquebus):		160, musket_shot_set
Infantry (Musket):		200, musket_shot_set
Infantry (Rifle-musket):	220, musket_shot_set
Infantry (Rifle):	240, musket_shot_set
Infantry (Magazine Rifle):	260, smokeless_shot_set

Skirmishers: projectile up 1 tiers, range + 40
Sharpshooter: projectile up 2 tiers, range + 40
Early Rifle: Rifle-musket a base, projectile down 1 tier
Cavalry: projectile down 1 tier, range -20  

Note sharpshooters are not elite units, the type designation only affects projectiles.
Pistols use `magazine_rifle_bullet_c`, 60 range, 15 ammunition, and `musket_shot_set`; copy the rest of the row from a matching pistol-armed precedent.

5. Melee
Attack (militia): 2-4 (default 3), 2-4 (charge, default 2)
Attack (regular): 4-6 (default 5), 3-5 (charge, default 3)
Attack (elite): 5-8 (default 7), 4-6 (charge, default 4)

Armour (militia): 3, 2-4 (default 2), 0, leather
Armour (regular): 3, 3-5 (default 3), 0, leather
Armour (elite): 3, 4-6 (default 4), 0, leather
Armour (Cavalry): 4, 3-6 (default 4), 0, leather
Armour (Cuirassiers): 7, 4-6 (default 5), 0, metal

`metal` is the valid armour sound token for armoured troops; `armoured` causes EDU parsing failures.

For non-western style units, ask for clarification

6. Standard stats for gunpowder inf and cav
attributes       free_upkeep_unit, sea_faring, hide_forest, gunpowder_unit (if applicable), gunmen, start_not_skirmishing, cannot_skirmish
stat_ground      0, 0, 0, 0

Attributes are opt-in: do not retain copied special attributes unless the unit's documented role uniquely requires them. `hide_improved_forest`, `hardy`, `very_hardy`, terrain bonuses, and similar advantages require explicit justification; ordinary `hide_forest` remains part of the standard gunpowder template. Default to `stat_ground 0, 0, 0, 0`. Late infantry and carbine-armed cavalry receive `stakes`; other units receive them only when specifically required.

7. Officers and standard bearers

Western-style infantry uses exactly one faction-appropriate officer plus one verified standard bearer as a second EDU `officer` entry in both the early and mid periods. Late infantry uses only the officer. The `banner faction` field does not replace the visible standard-bearer model. Cavalry uses one officer unless a mounted standard-bearer model has been separately verified. A single unit record spanning multiple periods, including a general-and-staff unit, likewise defaults to one officer because its complement cannot vary by era.

Internal model names are not reliable evidence of role. Do not use `usa_pri_1g`, `rus_pri_1g`, `eur_pri_1g`, or another apparent swordsman/private model as a substitute standard bearer merely because of its name or EDU use. Add a second `officer` entry only when its mesh, faction mapping, and animations support the standard-bearer role. Verified early/mid infantry bearers are `russia_qi` for Prussia and Spain, `BRIT_FootA_Bearer1` for Britain, and `francejunqshou` for France, Denmark, and the Netherlands; each uses a dedicated bearer mesh and the relevant faction mapping. No verified mounted bearer currently exists for these factions, so their cavalry receives no second officer. Despite its misleading internal name, `otto_sipahi` uses the mounted `pru_gen_1g` mesh and is the verified Prussian mounted officer/general donor.

Officer compatibility belongs to the complete modeldb model/texture mapping, not to the texture file alone. Reuse a faction mapping already proven for the unit's foot or mounted role, or copy the complete donor entry with all string-length checksums; never place a texture onto an unrelated officer mesh merely because the UV layout appears similar. Use the national officer texture where one exists. Colonial or auxiliary units use the commanding power's officer only when that role is intentional; otherwise use an appropriate local officer. Do not retain arbitrary inherited second officers.

8. Cost rules
Structure:
stat_cost        recruitment time, campaign cost, campaign upkeep, 100 (weapon upgrade, always set 100), 100 (armour upgrade, always set 100), custom battle cost, custom battle number, custom battle over-recruitment penalty

Cost (campaign and custom):
Baseline Infantry (Arquebus): 900
Baseline Infantry (Musket): 1000
Baseline Infantry (Rifle-musket): 1200
Baseline Infantry (Rifle): 1500
Baseline Infantry (Magazine Rifle): 1800

By type: Militia = -200, Regular = +-0, Elite = +200, Sharpshooter = +200, Cavalry (Gun Armed) = +200, Cavalry (Gun Armed and Cuirassier/armoured) = +500

Baseline Melee Cavalry: 1000
By equipment: Lance = +200, Pistol = +200, Cuirassier/armoured = +300
By type: Militia = -200, Regular = +-0, Elite = +200

Faction modifiers will be applied when balancing particular factions

Cost of upkeep: Total cost/3 for professional units, Total cost/3 otherwise; same as over-recruitment penalty

## Unit-balancing workflow

Use this end-to-end sequence for every faction so a single balancing request covers discovery, clarification, implementation, and validation.

1. Inspect version-control state, preserve unrelated changes, note any user exclusions, identify the converted faction code, and identify every canonical file and runtime mirror before editing.
2. Inventory every unit available to the faction through ownership or era lists. Separate the main roster from shared, auxiliary, mercenary, naval, and artillery units so their rules and availability are not conflated.
3. Trace each unit through the canonical EDU, dictionary/localization, ownership and era lists, EDB, campaign files, mercenary pools, soldier/modeldb entries, UI cards, and referenced assets.
4. Build a working roster matrix recording visible and internal names, lineage/tier, quality, battlefield role, national/colonial/auxiliary/mercenary status, era availability, exact named weapon, attributes, formation, melee, charge, armour, morale, cost, custom-battle limit, model support, and shared records/assets.
5. Infer classifications only from clear canonical evidence. Before mutation, ask one consolidated set of questions if a classification is unclear, modifiers may stack ambiguously, a shared edit affects another faction, a name conflicts with equipment, historical equipment lacks a supported precedent, EDB scope is uncertain, or the model does not visibly support the intended weapons.
6. Freeze the agreed roster matrix. Use `early`, `mid`, and `high` for tiered internal type/dictionary/model names and eras 0, 1, and 2 respectively; explicitly record obsolete, late-entry, and single-entry exceptions.
7. Create variants from the preceding tier's records and assets, never from a successor. Create a distinct soldier/modeldb entry whenever weapon visibility or reload animation differs, and clone shared records before applying faction-specific changes.
8. Give every firearm a specific named weapon. Copy the complete weapon row from an exact same-weapon precedent, or the closest same-faction and same-era precedent, before applying only the documented projectile, range, ammunition, smoke, or role modifiers.
9. Apply balance in this order: weapon-era baseline, unit quality, battlefield role, systemic faction tier, then faction-specific and national/colonial/regional modifiers once. A projectile accuracy role such as skirmisher or sharpshooter does not independently grant elite morale, melee, armour, or cost treatment.
10. Align attributes, formation, bayonet/melee weapon, reload animation, projectile, smoke, and modeldb weapon slots with the chosen equipment. Strip inherited special attributes and terrain bonuses unless the roster matrix explicitly justifies them; apply the standard stakes rule. Confirm the model visibly supports every weapon assigned in the EDU.
11. Keep melee and pistol/revolver cavalry in `category cavalry` with `class light` or `class heavy` unless the unit is intentionally a ranged missile-cavalry role. Firearm behaviour comes from the weapon rows and attributes, not from `class missile`.
12. Calculate every `stat_cost` field explicitly: recruitment time, total cost, upkeep, both upgrade costs fixed at 100, custom-battle cost, custom-battle limit, and over-recruitment penalty. The seventh field is the custom-battle limit; treat artillery limits separately unless requested. Reconcile any mercenary-pool cost override.
13. Keep recruitment scopes distinct: EDU ownership and era lists govern custom-battle availability, while EDB and mercenary pools govern campaign recruitment. Shared mercenary or auxiliary availability does not make a unit part of the faction's main line.
14. Update dictionary and localization names/descriptions to match the exact equipment and role. Create a properly composed 48x64 tactical card for every internal unit type during the faction pass, with a distinct documented historical unit reference for each type and no unit-reference reuse between period variants. Skirmishers and sharpshooters may additionally reuse an approved kneeling pose from the shared pose pool. Use predecessor or donor game art only to constrain the verified in-game uniform and rendering style, and handle the localization cache without changing file encoding. Use the canonical card background that matches the battle UI's exposed lower strip.
15. Edit canonical files first. Validate them before copying byte-for-byte to runtime mirrors; treat `data/tow_steamsteel` as canonical for database files and `camp_steamsteel` as canonical for campaign files.
16. Run static validation for unique types and dictionaries, valid tokens, ownership/era coverage, complete references, cost arithmetic, projectile/attribute compatibility, asset existence, tactical-card filenames, 48x64 dimensions, 32-bit RGBA/alpha, framing and background consistency, exact agreement between the canonical card background and the exposed lower strip of normal and selected battle-card sprites in every culture, modeldb header and entry counts, string-length checksums, weapon order, stale names, conflict markers, and exact canonical/runtime hashes.
17. After launch, inspect a freshly timestamped game log and fix every parsing error. If the game crashes without a useful log, revalidate modeldb structure and assets, then isolate the most recent change. Repeat until the affected roster loads cleanly.
18. Report the final roster and stat changes concisely, including assumptions, exceptions, validation performed, any runtime test still needed, and unrelated working-tree changes left untouched.

Mercenary units with the `mercenary_unit` attribute can be recruited through EDB or mercenary pools without factional EDU ownership. EDU ownership and era assignments control their custom-battle availability, so do not conflate those scopes.

### Systemic faction tiers

Every balanced faction must be assigned one systemic tier before its faction-specific rules are applied. Start from the completed weapon, quality, and battlefield-role baseline; apply the tier exactly once; then apply the faction-specific and national, colonial, or regional exceptions exactly once. Tier modifiers do not change weapon range, ammunition, weapon damage, formation, unit strength, health, training, armour material, the first armour value, shield value, or cost.

For this section, `defence` means only the second value in `stat_pri_armour` (defensive skill). It does not mean the first armour value. `Discipline +1` follows `low` to `normal` to `disciplined`; `discipline -1` reverses that sequence. Keep discipline within `low` and `disciplined`, and do not shift `impetuous` unless a unit-specific rule explicitly requires it. Projectile shifts follow `c` to `b` to `a` to `s`, capped at `c` and `s`. Pistols remain fixed at `magazine_rifle_bullet_c` and ignore tier accuracy modifiers.

* A tier: +1 projectile accuracy tier, +1 melee attack, +1 charge, +1 defensive skill, +1 morale, and +1 discipline tier. Armour value is unchanged.
* B tier: no systemic modifiers; use the completed weapon, quality, and role defaults.
* C tier: -1 projectile accuracy tier, -1 melee attack, and -1 discipline tier. Charge, defensive skill, morale, and armour value are unchanged.
* D tier: -1 projectile accuracy tier, -1 melee attack, -1 defensive skill, -1 morale, and -1 discipline tier. Charge and armour value are unchanged.

Record each faction's assigned tier beside its faction-specific rules. Do not restate or stack a systemic tier bonus as a faction-specific bonus: faction-specific rules contain only deliberate additions, reversals, subgroup treatments, or exceptions beyond the selected tier. If a subgroup uses another tier, calculate it directly from that tier rather than applying the main faction tier and reversing it. When converting a previously balanced faction, calculate every final value anew from the universal weapon, quality, and role baseline; never add the new tier to already-modified EDU values.

### Spain modifiers

Spain is B tier. National Spanish infantry receives +1 melee and +1 charge beyond the B-tier baseline. Colonial units instead receive -1 melee and -100 cost. Cazadores are regular-quality skirmishers; Cuban Infantry are regular-quality colonial sharpshooters and a late-only independent lineage.

### Denmark modifiers

Denmark is B tier. National Danish units receive +1 projectile accuracy tier where applicable, +1 morale, and +200 cost beyond the B-tier baseline. Apply the cavalry accuracy penalty and role modifiers before the faction bonus, capped at `s`; pistols remain fixed at `magazine_rifle_bullet_c`. Fod has a custom-battle limit of 3, while Lette Fod and every other Danish non-artillery unit have a limit of 1.

### Britain modifiers

Britain is A tier. British units receive only +1 additional morale and +200 cost beyond the complete A-tier package; do not repeat the A-tier projectile, melee, charge, defence, morale, or discipline bonuses. British infantry formations use 2 ranks in the fifth formation field by default. Indian Foot uses the B-tier stat baseline instead of A tier, retains its quality-default discipline, and receives no British cost premium, but still uses the British formation rule. Highlanders remain regular quality for accuracy, armour baseline, and cost, but use elite-quality melee and morale baselines before applying the A-tier and additional British morale modifiers. Gurkhas receive a further +2 melee attack and +2 defensive skill beyond the A-tier package. Pistols remain fixed at `magazine_rifle_bullet_c`. All British cavalry uses pistols rather than carbines except the Imperial Camel Corps. Create a separate British record when applying these modifiers to a unit shared with another faction rather than changing the shared unit.

### France modifiers

France is A tier. After the complete A-tier package, add +1 morale and reduce discipline one tier (`disciplined` to `normal`, `normal` to `low`, with `low` as the floor), leaving training unchanged. French militia and colonial units use the B-tier stat baseline instead of A tier, then receive the French additional morale and discipline reduction; do not apply and reverse A-tier modifiers. Colonial units are regular line troops unless otherwise specified: do not infer skirmisher status from the word `tirailleur`; apply -1 melee and -100 cost, and represent most of their historical disadvantage through older armament. France has no faction cost modifier, and roster breadth is its principal faction advantage.

### Prussia modifiers

Prussia is A tier. Core Prussian, Imperial German, and German colonial units use the complete A-tier package with no duplicate faction-wide skill bonuses. Regional German units use a B-tier baseline: early regional units receive +1 morale; mid regional units receive +1 morale and +1 discipline tier; late regional units receive +1 morale, +1 discipline tier, and +1 projectile accuracy tier. Pistols remain fixed at `magazine_rifle_bullet_c`. Prussia has no faction cost modifier.

### Netherlands modifiers

The Netherlands is B tier. National non-militia, non-colonial units receive +1 discipline tier, +1 melee attack, +1 defensive skill, and +200 cost beyond the B-tier baseline. Schutterij uses the militia-quality B-tier baseline without these national modifiers, while KNIL and other colonial units use their stated B-tier quality baseline without the national modifiers. Jagers are regular-quality skirmishers and receive only the standard +1 projectile role modifier. Dutch pistol cavalry uses the fixed pistol row and remains light or heavy cavalry; Dutch carbine cavalry is an intentional ranged role and uses `class missile`, the standard cavalry projectile penalty, a sabre secondary weapon, and stakes.

### Sweden–Norway modifiers

Sweden–Norway is A tier, except that units retain both their quality-default morale and quality-default discipline rather than receiving the A-tier +1 modifiers to those stats. Apply the remaining A-tier projectile, melee attack, charge, and defensive skill modifiers exactly once. National Swedish and Norwegian units receive +300 cost; the universal fixed cost for four-man general-and-staff units remains 200 and overrides this premium. Early-period placement does not make a firearm a muzzle-loader: purpose-built early breechloaders such as the Kammerlader use breechloader attributes and animations, while contemporary percussion muzzle-loaders use the muzzle-loading rules. Every weapon label must identify a specific service arm rather than a generic mechanism such as “percussion rifle.”

### Greece modifiers

Greece uses a modified C-tier baseline: apply the C-tier -1 projectile accuracy and -1 discipline tier, but do not apply its melee-attack penalty. Greek melee attack, charge, defensive skill, morale, and armour therefore remain at their completed B-tier quality and role defaults. Pistols remain fixed at `magazine_rifle_bullet_c`. Greece has no faction cost modifier. Early regular infantry uses a Greek-service Minié rifle-musket; older flintlock and percussion smoothbore arms are limited to militia or obsolete roles. Chassepot rifles do not appear in the early period.

##Modeldb Formatting:

Example modeldb entry; bold part is the relevant part.
Note that 20 MTW2_Fast_Arquebus_3 is the default M2 firing animation, while 14 MTW2_Musket_SS is the custom breechloading animation (only works for infantry)

9 uk_musket; (9 is a checksum for uk_musket)
1 4; (4 is a checksum for number of meshes)
43 unit_models/_Units/eng/eng_col_1g_lod0.mesh 20000
43 unit_models/_Units/eng/eng_col_1g_lod0.mesh 20000
43 unit_models/_Units/eng/eng_col_1g_lod0.mesh 20000
43 unit_models/_Units/eng/eng_col_1g_lod0.mesh 20000
2; (2 is a checksum for number of factions)
7 england
50 unit_models/_Units/eng/textures/eng_col_1g.texture
58 unit_models/_Units/attachments/textures/blank_norm.texture
51 unit_sprites/milan_Dummy_EN_Spearmen_ug1_sprite.spr
5 slave
50 unit_models/_Units/eng/textures/eng_col_1g.texture
58 unit_models/_Units/attachments/textures/blank_norm.texture
51 unit_sprites/milan_Dummy_EN_Spearmen_ug1_sprite.spr
2; (2 is a checksum for number of factions)
7 england
58 unit_models/_Units/attachments/textures/whi_gbfrxx.texture
58 unit_models/_Units/attachments/textures/blank_norm.texture 0
5 slave
58 unit_models/_Units/attachments/textures/whi_gbfrxx.texture
58 unit_models/_Units/attachments/textures/blank_norm.texture 0
1
4 None (4 is a checksum for none)
14 MTW2_Musket_SS 9 MTW2_Pike
1
19 MTW2_Musket_Primary
1
17 MTW2_Pike_primary
16 -0.090000004 0 0 -0.34999999 0.80000001 0.60000002
