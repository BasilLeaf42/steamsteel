const fs=require('fs'),path=require('path');
const p=path.join(__dirname,'audit_remaining_mercenaries.js');let s=fs.readFileSync(p,'utf8');
s=s.replace("  else if (!/^(Militia|Regular|Elite|Tribal|Mercenary|Naval)/i.test(short)) issues.push('short description not role/quality-first');", "  else { const base=display.replace(/ \\(Early|Mid|Late\\)$/,''); if (!short.startsWith(base)) issues.push('short description not name-first'); }");
s=s.replace("/unit_sprites\\/(?:tmp_cavalry_sprite|.*(?:cav|horse).*)\\.spr/i", "/unit_sprites\\/(?:tmp_cavalry_sprite|.*(?:cav|horse|hoshuchi|lancer|hussar|dragoon).*)\\.spr/i");
fs.writeFileSync(p,s);
