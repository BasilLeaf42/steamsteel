const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),regP=path.join(__dirname,'historical_card_sources.json');
const records=JSON.parse(fs.readFileSync(regP,'utf8'));
const record={
  id:'uni_general_staff',group_id:'union_general_staff_20260913',unit_type:'uni_general_staff',
  card_file:'data/ui/units/portugala/#uni_general_staff.tga',faction:'portugala',
  name:'General and Staff (mounted command)',role:'mounted command',weapon:'Colt Army Model 1860 revolver (holstered); sabre (sheathed)',
  source_url:'https://www.loc.gov/resource/cph.3a09244/',
  source_file:'tools/historical_card_refs/uni_general_staff_grant_mounted_1863.jpg',
  source_title:'Ulysses S. Grant / C. Schussele 1863; engraved by William Sartain',
  creator:'Charles Schussele; William Sartain',source_date:'1863',
  licence:'Library of Congress: no known restrictions on publication',
  depicted_subject:'Ulysses S. Grant mounted in Union uniform during the American Civil War',
  mapping_note:'The mounted Grant engraving controls the passive seat, Union uniform, horse relationship, tack, and reins. The generated card substitutes a folded campaign map for combat emphasis; no weapon is held, while the named Colt Army Model 1860 remains holstered and the sabre remains sheathed. Close mounted crop follows the shared General-and-Staff card rule.',
  pose_source_id:'',status:'approved',generated_file:'tools/card_generation_sources/uni_general_staff_master.png',crop_box:[0,0,1086,1448]
};
const i=records.findIndex(x=>x.id===record.id);if(i>=0)records[i]=record;else records.push(record);
fs.writeFileSync(regP,JSON.stringify(records,null,2)+'\n');

const stdP=path.join(__dirname,'standardize_union.js');let std=fs.readFileSync(stdP,'utf8');
const a="for(const u of all)if(u.type!=='uni_indian_scout_cavalry')fs.copyFileSync(path.join(cards,`#${u.card}.tga`),path.join(cards,`#${u.type}.tga`));";
const b="for(const u of all)if(!['uni_indian_scout_cavalry','uni_general_staff'].includes(u.type))fs.copyFileSync(path.join(cards,`#${u.card}.tga`),path.join(cards,`#${u.type}.tga`));";
if(std.includes(a))std=std.replace(a,b);else if(!std.includes(b))throw Error('Union card exclusion loop changed');
fs.writeFileSync(stdP,std);

const scoutInstaller=fs.readFileSync(path.join(__dirname,'install_union_scout_card.py'),'utf8');
const generalInstaller=scoutInstaller
  .replace("UNIT = 'uni_indian_scout_cavalry'","UNIT = 'uni_general_staff'")
  .replaceAll('Scout Cavalry','Union General and Staff')
  .replaceAll('Scout card','General card');
fs.writeFileSync(path.join(__dirname,'install_union_general_card.py'),generalInstaller);

const valP=path.join(__dirname,'validate_union.js');let val=fs.readFileSync(valP,'utf8');
const old="const r=registry.find(x=>x.id==='uni_indian_scout_cavalry');ok(r&&r.status==='approved'";
const newer="for(const cardId of ['uni_indian_scout_cavalry','uni_general_staff']){const r=registry.find(x=>x.id===cardId);ok(r&&r.status==='approved'";
if(val.includes(old)){
  val=val.replace(old,newer).replace("for(const p of [r.source_file,r.generated_file])ok(fs.existsSync(path.join(root,p)),'missing Scout card source '+p);}","for(const p of [r.source_file,r.generated_file])ok(fs.existsSync(path.join(root,p)),'missing approved Union card source '+p);}}");
}
fs.writeFileSync(valP,val);
console.log('Registered approved Union General-and-Staff card and persistent installer.');
