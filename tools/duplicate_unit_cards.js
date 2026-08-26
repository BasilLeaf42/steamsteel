const fs = require('fs');
const path = require('path');

const eduPath = 'data/tow_steamsteel/export_descr_unit.txt';
const unitRoot = 'data/ui/units';
const infoRoot = 'data/ui/unit_info';
const factions = new Set([
  'portugala', 'milan', 'scotland', 'denmark', 'poland', 'aztecs', 'england',
  'france', 'hre', 'spain', 'portugal', 'sicily', 'normans', 'mongols',
  'venice', 'russia', 'hungary', 'moors', 'teu', 'lith', 'turks', 'golden',
  'egypt', 'timurids', 'cuman', 'bulga', 'cru', 'byzantium', 'papal_states', 'saxons'
]);
const suffix = /^(.*)_(portugala|milan|scotland|denmark|poland|aztecs|england|france|hre|spain|portugal|sicily|normans|mongols|venice|russia|hungary|moors|teu|lith|turks|golden|egypt|timurids|cuman|bulga|cru|byzantium|papal_states|saxons)$/;
const source = fs.readFileSync(eduPath, 'utf8');
const clones = [];
for (const block of source.split(/(?=^type\s+)/m)) {
  const type = /^type\s+(.+?)(?:\s*;.*)?\s*$/m.exec(block)?.[1].trim();
  const owners = (/^ownership\s+(.+)$/m.exec(block)?.[1] ?? '')
    .split(',').map(value => value.trim()).filter(value => factions.has(value));
  const match = type?.match(suffix);
  if (match && owners.length === 1 && owners[0] === match[2]) clones.push({ type, base: match[1], faction: match[2] });
}
if (clones.length !== 58) throw new Error(`Expected 58 duplicated EDU types; found ${clones.length}.`);

function allFiles(root) {
  return fs.readdirSync(root, { recursive: true })
    .filter(file => typeof file === 'string' && file.toLowerCase().endsWith('.tga'))
    .map(file => path.join(root, file));
}
const unitFiles = allFiles(unitRoot);
const infoFiles = allFiles(infoRoot);
function prefer(files, names, faction) {
  const lowerNames = names.map(name => name.toLowerCase());
  return files.find(file => path.dirname(file).toLowerCase().endsWith(path.sep + faction.toLowerCase()) && lowerNames.includes(path.basename(file).toLowerCase()))
    ?? files.find(file => lowerNames.includes(path.basename(file).toLowerCase()));
}

let copiedUnits = 0;
let copiedInfos = 0;
let infoFallbacks = 0;
for (const clone of clones) {
  const unitSource = prefer(unitFiles, [`#${clone.base}.tga`], clone.faction);
  if (!unitSource) throw new Error(`No unit card found for ${clone.base}.`);
  const unitDestinationDir = path.join(unitRoot, clone.faction);
  const unitDestination = path.join(unitDestinationDir, `#${clone.type}.tga`);
  if (fs.existsSync(unitDestination)) throw new Error(`Unit card already exists: ${unitDestination}`);
  fs.mkdirSync(unitDestinationDir, { recursive: true });
  fs.copyFileSync(unitSource, unitDestination);
  copiedUnits++;

  const infoSource = prefer(infoFiles, [`${clone.base}_info.tga`, `${clone.base}.tga`], clone.faction) ?? unitSource;
  const infoDestinationDir = path.join(infoRoot, clone.faction);
  const infoDestination = path.join(infoDestinationDir, `${clone.type}_info.tga`);
  if (fs.existsSync(infoDestination)) throw new Error(`Unit info card already exists: ${infoDestination}`);
  fs.mkdirSync(infoDestinationDir, { recursive: true });
  fs.copyFileSync(infoSource, infoDestination);
  copiedInfos++;
  if (infoSource === unitSource) infoFallbacks++;
}
console.log(`Created ${copiedUnits} unit cards and ${copiedInfos} info cards (${infoFallbacks} unit-card fallbacks).`);
