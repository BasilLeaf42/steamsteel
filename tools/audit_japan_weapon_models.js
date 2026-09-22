const fs = require('fs');

const edu = fs.readFileSync('data/tow_steamsteel/export_descr_unit.txt', 'utf8').replace(/\r/g, '');
const db = fs.readFileSync('data/unit_models/battle_models.modeldb', 'utf8').replace(/\r/g, '');
const blocks = edu.split(/(?=^type\s+)/m).filter(b => /(?:^ownership|^era [012]).*\bsaxons\b/m.test(b));
const entries = new Map();
const starts = [...db.matchAll(/^(\d+) ([^\n]+)\s*\n1 \d+\s*\n\d+ unit_models\//gm)];
for (let i = 0; i < starts.length; i++) {
  const name = starts[i][2].trim();
  if (Number(starts[i][1]) !== name.length) continue;
  entries.set(name, db.slice(starts[i].index, starts[i + 1]?.index ?? db.length));
}

for (const b of blocks) {
  const type = b.match(/^type\s+(.+)$/m)?.[1].trim();
  const soldier = b.match(/^soldier\s+([^,]+),\s*(\d+)/m);
  const pri = b.match(/^stat_pri\s+(.+)$/m)?.[1];
  if (!soldier || !pri || !/bullet/.test(pri)) continue;
  const model = soldier[1].trim();
  const entry = entries.get(model) || '';
  const mesh = entry.match(/unit_models\/[^\s]+\.mesh/i)?.[0] || 'MISSING';
  let groups = 'MISSING';
  if (mesh !== 'MISSING' && fs.existsSync('data/' + mesh)) {
    const raw = fs.readFileSync('data/' + mesh).toString('latin1');
    const words = [...raw.matchAll(/[A-Za-z][A-Za-z0-9_.-]{3,}/g)].map(m => m[0]);
    groups = words.filter((w, i) => /^(?:primary|secondary)active\d+$/.test(w) || (i && /^(?:primary|secondary)active\d+$/.test(words[i - 1]))).join('|') || 'NONE';
  }
  const anims = [...entry.matchAll(/^\d+ (MTW2_[^\n]+)$/gm)].map(m => m[1].trim()).join('|') || 'MISSING';
  const attrs = b.match(/^attributes\s+(.+)$/m)?.[1] || '';
  console.log([type, soldier[2], model, pri.split(',')[2]?.trim(), /gunpowder_unit/.test(attrs) ? 'muzzle' : 'nonmuzzle', mesh, groups, anims].join('\t'));
}
