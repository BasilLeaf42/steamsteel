const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const tool=path.join(root,'tools/standardize_union.js');
let source=fs.readFileSync(tool,'utf8');
source=source.replace("limit:1,aux:true}\n];","limit:1,aux:true,axe:true}\n];");
source=source.replace("${E[u.p].label}; ${u.w.name})`","${E[u.p].label}; ${u.w.name}${u.axe?' and tomahawk':''})`");
source=source.replace("piercing, spear, 25, 1.2`,'stat_sec_attr    ap, short_pike'","piercing, ${u.axe?'axe, 25, 1':'spear, 25, 1.2'}`,`stat_sec_attr    ${u.axe?'ap':'ap, short_pike'}`");
source=source.replace("if(infantry.includes(u))fresh=infAnim(fresh,u);else fresh=mounted(fresh);","if(infantry.includes(u))fresh=u.axe?fresh.replace(/(?:18 MTW2_Fast_Musket_3|20 MTW2_Fast_Arquebus_3)(?=\\s)/,'20 MTW2_Fast_Arquebus_3'):infAnim(fresh,u);else fresh=mounted(fresh);");
fs.writeFileSync(tool,source);
for(const rel of ['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt']){const file=path.join(root,rel);let text=fs.readFileSync(file,'utf8');const m=text.match(/^type\s+uni_indian_scouts\r?\n[\s\S]*?(?=^type\s+)/m);if(!m)throw Error('Missing Union Indian Scouts');let block=m[0].replace(/^dictionary\s+.*$/m,'dictionary       uni_indian_scouts ; Indian Scouts (Early; Springfield Model 1855 rifle-musket and tomahawk)').replace(/^stat_sec\s+.*$/m,'stat_sec         3, 2, no, 0, 0, melee, melee_blade, piercing, axe, 25, 1').replace(/^stat_sec_attr\s+.*$/m,'stat_sec_attr    ap');text=text.replace(m[0],block);fs.writeFileSync(file,text);}
function entries(text){const a=text.replace(/\r\n/g,'\n').split('\n'),r=[];let start=1;for(let i=1;i<a.length;i++)if(/^16 -0\.090000004 /.test(a[i])){r.push({lines:a.slice(start,i+1),name:(a[start].match(/^\d+ (\S+)/)||[])[1]});start=i+1;}return r;}
const modelPath=path.join(root,'data/unit_models/battle_models.modeldb');let model=fs.readFileSync(modelPath,'utf8').replace(/\r\n/g,'\n');const donor=entries(model).find(x=>x.name==='apache_inf'),target=entries(model).find(x=>x.name==='uni_indian_scouts');if(!donor||!target)throw Error('Missing scout model');let fresh=donor.lines.join('\n').replace(/^10 apache_inf\s*$/m,'17 uni_indian_scouts ').replace(/18 MTW2_Fast_Musket_3(?=\s)/,'20 MTW2_Fast_Arquebus_3');model=model.replace(target.lines.join('\n'),fresh);fs.writeFileSync(modelPath,model.replace(/\n/g,'\r\n'));
console.log('Preserved the Indian Scouts tomahawk mesh, statistics, and two-handed axe animation mapping.');
