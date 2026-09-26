const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const eduPath = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const edbPath = path.join(root, 'data/tow_steamsteel/export_descr_buildings.txt');
const mirrorPath = path.join(root, 'data/export_descr_buildings.txt');

const edu = new Map();
for (const block of fs.readFileSync(eduPath, 'utf8').replace(/\r/g, '').split(/\n(?=type\s+)/)) {
  const type = block.match(/^type\s+(.+)$/m)?.[1].trim();
  if (!type) continue;
  edu.set(type, {
    category: block.match(/^category\s+(\S+)/m)?.[1] || '',
    time: +(block.match(/^stat_cost\s+(\d+)/m)?.[1] || 0),
    attributes: block.match(/^attributes\s+(.+)$/m)?.[1] || '',
  });
}

const isGuard = unit => /guard|garde|grenadier|grenadiere|lifeguard|hassa|palace|royal|imperial_guard/i.test(unit);
const isRegular = unit => {
  const d = edu.get(unit);
  if (!d || /\bgeneral_unit\b/.test(d.attributes) || isGuard(unit)) return false;
  return (d.category === 'infantry' && d.time === 3) || (d.category === 'cavalry' && d.time === 4);
};
const parse = line => {
  const m = line.match(/^\s*recruit_pool\s+"([^"]+)"\s+(\S+)\s+(\S+)\s+(\S+).*?factions\s*\{([^}]*)\}(.*)$/);
  if (!m) return null;
  const geo = [...line.matchAll(/(?<!not\s)hidden_resource\s+(\w+)/g)].map(x => x[1]).join(',');
  const window = [...line.matchAll(/(not\s+)?event_counter\s+(military_reforms_\w+)\s+1/g)].map(x => `${x[1] ? 'not ' : ''}${x[2]}`).join('|');
  const factions = m[5].split(',').map(x => x.trim()).filter(Boolean).sort().join(',');
  return {unit:m[1], max:+m[4], factions, geo, window};
};
const signature = r => [r.unit,r.factions,r.geo,r.window].join('|');

let text = fs.readFileSync(edbPath, 'utf8').replace(/\r/g, '');
const lines = text.split('\n');
let building = '', level = '';
const tier2 = new Set();
const higher = new Map();
let tier2Insert = -1;
for (let i = 0; i < lines.length; i++) {
  let m;
  if ((m = lines[i].match(/^building\s+(\S+)/))) building = m[1];
  if ((m = lines[i].match(/^\s{8}(\S+)\s+(?:city|castle)\s+requires\b/))) level = m[1];
  if (building === 'barracks' && level === 'militia_barracks' && tier2Insert < 0 && /^;us\s*$/.test(lines[i])) tier2Insert = i;
  if (building !== 'barracks') continue;
  const row = parse(lines[i]);
  if (!row || row.max < 1 || !isRegular(row.unit)) continue;
  if (level === 'militia_barracks') tier2.add(signature(row));
  if (level === 'army_barracks' && !higher.has(signature(row))) higher.set(signature(row), lines[i]);
}
if (tier2Insert < 0) throw new Error('Could not locate militia_barracks insertion point');

const additions = [];
for (const [sig,line] of higher) {
  if (tier2.has(sig)) continue;
  additions.push(line.replace(/^(\s*recruit_pool\s+"[^"]+"\s+)\S+(\s+)\S+(\s+)\S+/, (_, a, b, c) => `${a}1${b}.03${c}1`));
}
additions.sort((a,b) => a.localeCompare(b));
if (additions.length) lines.splice(tier2Insert, 0, '; regular non-guard formations available from barracks tier 2', ...additions, '');

text = lines.join('\n');
if (!text.endsWith('\n')) text += '\n';
fs.writeFileSync(edbPath, text);
fs.copyFileSync(edbPath, mirrorPath);
console.log(JSON.stringify({addedTier2Rows:additions.length, units:additions.map(x => parse(x)?.unit)}, null, 2));
