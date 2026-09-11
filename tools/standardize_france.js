const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const canonicalEdu = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const runtimeEdu = path.join(root, 'data/export_descr_unit.txt');
const modeldbPath = path.join(root, 'data/unit_models/battle_models.modeldb');
const locPath = path.join(root, 'data/text/export_units.txt');
const soundPath = path.join(root, 'data/export_descr_sounds_units_voice.txt');
const mercenaryPaths = [
  path.join(root, 'data/world/maps/campaign/camp_steamsteel/descr_mercenaries.txt'),
  path.join(root, 'data/world/maps/campaign/imperial_campaign/descr_mercenaries.txt'),
];

const nl = '\n';

function cost(total, limit = 1) {
  return `3, ${total}, ${Math.round(total / 3)}, 100, 100, ${total}, ${limit}, ${Math.round(total / 3)}`;
}

const eraData = {
  early: { era: 0, formation: '1.2, 1.2, 1.2, 1.2, 3, square', damage: 37, range: 220, ammo: 35, smoke: 'musket_shot_set', fireDelay: -100000 },
  mid:   { era: 1, formation: '1.2, 1.2, 2.0, 2.4, 3, square', damage: 20, range: 240, ammo: 35, smoke: 'musket_shot_set', fireDelay: 0 },
  high:  { era: 2, formation: '1.2, 1.4, 2.4, 2.8, 3, square', damage: 13, range: 260, ammo: 40, smoke: 'smokeless_shot_set', fireDelay: 0 },
};

const qualityData = {
  // National troops use A tier, plus the French +1 morale and -1 discipline.
  // Militia and colonial troops start directly from B tier instead.
  militia: { melee: 3, charge: 2, defence: 2, morale: 4, discipline: 'low', training: 'trained' },
  regular: { melee: 6, charge: 4, defence: 4, morale: 6, discipline: 'normal', training: 'trained' },
  elite:   { melee: 8, charge: 5, defence: 5, morale: 8, discipline: 'normal', training: 'highly_trained' },
  colonial:{ melee: 4, charge: 3, defence: 3, morale: 5, discipline: 'low', training: 'trained' },
};

function infantry(u) {
  const e = eraData[u.period];
  const q = qualityData[u.quality];
  const attrs = ['free_upkeep_unit', 'sea_faring', 'hide_forest'];
  if (u.muzzle) attrs.push('gunpowder_unit');
  attrs.push('gunmen', 'start_not_skirmishing', 'cannot_skirmish');
  if (u.period === 'high') attrs.push('stakes');
  const formation = u.skirmisher ? '1.4, 1.8, 2.8, 3.6, 3, square' : e.formation;
  const range = (u.range || e.range) + (u.skirmisher ? 40 : 0);
  const smoke = u.smoke || e.smoke;
  return [
    `type             ${u.type}`,
    `dictionary       ${u.type} ; ${u.label} (${u.period === 'high' ? 'Late' : u.period[0].toUpperCase() + u.period.slice(1)}; ${u.weaponClass}, ${u.weapon})`,
    'category         infantry',
    'class            missile',
    'voice_type       Light',
    'accent           france',
    'banner faction   main_infantry',
    'banner holy      crusade',
    `soldier          ${u.type}, 40, 0, 1.2`,
    'officer          swe_off_1g',
    ...(u.period !== 'high' ? ['officer          francejunqshou'] : []),
    `attributes       ${attrs.join(', ')}`,
    `formation        ${formation}`,
    'stat_health      1, 0',
    `stat_pri         ${u.damage || e.damage}, 0, ${u.projectile}, ${range}, ${u.ammo || e.ammo}, missile, missile_gunpowder, piercing, none, ${smoke}, 0, -999`,
    'stat_pri_attr    ap',
    `stat_sec         ${q.melee}, ${q.charge}, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1.2`,
    'stat_sec_attr    short_pike, ap',
    `stat_pri_armour  3, ${q.defence}, 0, leather`,
    'stat_sec_armour  0, 0, flesh',
    'stat_heat        0',
    'stat_ground      0, 0, 0, 0',
    `stat_mental      ${q.morale}, ${q.discipline}, ${q.training}`,
    'stat_charge_dist 40',
    `stat_fire_delay  ${e.fireDelay}`,
    'stat_food        60, 300',
    `stat_cost        ${cost(u.cost, u.limit || 1)}`,
    'ownership        france, slave',
    `era ${e.era}            france`,
  ].join(nl);
}

