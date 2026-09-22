const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),canonical=path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),runtime=path.join(root,'data/export_descr_unit.txt');
const targets=['uk_indian_lancers','euro_hussars','gre_lancers','ita_lancieri','rus_ulany','aus_ulanen','ott_mizrakli_suvari'];
let edu=fs.readFileSync(canonical,'utf8').replace(/\r\n/g,'\n');
function update(type){
  const starts=[...edu.matchAll(/^type\s+(.+)$/gm)],i=starts.findIndex(x=>x[1].trim()===type);
  if(i<0)throw Error(`Missing lancer ${type}`);
  const end=i+1<starts.length?starts[i+1].index:edu.length,b=edu.slice(starts[i].index,end);
  const sec=(b.match(/^stat_sec\s+\d+,\s*(\d+),/m)||[])[1],pri=(b.match(/^stat_pri\s+\d+,\s*(\d+),\s*no,.*melee_blade,\s*piercing,\s*spear,/m)||[])[1];
  if(!sec||!pri)throw Error(`${type}: lance/sabre rows not found`);
  const charge=+sec+3;
  const fresh=b.replace(/^(stat_pri\s+\d+,\s*)\d+(,\s*no,.*melee_blade,\s*piercing,\s*spear,)/m,`$1${charge}$2`).replace(/^stat_fire_delay\s+.*$/m,'stat_fire_delay  0');
  edu=edu.slice(0,starts[i].index)+fresh+edu.slice(end);
}
for(const t of targets)update(t);const out=edu.replace(/\n/g,'\r\n');fs.writeFileSync(canonical,out);fs.writeFileSync(runtime,out);console.log(`Applied +3 primary-lance charge to ${targets.length} balanced units.`);
