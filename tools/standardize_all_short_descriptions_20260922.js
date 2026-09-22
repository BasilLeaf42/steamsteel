const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const eduPath = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const mirrorPath = path.join(root, 'data/export_descr_unit.txt');
const locPath = path.join(root, 'data/text/export_units.txt');
const reportPath = path.join(__dirname, 'all_short_description_audit_20260922.json');

function readText(file) {
  const b = fs.readFileSync(file);
  return b[0] === 0xff && b[1] === 0xfe
    ? { text: b.toString('utf16le').replace(/^\uFEFF/, ''), encoding: 'utf16le', bom: true }
    : { text: b.toString('utf8').replace(/^\uFEFF/, ''), encoding: 'utf8', bom: false };
}
function writeText(file, state, text) {
  const body = state.encoding === 'utf16le' ? Buffer.from(text, 'utf16le') : Buffer.from(text, 'utf8');
  fs.writeFileSync(file, state.bom ? Buffer.concat([Buffer.from([0xff, 0xfe]), body]) : body);
}
function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
function stripPeriod(s) {
  return s.replace(/\s*\((?:Early|Mid|Late|High|Vroeg|Middel|Laat|Spät)\)\s*$/i, '').trim();
}
function splitTrailingTuple(s) {
  const text = s.trim();
  const open = text.indexOf(' (');
  if (open < 1) return null;
  let depth = 0, close = -1;
  for (let i = open + 1; i < text.length; i++) {
    if (text[i] === '(') depth++;
    else if (text[i] === ')' && --depth === 0) { close = i; break; }
  }
  if (close < 0) return null;
  const tail = text.slice(close + 1).trim();
  if (tail && !tail.startsWith(',')) return null;
  return {
    base: text.slice(0, open).trim(),
    equipment: text.slice(open + 2, close).trim(),
    detail: tail.replace(/^,\s*/, '').trim()
  };
}

// Ordering matters: identify compound firearm families before their shorter suffixes.
const familyPatterns = [
  ['Magazine Rifle', /\bmagazine[ -]rifles?\b/i],
  ['Rifle-Musket', /\b(?:rifle[ -]muskets?|rifled muskets?)\b/i],
  ['Breech-Loading Rifle', /\bbreech[ -]load(?:ing|er)? rifles?\b/i],
  ['Breech-Loading Carbine', /\bbreech[ -]load(?:ing|er)? carbines?\b/i],
  ['Matchlock', /\bmatchlocks?\b/i],
  ['Arquebus', /\bharquebus(?:es)?\b|\barquebus(?:es)?\b/i],
  ['Wall Gun', /\bwall[ -]guns?\b|\bjingals?\b/i],
  ['Carbine', /\bcarbines?\b/i],
  ['Revolver', /\brevolvers?\b/i],
  ['Pistol', /\bpistols?\b/i],
  ['Musket', /\bmuskets?\b/i],
  ['Rifle', /\brifles?\b/i]
];
const canonicalFamilies = new Set(familyPatterns.map(x => x[0].toLowerCase()));

