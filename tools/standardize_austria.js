const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const eduC=path.join(root,'data/tow_steamsteel/export_descr_unit.txt');
const eduR=path.join(root,'data/export_descr_unit.txt');
const modelP=path.join(root,'data/unit_models/battle_models.modeldb');
const locP=path.join(root,'data/text/export_units.txt');
const soundP=path.join(root,'data/export_descr_sounds_units_voice.txt');
const unitDir=path.join(root,'data/ui/units/hungary');
const infoDir=path.join(root,'data/ui/unit_info/hungary');
const archiveDir=path.join(root,'tools/card_source_archive/austria_before_standardization');

const E={early:{n:0,name:'Early',form:'1.2, 1.2, 1.2, 1.2, 3, square'},mid:{n:1,name:'Mid',form:'1.2, 1.2, 2.0, 2.4, 3, square'},high:{n:2,name:'Late',form:'1.2, 1.4, 2.4, 2.8, 3, square'}};
const W={
  lorenz:{name:'Lorenz Infanteriegewehr M1854',damage:37,family:'rifled_musket',range:220,ammo:35,smoke:'musket_shot_set',base:1200,muzzle:true},
  lorenzJ:{name:'Lorenz Jaegerstutzen M1854',damage:37,family:'rifled_musket',range:220,ammo:35,smoke:'musket_shot_set',base:1200,muzzle:true},
  wanzl:{name:'Waenzl-Gewehr M1867 conversion',damage:37,family:'rifled_musket',range:220,ammo:35,smoke:'musket_shot_set',base:1200},
  werndl:{name:'Werndl-Holub-Gewehr M1867',damage:29,family:'rifle',range:240,ammo:35,smoke:'musket_shot_set',base:1500},
  mann88:{name:'Mannlicher-Gewehr M1888/90',damage:13,family:'magazine_rifle',range:260,ammo:40,smoke:'smokeless_shot_set',base:1800},
  mann95:{name:'Mannlicher-Gewehr M1895',damage:13,family:'magazine_rifle',range:260,ammo:40,smoke:'smokeless_shot_set',base:1800}
};
const CW={
  early:{name:'Lorenz Kavalleriekarabiner M1854',damage:37,family:'rifled_musket_carbine',range:200,ammo:35,smoke:'musket_shot_set',base:1400,muzzle:true},
  mid:{name:'Werndl Kavalleriekarabiner M1867',damage:29,family:'rifle_carbine',range:220,ammo:35,smoke:'musket_shot_set',base:1700},
  high:{name:'Mannlicher Kavalleriekarabiner M1890',damage:13,family:'magazine_rifle_carbine',range:240,ammo:40,smoke:'smokeless_shot_set',base:2000}
};
const infantry=[];
function add(type,label,p,w,donor,card,opts={}){infantry.push({type,label,p,w,donor,card,role:'line',limit:1,...opts});}
add('aus_line_early','k.k. Linieninfanterie','early',W.lorenz,'ah_inf','dutch_militia',{limit:3});
add('aus_line_mid','k.u.k. Infanterie','mid',W.werndl,'aus_line_early','dutch_militia',{limit:3});
add('aus_line_high','k.u.k. Infanterie','high',W.mann88,'aus_line_mid','dutch_militia',{limit:3});
add('aus_kaiserjaeger_early','Kaiserjaeger','early',W.lorenzJ,'ah_jag','kaiserjager',{role:'skirmisher'});
add('aus_kaiserjaeger_mid','Kaiserjaeger','mid',W.werndl,'aus_kaiserjaeger_early','kaiserjager',{role:'skirmisher'});
add('aus_kaiserjaeger_high','Kaiserjaeger','high',W.mann95,'aus_kaiserjaeger_mid','kaiserjager',{role:'skirmisher'});
add('aus_grenz_early','Grenzinfanterie','early',W.lorenzJ,'ah_scout','aus_inf2',{role:'skirmisher'});
add('aus_landwehr_mid','k.k. Landwehr','mid',W.wanzl,'dutch_militia','aus_jag');
add('aus_landwehr_high','k.k. Landwehr','high',W.mann88,'aus_landwehr_mid','aus_jag');
add('aus_honved_mid','k.u. Honved','mid',W.wanzl,'rom_inf','rom_inf');
add('aus_honved_high','k.u. Honved','high',W.mann88,'aus_honved_mid','rom_inf');
add('aus_bosniak_mid','Bosnisch-herzegowinische Infanterie','mid',W.werndl,'rom_guard','rom_guard_hungary');
add('aus_bosniak_high','Bosnisch-herzegowinische Infanterie','high',W.mann95,'aus_bosniak_mid','rom_guard_hungary');
add('aus_matrosen_early','Matrosenkorps','early',W.lorenz,'fra_sailors','austro_sailor');
add('aus_matrosen_mid','Matrosenkorps','mid',W.werndl,'aus_matrosen_early','austro_sailor');
add('aus_matrosen_high','Matrosenkorps','high',W.mann88,'aus_matrosen_mid','austro_sailor');
const cavalry=[
  {type:'aus_kuerassiere',label:'Kuerassiere',kind:'cuirass',donor:'dan_cuirassier',card:'rus_imp_cav_hu',eras:[0]},
  ...['early','mid','high'].map(p=>({type:`aus_dragoner_${p}`,label:'Dragoner',kind:'carbine',p,w:CW[p],donor:p==='early'?'dan_cav':`aus_dragoner_${p==='mid'?'early':'mid'}`,card:'dan_cav_hungary',eras:[E[p].n]})),
  {type:'aus_husaren',label:'Husaren',kind:'pistol',donor:'fra_hussar',card:'aus_ulhans',eras:[0,1,2]},
  {type:'aus_ulanen',label:'Ulanen',kind:'lance',donor:'aus_lancers',card:'aus_lancers',eras:[0,1,2]},
  {type:'aus_general_staff',label:'General und Stab',kind:'general',donor:'fra_hussar',card:'rom_cav_hungary',eras:[0,1,2]}
];

