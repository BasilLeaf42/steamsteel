const fs = require('fs');

const files = [
  'data/text/export_units.txt',
];

// A previous normalizer repeatedly prepended its complete standardized clause.
// Collapse only byte-identical leading clauses; preserve unique trailing prose.
const leadingClause = /^([^\r\n]*?\([^\r\n]*?\))(?:,\s*\1)+(?=,|\.|$)/;
let changed = 0;
const repaired = [];

for (const file of files) {
  let text = fs.readFileSync(file, 'utf8');
  text = text.replace(/^\{([^}\r\n]+_descr_short)\}([^\r\n]*)/gm, (line, key, value) => {
    let next = value;
    let previous;
    do {
      previous = next;
      next = next.replace(leadingClause, '$1');
    } while (next !== previous);
    // Also remove an older, less-specific weapon tuple for the same unit when
    // it immediately follows the standardized family/model tuple.
    const standardized = next.match(/^(.+?)\s+\(([^,()]+),\s*(.+)\),\s*\1\s+\((.+)\)([.,]?)$/);
    if (standardized) next = `${standardized[1]} (${standardized[2]}, ${standardized[3]})${standardized[5] || ''}`;
    if (next !== value) {
      changed++;
      repaired.push(key);
    }
    return `{${key}}${next}`;
  });
  fs.writeFileSync(file, text, 'utf8');
}

fs.writeFileSync(
  'tools/short_description_duplication_fix_20260923.json',
  JSON.stringify({ changed, repaired }, null, 2) + '\n',
  'utf8'
);
console.log(JSON.stringify({ changed, repaired }));
