const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const canonical = path.join(root, 'data/tow_steamsteel/export_descr_buildings.txt');
const mirror = path.join(root, 'data/export_descr_buildings.txt');
let text = fs.readFileSync(canonical, 'utf8').replace(/\r/g, '');

// Remove Confederate access only, preserving other owners of shared rows.
const kept = [];
for (const line of text.split('\n')) {
  if (!/^\s*recruit_pool\s+/.test(line) || !/\bfactions\s*\{[^}]*\bmilan\b/.test(line)) { kept.push(line); continue; }
  const m = line.match(/\bfactions\s*\{([^}]*)\}/);
  if (!m) throw new Error(`Cannot parse faction list: ${line}`);
  const factions = m[1].split(',').map(x => x.trim()).filter(Boolean).filter(x => x !== 'milan');
  if (factions.length) kept.push(line.replace(m[0], `factions { ${factions.join(', ')}, }`).trimEnd());
}
text = kept.join('\n');

const ev = y => y === 1900 ? 'event_counter military_reforms_2 1' : `event_counter military_reforms_${y} 1`;
const windows = {
  all: [], to1865:[`not ${ev(1865)}`], from1865to1890:[ev(1865),`not ${ev(1890)}`],
  to1870:[`not ${ev(1870)}`], to1875:[`not ${ev(1875)}`],
  from1870to1890:[ev(1870),`not ${ev(1890)}`], from1870:[ev(1870)],
  from1875to1885:[ev(1875),`not ${ev(1885)}`], from1885:[ev(1885)],
  from1890:[ev(1890)], to1890:[`not ${ev(1890)}`]
};
const europeanized = ['csa','europe'];
const U = (type,n,quality,window,geo) => ({type,n,quality,window,geo});
const barracks = [
  U('csa_state_volunteers_early',3,'militia','to1875','europeanized'),
  U('csa_state_guard_mid',4,'militia','from1875to1885','europeanized'),
  U('csa_state_guard_high',4,'militia','from1885','europeanized'),
  U('csa_regulars_early',2,'regular','to1875','europeanized'),
  U('csa_regulars_mid',2,'regular','from1875to1885','europeanized'),
  U('csa_regulars_high',2,'regular','from1885','europeanized'),
  U('csa_louisiana_tigers',2,'militia','to1870',['csa']),
  U('csa_sharpshooters',1,'regular','to1870',['csa']),
  U('csa_state_cavalry_early',1,'militia','to1865',['csa']),
  U('csa_state_cavalry_mid',1,'militia','from1865to1890',['csa']),
  U('csa_state_cavalry_high',1,'militia','from1890',['csa']),
  U('csa_virginia_cavalry',1,'militia','to1870',['csa'])
];
const levels = [['militia_drill_square',0],['militia_barracks',1],['army_barracks',2],['royal_armoury',3]];
const tuples = {1:[[1,.01,1],[1,.03,1],[1,.06,1],[1,.10,1]],2:[[1,.02,1],[1,.06,1],[2,.12,2],[2,.20,2]],3:[[1,.03,1],[1,.09,1],[2,.18,2],[3,.30,3]],4:[[1,.04,1],[1,.12,1],[3,.24,3],[4,.40,4]],5:[[1,.05,2],[2,.15,2],[3,.30,3],[5,.50,5]]};
const fmt = n => Number.isInteger(n) ? String(n) : String(n).replace(/^0\./,'.');
const row = (type,a,r,m,parts=[]) => `\trecruit_pool "${type}"  ${fmt(a)}   ${fmt(r)}   ${fmt(m)}  0  requires factions { milan, }${parts.length?' and '+parts.join(' and '):''}`;
const replenish = u => row(u.type, +(u.n*.2).toFixed(2), +(u.n*.02).toFixed(2), .99, windows[u.window]);
const additions = new Map();
for (const [level,i] of levels) {
  const rows = [';confederate standardized normal recruitment'];
  for (const u of barracks) {
    if (u.quality === 'regular' && i === 0) continue;
    const [a,r,m] = tuples[u.n][i], geos = u.geo === 'europeanized' ? europeanized : u.geo;
    for (const g of geos) rows.push(row(u.type,a,r,m,[`hidden_resource ${g}`,...windows[u.window]]));
  }
  rows.push(';confederate standardized replenishment');
  for (const u of barracks) rows.push(replenish(u));
  additions.set(`barracks/${level}`,rows);
}
for (const [level,i] of [['port',0],['shipwright',1],['dockyard',2],['naval_drydock',3]]) {
  const u=U('csa_marines',1,'regular','to1870',['usa']), [a,r,m]=tuples[1][i];
  additions.set(`port/${level}`,[';confederate standardized marine recruitment',row(u.type,a,r,m,['hidden_resource csa',...windows[u.window]]),';confederate standardized marine replenishment',replenish(u)]);
}
for (const [level,norm] of [['military_academy',[1,.05,1]],['officers_academy',[1,.10,1]]]) additions.set(`professional_military/${level}`,[';confederate standardized command recruitment',row('csa_general_staff',...norm,['hidden_resource csa']),';confederate standardized command replenishment',row('csa_general_staff',.2,.02,.99)]);
const guns=[U('csa_12lb',2,'artillery','to1890',['usa']),U('csa_armstrong',2,'artillery','from1870',['usa']),U('csa_gatling',2,'artillery','from1870to1890',['usa']),U('csa_5lb',2,'artillery','from1890',['usa']),U('csa_maxim',2,'artillery','from1890',['usa']),U('csa_150mm',2,'artillery','from1890',['usa'])];
const min={csa_12lb:0,csa_armstrong:1,csa_gatling:1,csa_5lb:1,csa_maxim:2,csa_150mm:2};
for (const [level,i] of [['gunsmith',0],['cannon_maker',1],['cannon_foundry',2],['royal_arsenal',3]]) {
  const rows=[';confederate standardized artillery recruitment'];
  for(const u of guns) if(i>=min[u.type]) { const n=i===0?[1,.02,2]:i===1?[1,.06,2]:i===2?[1,.10,2]:[2,.20,2]; rows.push(row(u.type,...n,['hidden_resource csa',...windows[u.window]])); }
  rows.push(';confederate standardized artillery replenishment'); for(const u of guns) rows.push(replenish(u)); additions.set(`cannon/${level}`,rows);
}

