const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const eduPath=path.join(root,'data/tow_steamsteel/export_descr_unit.txt');
const edbPath=path.join(root,'data/tow_steamsteel/export_descr_buildings.txt');
const edbMirror=path.join(root,'data/export_descr_buildings.txt');
const regionsPath=path.join(root,'data/world/maps/map_steamsteel/descr_regions.txt');
const mercPath=path.join(root,'data/world/maps/campaign/camp_steamsteel/descr_mercenaries.txt');
const mercMirror=path.join(root,'data/world/maps/campaign/imperial_campaign/descr_mercenaries.txt');
const stratPath=path.join(root,'data/world/maps/campaign/camp_steamsteel/descr_strat.txt');
const backup=path.join(root,'tools/backup_before_mercenary_pool_rebuild_20260925');fs.mkdirSync(backup,{recursive:true});
for(const p of [edbPath,edbMirror,mercPath,mercMirror]){const b=path.join(backup,p.replace(root,'').replace(/^[\\/]/,'').replace(/[\\/]/g,'__'));if(!fs.existsSync(b))fs.copyFileSync(p,b)}

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
// Basic local formations may serve both a custom-battle subfaction and the
// regional campaign mercenary pool. Elite, command and complete roster units do not.
const regionalSubfactionMercenaries=new Set([
 'tib_militia','merc_tib_inf','tib_tribal_archer',
 'korean_archers','Korean Musketeers','Korean Pikemen','korean_rifles_mercs',
 'Japan Ainu Archers','Japan Ainu Teppo','Japan Ainu Geberu','Japan Ainu Minieru',
 'Japan Heimin Mob','Japan Heimin Partisans','Japan Heimin Partisans Geberu','Japan Heimin Partisans Minieru'
]);

const eduText=fs.readFileSync(eduPath,'utf8').replace(/\r/g,'');
const units=new Map();
for(const block of eduText.split(/\n(?=type\s+)/)){
 const type=block.match(/^type\s+(.+)$/m)?.[1].trim();if(!type)continue;
 const attr=block.match(/^attributes\s+(.+)$/m)?.[1]||'';if(!/\bmercenary_unit\b/.test(attr))continue;
 units.set(type,{category:block.match(/^category\s+(\S+)/m)?.[1]||'',cost:+(block.match(/^stat_cost\s+\d+\s*,\s*(\d+)/m)?.[1]||1000),block});
}

const lines=fs.readFileSync(regionsPath,'utf8').replace(/\r/g,'').split('\n');
const regions=[];
for(let i=0;i<lines.length;i++)if(/^[A-Za-z0-9_]+_Province\s*$/.test(lines[i]))regions.push({name:lines[i].trim(),tags:(lines[i+5]||'').split(',').map(x=>x.trim()).filter(Boolean)});
const allRegionNames=new Set(regions.map(x=>x.name));
const byTags=(...tags)=>regions.filter(r=>tags.some(t=>r.tags.includes(t))).map(r=>r.name);
const exact=(...names)=>names;
const union=(...sets)=>[...new Set(sets.flat())];

