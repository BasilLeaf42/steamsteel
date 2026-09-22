const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const eduC=path.join(root,'data/tow_steamsteel/export_descr_unit.txt');
const eduR=path.join(root,'data/export_descr_unit.txt');
const modelP=path.join(root,'data/unit_models/battle_models.modeldb');
const locP=path.join(root,'data/text/export_units.txt');
const unitDir=path.join(root,'data/ui/units/turks');
const archiveDir=path.join(root,'tools/card_source_archive/ottomans_before_standardization');

const E={early:{n:0,name:'Early',form:'1.2, 1.2, 1.2, 1.2, 3, square'},mid:{n:1,name:'Mid',form:'1.2, 1.2, 2.0, 2.4, 3, square'},high:{n:2,name:'Late',form:'1.2, 1.4, 2.4, 2.8, 3, square'}};
const W={
  musket:{name:'Ottoman Model 1847 percussion musket',damage:37,family:'musket',range:200,ammo:35,smoke:'musket_shot_set',base:1000,muzzle:true},
  minie:{name:'Pattern 1851 Minié rifle-musket',damage:37,family:'rifled_musket',range:220,ammo:35,smoke:'musket_shot_set',base:1200,muzzle:true},
  snider:{name:'Snider–Enfield conversion rifle',damage:29,family:'rifle',range:240,ammo:35,smoke:'musket_shot_set',base:1500},
  peabody:{name:'Peabody–Martini M1874 rifle',damage:21,family:'rifle',range:240,ammo:35,smoke:'musket_shot_set',base:1500},
  mauser:{name:'Mauser M1890 magazine rifle',damage:13,family:'magazine_rifle',range:260,ammo:40,smoke:'smokeless_shot_set',base:1800}
};
const CW={
  early:{name:'Pattern 1853 Enfield cavalry carbine',damage:37,family:'rifled_musket_carbine',range:200,ammo:35,smoke:'musket_shot_set',base:1400,muzzle:true},
  mid:{name:'Winchester Model 1866 carbine',damage:20,family:'rifle_carbine',range:220,ammo:35,smoke:'musket_shot_set',base:1700},
  high:{name:'Mauser M1893 cavalry carbine',damage:13,family:'magazine_rifle_carbine',range:240,ammo:40,smoke:'smokeless_shot_set',base:2000}
};

const infantry=[];
function add(type,label,p,w,donor,card,opts={}){infantry.push({type,label,p,w,donor,card,role:'line',quality:'regular',limit:1,...opts});}
add('ott_nizamiye_early','Nizamiye','early',W.minie,'otto_jan_inf','otto_jan_inf',{limit:3});
add('ott_nizamiye_mid','Nizamiye','mid',W.peabody,'ott_nizamiye_early','otto_jan_inf',{limit:3});
add('ott_nizamiye_high','Nizamiye','high',W.mauser,'ott_nizamiye_mid','otto_jan_inf',{limit:3});
add('ott_redif_early','Redif','early',W.musket,'arab_sailors','otto_militia',{quality:'militia',limit:2});
add('ott_redif_mid','Redif','mid',W.snider,'ott_redif_early','otto_militia',{quality:'militia',limit:2});
add('ott_redif_high','Redif','high',W.peabody,'ott_redif_mid','otto_militia',{quality:'militia',limit:2});
add('ott_avci_early','Avcı','early',W.minie,'turk_lt2','__generated_avci__',{role:'skirmisher'});
add('ott_avci_mid','Avcı','mid',W.peabody,'ott_avci_early','__generated_avci__',{role:'skirmisher'});
add('ott_avci_high','Avcı','high',W.mauser,'ott_avci_mid','__generated_avci__',{role:'skirmisher'});
add('ott_hassa_early','Hassa Piyadesi','early',W.minie,'otto_jan_inf','us_zouave_tu',{quality:'elite'});
add('ott_hassa_mid','Hassa Piyadesi','mid',W.peabody,'ott_hassa_early','us_zouave_tu',{quality:'elite'});
add('ott_hassa_high','Hassa Piyadesi','high',W.mauser,'ott_hassa_mid','us_zouave_tu',{quality:'elite'});
add('ott_bahriye_early','Bahriye Piyadesi','early',W.minie,'arab_sailors','uk_sailor_tu');
add('ott_bahriye_mid','Bahriye Piyadesi','mid',W.snider,'ott_bahriye_early','uk_sailor_tu');
add('ott_bahriye_high','Bahriye Piyadesi','high',W.mauser,'ott_bahriye_mid','uk_sailor_tu');
add('ott_mustahfiz_early','Müstahfız','early',W.musket,'otto_jan_inf','arab_brigade',{quality:'militia'});
add('ott_mustahfiz_mid','Müstahfız','mid',W.snider,'ott_mustahfiz_early','arab_brigade',{quality:'militia'});