function install(source,wanted){
  const lines=source.split('\n'); let building='';
  for(let i=0;i<lines.length;i++){
    const b=lines[i].match(/^building\s+(\S+)/); if(b) building=b[1];
    const l=lines[i].match(/^\s{8}(\S+)\s+(?:city|castle)\s+requires\b/); if(!l) continue;
    const key=`${building}/${l[1]}`, rows=wanted.get(key); if(!rows) continue;
    let c=i; while(c<lines.length&&lines[c].trim()!=='capability') c++;
    let o=c+1; while(o<lines.length&&lines[o].trim()!=='{') o++;
    let d=1,x=o+1; for(;x<lines.length;x++){for(const ch of lines[x]){if(ch==='{')d++;else if(ch==='}')d--;}if(!d)break;}
    if(d) throw new Error(`Unclosed capability ${key}`); lines.splice(x,0,...rows); i=x+rows.length; wanted.delete(key);
  }
  if(wanted.size) throw new Error(`Unresolved levels: ${[...wanted.keys()]}`); return lines.join('\n');
}
text=install(text,additions); if(!text.endsWith('\n')) text+='\n';
const tmp=canonical+'.csa.tmp'; fs.writeFileSync(tmp,text,'utf8'); fs.renameSync(tmp,canonical); fs.copyFileSync(canonical,mirror);
console.log('Confederate campaign recruitment rebuilt and mirrored.');
