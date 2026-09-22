const fs=require('fs'),path=require('path');
const p=path.join(__dirname,'audit_custom_battle_limits.js');let lines=fs.readFileSync(p,'utf8').split(/\r?\n/),out=[];
for(const line of lines){
  if(line.includes('row.eras.push({era:+era, types:combat.length')){
    out.push("    row.eras.push({era:+era, types:combat.length, total:combat.reduce((n,u)=>n+u.limit,0), core:combat.filter(u=>!u.type.startsWith('merc_')).reduce((n,u)=>n+u.limit,0), mercenary:combat.filter(u=>u.type.startsWith('merc_')).reduce((n,u)=>n+u.limit,0), artillery,");
  }else if(line.startsWith('for (const r of report) console.log(')){
    out.push("for (const r of report) console.log(`${r.faction}\\t${r.eras.map(x=>`${x.types}/${x.total} (${x.core}+${x.mercenary})`).join('\\t')}\\t${r.eras.flatMap(x=>x.multi).filter((x,i,a)=>a.indexOf(x)===i).join(', ') || '-'}`);");
  }else out.push(line);
}
fs.writeFileSync(p,out.join('\n'));
console.log('Added core and mercenary totals to custom-battle audit.');
