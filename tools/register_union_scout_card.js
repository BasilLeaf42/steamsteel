const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const registryPath = path.join(__dirname, 'historical_card_sources.json');
const records = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
const record = {
  id: 'uni_indian_scout_cavalry',
  group_id: 'union_indian_scout_cavalry_20260913',
  unit_type: 'uni_indian_scout_cavalry',
  card_file: 'data/ui/units/portugala/#uni_indian_scout_cavalry.tga',
  faction: 'portugala',
  name: 'Indian Scout Cavalry (Colt Revolver and spear)',
  role: 'pistol cavalry / frontier scout',
  weapon: 'Colt-type revolver and spear',
  source_url: 'https://www.loc.gov/item/89714480/',
  source_file: 'tools/historical_card_refs/uni_indian_scout_cavalry_remington_1886.jpg',
  source_title: "The Apache war—Indian scouts on Geronimo's trail",
  creator: 'Frederic Remington',
  source_date: '1886-01-09',
  licence: 'Library of Congress: no known restrictions on publication',
  depicted_subject: 'Apache military reconnaissance during the Geronimo campaign',
  mapping_note: 'Remington controls the mounted-on-trail relationship and period equipment. The Library of Congress Loco Jim portrait (https://www.loc.gov/item/2007678555/) is the secondary appearance reference. Final equipment follows the loaded usa_nat_1g rider mesh, whose active named groups and modeldb mapping support pistol primary and spear secondary. The generated figure is close-mounted framing on the canonical parchment field.',
  pose_source_id: '',
  status: 'approved',
  generated_file: 'tools/card_generation_sources/uni_indian_scout_cavalry_master.png',
  crop_box: [0, 0, 1086, 1448]
};
const index = records.findIndex(x => x.id === record.id);
if (index >= 0) records[index] = record; else records.push(record);
fs.writeFileSync(registryPath, JSON.stringify(records, null, 2) + '\n');

const stdPath = path.join(__dirname, 'standardize_union.js');
let std = fs.readFileSync(stdPath, 'utf8');
const oldCopy = "for(const u of all)fs.copyFileSync(path.join(cards,`#${u.card}.tga`),path.join(cards,`#${u.type}.tga`));";
const newCopy = "for(const u of all)if(u.type!=='uni_indian_scout_cavalry')fs.copyFileSync(path.join(cards,`#${u.card}.tga`),path.join(cards,`#${u.type}.tga`));";
if (std.includes(oldCopy)) std = std.replace(oldCopy, newCopy);
else if (!std.includes(newCopy)) throw new Error('Union card-copy loop changed unexpectedly');
fs.writeFileSync(stdPath, std);

const valPath = path.join(__dirname, 'validate_union.js');
let val = fs.readFileSync(valPath, 'utf8');
const needle = "const header=+(model.match(";
const check = "{const registry=JSON.parse(txt('tools/historical_card_sources.json'));const r=registry.find(x=>x.id==='uni_indian_scout_cavalry');ok(r&&r.status==='approved'&&r.source_url&&r.source_file&&r.generated_file&&r.crop_box.length===4,'Indian Scout Cavalry approved source mapping');for(const p of [r.source_file,r.generated_file])ok(fs.existsSync(path.join(root,p)),'missing Scout card source '+p);}\n";
if (!val.includes(check)) {
  if (!val.includes(needle)) throw new Error('Union validator insertion point missing');
  val = val.replace(needle, check + needle);
}
fs.writeFileSync(valPath, val);
console.log('Registered approved Union Indian Scout Cavalry card sources.');