const cavalry=[
  ...['early','mid','high'].map(p=>({type:`ott_suvari_${p}`,label:'Süvari',kind:'carbine',p,w:CW[p],donor:p==='early'?'otto_cav':`ott_suvari_${p==='mid'?'early':'mid'}`,card:'__generated_suvari__',eras:[E[p].n],quality:'regular'})),
  {type:'ott_hassa_suvarisi',label:'Hassa Süvarisi',kind:'pistol',donor:'otto_cav',card:'__generated_hassa_suvarisi__',eras:[0,1,2],quality:'elite'},
  {type:'ott_mizrakli_suvari',label:'Mızraklı Süvari',kind:'lance',donor:'rus_georgian_cav',card:'__generated_mizrakli__',eras:[0,1,2],quality:'regular'},
  {type:'ott_ertugrul_suvari',label:'Ertuğrul Süvari Alayı',kind:'carbine',p:'high',w:CW.high,donor:'rus_guard_cav',card:'turk_lt',eras:[2],quality:'elite'},
  {type:'ott_general_staff',label:'General ve Erkân-ı Harbiye',kind:'general',donor:'turk_lt',card:'__generated_general__',eras:[0,1,2],quality:'elite'}
];

const upkeep=n=>Math.round(n/3);
const cost=(n,limit=1)=>`3, ${n}, ${upkeep(n)}, 100, 100, ${n}, ${limit}, ${upkeep(n)}`;
const q={militia:{melee:2,charge:1,def:2,morale:3,disc:'low',training:'trained',proj:'c',cost:-200},regular:{melee:4,charge:2,def:3,morale:4,disc:'low',training:'trained',proj:'c',cost:0},elite:{melee:6,charge:3,def:4,morale:6,disc:'normal',training:'highly_trained',proj:'b',cost:200}};
function infRecord(u){
  const a=u.w,v=q[u.quality],skirm=u.role==='skirmisher',attrs=['free_upkeep_unit','sea_faring','hide_forest'];
  const officers=['officer          fez_off_1g'];if(u.p!=='high')officers.push('officer          ott_standard_bearer');
  if(skirm)attrs.push('can_withdraw'); if(a.muzzle)attrs.push('gunpowder_unit'); attrs.push('gunmen','start_not_skirmishing'); if(!skirm)attrs.push('cannot_skirmish'); if(u.p==='high')attrs.push('stakes');
  const proj=skirm?(u.quality==='elite'?'a':'b'):v.proj,range=a.range+(skirm?40:0),total=a.base+v.cost;
  return [`type             ${u.type}`,`dictionary       ${u.type} ; ${u.label} (${E[u.p].name}; ${a.name})`,'category         infantry','class            missile','voice_type       Light','accent           turkish','banner faction   main_infantry','banner holy      crusade',`soldier          ${u.type}, ${skirm?30:40}, 0, 1.2`,...officers,`attributes       ${attrs.join(', ')}`,`formation        ${skirm?'1.4, 1.8, 2.8, 3.6, 3, square':E[u.p].form}`,'stat_health      1, 0',`stat_pri         ${a.damage}, 0, ${a.family}_bullet_${proj}, ${range}, ${a.ammo}, missile, missile_gunpowder, piercing, none, ${a.smoke}, 0, -999`,'stat_pri_attr    ap',`stat_sec         ${v.melee}, ${v.charge}, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1.2`,'stat_sec_attr    ap, short_pike',`stat_pri_armour  3, ${v.def}, 0, leather`,'stat_sec_armour  0, 0, flesh','stat_heat        0','stat_ground      0, 0, 0, 0',`stat_mental      ${v.morale}, ${v.disc}, ${v.training}`,'stat_charge_dist 40','stat_fire_delay  0','stat_food        60, 300',`stat_cost        ${cost(total,u.limit)}`,'ownership        turks, slave',`era ${E[u.p].n}            turks`].join('\n');
}
function cavRecord(u){
  const v=q[u.quality],carbine=u.kind==='carbine',pistol=u.kind==='pistol'||u.kind==='general',lance=u.kind==='lance',general=u.kind==='general',attrs=['free_upkeep_unit','sea_faring','hide_forest','can_withdraw'];
  if(carbine||pistol){attrs.push('guncavalry','gunmen','start_not_skirmishing','cannot_skirmish');if(carbine&&u.w.muzzle)attrs.push('gunpowder_unit');if(carbine&&u.p==='high'&&!general)attrs.push('stakes');} if(general)attrs.push('general_unit','command');
  const secCharge=v.charge,pri=lance?`${v.melee}, ${secCharge+3}, no, 0, 0, melee, melee_blade, piercing, spear, 25, 1`:pistol?'20, 4, magazine_rifle_bullet_c, 60, 15, missile, missile_gunpowder, piercing, none, musket_shot_set, 25, 1':`${u.w.damage}, 2, ${u.w.family}_bullet_c, ${u.w.range}, ${u.w.ammo}, missile, missile_gunpowder, piercing, none, ${u.w.smoke}, 25, 1`;
  const total=general?200:lance?1000+200+q[u.quality].cost:pistol?1000+200+q[u.quality].cost:u.w.base+q[u.quality].cost;
  const equip=lance?'Lance and sabre':pistol?'Smith & Wesson No. 3 revolver and sabre':`${u.w.name} and sabre`;
  return [`type             ${u.type}`,`dictionary       ${u.type} ; ${u.label}${u.eras.length===1?` (${E[u.p].name}; ${equip})`:` (${equip})`}`,'category         cavalry',`class            ${carbine?'missile':'light'}`,'voice_type       Heavy','accent           turkish','banner faction   main_cavalry','banner holy      crusade_cavalry',`soldier          ${u.type}, ${general?4:24}, 0, 1`,'officer          fez_off_1g',`mount            ${lance?'lancer':'dragoon'}`,'mount_effect     elephant -4, camel -4',`attributes       ${attrs.join(', ')}`,`formation        2, 2, 4, 4, ${general?2:3}, square`,'stat_health      1, 0',`stat_pri         ${pri}`,`stat_pri_attr    ${lance?'ap, spear':'ap'}`,`stat_sec         ${v.melee}, ${secCharge}, no, 0, 0, melee, melee_blade, piercing, sword, 25, 1`,'stat_sec_attr    ap',`stat_pri_armour  4, ${u.quality==='elite'?5:4}, 0, leather`,'stat_sec_armour  0, 0, flesh','stat_heat        0','stat_ground      0, 0, 0, 0',`stat_mental      ${v.morale}, ${v.disc}, ${v.training}`,'stat_charge_dist 45','stat_fire_delay  0','stat_food        60, 300',`stat_cost        ${cost(total)}`,'ownership        turks, slave',...u.eras.map(e=>`era ${e}            turks`)].join('\n');
}