function cavalry(u) {
  const isCarbine = u.armament === 'carbine';
  const attrs = ['free_upkeep_unit', 'sea_faring', 'hide_forest', 'can_withdraw', 'guncavalry', 'gunmen', 'start_not_skirmishing', 'cannot_skirmish'];
  if (u.muzzle) attrs.push('gunpowder_unit');
  if (isCarbine) attrs.push('stakes');
  if (u.general) attrs.push('general_unit', 'command');
  const primary = isCarbine
    ? `${u.damage}, 2, ${u.projectile}, ${u.range}, ${u.ammo}, missile, missile_gunpowder, piercing, none, ${u.smoke}, 25, 1`
    : '20, 4, magazine_rifle_bullet_c, 60, 15, missile, missile_gunpowder, piercing, none, musket_shot_set, 25, 1';
  const armour = u.cuirassier ? `7, ${u.defence}, 0, metal` : `4, ${u.defence}, 0, leather`;
  const eras = u.period ? [`era ${eraData[u.period].era}            france`] : ['era 0            france', 'era 1            france', 'era 2            france'];
  return [
    `type             ${u.type}`,
    `dictionary       ${u.type} ; ${u.label}${u.period ? ` (${u.period === 'high' ? 'Late' : u.period[0].toUpperCase() + u.period.slice(1)}; ${u.weapon})` : ` (${u.weapon})`}`,
    'category         cavalry',
    `class            ${u.className}`,
    'voice_type       Heavy',
    'accent           france',
    'banner faction   main_cavalry',
    'banner holy      crusade_cavalry',
    `soldier          ${u.type}, ${u.general ? 4 : 24}, 0, 1`,
    'officer          swe_off_1g',
    `mount            ${u.mount || 'hussar'}`,
    'mount_effect     elephant -4, camel -4',
    `attributes       ${attrs.join(', ')}`,
    `formation        2, 2, 4, 4, ${u.general ? 2 : 3}, square`,
    'stat_health      1, 0',
    `stat_pri         ${primary}`,
    'stat_pri_attr    ap',
    `stat_sec         ${u.melee}, ${u.charge}, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1`,
    'stat_sec_attr    ap',
    `stat_pri_armour  ${armour}`,
    'stat_sec_armour  0, 0, flesh',
    'stat_heat        0',
    'stat_ground      0, 0, 0, 0',
    `stat_mental      ${u.morale}, ${u.discipline}, ${u.training}`,
    'stat_charge_dist 45',
    'stat_fire_delay  -20000',
    'stat_food        60, 300',
    `stat_cost        ${cost(u.cost, 1)}`,
    'ownership        france, slave',
    ...eras,
  ].join(nl);
}

const infantryUnits = [
  ['fra_fusiliers_early','Fusiliers','early','regular','Fusil d’infanterie modèle 1857','Rifle-Musket','rifled_musket_bullet_a',1200,true,false],
  ['fra_fusiliers_mid','Fusiliers','mid','regular','Fusil modèle 1866 Chassepot','Rifle','rifle_bullet_a',1500,false,false],
  ['fra_fusiliers_high','Fusiliers','high','regular','Fusil modèle 1886 Lebel','Magazine Rifle','magazine_rifle_bullet_a',1800,false,false],
  ['fra_garde_mobile_early','Garde mobile','early','militia','Fusil modèle 1857','Rifle-Musket','rifled_musket_bullet_c',1000,true,false],
  ['fra_garde_nationale_mid','Garde nationale','mid','militia','Fusil modèle 1853/67 Tabatière','Rifle','rifle_bullet_c',1300,false,false],
  ['fra_zouaves_early','Zouaves','early','elite','Fusil de voltigeur modèle 1857','Rifle-Musket','rifled_musket_bullet_s',1400,true,false],
  ['fra_zouaves_mid','Zouaves','mid','elite','Fusil modèle 1866 Chassepot','Rifle','rifle_bullet_s',1700,false,false],
  ['fra_zouaves_high','Zouaves','high','elite','Fusil modèle 1884 Kropatschek','Magazine Rifle','magazine_rifle_bullet_s',2000,false,false],
  ['fra_chasseurs_early','Chasseurs à pied','early','regular','Carabine de chasseurs modèle 1859','Rifle-Musket','rifled_musket_bullet_s',1200,true,true],
  ['fra_chasseurs_mid','Chasseurs à pied','mid','regular','Fusil modèle 1866 Chassepot','Rifle','rifle_bullet_s',1500,false,true],
  ['fra_chasseurs_high','Chasseurs à pied','high','regular','Fusil modèle 1886 Lebel','Magazine Rifle','magazine_rifle_bullet_s',1800,false,true],
  ['fra_guard_grenadiers_early','Grenadiers de la Garde impériale','early','elite','Fusil modèle 1857','Rifle-Musket','rifled_musket_bullet_s',1400,true,false],
  ['fra_guard_grenadiers_mid','Grenadiers de la Garde impériale','mid','elite','Fusil modèle 1866 Chassepot','Rifle','rifle_bullet_s',1700,false,false],
  ['fra_legion_early','Légion étrangère','early','elite','Fusil modèle 1853 T','Rifle-Musket','rifled_musket_bullet_s',1400,true,false],
  ['fra_legion_mid','Légion étrangère','mid','elite','Fusil modèle 1866 Chassepot','Rifle','rifle_bullet_s',1700,false,false],
  ['fra_legion_high','Légion étrangère','high','elite','Fusil modèle 1886 Lebel','Magazine Rifle','magazine_rifle_bullet_s',2000,false,false],
  ['fra_marins_early','Fusiliers marins','early','regular','Fusil de marine modèle 1857','Rifle-Musket','rifled_musket_bullet_a',1200,true,false],
  ['fra_marins_mid','Fusiliers marins','mid','regular','Fusil modèle 1874 Gras','Rifle','rifle_bullet_a',1500,false,false],
  ['fra_marins_high','Fusiliers marins','high','regular','Fusil de marine modèle 1878 Kropatschek','Magazine Rifle','magazine_rifle_bullet_a',1800,false,false],
  ['fra_senegalais_early','Tirailleurs sénégalais','early','colonial','Fusil modèle 1842 T','Rifle-Musket','rifled_musket_bullet_b',1100,true,false],
  ['fra_senegalais_mid','Tirailleurs sénégalais','mid','colonial','Fusil modèle 1853/67 Tabatière','Rifle','rifle_bullet_b',1400,false,false],
  ['fra_senegalais_high','Tirailleurs sénégalais','high','colonial','Fusil modèle 1874 Gras','Rifle','rifle_bullet_b',1400,false,false],
  ['fra_indochinois_high','Tirailleurs indochinois','high','colonial','Fusil modèle 1874 Gras','Rifle','rifle_bullet_b',1400,false,false],
].map(([type,label,period,quality,weapon,weaponClass,projectile,cost,muzzle,skirmisher]) => {
  const obsoleteRifle = period === 'high' && weapon.includes('Gras');
  return {
    type,label,period,quality,weapon,weaponClass,projectile,cost,muzzle,skirmisher,
    damage: obsoleteRifle ? 20 : undefined,
    range: obsoleteRifle ? 240 : undefined,
    ammo: obsoleteRifle ? 35 : undefined,
    smoke: weapon.includes('Kropatschek') || obsoleteRifle ? 'musket_shot_set' : undefined,
  };
});

