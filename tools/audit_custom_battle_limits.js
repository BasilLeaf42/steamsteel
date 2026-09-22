const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const edu = fs.readFileSync(path.join(root, 'data/tow_steamsteel/export_descr_unit.txt'), 'utf8').replace(/\r/g, '');
const factions = {
  Union:'portugala', Confederates:'milan', Mexico:'scotland', Peru:'denmark', Brazil:'poland', Argentina:'aztecs',
  Britain:'england', France:'france', Prussia:'hre', Spain:'spain', Netherlands:'portugal', Denmark:'sicily',
  'Sweden–Norway':'normans', Greece:'mongols', Italy:'venice', Russia:'russia', 'Austria–Hungary':'hungary',
  Morocco:'moors', Boers:'teu', Zulu:'lith', Ottoman:'turks', Oman:'golden', Qajar:'egypt', Afghanistan:'timurids',
  Turkestan:'cuman', 'Indian Princely States':'bulga', Siam:'cru', Qing:'byzantium', Ethiopia:'papal_states', Meiji:'saxons'
};
const starts = [...edu.matchAll(/^type\s+(\S+)/gm)];
const units = starts.map((m, i) => {
  const block = edu.slice(m.index, i + 1 < starts.length ? starts[i + 1].index : edu.length);
  const field = key => (block.match(new RegExp(`^${key}\\s+(.+)$`, 'm')) || [,''])[1].trim();
  const cost = field('stat_cost').split(',').map(x => x.trim());
  const eras = {};
  for (const match of block.matchAll(/^era ([012])\s+(.+)$/gm)) eras[match[1]] = match[2].split(',').map(x => x.trim());
  return {
    type:m[1], dictionary:field('dictionary').replace(/\s*;.*/, ''), category:field('category'), clazz:field('class'),
    ownership:field('ownership').split(',').map(x => x.trim()), limit:+cost[6] || 0, eras, block
  };
});

const report = [];
for (const [name, code] of Object.entries(factions)) {
  const row = {faction:name, code, eras:[]};
  for (const era of ['0','1','2']) {
    const available = units.filter(u => u.ownership.includes(code) && (u.eras[era] || []).includes(code));
    const field = available.filter(u => !['siege','ship'].includes(u.category));
    const artillery = field.filter(u => u.category === 'siege').reduce((n,u)=>n+u.limit,0);
    const combat = field.filter(u => u.category !== 'siege');
    row.eras.push({era:+era, types:combat.length, total:combat.reduce((n,u)=>n+u.limit,0), core:combat.filter(u=>!u.type.startsWith('merc_')).reduce((n,u)=>n+u.limit,0), mercenary:combat.filter(u=>u.type.startsWith('merc_')).reduce((n,u)=>n+u.limit,0), artillery,
      multi:combat.filter(u=>u.limit>1).map(u=>`${u.type}:${u.limit}`)});
  }
  report.push(row);
}
console.log('Faction\tEra0 types/slots\tEra1 types/slots\tEra2 types/slots\tLimits above 1');
for (const r of report) console.log(`${r.faction}\t${r.eras.map(x=>`${x.types}/${x.total} (${x.core}+${x.mercenary})`).join('\t')}\t${r.eras.flatMap(x=>x.multi).filter((x,i,a)=>a.indexOf(x)===i).join(', ') || '-'}`);
fs.writeFileSync(path.join(__dirname, 'custom_battle_limit_audit.json'), JSON.stringify(report, null, 2) + '\n');
