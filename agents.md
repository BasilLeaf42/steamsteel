# Universal Info

## Cautions
The existing systems are a patchwork, consider potential conflicts when making programmatic changes.

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

Note that the tow_steamsteel files are copied and overwrite the main directory ones!

## Balancing/Periodization:

1. Reloading animations must be set in "attributes" in conjunction with the entry of the "soldier" in the modeldb, specifically the primary weapon (first entry)*
For Infantry, they are:
Muzzle-loading - gunpowder_unit + 20 MTW2_Fast_Arquebus_3
Rifle - NO gunpowder_unit + 14 MTW2_Musket_SS
Magazine Rifle - NO gunpowder_unit + 20 MTW2_Fast_Arquebus_3 (reloading animation is thus disabled)

All modern line infantry should use 17 MTW2_Pike_primary for bayonets.

Cavalry: as the custom MTW2_Musket_SS breechloading animation cannot be used for them, their logic is much simpler
Muzzle-loading: gunpowder_unit
Breech-loading: NO gunpowder_unit

Artillery animations are set by the engine, just make sure the correct one is assigned.

2. Formations for infantry depend on unit type and period

Regular infantry (Muzzle-loading/early breechloaders/era 0):		1.2, 1.2, 1.2, 1.2, 3, square
Regular infantry (Rifle/era 1):			1.2, 1.2, 2.0, 2.4, 3, square
Regular infantry (Magazine Rifle/era 2): 		1.2, 1.4, 2.4, 2.8, 3, square
Skirmishers (all gunpowder): 				1.4, 1.8, 2.8, 3.6, 3, square
Cavalry:					2, 2, 4, 4, 3, square

3. Morale

Militia: 2-5 (default 3), low-normal (default low), untrained-trained (default trained)
Regular: 3-6 (default 4), normal-high (default normal), trained-disciplined (default trained)
Elite: 5-8 (default 6), normal-high (default high), disciplined

Note that non-line/western units may have impetuous

4. Projectile row:

In short, era 0 is for rifled_muskets/early breechloaders, era 1 is for rifles, and era 2 is for magazine rifles. However obselecence is entirely possible.

Projectiles: The tiering system uses the designations c, b, a, and s to represent ascending levels of troop training and role proficiency, which directly correspond to increased projectile accuracy. The tiers largely correspond to Militia, Regular, Elite, and Sharpshoopers/Skirmishers.

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

5. Melee
Attack (militia): 2-4 (default 3), 2-4 (charge, default 2)
Attack (regular): 4-6 (default 5), 3-5 (charge, default 3)
Attack (elite): 5-8 (default 7), 4-6 (charge, default 4)

Armour (militia): 3, 2-4 (default 2), 0, leather
Armour (regular): 3, 3-5 (default 3), 0, leather
Armour (elite): 3, 4-6 (default 4), 0, leather
Armour (Cavalry): 4, 3-6 (default 4), 0, leather
Armour (Cuirassiers): 7, 4-6 (default 5), 0, armoured 

For non-western style units, ask for clarification

6. Standard stats for gunpowder inf and cav
attributes       free_upkeep_unit, sea_faring, hide_forest, gunpowder_unit (if applicable), gunmen, start_not_skirmishing, cannot_skirmish
stat_ground      0, 0, 0, 0

7. Cost rules
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