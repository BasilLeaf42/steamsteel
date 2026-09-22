const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const mustReplace = (text, from, to, label) => {
  if (!text.includes(from)) throw new Error(`Missing ${label}`);
  return text.replace(from, to);
};

const stdPath = path.join(__dirname, 'standardize_union.js');
let std = fs.readFileSync(stdPath, 'utf8');
std = std.replaceAll('uni_regulars_early', 'uni_state_volunteers_early');
std = mustReplace(
  std,
  "{type:'uni_state_volunteers_early',label:'United States Regulars',p:'early',w:W.springfield61,quality:'regular',role:'line',donor:'us_inf',card:'us_inf',eras:[0],limit:2}",
  "{type:'uni_state_volunteers_early',label:'State Volunteers',p:'early',w:W.springfield61,quality:'militia',role:'line',donor:'us_inf',card:'us_inf',eras:[0],limit:6}",
  'State Volunteers row'
);
std = mustReplace(
  std,
  "{type:'uni_indian_scout_cavalry',label:'Indian Scout Cavalry',p:'mid',w:W.burnside,quality:'militia',donor:'ap_front_cav',card:'ap_front_cav',eras:[0,1],limit:1,aux:true}",
  "{type:'uni_indian_scout_cavalry',label:'Indian Scout Cavalry',p:'mid',w:W.pistol,quality:'militia',donor:'ap_front_cav',card:'ap_front_cav',eras:[0,1],limit:1,aux:true,pistolSpear:true}",
  'Indian Scout Cavalry row'
);
std = mustReplace(
  std,
  "const W={",
  "const W={pistol:{name:'Colt Revolver',damage:20,family:'magazine_rifle',range:60,ammo:15,smoke:'musket_shot_set',base:1000,muzzle:false},",
  'weapon table'
);
const oldCommand = "`stat_pri         ${q.melee}, ${q.charge}, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1`,'stat_pri_attr    no','stat_sec         0, 0, no, 0, 0, no, melee_simple, blunt, none, 0, 1','stat_sec_attr    no'";
const newCommand = "'stat_pri         20, 4, magazine_rifle_bullet_c, 60, 15, missile, missile_gunpowder, piercing, none, musket_shot_set, 25, 1','stat_pri_attr    ap',`stat_sec         ${q.melee}, ${q.charge}, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1`,'stat_sec_attr    no'";
std = mustReplace(std, oldCommand, newCommand, 'General pistol row');
const oldCavReturn = "const p=down[q.proj],total=u.w.base+q.premium+200;return [";
const newCavReturn = "const p=down[q.proj],total=u.pistolSpear?1200:u.w.base+q.premium+200;if(u.pistolSpear)return [`type             ${u.type}`,`dictionary       ${u.type} ; ${u.label} (Colt Revolver and spear)`,'category         cavalry','class            light','voice_type       Heavy','accent           american','banner faction   main_cavalry','banner holy      crusade_cavalry',`soldier          ${u.type}, 24, 0, 1`,'mount            dragoon','mount_effect     elephant -4, camel -4','attributes       free_upkeep_unit, sea_faring, hide_forest, can_withdraw, guncavalry, gunmen, start_not_skirmishing, cannot_skirmish, hide_improved_forest','formation        2, 2, 4, 4, 3, square','stat_health      1, 0','stat_pri         20, 4, magazine_rifle_bullet_c, 60, 15, missile, missile_gunpowder, piercing, none, musket_shot_set, 25, 1','stat_pri_attr    ap',`stat_sec         ${q.melee}, ${q.charge}, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1`,'stat_sec_attr    no',`stat_pri_armour  4, ${q.def}, 0, leather`,'stat_sec_armour  0, 0, flesh','stat_heat        0','stat_ground      0, 0, 0, 0',`stat_mental      ${q.morale}, impetuous, ${q.training}`,'stat_charge_dist 45','stat_fire_delay  0','stat_food        60, 300',`stat_cost        ${cost(total,u.limit)}`,'ownership        portugala, slave',...u.eras.map(e=>`era ${e}            portugala`)].join('\\n');return [";
std = mustReplace(std, oldCavReturn, newCavReturn, 'pistol scout cavalry record');
const oldModelLoop = "else fresh=mounted(fresh);const old=entries(model).find(x=>x.name===u.type);";
const newModelLoop = "else{fresh=mounted(fresh);if(u.command)fresh=fresh.replace('14 MTW2_HR_Pistol 13 MTW2_HR_Spear','14 MTW2_HR_Pistol 13 MTW2_HR_Sword').replace('21 MTW2_HR_spear_Primary','18 MTW2_Sword_Primary');}const old=entries(model).find(x=>x.name===u.type);";
std = mustReplace(std, oldModelLoop, newModelLoop, 'mounted command animation');
fs.writeFileSync(stdPath, std);

