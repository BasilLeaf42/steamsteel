const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),src=path.join(root,'data/tow_steamsteel/export_descr_unit.txt');
const text=fs.readFileSync(src,'utf8').replace(/\r/g,'');
const factions={portugala:'Union',milan:'Confederates',scotland:'Mexico',denmark:'Peru',poland:'Brazil',aztecs:'Argentina',england:'Britain',france:'France',hre:'Prussia',spain:'Spain',portugal:'Netherlands',sicily:'Denmark',normans:'Sweden-Norway',mongols:'Greece',venice:'Italy',russia:'Russia',hungary:'Austria-Hungary',moors:'Morocco',teu:'Boers',lith:'Zulu',turks:'Ottoman',golden:'Oman',egypt:'Qajar',timurids:'Afghanistan',cuman:'Turkestan',bulga:'Indian Princely States',cru:'Siam',byzantium:'Qing',papal_states:'Ethiopia',saxons:'Japan'};
const split=s=>(s||'').split(/[\s,]+/).filter(Boolean);
const units=[];
for(const b of text.split(/(?=^type\s+)/m)){
 const type=b.match(/^type\s+(.+)$/m)?.[1]?.trim();if(!type)continue;
 const dictionary=b.match(/^dictionary\s+([^;\s]+)/m)?.[1]||'';
 const category=b.match(/^category\s+(\S+)/m)?.[1]||'';
 const cls=b.match(/^class\s+(\S+)/m)?.[1]||'';
 const soldier=b.match(/^soldier\s+[^,]+,\s*([\d.]+)/m);const strength=soldier?+soldier[1]:0;
 const attributes=split(b.match(/^attributes\s+(.+)$/m)?.[1]);
 const pri=b.match(/^stat_pri\s+(.+)$/m)?.[1]||'';
 const priFields=pri.split(',').map(x=>x.trim());const missileRange=Number(priFields[3]||0);
 const costFields=(b.match(/^stat_cost\s+(.+)$/m)?.[1]||'').split(',').map(x=>x.trim());
 const customLimit=Number(costFields[6]||0);
 const eras={0:[],1:[],2:[]};for(const m of b.matchAll(/^era\s+([012])\s+(.+)$/gm))eras[m[1]].push(...split(m[2]));
 units.push({type,dictionary,category,class:cls,strength,attributes,pri,missileRange,customLimit,eras});
}
function role(u){
 if(u.category==='siege')return u.strength<=10?'light_artillery':'heavy_artillery';
 if(u.category==='cavalry')return /missile_gunpowder/.test(u.pri)&&u.missileRange>60?'carbineers':'cavalry';
 if(u.category==='infantry'&&/missile_gunpowder/.test(u.pri))return'gunpowder_infantry';
 if(u.category==='infantry'&&!/\bmissile\b/.test(u.pri))return'melee_auxiliaries';
 return'other';
}
const rows=[],detail=[];
for(const [f,name] of Object.entries(factions))for(const era of [0,1,2]){
 const core=units.filter(u=>u.eras[era].includes(f)&&!u.attributes.includes('mercenary_unit')&&u.category!=='ship');
 const availability={gunpowder_infantry:0,cavalry:0,carbineers:0,light_artillery:0,heavy_artillery:0,melee_auxiliaries:0,other:0};
 const recordTypes={gunpowder_infantry:0,cavalry:0,carbineers:0,light_artillery:0,heavy_artillery:0,melee_auxiliaries:0,other:0};
 for(const u of core){const r=role(u);availability[r]+=u.customLimit;recordTypes[r]++;detail.push({faction:f,factionName:name,era,role:r,...u});}
 rows.push({faction:f,factionName:name,era,totalAvailability:core.reduce((n,u)=>n+u.customLimit,0),totalRecordTypes:core.length,availability,recordTypes});
}
const out=path.join(root,'tools/custom_battle_availability_audit_20260923');fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'core_role_counts.json'),JSON.stringify({definitions:{core:'Era-listed national records excluding mercenary_unit and ships.',availability:'Sum of the seventh stat_cost field (custom-battle quantity limit), not the number of EDU records.',gunpowder_infantry:'All firearm infantry, including line infantry, skirmishers, sharpshooters and wall-gun teams.',cavalry:'Mounted melee, lance, bow, or pistol units; pistol range is 60.',carbineers:'Mounted gunpowder units with primary range greater than the 60-range pistol baseline.',light_artillery:'Siege-category unit with nominal crew strength <=10.',heavy_artillery:'Siege-category unit with nominal crew strength >10.',melee_auxiliaries:'Infantry whose primary attack is not missile.'},rows,detail},null,2)+'\n');
const md=['# Core custom-battle availability by battlefield role','','Each cell sums the custom-battle quantity limit from `stat_cost`. It does **not** count EDU record types. Line infantry includes firearm skirmishers, sharpshooters and wall-gun teams. Format: `line infantry / cavalry / carbineers / light artillery / heavy artillery / melee auxiliaries`.', '', '| Faction | Early | Mid | Late |','|---|---:|---:|---:|'];
for(const [f,name] of Object.entries(factions)){const cells=[0,1,2].map(e=>{const x=rows.find(r=>r.faction===f&&r.era===e),a=x.availability;return [a.gunpowder_infantry,a.cavalry,a.carbineers,a.light_artillery,a.heavy_artillery,a.melee_auxiliaries].join(' / ')});md.push(`| ${name} | ${cells[0]} | ${cells[1]} | ${cells[2]} |`)}
const others=detail.filter(x=>x.role==='other');md.push('','## Unclassified core land records','',`These **${others.length}** record-period memberships are deliberately outside the requested six buckets (principally bows or other non-gunpowder missile infantry):`,'');for(const x of others)md.push(`- ${x.factionName}, ${['Early','Mid','Late'][x.era]}: \`${x.type}\`.`);
fs.writeFileSync(path.join(out,'core_role_counts.md'),md.join('\n')+'\n');
console.log(md.slice(0,md.indexOf('## Unclassified core land records')).join('\n'));
