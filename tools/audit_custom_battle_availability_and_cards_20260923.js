const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const eduPath=path.join(root,'data/tow_steamsteel/export_descr_unit.txt');
const uiRoot=path.join(root,'data/ui/units');
const outDir=path.join(root,'tools/custom_battle_availability_audit_20260923');
fs.mkdirSync(outDir,{recursive:true});
const text=fs.readFileSync(eduPath,'utf8').replace(/\r/g,'');
const factionNames={portugala:'Union',milan:'Confederates',scotland:'Mexico',denmark:'Peru',poland:'Brazil',aztecs:'Argentina',england:'Britain',france:'France',hre:'Prussia',spain:'Spain',portugal:'Netherlands',sicily:'Denmark',normans:'Sweden-Norway',mongols:'Greece',venice:'Italy',russia:'Russia',hungary:'Austria-Hungary',moors:'Morocco',teu:'Boers',lith:'Zulu',turks:'Ottoman',golden:'Oman',egypt:'Qajar',timurids:'Afghanistan',cuman:'Turkestan',bulga:'Indian Princely States',cru:'Siam',byzantium:'Qing',papal_states:'Ethiopia',saxons:'Japan',slave:'Rebels'};
const national=new Set(Object.keys(factionNames).filter(x=>x!=='slave'));
const list=s=>(s||'').split(/[\s,]+/).map(x=>x.trim()).filter(Boolean);
const units=[];
for(const b of text.split(/(?=^type\s+)/m)){
 const type=b.match(/^type\s+(.+)$/m)?.[1]?.trim(); if(!type)continue;
 const dictionary=b.match(/^dictionary\s+([^;\s]+)/m)?.[1];
 const category=b.match(/^category\s+(\S+)/m)?.[1]||'';
 const cls=b.match(/^class\s+(\S+)/m)?.[1]||'';
 const engine=b.match(/^engine\s+(\S+)/m)?.[1]||'';
 const cost=list(b.match(/^stat_cost\s+(.+)$/m)?.[1]);
 const customLimit=Number(cost[6]||0);
 const attributes=list(b.match(/^attributes\s+(.+)$/m)?.[1]);
 const ownership=list(b.match(/^ownership\s+(.+)$/m)?.[1]);
 const eras={0:[],1:[],2:[]};for(const m of b.matchAll(/^era\s+([012])\s+(.+)$/gm))eras[m[1]].push(...list(m[2]));
 units.push({type,dictionary,category,class:cls,engine,attributes,ownership,eras,customLimit});
}

const allCardDirs=fs.readdirSync(uiRoot,{withFileTypes:true}).filter(x=>x.isDirectory()).map(x=>x.name);
function findExactCard(key){const n='#'+key+'.tga';for(const d of allCardDirs){const p=path.join(uiRoot,d,n);if(fs.existsSync(p))return p;}return null;}
const required=[];
for(const u of units){if(!u.dictionary)continue;for(const era of ['0','1','2'])for(const f of u.eras[era])if(f!=='all')required.push({unit:u.type,key:u.dictionary,folder:f,era,reason:'era'});if(u.attributes.includes('mercenary_unit'))required.push({unit:u.type,key:u.dictionary,folder:'mercs',era:'all',reason:'mercenary_unit'});}
const uniq=new Map();for(const x of required)uniq.set([x.key,x.folder].join('|'),x);
const repaired=[],unresolved=[];
for(const x of uniq.values()){
 const target=path.join(uiRoot,x.folder,'#'+x.key+'.tga');if(fs.existsSync(target))continue;
 const donor=findExactCard(x.key);if(!donor){unresolved.push(x);continue;}
 fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(donor,target);repaired.push({...x,donor:path.relative(root,donor),target:path.relative(root,target)});
}