const legacyCore=['arab_sailors','otto_jan_inf','ertu_cav','arab_brigade','turk_lt2','otto_inf_tu','otto_cav_tu','turk_lt'];
const auxiliary=['rus_georgian_cav_turks','fra_blacks_turks','georgian_inf','moroccan_camel_gunner','moroccan_gunner','mahdist_inf','fra_blacks_az','merc_bulgarian_inf','mahdist_camel_cav','mahdist_cav','merc_arab_sailors','merc_eng_for_cav','merc_georgian_inf','merc_serb_inf','bashi_inf'];
function stripTurks(b){b=b.replace(/^ownership\s+(.+)$/m,(m,x)=>{const a=x.split(',').map(y=>y.trim()).filter(y=>y&&y!=='turks');return a.length?`ownership        ${a.join(', ')}`:'';});b=b.replace(/^era ([012])\s+(.+)$/gm,(m,e,x)=>{const a=x.split(',').map(y=>y.trim()).filter(y=>y&&y!=='turks');return a.length?`era ${e}            ${a.join(', ')}`:'';});return b.replace(/\n{3,}/g,'\n\n');}
let edu=fs.readFileSync(eduC,'utf8').replace(/\r\n/g,'\n');
const begin='; BEGIN STANDARDIZED OTTOMAN EMPIRE',end='; END STANDARDIZED OTTOMAN EMPIRE';
if(edu.includes(begin)){const a=edu.indexOf(begin),z=edu.indexOf(end,a);if(z<0)throw Error('Unclosed Ottoman block');edu=edu.slice(0,a)+edu.slice(z+end.length).replace(/^\s*/, '');}
const starts=[...edu.matchAll(/^type\s+(\S+)/gm)],parts=[edu.slice(0,starts[0].index)];
for(let i=0;i<starts.length;i++){const t=starts[i][1],z=i+1<starts.length?starts[i+1].index:edu.length;let b=edu.slice(starts[i].index,z);if([...legacyCore,...auxiliary].includes(t))b=stripTurks(b);parts.push(b);}edu=parts.join('');
const roster=[...infantry.map(infRecord),...cavalry.map(cavRecord)],insertion=`${begin}\n\n${roster.join('\n\n')}\n\n${end}\n\n`;
const at=edu.indexOf('type             rus_georgian_cav_turks');if(at<0)throw Error('Ottoman insertion point missing');edu=edu.slice(0,at)+insertion+edu.slice(at);
function replaceType(text,type,replacement){const s=[...text.matchAll(/^type\s+(\S+)/gm)],i=s.findIndex(x=>x[1]===type);if(i<0)throw Error(`Missing legacy Ottoman type ${type}`);return text.slice(0,s[i].index)+replacement+'\n\n'+text.slice(i+1<s.length?s[i+1].index:text.length);}
const byType=Object.fromEntries([...infantry.map(u=>[u.type,infRecord(u)]),...cavalry.map(u=>[u.type,cavRecord(u)])]);
const aliases={arab_sailors:'ott_nizamiye_early',otto_jan_inf:'ott_nizamiye_mid',otto_inf_tu:'ott_nizamiye_high',arab_brigade:'ott_mustahfiz_early',turk_lt2:'ott_mustahfiz_mid',otto_cav_tu:'ott_suvari_mid',ertu_cav:'ott_suvari_high',turk_lt:'ott_ertugrul_suvari'};
for(const [old,modern] of Object.entries(aliases)){const a=byType[modern].replace(/^type\s+.*$/m,`type             ${old}`).replace(/^dictionary\s+\S+.*$/m,`dictionary       ${old}`).replace(/^soldier\s+\S+,/m,`soldier          ${modern},`).replace(/^officer\s+ott_standard_bearer\s*\n?/m,'').replace(/^ownership\s+.*$/m,'ownership        slave').replace(/^era [012]\s+.*\n?/gm,'').trimEnd();edu=replaceType(edu,old,a);}
const out=edu.replace(/\n/g,'\r\n');fs.writeFileSync(eduC,out);fs.writeFileSync(eduR,out);

