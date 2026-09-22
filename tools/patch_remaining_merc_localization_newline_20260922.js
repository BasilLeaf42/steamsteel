const fs=require('fs'),path=require('path');
const p=path.join(__dirname,'standardize_remaining_merc_localization_20260922.js');
let s=fs.readFileSync(p,'utf8');
s=s.replace(";}\\nlet text=readLoc(p), old=readLoc(backup);",";}\nlet text=readLoc(p), old=readLoc(backup);");
fs.writeFileSync(p,s);