// Written out below to keep the special cavalry combinations explicit.
const cav = [
  {type:'fra_cuirassiers', label:'Cuirassiers', weapon:'Revolver Lefaucheux modèle 1858 et sabre', className:'heavy', armament:'pistol', melee:8, charge:5, defence:6, morale:8, discipline:'normal', training:'highly_trained', cost:1700, cuirassier:true},
  {type:'fra_hussards', label:'Hussards', weapon:'Revolver Lefaucheux modèle 1858 et sabre', className:'light', armament:'pistol', melee:6, charge:4, defence:5, morale:6, discipline:'normal', training:'trained', cost:1200},
  {type:'fra_chasseurs_cheval', label:'Chasseurs à cheval', weapon:'Revolver Lefaucheux modèle 1858 et sabre', className:'light', armament:'pistol', melee:6, charge:4, defence:5, morale:6, discipline:'normal', training:'trained', cost:1200},
  {type:'fra_carabiniers_early', label:'Carabiniers', period:'early', weapon:'Carabine de cavalerie modèle 1853', className:'heavy', armament:'carbine', melee:6, charge:4, defence:5, morale:6, discipline:'normal', training:'trained', cost:1400, muzzle:true, damage:37, projectile:'rifled_musket_carbine_bullet_b', range:200, ammo:35, smoke:'musket_shot_set'},
  {type:'fra_carabiniers_mid', label:'Carabiniers', period:'mid', weapon:'Carabine modèle 1867 Tabatière', className:'heavy', armament:'carbine', melee:6, charge:4, defence:5, morale:6, discipline:'normal', training:'trained', cost:1700, damage:20, projectile:'rifle_carbine_bullet_b', range:220, ammo:35, smoke:'musket_shot_set'},
  {type:'fra_carabiniers_high', label:'Carabiniers', period:'high', weapon:'Mousqueton de cavalerie modèle 1890 Berthier', className:'heavy', armament:'carbine', melee:6, charge:4, defence:5, morale:6, discipline:'normal', training:'trained', cost:2000, damage:13, projectile:'magazine_rifle_carbine_bullet_b', range:240, ammo:40, smoke:'smokeless_shot_set'},
  {type:'fra_spahis_early', label:'Spahis', period:'early', weapon:'Carabine de cavalerie modèle 1857', className:'light', armament:'carbine', melee:4, charge:3, defence:4, morale:5, discipline:'low', training:'trained', cost:1300, muzzle:true, damage:37, projectile:'rifled_musket_carbine_bullet_c', range:200, ammo:35, smoke:'musket_shot_set'},
  {type:'fra_spahis_mid', label:'Spahis', period:'mid', weapon:'Carabine modèle 1866 Chassepot', className:'light', armament:'carbine', melee:4, charge:3, defence:4, morale:5, discipline:'low', training:'trained', cost:1600, damage:20, projectile:'rifle_carbine_bullet_c', range:220, ammo:35, smoke:'musket_shot_set'},
  {type:'fra_spahis_high', label:'Spahis', period:'high', weapon:'Carabine modèle 1874 Gras', className:'light', armament:'carbine', melee:4, charge:3, defence:4, morale:5, discipline:'low', training:'trained', cost:1600, damage:20, projectile:'rifle_carbine_bullet_c', range:220, ammo:35, smoke:'musket_shot_set'},
  {type:'fra_general_staff', label:'Général et état-major', weapon:'Revolver Lefaucheux modèle 1858 et sabre', className:'heavy', armament:'pistol', melee:8, charge:5, defence:5, morale:8, discipline:'normal', training:'highly_trained', cost:200, general:true},
];

