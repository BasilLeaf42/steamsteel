const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const eduCanonical = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const eduRuntime = path.join(root, 'data/export_descr_unit.txt');
const modelPath = path.join(root, 'data/unit_models/battle_models.modeldb');
const locPath = path.join(root, 'data/text/export_units.txt');
const soundPath = path.join(root, 'data/export_descr_sounds_units_voice.txt');
const nl = '\n';

const era = {
  early:{n:0, formation:'1.2, 1.2, 1.2, 1.2, 3, square'},
  mid:{n:1, formation:'1.2, 1.2, 2.0, 2.4, 3, square'},
  high:{n:2, formation:'1.2, 1.4, 2.4, 2.8, 3, square'},
};
const cost = (n, limit=1) => `3, ${n}, ${Math.round(n/3)}, 100, 100, ${n}, ${limit}, ${Math.round(n/3)}`;
const periodName = p => p === 'high' ? 'Late' : p === 'mid' ? 'Mid' : 'Early';

function infantry(u) {
  const attrs=['free_upkeep_unit','sea_faring','hide_forest'];
  if(u.muzzle) attrs.push('gunpowder_unit');
  attrs.push('gunmen','start_not_skirmishing','cannot_skirmish');
  if(u.period==='high') attrs.push('stakes');
  if(u.special) attrs.push(...u.special);
  const officers=['officer          pru_off_1g'];
  if(u.period!=='high') officers.push('officer          russia_qi');
  return [
    `type             ${u.type}`,
    `dictionary       ${u.type} ; ${u.label} (${periodName(u.period)}; ${u.weapon})`,
    'category         infantry','class            missile','voice_type       Light','accent           german',
    'banner faction   main_infantry','banner holy      crusade',
    `soldier          ${u.type}, ${u.strength||40}, 0, 1.2`,...officers,
    `attributes       ${attrs.join(', ')}`,
    `formation        ${u.skirm ? '1.4, 1.8, 2.8, 3.6, 3, square' : era[u.period].formation}`,
    'stat_health      1, 0',
    `stat_pri         ${u.damage}, 0, ${u.projectile}, ${u.range}, ${u.ammo}, missile, missile_gunpowder, piercing, none, ${u.smoke}, 0, -999`,
    'stat_pri_attr    ap',
    `stat_sec         ${u.melee}, ${u.charge}, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1.2`,
    'stat_sec_attr    short_pike, ap',
    `stat_pri_armour  3, ${u.defence}, 0, leather`,'stat_sec_armour  0, 0, flesh','stat_heat        0','stat_ground      0, 0, 0, 0',
    `stat_mental      ${u.morale}, ${u.discipline}, ${u.training}`,'stat_charge_dist 40','stat_fire_delay  0','stat_food        60, 300',
    `stat_cost        ${cost(u.cost,u.limit||1)}`,'ownership        hre, slave',`era ${era[u.period].n}            hre`
  ].join(nl);
}

function grenadeUnit(u) {
  return [
    `type             ${u.type}`,`dictionary       ${u.type} ; ${u.label} (Spät)`,'category         infantry','class            missile','voice_type       Heavy','accent           german',
    'banner faction   main_infantry','banner holy      crusade',`soldier          ${u.type}, 16, 0, 1.2`,'officer          pru_off_1g',
    'attributes       free_upkeep_unit, sea_faring, hide_forest, can_withdraw, incendiary, start_not_skirmishing, cannot_skirmish, stakes',
    'formation        1.4, 1.8, 2.8, 3.6, 3, square','stat_health      1, 0',
    'stat_pri         7, 3, greek_fire, 60, 2, missile, missile_gunpowder, slashing, none, 25, 1','stat_pri_attr    ap, bp',
    'stat_sec         8, 5, no, 0, 0, melee, melee_blade, blunt, sword, 25, 1','stat_sec_attr    ap, short_pike',
    'stat_pri_armour  3, 5, 0, leather','stat_sec_armour  0, 0, flesh','stat_heat        0','stat_ground      0, 0, 0, 0',
    'stat_mental      7, disciplined, highly_trained','stat_charge_dist 30','stat_fire_delay  0','stat_food        60, 300',
    `stat_cost        ${cost(1500)}`,'ownership        hre, slave','era 2            hre'
  ].join(nl);
}