const centralAmerica=exact('Granada_Province','Domrep_Province','Jamaica_Province','Panama_Province','Mexico_Province','Bolgar_Province','Veracruz_Province','Havana_Province');
const stratLines=fs.readFileSync(stratPath,'utf8').replace(/\r/g,'').split('\n');
const coastal=[];let settlementRegion='',inSettlement=false,hasPort=false;
const flushSettlement=()=>{if(inSettlement&&settlementRegion&&hasPort)coastal.push(settlementRegion);settlementRegion='';hasPort=false};
for(const line of stratLines){if(/^settlement\s*$/.test(line)){flushSettlement();inSettlement=true;continue}if(inSettlement&&/^\s*region\s+(\S+)/.test(line))settlementRegion=line.match(/^\s*region\s+(\S+)/)[1];if(inSettlement&&/^\s*type\s+port\s+/.test(line))hasPort=true;if(inSettlement&&/^(character|settlement|faction)\b/.test(line)&&!/^settlement\s*$/.test(line)){flushSettlement();inSettlement=false}}flushSettlement();
const coastalRegions=[...new Set(coastal)].filter(x=>allRegionNames.has(x));if(!coastalRegions.length)throw new Error('No coastal regions discovered from descr_strat');
const assignments=new Map([
 ['col_12lb',byTags('colonial')],
 ['merc_us_farmer_cav',byTags('settler')],['merc_ap_front_cav',byTags('amerindian')],['merc_apache_inf',byTags('amerindian')],
 ['merc_uru_inf',byTags('uruguay')],['merc_para_foot',byTags('paraguay')],['merc_us_farmers',centralAmerica],
 ['arab_cav',union(byTags('arab'),byTags('north_africa'))],['merc_bhutan_warrior',byTags('himalayan')],['merc_papa_bows',exact('Papua_Province')],
 ['merc_burmese_inf',exact('Taungoo_Province','Lang_sang_Province')],['merc_indian_fanatic',byTags('india')],
 ['merc_maori_spearmen',exact('New_zealand_Province')],['merc_maori_musketeers',exact('New_zealand_Province')],
 ['merc_arab_sailors',byTags('egypt')],['merc_fra_blacks',byTags('sub_sahara')],['merc_eng_for_cav',byTags('egypt')],['merc_fra_for_cav',byTags('north_africa')],
 ['merc_mongol_bows',byTags('mongolia')],['merc_pol_hussars',exact('Cracow_Province','Tejo_Province','Smolensk_Province','Pomeranie_Province')],
 ['merc_polish_inf',exact('Cracow_Province','Tejo_Province','Smolensk_Province','Pomeranie_Province')],['merc_georgian_inf',byTags('georgia')],
 ['merc_serb_inf',exact('Mesie_Province')],['africa_cav',byTags('sub_sahara')],['african_warband',byTags('sub_sahara')],
 ['merc_zulu_rifles',union(byTags('zululand'),byTags('south_africa'))],['fra_blacks_az',exact('Sudan_Province')],['merc_bulgarian_inf',byTags('bulgaria')],
 ['viet_inf',byTags('indochina')],['mongol_hevcav',byTags('mongolia')],['merc_kok_royal_cav',union(byTags('steppe'),byTags('kokand'))],
 ['merc_kashgar_inf',byTags('kokand')],['qing_green_banner_horse',union(byTags('china'),byTags('manchuria'))],
 ['merc_rus_georgian_cav',union(byTags('georgia'),byTags('armenia'))],['merc_zulu_spearmen',union(byTags('zululand'),byTags('south_africa'))],
 ['merc_sikh_warriors',byTags('india')],['merc_fra_inf_ch',exact('Cuzco_Province','Moravie_Province')],['merc_arab_brigade',byTags('arab')],
 ['merc_balk_cav_ch',exact('Cuzco_Province','Moravie_Province')],['merc_siam_agent',exact('Ayudhya_Province')],
 ['merc_uk_sailor',union(byTags('colonial'),byTags('settler'))],
 ['tib_militia',exact('Tibet_Province')],['merc_tib_inf',exact('Tibet_Province')],['tib_tribal_archer',exact('Tibet_Province')],
 ['korean_archers',exact('Korea_Province')],['Korean Musketeers',exact('Korea_Province')],['Korean Pikemen',exact('Korea_Province')],['korean_rifles_mercs',exact('Korea_Province')],
 ['Japan Ainu Archers',exact('Hokkaido_Province')],['Japan Ainu Teppo',exact('Hokkaido_Province')],['Japan Ainu Geberu',exact('Hokkaido_Province')],['Japan Ainu Minieru',exact('Hokkaido_Province')],
 ['Japan Heimin Mob',byTags('japan')],['Japan Heimin Partisans',byTags('japan')],['Japan Heimin Partisans Geberu',byTags('japan')],['Japan Heimin Partisans Minieru',byTags('japan')],
 ['merc galley',coastalRegions],['merc cog',coastalRegions]
]);

