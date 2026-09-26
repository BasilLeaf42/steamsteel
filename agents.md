# Universal Info

## Indian Princely States balance

Indian Princely States (`bulga`) is D tier with no faction-wide buff. Apply the D-tier quality baselines before equipment exceptions and grant only bonuses visibly supported by the loaded mesh. National firearm infantry uses 40 men, dedicated skirmishers and wall-gun teams use 30, melee infantry uses 80, cavalry uses 24, and Maharaja aur Lashkar is the universal four-man mounted light command unit in two ranks. Maratha Paltan, Rajput Banduqchi, Jazailchi Gingal Wall Gunners, Khalsa Guard and Akali Jatha receive their sword or axe melee adjustment only because their meshes visibly carry that weapon; Lashkar Nayzabaz, Khalsa Gorchara, Khalsa Guard and Akali Jatha retain only their mesh-supported shield value. Purbiya Sepoys retain bayonets because their mesh supports them. Sowar Banduqchi are matchlock-carbine missile cavalry, Risala Lancers use the regional Sikh lance-and-sword mesh, and no inherited terrain, discipline, armour, anti-cavalry or faction bonus is permitted without matching visible equipment. Armstrong artillery is early/mid; 12-pounder, 5-pounder and Maxim are late; Gatling and 150 mm artillery are hidden from the national custom-battle roster.

## Turkestan balance

Turkestan is D tier with no additional faction-wide stat or cost modifier. Russian-trained Sarbaz remain D-tier regulars with `trained` training; they do not receive a higher systemic baseline. Turkic cavalry receives no melee, charge, morale, discipline, or defence bonus: its faction distinction is greater relative availability, represented by a custom-battle limit of 3 for Jigitlar and 2 for Turkman Otliqlari. National firearm infantry uses 40 men, dedicated skirmishers use 30, melee levies use 80, cavalry uses 24, and Qorboshi va Mulozimlar is the universal four-man mounted light command unit. Retain only mesh-supported equipment: Tufangchilar use the visible matchlock-and-sword mapping, Ghulja and Darkhan skirmishers retain their donor two-handed axe secondary mappings, the late Berdan Sarbaz uses `MTW2_Musket_SS` without `gunpowder_unit`, and mounted gunmen retain their embedded arquebus and sword geometry. Tibetan formations and duplicate mercenary Kashgar/Kazakh records are not national Turkestan custom-battle units. Gatling and 150 mm artillery are hidden; bronze cannon is early/mid, while the mortar, smoothbore field gun, and Maxim are late and limited.

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

## Unit-name and short-description structure

Visible period variants use the historically appropriate unit name followed by exactly `(Early)`, `(Mid)`, or `(Late)` in English. Do not translate these three period labels. Internal record suffixes remain `_early`, `_mid`, and `_high`; `_high` maps to visible `(Late)`. A single unchanged record spanning periods does not need a visible period label.

Short descriptions do not include periodization. They begin formulaically with the unperiodized visible unit name and weapon identification: `Unit Name (Weapon Family, Exact Model), additional description.` For example: `Askar Infantry (Rifle-Musket, Pattern 1853 Enfield), infantry of the reformed Moroccan army.` Put the standardized weapon family first and the historically specific model second. Do not substitute prose such as `armed with` or `equipped with`. Preserve any useful existing short-description detail after the closing parenthesis and comma. Traditional melee or missile equipment may use a concise equipment tuple when no model distinction exists, while artillery uses its exact established weapon designation. Long descriptions are outside this normalization pass and must remain unchanged.

## Relevant files
"steamsteel\data\tow_steamsteel\export_descr_unit.txt" - edu, main unit database
"steamsteel\data\tow_steamsteel\export_descr_buildings.txt" - edb, main building database
"steamsteel\data\text\export_units.txt" - name translations
"steamsteel\data\unit_models\battle_models.modeldb" - unit model database
"steamsteel\data\ui\units" - unit gameplay cards
"steamsteel\data\ui\unit_info" - detailed description cards

### Unit cards

Create tactical unit cards as part of balancing each faction, not as a later cleanup. Every internal unit type must have its own correctly named physical card, but period variants within the same unit lineage may share one card when their loaded model, uniform, equipment, mount, and visible weapons are genuinely unchanged. Different unit trees must not share a card composition. Generate a new card only when no preserved or verified donor card can separate those trees honestly, or when the existing card fails the model-signature or visual audit. Every newly generated composition requires a documented historical unit-reference image; the only permitted pose-source reuse is an approved kneeling reference from the shared skirmisher pose pool described below.

Before generating or replacing any card, preserve every distinct pre-existing card in the source archive and record its original members. Assign preserved art to the most appropriate unit whose loaded model and visible equipment it genuinely matches; do not discard a valid low-resolution card merely because a new composition exists. If a pre-existing card fails the visual or model-signature audit and cannot be assigned honestly, retain it in the archive as a superseded reference rather than forcing it onto an unsuitable unit or overwriting its only copy.

`data/ui/units/<faction>/#<unit>.tga` is the same 48x64 source card used in battle, in a selected campaign army, and for recruitment. Steam & Steel's custom battle UI provides a 48x80 card background, but the lower 16 pixels belong to the normal or selected `BATTLE_CARD_BACKGROUND` sprite rather than the unit-card texture. Keep tactical cards at 48x64. Replace the complete 48x80 normal and selected battle-card background sprites with the same canonical background used by the cards so no old colour, transparency, or edge treatment remains and the combined battle display appears full-height. Apply this one-time UI-atlas correction consistently to every culture rather than extending or vertically stretching every unit card.

Preserve 32-bit RGBA and alpha. Reuse the established current card style, using the canonical parchment background colour `#B8AD8F` rather than retaining inconsistent donor background colours. Give each period variant its own historically grounded composition even when its in-game model is unchanged. `data/ui/unit_info` contains the separate large information portrait and need not be regenerated unless requested.

Background normalization is a hard acceptance gate, not a cosmetic afterthought. Never classify background by a broad beige, low-saturation, luminance, or corner-colour range: those tests consume skin, white clothing, pale horses, smoke and light headwear. Prefer a genuine alpha cutout composited over `#B8AD8F`. If an opaque generated master must be keyed, use border-seeded edge-continuity segmentation with a strict neighbour-to-neighbour colour-distance threshold; preserve a foreground mask before recolouring and fail installation if any protected interior foreground pixel changes. Render a labelled contact sheet of every installed 48x64 card on the actual canonical background and inspect every face, hand, garment edge, mount and weapon. A script reporting correct dimensions or corner pixels is insufficient, and the installer must not report success until the contact sheet shows no washed-out, parchment-coloured or partially erased figure regions.

The firing-state symbol drawn over a tactical card is `CARD_ATTACKING_MISSILE` in the 16x16 rectangle `(365,1)-(380,16)` of `sharedpage_01.tga`, as defined by `data/ui/shared.sd.xml`; it is not sourced from `data/ui/icons/missiles.tga`. Use the exact preserved majority/original crosshair tile in every culture and nested interface variant. Never generate a replacement crosshair when that verified original is available, and validate the installed tiles by exact pixel equality.