function cavalry(u) {
  const gun=u.armament==='carbine'||u.armament==='pistol';
  const attrs=['free_upkeep_unit','sea_faring','hide_forest','can_withdraw'];
  if(gun) attrs.push('guncavalry','gunmen','start_not_skirmishing','cannot_skirmish');
  if(u.armament==='carbine') attrs.push('stakes');
  if(u.general) attrs.push('general_unit','command');
  const officers=['officer          otto_sipahi'];
  const rows=gun ? [
    `stat_pri         ${u.damage}, ${u.armament==='pistol'?4:2}, ${u.projectile}, ${u.range}, ${u.ammo}, missile, missile_gunpowder, piercing, none, ${u.smoke}, 25, 1`,
    'stat_pri_attr    ap',`stat_sec         ${u.melee}, ${u.charge}, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1`,'stat_sec_attr    ap'
  ] : [
    `stat_pri         ${u.melee}, ${u.charge}, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1`,'stat_pri_attr    ap',
    'stat_sec         0, 0, no, 0, 0, no, no, no, none, 25, 1','stat_sec_attr    no'
  ];
  const eraRows=u.period?[`era ${era[u.period].n}            hre`]:['era 0            hre','era 1            hre','era 2            hre'];
  return [
    `type             ${u.type}`,`dictionary       ${u.type} ; ${u.label}${u.period?` (${periodName(u.period)}; ${u.weapon})`:` (${u.weapon})`}`,
    'category         cavalry',`class            ${u.className}`,'voice_type       Heavy','accent           german','banner faction   main_cavalry','banner holy      crusade_cavalry',
    `soldier          ${u.type}, ${u.general?4:24}, 0, 1`,...officers,`mount            ${u.mount||'hussar'}`,'mount_effect     elephant -4, camel -4',
    `attributes       ${attrs.join(', ')}`,`formation        2, 2, 4, 4, ${u.general?2:3}, square`,'stat_health      1, 0',...rows,
    `stat_pri_armour  ${u.cuirass?'7':'4'}, ${u.defence}, 0, ${u.cuirass?'metal':'leather'}`,'stat_sec_armour  0, 0, flesh','stat_heat        0','stat_ground      0, 0, 0, 0',
    `stat_mental      ${u.morale}, ${u.discipline}, ${u.training}`,'stat_charge_dist 45','stat_fire_delay  -20000','stat_food        60, 300',
    `stat_cost        ${cost(u.cost)}`,'ownership        hre, slave',...eraRows
  ].join(nl);
}

const Areg={melee:6,charge:4,defence:4,morale:5,discipline:'disciplined',training:'trained'};
const Aelite={melee:8,charge:5,defence:5,morale:7,discipline:'disciplined',training:'highly_trained'};
const national=(type,label,period,weapon,projectile,costValue,quality='regular',extra={})=>({type,label,period,weapon,projectile,cost:costValue,...(quality==='elite'?Aelite:Areg),...extra});
const rifle=(period,mag=false)=>({damage:mag?13:20,range:mag?260:240,ammo:mag?40:35,smoke:mag?'smokeless_shot_set':'musket_shot_set'});
const earlyBreech=()=>({damage:31,range:220,ammo:35,smoke:'musket_shot_set'});

