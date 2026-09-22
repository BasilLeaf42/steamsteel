const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const backup=path.join(__dirname,'backup_before_global_cavalry_role_20260913');
fs.mkdirSync(backup,{recursive:true});
for(const rel of ['agents.md','tools/standardize_union.js','tools/validate_union.js','data/tow_steamsteel/export_descr_unit.txt']){
  const src=path.join(root,rel),dst=path.join(backup,rel.replaceAll('/','__'));
  if(!fs.existsSync(dst))fs.copyFileSync(src,dst);
}
const must=(s,a,b,label)=>{if(!s.includes(a))throw Error('Missing '+label);return s.replace(a,b)};

const stdPath=path.join(__dirname,'standardize_union.js');
let std=fs.readFileSync(stdPath,'utf8');
std=must(std,"name:'Colt Revolver'","name:'Colt Army Model 1860 revolver'",'Union pistol name');
std=must(std,"eras:[0],limit:6","eras:[0],limit:3",'State Volunteer limit');
std=must(std,"eras:[1],limit:4","eras:[1],limit:3",'mid National Guard limit');
std=must(std,"eras:[2],limit:4","eras:[2],limit:3",'late National Guard limit');
std=must(std,"eras:[0],limit:2},\n {type:'uni_irish_brigade_early'","eras:[0],limit:1},\n {type:'uni_irish_brigade_early'",'USCT limit');
std=must(std,"role:'skirmisher',donor:'us_zouave',card:'us_zouave',eras:[0],limit:2","role:'skirmisher',donor:'us_zouave',card:'us_zouave',eras:[0],limit:1",'Zouave limit');
std=must(std,"card:'us_front_inf',eras:[0],limit:3","card:'us_front_inf',eras:[0],limit:2",'Volunteer Cavalry limit');
std=must(std,"dictionary       ${u.type} ; ${u.label} (mounted command)","dictionary       ${u.type} ; ${u.label} (Colt Army Model 1860 revolver and sabre)",'General pistol dictionary');
std=must(std,"'category         cavalry','class            light','voice_type       Heavy','accent           american','banner faction   main_cavalry'","'category         cavalry',`class            ${u.pistolSpear?'light':'missile'}`,'voice_type       Heavy','accent           american','banner faction   main_cavalry'",'Union carbine class');
std=must(std,"'apache_inf','rus_sailors_portugala'","'apache_inf','rus_sailors_portugala','merc_us_farmer_cav','merc_ap_front_cav','merc_apache_inf'",'Union duplicate merc list');
std=must(std,"${u.type}_descr_short}${u.label}${u.w?` (${u.w.name})`:''}","${u.type}_descr_short}${u.label}${u.command?' (Colt Army Model 1860 revolver and sabre)':u.w?` (${u.w.name})`:''}",'General localization weapon name');
fs.writeFileSync(stdPath,std);

function enforceCarbineClass(text){
  const n=text.replace(/\r\n/g,'\n'),starts=[...n.matchAll(/^type\s+(\S+)/gm)];
  let out=n.slice(0,starts[0].index);
  for(let i=0;i<starts.length;i++){
    let b=n.slice(starts[i].index,i+1<starts.length?starts[i+1].index:n.length);
    if(/^category\s+cavalry$/m.test(b)){
      const pri=(b.match(/^stat_pri\s+(.+)$/m)||[])[1]||'',p=pri.split(',').map(x=>x.trim());
      if(/_carbine_bullet_/.test(pri)&&(+p[3]>60))b=b.replace(/^class\s+(?:light|heavy)$/m,'class            missile');
    }
    out+=b;
  }
  return out.replace(/\n/g,'\r\n');
}
const eduC=path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),eduR=path.join(root,'data/export_descr_unit.txt');
const changed=enforceCarbineClass(fs.readFileSync(eduC,'utf8'));
fs.writeFileSync(eduC,changed);fs.writeFileSync(eduR,changed);

