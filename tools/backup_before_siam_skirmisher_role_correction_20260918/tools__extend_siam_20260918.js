const fs=require('fs'),P=require('path'),R=P.resolve(__dirname,'..');const paths=[P.join(R,'data/tow_steamsteel/export_descr_unit.txt'),P.join(R,'data/export_descr_unit.txt')],B=P.join(R,'tools/backup_before_siam_extension_20260918');fs.mkdirSync(B,{recursive:true});for(const p of paths){let q=P.join(B,P.basename(P.dirname(p))+'_'+P.basename(p));if(!fs.existsSync(q))fs.copyFileSync(p,q)}
let e=fs.readFileSync(paths[0],'utf8').replace(/\r/g,'');function block(t){let m=e.match(new RegExp(`^type\\s+${t}\\n[\\s\\S]*?(?=^type\\s+|(?![\\s\\S]))`,'m'));if(!m)throw Error('missing '+t);return m[0].trimEnd()}function rep(t,x){e=e.replace(block(t),x.trimEnd())}
let g=block('Siam_bodyguard').replace(/^stat_pri_armour.*$/m,'stat_pri_armour  7, 4, 0, metal');rep('Siam_bodyguard',g);
let s=block('siam_sea').replace(/^soldier.*$/m,'soldier          siam_sea, 30, 0, 1.2').replace(/^attributes.*$/m,'attributes       free_upkeep_unit, sea_faring, hide_forest, gunmen').replace(/^formation.*$/m,'formation        1.4, 1.8, 2.8, 3.6, 3, square').replace(/^stat_pri.*$/m,'stat_pri         37, 0, rifle_bullet_b, 280, 35, missile, missile_gunpowder, piercing, none, musket_shot_set, 0, -999');rep('siam_sea',s);
const cav=`type             siam_sword_cav
dictionary       siam_sword_cav ; Thahan Ma Krabi
category         cavalry
class            light
voice_type       Heavy
accent           middle_east
banner faction   main_cavalry
banner holy      crusade_cavalry
soldier          siam_sword_cav, 24, 0, 1
mount            hussar
mount_effect     elephant -4, camel -4
attributes       free_upkeep_unit, sea_faring, hide_forest, can_withdraw
formation        2, 2, 4, 4, 3, square
stat_health      1, 0
stat_pri         4, 3, no, 0, 0, melee, melee_blade, slashing, sword, 25, 1
stat_pri_attr    no
stat_sec         0, 0, no, 0, 0, no, melee_simple, blunt, none, 25, 1
stat_sec_attr    no
stat_pri_armour  4, 3, 0, leather
stat_sec_armour  0, 0, flesh
stat_heat        2
stat_ground      0, 0, 0, 0
stat_mental      3, low, trained
stat_charge_dist 50
stat_fire_delay  0
stat_food        60, 300
stat_cost        2, 1000, 333, 100, 100, 1000, 2, 333
ownership        cru, slave
era 0            cru, slave
era 1            cru, slave`;
if(/^type\s+siam_sword_cav$/m.test(e))rep('siam_sword_cav',cav);else e=e.replace(block('siam_late_cav'),cav+'\n\n'+block('siam_late_cav'));e=e.replace(/\n/g,'\r\n');for(const p of paths)fs.writeFileSync(p,e);
let mp=P.join(R,'data/unit_models/battle_models.modeldb'),m=fs.readFileSync(mp,'utf8');function mb(n){let x=m.match(new RegExp(`^${n.length} ${n}\\s*$[\\s\\S]*?(?=^\\d+ [^\\s;]+\\s*$\\r?\\n\\d+ \\d+\\s*$|(?![\\s\\S]))`,'m'));if(!x)throw Error('model '+n);return x[0]}let z=mb('siam_sea').replace('14 MTW2_Musket_SS','15 MTW2_Musket_SSK');m=m.replace(mb('siam_sea'),z);fs.writeFileSync(mp,m);
let lp=P.join(R,'data/text/export_units.txt'),buf=fs.readFileSync(lp),bom=buf[0]===255&&buf[1]===254,l=buf.subarray(bom?2:0).toString('utf16le');for(const [k,v] of Object.entries({siam_sword_cav:'Thahan Ma Krabi',siam_sea:'Thahan Ruea'})){let row=`{${k}}${v}`;if(new RegExp(`\\{${k}\\}`).test(l))l=l.replace(new RegExp(`\\{${k}\\}[^\\r\\n]*`),row);else l+=`\r\n${row}\r\n{${k}_descr}${v}.\r\n{${k}_descr_short}${v}.\r\n`}fs.writeFileSync(lp,Buffer.concat([Buffer.from([255,254]),Buffer.from(l,'utf16le')]));console.log('Extended Siam: cuirassier general armour, naval skirmisher, sword cavalry.');