const inf=[
  national('pru_fusiliere_early','Preußische Füsiliere','early','Zündnadelgewehr M/41','rifled_musket_bullet_b',1200,'regular',earlyBreech()),
  national('pru_fusiliere_mid','Preußische Füsiliere','mid','Gewehr M/71','rifle_bullet_a',1500,'regular',rifle('mid')),
  national('pru_fusiliere_high','Preußische Füsiliere','high','Gewehr 98','magazine_rifle_bullet_a',1800,'regular',rifle('high',true)),
  national('pru_pioniere_early','Preußische Pioniere','early','Zündnadelpioniergewehr U/M','rifled_musket_bullet_a',1400,'elite',earlyBreech()),
  national('pru_pioniere_mid','Preußische Pioniere','mid','Gewehr M/71','rifle_bullet_s',1700,'elite',rifle('mid')),
  national('pru_pioniere_high','Preußische Pioniere','high','Gewehr 98','magazine_rifle_bullet_s',2000,'elite',rifle('high',true)),
  national('pru_gardegrenadiere_early','Preußische Gardegrenadiere','early','Zündnadelgewehr M/41','rifled_musket_bullet_a',1400,'elite',earlyBreech()),
  national('pru_gardegrenadiere_mid','Preußische Gardegrenadiere','mid','Gewehr M/71','rifle_bullet_s',1700,'elite',rifle('mid')),
  national('pru_gardegrenadiere_high','Preußische Gardegrenadiere','high','Gewehr 98','magazine_rifle_bullet_s',2000,'elite',rifle('high',true)),
  national('pru_jaeger_early','Preußische Jäger','early','Zündnadelbüchse M/54','rifled_musket_bullet_a',1200,'regular',{...earlyBreech(),range:260,skirm:true,strength:30}),
  national('pru_jaeger_mid','Preußische Jäger','mid','Gewehr M/71','rifle_bullet_s',1500,'regular',{...rifle('mid'),range:280,skirm:true,strength:30}),
  national('pru_jaeger_high','Preußische Jäger','high','Gewehr 98','magazine_rifle_bullet_s',1800,'regular',{...rifle('high',true),range:300,skirm:true,strength:30}),
  national('pru_seesoldaten_early','Seesoldaten','early','Zündnadelgewehr M/41','rifled_musket_bullet_a',1400,'elite',earlyBreech()),
  national('pru_seesoldaten_mid','Seesoldaten','mid','Gewehr M/71','rifle_bullet_s',1700,'elite',rifle('mid')),
  national('pru_seesoldaten_high','Seesoldaten','high','Gewehr 98','magazine_rifle_bullet_s',2000,'elite',rifle('high',true)),
  {type:'pru_wuerttemberg_mid',label:'Württembergische Füsiliere',period:'mid',weapon:'Zündnadelgewehr M/65',projectile:'rifle_bullet_b',cost:1500,melee:5,charge:3,defence:3,morale:5,discipline:'disciplined',training:'trained',...rifle('mid')},
  {type:'pru_wuerttemberg_high',label:'Württembergische Füsiliere',period:'high',weapon:'Gewehr 88',projectile:'magazine_rifle_bullet_a',cost:1800,melee:5,charge:3,defence:3,morale:5,discipline:'disciplined',training:'trained',...rifle('high',true)},
  {type:'pru_bavarian_fusiliere_mid',label:'Bayerische Füsiliere',period:'mid',weapon:'Aptiertes Gewehr M/69',projectile:'rifle_bullet_b',cost:1500,melee:5,charge:3,defence:3,morale:5,discipline:'disciplined',training:'trained',...rifle('mid')},
  {type:'pru_bavarian_fusiliere_high',label:'Bayerische Füsiliere',period:'high',weapon:'Gewehr 88',projectile:'magazine_rifle_bullet_a',cost:1800,melee:5,charge:3,defence:3,morale:5,discipline:'disciplined',training:'trained',...rifle('high',true)},
  {type:'pru_bavarian_landwehr_mid',label:'Bayerische Landwehr',period:'mid',weapon:'Werdergewehr M/69',projectile:'rifle_bullet_c',cost:1300,melee:3,charge:2,defence:2,morale:4,discipline:'normal',training:'trained',...rifle('mid')},
  {type:'pru_bavarian_landwehr_high',label:'Bayerische Landwehr',period:'high',weapon:'Gewehr M/71',projectile:'rifle_bullet_b',cost:1300,melee:3,charge:2,defence:2,morale:4,discipline:'normal',training:'trained',...rifle('high')},
  {type:'pru_hannover_mid',label:'Hannoversche Füsiliere',period:'mid',weapon:'Gewehr M/71',projectile:'rifle_bullet_b',cost:1500,melee:5,charge:3,defence:3,morale:5,discipline:'disciplined',training:'trained',...rifle('mid')},
  {type:'pru_hannover_high',label:'Hannoversche Füsiliere',period:'high',weapon:'Gewehr 88',projectile:'magazine_rifle_bullet_a',cost:1800,melee:5,charge:3,defence:3,morale:5,discipline:'disciplined',training:'trained',...rifle('high',true)},
  national('pru_sturmpioniere_high','Sturmpioniere','high','Gewehr 98','magazine_rifle_bullet_s',2000,'elite',rifle('high',true)),
  national('pru_schutztruppe_high','Schutztruppe','high','Gewehr 88','magazine_rifle_bullet_s',1800,'regular',{...rifle('high',true),range:300,skirm:true,strength:30}),
];

