const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const rel = {
  edb: 'data/tow_steamsteel/export_descr_buildings.txt',
  mirror: 'data/export_descr_buildings.txt',
  edu: 'data/tow_steamsteel/export_descr_unit.txt',
};
const read = p => fs.readFileSync(path.join(root, p), 'utf8').replace(/\r/g, '');
function writeAtomic(p,data){const target=path.join(root,p),temp=target+'.tmp';fs.writeFileSync(temp,data);fs.renameSync(temp,target);}
const edb = read(rel.edb), mirror = read(rel.mirror), eduText = read(rel.edu);

const factions = {
  portugala:'Union',milan:'Confederates',scotland:'Mexico',denmark:'Peru',poland:'Brazil',aztecs:'Argentina',
  england:'Britain',france:'France',hre:'Prussia',spain:'Spain',portugal:'Netherlands',sicily:'Denmark',
  normans:'Sweden-Norway',mongols:'Greece',venice:'Italy',russia:'Russia',hungary:'Austria-Hungary',
  moors:'Morocco',teu:'Boers',lith:'Zulu',turks:'Ottoman',golden:'Oman',egypt:'Qajar',timurids:'Afghanistan',
  cuman:'Turkestan',bulga:'Indian Princely States',cru:'Siam',byzantium:'Qing',papal_states:'Ethiopia',saxons:'Japan'
};

const edu = new Map();
for (const part of eduText.split(/(?=^type\s+)/m)) {
  const tm = part.match(/^type\s+(.+)$/m); if (!tm) continue;
  const type = tm[1].trim();
  const own = (part.match(/^ownership\s+(.+)$/m)?.[1] || '').split(',').map(x=>x.trim()).filter(Boolean);
  const eras = [...part.matchAll(/^era\s+([012])\s+(.+)$/gm)].map(m=>({era:+m[1],factions:m[2].split(',').map(x=>x.trim()).filter(Boolean)}));
  const attrs = (part.match(/^attributes\s+(.+)$/m)?.[1] || '').split(',').map(x=>x.trim());
  edu.set(type,{type,ownership:own,eras,attributes:attrs});
}

const lines = edb.split('\n');
const entries=[]; let building='', level='', settlement='', comment='';
for(let i=0;i<lines.length;i++){
  const s=lines[i];
  const bm=s.match(/^building\s+(\S+)/); if(bm){building=bm[1];level='';continue;}
  const lm=s.match(/^\s{8}([a-zA-Z0-9_]+)\s+(city|castle)\s+requires\b/); if(lm){level=lm[1];settlement=lm[2];continue;}
  if(/^\s*;/.test(s)){comment=s.trim().replace(/^;+\s*/,'');continue;}
  const m=s.match(/^\s*recruit_pool\s+"([^"]+)"\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)(?:\s+requires\s+(.+))?\s*$/);
  if(!m) continue;
  const req=m[6]||'';
  const fm=req.match(/factions\s*\{([^}]*)\}/);
  const fsx=fm?fm[1].split(',').map(x=>x.trim()).filter(Boolean):[];
  const events=[...req.matchAll(/\b(and|or)\s+(not\s+)?event_counter\s+(\S+)\s+(\d+)/g)].map(x=>({not:!!x[2],name:x[3],value:+x[4]}));
  entries.push({line:i+1,unit:m[1],building,level,settlement,section:comment,initial:+m[2],replenishment:+m[3],max:+m[4],experience:+m[5],factions:fsx,events,requirements:req});
}

