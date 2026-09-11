const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const eduPaths = [
  path.join(root, 'data/tow_steamsteel/export_descr_unit.txt'),
  path.join(root, 'data/export_descr_unit.txt'),
];
const modelPath = path.join(root, 'data/unit_models/battle_models.modeldb');
const mountedSprite = 'unit_sprites/tmp_cavalry_sprite.spr';
const engineering = /(?:sapeur|sapper|pionier|zappator|engineer|ingenier|michanik|genio)/i;
const standingSprite = /(?:Dummy_EN_Spearmen|Huscarls|Musketeers|Arquebusiers|Italian_MAA|FootC?|Spearmen|Warriors|Forlorn_Hope|Nubian|spear_militia|tmp_inf|Feudal_Knights)/i;

function unitBlocks(text) {
  return text.replace(/\r\n/g, '\n').split(/(?=^type\s+)/m);
}

function normalizeStakes(text) {
  let added = 0;
  let removed = 0;
  const out = unitBlocks(text).map(block => {
    if (!/^type\s+/m.test(block) || !/^attributes\s+/m.test(block)) return block;
    const category = (block.match(/^category\s+(\S+)/m) || [])[1];
    const eras = [...block.matchAll(/^era\s+([012])\b/gm)].map(m => Number(m[1]));
    const lateOnly = eras.length > 0 && eras.every(value => value === 2);
    const isEngineer = engineering.test(block.match(/^(?:type|dictionary)\s+.*$/gm)?.join(' ') || '');
    const isCarbine = category === 'cavalry' && /^stat_pri\s+.*_carbine_bullet_/m.test(block);
    const shouldHave = isEngineer || (lateOnly && (category === 'infantry' || isCarbine));
    return block.replace(/^attributes\s+(.+)$/m, (line, body) => {
      const tokens = body.split(',').map(value => value.trim()).filter(Boolean);
      const had = tokens.includes('stakes');
      const filtered = tokens.filter(value => value !== 'stakes');
      if (shouldHave) filtered.push('stakes');
      if (had && !shouldHave) removed++;
      if (!had && shouldHave) added++;
      return `attributes       ${filtered.join(', ')}`;
    });
  }).join('');
  return { text: out, added, removed };
}

let canonicalResult;
for (const file of eduPaths) {
  const result = normalizeStakes(fs.readFileSync(file, 'utf8'));
  fs.writeFileSync(file, result.text.replace(/\n/g, '\r\n'), 'utf8');
  if (!canonicalResult) canonicalResult = result;
}
if (!fs.readFileSync(eduPaths[0]).equals(fs.readFileSync(eduPaths[1]))) {
  throw new Error('EDU mirrors differ after stakes normalization');
}

const edu = fs.readFileSync(eduPaths[0], 'utf8').replace(/\r\n/g, '\n');
const modelCategories = new Map();
for (const block of unitBlocks(edu)) {
  const category = (block.match(/^category\s+(\S+)/m) || [])[1];
  const soldier = (block.match(/^soldier\s+([^,\s]+)/m) || [])[1];
  if (!category || !soldier) continue;
  if (!modelCategories.has(soldier)) modelCategories.set(soldier, new Set());
  modelCategories.get(soldier).add(category);
}

let model = fs.readFileSync(modelPath, 'utf8').replace(/\r\n/g, '\n');
const lines = model.split('\n');
const corrected = [];
const skippedShared = [];
for (let i = 0; i < lines.length; i++) {
  const head = lines[i].match(/^(\d+) (\S+)\s*$/);
  if (!head || Number(head[1]) !== head[2].length) continue;
  const name = head[2];
  const categories = modelCategories.get(name);
  if (!categories || !categories.has('cavalry')) continue;
  let end = i;
  while (end < lines.length && !/^16 -0\.090000004 /.test(lines[end])) end++;
  if (end >= lines.length) throw new Error(`Unterminated modeldb entry: ${name}`);
  if (categories.size > 1) {
    if (lines.slice(i, end + 1).some(line => /unit_sprites\//.test(line) && standingSprite.test(line))) skippedShared.push(name);
    i = end;
    continue;
  }
  let changed = false;
  for (let j = i; j <= end; j++) {
    const sprite = lines[j].match(/^\d+ (unit_sprites\/\S+\.spr)\s*$/);
    if (!sprite || !standingSprite.test(sprite[1])) continue;
    lines[j] = `${mountedSprite.length} ${mountedSprite} `;
    changed = true;
  }
  if (changed) corrected.push(name);
  i = end;
}
model = lines.join('\n');
fs.writeFileSync(modelPath, model.replace(/\n/g, '\r\n'), 'utf8');

console.log(JSON.stringify({
  stakesAdded: canonicalResult.added,
  stakesRemoved: canonicalResult.removed,
  cavalryModelsCorrected: corrected.length,
  corrected,
  sharedModelsSkipped: skippedShared,
}, null, 2));