const valPath = path.join(__dirname, 'validate_union.js');
let val = fs.readFileSync(valPath, 'utf8').replaceAll('uni_regulars_early', 'uni_state_volunteers_early');
val = mustReplace(val, "const militia=['uni_national_guard_mid'", "const militia=['uni_state_volunteers_early','uni_national_guard_mid'", 'militia list');
val = mustReplace(val, "const regular=['uni_state_volunteers_early','uni_regulars_mid'", "const regular=['uni_regulars_mid'", 'regular list');
val = mustReplace(val, "for(const t of ['uni_volunteer_cavalry_early','uni_dragoons_early'])", "ok(/^stat_pri\\s+20, 4, magazine_rifle_bullet_c, 60, 15,/m.test(block('uni_general_staff'))&&/^stat_sec\\s+7, 4,/m.test(block('uni_general_staff')),'General and Staff pistol/sabre rows');ok(/^stat_pri\\s+20, 4, magazine_rifle_bullet_c, 60, 15,/m.test(block('uni_indian_scout_cavalry'))&&/^stat_sec\\s+3, 2,.*spear/m.test(block('uni_indian_scout_cavalry')),'Indian Scout Cavalry pistol/spear rows');ok(/^stat_cost\\s+3, 1000, 333, 100, 100, 1000, 6, 333$/m.test(block('uni_state_volunteers_early')),'State Volunteers mass limit/cost');for(const t of ['uni_volunteer_cavalry_early','uni_dragoons_early'])", 'new roster validation');
fs.writeFileSync(valPath, val);

for (const rel of [
  'data/tow_steamsteel/export_descr_buildings.txt',
  'data/export_descr_buildings.txt',
  'data/world/maps/campaign/camp_steamsteel/descr_strat.txt',
  'data/world/maps/campaign/imperial_campaign/descr_strat.txt'
]) {
  const p = path.join(root, rel);
  fs.writeFileSync(p, fs.readFileSync(p, 'utf8').replaceAll('uni_regulars_early', 'uni_state_volunteers_early'));
}

const modelPath = path.join(root, 'data/unit_models/battle_models.modeldb');
let model = fs.readFileSync(modelPath, 'utf8');
model = model.replace(/^18 uni_regulars_early\s*$/m, '26 uni_state_volunteers_early ');
fs.writeFileSync(modelPath, model);

const agentsPath = path.join(root, 'agents.md');
let agents = fs.readFileSync(agentsPath, 'utf8');
const oldUnion = /### Union modifiers\r?\n\r?\n[^\r\n]+/;
const newUnion = "### Union modifiers\r\n\r\nThe Union is B tier. State Volunteers are the mass early-period line infantry: they use the militia baseline and a custom-battle limit of 6, reflecting that the Civil War armies were overwhelmingly state-raised volunteer regiments rather than the small prewar Regular Army. The roster consolidates in the mid period into United States Regulars and National Guard lineages. National Guard, United States Colored Troops, Irish Brigade, Zouave Volunteers, and Union Volunteer Cavalry use militia baselines even when their historical identity or specialist role is distinguished. United States Regulars, United States Marines, and United States Dragoons use regular baselines. United States Sharpshooters are regular-quality sharpshooters: the role affects projectile accuracy and cost but does not make them elite in melee, armour, morale, or training. Indian Scouts and Indian Scout Cavalry are regional militia-quality auxiliaries, retain impetuous discipline, and may retain improved forest concealment as an explicit scouting-role exception. Indian Scout Cavalry uses the embedded pistol-and-spear rider equipment; General and Staff uses its embedded pistol with a sabre secondary. Early and mid national infantry uses usa_off_1g plus the verified usa_standard_bearer cloned from the complete francejunqshou model mapping: its existing portugala body texture visibly depicts a blue Union uniform and its existing portugala flag texture visibly depicts the United States flag. Late infantry uses only usa_off_1g. Artillery remains outside this infantry-and-cavalry balance pass.";
if (!oldUnion.test(agents)) throw new Error('Union agents section missing');
agents = agents.replace(oldUnion, newUnion);
fs.writeFileSync(agentsPath, agents);

console.log('Revised Union generator, validator, mirrors, campaign mapping, model name, and project rules.');
