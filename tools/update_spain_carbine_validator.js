const fs=require('fs'),path=require('path');
const p=path.join(__dirname,'validate_spain.js');let s=fs.readFileSync(p,'utf8');
const a="ok(/^class\\s+light$/m.test(b)&&/_carbine_bullet_c,/m.test(b)";
const b="ok(/^class\\s+missile$/m.test(b)&&/_carbine_bullet_c,/m.test(b)";
if(!s.includes(a))throw Error('Spain carbine validation pattern missing');
fs.writeFileSync(p,s.replace(a,b));
console.log('Updated Spain carbine validator to require class missile.');