Crop approved source artwork to the tactical card's 3:4 aspect ratio before reducing it to 48x64; never change the aspect ratio by stretching. For tall portrait outputs, preserve the head and torso and remove excess lower-body space first. Record a unit-specific crop box in the source register when the automatic top-weighted crop does not produce the close original-card framing.

The card must depict the unit actually loaded by the EDU: trace its `soldier` entry through modeldb and verify the mesh, faction texture, attachments, mount, and visible weapons. A donor card is valid only when its modeldb visual signature matches those assets; similarity of unit names, role, nation, or era is not enough. If no exact visual donor exists, retain or create a card from the actual model rather than substituting a convenient approximate unit.

Base every newly created unit-card composition on a documented period photograph, contemporary engraving, or historically reliable uniform plate for the same unit or the closest defensible national, period, and battlefield-role match. The historical image controls pose, anatomy, hand placement, mount posture, and weapon interaction; the traced in-game model controls the final uniform, equipment, and visible weapon. Record the source URL, attribution, date, licence, depicted subject, and any approximation in the card-source register. Do not install a historically styled card whose source or mapping has not been recorded.

Treat the historical source as a compositional constraint, not a mood reference: preserve its limb arrangement, weight distribution, grip, mount relationship, and weapon orientation unless a documented equipment difference requires a small change. Reject a result that invents a substantially different pose or mechanical action. Before installation, mark each newly generated composition's source mapping approved in `tools/historical_card_sources.json`; the card installer must fail closed when a generated composition has an incomplete, missing, or unapproved source record. Intentional sharing within one unchanged unit lineage must be recorded explicitly and must never conceal sharing between different unit trees.

Kneeling skirmisher photographs or plates need not exist for every uniform. Maintain a small, separately documented pool of mechanically correct period kneeling rifle poses in `tools/historical_skirmisher_pose_sources.json`. A skirmisher or sharpshooter may reuse one approved pool pose for anatomy, weight distribution, hand placement, and weapon orientation while retaining its own distinct national, period, and unit-specific historical reference for uniform and equipment. Record the pool ID as `pose_source_id` in the unit register. Do not use the pool for line infantry, cavalry, artillery, or generals, and do not use an unapproved, anachronistic, mirrored, or mechanically implausible pose merely to satisfy the kneeling rule.

When a pool pose has an approved generated master, create further cards as localized uniform/equipment retextures of that master. Preserve the master silhouette, limbs, hands, grip, shoulder contact, and rifle geometry pixel-for-pixel wherever the assigned weapon permits; do not regenerate the whole figure. A materially different weapon action requires another historically sourced and approved pose master rather than forcing a new mechanism or grip into an incompatible composition.

Visually audit every created or generated card individually at both source size and the final 48x64 reduction. Pale cloaks, white robes, light headwear, and exposed faces must retain a clean readable silhouette against the canonical parchment background; reject merging edges, patterned residue, halos, or background-coloured facial regions. Tactical role is mandatory at 48x64: skirmishers and sharpshooters must visibly kneel, while cavalry and camelry must visibly include the correct horse or camel, tack, and mounted posture. Double-check both hands, every finger-to-weapon contact, and the complete weapon before approval. Reject duplicated, disconnected, inverted, fused, or misplaced hands and limbs; malformed faces; implausible grips; awkward joint cuts; incorrect foot or mounted status; distorted weapon length; missing role-defining equipment; inappropriate general poses or props; mismatched uniforms; and compositions that become unreadable at tactical size. Do not rely on a spot check or generation success alone.

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

Choose the animation from both weapon action and battlefield role, not era alone. Every non-muzzle-loading skirmisher or sharpshooter uses `MTW2_Musket_SSK`, including late magazine-rifle units. Never combine `gunpowder_unit` with `MTW2_Musket_SSK`; a muzzle-loading skirmisher uses a normal muzzle-loading animation and must have a distinct soldier/modeldb entry when another period uses SSK. A skirmisher model must have a distinct soldier/modeldb entry whenever a shared line-infantry or different-period record requires another animation. Do not infer correctness from an existing late unit: the surviving Boer sharpshooter uses the generic set, while `moroccan_gunner1` is the verified `MTW2_Musket_SSK` precedent.

All modern line infantry should use 17 MTW2_Pike_primary for bayonets.

Cavalry: as the custom MTW2_Musket_SS breechloading animation cannot be used for them, their logic is much simpler
Muzzle-loading: gunpowder_unit
Breech-loading: NO gunpowder_unit

Changing a cavalry skeleton or EDU weapon does not create the visible weapon: pistol, carbine, lance, and sabre geometry is embedded in the rider mesh. Reject a nationally or regionally inappropriate lancer merely because it carries a lance; when no compatible lance model exists, prefer a verified generic regional sword-cavalry model and realign the EDU weapon, animations, cost, card, and localization instead of retaining an implausible donor. Lancers must use a verified period-appropriate lance mesh with the lance group marked `primaryactive0` and the sabre marked `secondaryactive0`; use a Western/European lance donor for European units and never substitute an Asian bamboo lance. Copy the complete donor modeldb structure and compatible texture mappings with correct string-length checksums.

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
Early rifle or converted breechloader: use the rifle-musket ballistic and cost baseline, with projectile accuracy down 1 tier before faction modifiers. A later conversion date does not promote an obsolete converted muzzle-loader to the full rifle tier; retain the parent arm's range and ballistic limitations unless evidence supports otherwise. Treat Maynard and Sharps arms, Spencer M1860/M1865 repeaters, Snider, Tabatiere, and Waenzl conversions, and comparable 1850s-1860s early breechloaders as subject to this debuff even when their date places them in the mid-period slot; any full-rifle exception must be stated explicitly in the faction rule. Keep `stat_fire_delay` at 0: nonzero values are engine-unsafe in this project and must not be used to simulate weapon speed or unreliability. Do not misrepresent mechanical unreliability as reduced carried ammunition.
Cavalry: projectile down 1 tier, range -20  

Note sharpshooters are not elite units, the type designation only affects projectiles.
Pistols use `magazine_rifle_bullet_c`, 60 range, 15 ammunition, and `musket_shot_set`; copy the rest of the row from a matching pistol-armed precedent. Every pistol or revolver is a named weapon: record the historically appropriate exact model in the EDU dictionary comment and localization rather than using generic `pistol` or `revolver` wording.

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

Detect sword-equipped infantry during every roster pass instead of assuming that every firearm infantry model carries a bayonet. Inspect the loaded mesh's named and active weapon groups, its complete modeldb primary/secondary animation mapping, and an in-game or extracted-model view where names are ambiguous. If the mesh visibly carries a sword as its secondary weapon, give the unit +1 melee attack beyond its completed quality, tier, and faction baseline, retain the normal charge value, remove `ap` and `short_pike`, use the appropriate sword weapon token, and assign a verified compatible sword animation set. Distinguish one-handed from two-handed sword meshes from the donor mapping; do not apply `MTW2_2HSwordsman` merely because a sword exists. Keep bayonet statistics and pike animations only when the model visibly supports a fixed bayonet. If a model visibly carries a shield, apply its documented shield value in the third `stat_pri_armour` field; do not infer `spear` or another explicit anti-cavalry attribute merely from a tribal or warband label.

