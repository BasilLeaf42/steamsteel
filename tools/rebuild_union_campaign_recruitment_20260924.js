const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const canonical = path.join(root, 'data/tow_steamsteel/export_descr_buildings.txt');
const mirror = path.join(root, 'data/export_descr_buildings.txt');
let text = fs.readFileSync(canonical, 'utf8').replace(/\r/g, '');

// Remove only Union access from existing rows. Preserve every other faction on
// shared rows, then install one clean Union definition below.
const stripped = [];
for (const line of text.split('\n')) {
  if (!/^\s*recruit_pool\s+/.test(line) || !/\bfactions\s*\{[^}]*\bportugala\b/.test(line)) {
    stripped.push(line);
    continue;
  }
  const match = line.match(/\bfactions\s*\{([^}]*)\}/);
  if (!match) throw new Error(`Unable to parse Union faction list: ${line}`);
  const factions = match[1].split(',').map(x => x.trim()).filter(Boolean).filter(x => x !== 'portugala');
  if (!factions.length) continue;
  stripped.push(line.replace(match[0], `factions { ${factions.join(', ')}, }`).trimEnd());
}
text = stripped.join('\n');

const event = {
  y1865: 'event_counter military_reforms_1865 1',
  y1870: 'event_counter military_reforms_1870 1',
  y1875: 'event_counter military_reforms_1875 1',
  y1890: 'event_counter military_reforms_1890 1',
  y1895: 'event_counter military_reforms_1895 1',
  y1900: 'event_counter military_reforms_2 1',
};
const windows = {
  all: [],
  to1865: [`not ${event.y1865}`],
  from1865to1895: [event.y1865, `not ${event.y1895}`],
  from1895: [event.y1895],
  to1870: [`not ${event.y1870}`],
  from1870to1890: [event.y1870, `not ${event.y1890}`],
  to1875: [`not ${event.y1875}`],
  from1875to1890: [event.y1875, `not ${event.y1890}`],
  from1875to1900: [event.y1875, `not ${event.y1900}`],
  from1890: [event.y1890],
  from1900: [event.y1900],
  to1890: [`not ${event.y1890}`],
};

// The authoritative Steam & Steel map supplies one shared `europe` tag for
// Europeanized regions. Pair it with the national home tag rather than listing
// national tags whose overseas extents would leak recruitment into colonies.
const europeanized = ['usa', 'europe'];

const unit = (type, n, quality, window, geography) => ({type, n, quality, window, geography});
const barracksUnits = [
  unit('uni_state_volunteers_early', 3, 'militia', 'to1875', 'europeanized'),
  unit('uni_regulars_mid', 2, 'regular', 'from1875to1900', 'europeanized'),
  unit('uni_regulars_high', 2, 'regular', 'from1900', 'europeanized'),
  unit('uni_national_guard_mid', 2, 'militia', 'from1875to1890', 'europeanized'),
  unit('uni_national_guard_high', 3, 'militia', 'from1890', 'europeanized'),
  unit('uni_colored_troops_early', 1, 'militia', 'to1870', ['usa']),
  unit('uni_irish_brigade_early', 1, 'militia', 'to1870', ['usa']),
  unit('uni_zouaves_early', 1, 'militia', 'to1870', ['usa']),
  unit('uni_sharpshooters_early', 1, 'regular', 'to1870', ['usa']),
  unit('uni_dragoons_early', 1, 'regular', 'to1875', ['usa']),
  unit('uni_dragoons_mid', 1, 'regular', 'from1875to1900', ['usa']),
  unit('uni_dragoons_high', 1, 'regular', 'from1900', ['usa']),
  unit('uni_volunteer_cavalry_early', 1, 'militia', 'to1870', ['usa']),
  unit('uni_indian_scouts', 1, 'militia', 'to1890', ['amerindian']),
  unit('uni_indian_scout_cavalry', 1, 'militia', 'to1890', ['amerindian']),
];

const barracksLevels = [
  ['militia_drill_square', 0], ['militia_barracks', 1], ['army_barracks', 2], ['royal_armoury', 3]
];
const tuples = {
  1: [[1,.01,1],[1,.03,1],[1,.06,1],[1,.10,1]],
  2: [[1,.02,1],[1,.06,1],[2,.12,2],[2,.20,2]],
  3: [[1,.03,1],[1,.09,1],[2,.18,2],[3,.30,3]],
  4: [[1,.04,1],[1,.12,1],[3,.24,3],[4,.40,4]],
  5: [[1,.05,2],[2,.15,2],[3,.30,3],[5,.50,5]],
};

function req(parts) { return `requires factions { portugala, }${parts.length ? ' and ' + parts.join(' and ') : ''}`; }
function row(type, initial, rate, max, parts) {
  const fmt = n => Number.isInteger(n) ? String(n) : String(n).replace(/^0\./, '.');
  return `\trecruit_pool "${type}"  ${fmt(initial)}   ${fmt(rate)}   ${fmt(max)}  0  ${req(parts)}`;
}
function normalRows(u, levelIndex) {
  if (u.quality === 'regular' && levelIndex === 0) return [];
  const [initial, rate, max] = tuples[u.n][levelIndex];
  const geos = u.geography === 'europeanized' ? europeanized : u.geography;
  return geos.map(g => row(u.type, initial, rate, max, [`hidden_resource ${g}`, ...windows[u.window]]));
}
function replenishRow(u) {
  return row(u.type, +(u.n * .2).toFixed(2), +(u.n * .02).toFixed(2), .99, windows[u.window]);
}

