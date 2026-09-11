const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const canonical = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const runtime = path.join(root, 'data/export_descr_unit.txt');
const types = [
  'uk_general',
  'civil_guard',
  'fra_general_staff', 'fra_hussar',
  'pru_general_staff', 'otto_sipahi',
  'net_general_staff', 'balk_cav_nl',
  'dan_general',
];

let edu = fs.readFileSync(canonical, 'utf8').replace(/\r\n/g, '\n');
for (const type of types) {
  const unit = new RegExp(`(^type\\s+${type}\\s*$[\\s\\S]*?^soldier\\s+[^,]+,\\s*4(?:,|\\s*$)[\\s\\S]*?^stat_cost\\s+)[^\\n]+`, 'm');
  if (!unit.test(edu)) throw new Error(`Missing four-man general-and-staff unit: ${type}`);
  edu = edu.replace(unit, '$13, 200, 67, 100, 100, 200, 1, 67');
}
fs.writeFileSync(canonical, edu, 'utf8');
fs.copyFileSync(canonical, runtime);
console.log(`Set ${types.length} four-man general-and-staff records to cost 200.`);
