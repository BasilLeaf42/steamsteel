const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const canonical = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const runtime = path.join(root, 'data/export_descr_unit.txt');
const backup = path.join(root, 'tools/backup_before_remaining_mercenary_standardization_20260922/export_descr_unit_canonical.txt');
if (!fs.existsSync(backup)) throw new Error('Required pre-edit backup is missing');

const targets = [
  'merc_us_farmer_cav','merc_ap_front_cav','merc_apache_inf','merc_uru_inf','merc_para_foot','merc_us_farmers',
  'merc_port_inf_early','merc_port_inf_mid','merc_port_inf_high','merc_port_cav_early','merc_port_cav_mid','merc_port_cav_high','merc_port_inf','merc_port_lancer',
  'merc_bhutan_warrior','merc_papa_bows','merc_burmese_inf','merc_indian_fanatic','merc_maori_spearmen','merc_maori_musketeers',
  'merc_arab_sailors','merc_fra_blacks','merc_eng_for_cav','merc_fra_for_cav','merc_mongol_bows','merc_pol_hussars','merc_polish_inf',
  'merc_georgian_inf','merc_serb_inf','merc_bulgarian_inf','merc_kok_royal_cav','merc_kashgar_inf','merc_rus_georgian_cav',
  'merc_zulu_spearmen','merc_sikh_warriors','merc_fra_inf_ch','merc_arab_brigade','merc_balk_cav_ch','merc_siam_agent','merc_uk_sailor'
];

function blocks(text) {
  const found = new Map();
  for (const m of text.matchAll(/(^type\s+(\S+)\s*\r?\n[\s\S]*?)(?=^type\s+|(?![\s\S]))/gm)) found.set(m[2], m[1]);
  return found;
}
function set(block, field, value) {
  const re = new RegExp(`^${field}\\s+.*$`, 'm');
  if (!re.test(block)) throw new Error(`Missing ${field}`);
  return block.replace(re, `${field.padEnd(17)}${value}`);
}
function setSoldierCount(block, n, soldierOverride) {
  const m = block.match(/^soldier\s+(\S+),\s*\d+,\s*([^\r\n]+)$/m);
  if (!m) throw new Error('Missing soldier field');
  return block.replace(m[0], `soldier          ${soldierOverride || m[1]}, ${n}, ${m[2]}`);
}
function cost(total, limit, turns=2) {
  const third = Math.round(total / 3);
  return `${turns}, ${total}, ${third}, 100, 100, ${total}, ${limit}, ${third}`;
}
const standardGun = muzzle => `free_upkeep_unit, sea_faring, hide_forest, gunmen, start_not_skirmishing, cannot_skirmish, mercenary_unit${muzzle ? ', gunpowder_unit' : ''}`;
const standardCavGun = muzzle => `free_upkeep_unit, sea_faring, hide_forest, gunmen, guncavalry, start_not_skirmishing, cannot_skirmish, mercenary_unit${muzzle ? ', gunpowder_unit' : ''}`;
const standardMelee = 'free_upkeep_unit, sea_faring, hide_forest, mercenary_unit';

const C = {};
function cfg(type, fields) { C[type] = fields; }
function gun(type, p) {
  cfg(type, {
    count:p.n || (p.skirm ? 30 : 40), class:'missile', attributes:standardGun(!!p.muzzle),
    formation:p.skirm ? '1.4, 1.8, 2.8, 3.6, 3, square' : p.formation,
    stat_pri:p.pri, stat_sec:p.sec, stat_sec_attr:p.secAttr || 'no', stat_pri_armour:p.armour,
    stat_ground:'0, 0, 0, 0', stat_mental:p.mental, stat_fire_delay:'0', stat_cost:cost(p.cost,p.limit || 1,p.turns || 2),
    ...(p.soldier ? {soldier:p.soldier} : {})
  });
}
function cavgun(type,p) {
  cfg(type,{count:24,class:'missile',attributes:standardCavGun(!!p.muzzle),formation:'2, 2, 4, 4, 3, square',stat_pri:p.pri,stat_sec:p.sec,
    stat_sec_attr:'no',stat_pri_armour:p.armour,stat_ground:'0, 0, 0, 0',stat_mental:p.mental,stat_fire_delay:'0',stat_cost:cost(p.cost,p.limit || 1,p.turns || 3)});
}
function melee(type,p) {
  cfg(type,{count:p.n,class:p.class || 'light',attributes:standardMelee,formation:p.formation || '1.2, 1.2, 1.2, 1.2, 3, square',
    stat_pri:p.pri,stat_pri_attr:p.priAttr || 'no',stat_sec:p.sec || '0, 0, no, 0, 0, no, melee_simple, blunt, none, 0, 1',stat_sec_attr:p.secAttr || 'no',
    stat_pri_armour:p.armour,stat_ground:'0, 0, 0, 0',stat_mental:p.mental,stat_fire_delay:'0',stat_cost:cost(p.cost,p.limit || 1,p.turns || 1)});
}

