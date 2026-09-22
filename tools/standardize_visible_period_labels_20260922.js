const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),eduPath=path.join(root,'data/tow_steamsteel/export_descr_unit.txt'),locPath=path.join(root,'data/text/export_units.txt');
function read(file){const b=fs.readFileSync(file);return {text:(b[0]===255&&b[1]===254?b.toString('utf16le'):b.toString('utf8')).replace(/^\uFEFF/,''),utf16:b[0]===255&&b[1]===254};}
function write(file,s,text){const b=Buffer.from(text,s.utf16?'utf16le':'utf8');fs.writeFileSync(file,s.utf16?Buffer.concat([Buffer.from([255,254]),b]):b);}
const es=read(eduPath),ls=read(locPath);let edu=es.text,loc=ls.text;const changed=[];
const esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
for(const block of edu.split(/(?=^type\s+)/m)){
 const type=(block.match(/^type\s+(\S+)/m)||[])[1],dict=(block.match(/^dictionary\s+(\S+)/m)||[])[1];if(!type||!dict)continue;
 const sm=type.match(/_(early|mid|high)$/i);if(!sm)continue;const label={early:'Early',mid:'Mid',high:'Late'}[sm[1].toLowerCase()];
 const re=new RegExp('^\\{'+esc(dict)+'\\}([^\\r\\n]*)','m'),m=loc.match(re);if(!m)continue;
 let name=m[1].trim();
 name=name.replace(/\s*\((?:Early|Mid|Late|High|Vroeg|Middel|Laat|Spät)\)\s*$/i,'').trim()+` (${label})`;
 if(name!==m[1].trim()){loc=loc.replace(re,`{${dict}}${name}`);changed.push({type,dict,name});}
}
// Dictionary comments may contain a period marker as metadata; it is always English.
edu=edu.replace(/^(dictionary\s+\S+\s*;[^\r\n]*?)\((?:Vroeg|Middel|Laat|Spät|high)(\s*[;)])/gmi,(all,prefix,tail)=>{
 const typeLine=prefix;let label=/\(Vroeg/i.test(all)?'Early':/\(Middel/i.test(all)?'Mid':'Late';return prefix+`(${label}`+tail;
});
write(locPath,ls,loc);write(eduPath,es,edu);fs.copyFileSync(eduPath,path.join(root,'data/export_descr_unit.txt'));
console.log(JSON.stringify({visibleNamesChanged:changed.length}));
