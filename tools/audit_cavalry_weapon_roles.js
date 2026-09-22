const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const edu=fs.readFileSync(path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),'utf8').replace(/\r/g,'');
const starts=[...edu.matchAll(/^type\s+(\S+)/gm)];
for(let i=0;i<starts.length;i++){
  const type=starts[i][1],b=edu.slice(starts[i].index,i+1<starts.length?starts[i+1].index:edu.length);
  if(!/^category\s+cavalry$/m.test(b))continue;
  const cls=(b.match(/^class\s+(\S+)/m)||[])[1];
  const dict=(b.match(/^dictionary\s+(.+)$/m)||[])[1]||'';
  const pri=(b.match(/^stat_pri\s+(.+)$/m)||[])[1]||'';
  const kind=/_carbine_bullet_/.test(pri)?'CARBINE':/^20, 4, magazine_rifle_bullet_c, 60, 15,/.test(pri)?'PISTOL':'';
  if(kind)console.log([kind,type,cls,dict,pri].join('\t'));
}
