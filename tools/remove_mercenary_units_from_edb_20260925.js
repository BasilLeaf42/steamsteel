const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const eduPath=path.join(root,'data/tow_steamsteel/export_descr_unit.txt');
const edbPath=path.join(root,'data/tow_steamsteel/export_descr_buildings.txt');
const mirrorPath=path.join(root,'data/export_descr_buildings.txt');
const edu=fs.readFileSync(eduPath,'utf8').replace(/\r/g,'');
const edb=fs.readFileSync(edbPath,'utf8').replace(/\r/g,'');
const mercenaryTypes=new Set();
for(const part of edu.split(/(?=^type\s+)/m)){
  const type=part.match(/^type\s+(.+)$/m)?.[1].trim();
  const attrs=(part.match(/^attributes\s+(.+)$/m)?.[1]||'').split(',').map(x=>x.trim());
  if(type&&attrs.includes('mercenary_unit'))mercenaryTypes.add(type);
}
// Explicit campaign exception approved by the user: Tibet is shared by Qing and Turkestan.
const tibetanCampaignUnits=new Set(['merc_tib_inf','merc_tib_noble_cav','mercs_tib_monks','tib_heavy_spear','tib_horse_archer','tib_militia','tib_roy_inf','tib_tribal_archer']);
let removedRows=0;const removedTypes=new Set();
const lines=edb.split('\n').filter(line=>{
  if(!/^\s*recruit_pool/.test(line))return true;
  const type=line.match(/recruit_pool\s+"([^"]+)"/)?.[1];
  if(!type||!mercenaryTypes.has(type)||tibetanCampaignUnits.has(type))return true;
  removedRows++;removedTypes.add(type);return false;
});
let out=lines.join('\n');if(!out.endsWith('\n'))out+='\n';
const tmp=edbPath+'.no-merc.tmp';fs.writeFileSync(tmp,out);fs.renameSync(tmp,edbPath);fs.copyFileSync(edbPath,mirrorPath);
console.log(JSON.stringify({mercenaryEduTypes:mercenaryTypes.size,removedRows,removedTypes:removedTypes.size,preservedTibetanException:[...tibetanCampaignUnits].filter(x=>mercenaryTypes.has(x))},null,2));
