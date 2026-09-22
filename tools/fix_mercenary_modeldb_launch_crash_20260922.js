const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const modelPath=path.join(root,'data/unit_models/battle_models.modeldb');
const backupPath=path.join(root,'tools/backup_before_remaining_mercenary_standardization_20260922/battle_models.modeldb');
const canonPath=path.join(root,'data/tow_steamsteel/export_descr_unit.txt');
const runtimePath=path.join(root,'data/export_descr_unit.txt');
const locPath=path.join(root,'data/text/export_units.txt');
if(!fs.existsSync(backupPath))throw new Error('Known-good modeldb backup missing');

// Restore the complete valid archive; never append model entries as raw text.
let model=fs.readFileSync(backupPath,'utf8');
function scopedAnim(name,oldText,newText){
 const esc=x=>x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const re=new RegExp('(^\\d+ '+esc(name)+'\\s*\\r?\\n[\\s\\S]*?^4 None\\s*\\r?\\n)'+esc(oldText),'m');
 if(!re.test(model))throw new Error(name+' animation signature missing');
 model=model.replace(re,(all,prefix)=>prefix+newText);
}
scopedAnim('apache_inf','18 MTW2_Fast_Musket_3 11 MTW2_2H_Axe','20 MTW2_Fast_Arquebus_3 11 MTW2_2H_Axe');
scopedAnim('maori_musketeers','11 MTW2_Musket 20 MTW2_Non_Shield_Fast','20 MTW2_Fast_Arquebus_3 20 MTW2_Non_Shield_Fast');
scopedAnim('arab_brigade','13 MTW2_Arquebus 20 MTW2_Non_Shield_Fast','20 MTW2_Fast_Arquebus_3 20 MTW2_Non_Shield_Fast');
if(/^15 merc_apache_inf\s*$/m.test(model))throw new Error('Apache clone survived restoration');
fs.writeFileSync(modelPath,model);

let edu=fs.readFileSync(canonPath,'utf8');
const re=/(^type\s+merc_apache_inf\s*$[\s\S]*?)(?=^type\s+|(?![\s\S]))/m;
const m=edu.match(re);if(!m)throw new Error('merc_apache_inf EDU record missing');
let b=m[1];
function field(name,value){const fr=new RegExp('^'+name+'\\s+.*$','m');if(!fr.test(b))throw new Error('Apache '+name+' missing');b=b.replace(fr,name.padEnd(17)+value);}
field('dictionary','merc_apache_inf ; Apache Mercenaries (Pattern 1853 Enfield Rifle-Musket)');
field('soldier','apache_inf, 30, 0, 1');
field('attributes','free_upkeep_unit, sea_faring, hide_forest, gunmen, start_not_skirmishing, mercenary_unit, gunpowder_unit');
field('stat_pri','29, 1, rifled_musket_bullet_b, 260, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999');
edu=edu.replace(re,()=>b);fs.writeFileSync(canonPath,edu);fs.writeFileSync(runtimePath,edu);

let loc=fs.readFileSync(locPath,'utf8');
loc=loc.replace(/^\{merc_apache_inf_descr_short\}[^\r\n]*/m,'{merc_apache_inf_descr_short}Apache Mercenaries (Pattern 1853 Enfield Rifle-Musket)');
loc=loc.replace(/^\{merc_apache_inf_descr\}([^\r\n]*)/m,(line,desc)=>'{merc_apache_inf_descr}'+desc.replace(/Hall rifles/g,'Pattern 1853 Enfield rifle-muskets'));
fs.writeFileSync(locPath,loc);
console.log('Restored valid modeldb archive, retained two scoped muzzle-animation fixes, and returned Apache to its verified shared model.');
