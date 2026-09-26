const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const canonical = path.join(root, 'data/tow_steamsteel/export_descr_buildings.txt');
const mirror = path.join(root, 'data/export_descr_buildings.txt');
const text = fs.readFileSync(canonical, 'utf8').replace(/\r/g, '');
const mirrorText = fs.readFileSync(mirror, 'utf8').replace(/\r/g, '');

const families = {
  barracks: new Set(['uni_state_volunteers_early','uni_regulars_mid','uni_regulars_high','uni_national_guard_mid','uni_national_guard_high','uni_colored_troops_early','uni_irish_brigade_early','uni_zouaves_early','uni_sharpshooters_early','uni_dragoons_early','uni_dragoons_mid','uni_dragoons_high','uni_volunteer_cavalry_early','uni_indian_scouts','uni_indian_scout_cavalry']),
  port: new Set(['uni_marines_early','uni_marines_mid','uni_marines_high']),
  professional_military: new Set(['uni_general_staff']),
  cannon: new Set(['usa_12lb','usa_armstrong','usa_gatling','usa_5lb','usa_maxim','usa_pompom','usa_150mm']),
};
const allUnits = new Set(Object.values(families).flatMap(x => [...x]));
const regularBarracks = new Set(['uni_regulars_mid','uni_regulars_high','uni_sharpshooters_early','uni_dragoons_early','uni_dragoons_mid','uni_dragoons_high']);

const entries = [];
let building = '', level = '';
for (const [index, line] of text.split('\n').entries()) {
  const bm = line.match(/^building\s+(\S+)/); if (bm) building = bm[1];
  const lm = line.match(/^\s{8}(\S+)\s+(?:city|castle)\s+requires\b/); if (lm) level = lm[1];
  const rm = line.match(/^\s*recruit_pool\s+"([^"]+)"\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+requires\s+(.+)$/);
  if (!rm || !/\bfactions\s*\{[^}]*\bportugala\b/.test(rm[6])) continue;
  entries.push({line:index+1, building, level, unit:rm[1], initial:+rm[2], rate:+rm[3], max:+rm[4], req:rm[6]});
}

const errors = [];
if (text !== mirrorText) errors.push('Canonical/runtime EDB mismatch');
if (!entries.length) errors.push('No Union recruitment rows found');
const units = new Set(entries.map(x => x.unit));
for (const u of allUnits) if (!units.has(u)) errors.push(`Missing Union unit: ${u}`);
for (const u of units) if (!allUnits.has(u)) errors.push(`Unexpected Union unit: ${u}`);
for (const e of entries) {
  if (!families[e.building]?.has(e.unit)) errors.push(`Wrong building family at ${e.line}: ${e.unit} in ${e.building}`);
  const replenishment = e.max < 1;
  if (replenishment && /hidden_resource/.test(e.req)) errors.push(`Geography-gated replenishment at ${e.line}`);
  if (replenishment && e.max !== .99) errors.push(`Replenishment maximum is not 0.99 at ${e.line}`);
  if (!replenishment && !/hidden_resource/.test(e.req)) errors.push(`Ungated normal recruitment at ${e.line}`);
  if (!replenishment && e.initial < 1) errors.push(`Normal recruitment initial pool below 1 at ${e.line}`);
  if (!replenishment && e.level === 'militia_drill_square' && regularBarracks.has(e.unit)) errors.push(`Regular unit in drill square at ${e.line}: ${e.unit}`);
}
const byBuilding = {};
for (const e of entries) {
  byBuilding[e.building] ||= {normal:0,replenishment:0,units:new Set()};
  byBuilding[e.building][e.max < 1 ? 'replenishment' : 'normal']++;
  byBuilding[e.building].units.add(e.unit);
}
for (const x of Object.values(byBuilding)) x.units = x.units.size;

const expectedWindows = {
  uni_state_volunteers_early:['not event_counter military_reforms_1875 1'],
  uni_regulars_mid:['event_counter military_reforms_1875 1','not event_counter military_reforms_2 1'],
  uni_regulars_high:['event_counter military_reforms_2 1'],
  uni_national_guard_mid:['event_counter military_reforms_1875 1','not event_counter military_reforms_1890 1'],
  uni_national_guard_high:['event_counter military_reforms_1890 1'],
  uni_marines_early:['not event_counter military_reforms_1865 1'],
  uni_marines_mid:['event_counter military_reforms_1865 1','not event_counter military_reforms_1895 1'],
  uni_marines_high:['event_counter military_reforms_1895 1'],
};
for (const e of entries) {
  for (const token of expectedWindows[e.unit] || []) if (!e.req.includes(token)) errors.push(`Missing date token at ${e.line}: ${e.unit} -> ${token}`);
}

console.log(JSON.stringify({ok:!errors.length, rows:entries.length, units:units.size, byBuilding, errors}, null, 2));
if (errors.length) process.exitCode = 1;
