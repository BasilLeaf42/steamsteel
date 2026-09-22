const fs=require('fs');
const p=require('path').join(__dirname,'standardize_remaining_merc_stats_20260922.js');
let s=fs.readFileSync(p,'utf8');
s=s.replaceAll("(?=^type\\s+|\\s*$)", "(?=^type\\s+|(?![\\s\\S]))");
fs.writeFileSync(p,s);