const cav=[
  {type:'pru_kuerassiere',label:'Preußische Kürassiere',weapon:'Zündnadelpistole M/57 und Säbel',className:'heavy',armament:'pistol',damage:20,projectile:'magazine_rifle_bullet_c',range:60,ammo:15,smoke:'musket_shot_set',melee:8,charge:5,defence:6,morale:7,discipline:'disciplined',training:'highly_trained',cost:1700,cuirass:true,mount:'cuirassier'},
  {type:'pru_husaren',label:'Preußische Husaren',weapon:'Zündnadelpistole M/57 und Säbel',className:'light',armament:'pistol',damage:20,projectile:'magazine_rifle_bullet_c',range:60,ammo:15,smoke:'musket_shot_set',melee:6,charge:4,defence:5,morale:5,discipline:'disciplined',training:'trained',cost:1200,mount:'hussar'},
  {type:'pru_dragoner_early',label:'Preußische Dragoner',period:'early',weapon:'Zündnadelkarabiner M/57',className:'heavy',armament:'carbine',damage:20,projectile:'rifle_carbine_bullet_b',range:220,ammo:35,smoke:'musket_shot_set',melee:6,charge:4,defence:5,morale:5,discipline:'disciplined',training:'trained',cost:1700,mount:'dragoon'},
  {type:'pru_dragoner_mid',label:'Preußische Dragoner',period:'mid',weapon:'Karabiner M/71',className:'heavy',armament:'carbine',damage:20,projectile:'rifle_carbine_bullet_b',range:220,ammo:35,smoke:'musket_shot_set',melee:6,charge:4,defence:5,morale:5,discipline:'disciplined',training:'trained',cost:1700,mount:'dragoon'},
  {type:'pru_dragoner_high',label:'Preußische Dragoner',period:'high',weapon:'Karabiner 88',className:'heavy',armament:'carbine',damage:13,projectile:'magazine_rifle_carbine_bullet_b',range:240,ammo:40,smoke:'smokeless_shot_set',melee:6,charge:4,defence:5,morale:5,discipline:'disciplined',training:'trained',cost:2000,mount:'dragoon'},
  {type:'pru_kolonialreiter_high',label:'Kolonialreiter',period:'high',weapon:'Karabiner 88 und Säbel',className:'light',armament:'carbine',damage:13,projectile:'magazine_rifle_carbine_bullet_b',range:240,ammo:40,smoke:'smokeless_shot_set',melee:6,charge:4,defence:5,morale:5,discipline:'disciplined',training:'trained',cost:2000,mount:'dragoon'},
  {type:'pru_general_staff',label:'General und Stab',weapon:'Zündnadelpistole M/57 und Säbel',className:'heavy',armament:'pistol',damage:20,projectile:'magazine_rifle_bullet_c',range:60,ammo:15,smoke:'musket_shot_set',melee:8,charge:5,defence:5,morale:7,discipline:'disciplined',training:'highly_trained',cost:200,general:true,mount:'hussar'},
];
const storm=grenadeUnit({type:'pru_sturmtruppen_high',label:'Sturmtruppen'});

