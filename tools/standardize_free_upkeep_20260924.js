const fs = require('fs');

const localizationPath = 'data/text/export_units.txt';
const eduPaths = [
  'data/tow_steamsteel/export_descr_unit.txt',
  'data/export_descr_unit.txt',
];

const localization = new Map();
for (const line of fs.readFileSync(localizationPath, 'utf8').split(/\r?\n/)) {
  const match = line.match(/^\{([^}]+)\}(.*)$/);
  if (match) localization.set(match[1], match[2]);
}

// Primary classification comes from stat_mental. The expressions below are
// explicit reserve/irregular overrides for formations whose training is better
// than the basic militia row.
const reservePattern = /\b(militia|milicia|reserv(?:e|es|ist|ists)|landwehr|landsturm|levy|levies|warband|irregulars?|village braves|national guard|state guards?|state volunteers|citizen[- ]soldiers?|tribal|garde mobile|guardia nacional|redif|montoneros|schutterij|bev[aä]ring|opolchenie|kazaki|cossacks?|gauchos?|farmers?|settlers?)\b|m[üu]stahf[iı]z|lashkar-e qawmi|haraka qabaliyya|boerekommando|volunt[aá]rios da p[aá]tria|risorgimento volunteers|volontari garibaldini|union volunteer cavalry|zouave volunteers/i;

// Faction tier penalties can reduce professional troops to low discipline.
// These verified Spanish regular lineages must never be inferred as militia
// from stat_mental alone.
const professionalOverrides = new Set([
  'spa_inf_early', 'spa_inf_mid', 'spa_inf_high',
  'spa_caz_early', 'spa_caz_mid', 'spa_caz_high',
  'spa_col_inf_early', 'spa_col_inf_mid', 'spa_col_inf_high',
  'cuban_inf_high',
  'spa_cav_early', 'spa_cav_mid', 'spa_cav_high',
  'spa_col_cav_mid', 'spa_cuirassiers_early', 'euro_hussars',
  'austro_sailor_spain_early', 'austro_sailor_spain_mid', 'austro_sailor_spain_high',
  'burmese_inf', 'merc_burmese_inf', 'skif_inf', 'turk_lt2',
  'rus_pekhota_early', 'rus_pekhota_mid', 'rus_pekhota_high',
  'rus_strelki_early', 'rus_strelki_mid', 'rus_strelki_high',
  'rus_marines_early', 'rus_marines_mid', 'rus_marines_high',
  'rus_sapery_early', 'rus_sapery_mid', 'rus_sapery_high',
  'rus_siberian_early', 'rus_siberian_mid', 'rus_siberian_high',
  'rus_conscript', 'rus_sailors', 'rus_conscript_ru', 'rus_roy_inf_ru',
  'rus_guard', 'russ_inf', 'rus_lat_inf_ru',
]);
const militiaOverrides = new Set([
  'csa_state_cavalry_early', 'csa_state_cavalry_mid', 'csa_state_cavalry_high',
  'csa_virginia_cavalry', 'uni_indian_scout_cavalry', 'merc_ap_front_cav',
  'mor_guich_cavalry', 'mor_hajjana', 'oma_bedouin_camelry',
  'qaj_tribal_cavalry', 'afg_tribal_cavalry',
  'qing_baqi_gunmen', 'qing_eight_banner_cavalry', 'korean_archers',
]);

