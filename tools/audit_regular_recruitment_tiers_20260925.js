const fs = require('fs');

const eduText = fs.readFileSync('data/tow_steamsteel/export_descr_unit.txt', 'utf8').replace(/\r/g, '');
const edbText = fs.readFileSync('data/tow_steamsteel/export_descr_buildings.txt', 'utf8').replace(/\r/g, '');

const units = new Map();
for (const block of eduText.split(/\n(?=type\s+)/)) {
  const type = block.match(/^type\s+(.+)$/m)?.[1].trim();
  if (!type) continue;
  const category = block.match(/^category\s+(\S+)/m)?.[1] || '';
  const recruitmentTime = +(block.match(/^stat_cost\s+(\d+)/m)?.[1] || 0);
  const attributes = block.match(/^attributes\s+(.+)$/m)?.[1] || '';
  units.set(type, {category, recruitmentTime, attributes});
}

const rows = [];
let building = '', level = '';
for (const [index, line] of edbText.split('\n').entries()) {
  let m;
  if ((m = line.match(/^building\s+(\S+)/))) building = m[1];
  if ((m = line.match(/^\s{8}(\S+)\s+(?:city|castle)\s+requires\b/))) level = m[1];
  m = line.match(/^\s*recruit_pool\s+"([^"]+)"\s+(\S+)\s+(\S+)\s+(\S+).*?factions\s*\{([^}]*)\}(.*)$/);
  if (!m) continue;
  const geo = [...line.matchAll(/(?<!not\s)hidden_resource\s+(\w+)/g)].map(x => x[1]);
  const window = [...line.matchAll(/(not\s+)?event_counter\s+(military_reforms_\w+)\s+1/g)].map(x => `${x[1] ? 'not ' : ''}${x[2]}`).join('|');
  for (const faction of m[5].split(',').map(x => x.trim()).filter(Boolean)) rows.push({line:index+1, building, level, unit:m[1], initial:+m[2], max:+m[4], faction, geo, window});
}

const normal = rows.filter(r => r.building === 'barracks' && r.max >= 1);
const regular = u => {
  const d = units.get(u);
  return d && !/\bgeneral_unit\b/.test(d.attributes) && ((d.category === 'infantry' && d.recruitmentTime === 3) || (d.category === 'cavalry' && d.recruitmentTime === 4));
};
const guardName = u => /guard|garde|grenadier|grenadiere|lifeguard|hassa|palace|royal|imperial_guard/i.test(u);
const key = r => [r.faction,r.unit,r.geo.join(','),r.window].join('|');
const tier2 = new Set(normal.filter(r => r.level === 'militia_barracks').map(key));
const missingTier2 = normal.filter(r => ['army_barracks','royal_armoury'].includes(r.level) && regular(r.unit) && !guardName(r.unit) && !tier2.has(key(r)));
const uniqueMissing = [...new Map(missingTier2.map(r => [key(r),r])).values()];
const tier1Regular = normal.filter(r => r.level === 'militia_drill_square' && regular(r.unit) && !guardName(r.unit));

const regularCavalry = [...new Set(normal.filter(r => units.get(r.unit)?.category === 'cavalry' && units.get(r.unit)?.recruitmentTime === 4 && !/\bgeneral_unit\b/.test(units.get(r.unit)?.attributes || '')).map(r => `${r.faction}|${r.unit}`))].sort();
const cavalryGeography = regularCavalry.map(k => {
  const [faction,unit] = k.split('|');
  const geos = [...new Set(normal.filter(r => r.faction === faction && r.unit === unit).map(r => r.geo.join(',')))].sort();
  return {faction,unit,geos};
});

console.log(JSON.stringify({regularUnitTypes:[...units].filter(([u]) => regular(u) && !guardName(u)).length, missingTier2:uniqueMissing, tier1Regular, regularCavalry:cavalryGeography}, null, 2));
