const fs = require('fs');

const edb = fs.readFileSync('data/tow_steamsteel/export_descr_buildings.txt', 'utf8').replace(/\r/g, '');
const mirror = fs.readFileSync('data/export_descr_buildings.txt', 'utf8').replace(/\r/g, '');
const regionLines = fs.readFileSync('data/world/maps/map_steamsteel/descr_regions.txt', 'utf8').replace(/\r/g, '').split('\n');
const eduLines = fs.readFileSync('data/tow_steamsteel/export_descr_unit.txt', 'utf8').replace(/\r/g, '').split('\n');
const shipTypes = new Set();
const mercenaryTypes = new Set();
let eduType = '';
for (const line of eduLines) {
  const tm = line.match(/^type\s+(.+)$/); if (tm) eduType = tm[1].trim();
  if (/^category\s+ship\s*$/.test(line) && eduType) shipTypes.add(eduType);
  if (/^attributes\s+.*\bmercenary_unit\b/.test(line) && eduType) mercenaryTypes.add(eduType);
}

const regions = [];
for (let i = 0; i < regionLines.length; i++) {
  if (!/^[A-Za-z0-9_]+_Province\s*$/.test(regionLines[i])) continue;
  regions.push({name: regionLines[i].trim(), tags: regionLines[i + 5].split(',').map(x => x.trim()).filter(Boolean)});
}
const mapTags = new Set(regions.flatMap(r => r.tags));
const declaredHiddenResources = new Set((edb.match(/^hidden_resources\s+(.+)$/m)?.[1] || '').trim().split(/\s+/).filter(Boolean));
const tagRegions = new Map([...mapTags].map(t => [t, new Set(regions.filter(r => r.tags.includes(t)).map(r => r.name))]));

const rows = [];
let building = '', level = '';
for (const [index, line] of edb.split('\n').entries()) {
  let m;
  if ((m = line.match(/^building\s+(\S+)/))) building = m[1];
  if ((m = line.match(/^\s{8}(\S+)\s+(?:city|castle)\s+requires\b/))) level = m[1];
  if (!/^\s*recruit_pool/.test(line)) continue;
  const u = line.match(/recruit_pool\s+"([^"]+)"\s+(\S+)\s+(\S+)\s+(\S+)/);
  const fm = line.match(/factions\s*\{([^}]*)\}/);
  if (!u || !fm) continue;
  const geo = [...line.matchAll(/(?<!not\s)hidden_resource\s+(\w+)/g)].map(x => x[1]);
  const window = [...line.matchAll(/(not\s+)?event_counter\s+(military_reforms_\w+)\s+1/g)].map(x => `${x[1] ? 'not ' : ''}${x[2]}`).join('|');
  for (const faction of fm[1].split(',').map(x => x.trim()).filter(Boolean)) {
    rows.push({line: index + 1, building, level, unit: u[1], initial: +u[2], max: +u[4], faction, geo, window});
  }
}

const auditedBuildings = new Set(['barracks', 'professional_military', 'cannon', 'port']);
const land = rows.filter(r => auditedBuildings.has(r.building) && !shipTypes.has(r.unit));
const normal = land.filter(r => r.max >= 1);
const replenishment = land.filter(r => r.max < 1);
const issues = [];
const add = (kind, row, detail = '') => issues.push({kind, line: row.line, faction: row.faction, unit: row.unit, detail});
const tibetanCampaignUnits = new Set(['merc_tib_inf','merc_tib_noble_cav','mercs_tib_monks','tib_heavy_spear','tib_horse_archer','tib_militia','tib_roy_inf','tib_tribal_archer']);
const excludedCampaignSubfactions = new Set([
  'merc_port_inf_early','merc_port_inf_mid','merc_port_inf_high','merc_port_cav_early','merc_port_cav_mid','merc_port_cav_high',
  'merc_aceh_marines','merc_aceh_noble','merc_aceh_reg','merc_aceh_gold','merc_aceh_warband','merc_aceh_inf',
  'merc_tib_temple_guard','taipingguners','taiping_inf','taiping_light','taiping_w',
  'korean_archers','Korean Byeolgigun','Korean Gimagungsu','Korean Musketeers','Korean Pikemen','korean_rifles_mercs','korean_cav_mercs',
  'mahdist_inf','mahdist_camel_cav','mahdist_cav','Ethiopia Sudanese Musketeers','Ethiopia Sudanese Warriors',
  'Japan Ainu Archers','Japan Ainu Geberu','Japan Ainu Minieru','Japan Ainu Teppo',
  'Japan Heimin Mob','Japan Heimin Partisans','Japan Heimin Partisans Geberu','Japan Heimin Partisans Minieru','Japan Ishin Shishi','Japan Ronin','Japan Shizoku','Japan Teppotai Merc',
]);

const universalRecruitment = new Set(['fra_legion_early', 'fra_legion_mid', 'fra_legion_high']);
for (const r of normal) {
  if (!r.geo.length && !universalRecruitment.has(r.unit)) add('normal_without_geography', r);
  for (const tag of r.geo) if (!mapTags.has(tag)) add('unknown_map_tag', r, tag);
}
for (const r of replenishment) if (r.geo.length) add('geography_gated_replenishment', r, r.geo.join(','));

