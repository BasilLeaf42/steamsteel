const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
for(const rel of ['data/tow_steamsteel/export_descr_unit.txt','data/export_descr_unit.txt']){
  const file=path.join(root,rel);
  let changed=0;
  let text=fs.readFileSync(file,'utf8').replace(/\r\n/g,'\n');
  text=text.split(/(?=^type\s+)/m).map(block=>{
    if(/^attributes\s+.*\bgeneral_unit\b/m.test(block)&&/^soldier\s+\S+,\s*4,/m.test(block)&&/^category\s+cavalry$/m.test(block)){
      const fresh=block.replace(/^class\s+\S+$/m,'class            light');
      if(fresh!==block)changed++;
      return fresh;
    }
    return block;
  }).join('');
  fs.writeFileSync(file,text.replace(/\n/g,'\r\n'));
  console.log(`${rel}: normalized ${changed} four-man general records to class light`);
}
