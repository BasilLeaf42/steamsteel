const fs=require('fs'),path=require('path');const root=path.resolve(__dirname,'..');
const read=p=>{const b=fs.readFileSync(p);return (b[0]===255&&b[1]===254?b.toString('utf16le'):b.toString('utf8')).replace(/^\uFEFF/,'').replace(/\r/g,'')};
const canon=read(path.join(root,'data/tow_steamsteel/export_descr_unit.txt')),mirror=read(path.join(root,'data/export_descr_unit.txt')),loc=read(path.join(root,'data/text/export_units.txt'));
const blocks=canon.split(/(?=^type\s+)/m).filter(x=>/^type\s+/m.test(x));const findings={};const add=(k,v)=>{(findings[k]??=[]).push(v)};
const locKeys=new Set([...loc.matchAll(/^\{([^}]+)\}/gm)].map(m=>m[1]));
const get=(b,re)=>(b.match(re)||[])[1]||'';
for(const b of blocks){const type=get(b,/^type\s+(.+)$/m).trim(),dict=get(b,/^dictionary\s+([^\s;]+)/m),cat=get(b,/^category\s+(\S+)/m),cls=get(b,/^class\s+(\S+)/m),sold=get(b,/^soldier\s+([^\r\n]+)/m).split(',').map(x=>x.trim()),pri=get(b,/^stat_pri\s+([^\r\n]+)/m).split(',').map(x=>x.trim()),attrs=get(b,/^attributes\s+([^\r\n]+)/m),formation=get(b,/^formation\s+([^\r\n]+)/m),cost=get(b,/^stat_cost\s+([^\r\n]+)/m).split(',').map(x=>Number(x.trim())),mental=get(b,/^stat_mental\s+([^\r\n]+)/m).split(',').map(x=>x.trim()),ground=get(b,/^stat_ground\s+([^\r\n]+)/m),armour=get(b,/^stat_pri_armour\s+([^\r\n]+)/m);
 if(cat==='ship'||cat==='siege')continue;
 if(!dict||!locKeys.has(dict)||!locKeys.has(dict+'_descr')||!locKeys.has(dict+'_descr_short'))add('localization',type);
 if(/\bhigh\b/.test(mental[1]||''))add('invalidDiscipline',type);if(/\barmoured\b/.test(armour))add('invalidArmourToken',type);
 const fd=Number(get(b,/^stat_fire_delay\s+(\S+)/m));if(fd) add('unsafeFireDelay',`${type}: ${fd}`);
 if(ground&&ground!=='0, 0, 0, 0'&&type!=='camel_wagon')add('terrainBonuses',`${type}: ${ground}`);
 if(cost.length>=8){if(cost[3]!==100||cost[4]!==100)add('upgradeCosts',type);const third=Math.round(cost[1]/3);if(Math.abs(cost[2]-third)>1)add('upkeep',`${type}: ${cost[2]} vs ${third}`);if(Math.abs(cost[7]-third)>1)add('overlimit',`${type}: ${cost[7]} vs ${third}`);}
 if(cat==='cavalry'&&Number(sold[1])>4&&!/^(?:boer_wagon|camel_wagon|indian_ele|siam_ele_gunner|Elephant Artillery)$/.test(type)&&formation&&!/^2(?:\.0)?, 2, 4, 4, 3, square$/.test(formation))add('cavalryFormation',`${type}: ${formation}`);
 const projectile=pri[2]||'',firearm=/(?:arquebus|harquebus|musket|rifle|wall_gun|long_gun).*_bullet/.test(projectile);
 if(firearm&&dict){const sm=loc.match(new RegExp('^\\{'+dict.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'_descr_short\\}([^\\n]*)','m'));const s=sm?sm[1]:'';if(!/\([^(),]+,\s*[^()]+(?:\([^)]*\))?\)/.test(s)||/\b(?:Early|Mid|Late|High|Vroeg|Middel|Laat)\b/.test(s))add('firearmShortDescription',`${type}: ${s}`);}
 if(dict&&/_(?:early|mid|high)$/.test(type)){const lm=loc.match(new RegExp('^\\{'+dict.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\}([^\\n]*)','m'));const want=type.endsWith('_early')?'Early':type.endsWith('_mid')?'Mid':'Late';if(!lm||!new RegExp('\\('+want+'\\)$').test(lm[1]))add('periodLabel',type);}
 if(cat==='infantry'&&sold[1]){const n=Number(sold[1]),skirm=/^1\.4, 1\.8, 2\.8, 3\.6, 3, square$/.test(formation),command=n<=4&&/general_unit|command/.test(attrs),otherMissile=projectile&&projectile!=='no'&&!firearm,specialTeam=n===16,warband=n===96&&/(?:warband|tribal|zulu|xhosa|mahdist|heimin|haraka|chäwa|cawa|merc_maori)/i.test(type+' '+dict);if(!command&&firearm&&skirm&&n!==30)add('skirmisherStrength',`${type}: ${n}`);else if(!command&&firearm&&!skirm&&n!==40)add('firearmStrength',`${type}: ${n}`);else if(!command&&!firearm&&!otherMissile&&!specialTeam&&!warband&&n!==80)add('meleeStrength',`${type}: ${n}`);}
 if(cat==='cavalry'&&sold[1]&&Number(sold[1])>4&&Number(sold[1])!==24&&!/^(?:boer_wagon|camel_wagon|indian_ele|siam_ele_gunner|Elephant Artillery)$/.test(type))add('cavalryStrength',`${type}: ${sold[1]}`);
 if(cat==='cavalry'&&/(?:rifle|musket)_carbine_bullet/.test(projectile)&&cls!=='missile'&&Number(pri[3])>60&&Number(sold[1])>4)add('carbineClass',`${type}: ${cls}`);
 if(/\bMTW2_Musket_SSK\b/.test(b)&&/\bgunpowder_unit\b/.test(attrs))add('sskGunpowderConflict',type);
}
const out={records:blocks.length,mirrorsEqual:canon===mirror,counts:Object.fromEntries(Object.entries(findings).map(([k,v])=>[k,v.length])),findings};fs.writeFileSync(path.join(__dirname,'all_units_audit_20260922.json'),JSON.stringify(out,null,2));console.log(JSON.stringify({records:out.records,mirrorsEqual:out.mirrorsEqual,counts:out.counts},null,2));
