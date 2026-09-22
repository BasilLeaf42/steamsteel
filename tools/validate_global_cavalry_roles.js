const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),edu=fs.readFileSync(path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),'utf8').replace(/\r/g,'');
const starts=[...edu.matchAll(/^type\s+(\S+)/gm)];let carbines=0;
for(let i=0;i<starts.length;i++){
  const t=starts[i][1],b=edu.slice(starts[i].index,i+1<starts.length?starts[i+1].index:edu.length);
  if(!/^category\s+cavalry$/m.test(b))continue;
  const pri=(b.match(/^stat_pri\s+(.+)$/m)||[])[1]||'',p=pri.split(',').map(x=>x.trim());
  if(/_carbine_bullet_/.test(pri)&&+p[3]>60){
    if(!/^class\s+missile$/m.test(b))throw Error(`${t}: genuine carbine cavalry is not class missile`);
    carbines++;
  }
}
const exact=['uni_general_staff','uni_indian_scout_cavalry','spa_col_cav_mid','spa_cuirassiers_early','civil_guard','qaj_horse_guard','rus_gusary','rus_guard_cuirassiers','rus_general_staff','aus_kuerassiere','aus_husaren','aus_general_staff'];
for(const t of exact){
  const i=starts.findIndex(x=>x[1]===t),b=edu.slice(starts[i].index,i+1<starts.length?starts[i+1].index:edu.length),d=(b.match(/^dictionary\s+(.+)$/m)||[])[1]||'';
  if(!/(?:Colt Army Model 1860|Revolver Lefaucheux Modelo 1858|Colt Model 1851 Navy|Smith & Wesson No\. 3 Russian Model|Gasser-Revolver M1870)/.test(d))throw Error(`${t}: pistol model is not named`);
}
console.log(`Global cavalry validation passed: ${carbines} genuine carbine records use class missile; named-pistol audit passed.`);
