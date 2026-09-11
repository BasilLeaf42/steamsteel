const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const eduPaths = [
  path.join(root, 'data/tow_steamsteel/export_descr_unit.txt'),
  path.join(root, 'data/export_descr_unit.txt'),
];
const locPath = path.join(root, 'data/text/export_units.txt');

const units = {
  gre_line_early: ['Pezikó', 'Early', 'Greek Minié Rifle-Musket'],
  gre_line_mid: ['Pezikó', 'Mid', 'Mylonas M1872'],
  gre_line_high: ['Pezikó', 'Late', 'Greek Gras M1874/M80'],
  gre_ethnofylaki_early: ['Ethnofylakí', 'Early', 'Nafplion M1833 Percussion Musket'],
  gre_efedroi_mid: ['Éfedroi', 'Mid', 'Chassepot M1866'],
  gre_efedroi_high: ['Éfedroi', 'Late', 'Mylonas M1872'],
  gre_evzones_early: ['Evzones', 'Early', 'Greek Minié Rifle-Musket'],
  gre_evzones_mid: ['Evzones', 'Mid', 'Mylonas M1872'],
  gre_evzones_high: ['Evzones', 'Late', 'Greek Gras M1874/M80'],
  gre_marines_early: ['Naftikó Ágima', 'Early', 'Greek Minié Rifle-Musket'],
  gre_marines_mid: ['Naftikó Ágima', 'Mid', 'Chassepot M1866'],
  gre_marines_high: ['Naftikó Ágima', 'Late', 'Greek Gras M1874/M80'],
  gre_lancers: ['Ipparchía Lonchistón', '', 'lance and sabre'],
  gre_royal_escort: ['Ágima', '', 'Lefaucheux M1854 revolver and sabre'],
  gre_carbineers_mid: ['Ipparchía Akrovolistón', 'Mid', 'Mylonas M1872 carbine and sabre'],
  gre_carbineers_high: ['Ipparchía Akrovolistón', 'Late', 'Steyr–Gras M1874 carbine and sabre'],
  gre_general_staff: ['Stratigós kai Epiteleío', '', 'Lefaucheux M1854 revolver and sabre'],
  gre_sappers_high: ['Michanikó', 'Late', 'Incendiary equipment'],
};

for (const eduPath of eduPaths) {
  let edu = fs.readFileSync(eduPath, 'utf8');
  for (const [type, [name, period, weapon]] of Object.entries(units)) {
    const detail = period ? `${name} (${period}; ${weapon})` : `${name} (${weapon})`;
    const re = new RegExp(`^(dictionary\\s+${type}\\s*;).*$`, 'm');
    if (!re.test(edu)) throw new Error(`Missing EDU dictionary row: ${type}`);
    edu = edu.replace(re, `$1 ${detail}`);
  }
  fs.writeFileSync(eduPath, edu);
}

const aliases = {
  fra_hussar_mongols: ['Stratigós kai Epiteleío', '', 'Lefaucheux M1854 revolver and sabre'],
  evzones_inf: ['Evzones', 'Mid', 'Mylonas M1872'],
  greek_roy: ['Michanikó', 'Late', 'Incendiary equipment'],
  greek_guard_cav: ['Ipparchía Akrovolistón', 'Mid', 'Mylonas M1872 carbine and sabre'],
  swed_inf: ['Pezikó', 'Late', 'Greek Gras M1874/M80'],
  rom_cav: ['Ipparchía Akrovolistón', 'Late', 'Steyr–Gras M1874 carbine and sabre'],
  greek_early_inf: ['Pezikó', 'Early', 'Greek Minié Rifle-Musket'],
};

for (const eduPath of eduPaths) {
  let edu = fs.readFileSync(eduPath, 'utf8');
  for (const [type, [name, period, weapon]] of Object.entries(aliases)) {
    const detail = period ? `${name} (${period}; ${weapon})` : `${name} (${weapon})`;
    const re = new RegExp(`^(dictionary\\s+${type}\\s*;).*$`, 'm');
    if (!re.test(edu)) throw new Error(`Missing legacy EDU dictionary row: ${type}`);
    edu = edu.replace(re, `$1 ${detail}`);
  }
  fs.writeFileSync(eduPath, edu);
}

const raw = fs.readFileSync(locPath);
if (raw[0] !== 0xff || raw[1] !== 0xfe) throw new Error('Localization is not UTF-16LE with BOM');
let loc = raw.slice(2).toString('utf16le');
for (const [key, [name, period, weapon]] of Object.entries({...units, ...aliases})) {
  const visible = period ? `${name} (${period})` : name;
  const replacements = {
    [key]: visible,
    [`${key}_descr`]: `${visible} serve in the Hellenic forces under their historical formation title.`,
    [`${key}_descr_short`]: `${visible} (${weapon})`,
  };
  for (const [locKey, value] of Object.entries(replacements)) {
    const re = new RegExp(`^\\{${locKey}\\}.*$`, 'm');
    if (!re.test(loc)) throw new Error(`Missing localization key: ${locKey}`);
    loc = loc.replace(re, `{${locKey}}${value}`);
  }
}
fs.writeFileSync(locPath, Buffer.concat([Buffer.from([0xff, 0xfe]), Buffer.from(loc, 'utf16le')]));

if (!fs.readFileSync(eduPaths[0]).equals(fs.readFileSync(eduPaths[1]))) {
  throw new Error('Canonical and runtime EDU files differ');
}
console.log(`Renamed ${Object.keys(units).length} Greek units and ${Object.keys(aliases).length} compatibility records.`);