const exact = new Map([
  ['england|uk_gurkhas_high', ['himalayan']],
  ['bulga|ind_bhutan_warrior', ['himalayan']],
  ['france|fra_spahis_mid', ['north_africa']], ['france|fra_zouaves_early', ['north_africa']],
  ['hre|pru_kolonialreiter_high', ['colonial']], ['hre|pru_schutztruppe_high', ['colonial']],
  ['spain|spa_col_inf_early', ['colonial']], ['spain|spa_col_inf_high', ['colonial']], ['spain|spa_col_cav_mid', ['colonial']],
  ['venice|libya_inf', ['north_africa']], ['golden|oma_baluchi_musketeers', ['persia']],
  ['cuman|uyghur_camel_cav', ['steppe']], ['egypt|merc_kok_royal_cav', ['steppe']],
]);
for (const [key, expected] of exact) {
  const [faction, unit] = key.split('|');
  for (const r of normal.filter(x => x.faction === faction && x.unit === unit)) {
    if (r.geo.join(',') !== expected.join(',')) add('regional_override_mismatch', r, `expected ${expected}`);
  }
}
function japanTag(unit) {
  if (/\b(?:Ezo|Hoppo|Hokuchin|Tondenhei)\b|Bodyguard Ezo/i.test(unit)) return 'ezo';
  if (/\b(?:Satsuma|Saga)\b/i.test(unit)) return 'kyushu';
  if (/\b(?:Kiheitai|Yamagunitai|Jinshotai)\b/i.test(unit)) return 'chugoku';
  if (/\b(?:Shogitai|Shinsengumi|Denshutai)\b|Kaiso Shinsengumi|Ryukihei Shogun/i.test(unit)) return 'kanto';
  return 'japan';
}
for (const r of normal.filter(x => x.faction === 'saxons')) {
  const expected = japanTag(r.unit);
  if (r.geo.join(',') !== expected) add('japan_geography_mismatch', r, `expected ${expected}, got ${r.geo.join(',')}`);
}
for (const r of normal.filter(x => x.faction === 'papal_states')) if (r.geo.join(',') !== 'ethiopia') add('ethiopia_geography_mismatch', r, r.geo.join(','));
const forbiddenEurope = new Set(['aztecs','denmark','milan','poland','portugala','scotland','teu']);
for (const r of normal.filter(x => forbiddenEurope.has(x.faction) && x.geo.includes('europe'))) add('non_european_power_uses_europe_gate', r);
for (const r of normal.filter(x => x.geo.includes('europe') && !/^euro_hussars(?:_|$)/i.test(x.unit))) add('unjustified_pan_european_recruitment', r);
for (const r of normal.filter(x => x.faction === 'england' && /uk_imperial_foot/i.test(x.unit) && x.geo.join(',') !== 'settler')) add('imperial_foot_gate_mismatch', r, r.geo.join(','));
for (const r of normal.filter(x => x.faction === 'england' && /uk_foot_/i.test(x.unit) && x.geo.join(',') !== 'uk')) add('british_foot_gate_mismatch', r, r.geo.join(','));
for (const unit of universalRecruitment) for (const r of normal.filter(x => x.unit === unit)) if (r.geo.length) add('universal_unit_is_geography_gated', r, r.geo.join(','));
for (const r of land.filter(x => excludedCampaignSubfactions.has(x.unit))) add('excluded_subfaction_campaign_row', r);
const intentionalBuildingMercenaries = new Set(['merc_fra_blacks']);
for (const r of land.filter(x => mercenaryTypes.has(x.unit) && !tibetanCampaignUnits.has(x.unit) && !intentionalBuildingMercenaries.has(x.unit))) add('mercenary_campaign_row', r);

// Separate rows for two tags must not stack in any actual map region.
const groups = new Map();
for (const r of normal) {
  const key = [r.faction, r.unit, r.building, r.level, r.window].join('|');
  if (!groups.has(key)) groups.set(key, []);
  groups.get(key).push(r);
}
for (const group of groups.values()) {
  const tagged = group.filter(r => r.geo.length === 1);
  for (let i = 0; i < tagged.length; i++) for (let j = i + 1; j < tagged.length; j++) {
    const a = tagged[i].geo[0], b = tagged[j].geo[0];
    if (a === b) continue;
    const overlap = [...(tagRegions.get(a) || [])].filter(x => tagRegions.get(b)?.has(x));
    if (overlap.length) add('overlapping_recruitment_tags', tagged[i], `${a}+${b}: ${overlap.join(',')}`);
  }
}

const usedTags = [...new Set(normal.flatMap(r => r.geo))].sort();
for (const tag of usedTags) if (!declaredHiddenResources.has(tag)) issues.push({kind:'undeclared_hidden_resource', line:4, faction:'', unit:'', detail:tag});
if (declaredHiddenResources.size > 64) issues.push({kind:'hidden_resource_limit_exceeded', line:4, faction:'', unit:'', detail:String(declaredHiddenResources.size)});
const result = {
  ok: !issues.length && edb === mirror,
  mirrorsMatch: edb === mirror,
  mapRegions: regions.length,
  mapTags: mapTags.size,
  declaredHiddenResources: declaredHiddenResources.size,
  recruitmentTagsUsed: usedTags.length,
  normalRows: normal.length,
  replenishmentRows: replenishment.length,
  excludedSubfactionRows: land.filter(x => excludedCampaignSubfactions.has(x.unit)).length,
  tibetanCampaignRows: normal.filter(x => tibetanCampaignUnits.has(x.unit)).length,
  issues: issues.length,
};
console.log(JSON.stringify(result, null, 2));
if (issues.length) console.log(JSON.stringify(issues.slice(0, 100), null, 2));
if (!result.ok) process.exitCode = 1;
