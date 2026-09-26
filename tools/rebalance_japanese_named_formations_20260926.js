const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const files = {
  edu: path.join(root, 'data/tow_steamsteel/export_descr_unit.txt'),
  eduMirror: path.join(root, 'data/export_descr_unit.txt'),
  edb: path.join(root, 'data/tow_steamsteel/export_descr_buildings.txt'),
  edbMirror: path.join(root, 'data/export_descr_buildings.txt'),
  loc: path.join(root, 'data/text/export_units.txt'),
};
const backup = path.join(root, 'tools/backup_before_japanese_named_rebalance_20260926');
fs.mkdirSync(backup, { recursive: true });
for (const file of Object.values(files)) {
  const target = path.join(backup, file.replace(root + path.sep, '').replace(/[\\/]/g, '__'));
  if (!fs.existsSync(target)) fs.copyFileSync(file, target);
}

const specs = {
  'Japan Kachi': { pri: [9, 7], mental: '6, disciplined, highly_trained', cost: 1100 },
  'Japan Shinsengumi': { sec: [9, 6], mental: '6, disciplined, highly_trained', cost: 1500, removeAttrs: ['frighten_foot', 'frighten_mounted'] },
  'Japan Shogitai': { pri: [8, 6], mental: '6, normal, highly_trained', cost: 1100 },
  'Japan Kenyotai': { pri: [8, 6], mental: '6, normal, highly_trained', cost: 1000 },
  'Japan Jinshotai': { sec: [8, 6], mental: '6, normal, highly_trained', cost: 1400 },
  'Japan Ishin Shishi': { pri: [8, 5], mental: '5, normal, trained', cost: 900 },
  'Japan Ronin': { pri: [8, 5], mental: '5, normal, trained', cost: 900 },
  'Japan Suzakutai': { sec: [9, 6], mental: '6, normal, highly_trained', cost: 1400 },
  'Japan Gakuheitai': { sec: [8, 6], mental: '6, normal, highly_trained', cost: 1600 },
  'Japan Satsuma Hoheitai': { sec: [8, 6], mental: '6, normal, highly_trained', cost: 1400 },
  'Japan Raijintai': { projectile: 'rifled_musket_bullet_b', sec: [7, 5], mental: '5, normal, trained', cost: 1400 },
  'Japan Karasugumi': { sec: [6, 6], mental: '5, normal, trained', cost: 1400 },
  'Japan Nagaoka Hoheitai': { sec: [6, 6], mental: '5, normal, trained', cost: 1400 },
  'Japan Yamagunitai': { projectile: 'rifled_musket_bullet_b', sec: [6, 3], mental: '6, normal, highly_trained', cost: 1400, removeAttrs: ['command'] },
  'Japan Denshutai': { sec: [6, 4], mental: '6, normal, highly_trained', cost: 1700 },
  'Japan Sampeitai': { sec: [7, 5], mental: '4, low, trained', cost: 1000 },
  'Japan Hokokutai': { sec: [7, 5], mental: '4, low, trained', cost: 1200, removeAttrs: ['command'] },
  'Japan Kiheitai': { sec: [7, 5], mental: '5, normal, trained', cost: 1300 },
  'Japan Kijutai': { sec: [7, 5], mental: '5, normal, trained', cost: 1600 },
  'Japan Teppotai': { sec: [7, 5], mental: '4, low, trained', cost: 1000 },
  'Japan Matsushiro Hoheitai': { sec: [7, 5], mental: '4, low, trained', cost: 1200 },
  'Japan Kaga Hoheitai': { sec: [7, 5], mental: '4, low, trained', cost: 1200 },
  'Japan Yukantai': { sec: [7, 5], mental: '4, low, trained', cost: 1200 },
  'Japan Saga Hoheitai': { sec: [7, 5], mental: '4, low, trained', cost: 1200 },
  'Japan Byakkotai': { sec: [5, 4], mental: '3, low, trained', cost: 800 },
};

function replaceWeaponPair(block, row, pair) {
  const re = new RegExp(`^${row}\\s+(\\d+),\\s*(\\d+),(.*)$`, 'm');
  if (!re.test(block)) throw new Error(`Missing ${row}`);
  return block.replace(re, `${row.padEnd(17)}${pair[0]}, ${pair[1]},$3`);
}

let edu = fs.readFileSync(files.edu, 'utf8');
for (const [type, spec] of Object.entries(specs)) {
  const escaped = type.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const re = new RegExp(`^type\\s+${escaped}\\r?\\n[\\s\\S]*?(?=^type\\s+|(?![\\s\\S]))`, 'm');
  const found = edu.match(re);
  if (!found) throw new Error(`Missing Japanese unit: ${type}`);
  let block = found[0];
  if (spec.pri) block = replaceWeaponPair(block, 'stat_pri', spec.pri);
  if (spec.sec) block = replaceWeaponPair(block, 'stat_sec', spec.sec);
  if (spec.projectile) {
    if (!/^stat_pri\s+\d+,\s*\d+,\s*[^,]+,/m.test(block)) throw new Error(`Missing projectile row: ${type}`);
    block = block.replace(/^(stat_pri\s+\d+,\s*\d+,\s*)[^,]+,/m, `$1${spec.projectile},`);
  }
  if (spec.mental) block = block.replace(/^stat_mental\s+[^\r\n]+/m, `stat_mental      ${spec.mental}`);
  if (spec.cost) {
    const upkeep = Math.round(spec.cost / 3);
    block = block.replace(/^stat_cost\s+(\d+),\s*\d+,\s*\d+,\s*(\d+),\s*(\d+),\s*\d+,\s*(\d+),\s*\d+/m,
      (_m, turns, weapon, armour, limit) => `stat_cost        ${turns}, ${spec.cost}, ${upkeep}, ${weapon}, ${armour}, ${spec.cost}, ${limit}, ${upkeep}`);
  }
  if (spec.removeAttrs) {
    block = block.replace(/^attributes\s+([^\r\n]+)/m, (_m, attrs) => {
      const kept = attrs.split(',').map(x => x.trim()).filter(x => !spec.removeAttrs.includes(x));
      return `attributes       ${kept.join(', ')}`;
    });
  }
  edu = edu.replace(found[0], block);
}
fs.writeFileSync(files.edu, edu);
fs.copyFileSync(files.edu, files.eduMirror);

let edb = fs.readFileSync(files.edb, 'utf8');
const lowTierGaku = /^\s*recruit_pool "Japan Gakuheitai"\s+1\s+\.03\s+1\s+0\s+requires factions \{ saxons, \} and hidden_resource japan and not event_counter military_reforms_1890 1\r?\n/m;
if (!lowTierGaku.test(edb)) throw new Error('Could not locate militia-barracks Gakuheitai recruitment');
edb = edb.replace(lowTierGaku, '');
fs.writeFileSync(files.edb, edb);
fs.copyFileSync(files.edb, files.edbMirror);

let loc = fs.readFileSync(files.loc, 'utf8');
loc = loc.replace('{Japan_Bodyguard_Retainers}Daimyō to Umamawari', '{Japan_Bodyguard_Retainers}Japanese General and Umamawari');
loc = loc.replace(/^\{Japan_Bodyguard_Retainers_descr_short\}.*$/m, '{Japan_Bodyguard_Retainers_descr_short}Japanese General and Umamawari (Revolver, Smith & Wesson No.2, Saber), mounted command retinue.');
fs.writeFileSync(files.loc, loc, 'utf8');

console.log(`Rebalanced ${Object.keys(specs).length} named Japanese formations and restricted Gakuheitai initial recruitment to army barracks or better.`);
