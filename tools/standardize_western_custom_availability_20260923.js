const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const files=['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt'];
const backup=path.join(root,'tools/backup_before_western_custom_availability_20260923');fs.mkdirSync(backup,{recursive:true});
for(const f of files)fs.copyFileSync(path.join(root,f),path.join(backup,f.replaceAll('/','__')));

const targets={
 portugala:[9,6,6],milan:[9,6,6],scotland:[6,6,6],denmark:[5,5,5],poland:[6,6,6],aztecs:[5,5,5],
 england:[7,7,7],france:[8,8,8],hre:[8,8,8],spain:[6,6,6],portugal:[6,6,6],sicily:[6,6,6],
 normans:[6,6,6],mongols:[5,5,5],venice:[8,8,8],russia:[9,9,9],hungary:[8,8,8],teu:[5,5,5]
};
const removals={
 england:{1:['volunteers_te','austro_sailor_england'],2:['volunteers_te','austro_sailor_england','uk_marines_high']},
 france:{1:['fra_guard']},
 hre:{1:['pru_hannover_mid'],2:['pru_wuerttemberg_high','pru_bavarian_fusiliere_high','pru_bavarian_landwehr_high','pru_hannover_high']},
 venice:{2:['ita_ascari_high','ita_libici_high']},
 russia:{1:['bulgarian_inf_russia']}
};
const preferred={
 portugala:{0:{uni_state_volunteers_early:3},1:{uni_regulars_mid:2,uni_national_guard_mid:2},2:{uni_regulars_high:2,uni_national_guard_high:3}},
 milan:{0:{csa_state_volunteers_early:3,csa_regulars_early:2,csa_louisiana_tigers:2},1:{csa_state_guard_mid:4,csa_regulars_mid:2},2:{csa_state_guard_high:4,csa_regulars_high:2}},
 scotland:{0:{mex_natl_guard:3,mex_federal_early:2},1:{mex_state_guard_mid:2,mex_federal_mid:3},2:{mex_army:3,mex_state_guard_mid:2}},
 denmark:{0:{per_line_early:2},1:{},2:{per_line_high:2}},
 poland:{0:{bra_line_early:2},1:{bra_line_mid:2},2:{bra_line_high:3}},
 aztecs:{0:{arg_line_early:2,arg_national_guard_early:2},1:{arg_line_mid:2,arg_national_guard_mid:2},2:{arg_line_high:2,arg_national_guard_high:2}},
 hre:{0:{pru_fusiliere_early:3,pru_jaeger_early:2}},
 spain:{0:{spa_inf_early:2},1:{spa_inf_mid:2}},
 sicily:{0:{dan_fod_early:3},1:{dan_fod_mid:3},2:{dan_fod_high:3}},
 mongols:{0:{gre_line_early:2},1:{gre_line_mid:2}},
 venice:{0:{ita_line_early:2},1:{ita_line_mid:2}},
 hungary:{0:{aus_line_early:3,aus_kaiserjaeger_early:2,aus_grenz_early:2},1:{aus_line_mid:3},2:{aus_line_high:3}},
 teu:{0:{boer_kommando_early:5},1:{boer_kommando_mid:5},2:{boer_kommando_high:4}}
};
const west=new Set(Object.keys(targets));
const split=s=>(s||'').split(/[\s,]+/).filter(Boolean);

