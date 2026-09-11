const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const canonical = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const runtime = path.join(root, 'data/export_descr_unit.txt');

const british = [
  'uk_foot_early', 'uk_foot_mid',
  'uk_guard_early', 'uk_guard_mid',
  'uk_light_early', 'uk_light_mid',
  'uk_highlanders_early', 'uk_highlanders_mid',
  'uk_marines_early', 'uk_marines_mid',
  'uk_indian_foot_early', 'uk_indian_foot_mid',
  'uk_imperial_foot_early', 'uk_imperial_foot_mid',
];

const spanish = [
  'spa_inf_early', 'spa_inf_mid',
  'spa_caz_early', 'spa_caz_mid',
  'spa_milicia_nacional_early', 'spa_milicia_nacional_mid',
  'spa_col_inf_early', 'spa_col_inf_mid',
  'austro_sailor_spain_early', 'austro_sailor_spain_mid',
];

const french = [
  'fra_fusiliers_early', 'fra_fusiliers_mid',
  'fra_garde_mobile_early', 'fra_garde_nationale_mid',
  'fra_zouaves_early', 'fra_zouaves_mid',
  'fra_chasseurs_early', 'fra_chasseurs_mid',
  'fra_guard_grenadiers_early', 'fra_guard_grenadiers_mid',
  'fra_legion_early', 'fra_legion_mid',
  'fra_marins_early', 'fra_marins_mid',
  'fra_senegalais_early', 'fra_senegalais_mid',
];

const danish = [
  'dan_fod_early', 'dan_fod_mid',
  'dan_guard_early', 'dan_guard_mid',
  'dan_light_early', 'dan_light_mid',
  'dan_marines_early', 'dan_marines_mid',
];

const dutch = [
  'net_line_early', 'net_line_mid',
  'net_grenadiers_early', 'net_grenadiers_mid',
  'net_jagers_early', 'net_jagers_mid',
  'net_mariniers_early', 'net_mariniers_mid',
  'net_schutterij_early', 'net_schutterij_mid',
  'net_knil_early', 'net_knil_mid',
];

const prussian = [
  'pru_fusiliere_early', 'pru_fusiliere_mid',
  'pru_pioniere_early', 'pru_pioniere_mid',
  'pru_gardegrenadiere_early', 'pru_gardegrenadiere_mid',
  'pru_jaeger_early', 'pru_jaeger_mid',
  'pru_seesoldaten_early', 'pru_seesoldaten_mid',
  'pru_wuerttemberg_mid', 'pru_bavarian_fusiliere_mid',
  'pru_bavarian_landwehr_mid', 'pru_hannover_mid',
];

function replaceBlock(edu, type, bearer) {
  const typeLine = new RegExp(`^type\\s+${type}$`, 'm');
  const match = typeLine.exec(edu);
  if (!match) throw new Error(`Missing EDU type ${type}`);
  const next = /^type\s+/gm;
  next.lastIndex = match.index + match[0].length;
  const nextMatch = next.exec(edu);
  const end = nextMatch ? nextMatch.index : edu.length;
  let block = edu.slice(match.index, end);
  block = block.replace(new RegExp(`^officer\\s+${bearer}\\s*\\n`, 'gm'), '');
  const officer = /^officer\s+[^\n]+$/m.exec(block);
  if (!officer) throw new Error(`Missing primary officer in ${type}`);
  block = block.slice(0, officer.index + officer[0].length) + `\nofficer          ${bearer}` + block.slice(officer.index + officer[0].length);
  return edu.slice(0, match.index) + block + edu.slice(end);
}

let edu = fs.readFileSync(canonical, 'utf8').replace(/\r\n/g, '\n');
for (const type of british) edu = replaceBlock(edu, type, 'BRIT_FootA_Bearer1');
for (const type of spanish) edu = replaceBlock(edu, type, 'russia_qi');
for (const type of french) edu = replaceBlock(edu, type, 'francejunqshou');
for (const type of danish) edu = replaceBlock(edu, type, 'francejunqshou');
for (const type of dutch) edu = replaceBlock(edu, type, 'francejunqshou');
for (const type of prussian) edu = replaceBlock(edu, type, 'russia_qi');

const types = [...edu.matchAll(/^type\s+(.+)$/gm)].map(match => match[1].trim());
const dictionaries = [...edu.matchAll(/^dictionary\s+(\S+)/gm)].map(match => match[1]);
const duplicates = items => items.filter((item, index) => items.indexOf(item) !== index);
if (duplicates(types).length) throw new Error('Duplicate EDU types after bearer update');
if (duplicates(dictionaries).length) throw new Error('Duplicate EDU dictionaries after bearer update');

const output = edu.replace(/\n/g, '\r\n');
fs.writeFileSync(canonical, output);
fs.writeFileSync(runtime, output);
console.log(`Applied verified early/mid bearers to ${british.length + spanish.length + french.length + danish.length + dutch.length + prussian.length} balanced-faction infantry records.`);
