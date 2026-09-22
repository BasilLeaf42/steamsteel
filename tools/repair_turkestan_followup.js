const fs=require('fs'),path=require('path'),R=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(R,p),'utf8').replace(/\r/g,'');
const write=(p,s)=>fs.writeFileSync(path.join(R,p),s.replace(/\n/g,'\r\n'),'utf8');
function block(text,type){const m=text.match(new RegExp(`^type\\s+${type}\\n[\\s\\S]*?(?=^type\\s+|(?![\\s\\S]))`,'m'));if(!m)throw Error('missing '+type);return m[0]}
function replaceBlock(text,type,next){const old=block(text,type);return text.replace(old,next.trimEnd()+'\n\n')}
let edu=read('data/tow_steamsteel/export_descr_unit.txt');
for(const type of ['kaz_inf','kok_ww1','kaz_cav','merc_kaz_inf','merc_kaz_cav']) edu=edu.replace(block(edu,type),'');
write('data/tow_steamsteel/export_descr_unit.txt',edu);write('data/export_descr_unit.txt',edu);
let edb=read('data/tow_steamsteel/export_descr_buildings.txt');
edb=edb.split('\n').filter(l=>!/^\s*recruit_pool\s+"(?:kaz_inf|kok_ww1|kaz_cav)"/.test(l)).join('\n');
write('data/tow_steamsteel/export_descr_buildings.txt',edb);write('data/export_descr_buildings.txt',edb);
let merc=read('data/world/maps/campaign/camp_steamsteel/descr_mercenaries.txt');
merc=merc.split('\n').filter(l=>!/^\s*unit\s+merc_kaz_(?:inf|cav)\b/.test(l)).join('\n');
write('data/world/maps/campaign/camp_steamsteel/descr_mercenaries.txt',merc);
let strat=read('data/world/maps/campaign/camp_steamsteel/descr_strat.txt');
strat=strat.replace(/^(\s*unit\s+)kok_ww1(\s+)/gm,'$1turkmen_inf$2').replace(/^(\s*unit\s+)kaz_inf(\s+)/gm,'$1turkmen_inf$2').replace(/^(\s*unit\s+)merc_kaz_inf(\s+)/gm,'$1turkmen_inf$2').replace(/^(\s*unit\s+)merc_kaz_cav(\s+)/gm,'$1kok_cav$2');
write('data/world/maps/campaign/camp_steamsteel/descr_strat.txt',strat);write('data/world/maps/campaign/imperial_campaign/descr_strat.txt',strat);
let rebels=read('data/descr_rebel_factions.txt').replace(/^(\s*unit\s+)kaz_inf\s*$/gm,'$1turkmen_inf').replace(/^(\s*unit\s+)kok_ww1\s*$/gm,'$1turkmen_inf').replace(/^(\s*unit\s+)kaz_cav\s*$/gm,'$1kok_cav');
write('data/descr_rebel_factions.txt',rebels);
console.log('Removed broken Kazakh infantry, Bahodirlar and Qozoq cavalry records and replaced every active reference.');