const sapeurs = `type             fra_guard
dictionary       fra_guard ; Sapeurs
category         infantry
class            missile
voice_type       Heavy
accent           france
banner faction   main_cavalry
banner holy      crusade
soldier          fra_guard, 16, 0, 1.2
officer          swe_off_1g
attributes       free_upkeep_unit, sea_faring, hide_forest, hide_improved_forest, can_withdraw, incendiary, start_not_skirmishing, cannot_skirmish, stakes, very_hardy
formation        1.4, 1.8, 2.8, 3.6, 3, square
stat_health      1, 0
stat_pri         7, 3, greek_fire, 60, 2, missile, missile_gunpowder, slashing, none, 25, 1
stat_pri_attr    ap, bp
stat_sec         8, 5, no, 0, 0, melee, melee_blade, blunt, mace, 25, 1
stat_sec_attr    ap, short_pike
stat_pri_armour  7, 5, 0, leather
stat_sec_armour  0, 0, flesh
stat_heat        0
stat_ground      1, 1, 1, 1
stat_mental      9, disciplined, highly_trained
stat_charge_dist 30
stat_fire_delay  0
stat_food        60, 300
stat_cost        3, 1500, 500, 200, 160, 1500, 1, 500
ownership        france, slave
era 1            france
era 2            france`;

function compatibilityAlias(block, oldType, oldSoldier) {
  return block
    .replace(/^type\s+.*$/m, `type             ${oldType}`)
    .replace(/^dictionary\s+\S+/m, `dictionary       ${oldType}`)
    .replace(/^soldier\s+\S+,/m, `soldier          ${oldSoldier},`)
    .replace(/^ownership\s+.*$/m, 'ownership        slave')
    .replace(/^era [012]\s+france\n?/gm, '')
    .trimEnd();
}

// Hidden compatibility records preserve campaign starts, sounds, and ancillary
// files that still refer to the patchwork internal names. They have no era rows,
// so only the standardized early/mid/high records appear in custom battle.
const compatibilityRecords = [
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_zouaves_early')), 'us_zouave_france', 'us_zouave'),
  compatibilityAlias(cavalry(cav.find(u => u.type === 'fra_carabiniers_high')), 'fra_cav', 'fra_cav'),
  compatibilityAlias(cavalry(cav.find(u => u.type === 'fra_carabiniers_early')), 'fra_cav2', 'fra_cav2'),
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_fusiliers_high')), 'fra_pith', 'fra_pith'),
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_fusiliers_high')), 'fra_ww1_inf', 'fra_ww1_inf'),
  compatibilityAlias(cavalry(cav.find(u => u.type === 'fra_chasseurs_cheval')), 'fra_carbs', 'fra_carbs'),
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_marins_mid')), 'fra_sailors', 'fra_sailors'),
  compatibilityAlias(cavalry(cav.find(u => u.type === 'fra_cuirassiers')), 'fra_hus_2', 'bol_hussar'),
  compatibilityAlias(cavalry(cav.find(u => u.type === 'fra_general_staff')), 'fra_hussar', 'fra_hussar'),
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_senegalais_early')), 'fra_blacks_fr', 'fra_blacks1'),
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_garde_mobile_early')), 'fra_rec', 'fra_rec'),
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_legion_mid')), 'fra_inf_fr', 'fra_inf'),
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_legion_high')), 'fra_inf_fl', 'fra_inf_sc'),
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_fusiliers_early')), 'fra_line_inf', 'fra_line_in2'),
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_chasseurs_mid')), 'fra_chass', 'uru_inf1'),
  compatibilityAlias(infantry(infantryUnits.find(u => u.type === 'fra_indochinois_high')), 'fra_vietna_france', 'fra_vietna'),
  compatibilityAlias(cavalry(cav.find(u => u.type === 'fra_spahis_mid')), 'merc_fra_for_cav', 'moroccan_camel_roy')
    .replace(/^attributes\s+(.+)$/m, 'attributes       $1, mercenary_unit'),
];

const franceBlock = [
  '; ============================================================================',
  '; France (france) — standardized infantry and cavalry',
  '; ============================================================================',
  ...infantryUnits.map(infantry),
  sapeurs,
  ...cav.map(cavalry),
  '; Legacy internal-name compatibility (not assigned to custom-battle eras)',
  ...compatibilityRecords,
].join(`${nl}${nl}`) + nl + nl;

let edu = fs.readFileSync(canonicalEdu, 'utf8').replace(/\r\n/g, '\n');
const standardizedTitle = '; France (france) — standardized infantry and cavalry';
const standardizedTitleAt = edu.indexOf(standardizedTitle);
let start = standardizedTitleAt >= 0 ? edu.lastIndexOf('; ============================================================================', standardizedTitleAt) : edu.indexOf('type             us_zouave_france');
const prussiaTitleAt = Math.max(
  edu.indexOf('; Prussia (hre) — standardized infantry and cavalry', start),
  edu.indexOf('; Prussia (hre) — infantry and cavalry', start),
);
const end = prussiaTitleAt >= 0 ? edu.lastIndexOf('; ============================================================================', prussiaTitleAt) : -1;
if (start < 0 || end < 0) throw new Error('Could not locate the legacy French EDU block');
edu = edu.slice(0, start) + franceBlock + edu.slice(end);
const eduOut = edu.replace(/\r?\n/g, '\r\n');
fs.writeFileSync(canonicalEdu, eduOut, 'utf8');
fs.writeFileSync(runtimeEdu, eduOut, 'utf8');

