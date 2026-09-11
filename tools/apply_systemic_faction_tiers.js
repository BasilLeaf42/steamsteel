const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const canonical = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const runtime = path.join(root, 'data/export_descr_unit.txt');

const regularA = [
  'uk_hussars_early', 'uk_hussars_mid', 'uk_hussars_high',
  'uk_dragoon_early', 'uk_dragoon_mid', 'uk_dragoon_high',
  'uk_camel_corps_high',
  'uk_foot_early', 'uk_foot_mid', 'uk_foot_high',
  'uk_light_early', 'uk_light_mid', 'uk_light_high',
  'uk_imperial_foot_early', 'uk_imperial_foot_mid', 'uk_imperial_foot_high',
];

const eliteA = [
  'uk_guard_early', 'uk_guard_mid', 'uk_guard_high',
  'uk_marines_early', 'uk_marines_mid', 'uk_marines_high',
  'uk_general', 'uk_indian_lancers',
];

const highlanders = ['uk_highlanders_early', 'uk_highlanders_mid', 'uk_highlanders_high'];
const gurkhas = ['uk_gurkhas_high'];
const indianFoot = ['uk_indian_foot_early', 'uk_indian_foot_mid', 'uk_indian_foot_high'];

const costs = {
  uk_hussars_early:1400, uk_hussars_mid:1400, uk_hussars_high:1400,
  uk_dragoon_early:1400, uk_dragoon_mid:1400, uk_dragoon_high:1400,
  uk_camel_corps_high:2200, uk_general:200, uk_indian_lancers:1600,
  uk_foot_early:1400, uk_foot_mid:1700, uk_foot_high:2000,
  uk_guard_early:1600, uk_guard_mid:1900, uk_guard_high:2200,
  uk_light_early:1400, uk_light_mid:1700, uk_light_high:2000,
  uk_highlanders_early:1400, uk_highlanders_mid:1700, uk_highlanders_high:2000,
  uk_marines_early:1600, uk_marines_mid:1900, uk_marines_high:2200,
  uk_indian_foot_early:1200, uk_indian_foot_mid:1500, uk_indian_foot_high:1800,
  uk_imperial_foot_early:1400, uk_imperial_foot_mid:1700, uk_imperial_foot_high:2000,
  uk_gurkhas_high:2200,
};

function statCost(total, oldRow) {
  const fields = oldRow.split(',').map(s => s.trim());
  const limit = Number(fields[6]);
  const third = Math.round(total / 3);
  return `3, ${total}, ${third}, 100, 100, ${total}, ${limit}, ${third}`;
}

function setPair(block, field, first, second) {
  const re = new RegExp(`^(${field}\\s+)\\d+,\\s*\\d+,`, 'm');
  if (!re.test(block)) throw new Error(`Missing ${field}`);
  return block.replace(re, `$1${first}, ${second},`);
}

function setArmourDefence(block, defence) {
  const re = /^(stat_pri_armour\s+\d+,\s*)\d+(,.*)$/m;
  if (!re.test(block)) throw new Error('Missing stat_pri_armour');
  return block.replace(re, `$1${defence}$2`);
}

function setMental(block, morale, discipline) {
  const re = /^(stat_mental\s+)\d+,\s*\w+,\s*(\w+)$/m;
  if (!re.test(block)) throw new Error('Missing stat_mental');
  return block.replace(re, `$1${morale}, ${discipline}, $2`);
}

function setCost(block, total) {
  const re = /^(stat_cost\s+)(.+)$/m;
  const match = block.match(re);
  if (!match) throw new Error('Missing stat_cost');
  return block.replace(re, `$1${statCost(total, match[2])}`);
}

function updateBlock(type, block) {
  if (!Object.hasOwn(costs, type)) return block;

  if (regularA.includes(type)) {
    block = setPair(block, 'stat_sec', 6, 4);
  } else if (eliteA.includes(type)) {
    block = setPair(block, 'stat_sec', 8, 5);
  } else if (highlanders.includes(type)) {
    block = setPair(block, 'stat_sec', 8, 5);
  } else if (gurkhas.includes(type)) {
    block = setPair(block, 'stat_sec', 10, 5);
  } else if (indianFoot.includes(type)) {
    block = setPair(block, 'stat_sec', 5, 3);
    block = setArmourDefence(block, 3);
    block = setMental(block, 4, 'normal');
    block = block
      .replace('rifled_musket_bullet_a', 'rifled_musket_bullet_b')
      .replace('rifle_bullet_a', 'rifle_bullet_b')
      .replace('magazine_rifle_bullet_a', 'magazine_rifle_bullet_b');
  }

  return setCost(block, costs[type]);
}

let edu = fs.readFileSync(canonical, 'utf8').replace(/\r\n/g, '\n');
const seen = new Set();
const starts = [...edu.matchAll(/^type\s+(\S+)/gm)];
const pieces = [edu.slice(0, starts[0].index)];
for (let i = 0; i < starts.length; i++) {
  const type = starts[i][1];
  const end = i + 1 < starts.length ? starts[i + 1].index : edu.length;
  let block = edu.slice(starts[i].index, end);
  if (Object.hasOwn(costs, type)) seen.add(type);
  pieces.push(updateBlock(type, block));
}
edu = pieces.join('');

const missing = Object.keys(costs).filter(type => !seen.has(type));
if (missing.length) throw new Error(`Missing British records: ${missing.join(', ')}`);

fs.writeFileSync(canonical, edu, 'utf8');
fs.copyFileSync(canonical, runtime);

console.log(`Applied systemic faction tiers to ${seen.size} British records.`);