function entries(text){const a=text.replace(/\r\n/g,'\n').split('\n'),r=[];let start=1;for(let i=1;i<a.length;i++)if(/^16 -0\.090000004 /.test(a[i])){r.push({start,end:i,lines:a.slice(start,i+1),name:(a[start].match(/^\d+ (\S+)/)||[])[1]});start=i+1;}return {a,r};}
function modelEntry(text,name){const e=entries(text).r.find(x=>x.name===name);if(!e)throw Error(`Missing Ottoman model donor ${name}`);return e.lines.join('\n');}
function counted(value){return `${value.length} ${value}`;}
function applyOttomanPistolMesh(e,kind){
  const hassa=kind==='pistol';
  const mesh=hassa?'unit_models/_Units/otto/ott_hassa_suvarisi_lod0.mesh':'unit_models/_Units/ott/ott_general_staff_lod0.mesh';
  const oldMesh=hassa?'unit_models/_Units/otto/otto_reg_lod0.mesh':'unit_models/_Units/ott/ott_cav_1g_lod0.mesh';
  const diffuse=hassa?'unit_models/_Units/otto/textures/ott_hassa_pistol_gear.texture':'unit_models/_Units/ott/textures/ott_general_pistol_gear.texture';
  const normal=hassa?'unit_models/_Units/otto/textures/ott_hassa_pistol_gear_norm.texture':'unit_models/_Units/ott/textures/ott_general_pistol_gear_norm.texture';
  const oldDiffuse=hassa?'unit_models/_Units/portugal/textures/port_inf_3.texture':'unit_models/_Units/attachments/textures/per_rugbxx.texture';
  const oldNormal=hassa?'unit_models/_Units/portugal/textures/yingguowuqi_n.texture':'unit_models/_Units/attachments/textures/blank_norm.texture';
  if(!e.includes(counted(oldMesh))||!e.includes(counted(oldDiffuse))||!e.includes(counted(oldNormal)))throw Error(`Unexpected ${kind} Ottoman donor structure`);
  e=e.split(counted(oldMesh)).join(counted(mesh));
  e=e.split(counted(oldDiffuse)).join(counted(diffuse));
  e=e.split(counted(oldNormal)).join(counted(normal));
  e=e.replace('16 MTW2_CR_Arquebus 13 MTW2_CR_Sword','14 MTW2_HR_Pistol \n13 MTW2_HR_Sword');
  e=e.replace('24 MTW2_HR_Arquebus_Primary','22 MTW2_HR_Pistol_Primary');
  return e;
}
function cloneModel(text,donor,name,mode,kind){let e=modelEntry(text,donor).replace(new RegExp(`^${donor.length} ${donor}\\s*$`,'m'),`${name.length} ${name} `);if(mode==='line')e=e.replace(/(?:20 MTW2_Fast_Arquebus_3|15 MTW2_Musket_SSK|17 MTW2_Flamethrower) 9 MTW2_Pike /,'14 MTW2_Musket_SS 9 MTW2_Pike ');if(mode==='skirmisher')e=e.replace(/(?:20 MTW2_Fast_Arquebus_3|14 MTW2_Musket_SS|17 MTW2_Flamethrower) 9 MTW2_Pike /,'15 MTW2_Musket_SSK 9 MTW2_Pike ');if(mode==='fast')e=e.replace(/(?:14 MTW2_Musket_SS|15 MTW2_Musket_SSK|17 MTW2_Flamethrower) 9 MTW2_Pike /,'20 MTW2_Fast_Arquebus_3 9 MTW2_Pike ');if(kind==='pistol'||kind==='general')e=applyOttomanPistolMesh(e,kind);if(kind)e=e.replace(/^\d+ unit_sprites\/[^\s]+_sprite\.spr\s*$/gm,'35 unit_sprites/tmp_cavalry_sprite.spr ');return e;}
function ottomanBearerModel(text){
  const donor=modelEntry(text,'francejunqshou'),tailAt=donor.indexOf('\n4 \n4 None \n9 MTW2_Pike ');if(tailAt<0)throw Error('Unexpected verified bearer donor structure');
  const name='ott_standard_bearer',mesh='unit_models/_Units/off/ott_standard_bearer_lod0.mesh',body='unit_models/_Units/ott/textures/ott_inf_1g.texture',bodyN='unit_models/_Units/attachments/textures/blank_norm.texture',flag='unit_models/_Units/bnw/textures/ott_standard_flag.texture',flagN='unit_models/_Units/bnw/textures/ott_standard_flag_n.texture',sprite='unit_sprites/turks_Janissary_Musketeers_sprite.spr';
  return [`${name.length} ${name} `,'1 1 ',`${counted(mesh)} 20000 `,'1 ','5 turks ',`${counted(body)} `,`${counted(bodyN)} `,`${counted(sprite)} `,'1 ','5 turks ',`${counted(flag)} `,`${counted(flagN)} 0 `].join('\n')+'\n'+donor.slice(tailAt+1);
}
let model=fs.readFileSync(modelP,'utf8').replace(/\r\n/g,'\n'),added=0;
{const name='ott_standard_bearer',fresh=ottomanBearerModel(model);if(entries(model).r.some(x=>x.name===name))model=model.replace(modelEntry(model,name),fresh);else{model=model.trimEnd()+'\n'+fresh+'\n';added++;}}
for(const u of infantry){const mode=u.w.muzzle?'fast':u.role==='skirmisher'?'skirmisher':u.p==='high'?'fast':'line';const fresh=cloneModel(model,u.donor,u.type,mode);if(entries(model).r.some(x=>x.name===u.type))model=model.replace(modelEntry(model,u.type),fresh);else{model=model.trimEnd()+'\n'+fresh+'\n';added++;}}
for(const u of cavalry){const fresh=cloneModel(model,u.donor,u.type,null,u.kind);if(entries(model).r.some(x=>x.name===u.type))model=model.replace(modelEntry(model,u.type),fresh);else{model=model.trimEnd()+'\n'+fresh+'\n';added++;}}
if(added){const h=model.match(/^(22 serialization::archive 3 0 0 0 0 )(\d+)( 0 0 )/);if(!h)throw Error('Bad modeldb header');model=model.replace(h[0],`${h[1]}${+h[2]+added}${h[3]}`);}fs.writeFileSync(modelP,model.replace(/\n/g,'\r\n'));