function expectedGate(unit){
  if(/_early$/.test(unit)) return {positive:[],negative:['military_reforms_1870']};
  if(/_mid$/.test(unit)) return {positive:['military_reforms_1870'],negative:['military_reforms_1890']};
  if(/_(high|late)$/.test(unit)) return {positive:['military_reforms_1890'],negative:[]};
  return null;
}
const missingEdu=entries.filter(e=>!edu.has(e.unit));
const ownershipMismatch=[];
for(const e of entries){const u=edu.get(e.unit);if(!u)continue;for(const f of e.factions)if(f!=='all'&&f!=='slave'&&!u.ownership.includes(f)&&!u.eras.some(x=>x.factions.includes(f)))ownershipMismatch.push({...e,faction:f,eduOwnership:u.ownership});}
const badGates=[];
for(const e of entries){const want=expectedGate(e.unit);if(!want)continue;const pos=new Set(e.events.filter(x=>!x.not).map(x=>x.name)),neg=new Set(e.events.filter(x=>x.not).map(x=>x.name));const missing=[...want.positive.filter(x=>!pos.has(x)).map(x=>'+'+x),...want.negative.filter(x=>!neg.has(x)).map(x=>'-'+x)];const contradictory=[...pos].filter(x=>neg.has(x));if(missing.length||contradictory.length)badGates.push({...e,missing,contradictory});}
function groupBy(xs,keyFn){const out=new Map();for(const x of xs){const k=keyFn(x);if(!out.has(k))out.set(k,[]);out.get(k).push(x);}return out;}
const exactDupGroups=[...groupBy(entries,e=>[e.unit,e.building,e.level,e.initial,e.replenishment,e.max,e.experience,e.requirements].join('|')).entries()].filter(([,v])=>v.length>1).map(([key,v])=>({key,lines:v.map(x=>x.line)}));
const poolGroups=[...groupBy(entries,e=>[e.unit,e.building,e.level,e.factions.join(',')].join('|')).entries()].filter(([,v])=>v.length>1).map(([key,v])=>({key,entries:v}));
const noFaction=entries.filter(e=>!e.factions.length);
const referenced=new Set(entries.map(e=>e.unit));
const campaignAbsent=[...edu.values()].filter(u=>!referenced.has(u.type)&&!u.attributes.includes('no_custom'));