const edbPaths = [
  path.join(root, 'data/tow_steamsteel/export_descr_buildings.txt'),
  path.join(root, 'data/export_descr_buildings.txt'),
];
const recruitmentMap = {
  us_zouave_france:'fra_zouaves_early',
  fra_cav:'fra_carabiniers_high',
  fra_pith:'fra_fusiliers_high',
  fra_ww1_inf:'fra_fusiliers_high',
  fra_carbs:'fra_chasseurs_cheval',
  fra_sailors:'fra_marins_mid',
  fra_hus_2:'fra_cuirassiers',
  fra_blacks_fr:'fra_senegalais_early',
  fra_rec:'fra_garde_mobile_early',
  fra_inf_fr:'fra_legion_mid',
  fra_inf_fl:'fra_legion_high',
  fra_line_inf:'fra_fusiliers_early',
  fra_chass:'fra_chasseurs_mid',
  fra_vietna_france:'fra_indochinois_high',
  merc_fra_for_cav:'fra_spahis_mid',
  fra_hussar:'fra_general_staff',
};
for (const edbPath of edbPaths) {
  let edb = fs.readFileSync(edbPath, 'utf8');
  for (const [oldName,newName] of Object.entries(recruitmentMap)) {
    edb = edb.replace(new RegExp(`"${oldName}"`, 'g'), `"${newName}"`);
  }
  fs.writeFileSync(edbPath, edb.replace(/\r\n/g, '\n'), 'utf8');
}
for (const mercenaryPath of mercenaryPaths) {
  let mercenaries = fs.readFileSync(mercenaryPath, 'utf8');
  mercenaries = mercenaries.replace(/(unit\s+merc_fra_for_cav\s+exp\s+\d+\s+cost\s+)\d+/g, (_,prefix) => `${prefix}1600`);
  fs.writeFileSync(mercenaryPath, mercenaries, 'utf8');
}

function extractModelEntry(text, name) {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const startIndex = lines.findIndex(line => line === `${name.length} ${name} `);
  if (startIndex < 0) throw new Error(`Missing modeldb donor ${name}`);
  let endIndex = startIndex;
  while (endIndex < lines.length && !/^16 -0\.090000004 /.test(lines[endIndex])) endIndex++;
  if (endIndex >= lines.length) throw new Error(`Could not find end of modeldb donor ${name}`);
  return lines.slice(startIndex, endIndex + 1).join('\n');
}

function cloneModel(text, donor, name, mode) {
  let entry = extractModelEntry(text, donor);
  entry = entry.replace(`${donor.length} ${donor} `, `${name.length} ${name} `);
  if (mode === 'musket') {
    entry = entry.replace(/20 MTW2_Fast_Arquebus_3 9 MTW2_Pike /, '14 MTW2_Musket_SS 9 MTW2_Pike ');
  } else if (mode === 'skirmisher') {
    entry = entry.replace(/(?:20 MTW2_Fast_Arquebus_3|14 MTW2_Musket_SS) 9 MTW2_Pike /, '15 MTW2_Musket_SSK 9 MTW2_Pike ');
  } else if (mode === 'fast') {
    entry = entry.replace(/14 MTW2_Musket_SS 9 MTW2_Pike /, '20 MTW2_Fast_Arquebus_3 9 MTW2_Pike ');
  } else if (mode === 'pistol_sword_from_sword') {
    entry = entry.replace('13 MTW2_HR_Sword 0 \n2 \n18 MTW2_Sword_Primary 14 fs_test_shield \n0 ', '14 MTW2_HR_Pistol 13 MTW2_HR_Sword \n1 \n22 MTW2_HR_Pistol_Primary \n1 \n18 MTW2_Sword_Primary ');
  } else if (mode === 'pistol_sword_from_spear') {
    entry = entry.replace('14 MTW2_HR_Pistol 13 MTW2_HR_Spear ', '14 MTW2_HR_Pistol 13 MTW2_HR_Sword ')
                 .replace('21 MTW2_HR_spear_Primary ', '18 MTW2_Sword_Primary ');
  }
  return entry;
}

const modelClones = [
  ['fra_line_in2','fra_fusiliers_early','fast'], ['fra_line_in2','fra_fusiliers_mid','musket'], ['fra_pith','fra_fusiliers_high','fast'],
  ['fra_rec','fra_garde_mobile_early','fast'], ['fra_rec','fra_garde_nationale_mid','musket'],
  ['us_zouave','fra_zouaves_early','fast'], ['us_zouave','fra_zouaves_mid','musket'], ['us_zouave','fra_zouaves_high','fast'],
  ['uru_inf1','fra_chasseurs_early','fast'], ['uru_inf1','fra_chasseurs_mid','skirmisher'], ['uru_inf1','fra_chasseurs_high','skirmisher'],
  ['fra_ww1_inf','fra_guard_grenadiers_early','fast'], ['fra_ww1_inf','fra_guard_grenadiers_mid','musket'],
  ['fra_inf','fra_legion_early','fast'], ['fra_inf','fra_legion_mid','musket'], ['fra_inf_sc','fra_legion_high','fast'],
  ['fra_sailors','fra_marins_early','fast'], ['fra_sailors','fra_marins_mid','musket'], ['fra_sailors','fra_marins_high','fast'],
  ['fra_blacks1','fra_senegalais_early','fast'], ['fra_blacks1','fra_senegalais_mid','musket'], ['fra_blacks1','fra_senegalais_high','musket'],
  ['fra_vietna','fra_indochinois_high','musket'],
  ['bol_hussar','fra_cuirassiers',null], ['fra_carbs','fra_hussards','pistol_sword_from_sword'], ['fra_carbs','fra_chasseurs_cheval','pistol_sword_from_sword'],
  ['fra_cav2','fra_carabiniers_early',null], ['fra_cav2','fra_carabiniers_mid',null], ['fra_cav','fra_carabiniers_high',null],
  ['moroccan_camel_roy','fra_spahis_early',null], ['moroccan_camel_roy','fra_spahis_mid',null], ['moroccan_camel_roy','fra_spahis_high',null],
  ['fra_hussar','fra_general_staff','pistol_sword_from_spear'],
];