6. Standard stats for gunpowder inf and cav
attributes       free_upkeep_unit, sea_faring, hide_forest, gunpowder_unit (if applicable), gunmen, start_not_skirmishing, cannot_skirmish
stat_ground      0, 0, 0, 0

Attributes are opt-in: do not retain copied special attributes unless the unit's documented role uniquely requires them. `hide_improved_forest`, `hardy`, `very_hardy`, terrain bonuses, and similar advantages require explicit justification; ordinary `hide_forest` remains part of the standard gunpowder template. Default to `stat_ground 0, 0, 0, 0`. Engineering units receive `stakes` in every period. Other infantry and carbine-armed cavalry receive `stakes` only in the late/`high` period; early- and mid-period non-engineering units must not retain them.

Every cavalry soldier model must also use a mounted distant-LOD sprite. During the modeldb audit, reject standing infantry sprites such as Musketeers, Spearmen, Huscarls, or ordinary Men-at-Arms on cavalry entries and copy a verified mounted cavalry sprite mapping instead. Correct the string-length checksum with the copied path; changing the close rider mesh alone does not fix the distant battlefield sprite.

7. Officers and standard bearers

Western-style infantry uses exactly one faction-appropriate officer plus one verified standard bearer as a second EDU `officer` entry in both the early and mid periods. Late infantry uses only the officer. The `banner faction` field does not replace the visible standard-bearer model. Cavalry uses one officer unless a mounted standard-bearer model has been separately verified. A single unit record spanning multiple periods, including a general-and-staff unit, likewise defaults to one officer because its complement cannot vary by era.

Every four-man General-and-Staff unit is mounted `category cavalry`, `class light`, and uses the standard two-rank formation. Do not classify it as heavy or missile cavalry merely because its donor rider or sidearm came from such a unit.

Internal model names are not reliable evidence of role. Do not use `usa_pri_1g`, `rus_pri_1g`, `eur_pri_1g`, or another apparent swordsman/private model as a substitute standard bearer merely because of its name or EDU use. Add a second `officer` entry only when its mesh, faction mapping, and animations support the standard-bearer role. Verified early/mid infantry bearers are `russia_qi` for Prussia, Spain, and Italy, `BRIT_FootA_Bearer1` for Britain, and `francejunqshou` for France, Denmark, and the Netherlands; each uses a dedicated bearer mesh and the relevant faction mapping. No verified mounted bearer currently exists for these factions, so their cavalry receives no second officer. Despite its misleading internal name, `otto_sipahi` uses the mounted `pru_gen_1g` mesh and is the verified Prussian mounted officer/general donor.

Officer compatibility belongs to the complete modeldb model/texture mapping, not to the texture file alone. Reuse a faction mapping already proven for the unit's foot or mounted role, or copy the complete donor entry with all string-length checksums; never place a texture onto an unrelated officer mesh merely because the UV layout appears similar. Use the national officer texture where one exists. Colonial or auxiliary units use the commanding power's officer only when that role is intentional; otherwise use an appropriate local officer. Do not retain arbitrary inherited second officers.

When moving or cloning a unit onto a new faction, preserve the source mesh's original face geometry and face attachment texture mapping. Standard bearers require the same face audit as rank-and-file models, and both faces of the visible cloth must show the intended national device rather than a blank or one-sided field. Do not recolour, remap, or transplant face islands merely to change ethnicity or complexion: malformed or unusual legacy meshes make those edits unreliable. Change faces only when the replacement is an independently verified, exact mesh-and-UV match and the user explicitly requests it. This default applies to future transplants; leave already accepted faction-specific assets unchanged unless they are reported faulty.

8. Cost rules
Structure:
stat_cost        recruitment time, campaign cost, campaign upkeep, 100 (weapon upgrade, always set 100), 100 (armour upgrade, always set 100), custom battle cost, custom battle number, custom battle over-recruitment penalty

Recruitment time is quality-based for land units: militia, reserve, levy, and irregular infantry use 2 turns; regular infantry uses 3; elite infantry uses 4. Cavalry adds 1 turn to the corresponding quality value, producing 3/4/5. Units carrying `general_unit` use 1 turn. Do not treat the broader `command` attribute as proof that a combat formation is a general. Ships and artillery retain their separately established recruitment times.

Cost (campaign and custom):
Baseline Infantry (Arquebus): 900
Baseline Infantry (Musket): 1000
Baseline Infantry (Rifle-musket): 1200
Baseline Infantry (Rifle): 1500
Baseline Infantry (Magazine Rifle): 1800

By type: Militia = -200, Regular = +-0, Elite = +200, Sharpshooter = +200, Cavalry (Gun Armed) = +200, Cavalry (Gun Armed and Cuirassier/armoured) = +500

Baseline Melee Infantry: 700

By type: Militia = -200, Regular = +-0, Elite = +200

Baseline Melee Cavalry: 1000
By equipment: Lance = +200, Pistol = +200, Cuirassier/armoured = +300
By type: Militia = -200, Regular = +-0, Elite = +200

Lance cavalry receives +3 charge on the primary lance weapon relative to its sabre secondary weapon. Apply this equipment bonus after quality and faction modifiers, only to `stat_pri`; do not repeat it on the sabre row.

Faction modifiers will be applied when balancing particular factions

Cost of upkeep: Total cost/3 for professional units, Total cost/3 otherwise; same as over-recruitment penalty

`free_upkeep_unit` belongs only to formations explicitly classified as militia, reserve, levy, or irregular. Never infer militia status from `low` discipline alone: C- and D-tier modifiers can reduce professional regulars to `low`, while some European reserves retain respectable training and morale. Determine the underlying quality from the frozen roster classification and faction rules; professional line infantry, skirmishers, Marines, engineers, and regular cavalry do not receive free upkeep merely because their final `stat_mental` row resembles militia.

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
11. Keep melee and pistol/revolver cavalry in `category cavalry` with `class light` or `class heavy`. Every genuine carbine-armed cavalry unit uses `class missile`; identify it from the loaded weapon row and visible mesh rather than from an inherited class or internal name. Short-range pistol rows that happen to use a legacy carbine projectile token remain light or heavy and are not carbine cavalry.
12. Calculate every `stat_cost` field explicitly: recruitment time, total cost, upkeep, both upgrade costs fixed at 100, custom-battle cost, custom-battle limit, and over-recruitment penalty. The seventh field is the custom-battle limit; treat artillery limits separately unless requested. Reconcile any mercenary-pool cost override. Audit the complete per-era custom-battle roster after each faction pass, including shared and mercenary records still carrying faction ownership. Main mass lineages normally receive limits of 2–3, while specialists, elites, regional subtypes, command units, and most cavalry default to 1 unless a documented historical availability case justifies more. Do not let overlapping named militia or mercenary copies inflate the total roster; remove redundant custom-battle ownership while preserving campaign mercenary recruitment.
13. Keep recruitment scopes distinct: EDU ownership and era lists govern custom-battle availability, while EDB and mercenary pools govern campaign recruitment. Shared mercenary or auxiliary availability does not make a unit part of the faction's main line.
14. Update dictionary and localization names/descriptions to match the exact equipment and role. Give every internal unit type a correctly named 48x64 tactical-card file during the faction pass. Reuse a verified card within one lineage when its loaded appearance is unchanged, but never share a composition between different unit trees; generate only the missing or visually invalid compositions. Record a distinct historical reference for each generated composition, while skirmishers and sharpshooters may additionally reuse an approved kneeling pose from the shared pose pool. Double-check hands, grips, and complete weapon geometry at source size and 48x64. Use predecessor or donor game art only to constrain the verified in-game uniform and rendering style, handle the localization cache without changing file encoding, and use the canonical card background that matches the battle UI's exposed lower strip.
15. Edit canonical files first. Validate them before copying byte-for-byte to runtime mirrors; treat `data/tow_steamsteel` as canonical for database files and `camp_steamsteel` as canonical for campaign files.
16. Run static validation for unique types and dictionaries, valid tokens, ownership/era coverage, complete references, cost arithmetic, projectile/attribute compatibility, asset existence, tactical-card filenames, 48x64 dimensions, 32-bit RGBA/alpha, framing and background consistency, exact agreement between the canonical card background and the exposed lower strip of normal and selected battle-card sprites in every culture, modeldb header and entry counts, string-length checksums, weapon order, stale names, conflict markers, and exact canonical/runtime hashes.
17. After launch, inspect a freshly timestamped game log and fix every parsing error. If the game crashes without a useful log, revalidate modeldb structure and assets, then isolate the most recent change. Repeat until the affected roster loads cleanly.
18. Report the final roster and stat changes concisely, including assumptions, exceptions, validation performed, any runtime test still needed, and unrelated working-tree changes left untouched.

