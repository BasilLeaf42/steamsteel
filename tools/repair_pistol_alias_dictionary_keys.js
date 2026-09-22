const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const names={
 balk_cav_gr:['balk_cav_gr','Preußische Husaren (Zündnadelpistole M/57 und Säbel)'],
 rus_imp_cav_no:['rus_imp_cav_no','General och stab (Revolver m/1871 och sabel)'],
 rus_sib_cossacks_no:['rus_sib_cossacks_no','Livgardet till häst (Revolver m/1871 och sabel)'],
 rus_imp_cav:['rus_imp_cav','General i Shtab (Smith & Wesson No. 3 Russian Model revolver and sabre)'],
 balk_cav:['balk_cav','Husaren (Gasser-Revolver M1870 und Saebel)'],
 rus_sib_cossacks:['rus_sib_cossacks','Gholaman-e Shah (Colt Model 1851 Navy revolver and shamshir)']
};
function repair(text){
 const n=text.replace(/\r\n/g,'\n'),starts=[...n.matchAll(/^type\s+(\S+)/gm)];let out=n.slice(0,starts[0].index);
 for(let i=0;i<starts.length;i++){
  const t=starts[i][1];let b=n.slice(starts[i].index,i+1<starts.length?starts[i+1].index:n.length);
  if(names[t])b=b.replace(/^dictionary\s+.*$/m,`dictionary       ${names[t][0]} ; ${names[t][1]}`);
  out+=b;
 }
 return out.replace(/\n/g,'\r\n');
}
const c=path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),r=path.join(root,'data/export_descr_unit.txt'),s=repair(fs.readFileSync(c,'utf8'));
fs.writeFileSync(c,s);fs.writeFileSync(r,s);console.log('Restored exact pistol alias dictionary keys and names.');