const upkeep=n=>Math.round(n/3);
const cost=(n,limit=1)=>`3, ${n}, ${upkeep(n)}, 100, 100, ${n}, ${limit}, ${upkeep(n)}`;
function infRecord(u){
  const a=u.w,skirm=u.role==='skirmisher',attrs=['free_upkeep_unit','sea_faring','hide_forest'];
  if(skirm)attrs.push('can_withdraw');
  if(a.muzzle)attrs.push('gunpowder_unit');
  attrs.push('gunmen','start_not_skirmishing');
  if(!skirm)attrs.push('cannot_skirmish');
  if(u.p==='high')attrs.push('stakes');
  const projectile=skirm?'a':'b',range=a.range+(skirm?40:0);
  return [`type             ${u.type}`,`dictionary       ${u.type} ; ${u.label} (${E[u.p].name}; ${a.name})`,'category         infantry','class            missile','voice_type       Light','accent           german','banner faction   main_infantry','banner holy      crusade',`soldier          ${u.type}, ${skirm?30:40}, 0, 1.2`,'officer          shk_off_1g',...(u.p!=='high'?['officer          BRIT_FootA_Bearer1']:[]),`attributes       ${attrs.join(', ')}`,`formation        ${skirm?'1.4, 1.8, 2.8, 3.6, 3, square':E[u.p].form}`,'stat_health      1, 0',`stat_pri         ${a.damage}, 0, ${a.family}_bullet_${projectile}, ${range}, ${a.ammo}, missile, missile_gunpowder, piercing, none, ${a.smoke}, 0, -999`,'stat_pri_attr    ap','stat_sec         6, 3, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1.2','stat_sec_attr    short_pike, ap','stat_pri_armour  3, 4, 0, leather','stat_sec_armour  0, 0, flesh','stat_heat        0','stat_ground      0, 0, 0, 0','stat_mental      4, normal, trained','stat_charge_dist 40','stat_fire_delay  0','stat_food        60, 300',`stat_cost        ${cost(a.base,u.limit)}`,'ownership        hungary, slave',`era ${E[u.p].n}            hungary`].join('\n');
}
function cavRecord(u){
  const carbine=u.kind==='carbine',pistol=['pistol','cuirass','general'].includes(u.kind),lance=u.kind==='lance',cuir=u.kind==='cuirass',general=u.kind==='general';
  const attrs=['free_upkeep_unit','sea_faring','hide_forest','can_withdraw'];
  if(carbine||pistol)attrs.push('guncavalry','gunmen','start_not_skirmishing','cannot_skirmish');
  if(carbine&&u.p==='early')attrs.push('gunpowder_unit');
  if(carbine&&u.p==='high')attrs.push('stakes');
  if(general)attrs.push('general_unit','command');
  const pri=carbine?`${u.w.damage}, 2, ${u.w.family}_bullet_c, ${u.w.range}, ${u.w.ammo}, missile, missile_gunpowder, piercing, none, ${u.w.smoke}, 25, 1`:pistol?'20, 4, magazine_rifle_bullet_c, 60, 15, missile, missile_gunpowder, piercing, none, musket_shot_set, 25, 1':'6, 6, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1';
  const melee=cuir||general?8:6,charge=cuir||general?4:3,def=cuir?6:5,morale=cuir||general?6:4,disc=cuir||general?'disciplined':'normal',training=cuir||general?'highly_trained':'trained';
  const total=general?200:carbine?u.w.base:cuir?1700:pistol?1200:1200;
  const armour=cuir?'7, 6, 0, metal':`4, ${def}, 0, leather`;
  const label=u.p?`${u.label} (${E[u.p].name}; ${u.w.name} und Saebel)`:u.kind==='lance'?`${u.label} (Lanze und Saebel)`:u.kind==='cuirass'?`${u.label} (Gasser-Revolver M1870 und Saebel)`:u.kind==='general'?`${u.label} (Gasser-Revolver M1870 und Saebel)`:`${u.label} (Gasser-Revolver M1870 und Saebel)`;
  return [`type             ${u.type}`,`dictionary       ${u.type} ; ${label}`,'category         cavalry',`class            ${carbine?'missile':cuir?'heavy':'light'}`,'voice_type       Heavy','accent           german','banner faction   main_cavalry','banner holy      crusade_cavalry',`soldier          ${u.type}, ${general?4:24}, 0, 1`,'officer          shk_off_1g',`mount            ${carbine?'dragoon':'hussar'}`,'mount_effect     elephant -4, camel -4',`attributes       ${attrs.join(', ')}`,`formation        2, 2, 4, 4, ${general?2:3}, square`,'stat_health      1, 0',`stat_pri         ${pri}`,`stat_pri_attr    ${lance?'spear, ap':'ap'}`,`stat_sec         ${melee}, ${charge}, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1`,'stat_sec_attr    ap',`stat_pri_armour  ${armour}`,'stat_sec_armour  0, 0, flesh','stat_heat        0','stat_ground      0, 0, 0, 0',`stat_mental      ${morale}, ${disc}, ${training}`,'stat_charge_dist 45','stat_fire_delay  0','stat_food        60, 300',`stat_cost        ${cost(total)}`,'ownership        hungary, slave',...u.eras.map(e=>`era ${e}            hungary`)].join('\n');
}

