const fs=require('fs');
const report=JSON.parse(fs.readFileSync('tools/regional_mercenary_pool_report_20260925.json','utf8'));
const merc=fs.readFileSync('data/world/maps/campaign/camp_steamsteel/descr_mercenaries.txt','utf8').replace(/\r/g,'');
const mirror=fs.readFileSync('data/world/maps/campaign/imperial_campaign/descr_mercenaries.txt','utf8').replace(/\r/g,'');
const edb=fs.readFileSync('data/tow_steamsteel/export_descr_buildings.txt','utf8').replace(/\r/g,'');
const edbMirror=fs.readFileSync('data/export_descr_buildings.txt','utf8').replace(/\r/g,'');
const expected=Object.keys(report.assignments);
const subfaction=new Set([
 'merc_port_inf_early','merc_port_inf_mid','merc_port_inf_high','merc_port_cav_early','merc_port_cav_mid','merc_port_cav_high',
 'merc_aceh_marines','merc_aceh_noble','merc_aceh_reg','merc_aceh_gold','merc_aceh_warband','merc_aceh_inf','merc_tib_temple_guard','taipingguners','taiping_inf','taiping_light','taiping_w','tib_temple_guard','merc_tib_noble_cav','tib_militia','merc_tib_inf','tib_horse_archer','tib_roy_inf','tib_tribal_archer','tib_temple_guard','tib_heavy_spear','mercs_tib_monks','korean_archers','Korean Byeolgigun','Korean Gimagungsu','Korean Musketeers','Korean Pikemen','korean_rifles_mercs','korean_cav_mercs','mahdist_inf','mahdist_camel_cav','mahdist_cav','Ethiopia Sudanese Musketeers','Ethiopia Sudanese Warriors','Japan Ainu Archers','Japan Ainu Geberu','Japan Ainu Minieru','Japan Ainu Teppo','Japan Heimin Mob','Japan Heimin Partisans','Japan Heimin Partisans Geberu','Japan Heimin Partisans Minieru','Japan Ishin Shishi','Japan Ronin','Japan Shizoku','Japan Teppotai Merc'
]);
const allowedRegionalSubfaction=new Set(report.regionalSubfactionMercenaries||[]);
const counts=new Map(expected.map(x=>[x,0]));const unknown=[];
for(const line of merc.split('\n')){
 if(!/^\s*unit\s+/.test(line))continue;
 const body=line.replace(/^\s*unit\s+/,'');
 const type=[...expected].sort((a,b)=>b.length-a.length).find(x=>body===x||body.startsWith(x+'\t')||body.startsWith(x+' '));
 if(!type)unknown.push(line.trim());else counts.set(type,counts.get(type)+1);
}
const missing=[...counts].filter(([,n])=>n===0).map(([u])=>u),duplicates=[...counts].filter(([,n])=>n>1).map(([u,n])=>({unit:u,count:n}));
const subPool=[...subfaction].filter(u=>!allowedRegionalSubfaction.has(u)&&(merc.includes(`unit ${u}\t`)||merc.includes(`unit ${u} `)));
const subEdb=[...subfaction].filter(u=>new RegExp(`recruit_pool\\s+"${u.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}"`).test(edb));
const result={ok:merc===mirror&&edb===edbMirror&&!missing.length&&!duplicates.length&&!unknown.length&&!subPool.length&&!subEdb.length,mercenaryPoolMirrorsMatch:merc===mirror,edbMirrorsMatch:edb===edbMirror,assignedExactlyOnce:[...counts].filter(([,n])=>n===1).length,expected:expected.length,missing,duplicates,unknown,subfactionPoolUnits:subPool,subfactionEdbUnits:subEdb};
console.log(JSON.stringify(result,null,2));if(!result.ok)process.exitCode=1;
