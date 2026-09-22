const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const tool=path.join(root,'tools/standardize_union.js');
let source=fs.readFileSync(tool,'utf8');
source=source.replace('berdan_inf|ap_front_cav|us_scout_cav|us_zouave','berdan_inf|ap_front_cav|us_front_cav|us_scout_cav|us_zouave');
source=source.replace("if(line.includes('\"berdan_inf\"'))return", "if(line.includes('\"us_front_cav\"'))return [cleanGates(line).replace('\"us_front_cav\"','\"uni_general_staff\"')];if(line.includes('\"berdan_inf\"'))return");
fs.writeFileSync(tool,source);
for(const rel of ['data/tow_steamsteel/export_descr_buildings.txt','data/export_descr_buildings.txt']){const p=path.join(root,rel);let text=fs.readFileSync(p,'utf8');text=text.split('recruit_pool "us_front_cav"').join('recruit_pool "uni_general_staff"');fs.writeFileSync(p,text);}
console.log('Mapped Union general recruitment to the standardized four-man command unit.');