## Campaign EDB recruitment

Treat `data/tow_steamsteel/export_descr_buildings.txt` as authoritative and copy the validated result byte-for-byte to `data/export_descr_buildings.txt`. Keep normal recruitment (`recruit_pool` maximum at least 1) distinct from replenishment (maximum below 1).

Normal recruitment follows building role and quality. Ordinary infantry and cavalry use barracks; marines use military ports; artillery uses cannon buildings; generals and command units use the professional-military chain; ships use ports. Militia Drill Squares recruit only militia, reserve, and irregular units; Militia Barracks add regulars; Army Barracks add elites; Royal Armouries retain all lower categories. Replenishment remains available at every tier of the unit's correct building family for player convenience. A replenishment row retains its faction and date restrictions but deliberately ignores quality-tier and geographic gates; do not mistake this intentional universal regional resupply access for unrestricted normal recruitment.

Every replenishment row has a maximum pool of `0.99`. This permits full retraining of any surviving formation while remaining below the `1.0` needed to recruit a new unit. Preserve each row's established initial reserve and replenishment rate when raising its older maximum to `0.99`; do not recalculate those two fields from the new maximum. An initial reserve must nevertheless remain below `1.0`, because an initial value of one would itself permit fresh recruitment and defeat the replenishment-only design.

Derive normal barracks pool values deterministically from the EDU custom-battle limit `N`. Every normal recruitment row starts with an initial pool of at least `1`; the separate replenishment initial may increase the effective total. For `N=1/2/3/4/5`, use Militia Drill Square `1/.01/1, 1/.02/1, 1/.03/1, 1/.04/1, 1/.05/2`; Militia Barracks `1/.03/1, 1/.06/1, 1/.09/1, 1/.12/1, 2/.15/2`; Army Barracks `1/.06/1, 2/.12/2, 2/.18/2, 3/.24/3, 3/.30/3`; Royal Armoury `1/.10/1, 2/.20/2, 3/.30/3, 4/.40/4, 5/.50/5`, where each tuple is `initial/rate/maximum`. Artillery normally has two available per distinct unit and cavalry one unless an explicit exception applies.

Every recruitment row must be geographically gated. European-style factions may recruit their standard line infantry and, where applicable, reserve line infantry throughout explicitly defined Europeanized regions; colonial infantry belongs only in its colonial regions. Non-European units and geographic auxiliaries are regionally restricted by default. Use separate complete rows for alternative regions rather than ambiguous mixed `and/or` requirement clauses.

Use the five-year event counters `military_reforms_1860`, `_1865`, `_1870`, `_1875`, `_1` (1880), `_1885`, `_1890`, `_1895`, `_2` (1900), and `_1905`. For firearm infantry and genuine carbine-armed missile cavalry, date normal recruitment from the exact weapon adoption or conversion year rounded to the nearest five years: the successor requires its starting counter and the predecessor gains `not event_counter <successor> 1`. Apply the same date window to replenishment so units cannot be supplied before introduction or after obsolescence. This weapon-driven rule does not apply to melee infantry, pistol/lance/sabre/bow cavalry, generals, artillery, or ships.

All other units follow their EDU period assignment for both normal recruitment and replenishment: early-only units run from 1860 until 1870, mid-only units from 1870 until 1890, and late-only units from 1890 onward; early/mid units stop in 1890, mid/late units begin in 1870, and units assigned to all three periods remain continuously available. A late unit continues indefinitely unless a distinct later successor exists, in which case terminate both normal recruitment and replenishment at that successor's explicit five-year gate. Existing field armies are not automatically converted by EDB changes.

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

Spain is C tier. National Spanish infantry receives +1 melee and +1 charge beyond the complete C-tier baseline. Colonial units instead receive -1 melee and -100 cost. Cazadores are regular-quality skirmishers; Cuban Infantry are regular-quality colonial sharpshooters and a late-only independent lineage. Apply the C-tier projectile and discipline penalties normally; pistols remain fixed at `magazine_rifle_bullet_c`.

### Denmark modifiers

Denmark is B tier. National Danish units receive +1 projectile accuracy tier where applicable, +1 morale, and +200 cost beyond the B-tier baseline. Apply the cavalry accuracy penalty and role modifiers before the faction bonus, capped at `s`; pistols remain fixed at `magazine_rifle_bullet_c`. Fod has a custom-battle limit of 3, while Lette Fod and every other Danish non-artillery unit have a limit of 1.

### Britain modifiers

Britain is A tier. British units receive only +1 additional morale and +200 cost beyond the complete A-tier package; do not repeat the A-tier projectile, melee, charge, defence, morale, or discipline bonuses. British infantry formations use 2 ranks in the fifth formation field by default. Indian Foot uses the B-tier stat baseline instead of A tier, retains its quality-default discipline, and receives no British cost premium, but still uses the British formation rule. Highlanders remain regular quality for accuracy, armour baseline, and cost, but use elite-quality melee and morale baselines before applying the A-tier and additional British morale modifiers. Gurkhas receive a further +2 melee attack and +2 defensive skill beyond the A-tier package. Pistols remain fixed at `magazine_rifle_bullet_c`. All British cavalry uses pistols rather than carbines except the Imperial Camel Corps. Create a separate British record when applying these modifiers to a unit shared with another faction rather than changing the shared unit.

### France modifiers

