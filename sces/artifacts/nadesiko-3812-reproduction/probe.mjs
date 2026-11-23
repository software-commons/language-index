import assert from 'node:assert/strict';
import { checkNakoMode } from './native/modules/nako_prepare.mjs';
import indent from './native/modules/nako_indent.mjs';

const marker = '!M';
const markerInputs = [
  ['exact trimmed segment', '  !M  ', true],
  ['partial segment', 'abc!M', false],
  ['256th code unit', 'x'.repeat(253) + ';!M', true],
  ['257th code unit', 'x'.repeat(254) + ';!M', false],
  ['supplementary characters measured as two code units', '😀'.repeat(127) + ';!M', false],
  ['30th segment', 'x;'.repeat(29) + '!M', true],
  ['31st segment', 'x;'.repeat(30) + '!M', false],
  ['Japanese full stop delimiter', 'x。!M', true],
  ['newline delimiter', 'x\n!M', true],
  ['fullwidth exclamation normalization', '！M', true],
  ['light bulb normalization', '💡M', true],
  ['first marker normalization only', '！x;！M', false],
  ['single-line block comment removal', '/*x*/!M', true],
  ['multiline comment exclusion from the regex', '/*\nx*/!M', false],
];
const results = markerInputs.map(([test, input, expected]) => {
  const actual = checkNakoMode(input, [marker]);
  assert.equal(actual, expected, test);
  return { test, expected, actual, utf16_length: input.length };
});
const inactive = 'ここまで # explicit ordinary close\n';
assert.deepEqual(indent.convert(inactive), { code: inactive, insertedLines: [], deletedLines: [] });
results.push({ test: 'unchanged path without recognized directive', actual: true });
for (const keyword of ['!インデント構文', '!ここまでだるい']) {
  assert.equal(indent.isIndentSyntaxEnabled(keyword), true);
  const filteredClose = keyword + '\n　ここまで # explanation';
  assert.throws(() => indent.convert(filteredClose), /ここまで/);
  results.push({ test: 'recognized directive and filtered terminator rejection', keyword, actual: true });
}
console.log(JSON.stringify({ engine: process.version, results }, null, 2));