let modeldb = fs.readFileSync(modeldbPath, 'utf8').replace(/\r\n/g, '\n');
const missingClones = modelClones.filter(([,name]) => !new RegExp(`^${name.length} ${name} $`, 'm').test(modeldb));
if (missingClones.length) {
  const header = modeldb.match(/^(22 serialization::archive 3 0 0 0 0 )(\d+)( 0 0 )/);
  if (!header) throw new Error('Could not parse modeldb header count');
  modeldb = modeldb.replace(header[0], `${header[1]}${Number(header[2]) + missingClones.length}${header[3]}`);
  modeldb = modeldb.trimEnd() + '\n' + missingClones.map(([donor,name,mode]) => cloneModel(modeldb, donor, name, mode)).join('\n') + '\n';
}
fs.writeFileSync(modeldbPath, modeldb.replace(/\r?\n/g, '\r\n'), 'utf8');

const descriptions = {
  fra_fusiliers_early:['Fusiliers (Early)','Regular French line infantry armed with the Fusil d’infanterie modèle 1857.','Fusiliers (Early; Rifle-Musket, Fusil d’infanterie modèle 1857)'],
  fra_fusiliers_mid:['Fusiliers (Mid)','Regular French line infantry armed with the breech-loading Chassepot.','Fusiliers (Mid; Rifle, Fusil modèle 1866 Chassepot)'],
  fra_fusiliers_high:['Fusiliers (Late)','Regular French line infantry armed with the smokeless-powder Lebel.','Fusiliers (Late; Magazine Rifle, Fusil modèle 1886 Lebel)'],
  fra_garde_mobile_early:['Garde mobile (Early)','Poorly trained French reserve infantry whose enthusiasm exceeds their battlefield steadiness.','Garde mobile (Early; Rifle-Musket, Fusil modèle 1857)'],
  fra_garde_nationale_mid:['Garde nationale (Mid)','French citizen infantry equipped with converted Tabatière rifles for local and emergency defence.','Garde nationale (Mid; Rifle, Fusil modèle 1853/67 Tabatière)'],
  fra_zouaves_early:['Zouaves (Early)','Elite French assault infantry armed with the Fusil de voltigeur modèle 1857.','Zouaves (Early; Rifle-Musket, Fusil de voltigeur modèle 1857)'],
  fra_zouaves_mid:['Zouaves (Mid)','Elite French assault infantry armed with the Chassepot.','Zouaves (Mid; Rifle, Fusil modèle 1866 Chassepot)'],
  fra_zouaves_high:['Zouaves (Late)','Elite French assault infantry issued the limited-service repeating Kropatschek.','Zouaves (Late; Magazine Rifle, Fusil modèle 1884 Kropatschek)'],
  fra_chasseurs_early:['Chasseurs à pied (Early)','Regular light infantry trained to screen and skirmish ahead of the French line.','Chasseurs à pied (Early; Rifle-Musket, Carabine de chasseurs modèle 1859)'],
  fra_chasseurs_mid:['Chasseurs à pied (Mid)','Regular light infantry equipped with the Chassepot.','Chasseurs à pied (Mid; Rifle, Fusil modèle 1866 Chassepot)'],
  fra_chasseurs_high:['Chasseurs à pied (Late)','Regular light infantry equipped with the Lebel.','Chasseurs à pied (Late; Magazine Rifle, Fusil modèle 1886 Lebel)'],
  fra_guard_grenadiers_early:['Grenadiers de la Garde impériale (Early)','Elite grenadiers of Napoleon III’s Imperial Guard.','Grenadiers de la Garde impériale (Early; Rifle-Musket, Fusil modèle 1857)'],
  fra_guard_grenadiers_mid:['Grenadiers de la Garde impériale (Mid)','Elite grenadiers of the Imperial Guard armed with Chassepot rifles.','Grenadiers de la Garde impériale (Mid; Rifle, Fusil modèle 1866 Chassepot)'],
  fra_legion_early:['Légion étrangère (Early)','Elite foreign volunteers in French service armed with converted percussion rifles.','Légion étrangère (Early; Rifle-Musket, Fusil modèle 1853 T)'],
  fra_legion_mid:['Légion étrangère (Mid)','Elite foreign volunteers in French service armed with Chassepot rifles.','Légion étrangère (Mid; Rifle, Fusil modèle 1866 Chassepot)'],
  fra_legion_high:['Légion étrangère (Late)','Elite foreign volunteers in French service armed with Lebel rifles.','Légion étrangère (Late; Magazine Rifle, Fusil modèle 1886 Lebel)'],
  fra_marins_early:['Fusiliers marins (Early)','French naval infantry armed with the marine model 1857 rifle.','Fusiliers marins (Early; Rifle-Musket, Fusil de marine modèle 1857)'],
  fra_marins_mid:['Fusiliers marins (Mid)','French naval infantry armed with the metallic-cartridge Gras.','Fusiliers marins (Mid; Rifle, Fusil modèle 1874 Gras)'],
  fra_marins_high:['Fusiliers marins (Late)','French naval infantry armed with the repeating naval Kropatschek.','Fusiliers marins (Late; Magazine Rifle, Fusil de marine modèle 1878 Kropatschek)'],
  fra_senegalais_early:['Tirailleurs sénégalais (Early)','Regular colonial line infantry serving France with older muzzle-loading rifles.','Tirailleurs sénégalais (Early; Rifle-Musket, Fusil modèle 1842 T)'],
  fra_senegalais_mid:['Tirailleurs sénégalais (Mid)','Regular colonial line infantry equipped with converted Tabatière rifles.','Tirailleurs sénégalais (Mid; Rifle, Fusil modèle 1853/67 Tabatière)'],
  fra_senegalais_high:['Tirailleurs sénégalais (Late)','Regular colonial line infantry continuing to use the reliable Gras.','Tirailleurs sénégalais (Late; Rifle, Fusil modèle 1874 Gras)'],
  fra_indochinois_high:['Tirailleurs indochinois (Late)','Regular colonial line infantry raised in French Indochina and armed with Gras rifles.','Tirailleurs indochinois (Late; Rifle, Fusil modèle 1874 Gras)'],
  fra_cuirassiers:['Cuirassiers','Elite French heavy cavalry protected by cuirasses and armed with Lefaucheux Model 1858 revolvers and sabres.','Cuirassiers (Lefaucheux Model 1858 Revolver and Sabre)'],
  fra_hussards:['Hussards','French light cavalry armed with Lefaucheux Model 1858 revolvers and sabres.','Hussards (Lefaucheux Model 1858 Revolver and Sabre)'],
  fra_chasseurs_cheval:['Chasseurs à cheval','French light cavalry armed with Lefaucheux Model 1858 revolvers and sabres.','Chasseurs à cheval (Lefaucheux Model 1858 Revolver and Sabre)'],
  fra_carabiniers_early:['Carabiniers (Early)','French heavy carbine cavalry armed with a muzzle-loading cavalry carbine.','Carabiniers (Early; Carabine de cavalerie modèle 1853)'],
  fra_carabiniers_mid:['Carabiniers (Mid)','French heavy carbine cavalry armed with the Tabatière.','Carabiniers (Mid; Carabine modèle 1867 Tabatière)'],
  fra_carabiniers_high:['Carabiniers (Late)','French heavy carbine cavalry armed with the Berthier cavalry carbine.','Carabiniers (Late; Mousqueton de cavalerie modèle 1890 Berthier)'],
  fra_spahis_early:['Spahis (Early)','French colonial horse cavalry armed with muzzle-loading carbines and sabres.','Spahis (Early; Carabine de cavalerie modèle 1857)'],
  fra_spahis_mid:['Spahis (Mid)','French colonial horse cavalry armed with Chassepot carbines and sabres.','Spahis (Mid; Carabine modèle 1866 Chassepot)'],
  fra_spahis_high:['Spahis (Late)','French colonial horse cavalry continuing to use Gras carbines.','Spahis (Late; Carabine modèle 1874 Gras)'],
  fra_general_staff:['Général et état-major','The French general and four-man staff direct the army from horseback, armed with Lefaucheux Model 1858 revolvers and sabres.','Général et état-major (Lefaucheux Model 1858 Revolver and Sabre)'],
};

