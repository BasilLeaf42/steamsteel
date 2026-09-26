const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const authoritative = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const mirror = path.join(root, 'data/export_descr_unit.txt');

const swordUnits = new Set([
  'us_militia',
  'peru_early_inf',
  'pru_sturmtruppen_high',
  'pru_ww1_inf',
  'skif_inf1',
  'georgian_inf',
  'afghan_gunner',
  'qing_xiang_huai_mid',
  'otto_inf_az',
]);

const axeUnits = new Set([
  'rus_conscript_de',
  'bra_foot',
  'peru_foot_aztecs',
  'fra_blacks',
  'fra_blacks_turks',
  'merc_aceh_noble',
  'merc_aceh_reg',
  'polish_inf',
]);

function update(text) {
  let changed = 0;
  const output = text.replace(/(^type\s+(.+?)\r?\n)([\s\S]*?)(?=^type\s+|(?![\s\S]))/gm, (block, header, rawType) => {
    const type = rawType.trim();
    if (!swordUnits.has(type) && !axeUnits.has(type)) return block;

    const expectedWeapon = swordUnits.has(type) ? 'sword' : 'axe';
    if (!new RegExp(`^stat_sec\\s+.*?,\\s*${expectedWeapon},\\s*\\d`, 'm').test(block)) {
      throw new Error(`${type}: expected ${expectedWeapon} secondary not found`);
    }
    if (!/^stat_sec_attr\s+ap, short_pike\s*$/m.test(block)) {
      throw new Error(`${type}: expected inherited ap, short_pike row not found`);
    }

    changed += 1;
    const replacement = swordUnits.has(type) ? 'stat_sec_attr    no' : 'stat_sec_attr    ap';
    return block.replace(/^stat_sec_attr\s+ap, short_pike\s*$/m, replacement);
  });
  if (changed !== swordUnits.size + axeUnits.size) {
    throw new Error(`changed ${changed}; expected ${swordUnits.size + axeUnits.size}`);
  }
  return output;
}

const source = fs.readFileSync(authoritative, 'utf8');
const updated = update(source);
fs.writeFileSync(authoritative, updated, 'utf8');
fs.writeFileSync(mirror, updated, 'utf8');

console.log(JSON.stringify({
  corrected: swordUnits.size + axeUnits.size,
  swordsNowNoAttributes: swordUnits.size,
  axesRetainingOnlyArmourPiercing: axeUnits.size,
  mirrorsMatch: fs.readFileSync(authoritative, 'utf8') === fs.readFileSync(mirror, 'utf8'),
}, null, 2));