const sharedNaval=[...units].filter(([t,u])=>u.category==='ship'&&!['merc galley','merc cog'].includes(t)).map(([t])=>t);
const intended=[...units].filter(([t,u])=>(!subfaction.has(t)||regionalSubfactionMercenaries.has(t))&&(u.category!=='ship'||['merc galley','merc cog'].includes(t))).map(([t])=>t).sort();
const missing=intended.filter(t=>!assignments.has(t));const extra=[...assignments.keys()].filter(t=>!intended.includes(t));
if(missing.length||extra.length)throw new Error(`Assignment mismatch missing=${missing.join(',')} extra=${extra.join(',')}`);
for(const [unit,names] of assignments){if(!names.length)throw new Error(`No regions for ${unit}`);for(const n of names)if(!allRegionNames.has(n))throw new Error(`Unknown region ${n} for ${unit}`)}

const poolName=t=>'Merc_'+t.replace(/[^A-Za-z0-9]+/g,'_').replace(/^_|_$/g,'');
const dateWindow=new Map([
 ['merc_arab_sailors','start_year 1870'],['merc_eng_for_cav','start_year 1870'],['merc_fra_blacks','start_year 1870'],['korean_rifles_mercs','start_year 1870'],
 ['Japan Ainu Teppo','start_year 1861 end_year 1870'],['Japan Ainu Geberu','start_year 1870 end_year 1880'],['Japan Ainu Minieru','start_year 1880'],
 ['Japan Heimin Partisans','start_year 1861 end_year 1870'],['Japan Heimin Partisans Geberu','start_year 1870 end_year 1880'],['Japan Heimin Partisans Minieru','start_year 1880']
]);
const unitLine=(type,u)=>{let replenish='0.05 - 0.10',max=2,initial=1,exp=0;if(u.category==='cavalry'){replenish='0.01 - 0.05';max=1;initial=0}else if(u.category==='siege'||u.category==='ship'){replenish='0.01 - 0.03';max=1;initial=0}const date=dateWindow.has(type)?` ${dateWindow.get(type)}`:'';return `\tunit ${type}\texp ${exp} cost ${u.cost} replenish ${replenish} max ${max} initial ${initial}${date}`};
let out='; Steam & Steel regional mercenary pools\n; Subfaction units are custom-battle-only and deliberately absent.\n; Every genuine regional mercenary record is assigned exactly once.\n\n';
for(const type of intended){const u=units.get(type);out+=`pool ${poolName(type)}\n\tregions ${assignments.get(type).join(' ')}\n${unitLine(type,u)}\n\n`}
fs.writeFileSync(mercPath,out);fs.copyFileSync(mercPath,mercMirror);

let edb=fs.readFileSync(edbPath,'utf8').replace(/\r/g,'');let removedEdbRows=0;
edb=edb.split('\n').filter(line=>{const type=line.match(/^\s*recruit_pool\s+"([^"]+)"/)?.[1];if(type&&subfaction.has(type)){removedEdbRows++;return false}return true}).join('\n');if(!edb.endsWith('\n'))edb+='\n';
fs.writeFileSync(edbPath,edb);fs.copyFileSync(edbPath,edbMirror);

const report={mercenaryUnitRecords:units.size,subfactionRecords:subfaction.size,subfactionRecordsPresent:[...subfaction].filter(x=>units.has(x)).length,regionalSubfactionMercenaries:[...regionalSubfactionMercenaries],campaignMercenaries:intended.length,removedEdbRows,sharedNavalAssetsExcluded:sharedNaval,duplicateRecordsDeleted:[],assignments:Object.fromEntries(intended.map(t=>[t,assignments.get(t)]))};
fs.writeFileSync(path.join(root,'tools/regional_mercenary_pool_report_20260925.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({...report,assignments:undefined},null,2));
