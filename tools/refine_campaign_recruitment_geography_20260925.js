const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const canonicalEdb = path.join(root, 'data/tow_steamsteel/export_descr_buildings.txt');
const runtimeEdb = path.join(root, 'data/export_descr_buildings.txt');
const canonicalRegions = path.join(root, 'data/world/maps/map_steamsteel/descr_regions.txt');
const runtimeRegions = path.join(root, 'data/world/maps/base/descr_regions.txt');
const backupDir = path.join(root, 'tools/backup_before_detailed_recruitment_geography_20260925');
fs.mkdirSync(backupDir, { recursive: true });
for (const file of [canonicalEdb, runtimeEdb, canonicalRegions, runtimeRegions]) {
  const backup = path.join(backupDir, path.basename(path.dirname(file)) + '_' + path.basename(file));
  if (!fs.existsSync(backup)) fs.copyFileSync(file, backup);
}

const requiredTags = ['ethiopia', 'himalayan', 'settler', 'colonial', 'ezo', 'kyushu', 'kanto', 'chugoku'];
let edb = fs.readFileSync(canonicalEdb, 'utf8').replace(/\r/g, '');
edb = edb.replace(/^hidden_resources\s+(.+)$/m, (_, body) => {
  const tags = body.trim().split(/\s+/);
  const obsolete = tags.indexOf('korea');
  if (obsolete !== -1) tags.splice(obsolete, 1);
  const broadSouthAmerica = tags.indexOf('s_america');
  if (broadSouthAmerica !== -1) tags.splice(broadSouthAmerica, 1);
  const unusedMiddleEast = tags.indexOf('middle_east');
  if (unusedMiddleEast !== -1) tags.splice(unusedMiddleEast, 1);
  for (const tag of requiredTags) if (!tags.includes(tag)) tags.push(tag);
  if (tags.length > 64) throw new Error(`Hidden-resource declaration exceeds vanilla-safe limit: ${tags.length}`);
  return `hidden_resources ${tags.join(' ')}`;
});

function japanTags(unit) {
  if (/\b(?:Ezo|Hoppo|Hokuchin|Tondenhei)\b|Bodyguard Ezo/i.test(unit)) return ['ezo'];
  if (/\b(?:Satsuma|Saga)\b/i.test(unit)) return ['kyushu'];
  if (/\b(?:Kiheitai|Yamagunitai|Jinshotai)\b/i.test(unit)) return ['chugoku'];
  if (/\b(?:Shogitai|Shinsengumi|Denshutai)\b|Kaiso Shinsengumi|Ryukihei Shogun/i.test(unit)) return ['kanto'];
  return ['japan'];
}

