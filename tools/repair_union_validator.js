const fs=require('fs'),path=require('path');
const file=path.resolve(__dirname,'validate_union.js');
let text=fs.readFileSync(file,'utf8');
text=text.replace('\n+const header=+(','\nconst header=+(');
fs.writeFileSync(file,text);
console.log('Repaired the validator insertion marker.');
