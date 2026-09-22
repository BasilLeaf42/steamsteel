const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const eduPath = path.join(root, 'data', 'tow_steamsteel', 'export_descr_unit.txt');
const edu = fs.readFileSync(eduPath, 'utf8').replace(/\r\n/g, '\n');
const blocks = edu.split(/(?=^type\s+)/m).filter((b) => /^type\s+/m.test(b));

function field(block, name) {
  const match = block.match(new RegExp(`^${name}\\s+(.+)$`, 'm'));
  return match ? match[1].trim() : '';
}

function typeOf(block) {
  return field(block, 'type');
}

function normalizedSignature(block) {
  return block
    .split('\n')
    .filter((line) => !/^(type|dictionary|ownership|era [012])\s+/.test(line))
    .map((line) => line.replace(/\s*;.*$/, '').trim().replace(/\s+/g, ' '))
    .filter(Boolean)
    .join('\n');
}

function combatSignature(block) {
  const names = [
    'category', 'class', 'voice_type', 'soldier', 'mount', 'mount_effect',
    'attributes', 'formation', 'stat_health', 'stat_pri', 'stat_pri_attr',
    'stat_sec', 'stat_sec_attr', 'stat_pri_armour', 'stat_sec_armour',
    'stat_heat', 'stat_ground', 'stat_mental', 'stat_charge_dist',
    'stat_fire_delay'
  ];
  return names.map((name) => `${name}=${field(block, name)}`).join('|');
}

const records = blocks.map((block) => ({
  type: typeOf(block),
  dictionary: field(block, 'dictionary').replace(/\s*;.*/, ''),
  soldier: field(block, 'soldier').split(',')[0].trim(),
  ownership: field(block, 'ownership'),
  eras: [0, 1, 2].filter((era) => field(block, `era ${era}`)).map((era) => `${era}:${field(block, `era ${era}`)}`).join(' '),
  normalized: normalizedSignature(block),
  combat: combatSignature(block),
}));

const candidate = (record) =>
  record.type.startsWith('merc_') ||
  /(^|,\s*)slave(\s*,|$)/.test(record.ownership);

function groupsBy(key) {
  const map = new Map();
  for (const record of records) {
    const value = record[key];
    if (!value) continue;
    if (!map.has(value)) map.set(value, []);
    map.get(value).push(record);
  }
  return [...map.values()].filter((group) => group.length > 1 && group.some(candidate));
}

function printGroup(label, groups) {
  console.log(`\n=== ${label} (${groups.length}) ===`);
  for (const group of groups) {
    console.log(group.map((r) => `${r.type} [${r.soldier}] owners={${r.ownership}} eras={${r.eras}}`).join('\n  == '));
  }
}

printGroup('Exact records except identity/custom-battle scope', groupsBy('normalized'));
printGroup('Same complete combat signature', groupsBy('combat'));

const bySoldier = new Map();
for (const record of records) {
  if (!record.soldier) continue;
  if (!bySoldier.has(record.soldier)) bySoldier.set(record.soldier, []);
  bySoldier.get(record.soldier).push(record);
}
printGroup('Same soldier/model entry', [...bySoldier.values()].filter((group) => group.length > 1 && group.some(candidate)));
