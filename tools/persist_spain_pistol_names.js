const fs=require('fs'),path=require('path');
const p=path.join(__dirname,'normalize_restored_spain.js');let s=fs.readFileSync(p,'utf8');
for(const [a,b] of [
 ["'Caballería Indígenas','spa_scout_cav','pistol'","'Caballería Indígenas (Revolver Lefaucheux Modelo 1858 and sabre)','spa_scout_cav','pistol'"],
 ["'Coracero','bol_hussar','cuirass'","'Coracero (Revolver Lefaucheux Modelo 1858 and sabre)','bol_hussar','cuirass'"],
 ["'General y Estado Mayor','spa_general_staff','general'","'General y Estado Mayor (Revolver Lefaucheux Modelo 1858 and sabre)','spa_general_staff','general'"]
]){
 if(!s.includes(a))throw Error('Missing Spain pistol label '+a);s=s.replace(a,b);
}
fs.writeFileSync(p,s);console.log('Persisted exact Spanish pistol names.');
