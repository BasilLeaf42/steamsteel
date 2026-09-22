const fs=require('fs'),path=require('path');
const p=path.join(__dirname,'custom_battle_limit_audit.json'),rows=JSON.parse(fs.readFileSync(p,'utf8'));
const balanced=new Set(['Union','Britain','France','Prussia','Spain','Netherlands','Denmark','Sweden–Norway','Greece','Italy','Russia','Austria–Hungary','Ottoman','Oman','Qajar','Afghanistan']);
const lines=['# Custom-battle availability audit','','Counts are `total slots (core + mercenary)` and exclude artillery/ships. A slot is the seventh `stat_cost` field, not model strength.','','| Faction | Status | Early | Mid | Late | Review |','|---|---|---:|---:|---:|---|'];
for(const r of rows){
  const fmt=e=>`${e.total} (${e.core}+${e.mercenary})`;
  const peak=Math.max(...r.eras.map(e=>e.total)),corePeak=Math.max(...r.eras.map(e=>e.core));
  let review='Within current band';
  if(!balanced.has(r.faction)&&peak>30)review='Unbalanced legacy roster: high priority';
  else if(peak>30)review='Large imperial/regional roster; verify auxiliaries each pass';
  else if(corePeak>24)review='Core roster broad; verify lineage overlap';
  else if(Math.min(...r.eras.map(e=>e.total))<8)review='Sparse period roster';
  lines.push(`| ${r.faction} | ${balanced.has(r.faction)?'Balanced':'Pending pass'} | ${fmt(r.eras[0])} | ${fmt(r.eras[1])} | ${fmt(r.eras[2])} | ${review} |`);
}
lines.push('','## Interpretation','','- Normal working band after a completed faction pass: roughly 8–24 non-artillery slots per era, adjusted for state scale and documented colonial/regional breadth.','- Main mass lineages normally receive 2–3 slots. Named specialists, elites, command units, and most cavalry normally receive 1.','- Mercenary or auxiliary records remain visible in this audit even when recruited through campaign pools, because faction ownership also exposes them in custom battle.','- Large pending rosters are findings, not silently normalized: their overlapping lineages and era lists must be resolved during their full faction pass.');
fs.writeFileSync(path.join(__dirname,'custom_battle_limit_audit.md'),lines.join('\n')+'\n');
console.log('Wrote tools/custom_battle_limit_audit.md');