function alias(block,type,soldier){return block.replace(/^type\s+.*$/m,`type             ${type}`).replace(/^dictionary\s+\S+/m,`dictionary       ${type}`).replace(/^soldier\s+\S+,/m,`soldier          ${soldier},`).replace(/^ownership\s+.*$/m,'ownership        slave').replace(/^era [012]\s+hre\n?/gm,'').trimEnd();}
const byType=Object.fromEntries([...inf.map(u=>[u.type,infantry(u)]),...cav.map(u=>[u.type,cavalry(u)]),['pru_sturmtruppen_high',storm]]);
const legacyMap={
  otto_sipahi:['pru_general_staff','otto_sipahi'],gr_gren:['pru_pioniere_early','gr_gren'],gr_carbs:['pru_dragoner_mid','gr_carbs'],wurt_inf:['pru_wuerttemberg_mid','wurt_inf'],
  pru_ww1_gren:['pru_sturmpioniere_high','pru_ww1_gren'],pru_ww1_inf:['pru_sturmtruppen_high','pru_ww1_inf'],bav_inf:['pru_jaeger_mid','bav_inf'],gr_inf:['pru_fusiliere_high','gr_inf'],
  gr_colonial:['pru_schutztruppe_high','gr_colonial'],jager_inf:['pru_bavarian_fusiliere_mid','aus_inf3'],rec_bav:['pru_bavarian_landwehr_mid','rec_bav'],gr_sailor:['pru_seesoldaten_mid','gr_sailor'],
  balk_cav_gr:['pru_husaren','balk_cav1'],ger_hus:['pru_kuerassiere','otto_sipahi'],hannover_inf:['pru_hannover_mid','hannover_inf'],gr_lancer:['pru_kolonialreiter_high','gr_lancer'],siam_riflemen_gr:['pru_fusiliere_early','siam_riflemen_gr']
};
const block=['; ============================================================================','; Prussia (hre) — standardized infantry and cavalry','; ============================================================================',...inf.map(infantry),storm,...cav.map(cavalry),'; Legacy internal-name compatibility (not assigned to custom-battle eras)',...Object.entries(legacyMap).map(([old,[modern,soldier]])=>alias(byType[modern],old,soldier))].join('\n\n')+'\n\n';

let edu=fs.readFileSync(eduCanonical,'utf8').replace(/\r\n/g,'\n');
const title='; Prussia (hre) — standardized infantry and cavalry';
const oldTitle='; Prussia (hre) — infantry and cavalry';
const titleAt=Math.max(edu.indexOf(title),edu.indexOf(oldTitle));
const start=edu.lastIndexOf('; ============================================================================',titleAt);
const netAt=edu.indexOf('; Netherlands (portugal) — infantry and cavalry',start);
const end=edu.lastIndexOf('; ============================================================================',netAt);
if(start<0||end<0) throw new Error('Could not locate Prussian EDU block');
edu=edu.slice(0,start)+block+edu.slice(end);
const eduOut=edu.replace(/\n/g,'\r\n');fs.writeFileSync(eduCanonical,eduOut);fs.writeFileSync(eduRuntime,eduOut);

