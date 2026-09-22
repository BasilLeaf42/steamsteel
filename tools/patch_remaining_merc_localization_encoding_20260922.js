const fs=require('fs'),path=require('path');
const p=path.join(__dirname,'standardize_remaining_merc_localization_20260922.js');
let s=fs.readFileSync(p,'utf8');
const old="let text=fs.readFileSync(p,'utf8'), old=fs.readFileSync(backup,'utf8');";
const replacement="function readLoc(file){const b=fs.readFileSync(file);return b[0]===255&&b[1]===254?b.toString('utf16le').replace(/^\\uFEFF/,''):b.toString('utf8').replace(/^\\uFEFF/,'');}\\nlet text=readLoc(p), old=readLoc(backup);";
if(!s.includes(old))throw new Error('encoding target not found');
fs.writeFileSync(p,s.replace(old,replacement));