function parse(text){const out=[];for(const b of text.replace(/\r/g,'').split(/(?=^type\s+)/m)){const type=b.match(/^type\s+(.+)$/m)?.[1]?.trim();if(!type)continue;const category=b.match(/^category\s+(\S+)/m)?.[1]||'',attrs=split(b.match(/^attributes\s+(.+)$/m)?.[1]),pri=b.match(/^stat_pri\s+(.+)$/m)?.[1]||'',range=+(pri.split(',')[3]||0),strength=+(b.match(/^soldier\s+[^,]+,\s*([\d.]+)/m)?.[1]||0),customLimit=+((b.match(/^stat_cost\s+(.+)$/m)?.[1]||'').split(',')[6]||0),eras={0:[],1:[],2:[]};for(const m of b.matchAll(/^era\s+([012])\s+(.+)$/gm))eras[m[1]].push(...split(m[2]));out.push({type,category,attrs,pri,range,strength,customLimit,eras});}return out;}
function role(u){if(u.category==='siege')return u.strength<=10?'light_artillery':'heavy_artillery';if(u.category==='cavalry')return /missile_gunpowder/.test(u.pri)&&u.range>60?'carbineers':'cavalry';if(u.category==='infantry'&&/missile_gunpowder/.test(u.pri))return'line';return'other';}

let text=fs.readFileSync(path.join(root,files[0]),'utf8').replace(/\r/g,'');
let units=parse(text),byType=new Map(units.map(x=>[x.type,x]));
for(const [f,periods] of Object.entries(removals))for(const [era,names] of Object.entries(periods))for(const type of names){const u=byType.get(type);if(!u||!u.eras[era].includes(f))throw Error(`cannot remove ${f} era ${era} from ${type}`);const re=new RegExp(`(^type\\s+${type.replace(/[.*+?^${}()|[\\]\\]/g,'\\$&')}\\s*$[\\s\\S]*?^era\\s+${era}\\s+)([^\\r\\n]+)`,'m');text=text.replace(re,(all,head,list)=>{const left=split(list).filter(x=>x!==f);return left.length?head+left.join(', '):head.replace(/era\s+[012]\s+$/,'');});}

units=parse(text);byType=new Map(units.map(x=>[x.type,x]));
const desired=new Map();
for(const u of units){const r=role(u);if((r==='cavalry'||r==='carbineers')&&[0,1,2].some(e=>u.eras[e].some(f=>west.has(f))))desired.set(u.type,1);if((r==='light_artillery'||r==='heavy_artillery')&&[0,1,2].some(e=>u.eras[e].some(f=>west.has(f))))desired.set(u.type,2);if(r==='line'&&!u.attrs.includes('mercenary_unit')&&[0,1,2].some(e=>u.eras[e].some(f=>west.has(f))))desired.set(u.type,1);}
for(const [f,eras] of Object.entries(preferred))for(const [era,map] of Object.entries(eras))for(const [type,n] of Object.entries(map)){const u=byType.get(type);if(!u||!u.eras[era].includes(f)||role(u)!=='line')throw Error(`bad preferred ${f}/${era}/${type}`);desired.set(type,n);}

for(const [type,n] of desired){const re=new RegExp(`(^type\\s+${type.replace(/[.*+?^${}()|[\\]\\]/g,'\\$&')}\\s*$[\\s\\S]*?^stat_cost\\s+)([^\\r\\n]+)`,'m');let hit=false;text=text.replace(re,(all,head,row)=>{hit=true;const a=row.split(',').map(x=>x.trim());if(a.length!==8)throw Error(`stat_cost fields ${type}`);a[6]=String(n);return head+a.join(', ');});if(!hit)throw Error(`missing stat_cost ${type}`);}

function validate(s){const us=parse(s),issues=[];for(const [f,t] of Object.entries(targets))for(const era of [0,1,2]){const xs=us.filter(u=>u.eras[era].includes(f)&&!u.attrs.includes('mercenary_unit')&&role(u)==='line');const total=xs.reduce((n,u)=>n+u.customLimit,0);if(total!==t[era])issues.push(`${f} era${era}: ${total} != ${t[era]}`);}return issues;}
const issues=validate(text);if(issues.length)throw Error(issues.join('\n'));
const out=text.replace(/\n/g,'\r\n');for(const f of files)fs.writeFileSync(path.join(root,f),out);
console.log(`Standardized western custom availability: ${desired.size} unit limits; ${Object.values(removals).flatMap(x=>Object.values(x).flat()).length} era memberships removed.`);
