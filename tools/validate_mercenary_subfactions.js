const fs=require('fs'),path=require('path');
const root=String.raw`C:\Program Files (x86)\Steam\steamapps\common\Medieval II Total War\mods\steamsteel`, ok=(v,m)=>{if(!v)throw Error(m)};
const ep=path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),rp=path.join(root,'data/export_descr_unit.txt');
const edu=fs.readFileSync(ep,'utf8').replace(/\r/g,''),run=fs.readFileSync(rp,'utf8').replace(/\r/g,'');ok(edu===run,'EDU mirrors differ');
const unit=n=>{let p='^type\\s+'+n.replace(/ /g,'\\s+')+'\\s*$[\\s\\S]*?(?=^type\\s+|(?![\\s\\S]))',m=edu.match(new RegExp(p,'m'));ok(m,'missing '+n);return m[0]};
const groups={
 Aceh:{owners:'portugal',units:['merc_aceh_marines','merc_aceh_noble','merc_aceh_reg','merc_aceh_gold','merc_aceh_warband','merc_aceh_inf']},
 Taiping:{owners:'byzantium, slave',units:['merc_tib_temple_guard','taipingguners','taiping_inf','taiping_light','taiping_w']},
 Tibet:{owners:'byzantium, slave',units:['merc_tib_noble_cav','tib_militia','merc_tib_inf','tib_horse_archer','tib_roy_inf','tib_tribal_archer','tib_heavy_spear','mercs_tib_monks']},
 Korea:{owners:'byzantium, saxons, slave',units:['korean_archers','Korean Byeolgigun','Korean Gimagungsu','Korean Musketeers','Korean Pikemen','korean_rifles_mercs','korean_cav_mercs']},
 Japan:{owners:'saxons, slave',units:['Japan Ainu Archers','Japan Ainu Geberu','Japan Ainu Minieru','Japan Ainu Teppo','Japan Heimin Mob','Japan Heimin Partisans','Japan Heimin Partisans Geberu','Japan Heimin Partisans Minieru','Japan Ronin','Japan Teppotai Merc']}}
for(const [g,x] of Object.entries(groups))for(const n of x.units){const b=unit(n);ok(new RegExp('^ownership\\s+'+x.owners.replace(/ /g,'\\s*')+'$','m').test(b),g+' ownership '+n);ok(/^stat_ground\s+0, 0, 0, 0$/m.test(b),g+' terrain '+n);ok(!/hide_improved_forest|hide_anywhere|hide_long_grass|very_hardy|\bhardy\b|move_speed_mod/.test(b),g+' inherited special '+n);const c=b.match(/^stat_cost\s+([^\n]+)/m);ok(c,g+' cost '+n);const f=c[1].split(',').map(s=>s.trim());ok(f[3]==='100'&&f[4]==='100',g+' upgrades '+n);ok(f[2]===f[7],g+' upkeep/penalty '+n)}
const q={
 'merc_aceh_marines':['aceh_marines, 30','rifled_musket_bullet_a, 260','stat_mental      6, disciplined','stat_cost        2, 1400, 467'],
 'merc_aceh_warband':['aceh_warband, 96','stat_pri         3, 2','stat_cost        1, 500, 167'],
 'taiping_light':['taiping_light, 30','formation        1.4, 1.8, 2.8, 3.6','stat_sec         4, 2'],
 'merc_tib_inf':['tib_inf, 40','arquebus_bullet_c, 160','slashing, axe'],
 'mercs_tib_monks':['tib_monks, 80','stat_pri         7, 4','stat_mental      6, impetuous, highly_trained'],
 'Korean Byeolgigun':['Korean_Byeolgigun, 40','rifled_musket_bullet_c, 220','stat_cost        2, 1200, 400'],
 'Korean Musketeers':['Korean_Musketeers, 40','musket_bullet_b, 200','stat_sec         6, 3'],
 'korean_rifles_mercs':['korean_rifles, 40','rifle_bullet_b, 240','Mauser Gewehr 71','stat_cost        2, 1500, 500'],
 'korean_cav_mercs':['korean_cav, 24','class            missile','rifle_carbine_bullet_c, 220','Mauser Karabiner 71'],
 'Japan Ainu Geberu':['Japan_Ainu_Geberu, 30','musket_bullet_b, 240','stat_cost        1, 800, 267'],
 'Japan Ainu Minieru':['Japan_Ainu_Geberu, 30','rifled_musket_bullet_b, 260','stat_cost        1, 1000, 333'],
 'Japan Heimin Mob':['Japan_Heimin_Mob, 96','stat_pri         3, 2'],
 'Japan Ronin':['Japan_Ronin, 80','stat_pri         8, 5','stat_cost        1, 700, 233'],
 'Japan Teppotai Merc':['Japan_Teppotai, 40','musket_bullet_b, 200','stat_sec         8, 5']};