cavgun('merc_us_farmer_cav',{pri:'26, 2, rifled_musket_carbine_bullet_c, 200, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'3, 2, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',armour:'4, 3, 0, leather',mental:'3, low, trained',cost:1200,limit:2});
cavgun('merc_ap_front_cav',{pri:'28, 2, rifled_musket_carbine_bullet_c, 200, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'3, 2, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',armour:'4, 3, 0, leather',mental:'3, low, trained',cost:1200,limit:2});
gun('merc_apache_inf',{soldier:'merc_apache_inf',skirm:true,pri:'29, 1, rifled_musket_bullet_b, 260, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'3, 2, no, 0, 0, melee, melee_blade, slashing, axe, 25, 1',armour:'3, 1, 0, flesh',mental:'2, impetuous, trained',cost:1000,limit:2});
gun('merc_uru_inf',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'29, 0, rifled_musket_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'4, low, trained',cost:1200});
gun('merc_para_foot',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'40, 0, musket_bullet_c, 200, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'2, 2, no, 0, 0, melee, melee_blade, slashing, axe, 25, 1',armour:'3, 2, 0, leather',mental:'3, low, trained',cost:800,limit:2});
gun('merc_us_farmers',{muzzle:true,skirm:true,pri:'27, 0, rifled_musket_bullet_b, 260, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'2, 2, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 2, 0, leather',mental:'3, low, trained',cost:1000,limit:2});

gun('merc_port_inf_early',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'29, 0, rifled_musket_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'4, low, trained',cost:1200,limit:1});
gun('merc_port_inf_mid',{formation:'1.2, 1.2, 2.0, 2.4, 3, square',pri:'21, 0, rifle_bullet_c, 240, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'4, low, trained',cost:1500});
gun('merc_port_inf_high',{formation:'1.2, 1.4, 2.4, 2.8, 3, square',pri:'15, 0, magazine_rifle_bullet_c, 260, 35, missile, missile_gunpowder, piercing, none, smokeless_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'4, low, trained',cost:1800});
cavgun('merc_port_cav_early',{pri:'21, 2, rifled_musket_carbine_bullet_c, 200, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',armour:'4, 4, 0, leather',mental:'4, low, trained',cost:1400});
cavgun('merc_port_cav_mid',{pri:'20, 2, rifle_carbine_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',armour:'4, 4, 0, leather',mental:'4, low, trained',cost:1700});
cavgun('merc_port_cav_high',{pri:'15, 2, magazine_rifle_carbine_bullet_c, 240, 35, missile, missile_gunpowder, piercing, none, smokeless_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',armour:'4, 4, 0, leather',mental:'4, low, trained',cost:2000});
Object.assign(C.merc_port_inf_early,{hideCustom:true}); Object.assign(C.merc_port_inf_mid,{hideCustom:true}); Object.assign(C.merc_port_inf_high,{hideCustom:true});
Object.assign(C.merc_port_cav_early,{hideCustom:true}); Object.assign(C.merc_port_cav_mid,{hideCustom:true}); Object.assign(C.merc_port_cav_high,{hideCustom:true});
gun('merc_port_inf',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'29, 0, rifled_musket_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'4, low, trained',cost:1200,limit:2});
cavgun('merc_port_lancer',{pri:'21, 2, rifled_musket_carbine_bullet_c, 200, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',armour:'4, 4, 0, leather',mental:'4, low, trained',cost:1400});
Object.assign(C.merc_port_inf,{ownership:'slave, england, spain',eras:'era 0            england, spain\nera 1            england, spain\nera 2            england, spain'});
Object.assign(C.merc_port_lancer,{ownership:'slave, england, spain',eras:'era 0            england, spain\nera 1            england, spain\nera 2            england, spain'});

melee('merc_bhutan_warrior',{n:80,pri:'3, 2, no, 0, 0, melee, melee_blade, slashing, sword, 25, 1',armour:'3, 1, 2, flesh',mental:'2, low, untrained',cost:500});
cfg('merc_papa_bows',{count:64,class:'missile',attributes:standardMelee,formation:'1.4, 1.8, 2.8, 3.6, 3, square',stat_sec:'2, 2, no, 0, 0, melee, melee_blade, blunt, mace, 25, 1',stat_sec_attr:'no',stat_pri_armour:'3, 1, 0, flesh',stat_ground:'0, 0, 0, 0',stat_mental:'2, impetuous, untrained',stat_fire_delay:'0',stat_cost:cost(500,1,1)});
gun('merc_burmese_inf',{muzzle:true,skirm:true,pri:'37, 0, rifled_musket_bullet_b, 260, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 2, 0, leather',mental:'3, low, trained',cost:1200});
melee('merc_indian_fanatic',{n:80,pri:'5, 2, javelin, 60, 2, thrown, missile_mechanical, piercing, spear, 25, 1',priAttr:'prec, thrown',sec:'7, 4, no, 0, 0, melee, melee_blade, slashing, sword, 25, 1',armour:'3, 3, 2, flesh',mental:'5, impetuous, highly_trained',cost:900});
melee('merc_maori_spearmen',{n:96,pri:'2, 2, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',priAttr:'light_spear',armour:'3, 1, 2, flesh',mental:'2, impetuous, untrained',cost:500,limit:2});
gun('merc_maori_musketeers',{muzzle:true,skirm:true,pri:'40, 0, musket_bullet_b, 240, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'2, 2, no, 0, 0, melee, melee_blade, slashing, sword, 25, 1',armour:'3, 1, 0, leather',mental:'2, impetuous, untrained',cost:800,limit:2});
gun('merc_arab_sailors',{formation:'1.2, 1.2, 2.0, 2.4, 3, square',pri:'24, 0, rifle_bullet_c, 240, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'4, low, trained',cost:1500,limit:2});
gun('merc_fra_blacks',{formation:'1.2, 1.2, 2.0, 2.4, 3, square',pri:'24, 0, rifle_bullet_b, 240, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'5, low, trained',cost:1400});
cavgun('merc_eng_for_cav',{pri:'21, 2, rifle_carbine_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',armour:'4, 3, 0, leather',mental:'4, low, trained',cost:1700});
cavgun('merc_fra_for_cav',{pri:'20, 2, rifle_carbine_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',armour:'4, 4, 0, leather',mental:'5, low, trained',cost:1600});
cfg('merc_mongol_bows',{count:64,class:'missile',attributes:standardMelee,formation:'1.4, 1.8, 2.8, 3.6, 3, square',stat_sec:'3, 3, no, 0, 0, melee, melee_blade, blunt, mace, 25, 1',stat_sec_attr:'no',stat_pri_armour:'3, 2, 0, leather',stat_ground:'0, 0, 0, 0',stat_mental:'3, low, trained',stat_fire_delay:'0',stat_cost:cost(700,1,1)});
cavgun('merc_pol_hussars',{muzzle:true,pri:'37, 2, musket_carbine_bullet_c, 180, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'5, 3, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',armour:'4, 4, 0, leather',mental:'4, normal, trained',cost:1200});
gun('merc_polish_inf',{formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'31, 0, rifled_musket_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'5, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'4, normal, trained',cost:1200,limit:2});
gun('merc_georgian_inf',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'37, 0, musket_bullet_c, 200, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'5, 3, no, 0, 0, melee, melee_blade, slashing, sword, 25, 1',armour:'3, 3, 0, leather',mental:'4, impetuous, trained',cost:1000,limit:2});
gun('merc_serb_inf',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'37, 0, rifled_musket_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'4, low, trained',cost:1200,limit:2});
gun('merc_bulgarian_inf',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'27, 0, rifled_musket_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'4, low, trained',cost:1200});
cfg('merc_kok_royal_cav',{count:24,class:'light',attributes:standardMelee,formation:'2, 2, 4, 4, 3, square',stat_pri:'4, 6, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',stat_pri_attr:'no',stat_sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',stat_sec_attr:'no',stat_pri_armour:'4, 3, 0, leather',stat_ground:'0, 0, 0, 0',stat_mental:'3, low, trained',stat_fire_delay:'0',stat_cost:cost(1200,2,2)});
gun('merc_kashgar_inf',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'37, 0, musket_bullet_c, 200, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 2, 0, leather',mental:'3, low, trained',cost:1000,limit:2});
cfg('merc_rus_georgian_cav',{count:24,class:'light',attributes:standardMelee,formation:'2, 2, 4, 4, 3, square',stat_pri:'4, 6, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',stat_pri_attr:'no',stat_sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',stat_sec_attr:'no',stat_pri_armour:'4, 3, 0, leather',stat_ground:'0, 0, 0, 0',stat_mental:'4, impetuous, trained',stat_fire_delay:'0',stat_cost:cost(1200,1,2)});
melee('merc_zulu_spearmen',{n:96,pri:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',armour:'3, 1, 4, flesh',mental:'3, impetuous, trained',cost:500,limit:2});
gun('merc_sikh_warriors',{formation:'1.2, 1.2, 2.0, 2.4, 3, square',pri:'19, 0, rifle_bullet_c, 240, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'5, 3, no, 0, 0, melee, melee_blade, slashing, sword, 25, 1',armour:'3, 2, 2, leather',mental:'3, low, trained',cost:1500});
gun('merc_fra_inf_ch',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'37, 0, rifled_musket_bullet_c, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'4, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 3, 0, leather',mental:'4, low, trained',cost:1200,limit:2});
gun('merc_arab_brigade',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'37, 0, musket_bullet_c, 200, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'3, 2, no, 0, 0, melee, melee_blade, slashing, sword, 25, 1',armour:'3, 1, 0, flesh',mental:'2, impetuous, trained',cost:800,limit:2});
cfg('merc_balk_cav_ch',{count:24,class:'light',attributes:standardMelee,formation:'2, 2, 4, 4, 3, square',stat_pri:'4, 3, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1',stat_pri_attr:'no',stat_sec:'0, 0, no, 0, 0, no, no, no, none, 25, 1',stat_sec_attr:'no',stat_pri_armour:'4, 4, 0, leather',stat_ground:'0, 0, 0, 0',stat_mental:'4, low, trained',stat_fire_delay:'0',stat_cost:cost(1000,1,2)});
gun('merc_siam_agent',{muzzle:true,formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'32, 0, arquebus_bullet_c, 160, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'2, 2, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 1, 0, leather',mental:'2, low, trained',cost:700,limit:2});
gun('merc_uk_sailor',{formation:'1.2, 1.2, 1.2, 1.2, 3, square',pri:'29, 0, rifled_musket_bullet_b, 220, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999',sec:'6, 4, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1',secAttr:'ap, short_pike',armour:'3, 4, 0, leather',mental:'6, disciplined, trained',cost:1400});

function rewrite(text) {
  const beforeCount = (text.match(/^type\s+/gm)||[]).length;
  const seen = new Set();
  text = text.replace(/(^type\s+(\S+)\s*\r?\n[\s\S]*?)(?=^type\s+|(?![\s\S]))/gm, (whole, block, type) => {
    const c = C[type]; if (!c) return block; seen.add(type);
    if (c.count) { try { block = setSoldierCount(block,c.count,c.soldier); } catch (e) { throw new Error(`${type}: ${e.message}`); } }
    for (const [field,value] of Object.entries(c)) {
      if (['count','soldier','hideCustom','ownership','eras'].includes(field)) continue;
      block = set(block,field,value);
    }
    if (c.hideCustom) block = set(block,'attributes',block.match(/^attributes\s+(.+)$/m)[1].replace(/,?\s*no_custom/g,'') + ', no_custom');
    else block = set(block,'attributes',block.match(/^attributes\s+(.+)$/m)[1].replace(/,?\s*no_custom/g,''));
    if (c.ownership) block = set(block,'ownership',c.ownership);
    if (c.eras) {
      block = block.replace(/^era\s+[012].*(?:\r?\n|$)/gm,'');
      block = block.trimEnd() + '\n' + c.eras + '\n\n';
    }
    return block;
  });
  const missing = targets.filter(t=>!seen.has(t));
  if (missing.length) throw new Error('Target records not found: '+missing.join(', '));
  if ((text.match(/^type\s+/gm)||[]).length !== beforeCount) throw new Error('EDU record count changed');
  return text;
}

const source = fs.readFileSync(canonical,'utf8');
const output = rewrite(source);
fs.writeFileSync(canonical,output);
fs.writeFileSync(runtime,output);
console.log(`Standardized ${targets.length} mercenary records without deleting or renaming any EDU type.`);