for(const p of [path.join(root,'data/tow_steamsteel/export_descr_buildings.txt'),path.join(root,'data/export_descr_buildings.txt')]){
  let s=fs.readFileSync(p,'utf8').replace(/\r\n/g,'\n');
  for(const [old,[modern]] of Object.entries(legacyMap))s=s.replace(new RegExp(`"${old}"`,'g'),`"${modern}"`);
  s=s.split('\n').filter(line=>!/^\s*recruit_pool "pru_gardegrenadiere_(?:early|mid|high)"/.test(line)).join('\n');
  const edb=[];
  for(const line of s.split('\n')){
    edb.push(line);
    if(/^\s*recruit_pool "pru_fusiliere_early"/.test(line) && /requires factions \{ hre, \}/.test(line) && !/factions \{ all, \}/.test(line)){
      let guard=line.replace('"pru_fusiliere_early"','"pru_gardegrenadiere_early"').replace(/(recruit_pool "pru_gardegrenadiere_early"\s+)[\d.]+\s+[\d.]+\s+[\d.]+/,(_,a)=>`${a}${/;resupply/.test(edb.slice(-20).join('\n'))?'0.2   0.02   0.2':'0   0.01   1'}`);
      edb.push(guard);
    }
    if(/^\s*recruit_pool "pru_jaeger_mid"/.test(line) && /requires factions \{ hre, \}/.test(line)){
      let guard=line.replace('"pru_jaeger_mid"','"pru_gardegrenadiere_mid"').replace(/hidden_resource prussia or hidden_resource bavaria or hidden_resource hanover/g,'hidden_resource prussia');
      edb.push(guard);
    }
    if(/^\s*recruit_pool "pru_fusiliere_high"/.test(line) && /requires factions \{ hre, \}/.test(line) && !/factions \{ all, \}/.test(line)){
      let guard=line.replace('"pru_fusiliere_high"','"pru_gardegrenadiere_high"').replace(/(recruit_pool "pru_gardegrenadiere_high"\s+)[\d.]+\s+[\d.]+\s+[\d.]+/,(_,a)=>`${a}${/;resupply/.test(edb.slice(-20).join('\n'))?'0.2   0.02   0.2':'0   0.01   1'}`);
      edb.push(guard);
    }
  }
  fs.writeFileSync(p,edb.join('\n'));
}