function classifyAndRewrite(text) {
  const newline = text.includes('\r\n') ? '\r\n' : '\n';
  const hadFinalNewline = text.endsWith('\n');
  const lines = text.split(/\r?\n/);
  const output = [];
  const records = [];
  let record = null;

  function finishRecord() {
    if (!record) return;
    const name = localization.get(record.dictionary) || '';
    const short = localization.get(`${record.dictionary}_descr_short`) || '';
    const long = localization.get(`${record.dictionary}_descr`) || '';
    const quality = long.match(/Quality:\s*([^\\\r\n]+)/i)?.[1].trim().toLowerCase() || '';
    const explicitProfessional = /professional|elite/.test(quality);
    const explicitMilitia = /militia|levy|irregular|reserve/.test(quality);
    const projectileBase = (() => {
      const p = record.projectile;
      if (/^arquebus_bullet_/.test(p)) return 900;
      if (/^(?:harquebus|musket)_bullet_/.test(p)) return 1000;
      if (/^rifled_musket_bullet_/.test(p)) return 1200;
      if (/^rifle_bullet_/.test(p)) return 1500;
      if (/^magazine_rifle_bullet_/.test(p)) return 1800;
      return null;
    })();
    const campaignCost = Number(record.statCost?.[1]);
    const firearmInfantryMilitia = record.category === 'infantry' && projectileBase !== null && campaignCost <= projectileBase - 200;
    const meleeInfantryMilitia = record.category === 'infantry' && (!record.projectile || record.projectile === 'no') && campaignCost <= 500;
    const statMilitia = record.training === 'untrained' || firearmInfantryMilitia || meleeInfantryMilitia;
    const semanticReserve = reservePattern.test(`${name} ${short}`);
    const command = /(?:^|,\s*)(?:general_unit|command)(?:\s*,|$)/.test(record.attributes || '');
    const eligibleCategory = record.category !== 'ship' && record.category !== 'siege';
    const qualityMilitia = militiaOverrides.has(record.type) || explicitMilitia || (!explicitProfessional && (statMilitia || semanticReserve));
    record.keepFreeUpkeep = eligibleCategory && !command && !professionalOverrides.has(record.type) && qualityMilitia;
    records.push(record);
    record = null;
  }

  for (let index = 0; index < lines.length; index++) {
    const line = lines[index];
    let match;
    if ((match = line.match(/^type\s+(.+?)\s*$/))) {
      finishRecord();
      record = { type: match[1], start: output.length, attributesIndex: -1, attributes: '', statCostIndex: -1, statCost: null, dictionary: '', category: '', discipline: '', training: '', projectile: '' };
    } else if (record && (match = line.match(/^dictionary\s+([^;\s]+)/))) {
      record.dictionary = match[1];
    } else if (record && (match = line.match(/^category\s+(.+?)\s*$/))) {
      record.category = match[1];
    } else if (record && (match = line.match(/^attributes\s+(.+?)\s*$/))) {
      record.attributesIndex = output.length;
      record.attributes = match[1];
    } else if (record && (match = line.match(/^stat_mental\s+\d+\s*,\s*([^,]+)\s*,\s*([^,\s]+)/))) {
      record.discipline = match[1].trim();
      record.training = match[2].trim();
    } else if (record && (match = line.match(/^stat_pri\s+[^,]+\s*,\s*[^,]+\s*,\s*([^,\s]+)/))) {
      record.projectile = match[1].trim();
    } else if (record && (match = line.match(/^stat_cost\s+(.+)$/))) {
      record.statCostIndex = output.length;
      record.statCost = match[1].split(',').map(value => value.trim());
    }
    output.push(line);
  }
  finishRecord();

  let added = 0;
  let removed = 0;
  let kept = 0;
  let costChanged = 0;
  for (const item of records) {
    if (item.attributesIndex < 0) throw new Error(`Missing attributes row: ${item.type}`);
    const tokens = item.attributes.split(',').map(token => token.trim()).filter(Boolean);
    const has = tokens.includes('free_upkeep_unit');
    if (item.keepFreeUpkeep) {
      kept++;
      if (!has) {
        tokens.unshift('free_upkeep_unit');
        added++;
      }
    } else if (has) {
      tokens.splice(tokens.indexOf('free_upkeep_unit'), 1);
      removed++;
    }
    output[item.attributesIndex] = `attributes       ${tokens.join(', ')}`;

    if (!item.statCost || item.statCost.length < 8) throw new Error(`Missing/invalid stat_cost row: ${item.type}`);
    const campaignCost = Number(item.statCost[1]);
    const expectedUpkeep = Math.round(campaignCost / 3);
    if (Number(item.statCost[2]) !== expectedUpkeep || Number(item.statCost[7]) !== expectedUpkeep) {
      item.statCost[2] = String(expectedUpkeep);
      item.statCost[7] = String(expectedUpkeep);
      output[item.statCostIndex] = `stat_cost        ${item.statCost.join(', ')}`;
      costChanged++;
    }
  }

  let rewritten = output.join(newline);
  if (!hadFinalNewline && rewritten.endsWith(newline)) rewritten = rewritten.slice(0, -newline.length);
  return { rewritten, records, added, removed, kept, costChanged };
}

let expectedText = null;
for (const eduPath of eduPaths) {
  const original = fs.readFileSync(eduPath, 'utf8');
  const result = classifyAndRewrite(original);
  if (expectedText !== null && result.rewritten !== expectedText) {
    throw new Error(`Canonical/runtime rewrite mismatch at ${eduPath}`);
  }
  expectedText = result.rewritten;
  fs.writeFileSync(eduPath, result.rewritten, 'utf8');
  process.stdout.write(`${eduPath}: keep=${result.kept}, added=${result.added}, removed=${result.removed}, cost_changed=${result.costChanged}\n`);
}