for(const [n,ss] of Object.entries(q)){const b=unit(n);for(const s of ss)ok(b.includes(s),n+' '+s)}
for(const n of groups.Aceh.units){const b=unit(n);ok(!/(ownership|era [012]).*(england|slave)/.test(b),'Aceh leaked '+n)}
for(const n of ['tib_inf','tib_tribal_spear'])ok(!/(ownership|era [012]).*byzantium/.test(unit(n)),'duplicate Tibetan Qing ownership '+n);
const model=fs.readFileSync(path.join(root,'data/unit_models/battle_models.modeldb'),'utf8').replace(/\r/g,'');
for(const [n,anim] of [['aceh_marines','15 MTW2_Musket_SSK'],['korean_rifles','14 MTW2_Musket_SS']]){const i=model.indexOf(n.length+' '+n+' ');ok(i>=0,'model '+n);ok(model.slice(i,i+2500).includes(anim),'animation '+n)}
const backup=path.join(root,'tools/backup_before_remaining_subfactions_20260922/export_units.txt');
function readLoc(p){const b=fs.readFileSync(p);return b.toString(b[0]===255&&b[1]===254?'utf16le':'utf8')}
const oldLoc=readLoc(backup),newLoc=readLoc(path.join(root,'data/text/export_units.txt'));
const keys=['merc_aceh_marines','merc_aceh_noble','merc_aceh_reg','merc_aceh_gold','merc_aceh_warband','merc_aceh_inf','merc_tib_temple_guard','taipingguners','taiping_inf','taiping_light','taiping_w','tib_temple_guard','merc_tib_noble_cav','tib_militia','merc_tib_inf','tib_horse_archer','tib_roy_inf','tib_tribal_archer','tib_heavy_spear','mercs_tib_monks','korean_archers','Korean_Byeolgigun','Korean_Gimagungsu','Korean_Musketeers','Korean_Pikemen','korean_rifles_mercs','korean_cav_mercs','Japan_Ainu_Archers','Japan_Ainu_Geberu','Japan_Ainu_Minieru','Japan_Ainu_Teppo','Japan_Heimin_Mob','Japan_Heimin_Partisans','Japan_Heimin_Partisans_Geberu','Japan_Heimin_Partisans_Minieru','Japan_Ronin','Japan_Teppotai_Merc'];
for(const k of keys){const re=new RegExp('^\\{'+k+'_descr\\}[^\\r\\n]*','m'),a=oldLoc.match(re),b=newLoc.match(re);ok(a&&b&&a[0]===b[0],'full description changed '+k)}
const cards={portugal:groups.Aceh.units,byzantium:[...groups.Taiping.units,'tib_temple_guard',...groups.Tibet.units,...groups.Korea.units]};
for(const [f,ns] of Object.entries(cards))for(const n of ns){const card=n.startsWith('Korean ')?n.replace(' ','_'):n;ok(fs.existsSync(path.join(root,'data/ui/units',f,'#'+card+'.tga')),'card '+f+' '+card);}
console.log('Remaining subfactions validation passed: 6 Aceh, 5 Taiping, 8 Tibet, 7 Korea, 10 Ainu/Japanese irregular records.');