France is A tier. After the complete A-tier package, add +1 morale and reduce discipline one tier (`disciplined` to `normal`, `normal` to `low`, with `low` as the floor), leaving training unchanged. French militia and colonial units use the B-tier stat baseline instead of A tier, then receive the French additional morale and discipline reduction; do not apply and reverse A-tier modifiers. Colonial units are regular line troops unless otherwise specified: do not infer skirmisher status from the word `tirailleur`; apply -1 melee and -100 cost, and represent most of their historical disadvantage through older armament. France has no faction cost modifier, and roster breadth is its principal faction advantage.

### Prussia modifiers

Prussia is A tier. Core Prussian, Imperial German, and German colonial units use the complete A-tier package with no duplicate faction-wide skill bonuses. Regional German units use a B-tier baseline: early regional units receive +1 morale; mid regional units receive +1 morale and +1 discipline tier; late regional units receive +1 morale, +1 discipline tier, and +1 projectile accuracy tier. Pistols remain fixed at `magazine_rifle_bullet_c`. Prussia has no faction cost modifier.

### Ottoman modifiers

The Ottoman Empire is C tier. National Ottoman units receive -1 charge beyond the complete C-tier baseline, with no faction-wide cost modifier. Apply the charge penalty to the ordinary melee row first; lance cavalry then receives the universal +3 primary-lance charge relative to its adjusted sabre row. Nizamiye, Avcı, Bahriye Piyadesi, and Süvari use their stated regular-quality baselines; Redif and Müstahfız are militia quality; Hassa formations and the Ertuğrul Süvari Alayı are elite quality. Keep Bashi-Bazouks, Khedival/Egyptian troops, Georgian, Moroccan, Mahdist, Bulgarian, Serbian, and other auxiliary or mercenary records outside the main Ottoman custom-battle roster. Hassa Süvarisi and General ve Erkân-ı Harbiye are explicit pistol-and-sabre exceptions spanning all three eras; use the fixed pistol row and pistol animation mapping, keep them as light rather than missile cavalry, and do not periodize them. Their rider entries originated from carbine donors, so the experimental visible-weapon mapping requires an in-game visual check. The Ottoman standard bearer uses a dedicated Omani-compatible bearer mesh whose flag and head groups both render through the attachment material: preserve the donor flag's renderer-space aspect ratio in the lower-left attachment region, treat low texture U as the fly edge so the crescent opens and the star sits away from the pole, and retain the original donor pixels on every head island. The actual visible cloth is the 264-triangle component at renderer UV U 0.188–0.490 and V 0.694–0.990; keep the complete crescent and star inside that component and reject any device crossing its upper seam. Müstahfız must use the complete native `otto_jan_inf` Ottoman infantry model and texture mapping in both periods; the shared Nejd mesh produces unreliable faces even with its untouched donor attachment. Retain the native `per_rugbxx.texture` face attachment for both `turks` and `slave`, and do not create a faction-specific face repaint.

### Oman modifiers

Oman is D tier with no additional faction-wide stat or cost modifier. Omani regular infantry and Zanzibar regulars use regular-quality baselines; the Sultan's Palace Guard, Sultan's Horse Guard, and mounted command retinue are elite; Baluchi musketeers and Bedouin camelry use militia-quality baselines, with the camelry retaining impetuous discipline. Oman deliberately remains on single-shot weapons in the late period rather than receiving a magazine-rifle progression. The national regular line progresses from Pattern 1853 Enfield to Snider-Enfield to Martini-Henry Mk III; the Palace Guard instead receives the Peabody-Martini Model 1874 in the mid period and a Belgian Francotte Martini-Henry in the late period, while Zanzibar regulars retain their documented Snider-Enfields in the late period. Use readable Latin transliterations for Arabic formation names and retain English period and weapon descriptions. Early and mid organised Omani infantry uses `oma_standard_bearer`, built byte-for-byte from the proven visible Ottoman bearer mesh and mapped to the Omani guard body texture. Its attachment atlas preserves the donor faces unchanged and replaces only the proportionally mapped lower-left flag region with the period plain deep-red Muscat and Oman standard. Baluchi militia and late infantry do not receive it. Baluchi musketeers use the complete `moroccan_gunner` package: its mesh contains `arquebus_01`, `sword_01`, and seven native head variants, and its existing `golden` mapping pairs `moroccan_golden.texture` with `arab_gear_malib.texture`; correct the donor's erroneous axe animation slots to `MTW2_2HSwordsman` and `MTW2_2HSwordsman_Primary` without altering its textures. The Nizamiye line uses the complete `arab_sailors1` package with `koi_ask_1g_lod0.mesh`, `koi_ask_1g.texture`, and `afr_grfrgb.texture`, remapping its proven `venice` faction slot to `golden`; its mesh visibly contains the rifle, sabre, scabbard, turbans, and five native heads. Do not mix either donor's body and attachment textures or reuse the unreliable Nejd meshes. Palace Guard retains the untouched `oman_inf` mapping, and the native pistol rider retains its archived original texture. Do not install dedicated Omani face atlases or recolour face islands. Balush, Nizamiye, and Palace Guard infantry use their meshes' swords as secondary weapons: add +1 melee attack, retain the normal charge value, remove AP and `short_pike`, use the sword weapon token, and map `MTW2_2HSwordsman` with `MTW2_2HSwordsman_Primary`; Zanzibar infantry retains its bayonet row and pike animation. The Sultan's Horse Guard uses the same verified native Omani pistol-and-sabre rider as the command retinue in all three periods, with the fixed pistol projectile row, `class light`, and a total cost of 1400; it must not retain a carbine row or carbine card. The Bedouin cavalry record is camelry and its tactical card must visibly show the camel, Arabian rider, and matchlock carbine rather than a European horseman. African, Zulu, and Mahdist units remain auxiliary or mercenary records rather than national Omani custom-battle units. Dedicated melee infantry uses 80 men for organised formations or 96 for deliberately massed warbands; do not retain 100-man melee units.

### Netherlands modifiers

The Netherlands is B tier. National non-militia, non-colonial units receive +1 discipline tier, +1 melee attack, +1 defensive skill, and +200 cost beyond the B-tier baseline. Schutterij uses the militia-quality B-tier baseline without these national modifiers, while KNIL and other colonial units use their stated B-tier quality baseline without the national modifiers. Jagers are regular-quality skirmishers and receive only the standard +1 projectile role modifier. Dutch pistol cavalry uses the fixed pistol row and remains light or heavy cavalry; Dutch carbine cavalry is an intentional ranged role and uses `class missile`, the standard cavalry projectile penalty, a sabre secondary weapon, and stakes.

### Sweden–Norway modifiers

Sweden–Norway is A tier, except that units retain both their quality-default morale and quality-default discipline rather than receiving the A-tier +1 modifiers to those stats. Apply the remaining A-tier projectile, melee attack, charge, and defensive skill modifiers exactly once. National Swedish and Norwegian units receive +300 cost; the universal fixed cost for four-man general-and-staff units remains 200 and overrides this premium. Early-period placement does not make a firearm a muzzle-loader: purpose-built early breechloaders such as the Kammerlader use breechloader attributes and animations, while contemporary percussion muzzle-loaders use the muzzle-loading rules. Every weapon label must identify a specific service arm rather than a generic mechanism such as “percussion rifle.”

### Italy modifiers

