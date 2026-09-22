const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const replace=(s,a,b,label)=>{if(!s.includes(a))throw Error('Missing '+label);return s.replace(a,b)};

// Persist exact weapon names in active faction builders.
for(const spec of [
  ['standardize_qajar.js',[["pistol?'pistol and shamshir'","pistol?'Colt Model 1851 Navy revolver and shamshir'"],["u.kind==='pistol'?'pistol and shamshir'","u.kind==='pistol'?'Colt Model 1851 Navy revolver and shamshir'"]]],
  ['standardize_russia.js',[["'revolver and sabre'","'Smith & Wesson No. 3 Russian Model revolver and sabre'"]]],
  ['standardize_austria.js',[["u.kind==='cuirass'?`${u.label} (Revolver und Saebel)`:u.kind==='general'?u.label:`${u.label} (Revolver und Saebel)`","u.kind==='cuirass'?`${u.label} (Gasser-Revolver M1870 und Saebel)`:u.kind==='general'?`${u.label} (Gasser-Revolver M1870 und Saebel)`:`${u.label} (Gasser-Revolver M1870 und Saebel)`"],["u.kind==='general'?'mounted command staff':'Revolver und Säbel'","u.kind==='general'?'mounted command staff; Gasser-Revolver M1870 holstered':'Gasser-Revolver M1870 und Säbel'"]]],
]){
  const p=path.join(__dirname,spec[0]);let s=fs.readFileSync(p,'utf8');
  for(const [a,b] of spec[1])s=replace(s,a,b,spec[0]+' weapon name');
  fs.writeFileSync(p,s);
}

// Persist the universal class rule in the remaining builders that had hard-coded classes.
for(const [file,edits] of [
  ['normalize_restored_spain.js',[["`class            ${heavy}`","`class            ${carbine?'missile':heavy}`"]]],
  ['standardize_afghanistan.js',[["'category         cavalry','class            light','voice_type       Heavy'","'category         cavalry',`class            ${camel?'missile':'light'}`,'voice_type       Heavy'"]]],
  ['standardize_france.js',[["className:'heavy', armament:'carbine'","className:'missile', armament:'carbine'"],["className:'light', armament:'carbine'","className:'missile', armament:'carbine'"]]],
  ['standardize_prussia.js',[["className:'heavy',armament:'carbine'","className:'missile',armament:'carbine'"],["className:'light',armament:'carbine'","className:'missile',armament:'carbine'"]]],
]){
  const p=path.join(__dirname,file);let s=fs.readFileSync(p,'utf8');
  for(const [a,b] of edits)s=s.replaceAll(a,b);
  fs.writeFileSync(p,s);
}

const exact={
  spa_col_cav_mid:'Caballería Indígenas (Revolver Lefaucheux Modelo 1858 and sabre)',
  spa_cuirassiers_early:'Coracero (Revolver Lefaucheux Modelo 1858 and sabre)',
  civil_guard:'General y Estado Mayor (Revolver Lefaucheux Modelo 1858 and sabre)',
  qaj_horse_guard:'Gholaman-e Shah (Colt Model 1851 Navy revolver and shamshir)',
  rus_gusary:'Gusary (Smith & Wesson No. 3 Russian Model revolver and sabre)',
  rus_guard_cuirassiers:'Gvardeyskiye Kirasiry (Smith & Wesson No. 3 Russian Model revolver and sabre)',
  rus_general_staff:'General i Shtab (Smith & Wesson No. 3 Russian Model revolver and sabre)',
  aus_kuerassiere:'Kuerassiere (Gasser-Revolver M1870 und Saebel)',
  aus_husaren:'Husaren (Gasser-Revolver M1870 und Saebel)',
  aus_general_staff:'General und Stab (Gasser-Revolver M1870 und Saebel)'
};
function rewriteEdu(text){
  const n=text.replace(/\r\n/g,'\n'),starts=[...n.matchAll(/^type\s+(\S+)/gm)];let out=n.slice(0,starts[0].index);
  for(let i=0;i<starts.length;i++){
    const t=starts[i][1];let b=n.slice(starts[i].index,i+1<starts.length?starts[i+1].index:n.length);
    if(exact[t])b=b.replace(/^dictionary\s+\S+.*$/m,`dictionary       ${t} ; ${exact[t]}`);
    out+=b;
  }
  return out.replace(/\n/g,'\r\n');
}
const eduC=path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),eduR=path.join(root,'data/export_descr_unit.txt');
const edu=rewriteEdu(fs.readFileSync(eduC,'utf8'));fs.writeFileSync(eduC,edu);fs.writeFileSync(eduR,edu);

// Update displayed short descriptions without disturbing UTF-16LE encoding.
const locP=path.join(root,'data/text/export_units.txt');let raw=fs.readFileSync(locP),bom=raw[0]===255&&raw[1]===254;
let loc=raw.slice(bom?2:0).toString('utf16le').replace(/\r\n/g,'\n');
for(const [t,name] of Object.entries(exact))loc=loc.replace(new RegExp(`^\\{${t}_descr_short\\}.*$`,'m'),`{${t}_descr_short}${name}`);
fs.writeFileSync(locP,Buffer.concat([Buffer.from([255,254]),Buffer.from(loc.replace(/\n/g,'\r\n'),'utf16le')]));

console.log('Persisted exact pistol names and universal carbine missile-class builders.');
