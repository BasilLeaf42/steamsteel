const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const canonical = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const mirror = path.join(root, 'data/export_descr_unit.txt');
const backupDir = path.join(root, 'tools/backup_before_hide_forest_repair_20260926');
fs.mkdirSync(backupDir, { recursive: true });

for (const file of [canonical, mirror]) {
  const backup = path.join(backupDir, path.basename(path.dirname(file)) + '__' + path.basename(file));
  if (!fs.existsSync(backup)) fs.copyFileSync(file, backup);
}

const excluded = new Set([
  'boer_wagon',
  'camel_wagon',
  'indian_ele',
  'siam_ele_gunner',
  'Elephant Artillery',
]);

let text = fs.readFileSync(canonical, 'utf8');
let changed = 0;
text = text.replace(/^type\s+(.+?)\r?\n[\s\S]*?(?=^type\s+|(?![\s\S]))/gm, block => {
  const type = (block.match(/^type\s+(.+?)\s*$/m) || [])[1]?.trim();
  const category = (block.match(/^category\s+(\S+)/m) || [])[1];
  const attributes = (block.match(/^attributes\s+([^\r\n]+)/m) || [])[1];
  if (!type || !['infantry', 'cavalry'].includes(category) || !attributes || excluded.has(type)) return block;
  if (/\bhide_(?:forest|improved_forest|anywhere)\b/.test(attributes)) return block;
  changed++;
  return block.replace(/^attributes\s+([^\r\n]+)/m, (_line, value) => `attributes       ${value.trim()}, hide_forest`);
});

if (changed !== 79) throw new Error(`Expected 79 standard concealment repairs, got ${changed}`);
fs.writeFileSync(canonical, text);
fs.copyFileSync(canonical, mirror);
console.log(`Added hide_forest to ${changed} ordinary infantry/cavalry records; retained five wagon/elephant exceptions.`);
