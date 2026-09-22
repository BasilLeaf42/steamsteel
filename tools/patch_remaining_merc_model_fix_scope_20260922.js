const fs=require('fs');
const p=require('path').join(__dirname,'fix_remaining_merc_model_animations_20260922.js');
let s=fs.readFileSync(p,'utf8');
const old="replaceOnce('11 MTW2_Musket 20 MTW2_Non_Shield_Fast','20 MTW2_Fast_Arquebus_3 20 MTW2_Non_Shield_Fast','Maori muzzle-loader animation');\nreplaceOnce('13 MTW2_Arquebus 20 MTW2_Non_Shield_Fast','20 MTW2_Fast_Arquebus_3 20 MTW2_Non_Shield_Fast','Bedouin muzzle-loader animation');";
const replacement=`function replaceEntryAnim(name,oldText,newText){
  const esc=x=>x.replace(/[.*+?^\${}()|[\\]\\\\]/g,'\\\\$&');
  const re=new RegExp('(\\\\d+ '+esc(name)+'\\\\s*\\\\r?\\\\n[\\\\s\\\\S]*?\\\\n4 None\\\\s*\\\\r?\\\\n)'+esc(oldText));
  const m=s.match(re); if(!m) throw new Error(name+': scoped animation signature not found');
  s=s.replace(re,(all,prefix)=>prefix+newText);
}
replaceEntryAnim('maori_musketeers','11 MTW2_Musket 20 MTW2_Non_Shield_Fast','20 MTW2_Fast_Arquebus_3 20 MTW2_Non_Shield_Fast');
replaceEntryAnim('arab_brigade','13 MTW2_Arquebus 20 MTW2_Non_Shield_Fast','20 MTW2_Fast_Arquebus_3 20 MTW2_Non_Shield_Fast');`;
if(!s.includes(old)) throw new Error('target calls not found');
fs.writeFileSync(p,s.replace(old,replacement));