const oldTypes=['merc_pol_hussars','merc_polish_inf','fra_sailors_hungary','dan_cav_hungary','rom_cav_hungary','rom_guard_hungary','dutch_militia','rom_inf','it_royals_hungary','aus_jag','austro_sailor','aus_lancers','aus_ulhans','aus_inf2','aus_inf3','balk_cav','kaiserjager','bulgarian_inf','merc_bulgarian_inf'];
function stripHungary(b){
  b=b.replace(/^ownership\s+(.+)$/m,(m,x)=>{const a=x.split(',').map(y=>y.trim()).filter(y=>y&&y!=='hungary');return a.length?`ownership        ${a.join(', ')}`:'';});
  b=b.replace(/^era ([012])\s+(.+)$/gm,(m,e,x)=>{const a=x.split(',').map(y=>y.trim()).filter(y=>y&&y!=='hungary');return a.length?`era ${e}            ${a.join(', ')}`:'';});
  return b.replace(/\n{3,}/g,'\n\n');
}
let edu=fs.readFileSync(eduC,'utf8').replace(/\r\n/g,'\n');
const begin='; BEGIN STANDARDIZED AUSTRIA-HUNGARY',end='; END STANDARDIZED AUSTRIA-HUNGARY';
if(edu.includes(begin)){const a=edu.indexOf(begin),z=edu.indexOf(end,a);if(z<0)throw Error('Unclosed Austrian block');edu=edu.slice(0,a)+edu.slice(z+end.length).replace(/^\s*/,'');}
const starts=[...edu.matchAll(/^type\s+(\S+)/gm)],parts=[edu.slice(0,starts[0].index)];
for(let i=0;i<starts.length;i++){const t=starts[i][1],z=i+1<starts.length?starts[i+1].index:edu.length;let b=edu.slice(starts[i].index,z);if(oldTypes.includes(t))b=stripHungary(b);parts.push(b);}edu=parts.join('');
const roster=[...infantry.map(infRecord),...cavalry.map(cavRecord)];
const insertion=`${begin}\n\n${roster.join('\n\n')}\n\n${end}\n\n`;
const at=edu.indexOf('type             merc_pol_hussars');if(at<0)throw Error('Austrian insertion point missing');edu=edu.slice(0,at)+insertion+edu.slice(at);
function replaceType(text,type,replacement){const s=[...text.matchAll(/^type\s+(\S+)/gm)],i=s.findIndex(x=>x[1]===type);if(i<0)throw Error(`Missing legacy Austrian type ${type}`);return text.slice(0,s[i].index)+replacement+'\n\n'+text.slice(i+1<s.length?s[i+1].index:text.length);}
const byType=Object.fromEntries([...infantry.map(u=>[u.type,infRecord(u)]),...cavalry.map(u=>[u.type,cavRecord(u)])]);
const aliases={fra_sailors_hungary:'aus_matrosen_mid',dan_cav_hungary:'aus_dragoner_early',rom_cav_hungary:'aus_dragoner_high',rom_guard_hungary:'aus_bosniak_mid',dutch_militia:'aus_line_early',rom_inf:'aus_honved_mid',aus_jag:'aus_line_high',austro_sailor:'aus_matrosen_mid',aus_lancers:'aus_ulanen',aus_ulhans:'aus_general_staff',aus_inf2:'aus_landwehr_mid',aus_inf3:'aus_kaiserjaeger_high',balk_cav:'aus_husaren',kaiserjager:'aus_grenz_early'};
for(const [old,modern] of Object.entries(aliases)){const a=byType[modern].replace(/^type\s+.*$/m,`type             ${old}`).replace(/^dictionary\s+\S+.*$/m,`dictionary       ${old}`).replace(/^soldier\s+\S+,/m,`soldier          ${modern},`).replace(/^ownership\s+.*$/m,'ownership        slave').replace(/^era [012]\s+.*\n?/gm,'').trimEnd();edu=replaceType(edu,old,a);}
const out=edu.replace(/\n/g,'\r\n');fs.writeFileSync(eduC,out);fs.writeFileSync(eduR,out);