let locBuf = fs.readFileSync(locPath);
const hasBom = locBuf[0] === 0xff && locBuf[1] === 0xfe;
let loc = locBuf.slice(hasBom ? 2 : 0).toString('utf16le').replace(/\r\n/g, '\n');
for (const key of Object.keys(descriptions)) {
  const re = new RegExp(`^\\{${key}(?:_descr|_descr_short)?\\}.*(?:\\n|$)`, 'gm');
  loc = loc.replace(re, '');
}
loc = loc.trimEnd() + '\n\n' + Object.entries(descriptions).map(([key,[name,desc,short]]) =>
  `{${key}}${name}\n{${key}_descr}${desc}\n{${key}_descr_short}${short}`
).join('\n\n') + '\n';
const locOut = Buffer.concat([Buffer.from([0xff,0xfe]), Buffer.from(loc.replace(/\n/g, '\r\n'), 'utf16le')]);
fs.writeFileSync(locPath, locOut);

const cardMap = {
  fra_fusiliers_early:'fra_line_inf', fra_fusiliers_mid:'fra_line_inf', fra_fusiliers_high:'fra_pith',
  fra_garde_mobile_early:'fra_rec', fra_garde_nationale_mid:'fra_rec',
  fra_zouaves_early:'us_zouave_france', fra_zouaves_mid:'us_zouave_france', fra_zouaves_high:'us_zouave_france',
  fra_chasseurs_early:'fra_chass', fra_chasseurs_mid:'fra_chass', fra_chasseurs_high:'fra_chass',
  fra_guard_grenadiers_early:'fra_ww1_inf', fra_guard_grenadiers_mid:'fra_ww1_inf',
  fra_legion_early:'fra_inf_fr', fra_legion_mid:'fra_inf_fr', fra_legion_high:'fra_inf_fl',
  fra_marins_early:'fra_sailors', fra_marins_mid:'fra_sailors', fra_marins_high:'fra_sailors',
  fra_senegalais_early:'fra_blacks_fr', fra_senegalais_mid:'fra_blacks_fr', fra_senegalais_high:'fra_blacks_fr',
  fra_indochinois_high:'fra_vietna_france', fra_cuirassiers:'fra_hus_2', fra_hussards:'fra_carbs', fra_chasseurs_cheval:'fra_carbs',
  fra_carabiniers_early:'fra_cav2', fra_carabiniers_mid:'fra_cav2', fra_carabiniers_high:'fra_cav', fra_general_staff:'fra_hussar',
};
const cardsDir = path.join(root, 'data/ui/units/france');
const infoDir = path.join(root, 'data/ui/unit_info/france');
for (const [target,source] of Object.entries(cardMap)) {
  const src = path.join(cardsDir, `#${source}.tga`);
  if (fs.existsSync(src)) fs.copyFileSync(src, path.join(cardsDir, `#${target}.tga`));
  const infoSrc = path.join(infoDir, `${source}_info.tga`);
  if (fs.existsSync(infoSrc)) fs.copyFileSync(infoSrc, path.join(infoDir, `${target}_info.tga`));
}
for (const target of ['fra_spahis_early','fra_spahis_mid','fra_spahis_high']) {
  const src = path.join(root, 'data/ui/units/mercs/#merc_fra_for_cav.tga');
  if (fs.existsSync(src)) fs.copyFileSync(src, path.join(cardsDir, `#${target}.tga`));
}