function normalizeEquipment(raw, statFamily) {
  if (!raw) return null;
  raw = raw.replace(/^\s*(?:Early|Mid|Late|High|Vroeg|Middel|Laat|Spät)\s*;\s*/i, '').trim();
  let parts = raw.split(',').map(x => x.trim()).filter(Boolean);
  if (parts.length >= 2 && canonicalFamilies.has(parts[0].toLowerCase())) {
    parts[1] = parts[1].replace(/^\s*(?:Early|Mid|Late|High|Vroeg|Middel|Laat|Spät)\s*;\s*/i, '').trim();
    return parts.filter(Boolean).join(', ');
  }

  const joined = parts.join(', ');
  for (const [family, re] of familyPatterns) {
    if (!re.test(joined)) continue;
    let model = joined.replace(re, '').replace(/^\s*[-,:]\s*|\s*[-,:]\s*$/g, '').replace(/\s{2,}/g, ' ').trim();
    // Preserve secondary visible equipment without pretending it is part of the firearm model.
    model = model.replace(/,\s*(Sabre|Sword|Bayonet|Axe|Shield)s?\b/gi, '; $1');
    if (!model || /^(mixed|various|standard|generic)$/i.test(model)) return null;
    return `${family}, ${model}`;
  }
  if (statFamily) {
    const model = joined.replace(/^\s*(?:Early|Mid|Late|High|Vroeg|Middel|Laat|Spät)\s*;\s*/i, '').trim();
    if (model && !/^(mixed|various|standard|generic)$/i.test(model)) return `${statFamily}, ${model}`;
  }
  // Traditional and melee equipment legitimately uses a one-part equipment label.
  if (/\b(?:bow|sword|sabre|lance|spear|javelin|axe|mace|shield|halberd|unarmed)\b/i.test(joined)) return joined;
  // Artillery titles are already the weapon designation and need no artificial family/model split.
  if (/\b(?:cannon|gun|howitzer|mortar|mitrailleuse|pom-pom|artillery)\b/i.test(joined)) return joined;
  return null;
}

const edu = readText(eduPath).text;
if (readText(mirrorPath).text !== edu) throw new Error('Canonical EDU and runtime mirror differ before localization pass');
const locState = readText(locPath);
let loc = locState.text;
const entries = new Map();
for (const block of edu.split(/(?=^type\s+)/m)) {
  const m = block.match(/^dictionary\s+([^\s;]+)(?:\s*;\s*(.*))?$/m);
  if (!m || entries.has(m[1])) continue;
  const category = (block.match(/^category\s+(\S+)/m) || [])[1] || '';
  const statPri = (block.match(/^stat_pri\s+([^\r\n]+)/m) || [])[1] || '';
  const projectile = statPri.split(',')[2]?.trim() || '';
  let statFamily = null;
  if (/magazine_rifle_carbine/.test(projectile)) statFamily = 'Carbine';
  else if (/magazine_rifle/.test(projectile)) statFamily = 'Magazine Rifle';
  else if (/rifled_musket_carbine|rifle_carbine/.test(projectile)) statFamily = 'Carbine';
  else if (/rifled_musket/.test(projectile)) statFamily = 'Rifle-Musket';
  else if (/rifle_bullet/.test(projectile)) statFamily = 'Rifle';
  else if (/musket_carbine/.test(projectile)) statFamily = 'Carbine';
  else if (/musket_bullet/.test(projectile)) statFamily = 'Musket';
  else if (/arquebus|harquebus/.test(projectile)) statFamily = 'Matchlock';
  else if (/wall_gun|long_gun/.test(projectile)) statFamily = 'Wall Gun';
  entries.set(m[1], { key: m[1], comment: (m[2] || '').trim(), category, statFamily });
}
function get(key) {
  const m = loc.match(new RegExp('^\\{' + esc(key) + '\\}([^\\r\\n]*)', 'm'));
  return m ? m[1].trim() : null;
}
function put(key, value) {
  const re = new RegExp('^\\{' + esc(key) + '\\}[^\\r\\n]*', 'm');
  if (!re.test(loc)) return false;
  loc = loc.replace(re, `{${key}}${value}`);
  return true;
}