Italy is B tier. Ordinary national line infantry, mobile militia, and non-general national cavalry receive -1 morale beyond the complete B-tier baseline. Elite, guard, specialist, volunteer, colonial, marine, engineer, and general-and-staff units retain their quality and role morale baselines. No other faction-wide stat or cost modifier applies, and the four-man general-and-staff unit costs 200 as usual.

### Qajar modifiers

Qajar Persia is D tier with no additional faction-wide cost modifier. Tofangchi-ye Mahalli are militia-quality local matchlock infantry and use a visible shamshir secondary weapon: add +1 melee attack beyond the completed D-tier militia value, retain normal charge, remove AP and `short_pike`, and use the verified sword animation pair. Sarbazan-e Nezam are regular line infantry and Negahbanan-e Shah are elite line infantry; both retain bayonets and use the full early, mid, and late weapon progression from Pattern 1853 Enfield rifle-musket through Mle 1853/67 Tabatiere conversion to Werndl-Holub M1867 rifle. Neshanzanan-e Shahi are regular-quality sharpshooters using the D-tier projectile result after the +2 sharpshooter role shift. Fowj-e Otrishi uses a complete B-tier regular baseline as a deliberate Austrian-trained subgroup and receives no D-tier penalties. Savaran-e Ashayeri uses a complete C-tier militia cavalry baseline, remains impetuous, and carries the verified regional lance and shamshir. Brigad-e Qazzaq uses a complete B-tier regular cavalry baseline with disciplined discipline; its Cossack lance receives the universal +3 primary charge and its distant LOD must be a mounted cavalry sprite. Gholaman-e Shah is elite D-tier pistol-and-shamshir cavalry using the fixed pistol row. Farmandeh va Setad is the universal four-man, 200-cost mounted light command unit and holds no ranged weapon. Tajik Hillmen (`afghan_militia`) remain a regional Persian campaign auxiliary but use the complete D-tier militia-skirmisher profile: 30 men, skirmisher spacing, +40 range, standard terrain/attributes, and the muzzle-loading animation; they do not inherit Afghanistan's national modifiers. All Sarbazan-e Nezam periods receive +1 shield beyond their completed D-tier line-infantry baseline. Afghan militia otherwise remains a regional campaign auxiliary; Kazakh, Kokand, Persian Marine, and other foreign records are not national Qajar custom-battle units.

Early and mid Sarbaz and Guard records use exactly one `qajargeneral` officer plus `qaj_standard_bearer`; their late records use only the officer. The Qajar bearer is a dedicated mesh made from the complete native `qaj_inf_1g` body, five heads, beards, and hats, replacing only the rifle group with the verified French pole-and-flag geometry. Its attachment atlas preserves `per_rugbxx.texture` outside the isolated flag region and shows a deep-red Qajar military banner with a large gold Lion-and-Sun device. Do not substitute `qajargeneral` or `qajar_gen` as a bearer: they are ordinary foot officer meshes and contain no flag geometry. Do not map Qajar body textures onto foreign bearer meshes.

### Afghanistan modifiers

Afghanistan is D tier. National Afghan units receive +1 morale, +1 melee attack, and +1 charge beyond the complete D-tier baseline, use `impetuous` discipline, and receive no cost modifier. The bonuses do not alter the D-tier projectile or defensive-skill penalties; Afghan equipment also remains generally older than the contemporary Qajar progression. Sword-equipped infantry receives the universal additional +1 melee attack after the Afghan modifier and uses the verified one- or two-handed sword animation supported by its mesh. Clone Tajik Hillmen for the national Afghan roster so these modifiers do not alter the existing Persian-tree `afghan_militia` auxiliary. Hide Herat Thunderers from ownership, eras, and recruitment without deleting its mesh, texture, or archived card, which remain available as donors. Afghan line gunpowder infantry use 40 men, while skirmishers and sharpshooters use 30; Lashkar-e Qawmi remains a 40-man exception; Lashkar-e Qawmi remains a jezail-and-pulwar warband in role and presentation. Afghan general-and-staff units receive +2 armour and +1 shield beyond the completed tier and faction baseline. Sipahsalar va Setad is the universal four-man, 200-cost mounted light command unit.

### Greece modifiers

Greece uses a modified C-tier baseline: apply the C-tier -1 projectile accuracy and -1 discipline tier, but do not apply its melee-attack penalty. Greek melee attack, charge, defensive skill, morale, and armour therefore remain at their completed B-tier quality and role defaults. Pistols remain fixed at `magazine_rifle_bullet_c`. Greece has no faction cost modifier. Early regular infantry uses a Greek-service Minié rifle-musket; older flintlock and percussion smoothbore arms are limited to militia or obsolete roles. Chassepot rifles do not appear in the early period.

### Russia modifiers

Russia is C tier. Russian core units receive -200 cost beyond the complete C-tier package and receive no additional morale modifier. Cossacks use militia-quality baselines. Siberian Riflemen form a complete early, mid, and late lineage; they receive -1 additional melee attack and a total Russian cost modifier of -300 rather than stacking -300 on top of the normal -200. The universal fixed cost of 200 for a four-man General-and-Staff unit overrides Russia's cost modifier. Regional and ethnic auxiliaries remain separate from the national core roster unless explicitly assigned their own treatment. The M1856/69 Krnka is an early-quality converted breechloader: use the rifle-musket baseline, reduced accuracy, 220 range, normal carried ammunition, and zero firing delay; represent its documented extraction and fouling problems through the deliberately low ballistic tier rather than an engine-unsafe firing-delay value. Georgian Militia remain a separate regional auxiliary and use militia-quality skirmisher rules without terrain bonuses.

### Austria–Hungary modifiers

Austria–Hungary is B tier. Its professional main-roster units receive +1 melee attack and +1 defensive skill beyond the complete B-tier baseline; charge, projectile accuracy, morale, discipline, armour value, and cost remain at their quality and role defaults. Apply this professional modifier once to Common Army, Kaiserjäger, Grenzinfanterie, Matrosenkorps, Landwehr, Honvéd, Bosnian-Herzegovinian infantry, and regular cavalry. Detached Polish, Bulgarian, Albanian, or other mercenary auxiliaries do not receive it merely because they can be recruited by Austria–Hungary. The Wänzl M1867 remains an early-quality converted breechloader using the rifle-musket baseline, while the purpose-built Werndl M1867 uses the rifle baseline.

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

### Union modifiers

The Union is B tier. State Volunteers are the mass early-period line infantry: they use the militia baseline and a custom-battle limit of 3, reflecting that the Civil War armies were overwhelmingly state-raised volunteer regiments rather than the small prewar Regular Army. The roster consolidates in the mid period into United States Regulars and National Guard lineages. National Guard, United States Colored Troops, Irish Brigade, Zouave Volunteers, and Union Volunteer Cavalry use militia baselines even when their historical identity or specialist role is distinguished. United States Regulars, United States Marines, and United States Dragoons use regular baselines. United States Sharpshooters are regular-quality sharpshooters: the role affects projectile accuracy and cost but does not make them elite in melee, armour, morale, or training. Indian Scouts and Indian Scout Cavalry are regional militia-quality auxiliaries, retain impetuous discipline, and may retain improved forest concealment as an explicit scouting-role exception. United States Colored Troops, the Irish Brigade, and Zouave Volunteers each have a limit of 1; Union Volunteer Cavalry has a limit of 2. Redundant legacy mercenary copies of the standardized Union frontier units have no Union custom-battle ownership. Indian Scout Cavalry uses the embedded Colt Army Model 1860 revolver-and-spear rider equipment; General and Staff uses the same named revolver with a sabre secondary. Early and mid national infantry uses usa_off_1g plus the verified usa_standard_bearer cloned from the complete francejunqshou model mapping: its existing portugala body texture visibly depicts a blue Union uniform and its existing portugala flag texture visibly depicts the United States flag. Late infantry uses only usa_off_1g. Artillery remains outside this infantry-and-cavalry balance pass.

