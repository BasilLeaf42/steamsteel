const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const eduPaths=['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt'].map(p=>path.join(root,p));
const bearerTypes=new Set([
  'ita_line_early','ita_line_mid','ita_milizia_early','ita_milizia_mid',
  'ita_granatieri_early','ita_granatieri_mid','ita_bersaglieri_early','ita_bersaglieri_mid',
  'ita_alpini_mid','ita_marina_early','ita_marina_mid','ita_zappatori_early',
  'ita_zappatori_mid','ita_garibaldini_early'
]);
for(const file of eduPaths){
  let text=fs.readFileSync(file,'utf8').replace(/\r\n/g,'\n');
  text=text.split(/(?=^type\s+)/m).map(block=>{
    const m=block.match(/^type\s+([^\s;]+)/m);if(!m)return block;
    const type=m[1];
    block=block.replace(/\n(?:officer\s+russia_qi\n)+/g,'\n');
    if(bearerTypes.has(type))block=block.replace('officer          shk_off_1g\n','officer          shk_off_1g\nofficer          russia_qi\n');
    if(type==='ita_general_staff')block=block.replace(/^class\s+heavy$/m,'class            light');
    return block;
  }).join('');
  fs.writeFileSync(file,text.replace(/\n/g,'\r\n'));
}

const modelPath=path.join(root,'data/unit_models/battle_models.modeldb');
let model=fs.readFileSync(modelPath,'utf8').replace(/\r\n/g,'\n');
function entry(name){const lines=model.split('\n'),i=lines.findIndex(x=>new RegExp(`^${name.length} ${name}\\s*$`).test(x));if(i<0)throw Error(`Missing ${name}`);let j=i;while(j<lines.length&&!/^16 -0\.090000004 /.test(lines[j]))j++;return lines.slice(i,j+1).join('\n');}
function setVisual(name,to){const old=entry(name);let fresh=old.replaceAll(/koi_(?:crb|pis)_1g_lod0\.mesh/g,`koi_${to}_1g_lod0.mesh`).replaceAll(/koi_(?:crb|pis)_1g\.texture/g,`koi_${to}_1g.texture`).replace(/^\d+ unit_sprites\/(?:milan_Dummy_EN_Spearmen_ug1|england_Feudal_Knights|tmp_cavalry)_sprite\.spr\s*$/gm,'35 unit_sprites/tmp_cavalry_sprite.spr ');if(fresh===old)return;model=model.replace(old,fresh);}
setVisual('ita_cavalleggeri','pis');
for(const name of ['ita_carabinieri_early','ita_carabinieri_mid','ita_carabinieri_high'])setVisual(name,'crb');
fs.writeFileSync(modelPath,model.replace(/\n/g,'\r\n'));
console.log('Applied Italian bearers, light general class, pistol Cavalleggeri, and carbine-model Carabinieri with mounted sprites.');
