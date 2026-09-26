const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const files=['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt'];
const backup=path.join(root,'tools/backup_before_slave_merc_availability_20260923');
fs.mkdirSync(backup,{recursive:true});
for(const f of files){const dst=path.join(backup,f.replaceAll('/','__'));if(!fs.existsSync(dst))fs.copyFileSync(path.join(root,f),dst);}
const split=s=>(s||'').split(/[\s,]+/).filter(Boolean);

function parse(text){const out=[];for(const b of text.replace(/\r/g,'').split(/(?=^type\s+)/m)){
 const type=b.match(/^type\s+(.+)$/m)?.[1]?.trim();if(!type)continue;
 const dictionary=b.match(/^dictionary\s+([^;\r\n]+)/m)?.[1]?.trim()||'';
 const category=b.match(/^category\s+(\S+)/m)?.[1]||'';
 const attributes=split(b.match(/^attributes\s+(.+)$/m)?.[1]);
 const ownership=split(b.match(/^ownership\s+(.+)$/m)?.[1]);
 const cost=(b.match(/^stat_cost\s+(.+)$/m)?.[1]||'').split(',').map(x=>x.trim());
 const eras=[];for(const m of b.matchAll(/^era\s+([012])\s+(.+)$/gm))eras.push({era:+m[1],factions:split(m[2])});
 out.push({type,dictionary,category,attributes,ownership,limit:+(cost[6]||0),eras});
}return out;}

function subfaction(type){
 const t=type.toLowerCase();
 if(t.startsWith('taiping'))return'Taiping';
 if(t.startsWith('merc_aceh_'))return'Aceh';
 if(t.startsWith('korean ')||t.startsWith('korean_')||t==='turtle ship')return'Korea';
 if(t.startsWith('merc_tib_')||t.startsWith('mercs_tib_')||t.startsWith('tib_'))return'Tibet';
 if(t.startsWith('mahdist_')||t.startsWith('ethiopia sudanese'))return'Mahdist/Sudanese';
 if(t.startsWith('japan ainu ')||t.startsWith('japan heimin ')||['japan ronin','japan shizoku','japan teppotai merc'].includes(t))return'Ainu/Japanese irregulars';
 if(t.startsWith('merc_port_'))return'Portuguese auxiliaries';
 return null;
}

let text=fs.readFileSync(path.join(root,files[0]),'utf8').replace(/\r/g,'');
const before=parse(text),slaveOnly=before.filter(u=>u.ownership.length===1&&u.ownership[0]==='slave');
for(const u of slaveOnly){
 const escaped=u.type.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const re=new RegExp(`(^type\\s+${escaped}\\s*$[\\s\\S]*?^stat_cost\\s+)([^\\r\\n]+)`,'m');let hit=false;
 text=text.replace(re,(all,head,row)=>{hit=true;const a=row.split(',').map(x=>x.trim());if(a.length!==8)throw Error(`stat_cost fields ${u.type}`);a[6]='1';return head+a.join(', ');});
 if(!hit)throw Error(`missing stat_cost ${u.type}`);
}

// Aceh is a deliberately weak Netherlands-hosted subfaction. Keep one of each
// distinct formation instead of stacking militia-style quantity multipliers.
for(const u of before.filter(x=>x.type.startsWith('merc_aceh_'))){
 const escaped=u.type.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const re=new RegExp(`(^type\\s+${escaped}\\s*$[\\s\\S]*?^stat_cost\\s+)([^\\r\\n]+)`,'m');let hit=false;
 text=text.replace(re,(all,head,row)=>{hit=true;const a=row.split(',').map(x=>x.trim());if(a.length!==8)throw Error(`stat_cost fields ${u.type}`);a[6]='1';return head+a.join(', ');});
 if(!hit)throw Error(`missing Aceh stat_cost ${u.type}`);
}

// Mahdist identity is melee mass. Increase both foot-melee formations while
// leaving musketeers and cavalry at their existing quantities.
for(const type of ['mahdist_inf','Ethiopia Sudanese Warriors']){
 const escaped=type.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const re=new RegExp(`(^type\\s+${escaped}\\s*$[\\s\\S]*?^stat_cost\\s+)([^\\r\\n]+)`,'m');let hit=false;
 text=text.replace(re,(all,head,row)=>{hit=true;const a=row.split(',').map(x=>x.trim());if(a.length!==8)throw Error(`stat_cost fields ${type}`);a[6]='3';return head+a.join(', ');});
 if(!hit)throw Error(`missing Mahdist stat_cost ${type}`);
}

// The Mahdist state belongs to the mid/late periods. The lower-tier Sudanese
// tribal warriors remain the sole early-period member of this regional pool.
for(const type of ['mahdist_inf','mahdist_camel_cav','mahdist_cav','Ethiopia Sudanese Musketeers']){
 const escaped=type.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const blockRe=new RegExp(`(^type\\s+${escaped}\\s*$[\\s\\S]*?)(?=^type\\s+|(?![\\s\\S]))`,'m');
 text=text.replace(blockRe,block=>block.replace(/^era\s+0\s+.+\r?\n?/m,''));
}