const changed = [], unresolved = [], missing = [];
const equipmentOverrides = {
  net_grenadiers_high: 'Magazine Rifle, Geweer M.95 (Mannlicher)',
  net_jagers_high: 'Magazine Rifle, Geweer M.95 (Mannlicher)',
  dan_marines_mid: 'Rifle, Flådens Bagladeriffel M/1853/66 (Snider)'
  ,mex_state_guard_mid: 'Breech-Loading Rifle, Winchester Model 1866'
  ,qing_xiang_huai_mid: 'Rifle, Dreyse M1868'
  ,qing_green_banner_regulars: 'Rifle-Musket, Pattern 1853 Enfield'
  ,qing_xiang_huai_early: 'Rifle-Musket, Pattern 1853 Enfield'
  ,qing_green_banner_late: 'Rifle, Mauser Model 1871'
  ,austro_sailor_england: 'Rifle, Lorenz Model 1862 Wänzl'
  ,austro_sailor_normans: 'Rifle, Lorenz Model 1862 Wänzl'
  ,black_guard: 'Musket, Brown Bess India Pattern'
  ,moroccan_camel_roy: 'Matchlock, North African Trade Pattern'
  ,csa_lancer_te: 'Carbine, Mauser Model 1895'
  ,moroccan_camel_gunner: 'Matchlock, North African Trade Pattern'
  ,arab_brigade: 'Musket, Brown Bess India Pattern'
  ,qajar_foot: 'Matchlock, Persian Jazayer Pattern'
  ,pashtun_inf: 'Wall Gun, Afghan Jezail Pattern'
  ,pashtun_camel_gunner: 'Matchlock, Afghan Trade Pattern'
  ,uyghur_camel_cav: 'Matchlock, Central Asian Tufang Pattern'
  ,ghulja_inf: 'Matchlock, Central Asian Tufang Pattern'
  ,camel_wagon: 'Wall Gun, Central Asian Jingal'
  ,indian_ele: 'Musket, Indian Toradar Pattern'
  ,qing_baqi_gunmen: 'Wall Gun, Chinese Jingal'
  ,qing_green_banner_gunmen: 'Matchlock, Chinese Matchlock Pattern'
  ,bolsh_cav: 'Rifle, Mosin–Nagant M1891 Dragoon'
  ,india_light_musk: 'Matchlock, Indian Toradar Pattern'
  ,peru_hussars: 'Carbine, Remington Rolling Block Carbine'
  ,fra_cav2_poland: 'Carbine, Mannlicher M1888–90'
  ,peru_foot_aztecs: 'Rifle, Remington Rolling Block Modelo 1871'
  ,turk_lt: 'Carbine, Mauser Model 1890'
};
for (const e of entries.values()) {
  const visible = get(e.key);
  const oldShort = get(e.key + '_descr_short');
  if (visible === null || oldShort === null) { missing.push({ key: e.key, visible: visible !== null, short: oldShort !== null }); continue; }

  const visibleTuple = splitTrailingTuple(visible);
  const commentTuple = splitTrailingTuple(e.comment);
  const shortTuple = splitTrailingTuple(oldShort);
  const baseName = stripPeriod(visibleTuple ? visibleTuple.base : visible);
  const evidence = [commentTuple && commentTuple.equipment, shortTuple && shortTuple.equipment, visibleTuple && visibleTuple.equipment].filter(Boolean);
  let equipment = equipmentOverrides[e.key] || null;
  for (const candidate of evidence) {
    if (equipment) break;
    if (/^(?:Early|Mid|Late|High|Vroeg|Middel|Laat|Spät)$/i.test(candidate)) continue;
    equipment = normalizeEquipment(candidate, e.statFamily); if (equipment) break;
  }
  if (!equipment) { unresolved.push({ key: e.key, category: e.category, firearmFamily: e.statFamily, name: visible, comment: e.comment, short: oldShort }); continue; }

  // Only text after an existing equipment tuple is a structured additional description.
  // Plain legacy prose is retained unless it is merely a duplicate name/role label.
  let detail = shortTuple ? shortTuple.detail : oldShort.trim();
  if (detail && (stripPeriod(detail).toLowerCase() === baseName.toLowerCase() || detail.toLowerCase() === e.comment.toLowerCase())) detail = '';
  const next = `${baseName} (${equipment})${detail ? ', ' + detail.replace(/^,\s*/, '') : ''}`;
  if (next !== oldShort) { put(e.key + '_descr_short', next); changed.push({ key: e.key, before: oldShort, after: next }); }
}

writeText(locPath, locState, loc);
fs.writeFileSync(reportPath, JSON.stringify({ changedCount: changed.length, unresolvedCount: unresolved.length, missingCount: missing.length, changed, unresolved, missing }, null, 2));
console.log(JSON.stringify({ changed: changed.length, unresolved: unresolved.length, missing: missing.length, report: path.relative(root, reportPath) }));
