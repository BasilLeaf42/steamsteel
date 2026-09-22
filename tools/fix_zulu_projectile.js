const fs=require('fs'),path=require('path'),R=path.resolve(__dirname,'..');
for(const rel of ['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt']){
  const p=path.join(R,rel),s=fs.readFileSync(p,'utf8');
  const out=s.replace(/(^type\s+zulu_elite[\s\S]*?stat_pri\s+37, 0, )musket_bullet_c/m,'$1musket_bullet_b');
  if(out===s)throw Error('zulu_elite projectile not found in '+rel);
  fs.writeFileSync(p,out);
}
console.log('Corrected iNduna Nezikhulu to elite D-tier musket_bullet_b.');
