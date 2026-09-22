const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const backup = path.join(root, 'tools/backup_before_boer_cowboy_laager_raise_20260916/battle_models.modeldb');
const target = path.join(root, 'data/unit_models/battle_models.modeldb');
let text = fs.readFileSync(backup, 'utf8');

function headers(s) {
  const out = [];
  const re = /^(\d+) ([^\s;]+)\s*\r?\n\d+ \d+\s*$/gm;
  for (const m of s.matchAll(re)) if (+m[1] === m[2].length) out.push({name:m[2], start:m.index});
  return out;
}

const entry = name => [
  `${name.length} ${name}`,
  '1 4',
  ...Array(4).fill('43 unit_models/_Units/bnw/usa_cowboy_lod0.mesh 20000'),
  '2',
  '3 teu',
  '46 unit_models/_Units/bnw/textures/cowboy.texture',
  '48 unit_models/_Units/bnw/textures/cowboy_n.texture',
  '35 unit_sprites/tmp_cavalry_sprite.spr',
  '5 slave',
  '46 unit_models/_Units/bnw/textures/cowboy.texture',
  '48 unit_models/_Units/bnw/textures/cowboy_n.texture',
  '35 unit_sprites/tmp_cavalry_sprite.spr',
  '2',
  '3 teu',
  '47 unit_models/_Units/bnw/textures/cowboy2.texture',
  '49 unit_models/_Units/bnw/textures/cowboy2_n.texture 0',
  '5 slave',
  '47 unit_models/_Units/bnw/textures/cowboy2.texture',
  '49 unit_models/_Units/bnw/textures/cowboy2_n.texture 0',
  '1',
  '5 Horse',
  '16 MTW2_CR_Arquebus 13 MTW2_CR_Sword',
  '1',
  '24 MTW2_HR_Arquebus_Primary',
  '1',
  '18 MTW2_Sword_Primary',
  '16 -0.090000004 0 0 -0.34999999 0.80000001 0.60000002',
  ''
].join('\r\n');

for (const name of ['boer_mounted_kommando_early','boer_mounted_kommando_mid','boer_mounted_kommando_high']) {
  const hs = headers(text);
  const i = hs.findIndex(h => h.name === name);
  if (i < 0) throw new Error(`missing ${name}`);
  const end = i + 1 < hs.length ? hs[i+1].start : text.length;
  text = text.slice(0, hs[i].start) + entry(name) + text.slice(end);
}

fs.writeFileSync(target, text, 'utf8');
console.log('Restored backup and safely installed clean Cowboy model entries.');