### Confederate modifiers

The Confederacy is B tier. State Volunteers, State Guards, Louisiana Tigers, State Cavalry, and Virginia Cavalry use militia baselines and receive +1 melee attack, +1 charge, and +1 morale beyond that completed baseline. They remain low-discipline trained militia with militia defensive skill, projectile quality, and cost. Confederate States Regulars, Confederate States Marines, and Confederate Sharpshooters use regular baselines; the sharpshooter role changes projectile accuracy and cost only. State Volunteers and State Guards have custom-battle limit 3, State Cavalry has limit 2, and every other non-artillery formation has limit 1. The post-1865 roster is explicitly a conservative alternate-history continuation centred on decentralized state military institutions, not a claim about historical Confederate forces after the Civil War. State Cavalry is periodized as Maynard Model 1858, Spencer Model 1865, and Winchester Model 1892 carbine formations; all three use the native Confederate `usa_cav_1g` faction mapping to preserve its original faces, and Virginia Cavalry remains the separate early Sharps-carbine regional formation. The native csa_officer mapping is cloned from the complete nanjungeneralzhang entry. The verified Confederate foot bearer is `csa_standard_bearer`: it uses the complete native `csa_officer` body and its untouched `csa_captain` face/uniform material, and replaces only that mesh's separate carried-prop group with the verified `fra_qishou` pole-and-flag geometry mapped to the dedicated two-sided Confederate battle-flag atlas. Use it as the second officer for Confederate early and mid infantry; late infantry retains only `csa_officer`.

### Mexico modifiers

Mexico is C tier with no faction-specific modifiers. Guardia Nacional uses militia baselines; Infantería Federal, Cazadores, Carabineros, and Húsares use regular baselines; Levas Provinciales are militia-quality late provincial troops. Cazadores are 30-man skirmishers, while all other Mexican firearm infantry use 40 men. Sharps Model 1859 and Winchester Model 1866 carbine units use the early-breechloader rifle-musket baseline before cavalry and C-tier accuracy shifts. General y Estado Mayor is the universal four-man mounted light command unit with a named Lefaucheux Modelo 1858 revolver. Early and mid national infantry use `shk_off_1g` plus `mex_standard_bearer`; late infantry uses only `shk_off_1g`. The Mexican bearer uses the verified pole-and-flag bearer mesh with a dedicated red Mexican National Guard-style bearer texture that leaves the donor face, hands, hair, and equipment islands untouched, plus a two-sided green-white-red flag confined to the verified cloth UV footprint. Borrowed United States scouts, Brazilian cavalry, and French sailors are not national Mexican custom-battle formations. Artillery remains outside this infantry-and-cavalry pass.
### Brazil modifiers

Brazil is C tier. Brazilian militia-quality units receive an additional 100 cost reduction after the normal militia adjustment, for a total discount of 300 from the weapon-era infantry baseline; this represents their broad availability and does not alter professional-unit costs or custom-battle limits. Guarda Nacional and Voluntários da Pátria use militia baselines; Infantaria de Linha, Infantaria do Exército, Caçadores, Atiradores, Zuavos Baianos, Batalhão de Engenheiros, Marinheiros Imperiais, Cavalaria de Linha, and Dragões use regular baselines. Firearm infantry use 40 men; Caçadores, Atiradores, and Zuavos Baianos use 30. Zuavos Baianos are regular-quality early light infantry/skirmishers, not line infantry: apply the skirmisher accuracy and range modifiers, dispersed formation, and role-appropriate card while retaining the normal muzzle-loading animation. Early and mid infantry, including skirmishers, use `usa_off_1g` plus the verified `bra_standard_bearer`, cloned from the complete `francejunqshou` mapping that already supplies its Brazilian uniform and flag textures for `poland`; late infantry uses only `usa_off_1g`. Cavalaria de Linha uses an Enfield percussion cavalry carbine, mid Dragões use the early-breechloader-debuffed Spencer M1865, and late Dragões use a Mannlicher M1888-90 carbine; all genuine carbine cavalry are missile cavalry. General e Estado-Maior is the four-man mounted light command unit with a named Lefaucheux Mle 1858 revolver and the standard two-rank formation. No Brazilian lance lineage is created without a verified Brazilian-compatible lance rider mesh. Shared artillery remains outside this infantry-and-cavalry pass.
### Argentina modifiers

Argentina is C tier with no additional faction modifier. Infantería de Línea, Infantería del Ejército, Cazadores, Tiradores, Caballería de Línea, and Lanceros de Frontera use regular baselines; Guardia Nacional and Gauchos de la Frontera use militia baselines. Firearm line infantry use 40 men and skirmishers use 30. Cazadores and Tiradores are true skirmishers with dispersed formation and kneeling cards; muzzle-loading Cazadores retain the normal muzzle-loader animation, while later variants use `MTW2_Musket_SSK`. Caballería de Línea is carbine-armed missile cavalry in every period. Lanceros and Gauchos use the verified Argentine-compatible `gaucho_cav` lance mesh; therefore both receive the universal lance charge and cost additions, while Gauchos remain militia-quality and `impetuous`. Early and mid national infantry use one faction-appropriate officer plus `arg_standard_bearer`; late infantry uses only the officer. General y Estado Mayor is a four-man mounted light command unit with a named Lefaucheux Modelo 1858 revolver and standard two-rank formation. Foreign Mexican, Peruvian, Paraguayan, Uruguayan, French, and United States formations are excluded from Argentina's custom-battle roster; campaign mercenary recruitment remains distinct. Shared artillery remains outside this infantry-and-cavalry pass.
### Morocco modifiers