function detailedTags(faction, unit) {
  if (faction === 'saxons') return japanTags(unit);
  if (faction === 'papal_states') return ['ethiopia'];
  // "europe" is a geographic European-core gate, not a synonym for Western-style.
  // Overseas Western-style powers remain restricted to their own national territory.
  if (faction === 'aztecs') return ['argentina'];
  if (faction === 'denmark') return ['peru'];
  if (faction === 'milan') return ['csa'];
  if (faction === 'poland') return ['brazil'];
  if (faction === 'scotland') return ['mexico'];
  if (faction === 'teu') return ['south_africa'];
  if (faction === 'portugala' && /indian_scout/i.test(unit)) return ['amerindian'];
  if (faction === 'portugala') return ['usa'];
  if (faction === 'france' && /senegalais/i.test(unit)) return ['sub_sahara'];
  if (faction === 'france' && /(?:spahis|zouaves)/i.test(unit)) return ['north_africa'];
  if (faction === 'france' && /indochinois/i.test(unit)) return ['indochina'];
  if (faction === 'france' && /fra_legion/i.test(unit)) return [];
  if (faction === 'france' && /fra_fusiliers/i.test(unit)) return ['france', 'settler'];
  if (faction === 'france' && /fra_chasseurs_cheval/i.test(unit)) return ['france', 'settler'];
  if (faction === 'england' && /gurkha/i.test(unit)) return ['himalayan'];
  if (faction === 'england' && /indian/i.test(unit)) return ['india'];
  if (faction === 'england' && /camel_corps/i.test(unit)) return ['arab'];
  if (faction === 'england' && /uk_imperial_foot/i.test(unit)) return ['settler'];
  if (faction === 'england' && /uk_foot_/i.test(unit)) return ['uk'];
  if (faction === 'england' && /uk_dragoon_/i.test(unit)) return ['uk'];
  if (faction === 'hre' && /kolonial|schutztruppe/i.test(unit)) return ['colonial'];
  if (faction === 'hre' && /pru_fusiliere/i.test(unit)) return ['prussia', 'settler'];
  if (faction === 'hre' && /pru_dragoner/i.test(unit)) return ['prussia', 'settler'];
  if (faction === 'hre' && /pru_jaeger/i.test(unit)) return ['prussia'];
  if (faction === 'spain' && /spa_col_/i.test(unit)) return ['colonial'];
  if (faction === 'spain' && /cuban/i.test(unit)) return ['cuba'];
  if (/^euro_hussars(?:_|$)/i.test(unit)) return ['europe'];
  if (faction === 'spain' && /spa_inf_/i.test(unit)) return ['spain', 'settler'];
  if (faction === 'spain' && /spa_cav_/i.test(unit)) return ['spain', 'settler'];
  if (faction === 'portugal' && /net_knil/i.test(unit)) return ['east_indies'];
  if (faction === 'portugal' && /net_line/i.test(unit)) return ['netherlands', 'settler'];
  if (faction === 'portugal' && /net_karabiniers/i.test(unit)) return ['netherlands', 'settler'];
  if (faction === 'sicily' && /dan_fod/i.test(unit)) return ['denmark', 'settler'];
  if (faction === 'sicily' && /dan_dragoon/i.test(unit)) return ['denmark', 'settler'];
  if (faction === 'mongols' && /gre_line/i.test(unit)) return ['greece', 'settler'];
  if (faction === 'mongols' && /gre_carbineers/i.test(unit)) return ['greece', 'settler'];
  if (faction === 'venice' && /ita_line/i.test(unit)) return ['italy', 'settler'];
  if (faction === 'venice' && /ita_carabinieri/i.test(unit)) return ['italy', 'settler'];
  if (faction === 'hungary' && /aus_bosniak/i.test(unit)) return ['albania'];
  if (faction === 'hungary' && /aus_honved/i.test(unit)) return ['hungary'];
  if (faction === 'hungary' && /aus_grenz/i.test(unit)) return ['hungary'];
  if (faction === 'hungary' && /aus_(?:landwehr|kaiserjaeger)/i.test(unit)) return ['austria'];
  if (faction === 'hungary' && /aus_line/i.test(unit)) return ['austria', 'hungary', 'settler'];
  if (faction === 'hungary' && /aus_dragoner/i.test(unit)) return ['austria', 'hungary', 'settler'];
  if (faction === 'normans' && /\bnor_line/i.test(unit)) return ['norway', 'settler'];
  if (faction === 'normans' && /\bswe_line/i.test(unit)) return ['sweden', 'settler'];
  if (faction === 'normans' && /\bswe_dragoons/i.test(unit)) return ['sweden', 'norway', 'settler'];
  if (faction === 'normans' && /\bnor_/i.test(unit)) return ['norway'];
  if (faction === 'normans' && /\bswe_(?:bevaring|jagare|guard)/i.test(unit)) return ['sweden'];
  if (faction === 'russia' && /rus_siberian/i.test(unit)) return ['siberia'];
  if (faction === 'russia' && /rus_pekhota/i.test(unit)) return ['russia', 'settler'];
  if (faction === 'russia' && /rus_draguny/i.test(unit)) return ['russia', 'settler'];
  if (faction === 'russia' && /georgian/i.test(unit)) return ['georgia'];
  if (faction === 'golden' && /zanzibar/i.test(unit)) return ['sub_sahara'];
  if (faction === 'golden' && /baluchi/i.test(unit)) return ['persia'];
  if (faction === 'byzantium' && /baqi/i.test(unit)) return ['manchuria'];
  if (faction === 'byzantium' && /eight_banner_cavalry/i.test(unit)) return ['manchuria', 'mongolia'];
  if (faction === 'byzantium' && /oirat/i.test(unit)) return ['mongolia'];
  if (faction === 'cuman' && /uyghur/i.test(unit)) return ['steppe'];
  if (faction === 'egypt' && /afghan/i.test(unit)) return ['afghanistan'];
  if (faction === 'bulga' && /bhutan/i.test(unit)) return ['himalayan'];
  return null;
}

