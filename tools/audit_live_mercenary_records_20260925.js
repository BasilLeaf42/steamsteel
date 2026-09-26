const fs=require('fs');
const edu=fs.readFileSync('data/tow_steamsteel/export_descr_unit.txt','utf8').replace(/\r/g,'');
const text=fs.readFileSync('data/text/export_units.txt','utf8').replace(/\r/g,'');
const loc=new Map([...text.matchAll(/^\{([^}]+)\}([^\n]*)$/gm)].map(m=>[m[1],m[2].trim()]));
const subfaction=new Set([
  'merc_port_inf_early','merc_port_inf_mid','merc_port_inf_high','merc_port_cav_early','merc_port_cav_mid','merc_port_cav_high',
  'merc_aceh_marines','merc_aceh_noble','merc_aceh_reg','merc_aceh_gold','merc_aceh_warband','merc_aceh_inf',
  'merc_tib_temple_guard','taipingguners','taiping_inf','taiping_light','taiping_w','tib_temple_guard',
  'merc_tib_noble_cav','tib_militia','merc_tib_inf','tib_horse_archer','tib_roy_inf','tib_tribal_archer','tib_heavy_spear','mercs_tib_monks',
  'korean_archers','Korean Byeolgigun','Korean Gimagungsu','Korean Musketeers','Korean Pikemen','korean_rifles_mercs','korean_cav_mercs',
  'mahdist_inf','mahdist_camel_cav','mahdist_cav','Ethiopia Sudanese Musketeers','Ethiopia Sudanese Warriors',
  'Japan Ainu Archers','Japan Ainu Geberu','Japan Ainu Minieru','Japan Ainu Teppo',
  'Japan Heimin Mob','Japan Heimin Partisans','Japan Heimin Partisans Geberu','Japan Heimin Partisans Minieru','Japan Ishin Shishi','Japan Ronin','Japan Shizoku','Japan Teppotai Merc'
]);
const units=[];
for(const block of edu.split(/\n(?=type\s+)/)){
 const type=block.match(/^type\s+(.+)$/m)?.[1].trim(); if(!type||!/^attributes\s+.*\bmercenary_unit\b/m.test(block))continue;
 const dict=block.match(/^dictionary\s+(\S+)/m)?.[1]||type;
 const category=block.match(/^category\s+(\S+)/m)?.[1]||'';
 // Dictionary comments carry the exact named weapon; visually shared period
 // variants are not duplicates when their documented equipment differs.
 const signature=block.split('\n').filter(l=>! /^(type|ownership|era\s)/.test(l)).join('\n').trim();
 units.push({type,dict,display:loc.get(dict)||'',category,subfaction:subfaction.has(type),signature});
}
const groups=new Map();for(const u of units){if(!groups.has(u.signature))groups.set(u.signature,[]);groups.get(u.signature).push(u.type)}
const duplicates=[...groups.values()].filter(g=>g.length>1);
const result={total:units.length,subfaction:units.filter(x=>x.subfaction).length,standard:units.filter(x=>!x.subfaction).length,duplicates,unclassifiedSubfactionNames:units.filter(x=>!x.subfaction&&/taiping|tib_|korean|Korean|mahdist|Sudanese|Japan (?:Ainu|Heimin|Ishin|Ronin|Shizoku|Teppotai)|merc_aceh|merc_port_/i.test(x.type)).map(x=>x.type),units:units.map(({signature,...x})=>x)};
fs.writeFileSync('tools/live_mercenary_record_audit_20260925.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({...result,units:undefined},null,2));