let soundRaw = fs.readFileSync(soundPath, 'utf8');
const soundEol = soundRaw.includes('\r\n') ? '\r\n' : '\n';
let sounds = soundRaw.replace(/\r\n/g, '\n');
const soundTemplateMatch = sounds.match(/(^\s*unit fra_line_inf\n\s*event\n\s*folder data\/sounds\/Voice\/Human\/Localized\/Battle_Map\/french\n\s*inf_unit_selection_1\.wav\n\s*inf_unit_selection_2\.wav\n\s*end)/m);
if (!soundTemplateMatch) throw new Error('Could not locate French unit-selection sound template');
const soundIndent = soundTemplateMatch[1].match(/^(\s*)unit/m)[1];
const soundTargets = Object.keys(descriptions);
const newSoundBlocks = soundTargets.filter(name => !new RegExp(`^\\s*unit ${name}$`, 'm').test(sounds)).map(name =>
  soundTemplateMatch[1].replace(`${soundIndent}unit fra_line_inf`, `${soundIndent}unit ${name}`)
);
if (newSoundBlocks.length) {
  sounds = sounds.replace(soundTemplateMatch[1], soundTemplateMatch[1] + '\n' + newSoundBlocks.join('\n'));
  fs.writeFileSync(soundPath, sounds.replace(/\n/g, soundEol), 'utf8');
}

function duplicates(items) {
  const seen = new Set();
  const dupes = new Set();
  for (const item of items) (seen.has(item) ? dupes : seen).add(item);
  return [...dupes];
}

const finalEdu = fs.readFileSync(canonicalEdu, 'utf8');
const allTypes = [...finalEdu.matchAll(/^type\s+(.+)$/gm)].map(m => m[1].trim());
const allDictionaries = [...finalEdu.matchAll(/^dictionary\s+(\S+)/gm)].map(m => m[1]);
if (duplicates(allTypes).length) throw new Error(`Duplicate EDU types: ${duplicates(allTypes).join(', ')}`);
if (duplicates(allDictionaries).length) throw new Error(`Duplicate EDU dictionaries: ${duplicates(allDictionaries).join(', ')}`);
const typeSet = new Set(allTypes);
const finalEdb = fs.readFileSync(edbPaths[0], 'utf8');
const missingRecruitment = [...new Set([...finalEdb.matchAll(/recruit_pool\s+"([^"]+)/g)].map(m => m[1]).filter(name => !typeSet.has(name)))];
if (missingRecruitment.length) throw new Error(`EDB references missing EDU types: ${missingRecruitment.join(', ')}`);
for (const [,name] of modelClones) {
  const hits = finalModelHits(modeldb, name);
  if (hits !== 1) throw new Error(`Expected one modeldb entry for ${name}, found ${hits}`);
}
function finalModelHits(text, name) {
  return [...text.matchAll(new RegExp(`^${name.length} ${name} $`, 'gm'))].length;
}
for (const key of Object.keys(descriptions)) {
  if (!loc.includes(`{${key}}`)) throw new Error(`Missing localization for ${key}`);
  if (!fs.existsSync(path.join(cardsDir, `#${key}.tga`))) throw new Error(`Missing unit card for ${key}`);
}
if (!fs.readFileSync(canonicalEdu).equals(fs.readFileSync(runtimeEdu))) throw new Error('Canonical and runtime EDU files differ');
if (!fs.readFileSync(edbPaths[0]).equals(fs.readFileSync(edbPaths[1]))) throw new Error('Canonical and runtime EDB files differ');

console.log(`Standardized ${infantryUnits.length + cav.length + 1} French EDU records and added ${missingClones.length} modeldb entries.`);
