const fs=require('fs'),path=require('path'),R=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(R,p),'utf8').replace(/\r/g,''),ok=(v,m)=>{if(!v)throw Error(m)};
const edu=read('data/tow_steamsteel/export_descr_unit.txt'),mirror=read('data/export_descr_unit.txt'),edb=read('data/tow_steamsteel/export_descr_buildings.txt'),edbm=read('data/export_descr_buildings.txt'),merc=read('data/world/maps/campaign/camp_steamsteel/descr_mercenaries.txt'),strat=read('data/world/maps/campaign/camp_steamsteel/descr_strat.txt'),model=read('data/unit_models/battle_models.modeldb');
ok(edu===mirror,'EDU mirror');ok(edb===edbm,'EDB mirror');
function b(t){const x=edu.match(new RegExp(`^type\\s+${t}\\n[\\s\\S]*?(?=^type\\s+|(?![\\s\\S]))`,'m'));ok(x,'unit '+t);return x[0]}
function mb(t){const x=model.match(new RegExp(`^${t.length} ${t}\\s*$[\\s\\S]*?(?=^\\d+ [^\\s;]+\\s*$\\n\\d+ \\d+\\s*$|(?![\\s\\S]))`,'m'));ok(x,'model '+t);return x[0]}
for(const t of ['kaz_inf','kok_ww1','kaz_cav','merc_kaz_inf','merc_kaz_cav'])ok(!new RegExp(`^type\\s+${t}$`,'m').test(edu),t+' removed');
ok(!/recruit_pool\s+"(?:kaz_inf|kok_ww1|kaz_cav)"/.test(edb),'broken units absent from EDB');ok(!/^\s*unit\s+merc_kaz_(?:inf|cav)\b/m.test(merc),'broken Kazakh mercenaries absent');ok(!/^\s*unit\s+(?:kok_ww1|kaz_inf|kaz_cav|merc_kaz_inf|merc_kaz_cav)\b/m.test(strat),'broken units absent from startpos');
ok(/^era 2\s+cuman, slave$/m.test(b('kok_5lb'))&&!/^era [01]/m.test(b('kok_5lb')),'mortar late only');
ok(/^stat_pri\s+2, 2, no, 0, 0, melee, melee_blade, piercing, spear,/m.test(b('kok_spears'))&&/^stat_pri_armour\s+3, 1, 3,/m.test(b('kok_spears'))&&/MTW2_Spear_primary[\s\S]*fs_test_shield/.test(mb('kok_spears')),'spear and shield distinction');
ok(/^stat_sec\s+3, 2, no, 0, 0, melee, melee_blade, piercing, sword,/m.test(b('turkmen_inf'))&&/^stat_sec_attr\s+no$/m.test(b('turkmen_inf'))&&/MTW2_CR_Sword[\s\S]*MTW2_Sword_Primary/.test(mb('turkmen_inf')),'sword-only distinction');
for(const t of ['kashgar_inf','kok_inf'])ok(/^stat_sec_attr\s+ap, short_pike$/m.test(b(t))&&/MTW2_Pike[\s\S]*MTW2_Pike_primary/.test(mb(t)),t+' bayonet distinction');
for(const t of ['kok_spears','turkmen_inf','uyghur_camel_cav']){const d=fs.readFileSync(path.join(R,'data/ui/units/cuman',`#${t}.tga`));ok(d.readUInt16LE(12)===48&&d.readUInt16LE(14)===64&&d[16]===32,t+' RGBA card')}
console.log('Turkestan follow-up validation passed: disabled units, mortar periods, weapon distinctions and role cards.');
