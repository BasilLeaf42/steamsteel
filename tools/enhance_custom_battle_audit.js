const fs=require('fs'),path=require('path');
const p=path.join(__dirname,'audit_custom_battle_limits.js');let s=fs.readFileSync(p,'utf8');
const old="row.eras.push({era:+era, types:combat.length, total:combat.reduce((n,u)=>n+u.limit,0), artillery,\n+      multi:combat.filter(u=>u.limit>1).map(u=>`${u.type}:${u.limit}`)});";
const newer="row.eras.push({era:+era, types:combat.length, total:combat.reduce((n,u)=>n+u.limit,0), core:combat.filter(u=>!u.type.startsWith('merc_')).reduce((n,u)=>n+u.limit,0), mercenary:combat.filter(u=>u.type.startsWith('merc_')).reduce((n,u)=>n+u.limit,0), artillery,\n+      multi:combat.filter(u=>u.limit>1).map(u=>`${u.type}:${u.limit}`)});";
if(s.includes(old))s=s.replace(old,newer);else if(!s.includes('mercenary:combat.filter'))throw Error('Audit insertion point changed');
s=s.replace("`${x.types}/${x.total}`","`${x.types}/${x.total} (${x.core}+${x.mercenary})`");
fs.writeFileSync(p,s);
console.log('Enhanced custom-battle audit with core and mercenary slot totals.');
