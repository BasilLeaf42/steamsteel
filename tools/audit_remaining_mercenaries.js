const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const edu = fs.readFileSync(path.join(root, 'data/tow_steamsteel/export_descr_unit.txt'), 'utf8').replace(/\r/g, '');
const locBuffer = fs.readFileSync(path.join(root, 'data/text/export_units.txt'));
const loc = locBuffer.subarray(locBuffer[0] === 0xff && locBuffer[1] === 0xfe ? 2 : 0).toString(locBuffer[0] === 0xff && locBuffer[1] === 0xfe ? 'utf16le' : 'utf8').replace(/\r/g, '');
const model = fs.readFileSync(path.join(root, 'data/unit_models/battle_models.modeldb'), 'utf8').replace(/\r/g, '');

const completed = new Set([
  'merc_aceh_marines', 'merc_aceh_noble', 'merc_aceh_reg', 'merc_aceh_gold',
  'merc_aceh_warband', 'merc_aceh_inf', 'merc_tib_temple_guard',
  'merc_tib_noble_cav', 'merc_tib_inf', 'merc_viet_early_inf', 'merc_zulu_rifles',
]);
const blocks = edu.match(/^type\s+[\s\S]*?(?=^type\s+|(?![\s\S]))/gm) || [];
const field = (block, name) => block.match(new RegExp(`^${name}\\s+(.+)$`, 'm'))?.[1].trim() || '';
const locValue = (key) => loc.match(new RegExp(`^\\{${key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\}([^\\n]*)$`, 'm'))?.[1].trim() || '';
const splitNums = (value) => value.split(',').map((part) => part.trim());
const results = [];

for (const block of blocks) {
  const type = field(block, 'type');
  if (!/^merc(?:_|\s)/.test(type) || completed.has(type)) continue;
  const category = field(block, 'category');
  const dictionary = field(block, 'dictionary').replace(/\s*;.*/, '');
  const soldierFields = splitNums(field(block, 'soldier'));
  const soldier = soldierFields[0];
  const count = Number(soldierFields[1]);
  const cost = splitNums(field(block, 'stat_cost'));
  const formation = field(block, 'formation');
  const attributes = field(block, 'attributes');
  const pri = splitNums(field(block, 'stat_pri'));
  const sec = splitNums(field(block, 'stat_sec'));
  const display = locValue(dictionary);
  const short = locValue(`${dictionary}_descr_short`);
  const issues = [];

  if (category === 'ship') {
    results.push({ type, display, category, issues: ['naval: outside land-unit balance'] });
    continue;
  }
  if (category === 'cavalry' && count !== 24) issues.push(`strength ${count}, expected 24 cavalry`);
  if (category === 'infantry' && pri[5] === 'missile' && /gunpowder/.test(pri[6] || '') && ![30, 40].includes(count)) issues.push(`strength ${count}, expected 30/40 firearm infantry`);
  if (category === 'infantry' && pri[2] === 'no' && ![80, 96].includes(count)) issues.push(`strength ${count}, expected 80/96 melee infantry`);
  if (category === 'cavalry' && formation !== '2, 2, 4, 4, 3, square') issues.push(`cavalry formation ${formation}`);
  if (field(block, 'stat_ground') !== '0, 0, 0, 0') issues.push(`terrain ${field(block, 'stat_ground')}`);
  if (field(block, 'stat_fire_delay') !== '0') issues.push(`fire delay ${field(block, 'stat_fire_delay') || 'missing'}`);
  if (cost.length !== 8) issues.push(`malformed cost (${cost.join(', ')})`);
  else {
    if (cost[3] !== '100' || cost[4] !== '100') issues.push(`upgrade costs ${cost[3]}/${cost[4]}`);
    if (cost[2] !== cost[7]) issues.push(`upkeep/penalty ${cost[2]}/${cost[7]}`);
  }
  for (const token of ['hide_improved_forest', 'hide_anywhere', 'hide_long_grass', 'very_hardy', 'hardy', 'affected_by_rain']) {
    if (new RegExp(`(^|,\\s*)${token}(\\s*,|$)`).test(attributes)) issues.push(`special attribute ${token}`);
  }
  if (!/(^|,\s*)mercenary_unit(\s*,|$)/.test(attributes)) issues.push('missing mercenary_unit attribute');
  if (/\([^)]*(Musket|Rifle|Carbine|Bow|Spear|Sword|Shield|Kaskara|Klewang|Arquebus|Bayonet)/i.test(display)) issues.push('equipment embedded in visible name');
  if (!short) issues.push('missing short description');
  else { const base=display.replace(/ \((?:Early|Mid|Late)\)$/,''); if (!short.startsWith(base)) issues.push('short description not name-first'); }
  if (/unused|merc_[a-z_]+|Papua New Guinea Natives|Hardy .*warriors|Veteran .*renowned/i.test(short)) issues.push('placeholder/prose short description');
  if (/Musktet|Paraguayian|Auxililaries/i.test(display + ' ' + short)) issues.push('spelling error');
  const modelStart = model.search(new RegExp(`^${soldier.length} ${soldier}\\s*$`, 'm'));
  if (modelStart < 0) issues.push(`missing modeldb soldier ${soldier}`);
  else {
    const modelEnd = model.indexOf('16 -0.090000004', modelStart);
    const modelBlock = model.slice(modelStart, modelEnd < 0 ? modelStart + 5000 : modelEnd);
    const muzzle = /gunpowder_unit/.test(attributes);
    const skirmishFormation = formation === '1.4, 1.8, 2.8, 3.6, 3, square';
    if (category === 'infantry' && pri[5] === 'missile' && /gunpowder/.test(pri[6] || '')) {
      if (muzzle && !/20 MTW2_Fast_Arquebus_3/.test(modelBlock)) issues.push('muzzle-loader animation mismatch');
      if (!muzzle && skirmishFormation && !/15 MTW2_Musket_SSK/.test(modelBlock)) issues.push('skirmisher SSK animation mismatch');
      if (!muzzle && !skirmishFormation && !/14 MTW2_Musket_SS|20 MTW2_Fast_Arquebus_3/.test(modelBlock)) issues.push('breechloader animation mismatch');
    }
    if (category === 'cavalry' && !/unit_sprites\/(?:tmp_cavalry_sprite|.*(?:cav|horse|hoshuchi|lancer|hussar|dragoon).*)\.spr/i.test(modelBlock)) issues.push('distant LOD not visibly cavalry-labelled');
  }
  results.push({ type, display, category, issues });
}

const summary = {
  audited: results.filter((row) => row.category !== 'ship').length,
  ships: results.filter((row) => row.category === 'ship').length,
  clean: results.filter((row) => row.category !== 'ship' && row.issues.length === 0).length,
  withIssues: results.filter((row) => row.category !== 'ship' && row.issues.length > 0).length,
  issueCounts: {},
  units: results,
};
for (const row of results) for (const issue of row.issues) {
  const key = issue.replace(/\s+[-+]?\d+(?:[.,/]\d+)*(?:\/[-+]?\d+)?(?: cavalry| firearm infantry| melee infantry)?$/, '').replace(/ \(.+\)$/, '');
  summary.issueCounts[key] = (summary.issueCounts[key] || 0) + 1;
}
fs.writeFileSync(path.join(root, 'tools/remaining_mercenary_audit.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify({ audited: summary.audited, ships: summary.ships, clean: summary.clean, withIssues: summary.withIssues, issueCounts: summary.issueCounts }, null, 2));
for (const row of results.filter((item) => item.category !== 'ship')) console.log(`${row.type}: ${row.issues.join('; ') || 'clean'}`);
