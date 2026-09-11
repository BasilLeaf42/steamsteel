const fs = require('fs');
const path = require('path');
const cp = require('child_process');

const root = path.resolve(__dirname, '..');
const canonical = path.join(root, 'data/tow_steamsteel/export_descr_unit.txt');
const runtime = path.join(root, 'data/export_descr_unit.txt');
const source = cp.execFileSync('git', ['show', '700a9c7c:data/tow_steamsteel/export_descr_unit.txt'], {cwd:root, encoding:'utf8', maxBuffer:32*1024*1024}).replace(/\r\n/g, '\n');
const fromCommit = [
  'spa_inf_early','spa_inf_mid','spa_inf_high','spa_caz_early','spa_caz_mid','spa_caz_high',
  'spa_milicia_nacional_early','spa_milicia_nacional_mid','spa_milicia_nacional_high',
  'spa_col_inf_early','spa_col_inf_mid','spa_col_inf_high','cuban_inf_high',
  'spa_cav_early','spa_cav_mid','spa_cav_high','spa_col_cav_mid','spa_cuirassiers_early',
  'civil_guard','euro_hussars'
];
const marines=['austro_sailor_spain_early','austro_sailor_spain_mid','austro_sailor_spain_high'];
const wanted=[...fromCommit,...marines];

function record(text, type) {
  const starts=[...text.matchAll(/^type\s+(\S+)/gm)];
  const i=starts.findIndex(m=>m[1]===type);
  if(i<0) throw new Error(`Recovery source lacks ${type}`);
  const end=i+1<starts.length?starts[i+1].index:text.length;
  return text.slice(starts[i].index,end).trimEnd();
}

const recovered=fromCommit.map(type=>record(source,type));
for(const [i,type] of marines.entries()){
  const period=['early','mid','high'][i];
  recovered.push(record(source,`spa_inf_${period}`)
    .replace(/^type\s+.*$/m,`type             ${type}`)
    .replace(/^dictionary\s+\S+.*$/m,`dictionary       ${type}`)
    .replace(/^soldier\s+\S+,/m,`soldier          ${type},`));
}
let edu=fs.readFileSync(canonical,'utf8').replace(/\r\n/g,'\n');
const marker='; Spain (spain) — recovered standardized records';
const oldAt=edu.indexOf(marker);
if(oldAt>=0){
  const oldStart=edu.lastIndexOf('; ============================================================================',oldAt);
  const franceAt=edu.indexOf('; France (france) — standardized infantry and cavalry',oldAt);
  const oldEnd=edu.lastIndexOf('; ============================================================================',franceAt);
  edu=edu.slice(0,oldStart)+edu.slice(oldEnd);
}
for(const type of wanted){
  if(new RegExp(`^type\\s+${type}$`,'m').test(edu)) throw new Error(`Current EDU already contains ${type}`);
}
const franceAt=edu.indexOf('; France (france) — standardized infantry and cavalry');
const insertAt=edu.lastIndexOf('; ============================================================================',franceAt);
if(insertAt<0) throw new Error('Could not locate France block');
const block=['; ============================================================================',marker,'; ============================================================================',...recovered].join('\n\n')+'\n\n';
edu=edu.slice(0,insertAt)+block+edu.slice(insertAt);
const out=edu.replace(/\n/g,'\r\n');
fs.writeFileSync(canonical,out);fs.writeFileSync(runtime,out);
console.log(`Recovered ${wanted.length} Spanish EDU records from commit 700a9c7c.`);