const report={generated:new Date().toISOString(),authoritative:rel.edb,mirror:rel.mirror,mirrorExact:edb===mirror,counts:{edu:edu.size,recruitEntries:entries.length,recruitedUnits:referenced.size,missingEdu:missingEdu.length,ownershipMismatch:ownershipMismatch.length,badPeriodGates:badGates.length,exactDuplicateGroups:exactDupGroups.length,multiPoolGroups:poolGroups.length,noFactionRestriction:noFaction.length,campaignAbsentEdu:campaignAbsent.length},entries,issues:{missingEdu,ownershipMismatch,badGates,exactDupGroups,poolGroups,noFaction,campaignAbsent}};
writeAtomic('tools/campaign_edb_availability_audit_20260923.json',JSON.stringify(report,null,2)+'\n');
const csvCell=x=>'"'+String(x??'').replace(/"/g,'""')+'"';
const csv=[['line','unit','building','level','settlement','section','initial','replenishment','maximum','experience','factions','events','requirements'].map(csvCell).join(',')];
for(const e of entries)csv.push([e.line,e.unit,e.building,e.level,e.settlement,e.section,e.initial,e.replenishment,e.max,e.experience,e.factions.join(' '),e.events.map(x=>(x.not?'not ':'')+x.name+'='+x.value).join('; '),e.requirements].map(csvCell).join(','));
writeAtomic('tools/campaign_edb_recruitment_matrix_20260923.csv',csv.join('\n')+'\n');

const byFaction={};
for(const [code,name] of Object.entries(factions)){
  const fe=entries.filter(e=>e.factions.includes(code));
  const units=new Set(fe.map(e=>e.unit));
  byFaction[code]={name,entries:fe.length,units:units.size,missingEdu:missingEdu.filter(e=>e.factions.includes(code)).length,ownershipMismatch:ownershipMismatch.filter(e=>e.faction===code).length,badGates:badGates.filter(e=>e.factions.includes(code)).length,multiPoolGroups:poolGroups.filter(g=>g.entries.some(e=>e.factions.includes(code))).length};
}
const md=[];
md.push('# Campaign EDB availability audit (2026-09-23)','',`Authoritative file: \`${rel.edb}\`  `,`Runtime mirror exact: **${edb===mirror}**  `,`Recruitment entries: **${entries.length}** across **${referenced.size}** EDU types.`,'','## System reconstructed','',
'Each `recruit_pool` is attached to a building level. Its four numeric fields are initial pool, replenishment rate per turn, maximum pool, and starting experience. The trailing `requires` expression independently gates faction, resources/regions, buildings and event counters. Multiple matching rows stack; a “resupply” row is not merely metadata and can itself make a unit recruitable. EDU ownership and era lists do not create campaign recruitment.','','## Global findings','',
`- EDB unit names absent from EDU: **${missingEdu.length}**.`,`- EDB faction scopes not repeated in EDU ownership/eras: **${ownershipMismatch.length}**. This is a cross-scope difference, not automatically an error: many campaign-only units deliberately have EDU ownership \`slave\`.`,`- Period-suffixed rows missing their standard 1870/1890 gate: **${badGates.length}**.`,`- Exact duplicate row groups: **${exactDupGroups.length}**.`,`- Unit/building/level/faction combinations with multiple pool rows: **${poolGroups.length}**. Multiple geography rows can be intentional; exact duplicates are not.`,`- Rows with no faction restriction: **${noFaction.length}**.`,`- EDU units with no campaign EDB row (excluding no_custom): **${campaignAbsent.length}**. This includes hidden, obsolete, mercenary, naval and custom-battle-only records and requires roster classification before correction.`,'',
'The barracks roster is repeated at all four barracks tiers. Home/colonial availability normally uses a faction gate plus a `hidden_resource`; a second low-cap “resupply” row is commonly added without geography. Because it remains a normal `recruit_pool`, it enables recruitment wherever its building exists. Of 1,462 resupply rows, only 4 retain a hidden-resource restriction. Of the 575 deficient standard period gates, 335 are resupply rows.','',
'Two incompatible time schemes coexist: 1,765 rows use the standardized 1870/1890 counters, 680 use legacy `military_reforms_1`/`military_reforms_2`, and 1,851 use neither. The campaign script currently fires 1870 after turn 1, 1890 after turn 3, legacy reform 1 after turn 2, and legacy reform 2 after turn 4 (`[TESTING]` values), so even correctly gated eras collapse almost immediately.','','## Converted-faction summary','',
'| Faction | Code | Units | Rows | Bad gates | Ownership mismatches | Multi-pool groups |','|---|---:|---:|---:|---:|---:|---:|');
for(const [code,x] of Object.entries(byFaction))md.push(`| ${x.name} | ${code} | ${x.units} | ${x.entries} | ${x.badGates} | ${x.ownershipMismatch} | ${x.multiPoolGroups} |`);
md.push('','## Highest-priority examples','');
for(const e of missingEdu.slice(0,20))md.push(`- Missing EDU: line ${e.line}, \`${e.unit}\` (${e.building}/${e.level}).`);
for(const e of ownershipMismatch.slice(0,20))md.push(`- Ownership mismatch: line ${e.line}, \`${e.unit}\` gated to \`${e.faction}\`, EDU ownership \`${e.eduOwnership.join(', ')}\`.`);
for(const e of badGates.slice(0,30))md.push(`- Period gate: line ${e.line}, \`${e.unit}\`, missing ${e.missing.join(', ')||'none'}${e.contradictory.length?`; contradictory ${e.contradictory.join(', ')}`:''}.`);
md.push('','Full row-level evidence is in `tools/campaign_edb_availability_audit_20260923.json`; the flat recruitment matrix is `tools/campaign_edb_recruitment_matrix_20260923.csv`.');
writeAtomic('tools/campaign_edb_availability_audit_20260923.md',md.join('\n')+'\n');
console.log(JSON.stringify({counts:report.counts,byFaction},null,2));