const valPath=path.join(__dirname,'validate_union.js');
let val=fs.readFileSync(valPath,'utf8');
val=must(val,"ok(/^category\\s+cavalry$/m.test(b)&&/^class\\s+light$/m.test(b),t+' cavalry class')","ok(/^category\\s+cavalry$/m.test(b)&&new RegExp(`^class\\\\s+${['uni_indian_scout_cavalry','uni_general_staff'].includes(t)?'light':'missile'}$`,'m').test(b),t+' cavalry class')",'Union cavalry class validator');
val=val.replace("3, 1000, 333, 100, 100, 1000, 6, 333","3, 1000, 333, 100, 100, 1000, 3, 333");
val=must(val,"'apache_inf','rus_sailors_portugala'","'apache_inf','rus_sailors_portugala','merc_us_farmer_cav','merc_ap_front_cav','merc_apache_inf'",'validator duplicate merc list');
val=must(val,"'General and Staff pistol/sabre rows'","'General and Staff pistol/sabre rows');ok(/Colt Army Model 1860 revolver and sabre/.test(block('uni_general_staff')),'General and Staff named pistol'",'named pistol validator');
fs.writeFileSync(valPath,val);

let agents=fs.readFileSync(path.join(root,'agents.md'),'utf8');
agents=agents.replace("Keep melee and pistol/revolver cavalry in `category cavalry` with `class light` or `class heavy` unless the unit is intentionally a ranged missile-cavalry role. Firearm behaviour comes from the weapon rows and attributes, not from `class missile`.","Keep melee and pistol/revolver cavalry in `category cavalry` with `class light` or `class heavy`. Every genuine carbine-armed cavalry unit uses `class missile`; identify it from the loaded weapon row and visible mesh rather than from an inherited class or internal name. Short-range pistol rows that happen to use a legacy carbine projectile token remain light or heavy and are not carbine cavalry.");
agents=agents.replace("Pistols use `magazine_rifle_bullet_c`, 60 range, 15 ammunition, and `musket_shot_set`; copy the rest of the row from a matching pistol-armed precedent.","Pistols use `magazine_rifle_bullet_c`, 60 range, 15 ammunition, and `musket_shot_set`; copy the rest of the row from a matching pistol-armed precedent. Every pistol or revolver is a named weapon: record the historically appropriate exact model in the EDU dictionary comment and localization rather than using generic `pistol` or `revolver` wording.");
agents=agents.replace("The seventh field is the custom-battle limit; treat artillery limits separately unless requested. Reconcile any mercenary-pool cost override.","The seventh field is the custom-battle limit; treat artillery limits separately unless requested. Reconcile any mercenary-pool cost override. Audit the complete per-era custom-battle roster after each faction pass, including shared and mercenary records still carrying faction ownership. Main mass lineages normally receive limits of 2–3, while specialists, elites, regional subtypes, command units, and most cavalry default to 1 unless a documented historical availability case justifies more. Do not let overlapping named militia or mercenary copies inflate the total roster; remove redundant custom-battle ownership while preserving campaign mercenary recruitment.");
agents=agents.replace("a custom-battle limit of 6","a custom-battle limit of 3").replace("Indian Scout Cavalry uses the embedded pistol-and-spear rider equipment; General and Staff uses its embedded pistol with a sabre secondary.","United States Colored Troops, the Irish Brigade, and Zouave Volunteers each have a limit of 1; Union Volunteer Cavalry has a limit of 2. Redundant legacy mercenary copies of the standardized Union frontier units have no Union custom-battle ownership. Indian Scout Cavalry uses the embedded Colt Army Model 1860 revolver-and-spear rider equipment; General and Staff uses the same named revolver with a sabre secondary.");
fs.writeFileSync(path.join(root,'agents.md'),agents);
console.log('Applied Union limit corrections, exact pistol naming, global carbine missile classes, and persistent rules.');