const after=parse(text),issues=[];
for(const u of after.filter(x=>x.ownership.length===1&&x.ownership[0]==='slave'))if(u.limit!==1)issues.push(`${u.type}: slave-only limit ${u.limit}`);
for(const u of after.filter(x=>x.type.startsWith('merc_aceh_')))if(u.limit!==1)issues.push(`${u.type}: Aceh limit ${u.limit}`);
for(const type of ['mahdist_inf','Ethiopia Sudanese Warriors'])if(after.find(x=>x.type===type)?.limit!==3)issues.push(`${type}: Mahdist melee availability`);
for(const type of ['mahdist_inf','mahdist_camel_cav','mahdist_cav','Ethiopia Sudanese Musketeers'])if(after.find(x=>x.type===type)?.eras.some(x=>x.era===0))issues.push(`${type}: still early`);
if(issues.length)throw Error(issues.join('\n'));
const outText=text.replace(/\n/g,'\r\n');for(const f of files)fs.writeFileSync(path.join(root,f),outText);

const allMercs=after.filter(u=>u.attributes.includes('mercenary_unit')).map(u=>({...u,subfaction:subfaction(u.type)}));
const mercs=allMercs.filter(u=>!u.attributes.includes('no_custom'));
const hiddenMercs=allMercs.filter(u=>u.attributes.includes('no_custom'));
const groups={};for(const u of mercs.filter(x=>x.subfaction))(groups[u.subfaction]??=[]).push(u);
const standard=mercs.filter(x=>!x.subfaction);
const original=parse(fs.readFileSync(path.join(backup,'data__tow_steamsteel__export_descr_unit.txt'),'utf8'));
const originalSlave=original.filter(u=>u.ownership.length===1&&u.ownership[0]==='slave');
const report={definitions:{slaveOnly:'The ownership row contains slave and no national faction.',customAvailableMercenary:'A mercenary_unit record without no_custom.',hiddenMercenary:'A mercenary_unit record carrying no_custom; retained for campaign, rebel, compatibility, or other non-custom use.',subfaction:'A coherent named political, regional, or irregular pool with multiple related custom-visible records.',standardMercenary:'A standalone mercenary, auxiliary, generic naval, or otherwise ungrouped custom-visible record.'},summary:{slaveOnlyRecords:slaveOnly.length,slaveOnlyLimitsChanged:originalSlave.filter(u=>u.limit!==1).length,mercenaryRecords:allMercs.length,customAvailableMercenaryRecords:mercs.length,hiddenMercenaryRecords:hiddenMercs.length,subfactionRecords:mercs.length-standard.length,standardMercenaryRecords:standard.length},subfactions:Object.fromEntries(Object.entries(groups).sort().map(([k,v])=>[k,v.sort((a,b)=>a.type.localeCompare(b.type))])),standardMercenaries:standard.sort((a,b)=>a.type.localeCompare(b.type)),hiddenMercenaries:hiddenMercs.sort((a,b)=>a.type.localeCompare(b.type))};
const reportDir=path.join(root,'tools/slave_merc_availability_audit_20260923');fs.mkdirSync(reportDir,{recursive:true});
fs.writeFileSync(path.join(reportDir,'audit.json'),JSON.stringify(report,null,2)+'\n');
const md=['# Slave and mercenary custom-battle availability audit','',`- Slave-only records: **${report.summary.slaveOnlyRecords}**; changed to limit one: **${report.summary.slaveOnlyLimitsChanged}**.`,`- Mercenary records: **${report.summary.mercenaryRecords}**.`,`- Custom-visible mercenary records: **${report.summary.customAvailableMercenaryRecords}**.`,`- Hidden \`no_custom\` mercenary records: **${report.summary.hiddenMercenaryRecords}**.`,`- Custom-visible subfaction records: **${report.summary.subfactionRecords}**.`,`- Custom-visible standard mercenary records: **${report.summary.standardMercenaryRecords}**.`,'','## Subfaction pools',''];
for(const [name,units] of Object.entries(report.subfactions)){md.push(`### ${name}`,'');for(const u of units)md.push(`- \`${u.type}\` — ${u.dictionary}; limit ${u.limit}.`);md.push('');}
md.push('## Standard mercenaries','');for(const u of report.standardMercenaries)md.push(`- \`${u.type}\` — ${u.dictionary}; limit ${u.limit}.`);
md.push('','## Hidden mercenary records (`no_custom`)','');for(const u of report.hiddenMercenaries)md.push(`- \`${u.type}\` — ${u.dictionary}; limit ${u.limit}.`);
fs.writeFileSync(path.join(reportDir,'audit.md'),md.join('\n')+'\n');
console.log(JSON.stringify(report.summary));