let lb=fs.readFileSync(locP),loc=lb.slice(lb[0]===255&&lb[1]===254?2:0).toString('utf16le').replace(/\r\n/g,'\n');
for(const u of [...infantry,...cavalry])for(const k of [u.type,`${u.type}_descr`,`${u.type}_descr_short`])loc=loc.replace(new RegExp(`^\\{${k}\\}.*(?:\\n|$)`,'gm'),'');
const entriesLoc=[...infantry.map(u=>`{${u.type}}${u.label} (${E[u.p].name})\n{${u.type}_descr}${u.label} serve in the Ottoman army in the ${E[u.p].name.toLowerCase()} period.\n{${u.type}_descr_short}${u.label} (${u.w.name})`),...cavalry.map(u=>`{${u.type}}${u.label}${u.eras.length===1?` (${E[u.p].name})`:''}\n{${u.type}_descr}${u.label} serve in the mounted arm of the Ottoman army.\n{${u.type}_descr_short}${u.label} (${u.kind==='lance'?'lance and sabre':u.kind==='general'?'mounted command staff with Smith & Wesson No. 3 revolver and sabre':u.kind==='pistol'?'Smith & Wesson No. 3 revolver and sabre':u.w.name+' and sabre'})`)];
loc=loc.trimEnd()+'\n\n'+entriesLoc.join('\n\n')+'\n';fs.writeFileSync(locP,Buffer.concat([Buffer.from([255,254]),Buffer.from(loc.replace(/\n/g,'\r\n'),'utf16le')]));

fs.mkdirSync(archiveDir,{recursive:true});fs.mkdirSync(unitDir,{recursive:true});
for(const source of new Set([...infantry.map(u=>u.card),...cavalry.map(u=>u.card)].filter(x=>!x.startsWith('__generated_')))){const src=path.join(unitDir,`#${source}.tga`),arc=path.join(archiveDir,`#${source}.tga`);if(!fs.existsSync(src))throw Error(`Missing Ottoman card donor ${source}`);if(!fs.existsSync(arc))fs.copyFileSync(src,arc);}
for(const u of [...infantry,...cavalry]){if(u.card.startsWith('__generated_'))continue;const src=path.join(unitDir,`#${u.card}.tga`),dst=path.join(unitDir,`#${u.type}.tga`);fs.copyFileSync(src,dst);}
if(!fs.readFileSync(eduC).equals(fs.readFileSync(eduR)))throw Error('Ottoman EDU mirrors differ');console.log(`Standardized ${infantry.length+cavalry.length} Ottoman records; added ${added} model entries.`);