function modelEntry(text,name){const a=text.replace(/\r\n/g,'\n').split('\n'),i=a.findIndex(x=>new RegExp(`^${name.length} ${name}\\s*$`).test(x));if(i<0)throw Error(`Missing Austrian model donor ${name}`);let j=i;while(j<a.length&&!/^16 -0\.090000004 /.test(a[j]))j++;return a.slice(i,j+1).join('\n');}
function cloneModel(text,donor,name,mode,kind){let e=modelEntry(text,donor).replace(new RegExp(`^${donor.length} ${donor}\\s*$`,'m'),`${name.length} ${name} `);if(mode==='line')e=e.replace(/(?:20 MTW2_Fast_Arquebus_3|15 MTW2_Musket_SSK|17 MTW2_Flamethrower) 9 MTW2_Pike /,'14 MTW2_Musket_SS 9 MTW2_Pike ');if(mode==='skirmisher')e=e.replace(/(?:20 MTW2_Fast_Arquebus_3|14 MTW2_Musket_SS|17 MTW2_Flamethrower) 9 MTW2_Pike /,'15 MTW2_Musket_SSK 9 MTW2_Pike ');if(mode==='fast')e=e.replace(/(?:14 MTW2_Musket_SS|15 MTW2_Musket_SSK|17 MTW2_Flamethrower) 9 MTW2_Pike /,'20 MTW2_Fast_Arquebus_3 9 MTW2_Pike ');if(['pistol','general'].includes(kind))e=e.replace(/13 MTW2_HR_Spear /g,'13 MTW2_HR_Sword ').replace(/21 MTW2_HR_spear_Primary/g,'18 MTW2_Sword_Primary');if(kind==='cuirass')e=e.replace(/^6 sicily\s*$/gm,'7 hungary ');if(kind)e=e.replace(/^\d+ unit_sprites\/[^\s]+_sprite\.spr\s*$/gm,'35 unit_sprites/tmp_cavalry_sprite.spr ');return e;}
let model=fs.readFileSync(modelP,'utf8').replace(/\r\n/g,'\n'),added=0;
for(const u of infantry){const mode=u.w.muzzle?'fast':u.role==='skirmisher'?'skirmisher':u.p==='high'?'fast':'line',fresh=cloneModel(model,u.donor,u.type,mode);if(new RegExp(`^${u.type.length} ${u.type} $`,'m').test(model))model=model.replace(modelEntry(model,u.type),fresh);else{model=model.trimEnd()+'\n'+fresh+'\n';added++;}}
for(const u of cavalry){const fresh=cloneModel(model,u.donor,u.type,null,u.kind);if(new RegExp(`^${u.type.length} ${u.type} $`,'m').test(model))model=model.replace(modelEntry(model,u.type),fresh);else{model=model.trimEnd()+'\n'+fresh+'\n';added++;}}
if(added){const h=model.match(/^(22 serialization::archive 3 0 0 0 0 )(\d+)( 0 0 )/);if(!h)throw Error('Bad modeldb header');model=model.replace(h[0],`${h[1]}${+h[2]+added}${h[3]}`);}fs.writeFileSync(modelP,model.replace(/\n/g,'\r\n'));

