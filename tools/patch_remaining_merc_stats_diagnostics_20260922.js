const fs=require('fs');
const p=require('path').join(__dirname,'standardize_remaining_merc_stats_20260922.js');
let s=fs.readFileSync(p,'utf8');
s=s.replace("    if (c.count) block = setSoldierCount(block,c.count,c.soldier);", "    if (c.count) { try { block = setSoldierCount(block,c.count,c.soldier); } catch (e) { throw new Error(`${type}: ${e.message}`); } }");
fs.writeFileSync(p,s);
