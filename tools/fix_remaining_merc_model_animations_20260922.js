const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const p=path.join(root,'data/unit_models/battle_models.modeldb');
const backup=path.join(root,'tools/backup_before_remaining_mercenary_standardization_20260922/battle_models.modeldb');
if(!fs.existsSync(backup)) throw new Error('Required modeldb backup is missing');
let s=fs.readFileSync(p,'utf8');

function replaceOnce(oldText,newText,label){
  const n=s.split(oldText).length-1;
  if(n!==1) throw new Error(`${label}: expected one match, found ${n}`);
  s=s.replace(oldText,newText);
}

if(!/^15 merc_apache_inf\s*$/m.test(s)){
  const re=/^10 apache_inf\s*\r?\n[\s\S]*?^16 -0\.090000004 0 0 -0\.34999999 0\.80000001 0\.60000002\s*$/m;
  const m=s.match(re);
  if(!m) throw new Error('apache_inf model entry not found');
  let clone=m[0].replace(/^10 apache_inf\s*$/m,'15 merc_apache_inf ');
  const oldAnim='18 MTW2_Fast_Musket_3 11 MTW2_2H_Axe';
  if(!clone.includes(oldAnim)) throw new Error('Apache donor animation signature changed');
  clone=clone.replace(oldAnim,'15 MTW2_Musket_SSK 11 MTW2_2H_Axe');
  const header=/^22 serialization::archive 3 0 0 0 0 (\d+) 0 0\s*$/m;
  const hm=s.match(header); if(!hm) throw new Error('modeldb header not found');
  s=s.replace(header,`22 serialization::archive 3 0 0 0 0 ${Number(hm[1])+1} 0 0 `);
  s=s.trimEnd()+'\n'+clone+'\n';
}

function replaceEntryAnim(name,oldText,newText){
  const esc=x=>x.replace(/[.*+?^${}()|[\]\\]/g,'\\replaceOnce('11 MTW2_Musket 20 MTW2_Non_Shield_Fast','20 MTW2_Fast_Arquebus_3 20 MTW2_Non_Shield_Fast','Maori muzzle-loader animation');
replaceOnce('13 MTW2_Arquebus 20 MTW2_Non_Shield_Fast','20 MTW2_Fast_Arquebus_3 20 MTW2_Non_Shield_Fast','Bedouin muzzle-loader animation');');
  const re=new RegExp('(\\d+ '+esc(name)+'\\s*\\r?\\n[\\s\\S]*?\\n4 None\\s*\\r?\\n)'+esc(oldText));
  const m=s.match(re); if(!m) throw new Error(name+': scoped animation signature not found');
  s=s.replace(re,(all,prefix)=>prefix+newText);
}
replaceEntryAnim('maori_musketeers','11 MTW2_Musket 20 MTW2_Non_Shield_Fast','20 MTW2_Fast_Arquebus_3 20 MTW2_Non_Shield_Fast');
replaceEntryAnim('arab_brigade','13 MTW2_Arquebus 20 MTW2_Non_Shield_Fast','20 MTW2_Fast_Arquebus_3 20 MTW2_Non_Shield_Fast');

if(!/^15 merc_apache_inf\s*$/m.test(s) || !s.includes('15 MTW2_Musket_SSK 11 MTW2_2H_Axe')) throw new Error('Apache clone validation failed');
fs.writeFileSync(p,s);
console.log('Installed isolated Hall-rifle SSK mapping and corrected two muzzle-loader animation mappings.');
