const fs=require('fs'),path=require('path');
const src=path.join(__dirname,'backup_before_global_cavalry_role_20260913','tools__validate_union.js');
const out=path.join(__dirname,'validate_union.js');
let lines=fs.readFileSync(src,'utf8').split(/\r?\n/);
lines=lines.map(line=>{
  if(line.startsWith('for(const t of cavalry)'))return "for(const t of cavalry){const b=block(t),expectedClass=['uni_indian_scout_cavalry','uni_general_staff'].includes(t)?'light':'missile';ok(/^category\\s+cavalry$/m.test(b)&&new RegExp('^class\\\\s+'+expectedClass+'$','m').test(b),t+' cavalry class');ok(new RegExp(`^soldier\\\\s+${t}, ${t==='uni_general_staff'?4:24},`,'m').test(b),t+' cavalry strength');ok(/unit_sprites\\/tmp_cavalry_sprite\\.spr/.test(mb(t)),t+' mounted distant sprite');}"
  if(line.startsWith('const legacy='))return line.replace("'apache_inf','rus_sailors_portugala'","'apache_inf','rus_sailors_portugala','merc_us_farmer_cav','merc_ap_front_cav','merc_apache_inf'");
  if(line.includes("State Volunteers mass limit/cost"))return line.replace('1000, 6, 333','1000, 3, 333').replace("'General and Staff pistol/sabre rows');","'General and Staff pistol/sabre rows');ok(/Colt Army Model 1860 revolver and sabre/.test(block('uni_general_staff')),'General and Staff named pistol');");
  return line;
});
fs.writeFileSync(out,lines.join('\n'));
console.log('Restored and safely patched Union validator.');