function modelEntry(text,name){const lines=text.replace(/\r\n/g,'\n').split('\n');const head=new RegExp(`^${name.length} ${name}\\s*$`);const i=lines.findIndex(x=>head.test(x));if(i<0)throw new Error(`Missing model donor ${name}`);let j=i;while(j<lines.length&&!/^16 -0\.090000004 /.test(lines[j]))j++;if(j===lines.length)throw new Error(`Bad model donor ${name}`);return lines.slice(i,j+1).join('\n');}
function clone(text,donor,name,mode){let e=modelEntry(text,donor).replace(new RegExp(`^${donor.length} ${donor}\\s*$`,'m'),`${name.length} ${name} `);if(mode==='musket')e=e.replace(/20 MTW2_Fast_Arquebus_3 9 MTW2_Pike /,'14 MTW2_Musket_SS 9 MTW2_Pike ');if(mode==='skirmisher')e=e.replace(/(?:20 MTW2_Fast_Arquebus_3|14 MTW2_Musket_SS) 9 MTW2_Pike /,'15 MTW2_Musket_SSK 9 MTW2_Pike ');if(mode==='fast')e=e.replace(/(?:14 MTW2_Musket_SS|15 MTW2_Musket_SSK) 9 MTW2_Pike /,'20 MTW2_Fast_Arquebus_3 9 MTW2_Pike ');return e;}
function copyMountedWeaponSetup(target,donor){const tail=e=>{const m=e.match(/\n1\s*\n5 Horse\s*\n[\s\S]*$/);if(!m)throw new Error('Missing mounted weapon setup');return m[0];};return target.replace(tail(target),tail(donor));}
const donors={
  pru_fusiliere_early:['siam_riflemen_gr','musket'],pru_fusiliere_mid:['siam_riflemen_gr','musket'],pru_fusiliere_high:['gr_inf','fast'],
  pru_pioniere_early:['gr_gren','musket'],pru_pioniere_mid:['gr_gren','musket'],pru_pioniere_high:['gr_gren','fast'],
  pru_gardegrenadiere_early:['gr_gren','musket'],pru_gardegrenadiere_mid:['pru_gardegrenadiere_early','musket'],pru_gardegrenadiere_high:['pru_gardegrenadiere_mid','fast'],
  pru_jaeger_early:['bav_inf','skirmisher'],pru_jaeger_mid:['bav_inf','skirmisher'],pru_jaeger_high:['bav_inf','skirmisher'],
  pru_seesoldaten_early:['siam_riflemen_gr','musket'],pru_seesoldaten_mid:['gr_sailor','musket'],pru_seesoldaten_high:['gr_sailor','fast'],
  pru_wuerttemberg_mid:['wurt_inf','musket'],pru_wuerttemberg_high:['wurt_inf','fast'],pru_bavarian_fusiliere_mid:['aus_inf3','musket'],pru_bavarian_fusiliere_high:['aus_inf3','fast'],
  pru_bavarian_landwehr_mid:['rec_bav','musket'],pru_bavarian_landwehr_high:['rec_bav','musket'],pru_hannover_mid:['hannover_inf','musket'],pru_hannover_high:['hannover_inf','fast'],
  pru_sturmpioniere_high:['pru_ww1_gren','fast'],pru_schutztruppe_high:['gr_colonial','skirmisher'],pru_sturmtruppen_high:['pru_ww1_inf',null],
  pru_kuerassiere:['otto_sipahi',null],pru_husaren:['balk_cav1',null],pru_dragoner_early:['gr_carbs',null],pru_dragoner_mid:['gr_carbs',null],pru_dragoner_high:['gr_carbs',null],
  pru_kolonialreiter_high:['gr_lancer',null],pru_general_staff:['otto_sipahi',null]
};
let model=fs.readFileSync(modelPath,'utf8').replace(/\r\n/g,'\n');const missing=[];
for(const [name,[donor,mode]] of Object.entries(donors))if(!new RegExp(`^${name.length} ${name} $`,'m').test(model)){
  model=model.trimEnd()+'\n'+clone(model,donor,name,mode)+'\n';
  missing.push([name,[donor,mode]]);
}
if(missing.length){const h=model.match(/^(22 serialization::archive 3 0 0 0 0 )(\d+)( 0 0 )/);if(!h)throw new Error('Bad model header');model=model.replace(h[0],`${h[1]}${+h[2]+missing.length}${h[3]}`);}
for(const [name,[donor,mode]] of Object.entries({pru_general_staff:['otto_sipahi',null]}))model=model.replace(modelEntry(model,name),clone(model,donor,name,mode));
model=model.replace(modelEntry(model,'pru_husaren'),copyMountedWeaponSetup(modelEntry(model,'pru_husaren'),modelEntry(model,'fra_hussards')));
fs.writeFileSync(modelPath,model.replace(/\n/g,'\r\n'));

const all=[...inf,{type:'pru_sturmtruppen_high',label:'Sturmtruppen',period:'high',weapon:'Handgranaten'},...cav];
let buf=fs.readFileSync(locPath);const bom=buf[0]===255&&buf[1]===254;let loc=buf.slice(bom?2:0).toString('utf16le').replace(/\r\n/g,'\n');
const legacyLocalized=Object.entries(legacyMap).map(([type,[modern]])=>({...all.find(u=>u.type===modern),type}));
const localized=[...all,...legacyLocalized];
for(const u of localized)loc=loc.replace(new RegExp(`^\\{${u.type}(?:_descr|_descr_short)?\\}.*(?:\\n|$)`,'gm'),'');
loc=loc.trimEnd()+'\n\n'+localized.map(u=>`{${u.type}}${u.label}${u.period?` (${periodName(u.period)})`:''}\n{${u.type}_descr}${u.label} serve in the German armed forces and are equipped and trained for their stated battlefield role.\n{${u.type}_descr_short}${u.label}${u.weapon?` (${u.weapon})`:''}`).join('\n\n')+'\n';
fs.writeFileSync(locPath,Buffer.concat([Buffer.from([255,254]),Buffer.from(loc.replace(/\n/g,'\r\n'),'utf16le')]));

