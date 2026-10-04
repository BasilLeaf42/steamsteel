const fs = require('fs');

function readText(path, encoding = 'latin1') {
  return fs.readFileSync(path).toString(encoding);
}

function writeText(path, text, encoding = 'latin1') {
  fs.writeFileSync(path, Buffer.from(text, encoding));
}

// Medieval II accepts at most 64 hidden-resource declarations. These three
// broad South-American labels were never used by an EDB recruitment row.
for (const path of [
  'data/world/maps/map_steamsteel/descr_regions.txt',
  'data/world/maps/base/descr_regions.txt',
]) {
  let text = readText(path);
  for (const tag of ['paraguay', 'uruguay', 's_america', 'middle_east']) {
    text = text.replace(new RegExp(`(^\\s*)([^\\r\\n;]*)(?:^|,\\s*)${tag}(?=,|\\r?$)`, 'gmi'),
      (_m, indent, before) => `${indent}${before}`);
    text = text.replace(new RegExp(`(^\\s*)${tag},\\s*`, 'gmi'), '$1');
    text = text.replace(new RegExp(`,\\s*${tag}(?=,|\\r?$)`, 'gmi'), '');
  }
  writeText(path, text);
}

// Existing saves can still contain the now-retired Merchant Marine mercenary.
// Give its verified British visual to every possible owner so it remains
// visible instead of becoming a riderless/invisible legacy unit.
{
  const path = 'data/unit_models/battle_models.modeldb';
  let text = readText(path);
  const start = text.indexOf('16 ssk_uk_sailor_ss ');
  const end = text.indexOf('\r\n1 \r\n', start + 1);
  if (start < 0 || end < 0) throw new Error('Merchant Marine modeldb block not found');
  const oldBlock = text.slice(start, end);
  const factions = [
    'spain','moors','turks','egypt','cru','france','hre','normans','poland','hungary',
    'golden','scotland','teu','sicily','cuman','lith','mongols','byzantium','papal_states',
    'portugal','russia','venice','aztecs','slave','timurids','denmark','milan','bulga',
    'portugala','england','saxons'
  ];
  const visual = factions.map(f =>
    `${f.length} ${f} \r\n50 unit_models/_Units/eng/textures/eng_mar_1g.texture \r\n58 unit_models/_Units/attachments/textures/blank_norm.texture \r\n51 unit_sprites/milan_Dummy_EN_Spearmen_ug1_sprite.spr `
  ).join('\r\n');
  const attachment = factions.map(f =>
    `${f.length} ${f} \r\n58 unit_models/_Units/attachments/textures/whi_gbfrxx.texture \r\n58 unit_models/_Units/attachments/textures/blank_norm.texture 0 `
  ).join('\r\n');
  let block = oldBlock;
  if (!block.includes(`\r\n${factions.length} \r\n`)) {
    block = block.replace(/\r\n2 \r\n7 england [\s\S]*?51 unit_sprites\/milan_Dummy_EN_Spearmen_ug1_sprite\.spr \r\n5 slave [\s\S]*?51 unit_sprites\/milan_Dummy_EN_Spearmen_ug1_sprite\.spr /,
      `\r\n${factions.length} \r\n${visual}`);
    block = block.replace(/\r\n2 \r\n7 england [\s\S]*?58 unit_models\/_Units\/attachments\/textures\/blank_norm\.texture 0 \r\n5 slave [\s\S]*?58 unit_models\/_Units\/attachments\/textures\/blank_norm\.texture 0 /,
      `\r\n${factions.length} \r\n${attachment}`);
    if (block === oldBlock || !block.includes(`\r\n${factions.length} \r\n`)) {
      throw new Error('Merchant Marine modeldb mapping replacement failed');
    }
  }
  text = text.slice(0, start) + block + text.slice(end);
  writeText(path, text);
}

const men = [
  'Tewodros','Menelik','Yohannes','Tekle','Giyorgis','Makonnen','Alula','Mikael','Wolde',
  'Gebre','Mariam','Haile','Selassie','Gugsa','Wale','Mengesha','Asfaw','Darge','Balcha',
  'Habte','Abebe','Bekele','Kebede','Tesfaye','Fikre','Girma','Tadesse','Zewde','Kassa','Hailu'
];
const surnames = [
  'Hailu','Makonnen','Mariam','Giyorgis','Selassie','Wolde','Gebre','Mikael','Darge','Gugsa',
  'Mengesha','Asfaw','Balcha','Habte','Kassa','Abebe','Bekele','Kebede','Tesfaye','Tadesse'
];
const women = [
  'Taytu','Zewditu','Tiruwork','Desta','Romanework','Walatta','Mariam','Askale','Almaz',
  'Emebet','Hirut','Sahle','Senait','Woizero','Yeshimebet'
];
const block = [
  'faction: papal_states', '', '\tcharacters', ...men.map(n => `\t\t${n}`), '',
  '\tsurnames', ...surnames.map(n => `\t\t${n}`), '',
  '\twomen', ...women.map(n => `\t\t${n}`), '', ''
].join('\r\n');

for (const path of ['data/tow_steamsteel/descr_names.txt', 'data/descr_names.txt']) {
  let text = readText(path);
  const rx = /^faction: papal_states\r?\n[\s\S]*?(?=^faction:)/m;
  if (!rx.test(text)) throw new Error(`Ethiopian name block not found in ${path}`);
  text = text.replace(rx, block);
  writeText(path, text);
}

for (const path of [
  'data/world/maps/campaign/camp_steamsteel/descr_strat.txt',
  'data/world/maps/campaign/imperial_campaign/descr_strat.txt',
]) {
  let text = readText(path);
  text = text.replace('character\tUmakai Tadazumi, named character, male, leader,',
    'character\tTewodros Hailu, named character, male, leader,');
  writeText(path, text);
}

// Add text lookup keys without disturbing the UTF-16 localization format.
{
  const path = 'data/text/names.txt';
  const bytes = fs.readFileSync(path);
  let text = bytes.toString('utf16le');
  const additions = [...new Set([...men, ...surnames, ...women])]
    .filter(n => !text.includes(`{${n}}`))
    .map(n => `{${n}}${n}`);
  if (additions.length) text += `\r\n${additions.join('\r\n')}\r\n`;
  fs.writeFileSync(path, Buffer.from(text, 'utf16le'));
}

for (const cache of ['data/text/names.txt.strings.bin']) {
  if (fs.existsSync(cache)) fs.unlinkSync(cache);
}

console.log('Repaired hidden-resource ceiling, legacy Merchant Marine visuals, and Ethiopian names.');
