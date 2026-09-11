const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const modelPath = path.join(root, 'data/unit_models/battle_models.modeldb');
const canonicalEdu = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const runtimeEdu = path.join(root, 'data/export_descr_unit.txt');

function modelEntry(text, name) {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const head = new RegExp(`^${name.length} ${name}\\s*$`);
  const start = lines.findIndex(line => head.test(line));
  if (start < 0) throw new Error(`Missing modeldb entry: ${name}`);
  let end = start;
  while (end < lines.length && !/^16 -0\.090000004 /.test(lines[end])) end++;
  if (end === lines.length) throw new Error(`Unterminated modeldb entry: ${name}`);
  return lines.slice(start, end + 1).join('\n');
}

function useSkirmisherSet(entry) {
  const changed = entry.replace(
    /(?:20 MTW2_Fast_Arquebus_3|14 MTW2_Musket_SS|15 MTW2_Musket_SSK) 9 MTW2_Pike /,
    '15 MTW2_Musket_SSK 9 MTW2_Pike '
  );
  if (!/15 MTW2_Musket_SSK 9 MTW2_Pike /.test(changed)) {
    throw new Error('Compatible infantry primary animation row not found');
  }
  return changed;
}

function cloneModel(text, donor, name) {
  return useSkirmisherSet(modelEntry(text, donor).replace(
    new RegExp(`^${donor.length} ${donor}\\s*$`, 'm'),
    `${name.length} ${name} `
  ));
}

// A distinct soldier is required where an early or line-infantry record shares
// the same modeldb entry but must retain a different firing animation.
const splits = [
  ['uk_light_high', 'pith_troopers'],
  ['spa_caz_mid', 'aus_inf_sp'],
  ['spa_caz_high', 'spa_caz_mid'],
];

const skirmisherModels = [
  'uk_light_mid', 'uk_light_high',
  'spa_caz_mid', 'spa_caz_high', 'cuban_inf',
  'fra_chasseurs_mid', 'fra_chasseurs_high',
  'pru_jaeger_early', 'pru_jaeger_mid', 'pru_jaeger_high', 'pru_schutztruppe_high',
  'net_jagers_mid', 'net_jagers_high',
  'dan_light_mid',
];

let model = fs.readFileSync(modelPath, 'utf8').replace(/\r\n/g, '\n');
let added = 0;
for (const [name, donor] of splits) {
  if (!new RegExp(`^${name.length} ${name}\\s*$`, 'm').test(model)) {
    model = model.trimEnd() + '\n' + cloneModel(model, donor, name) + '\n';
    added++;
  }
}
if (added) {
  const header = model.match(/^(22 serialization::archive 3 0 0 0 0 )(\d+)( 0 0 )/);
  if (!header) throw new Error('Invalid modeldb header');
  model = model.replace(header[0], `${header[1]}${Number(header[2]) + added}${header[3]}`);
}
for (const name of skirmisherModels) {
  const current = modelEntry(model, name);
  model = model.replace(current, useSkirmisherSet(current));
}
fs.writeFileSync(modelPath, model.replace(/\n/g, '\r\n'), 'utf8');

let edu = fs.readFileSync(canonicalEdu, 'utf8').replace(/\r\n/g, '\n');
for (const [type] of splits) {
  const unit = new RegExp(`(^type\\s+${type}\\s*$[\\s\\S]*?^soldier\\s+)([^,]+)`, 'm');
  if (!unit.test(edu)) throw new Error(`Missing EDU unit: ${type}`);
  edu = edu.replace(unit, `$1${type}`);
}
fs.writeFileSync(canonicalEdu, edu, 'utf8');
fs.copyFileSync(canonicalEdu, runtimeEdu);

for (const name of skirmisherModels) {
  if (!/15 MTW2_Musket_SSK 9 MTW2_Pike /.test(modelEntry(model, name))) {
    throw new Error(`Skirmisher animation validation failed: ${name}`);
  }
}
console.log(`Applied MTW2_Musket_SSK to ${skirmisherModels.length} model entries; added ${added} split entries.`);