const additions = new Map();
for (const [level, index] of barracksLevels) {
  const rows = [';union standardized normal recruitment'];
  for (const u of barracksUnits) rows.push(...normalRows(u, index));
  rows.push(';union standardized replenishment');
  for (const u of barracksUnits) rows.push(replenishRow(u));
  additions.set(`barracks/${level}`, rows);
}

const marines = [
  unit('uni_marines_early', 1, 'regular', 'to1865', ['usa']),
  unit('uni_marines_mid', 1, 'regular', 'from1865to1895', ['usa']),
  unit('uni_marines_high', 1, 'regular', 'from1895', ['usa']),
];
for (const [level, index] of [['port',0],['shipwright',1],['dockyard',2],['naval_drydock',3]]) {
  const rows = [';union standardized marine recruitment'];
  for (const u of marines) {
    const [initial, rate, max] = tuples[1][index];
    rows.push(row(u.type, initial, rate, max, [`hidden_resource usa`, ...windows[u.window]]));
  }
  rows.push(';union standardized marine replenishment');
  for (const u of marines) rows.push(replenishRow(u));
  additions.set(`port/${level}`, rows);
}

for (const [level, normal] of [['military_academy',[1,.05,1]],['officers_academy',[1,.10,1]]]) {
  additions.set(`professional_military/${level}`, [
    ';union standardized command recruitment',
    row('uni_general_staff', ...normal, ['hidden_resource usa']),
    ';union standardized command replenishment',
    row('uni_general_staff', .2, .02, .99, []),
  ]);
}

const artillery = [
  unit('usa_12lb', 2, 'artillery', 'to1890', ['usa']),
  unit('usa_armstrong', 2, 'artillery', 'all', ['usa']),
  unit('usa_gatling', 2, 'artillery', 'from1870to1890', ['usa']),
  unit('usa_5lb', 2, 'artillery', 'from1890', ['usa']),
  unit('usa_maxim', 2, 'artillery', 'from1890', ['usa']),
  unit('usa_pompom', 2, 'artillery', 'from1890', ['usa']),
  unit('usa_150mm', 2, 'artillery', 'from1890', ['usa']),
];
const artilleryMinTier = {usa_12lb:0, usa_armstrong:1, usa_gatling:1, usa_5lb:1, usa_maxim:2, usa_pompom:2, usa_150mm:2};
for (const [level, index] of [['gunsmith',0],['cannon_maker',1],['cannon_foundry',2],['royal_arsenal',3]]) {
  const rows = [';union standardized artillery recruitment'];
  for (const u of artillery) {
    if (index < artilleryMinTier[u.type]) continue;
    const normal = index === 0 ? [1,.02,2] : index === 1 ? [1,.06,2] : index === 2 ? [1,.10,2] : [2,.20,2];
    rows.push(row(u.type, ...normal, ['hidden_resource usa', ...windows[u.window]]));
  }
  rows.push(';union standardized artillery replenishment');
  for (const u of artillery) rows.push(replenishRow(u));
  additions.set(`cannon/${level}`, rows);
}

function insertInCapabilities(source, wanted) {
  const lines = source.split('\n');
  let building = '';
  for (let i = 0; i < lines.length; i++) {
    const bm = lines[i].match(/^building\s+(\S+)/);
    if (bm) building = bm[1];
    const lm = lines[i].match(/^\s{8}(\S+)\s+(?:city|castle)\s+requires\b/);
    if (!lm) continue;
    const key = `${building}/${lm[1]}`;
    const rows = wanted.get(key);
    if (!rows) continue;
    let cap = i;
    while (cap < lines.length && lines[cap].trim() !== 'capability') cap++;
    if (cap >= lines.length) throw new Error(`No capability block for ${key}`);
    let open = cap + 1;
    while (open < lines.length && lines[open].trim() !== '{') open++;
    if (open >= lines.length) throw new Error(`No capability opening brace for ${key}`);
    let depth = 1, close = open + 1;
    for (; close < lines.length; close++) {
      for (const c of lines[close]) { if (c === '{') depth++; else if (c === '}') depth--; }
      if (depth === 0) break;
    }
    if (depth !== 0) throw new Error(`No capability closing brace for ${key}`);
    lines.splice(close, 0, ...rows);
    i = close + rows.length;
    wanted.delete(key);
  }
  if (wanted.size) throw new Error(`Unresolved building levels: ${[...wanted.keys()].join(', ')}`);
  return lines.join('\n');
}

text = insertInCapabilities(text, additions);
text = text.split('\n').map(line =>
  /^\s*recruit_pool\s+"usa_(?:12lb|150mm|5lb|armstrong|gatling|maxim|pompom)"/.test(line) && /factions\s*\{\s*denmark,?\s*\}/.test(line)
    ? line.trimEnd()
    : line
).join('\n');
if (!text.endsWith('\n')) text += '\n';

const temp = canonical + '.union.tmp';
fs.writeFileSync(temp, text, 'utf8');
fs.renameSync(temp, canonical);
fs.copyFileSync(canonical, mirror);
console.log('Union campaign recruitment rebuilt and mirrored.');
