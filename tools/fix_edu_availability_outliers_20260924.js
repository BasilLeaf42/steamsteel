const fs = require('fs');

const targets = new Map([
  ['mongol_hevcav', 1],
  ['merc_kok_royal_cav', 1],
  ['qing_green_banner_horse', 2],
  ['ind_150mm', 2],
  ['ind_gatling', 2],
  ['kok_gatling', 2],
  ['kok_150mm', 2],
  ['zul_maxim', 2],
  ['zul_12lb', 2],
  ['zul_5lb', 2],
  ['zul_gatling', 2],
  ['zul_armstrong', 2],
]);

const paths = [
  'data/tow_steamsteel/export_descr_unit.txt',
  'data/export_descr_unit.txt',
];

function rewrite(text) {
  const newline = text.includes('\r\n') ? '\r\n' : '\n';
  const lines = text.split(/\r?\n/);
  let type = null;
  const seen = new Set();
  let changed = 0;

  for (let i = 0; i < lines.length; i++) {
    let match = lines[i].match(/^type\s+(.+?)\s*$/);
    if (match) {
      type = match[1];
      continue;
    }
    if (!targets.has(type)) continue;
    match = lines[i].match(/^(stat_cost\s+)(.+)$/);
    if (!match) continue;
    const fields = match[2].split(',').map(value => value.trim());
    if (fields.length < 8) throw new Error(`Invalid stat_cost for ${type}`);
    const expected = String(targets.get(type));
    if (fields[6] !== expected) {
      fields[6] = expected;
      lines[i] = `${match[1]}${fields.join(', ')}`;
      changed++;
    }
    seen.add(type);
  }

  for (const typeName of targets.keys()) {
    if (!seen.has(typeName)) throw new Error(`Target not found: ${typeName}`);
  }
  return { text: lines.join(newline), changed };
}

let canonical = null;
for (const path of paths) {
  const result = rewrite(fs.readFileSync(path, 'utf8'));
  if (canonical !== null && result.text !== canonical) {
    throw new Error(`Canonical/runtime output mismatch: ${path}`);
  }
  canonical = result.text;
  fs.writeFileSync(path, result.text, 'utf8');
  process.stdout.write(`${path}: changed=${result.changed}\n`);
}