const display={Kaiserjaeger:'Kaiserjäger',Kuerassiere:'Kürassiere','k.u. Honved':'k.u. Honvéd'};
const shown=s=>display[s]||s;
let lb=fs.readFileSync(locP),loc=lb.slice(lb[0]===255&&lb[1]===254?2:0).toString('utf16le').replace(/\r\n/g,'\n');
for(const u of [...infantry,...cavalry])for(const k of [u.type,`${u.type}_descr`,`${u.type}_descr_short`])loc=loc.replace(new RegExp(`^\\{${k}\\}.*(?:\\n|$)`,'gm'),'');
const entries=[...infantry.map(u=>{const n=shown(u.label),period=E[u.p].name,role=u.role==='skirmisher'?'light infantry':'infantry';return `{${u.type}}${n} (${period})\n{${u.type}_descr}${n} serve as ${role} of the Habsburg forces, equipped and organized for the ${period.toLowerCase()} period.\n{${u.type}_descr_short}${n} (${u.w.name})`;}),...cavalry.map(u=>{const n=shown(u.label),period=u.p?` (${E[u.p].name})`:'';const equip=u.kind==='carbine'?`${u.w.name} und Säbel`:u.kind==='lance'?'Lanze und Säbel':u.kind==='general'?'mounted command staff; Gasser-Revolver M1870 holstered':'Gasser-Revolver M1870 und Säbel';return `{${u.type}}${n}${period}\n{${u.type}_descr}${n} serve in the mounted arm of the Habsburg forces.\n{${u.type}_descr_short}${n} (${equip})`;})];
loc=loc.trimEnd()+'\n\n'+entries.join('\n\n')+'\n';fs.writeFileSync(locP,Buffer.concat([Buffer.from([255,254]),Buffer.from(loc.replace(/\n/g,'\r\n'),'utf16le')]));

fs.mkdirSync(archiveDir,{recursive:true});fs.mkdirSync(unitDir,{recursive:true});
for(const source of new Set([...infantry.map(u=>u.card),...cavalry.map(u=>u.card)])){const src=path.join(unitDir,`#${source}.tga`),arc=path.join(archiveDir,`#${source}.tga`);if(!fs.existsSync(src))throw Error(`Missing Austrian card donor ${source}`);if(!fs.existsSync(arc))fs.copyFileSync(src,arc);}
for(const u of [...infantry,...cavalry]){const src=path.join(unitDir,`#${u.card}.tga`),dst=path.join(unitDir,`#${u.type}.tga`);if(!fs.existsSync(dst))fs.copyFileSync(src,dst);}

let sounds=fs.readFileSync(soundP,'utf8').replace(/\r\n/g,'\n');const tmpl=sounds.match(/(^\s*unit aus_jag\n\s*event\n\s*folder[^\n]+\n(?:\s+[^\n]+\.wav\n)+\s*end)/m);if(tmpl){const indent=tmpl[1].match(/^(\s*)unit/m)[1],adds=[...infantry,...cavalry].filter(u=>!new RegExp(`^\\s*unit ${u.type}$`,'m').test(sounds)).map(u=>tmpl[1].replace(`${indent}unit aus_jag`,`${indent}unit ${u.type}`));if(adds.length)sounds=sounds.replace(tmpl[1],tmpl[1]+'\n'+adds.join('\n'));fs.writeFileSync(soundP,sounds.replace(/\n/g,'\r\n'));}
if(!fs.readFileSync(eduC).equals(fs.readFileSync(eduR)))throw Error('Austrian EDU mirrors differ');console.log(`Standardized ${infantry.length+cavalry.length} Austrian records; added ${added} model entries.`);
