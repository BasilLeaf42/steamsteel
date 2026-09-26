const fs=require('fs');
const eduText=fs.readFileSync('data/tow_steamsteel/export_descr_unit.txt','utf8').replace(/\r/g,'');
const edb=fs.readFileSync('data/tow_steamsteel/export_descr_buildings.txt','utf8').replace(/\r/g,'');
const factions=['portugala','milan','scotland','denmark','poland','aztecs','england','france','hre','spain','portugal','sicily','normans','mongols','venice','russia','hungary','moors','teu','lith','turks','golden','egypt','timurids','cuman','bulga','cru','byzantium','papal_states','saxons'];
const names={portugala:'Union',milan:'Confederates',scotland:'Mexico',denmark:'Peru',poland:'Brazil',aztecs:'Argentina',england:'Britain',france:'France',hre:'Prussia',spain:'Spain',portugal:'Netherlands',sicily:'Denmark',normans:'Sweden-Norway',mongols:'Greece',venice:'Italy',russia:'Russia',hungary:'Austria-Hungary',moors:'Morocco',teu:'Boers',lith:'Zulu',turks:'Ottoman',golden:'Oman',egypt:'Qajar',timurids:'Afghanistan',cuman:'Turkestan',bulga:'Indian States',cru:'Siam',byzantium:'Qing',papal_states:'Ethiopia',saxons:'Japan'};
const excluded=new Set([
  'merc_port_inf_early','merc_port_inf_mid','merc_port_inf_high','merc_port_cav_early','merc_port_cav_mid','merc_port_cav_high',
  'merc_aceh_marines','merc_aceh_noble','merc_aceh_reg','merc_aceh_gold','merc_aceh_warband','merc_aceh_inf',
  'merc_tib_temple_guard','taipingguners','taiping_inf','taiping_light','taiping_w',
  'korean_archers','Korean Byeolgigun','Korean Gimagungsu','Korean Musketeers','Korean Pikemen','korean_rifles_mercs','korean_cav_mercs',
  'mahdist_inf','mahdist_camel_cav','mahdist_cav','Ethiopia Sudanese Musketeers','Ethiopia Sudanese Warriors',
  'Japan Ainu Archers','Japan Ainu Geberu','Japan Ainu Minieru','Japan Ainu Teppo',
  'Japan Heimin Mob','Japan Heimin Partisans','Japan Heimin Partisans Geberu','Japan Heimin Partisans Minieru','Japan Ishin Shishi','Japan Ronin','Japan Shizoku','Japan Teppotai Merc',
]);
const uniqueNamedCampaignExclusions=new Set(['Japan Enomoto Takeaki','Japan Hijikata Toshizo','Japan Itagaki Taisuke','Japan Jules Brunet','Japan Kondo Isami','Japan Matsudaira Katamori','Japan Saigo Takamori 1860','Japan Sakamoto Ryoma','Japan Takeda Ayasaburo','Japan Tokugawa Yoshinobu']);
const records=[];
for(const part of eduText.split(/(?=^type\s+)/m)){
  const tm=part.match(/^type\s+(.+)$/m);if(!tm)continue;
  const type=tm[1].trim(),category=part.match(/^category\s+(.+)$/m)?.[1].trim()||'',attributes=(part.match(/^attributes\s+(.+)$/m)?.[1]||'').split(',').map(x=>x.trim());
  const eras=[...part.matchAll(/^era\s+([012])\s+(.+)$/gm)].flatMap(m=>m[2].split(',').map(x=>x.trim()).filter(Boolean));
  records.push({type,category,attributes,eras:[...new Set(eras)]});
}
const present=new Map(factions.map(f=>[f,new Set()]));
for(const line of edb.split('\n')){if(!/^\s*recruit_pool/.test(line))continue;const u=line.match(/recruit_pool\s+"([^"]+)"/)?.[1],fm=line.match(/factions\s*\{([^}]*)\}/)?.[1];if(!u||!fm)continue;for(const f of fm.split(',').map(x=>x.trim()))if(present.has(f))present.get(f).add(u);}
const result={};let total=0;
for(const f of factions){
  const eligible=records.filter(r=>r.category!=='ship'&&!r.attributes.includes('no_custom')&&!r.attributes.includes('mercenary_unit')&&!excluded.has(r.type)&&!uniqueNamedCampaignExclusions.has(r.type)&&r.eras.includes(f));
  const missing=eligible.filter(r=>!present.get(f).has(r.type)).map(r=>r.type).sort();
  if(missing.length){result[f]={name:names[f],missing:missing.length,units:missing};total+=missing.length;}
}
console.log(JSON.stringify({totalMissingNational:total,factionsAffected:Object.keys(result).length,byFaction:result},null,2));
