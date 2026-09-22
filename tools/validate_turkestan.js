const fs=require('fs'),path=require('path'),R=path.resolve(__dirname,'..'),txt=p=>fs.readFileSync(path.join(R,p),'utf8').replace(/\r/g,''),ok=(v,m)=>{if(!v)throw Error(m)};
const e=txt('data/tow_steamsteel/export_descr_unit.txt'),em=txt('data/export_descr_unit.txt'),m=txt('data/unit_models/battle_models.modeldb');ok(e===em,'EDU mirror');
function b(t){let x=e.match(new RegExp(`^type\\s+${t}\\n[\\s\\S]*?(?=^type\\s+|(?![\\s\\S]))`,'m'));ok(x,'unit '+t);return x[0]}
function mb(t){let x=m.match(new RegExp(`^${t.length} ${t}\\s*$[\\s\\S]*?(?=^\\d+ [^\\s;]+\\s*$\\n\\d+ \\d+\\s*$|(?![\\s\\S]))`,'m'));ok(x,'model '+t);return x[0]}
const core=['kok_spears','turkmen_inf','ghulja_inf','buk_guard','kashgar_inf','kok_inf','kok_cav','kok_royal_cav','uyghur_camel_cav','kok_rcav','camel_wagon'];
for(const t of core){if(t!=='camel_wagon')ok(/^stat_ground\s+0, 0, 0, 0$/m.test(b(t)),t+' ground');const p=path.join(R,'data/ui/units/cuman',`#${t}.tga`),d=fs.readFileSync(p);ok(d.readUInt16LE(12)===48&&d.readUInt16LE(14)===64&&d[16]===32,t+' card')}
ok(/^class\s+missile$/m.test(b('camel_wagon'))&&/^stat_ground\s+1, 0, 0, 1$/m.test(b('camel_wagon'))&&/^stat_fire_delay\s+0$/m.test(b('camel_wagon')),'missile camel fort, wagon-specific ground and safe fire delay');
for(const t of ['ghulja_inf','buk_guard'])ok(/^soldier\s+\S+, 30,/m.test(b(t))&&/^formation\s+1.4, 1.8, 2.8, 3.6, 3, square$/m.test(b(t)),t+' skirmisher');
for(const t of ['turkmen_inf','kashgar_inf','kok_inf'])ok(/^soldier\s+\S+, 40,/m.test(b(t)),t+' strength');
for(const t of ['kok_cav','kok_royal_cav','uyghur_camel_cav'])ok(/^soldier\s+\S+, 24,/m.test(b(t)),t+' cavalry strength');
ok(/^soldier\s+kok_rcav, 4,/m.test(b('kok_rcav'))&&/^formation\s+2, 2, 4, 4, 2, square$/m.test(b('kok_rcav'))&&/general_unit/.test(b('kok_rcav')),'command');
ok(/14 MTW2_Musket_SS/.test(mb('kok_inf'))&&!/gunpowder_unit/.test(b('kok_inf')),'Berdan animation');ok(/13 MTW2_CR_Sword[\s\S]*18 MTW2_Sword_Primary/.test(mb('turkmen_inf')),'Turkmen sword mapping');
for(const t of ['merc_tib_noble_cav','tib_militia','merc_tib_inf','tib_horse_archer','tib_roy_inf','tib_tribal_archer','tib_heavy_spear','merc_kashgar_inf'])ok(!/^era\s+[012].*\bcuman\b/m.test(b(t)),t+' custom battle exclusion');
ok(/^stat_cost\s+3, 1200, 400, 100, 100, 1200, 3, 400$/m.test(b('kok_cav')),'Jigit availability');ok(/^stat_cost\s+3, 1100, 367, 100, 100, 1100, 2, 367$/m.test(b('kok_royal_cav')),'Turkmen availability');
for(const t of ['kok_gatling','kok_150mm'])ok(!/^ownership.*\bcuman\b/m.test(b(t))&&!/^era.*\bcuman\b/m.test(b(t)),t+' hidden');
console.log('Turkestan validation passed: D-tier roster, model animations, cards, availability and exclusions.');