const cardSources={};for(const [old,[modern]] of Object.entries(legacyMap))if(!cardSources[modern])cardSources[modern]=old;
for(const u of all){let source=cardSources[u.type];if(!source){if(u.type.startsWith('pru_fusiliere_'))source=u.period==='high'?'gr_inf':'siam_riflemen_gr';else if(u.type.startsWith('pru_pioniere_'))source='gr_gren';else if(u.type==='pru_gardegrenadiere_early')source='gr_gren';else if(u.type==='pru_gardegrenadiere_mid')source='pru_gardegrenadiere_early';else if(u.type==='pru_gardegrenadiere_high')source='pru_gardegrenadiere_mid';else if(u.type.startsWith('pru_jaeger_'))source='bav_inf';else if(u.type.startsWith('pru_seesoldaten_'))source='gr_sailor';else if(u.type==='pru_wuerttemberg_high')source='wurt_inf';else if(u.type==='pru_bavarian_fusiliere_high')source='jager_inf';else if(u.type==='pru_bavarian_landwehr_high')source='rec_bav';else if(u.type==='pru_hannover_high')source='hannover_inf';else if(u.type.startsWith('pru_dragoner_'))source='gr_carbs';}
  if(!source)continue;
  const unitDir=path.join(root,'data/ui/units/hre'),infoDir=path.join(root,'data/ui/unit_info/hre');
  const card=path.join(unitDir,`#${source}.tga`),info=path.join(infoDir,`${source}_info.tga`);
  if(fs.existsSync(card))fs.copyFileSync(card,path.join(unitDir,`#${u.type}.tga`));
  const infoFallback=u.type==='pru_gardegrenadiere_early'?path.join(infoDir,'pru_fusiliere_early_info.tga'):info;
  if(fs.existsSync(infoFallback))fs.copyFileSync(infoFallback,path.join(infoDir,`${u.type}_info.tga`));
}

let soundRaw=fs.readFileSync(soundPath,'utf8');const soundEol=soundRaw.includes('\r\n')?'\r\n':'\n';let sounds=soundRaw.replace(/\r\n/g,'\n');
const template=sounds.match(/(^\s*unit siam_riflemen_gr\n\s*event\n\s*folder data\/sounds\/Voice\/Human\/Localized\/Battle_Map\/prussian\n(?:\s+[^\n]+\.wav\n)+\s*end)/m);
if(!template)throw new Error('Missing Prussian sound template');
const indent=template[1].match(/^(\s*)unit/m)[1];const soundBlocks=all.filter(u=>!new RegExp(`^\\s*unit ${u.type}$`,'m').test(sounds)).map(u=>template[1].replace(`${indent}unit siam_riflemen_gr`,`${indent}unit ${u.type}`));
if(soundBlocks.length){sounds=sounds.replace(template[1],template[1]+'\n'+soundBlocks.join('\n'));fs.writeFileSync(soundPath,sounds.replace(/\n/g,soundEol));}

const finalEdu=fs.readFileSync(eduCanonical,'utf8');const types=[...finalEdu.matchAll(/^type\s+(.+)$/gm)].map(m=>m[1].trim());const dict=[...finalEdu.matchAll(/^dictionary\s+(\S+)/gm)].map(m=>m[1]);
const dup=a=>a.filter((x,i)=>a.indexOf(x)!==i);if(dup(types).length||dup(dict).length)throw new Error('Duplicate EDU identifiers');
for(const name of Object.keys(donors))if(([...model.matchAll(new RegExp(`^${name.length} ${name} $`,'gm'))]).length!==1)throw new Error(`Bad model count ${name}`);
if(!fs.readFileSync(eduCanonical).equals(fs.readFileSync(eduRuntime)))throw new Error('EDU mirrors differ');
console.log(`Standardized ${all.length} Prussian records and added ${missing.length} model entries.`);
