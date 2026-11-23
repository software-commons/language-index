const assert = require('node:assert/strict');
const { createHash } = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const preamble = [0, 97, 115, 109, 1, 0, 0, 0];
const custom = [0, 2, 1, 120];
const noTypes = [1, 1, 0];
const noImports = [2, 1, 0];

function unsignedLeb128(value) {
  const bytes = [];
  do {
    const low = value % 128;
    value = Math.floor(value / 128);
    bytes.push(low | (value ? 128 : 0));
  } while (value);
  return bytes;
}

function section(id, data) {
  return [id, ...unsignedLeb128(data.length), ...data];
}

function memoryType(minimum, maximum) {
  return maximum === undefined
    ? [0, ...unsignedLeb128(minimum)]
    : [1, ...unsignedLeb128(minimum), ...unsignedLeb128(maximum)];
}

function memoryModule(minimum, maximum) {
  return [...preamble, ...section(5, [1, ...memoryType(minimum, maximum)])];
}

function fnModule(paramTypes, resultTypes, instructions, limits) {
  const type = [1, 0x60, paramTypes.length, ...paramTypes, resultTypes.length, ...resultTypes];
  const func = [1, 0];
  const exports = limits ? [2, 1, 102, 0, 0, 1, 109, 2, 0] : [1, 1, 102, 0, 0];
  const body = [0, ...instructions, 0x0b];
  return [...preamble, ...section(1, type), ...section(3, func),
    ...(limits ? section(5, [1, ...memoryType(...limits)]) : []),
    ...section(7, exports), ...section(10, [1, ...unsignedLeb128(body.length), ...body])];
}

function digest(bytes) {
  return createHash('sha256').update(Uint8Array.from(bytes)).digest('hex');
}

function validity(bytes) {
  return { bytes_sha256: digest(bytes), valid: WebAssembly.validate(Uint8Array.from(bytes)) };
}

const i32 = 0x7f;
const i64 = 0x7e;
const binary = {
  empty: validity(preamble),
  custom_sections_interspersed: validity([...preamble, ...custom, ...noTypes, ...custom, ...noImports, ...custom]),
  wrong_version: validity([...preamble.slice(0, 4), 2, 0, 0, 0]),
  repeated_type_section: validity([...preamble, ...noTypes, ...noTypes]),
  out_of_order: validity([...preamble, ...noImports, ...noTypes]),
  invalid_start_reference: validity([...preamble, 8, 1, 0]),
};
assert(binary.empty.valid && binary.custom_sections_interspersed.valid);
assert(!binary.wrong_version.valid && !binary.repeated_type_section.valid && !binary.out_of_order.valid);
assert(!binary.invalid_start_reference.valid);

const selector = fnModule([i32, i32, i32], [i32], [0x20, 0, 0x20, 1, 0x20, 2, 0x1b]);
const mismatched = fnModule([i32, i64, i32], [i32], [0x20, 0, 0x20, 1, 0x20, 2, 0x1b]);
const select = new WebAssembly.Instance(new WebAssembly.Module(Uint8Array.from(selector))).exports.f;
const selection = { bytes_sha256: digest(selector), zero: select(17, 29, 0),
  nonzero: select(17, 29, 1), negative: select(17, 29, -1), mismatched_operands: validity(mismatched) };
assert.deepEqual([selection.zero, selection.nonzero, selection.negative], [29, 17, 17]);
assert(!selection.mismatched_operands.valid);

const memory = { at_limit: validity(memoryModule(65536, 65536)),
  over_limit: validity(memoryModule(65537, 65537)), reversed: validity(memoryModule(2, 1)),
  without_maximum: validity(memoryModule(1)) };
assert(memory.at_limit.valid && memory.without_maximum.valid);
assert(!memory.over_limit.valid && !memory.reversed.valid);

const loadBytes = fnModule([i32], [i32], [0x20, 0, 0x28, 2, 2], [1, 1]);
const load = new WebAssembly.Instance(new WebAssembly.Module(Uint8Array.from(loadBytes))).exports;
new Uint8Array(load.m.buffer).set([0x12, 0x34, 0x56, 0x78], 65532);
function callLoad(address) {
  try {
    return { return_value: load.f(address) };
  } catch (error) {
    assert(error instanceof WebAssembly.RuntimeError);
    return { trap: true };
  }
}
const loadObservations = { bytes_sha256: digest(loadBytes), memory_bytes: load.m.buffer.byteLength,
  exactly_in_bounds: callLoad(65530), one_past_end: callLoad(65531), offset_does_not_wrap: callLoad(-1) };
assert.equal(loadObservations.exactly_in_bounds.return_value, 0x78563412);
assert(loadObservations.one_past_end.trap && loadObservations.offset_does_not_wrap.trap);

const growBytes = fnModule([i32], [i32], [0x20, 0, 0x40, 0], [1, 2]);
const grow = new WebAssembly.Instance(new WebAssembly.Module(Uint8Array.from(growBytes))).exports;
const growth = { bytes_sha256: digest(growBytes), start_bytes: grow.m.buffer.byteLength,
  at_zero_delta: grow.f(0), grows_to_maximum: grow.f(1), exceeds_maximum: grow.f(1),
  unsigned_large_delta: grow.f(-1), end_bytes: grow.m.buffer.byteLength };
assert.deepEqual([growth.at_zero_delta, growth.grows_to_maximum, growth.exceeds_maximum, growth.unsigned_large_delta], [1, 1, -1, -1]);
assert.equal(growth.start_bytes, 65536);
assert.equal(growth.end_bytes, 131072);

const results = { node: process.version, v8: process.versions.v8, binary, selection, memory, load: loadObservations, growth,
  limits: 'Current engine context for independently constructed small cases. Only the dated recommendation governs the exact clauses. No resource-induced in-range failure was forced.' };
fs.writeFileSync(path.join(__dirname, 'challenge-results.json'), JSON.stringify(results, null, 2) + '\n');
console.log('Verified independent binary, select, limits, load and grow challenges', process.version, process.versions.v8);
