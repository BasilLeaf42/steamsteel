const fs=require('fs'),path=require('path');
const p=path.resolve(__dirname,'../data/unit_models/battle_models.modeldb');
let text=fs.readFileSync(p,'utf8').replace(/\r\n/g,'\n');
function entry(name){const a=text.split('\n'),i=a.findIndex(x=>new RegExp(`^${name.length} ${name}\\s*$`).test(x));if(i<0)throw Error(`Missing ${name}`);let j=i;while(j<a.length&&!/^16 -0\.090000004 /.test(a[j]))j++;return a.slice(i,j+1).join('\n');}
for(const name of ['ita_cavalleggeri','ita_general_staff']){const old=entry(name),fresh=old.replace('14 MTW2_HR_Pistol 13 MTW2_HR_Spear','14 MTW2_HR_Pistol 13 MTW2_HR_Sword').replace('21 MTW2_HR_spear_Primary','18 MTW2_Sword_Primary');if(fresh===old)throw Error(`${name}: expected pistol/spear donor slots not found`);text=text.replace(old,fresh);}
fs.writeFileSync(p,text.replace(/\n/g,'\r\n'));
console.log('Italian pistol cavalry model slots corrected to pistol/sabre.');
