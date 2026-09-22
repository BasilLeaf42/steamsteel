const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),names={
 l_pith_cav_aztecs:'Argentine Cavalry (Remington Model 1875 revolver and sabre)',
 rus_imp_cav:'General i Shtab (Smith & Wesson No. 3 Russian Model revolver and sabre)',
 balk_cav:'Husaren (Gasser-Revolver M1870 und Saebel)',
 rus_sib_cossacks:'Gholaman-e Shah (Colt Model 1851 Navy revolver and shamshir)'
};
const c=path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),r=path.join(root,'data/export_descr_unit.txt');let s=fs.readFileSync(c,'utf8').replace(/\r\n/g,'\n');
for(const [k,v] of Object.entries(names)){
 const re=new RegExp(`^dictionary\\s+${k}(?:\\s*;.*)?$`,'m');if(!re.test(s))throw Error('Missing exact dictionary '+k);s=s.replace(re,`dictionary       ${k} ; ${v}`);
}
s=s.replace(/\n/g,'\r\n');fs.writeFileSync(c,s);fs.writeFileSync(r,s);
const audit=path.join(__dirname,'audit_unnamed_pistols.js');let a=fs.readFileSync(audit,'utf8');
a=a.replace('|Revolver M1873)', '|Revolver M1873|Remington Model 1875)');fs.writeFileSync(audit,a);
console.log('Corrected exact-key legacy pistol names.');
