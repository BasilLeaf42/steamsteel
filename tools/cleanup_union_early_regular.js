const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');

const stdPath = path.join(__dirname, 'standardize_union.js');
let std = fs.readFileSync(stdPath, 'utf8');
const oldLoop = "for(const u of all)for(const k of [u.type,`${u.type}_descr`,`${u.type}_descr_short`])";
const newLoop = "for(const u of [...all,{type:'uni_regulars_early'}])for(const k of [u.type,`${u.type}_descr`,`${u.type}_descr_short`])";
if (std.includes(oldLoop)) std = std.replace(oldLoop, newLoop);
else if (!std.includes(newLoop)) throw new Error('Localization cleanup loop changed unexpectedly');
fs.writeFileSync(stdPath, std);

const valPath = path.join(__dirname, 'validate_union.js');
let val = fs.readFileSync(valPath, 'utf8');
const marker = "const header=+(model.match(";
const check = "ok(!/\\{uni_regulars_early(?:_descr|_descr_short)?\\}/.test(txt('data/text/export_units.txt')),'stale early Regular localization');\n";
if (!val.includes(check)) val = val.replace(marker, check + marker);
fs.writeFileSync(valPath, val);
console.log('Added stale early-Regular localization cleanup and validation.');