const lines = edb.split('\n');
const output = [];
const emitted = new Set();
let changedRows = 0;
let currentBuilding = '';
let currentLevel = '';
for (const line of lines) {
  let context;
  if ((context = line.match(/^building\s+(\S+)/))) currentBuilding = context[1];
  if ((context = line.match(/^\s{8}(\S+)\s+(?:city|castle)\s+requires\b/))) currentLevel = context[1];
  const m = line.match(/^(\s*recruit_pool\s+"([^"]+)"\s+(\S+)\s+\S+\s+(\S+).*?requires\s+factions\s*\{\s*([^,}]+),?\s*\})(.*)$/);
  if (!m || +m[4] < 1) { output.push(line); continue; }
  const [, prefix, unit, , , factionRaw, tail] = m;
  const faction = factionRaw.trim();
  const tags = detailedTags(faction, unit);
  if (!tags) { output.push(line); continue; }
  if (tags.includes('colonial') && currentBuilding === 'barracks' && currentLevel === 'militia_drill_square') continue;
  const existing = tail.match(/(?<!not\s)hidden_resource\s+(\w+)/);
  if (!existing && !tags.length) { output.push(line); continue; }
  if (!existing) throw new Error(`Normal recruitment row lacks geography: ${line}`);
  const structural = `${prefix}${tail.replace(existing[0], 'hidden_resource <TAG>')}`;
  if (emitted.has(structural)) continue;
  emitted.add(structural);
  if (!tags.length) {
    output.push(`${prefix}${tail.replace(/\s+and\s+(?<!not\s)hidden_resource\s+\w+/, '')}`);
  } else {
    for (const tag of tags) output.push(`${prefix}${tail.replace(existing[0], `hidden_resource ${tag}`)}`);
  }
  if (tags.length !== 1 || existing[1] !== tags[0]) changedRows++;
}
edb = output.join('\n');
if (!edb.endsWith('\n')) edb += '\n';
const edbTemp = canonicalEdb + '.geography.tmp';
fs.writeFileSync(edbTemp, edb);
fs.renameSync(edbTemp, canonicalEdb);
fs.copyFileSync(canonicalEdb, runtimeEdb);

const regionTags = new Map([
  ['Hokkaido_Province', 'ezo'],
  ['Estonie_Province', 'kyushu'],
  ['Edo_Province', 'kanto'],
  ['Akita_Province', 'chugoku'],
  ['Dehli_Province', 'himalayan'],
  ['Bengal_Province', 'himalayan'],
]);
const settlerExcluded = new Set(['Papua_Province', 'Arctic_Province', 'Ruperts_land_Province', 'Alaska_Province']);
const settlerSouthAfrica = new Set(['Afrique_Sud_Province', 'Rhodesie_Province', 'Jerusalemb_Province']);
const settlerColonies = new Set(['Krasnodar_Province']); // French Algeria
let regions = fs.readFileSync(canonicalRegions, 'utf8').replace(/\r/g, '').split('\n');
for (let i = 0; i < regions.length; i++) {
  if (!/^[A-Za-z0-9_]+_Province\s*$/.test(regions[i])) continue;
  const tag = regionTags.get(regions[i].trim());
  const resourceIndex = i + 5;
  if (resourceIndex >= regions.length) continue;
  const values = regions[resourceIndex].split(',').map(x => x.trim()).filter(Boolean);
  if (tag && !values.includes(tag)) values.push(tag);
  const region = regions[i].trim();
  if (settlerExcluded.has(region)) {
    const existingSettler = values.indexOf('settler');
    if (existingSettler !== -1) values.splice(existingSettler, 1);
  }
  const settlerBase = values.some(x => ['usa','csa','canada','anzac','argentina','uruguay'].includes(x));
  if ((settlerBase && !settlerExcluded.has(region)) || settlerSouthAfrica.has(region) || settlerColonies.has(region)) {
    if (!values.includes('settler')) values.push('settler');
  }
  // Generic colonial formations can be raised outside Europe and settler societies,
  // provided their faction has built the required barracks tier there.
  if (!values.includes('europe') && !values.includes('settler') && !values.includes('colonial')) values.push('colonial');
  regions[resourceIndex] = '\t' + values.join(', ');
}
let regionText = regions.join('\n');
if (!regionText.endsWith('\n')) regionText += '\n';
const regionsTemp = canonicalRegions + '.geography.tmp';
fs.writeFileSync(regionsTemp, regionText);
fs.renameSync(regionsTemp, canonicalRegions);
fs.copyFileSync(canonicalRegions, runtimeRegions);

console.log(JSON.stringify({ hiddenResourceCount: edb.match(/^hidden_resources\s+(.+)$/m)[1].trim().split(/\s+/).length, changedRecruitmentGroups: changedRows, japanRegionalTags: Object.fromEntries(regionTags), backupDir }, null, 2));
