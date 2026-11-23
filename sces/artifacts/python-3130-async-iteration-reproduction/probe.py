import dis
import json
import sys

assert sys.version_info[:3] == (3, 13, 0)
assert sys.implementation.name == "cpython"

events = []
class Pause:
    def __await__(self):
        yield "suspended"
        return None

class Iterator:
    def __init__(self, fail=None):
        self.index = 0
        self.fail = fail

    def __aiter__(self):
        if self.fail == "aiter":
            raise StopAsyncIteration("aiter")
        return self

    async def __anext__(self):
        self.index += 1
        await Pause()
        if self.fail == "other":
            raise ValueError("anext")
        if self.index == 2:
            raise StopAsyncIteration("awaited anext")
        return 42

class Target:
    def __init__(self, fail=False):
        self.fail = fail

    @property
    def value(self):
        return self.last

    @value.setter
    def value(self, value):
        if self.fail:
            raise StopAsyncIteration("target setter")
        self.last = value

async def consume(iterator, target, fail_body=False):
    async for target.value in iterator:
        events.append(["body", target.value])
        if fail_body:
            raise StopAsyncIteration("body")
    else:
        events.append(["else", None])

def observe(iterator, target, body=False):
    events.clear()
    operations = 0
    coroutine = consume(iterator, target, body)
    while True:
        try:
            marker = coroutine.send(None)
            assert marker == "suspended"
            operations += 1
        except StopIteration:
            return {"outcome": "completed", "events": list(events), "suspensions": operations}
        except (StopAsyncIteration, ValueError) as caught:
            return {"outcome": type(caught).__name__, "message": str(caught),
                    "events": list(events), "suspensions": operations}

tests = {
    "awaited_anext_exhaustion": observe(Iterator(), Target()),
    "target_assignment_exception": observe(Iterator(), Target(fail=True)),
    "loop_body_exception": observe(Iterator(), Target(), body=True),
    "different_anext_exception": observe(Iterator("other"), Target()),
    "aiter_exception": observe(Iterator("aiter"), Target()),
}
assert tests["awaited_anext_exhaustion"] == {
    "outcome": "completed", "events": [["body", 42], ["else", None]], "suspensions": 2}
assert tests["target_assignment_exception"] == {
    "outcome": "StopAsyncIteration", "message": "target setter", "events": [], "suspensions": 1}
assert tests["loop_body_exception"] == {
    "outcome": "StopAsyncIteration", "message": "body", "events": [["body", 42]], "suspensions": 1}
assert tests["different_anext_exception"] == {
    "outcome": "ValueError", "message": "anext", "events": [], "suspensions": 1}
assert tests["aiter_exception"] == {
    "outcome": "StopAsyncIteration", "message": "aiter", "events": [], "suspensions": 0}

instructions = {instr.opname: instr.offset for instr in dis.get_instructions(consume)
                if instr.opname in {"GET_ANEXT", "STORE_ATTR", "END_ASYNC_FOR"}}
assert set(instructions) == {"GET_ANEXT", "STORE_ATTR", "END_ASYNC_FOR"}
handlers = [entry for entry in dis.Bytecode(consume).exception_entries if entry.target == instructions["END_ASYNC_FOR"]]
assert any(entry.start <= instructions["GET_ANEXT"] < entry.end for entry in handlers)
assert not any(entry.start <= instructions["STORE_ATTR"] < entry.end for entry in handlers)
print(json.dumps({"cpython": sys.version, "tests": tests, "instruction_offsets": instructions,
                  "end_async_for_handlers": [entry._asdict() for entry in handlers]}, sort_keys=True))

