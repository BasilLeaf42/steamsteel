const fs=require('fs'),path=require('path');
const R=path.resolve(__dirname,'..'),stamp='backup_before_siam_sword_cavalry_mesh_fix_20260918';
const medbPath=path.join(R,'data/unit_models/battle_models.modeldb');
const eduPaths=[path.join(R,'data/tow_steamsteel/export_descr_unit.txt'),path.join(R,'data/export_descr_unit.txt')];
const scriptPath=path.join(R,'tools/extend_siam_20260918.js');
const backup=path.join(R,'tools',stamp);fs.mkdirSync(backup,{recursive:true});
for(const p of [medbPath,...eduPaths,scriptPath])fs.copyFileSync(p,path.join(backup,path.basename(p).replace('export_descr_unit','export_descr_unit_'+(p.includes('tow_steamsteel')?'canonical':'mirror'))));

let medb=fs.readFileSync(medbPath,'utf8');
if(!/^14 siam_sword_cav\s*$/m.test(medb)){
  const start=medb.search(/^14 Siam_bodyguard\s*$/m);if(start<0)throw Error('Siam_bodyguard model missing');
  const tail=medb.indexOf('16 -0.090000004 0 0 -0.34999999 0.80000001 0.60000002',start);if(tail<0)throw Error('Siam_bodyguard end missing');
  const end=medb.indexOf('\n',tail)+1;let block=medb.slice(start,end);
  const oldMesh='unit_models/_Units/sia/sia_cav_1g_lod0.mesh',newMesh='unit_models/_Units/sia/siam_sword_cav_lod0.mesh';
  block=block.replace(/^14 Siam_bodyguard\s*$/m,'14 siam_sword_cav');
  block=block.split(oldMesh.length+' '+oldMesh).join(newMesh.length+' '+newMesh);
  block=block.replace('1 \n5 Horse \n14 MTW2_HR_Pistol \n13 MTW2_HR_Sword \n1 \n22 MTW2_HR_Pistol_Primary \n1 \n18 MTW2_Sword_Primary \n','1 \n5 Horse \n13 MTW2_HR_Sword 0 \n1 \n18 MTW2_Sword_Primary \n0 \n');
  if(!block.includes('13 MTW2_HR_Sword 0')||block.includes('MTW2_HR_Pistol'))throw Error('animation rewrite failed');
  medb=medb.slice(0,end)+block+medb.slice(end);
  medb=medb.replace(/^(22 serialization::archive 3 0 0 0 0 )(\d+)( 0 0 )/m,(_,a,n,z)=>a+(+n+1)+z);
  fs.writeFileSync(medbPath,medb);
}
for(const p of eduPaths){let s=fs.readFileSync(p,'utf8');const i=s.search(/^type\s+siam_sword_cav\s*$/m),e=s.indexOf('\ntype ',i+5);if(i<0)throw Error('EDU unit missing');let b=s.slice(i,e<0?s.length:e);b=b.replace(/^soldier\s+siam_general,/m,'soldier          siam_sword_cav,');if(!/^soldier\s+siam_sword_cav, 24,/m.test(b))throw Error('EDU rewrite failed');s=s.slice(0,i)+b+s.slice(e<0?s.length:e);fs.writeFileSync(p,s)}
let ext=fs.readFileSync(scriptPath,'utf8').replace('soldier          siam_general, 24, 0, 1','soldier          siam_sword_cav, 24, 0, 1');fs.writeFileSync(scriptPath,ext);
console.log('Installed genuine Siam rider derivative with sabre-only mapping; backups:',stamp);
