const fs=require('fs'),path=require('path');
const R=path.resolve(__dirname,'..'),B=path.join(R,'tools/backup_before_siam_bearer_removal_and_cav_donor_20260918');fs.mkdirSync(B,{recursive:true});
const files=['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt','data/unit_models/battle_models.modeldb','tools/extend_siam_20260918.js','tools/validate_siam.js','AGENTS.md'];
for(const f of files){const p=path.join(R,f);fs.copyFileSync(p,path.join(B,f.replace(/[\\/]/g,'__')))}
for(const f of files.slice(0,2)){const p=path.join(R,f);let s=fs.readFileSync(p,'utf8');s=s.replace(/^officer\s+siam_standard_bearer\s*\r?\n/gm,'');fs.writeFileSync(p,s)}
const mp=path.join(R,'data/unit_models/battle_models.modeldb');let m=fs.readFileSync(mp,'utf8');
const bs=m.search(/^20 siam_standard_bearer\s*$/m);if(bs>=0){const te=m.indexOf('16 -0.090000004 0 0 -0.34999999 0.80000001 0.60000002',bs),be=m.indexOf('\n',te)+1;if(te<0||be<1)throw Error('bearer block end');m=m.slice(0,bs)+m.slice(be);m=m.replace(/^(22 serialization::archive 3 0 0 0 0 )(\d+)( 0 0 )/m,(_,a,n,z)=>a+(+n-1)+z)}
const cs=m.search(/^14 siam_sword_cav\s*$/m),ct=m.indexOf('16 -0.090000004 0 0 -0.34999999 0.80000001 0.60000002',cs),ce=m.indexOf('\n',ct)+1;if(cs<0||ct<0)throw Error('sword cav block');let cb=m.slice(cs,ce);
cb=cb.split('unit_models/_Units/fra/textures/fra_cav_1g.texture').join('unit_models/_Units/sia/textures/sia_col_2g.texture');
cb=cb.replaceAll('50 unit_models/_Units/sia/textures/sia_col_2g.texture','50 unit_models/_Units/sia/textures/sia_col_2g.texture');
m=m.slice(0,cs)+cb+m.slice(ce);fs.writeFileSync(mp,m);
let e=fs.readFileSync(path.join(R,'tools/extend_siam_20260918.js'),'utf8');e=e.replace(/\.replace\(\/\^officer.*siam_standard_bearer[^\n]+\n?/g,'');fs.writeFileSync(path.join(R,'tools/extend_siam_20260918.js'),e);
let v=fs.readFileSync(path.join(R,'tools/validate_siam.js'),'utf8');v=v.replace(/for\(const t of \['siam_agent','Siam_Archers','siam_inf'\]\)ok\(unit\(t\)\.includes\('officer          siam_standard_bearer'\),t\+' visible standard bearer'\);/,'for(const t of [\'siam_agent\',\'Siam_Archers\',\'siam_inf\'])ok(!unit(t).includes(\'siam_standard_bearer\'),t+\' bearer removed\');');fs.writeFileSync(path.join(R,'tools/validate_siam.js'),v);
let a=fs.readFileSync(path.join(R,'AGENTS.md'),'utf8');a=a.replace(/ `siam_standard_bearer` is the verified[\s\S]*?Never restore `officer siam_inf`; that record visibly carries a rifle\./,' Siam has no standard-bearer officer: the attempted custom bearer was rejected and removed. Do not restore `siam_standard_bearer` or substitute an armed infantry model.');a=a.replace('derived from the genuine mounted `Siam_bodyguard` rider mesh','derived from the genuine unarmoured mounted `sia_col_2g_lod0.mesh` rider');fs.writeFileSync(path.join(R,'AGENTS.md'),a);
console.log('Removed Siam bearer references/model and remapped early cavalry textures to unarmoured Siam donor.');