Morocco is D tier with no universal faction-wide bonus. Askar al-Nizam, Rifiyya, Fursan al-Makhzen, and the command unit use regular baselines; Makhzeniyya, Haraka Qabaliyya, Fursan al-Guich, and Hajjana use militia baselines; Abid al-Bukhari uses elite baselines. Rifiyya are 30-man skirmishers and use `impetuous`; all other firearm infantry use 40 men. Haraka Qabaliyya is a 96-man impetuous tribal melee formation. Fursan al-Guich and Haraka Qabaliyya receive +1 melee and +1 charge beyond their completed D-tier militia baselines. Fursan al-Guich uses the verified generic Arab sword-cavalry model because no compatible Moroccan lance rider exists; it receives no lance charge or cost premium. Hajjana is impetuous matchlock camelry. Makhzeniyya, Rifiyya, and Abid meshes visibly carry swords: apply the universal +1 sword-infantry melee modifier, remove AP and `short_pike`, and use their verified sword animations. Makhzeniyya and Abid al-Bukhari are non-uniformed traditional formations and receive +1 shield; neither is treated as bayonet infantry. Haraka Qabaliyya also receives +1 shield but no `spear` anti-cavalry attribute. Early and mid organized line infantry uses `fez_off_1g` plus `mor_standard_bearer`; late infantry uses only the officer. The Moroccan bearer uses the verified Ottoman bearer mesh with its original compatible face geometry, a dedicated reform-era body texture, and a red Moroccan flag with the green pentagram as the user-directed recognizable national-standard exception. Foreign Khedival, Ottoman, Zulu, Ethiopian, and generic sub-Saharan records are excluded from Morocco's national custom-battle roster. Shared artillery remains outside this pass.

## Siam balance

Siam (`cru`) is D tier with no additional faction-wide modifier. Apply the D-tier baseline before role or mesh-supported equipment adjustments. National firearm infantry uses 40 men, cavalry uses 24, and Mae Thap lae Khana is the universal four-man mounted light command unit in two ranks. Kong Asa and Thahan Ban are militia-quality; Thahan Bok, Thahan Bok Samai Mai, Thahan Ruea, Burmese and Vietnamese auxiliaries are regular-quality. The late Thahan Ma is carbine-armed missile cavalry using the early-breechloader ballistic penalty. Preserve visible secondary weapons: Quan Viet Phu Tro keeps its mesh-supported two-handed axe and receives the universal +1 melee adjustment, while bayonet statistics remain only on meshes that visibly support them. Keep Acehn mercenaries and the shared `viet_inf` record outside Siam's national custom-battle roster. Siam uses cloned national artillery records: bronze field cannon in early/mid, smoothbore cannon in mid/late, and mortar and Maxim in late; Gatling and 150 mm artillery remain unavailable. Cards must pass the universal canonical-background audit; the general card is passive mounted command art and carbine cavalry must visibly show both mount and carbine. The Siamese general model is a cuirassier and therefore retains cuirassier armour while remaining a four-man light command unit. Thahan Ruea marines are 40-man regular rifle infantry using `MTW2_Musket_SS`, regular rifle formation, and the regular projectile baseline. Burmese Irregulars are the roster's 30-man skirmishers: they receive skirmisher formation and the +1 projectile/range modifier, but retain `gunpowder_unit` with `MTW2_Fast_Arquebus_3` because their Pattern 1853 rifle-muskets are muzzle-loaders; never combine them with `MTW2_Musket_SSK`. Their tactical card must kneel, while the marine card must stand. Siam has no standard-bearer officer: the attempted custom bearer was rejected and removed. Do not restore `siam_standard_bearer` or substitute an armed infantry model. Thahan Ma Krabi is the early/mid 24-man regular sword-only cavalry lineage using the dedicated `siam_sword_cav` mapping derived from the genuine unarmoured mounted `sia_col_2g_lod0.mesh` rider. Its carbine geometry is physically removed from the dedicated derivative, and its sabre is the sole primary weapon, and it retains the verified mounted cavalry distant sprite. Never remap it to the foot-geometry `siam_general` model merely because that entry contains horse animation mappings; that makes the men stand on horseback. It receives no firearm, lance, shield, cuirassier, or faction bonus, and is replaced in late modernization by Thahan Ma carbine cavalry.

## Ethiopia balance

Ethiopia (`papal_states`) is D tier. Traditional national formations receive +1 morale and normally use `impetuous`; there is no universal projectile, armour, terrain, discipline, or European-quality bonus. The national roster is Č̣äwa, Fanno, Ras and Retinue, Näftäñña, Tigrayan Riflemen, Mehal Sefari, Oromo Horsemen, Shewan Horsemen, Mounted Näftäñña, and the three Ethiopian artillery clones. Mixed firearms are a defining feature represented by overlapping formations, not one homogenized weapon row or a linear Western modernization tree. Tigrayan Musketeers (Musket, Mixed Trade Patterns) are 30-man impetuous skirmishers in every period and retain normal muzzleloading animations. Näftäñña (Rifle-Musket, Mixed Patterns) are 40-man impetuous militia-quality infantry in every period using `gunpowder_unit`; Näftäñña (Rifle, Fusil Gras Mle 1874) overlap them from mid onward using the distinct `aby_inf_3g_gras` mapping with `MTW2_Musket_SS`. Mehal Sefari is a late central-host formation with another mixed pool of breech-loading rifles and better morale, but remains impetuous and only trained, not a Western-style regular or guard. Fanno retains the original 80-man javelin-and-mace `aby_grd_1g` model, while Č̣äwa retains the original 96-man javelin-and-spear `aby_spr_1g` model. Both are `class light` melee infantry with a one-volley javelin precursor, not heavy or dedicated missile infantry, cavalry 24, and Ras and Retinue four mounted men in two ranks. The command unit remains `class light`, not missile cavalry, but its verified `aby_grd_2g` mesh and model mapping carry a Gras Mle 1874 carbine as primary and a sword as secondary; retain the matching short carbine volley and sword melee rows. Mahdist, Dervish, Sudanese, generic African, and duplicate Ethiopian records retain mercenary or slave availability but have no Ethiopian national ownership or custom-battle eras. Ethiopian artillery is `eth_field_gun` early/mid, `eth_rifled_gun` mid/late, and `eth_maxim` late; never recruit the `sho_*` Japanese records for Ethiopia.


## Remaining mercenary and rebel balance

The residual land mercenary pool is balanced by the nearest national system rather than as a separate global tier. US frontier formations follow Union B-tier militia rules; Uruguay, Paraguay, Filibusters and Chile follow the relevant C-tier American rules; Portuguese auxiliaries follow a C-tier European baseline; Bhutanese, Burmese, Sikh, Siamese, Kashgar, Mongol and other Asian irregulars follow the appropriate D-tier regional rules; Khedival troops follow Ottoman C; Askari and Spahis follow the French colonial B baseline; Polish formations follow B-tier central-European rules; Georgian, Serbian and Bulgarian formations follow C-tier Russian/Ottoman regional rules; Bedouin irregulars follow Morocco D; Xhosa formations follow Zulu D including the Zulu melee, charge and morale modifiers; and Merchant Marine follows Britain A. Mercenary records receive no terrain or inherited special-attribute bonuses. The two mercenary ships remain outside land-unit balance.

Mercenary custom-battle presentation does not require period variants. Retain legacy Portuguese early/mid/late records only as hidden campaign compatibility records; use the non-periodized Fuzileiros Portugueses and Carabineiros Portugueses aliases for custom battle across all periods. Display names remain plain historical unit names, while weapon detail belongs in the name-first short description in the form `Name (specific weapon)`. Preserve the exact original Japanese irregular display names and all existing full descriptions.

For opaque legacy mercenary cards, never use broad reference-colour replacement. Work from the archived original and use border-seeded flood fill that requires strict neighbour-to-neighbour continuity, then inspect the complete 48x64 contact sheet. The broad normalization pass is known to erase pale uniforms, faces and horses and must not be reused.