const counts={};for(const f of national)counts[f]={};
const memberships=[];
for(const era of ['0','1','2'])for(const u of units){const fsx=[...new Set(u.eras[era].filter(f=>national.has(f)))];for(const f of fsx)memberships.push({era:+era,faction:f,unit:u.type,dictionary:u.dictionary,category:u.category,class:u.class,engine:u.engine,artillery:u.category==='siege',mercenary:u.attributes.includes('mercenary_unit'),customLimit:u.customLimit});}
for(const f of national)for(const era of [0,1,2]){const xs=memberships.filter(x=>x.faction===f&&x.era===era);counts[f][era]={total:xs.length,totalFormationCap:xs.reduce((n,x)=>n+x.customLimit,0),artillery:xs.filter(x=>x.artillery).length,artilleryFormationCap:xs.filter(x=>x.artillery).reduce((n,x)=>n+x.customLimit,0),mercenary:xs.filter(x=>x.mercenary).length,landNonArtillery:xs.filter(x=>!x.artillery&&x.category!=='ship').length,naval:xs.filter(x=>x.category==='ship').length};}
const crossFaction=[];for(const era of [0,1,2])for(const u of units){const fsx=[...new Set(u.eras[era].filter(f=>national.has(f)))];if(fsx.length>1)crossFaction.push({era,unit:u.type,dictionary:u.dictionary,category:u.category,factions:fsx,count:fsx.length});}
const ownershipWithoutEra=[];for(const u of units)for(const f of u.ownership.filter(x=>national.has(x)))if(![0,1,2].some(e=>u.eras[e].includes(f)))ownershipWithoutEra.push({unit:u.type,dictionary:u.dictionary,category:u.category,faction:f});
const eraWithoutOwnership=[];for(const u of units)for(const era of [0,1,2])for(const f of u.eras[era].filter(x=>national.has(x)))if(!u.ownership.includes(f))eraWithoutOwnership.push({unit:u.type,dictionary:u.dictionary,category:u.category,era,faction:f});

const result={generated:new Date().toISOString(),authoritative:path.relative(root,eduPath),counts,totals:{records:units.length,memberships:memberships.length,repairedCards:repaired.length,unresolvedCards:unresolved.length,crossFactionRows:crossFaction.length,ownershipWithoutAnyEra:ownershipWithoutEra.length,eraWithoutOwnership:eraWithoutOwnership.length},repairedCards:repaired,unresolvedCards:unresolved,crossFaction,ownershipWithoutEra,eraWithoutOwnership,memberships};
fs.writeFileSync(path.join(outDir,'audit.json'),JSON.stringify(result,null,2)+'\n');
const q=x=>'"'+String(x??'').replace(/"/g,'""')+'"';
const csv=[['era','faction','faction_name','unit','dictionary','category','class','engine','artillery','mercenary_unit','custom_battle_limit'].map(q).join(',')];for(const x of memberships)csv.push([x.era,x.faction,factionNames[x.faction],x.unit,x.dictionary,x.category,x.class,x.engine,x.artillery,x.mercenary,x.customLimit].map(q).join(','));fs.writeFileSync(path.join(outDir,'membership_matrix.csv'),csv.join('\n')+'\n');
const md=['# Custom-battle availability and tactical-card audit','','EDU era lists are authoritative for custom-battle period membership. Each period cell is `unit types / summed formation cap`; the parenthesis is `artillery types / artillery cap`. Ships remain included in the headline total and are identifiable in the matrix.','','| Faction | Code | Early | Mid | Late |','|---|---|---:|---:|---:|'];
for(const [f,name] of Object.entries(factionNames)){if(f==='slave')continue;const c=counts[f],cell=e=>`${c[e].total} / ${c[e].totalFormationCap} (${c[e].artillery} / ${c[e].artilleryFormationCap})`;md.push(`| ${name} | ${f} | ${cell(0)} | ${cell(1)} | ${cell(2)} |`);}
md.push('',`Exact-key tactical cards installed: **${repaired.length}**.`,`Required cards with no exact donor: **${unresolved.length}**.`,`Unit/period rows shared by multiple national factions: **${crossFaction.length}**.`,`Ownership entries with no custom-battle era membership: **${ownershipWithoutEra.length}**.`,`Era memberships absent from ownership: **${eraWithoutOwnership.length}**.`,'','## Repaired card copies','');for(const x of repaired)md.push(`- \`${x.target}\` from \`${x.donor}\` (${x.reason}).`);md.push('','## Unresolved exact cards','');for(const x of unresolved)md.push(`- \`${x.folder}/#${x.key}.tga\` for \`${x.unit}\` (${x.reason}).`);fs.writeFileSync(path.join(outDir,'audit.md'),md.join('\n')+'\n');
console.log(JSON.stringify(result.totals));
