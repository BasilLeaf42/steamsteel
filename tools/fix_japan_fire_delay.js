const fs=require('fs'),path=require('path'),R=path.resolve(__dirname,'..');
for(const rel of ['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt']){const p=path.join(R,rel);let s=fs.readFileSync(p,'utf8').replace(/\r/g,'');s=s.split(/(?=^type\s+)/m).map(b=>/(?:^ownership|^era [012]).*\bsaxons\b/m.test(b)?b.replace(/^stat_fire_delay\s+.*$/gm,'stat_fire_delay  0'):b).join('');fs.writeFileSync(p,s.replace(/\n/g,'\r\n'))}
console.log('Cleared Japanese firing delays to zero.');
