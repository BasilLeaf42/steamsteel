const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p)),txt=p=>read(p).toString('utf8').replace(/\r/g,''),ok=(v,m)=>{if(!v)throw Error(m)};
const edu=txt('data/tow_steamsteel/export_descr_unit.txt'),mirror=txt('data/export_descr_unit.txt'),edb=txt('data/tow_steamsteel/export_descr_buildings.txt'),edbM=txt('data/export_descr_buildings.txt'),model=txt('data/unit_models/battle_models.modeldb');
ok(edu===mirror,'EDU mirrors differ');ok(edb===edbM,'EDB mirrors differ');
function block(t){const m=edu.match(new RegExp(`^type\\s+${t}\\n[\\s\\S]*?(?=^type\\s+|(?![\\s\\S]))`,'m'));if(!m)throw Error('missing '+t);return m[0];}
function mb(t){const a=model.split('\n'),i=a.findIndex(x=>new RegExp(`^${t.length} ${t}\\s*$`).test(x));ok(i>=0,'missing model '+t);let j=i;while(j<a.length&&!/^16 -0\.090000004 /.test(a[j]))j++;return a.slice(i,j+1).join('\n');}
const cav=['csa_state_cavalry_early','csa_state_cavalry_mid','csa_state_cavalry_high'];
const expected=[
  ['early',0,'Maynard Model 1858','rifled_musket_carbine_bullet_c',200,35,'musket_shot_set',1200],
  ['mid',1,'Spencer Model 1865','rifled_musket_carbine_bullet_c',200,40,'musket_shot_set',1200],
  ['high',2,'Winchester Model 1892','magazine_rifle_carbine_bullet_c',240,40,'smokeless_shot_set',1800],
];
for(let i=0;i<cav.length;i++){
  const t=cav[i],b=block(t),e=expected[i];
  ok((edu.match(new RegExp(`^type\\s+${t}$`,'gm'))||[]).length===1,t+' duplicate');
  ok(new RegExp(`^soldier\\s+${t}, 24,`,'m').test(b),t+' soldier');ok(/^category\s+cavalry$/m.test(b)&&/^class\s+missile$/m.test(b),t+' class');
  ok(new RegExp(`^era ${e[1]}\\s+milan$`,'m').test(b),t+' era');ok(b.includes(e[2])&&b.includes(e[3]+', '+e[4]+', '+e[5])&&b.includes(e[6]),t+' named weapon/ballistics');
  ok(/^stat_mental\s+4, low, trained$/m.test(b)&&/^stat_sec\s+4, 3,/m.test(b)&&/^stat_pri_armour\s+4, 2, 0, leather$/m.test(b),t+' Confederate militia modifiers');
  ok(new RegExp(`^stat_cost\\s+3, ${e[7]}, ${Math.round(e[7]/3)}, 100, 100, ${e[7]}, 2, ${Math.round(e[7]/3)}$`,'m').test(b),t+' cost/limit');
  ok(/unit_models\/_Units\/usa\/usa_cav_1g_lod0\.mesh/.test(mb(t))&&/unit_models\/_Units\/csa\/textures\/csa_cav_1g\.texture/.test(mb(t)),t+' native Confederate cavalry visual');
  ok(/unit_sprites\/tmp_cavalry_sprite\.spr/.test(mb(t)),t+' mounted sprite');
}
ok(!/^type\s+csa_state_cavalry$/m.test(edu)&&!model.includes('17 csa_state_cavalry\n'),'stale unsplit cavalry');
ok(/^era 0\s+milan$/m.test(block('csa_virginia_cavalry'))&&!/^era [12]\s+milan$/m.test(block('csa_virginia_cavalry')),'Virginia Cavalry must remain early only');ok(/^stat_pri\s+29, 2, rifled_musket_carbine_bullet_c, 200, 35,/m.test(block('csa_virginia_cavalry'))&&/^stat_cost\s+3, 1200, 400, 100, 100, 1200, 1, 400$/m.test(block('csa_virginia_cavalry')),'Virginia Cavalry early-breechloader baseline');ok(/^stat_pri\s+29, 0, rifled_musket_bullet_a, 260, 35,/m.test(block('csa_sharpshooters'))&&/^stat_cost\s+3, 1400, 467,/m.test(block('csa_sharpshooters')),'Confederate Sharpshooter early-breechloader baseline');
const tiger=block('csa_louisiana_tigers');ok(/^soldier\s+csa_louisiana_tigers, 30,/m.test(tiger)&&/^formation\s+1\.4, 1\.8, 2\.8, 3\.6, 3, square$/m.test(tiger),'Tigers skirmisher strength/formation');
const bearer=mb('csa_standard_bearer');for(const p of ['unit_models/_Units/off/csa_standard_bearer_lod0.mesh','unit_models/_Units/bnw/textures/csa_captain.texture','unit_models/_Units/bnw/textures/csa_standard_flag.texture'])ok(bearer.includes(`${p.length} ${p}`),'bearer mapping '+p);ok(/9 MTW2_Pike/.test(bearer),'bearer animation');
for(const t of cav.concat(['csa_virginia_cavalry','csa_louisiana_tigers','csa_state_guard_mid','csa_state_guard_high'])){const p=path.join(root,'data/ui/units/milan',`#${t}.tga`);ok(fs.existsSync(p),t+' missing card');const b=fs.readFileSync(p);ok(b.readUInt16LE(12)===48&&b.readUInt16LE(14)===64&&b[16]===32,t+' card format');}
const crypto=require('crypto'),cardHashes=cav.map(t=>crypto.createHash('sha256').update(read(`data/ui/units/milan/#${t}.tga`)).digest('hex'));ok(new Set(cardHashes).size===3,'State Cavalry cards must be visually distinct');
const cavalrySources=JSON.parse(txt('tools/historical_card_sources.json'));for(const t of cav){const cr=cavalrySources.find(x=>x.id===t);ok(cr&&cr.status==='card-approved'&&cr.role==='mounted carbine cavalry'&&cr.weapon.includes('carbine')&&cr.source_url&&cr.source_file&&cr.generated_file&&cr.crop_box.length===4,t+' approved carbine card source');for(const p of [cr.source_file,cr.generated_file])ok(fs.existsSync(path.join(root,p)),t+' missing card source '+p);}
const vr=cavalrySources.find(x=>x.id==='csa_virginia_cavalry');ok(vr&&vr.status==='card-approved'&&vr.role==='mounted carbine cavalry'&&vr.weapon.includes('Sharps')&&vr.source_url&&vr.source_file&&vr.generated_file,'Virginia Cavalry approved carbine card source');for(const p of [vr.source_file,vr.generated_file])ok(fs.existsSync(path.join(root,p)),'missing Virginia card source '+p);
const reg=JSON.parse(txt('tools/historical_card_sources.json')),r=reg.find(x=>x.id==='csa_louisiana_tigers');ok(r&&r.status==='card-approved'&&r.pose_source_id==='kneel_aim_waud_1860_65'&&r.source_url&&r.source_file&&r.generated_file&&r.crop_box.length===4,'Tigers source approval');for(const p of [r.source_file,r.generated_file])ok(fs.existsSync(path.join(root,p)),'missing Tigers source '+p);
for(const t of cav){ok(edb.includes(`recruit_pool "${t}"`),t+' EDB recruitment');const loc=read('data/text/export_units.txt').toString('utf16le').replace(/\r/g,'');ok(loc.includes(`{${t}}`)&&loc.includes(`{${t}_descr}`)&&loc.includes(`{${t}_descr_short}`),t+' localization');}
ok(!edb.includes('"csa_state_cavalry"'),'stale cavalry EDB');
const header=+(model.match(/^22 serialization::archive 3 0 0 0 0 (\d+) 0 0 /)||[])[1],heads=[...model.matchAll(/^(\d+) ([^\s;]+)\s*\n\d+ \d+\s*$/gm)].filter(m=>+m[1]===m[2].length);ok(header-heads.length===1,`model count ${header}/${heads.length}`);
console.log(`Confederate validation passed: ${cav.length} State Cavalry periods; modeldb ${header}.`);
