"""Local boundary probes for Python 3.13 language-reference statements."""

import gc
import importlib.abc
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import platform
import sys
import sysconfig
from tempfile import TemporaryDirectory
import tokenize
import typing
import weakref


def indentation():
    sample = 'if True:\n    body = (\n          42\n    )\n\n    # comment\n    if body:\n        pass\n'
    tokens = [(tokenize.tok_name[token.type], token.start[0])
              for token in tokenize.generate_tokens(io.StringIO(sample).readline)
              if token.type in (tokenize.INDENT, tokenize.DEDENT)]
    assert tokens == [("INDENT", 2), ("INDENT", 8), ("DEDENT", 9), ("DEDENT", 9)]
    return tokens


def blocks_and_frames():
    names = []
    filename = "<block-frame-probe>"

    def profile(frame, event, arg):
        if event == "call" and frame.f_code.co_filename == filename:
            names.append(frame.f_code.co_name)

    sys.setprofile(profile)
    try:
        exec(compile("class Probe: pass\ndef worker(): pass\nworker()", filename, "exec"), {})
    finally:
        sys.setprofile(None)
    assert names == ["<module>", "Probe", "worker"]
    return names


def object_models():
    left = [1]
    right = [1]
    assert left == right and left is not right
    before = (left,)
    left.append(2)
    assert before[0] is left and before[0] == [1, 2]
    return {"equal_lists_identical": left is right, "tuple_referent_value": before[0]}


def collection():
    class Node:
        pass

    gc.disable()
    try:
        node = Node()
        node.cycle = node
        reference = weakref.ref(node)
        gc.collect()
        reachable_survived = reference() is node
        del node
        unreachable_deferred = reference() is not None
        gc.collect()
        eventually_collected = reference() is None
    finally:
        gc.enable()
    assert reachable_survived and unreachable_deferred and eventually_collected
    return [reachable_survived, unreachable_deferred, eventually_collected]


def context_manager():
    events = []

    class Demo:
        def __init__(self, fail_enter=False):
            self.fail_enter = fail_enter

        def __enter__(self):
            events.append("enter")
            if self.fail_enter:
                raise LookupError
            return (1,)

        def __exit__(self, kind, value, traceback):
            events.append(kind.__name__)

    try:
        with Demo() as (first, second):
            events.append("body")
    except ValueError:
        pass
    try:
        with Demo(fail_enter=True):
            events.append("body")
    except LookupError:
        pass
    assert events == ["enter", "ValueError", "enter"]
    return events


def assignment_order():
    events = []

    def record(name, value):
        events.append(name)
        return value

    target = [0]
    record("target", target)[record("index", 0)] = record("value", 2)
    record("aug-target", target)[record("aug-index", 0)] += record("aug-value", 4)
    assert events == ["value", "target", "index", "aug-target", "aug-index", "aug-value"]
    return events


def generator():
    events = []

    def generator_function():
        events.append("start")
        local = 17
        delta = yield local
        yield local + delta

    iterator = generator_function()
    assert not events and iter(iterator) is iterator
    first = next(iterator)
    second = iterator.send(5)
    iterator.close()
    assert (first, second, events) == (17, 22, ["start"])
    return [first, second, *events]


def short_circuit():
    calls = []

    class Operand:
        def __init__(self, truth):
            self.truth = truth

        def __bool__(self):
            calls.append(self.truth)
            return self.truth

    truthy = Operand(True)
    falsy = Operand(False)
    right = object()

    def rhs():
        calls.append("right")
        return right

    assert (falsy and rhs()) is falsy
    assert (truthy or rhs()) is truthy
    assert (truthy and rhs()) is right
    assert (falsy or rhs()) is right
    assert calls == [False, True, True, "right", False, "right"]
    return calls


def grouped_exceptions():
    events = []
    try:
        raise ExceptionGroup("mixed", [ValueError(), LookupError()])
    except* ValueError as part:
        events.append([type(error).__name__ for error in part.exceptions])
    except* Exception as part:
        events.append([type(error).__name__ for error in part.exceptions])
    assert events == [["ValueError"], ["LookupError"]]
    return events


def coroutine():
    class WaitOnce:
        def __await__(self):
            received = yield "pause"
            return received

    async def run():
        marker = 3
        return marker + await WaitOnce()

    pending = run()
    suspended = pending.send(None)
    try:
        pending.send(4)
    except StopIteration as done:
        value = done.value
    assert (suspended, value) == ("pause", 7)
    return [suspended, value]


def type_parameter_defaults():
    events = []

    def marker():
        events.append("evaluated")
        return int

    class Defaulted[T=marker()]:
        pass

    class NoDefault[T]:
        pass

    parameter, = Defaulted.__type_params__
    assert not events and parameter.has_default() and not events
    assert parameter.__default__ is int and events == ["evaluated"]
    assert NoDefault.__type_params__[0].__default__ is typing.NoDefault
    return events


def package_kinds():
    with TemporaryDirectory(dir=Path(__file__).resolve().parent) as temp:
        root = Path(temp)
        portion_paths = [root / folder for folder in ("first", "second")]
        for index, location in enumerate(portion_paths):
            portion = location / "sces_package_probe"
            portion.mkdir(parents=True)
            (portion / f"piece{index}.py").write_text(f"value = {index}\n", encoding="utf-8")
        regular = portion_paths[0] / "sces_regular_probe"
        regular.mkdir()
        (regular / "__init__.py").write_text("value = 2\n", encoding="utf-8")
        sys.path[:0] = [str(path) for path in portion_paths]
        try:
            package = importlib.import_module("sces_package_probe")
            observed = [len(list(package.__path__))]
            observed.extend(importlib.import_module(f"sces_package_probe.piece{index}").value
                            for index in range(len(portion_paths)))
            observed.append(importlib.import_module("sces_regular_probe").value)
        finally:
            del sys.path[:len(portion_paths)]
    assert observed == [2, 0, 1, 2]
    return observed


def import_finder():
    events = []
    name = "sces_meta_path_probe"

    class Loader(importlib.abc.Loader):
        def exec_module(self, module):
            module.answer = 11

    class Finder:
        def __init__(self, label, available=False):
            self.label = label
            self.available = available

        def find_spec(self, fullname, path=None, target=None):
            events.append([self.label, fullname])
            if self.available and fullname == name:
                return importlib.machinery.ModuleSpec(name, Loader())

    old_path = sys.meta_path
    try:
        sys.meta_path = [Finder("declines"), Finder("accepts", True), Finder("after")]
        first = importlib.import_module(name)
        assert first.answer == 11
        assert importlib.import_module(name) is first
        sys.modules[name] = None
        try:
            importlib.import_module(name)
        except ModuleNotFoundError:
            events.append("cached-none")
        del sys.modules[name]
        try:
            importlib.import_module("sces_unavailable_probe.child")
        except ModuleNotFoundError:
            events.append("missing-parent")
        try:
            sys.meta_path = [Finder("declines"), Finder("also-declines")]
            importlib.import_module(name)
        except ModuleNotFoundError:
            events.append("exhausted")
    finally:
        sys.meta_path = old_path
        sys.modules.pop(name, None)
    assert events[:3] == [["declines", name], ["accepts", name], "cached-none"]
    assert ["declines", "sces_unavailable_probe.child"] not in events
    assert events[-1] == "exhausted"
    return events


def metaclass():
    class DemoMeta(type):
        pass

    class OtherMeta(type):
        pass

    class Base(metaclass=DemoMeta):
        pass

    class Child(Base):
        pass

    class Other(metaclass=OtherMeta):
        pass

    assert type(Child) is type(Base) is DemoMeta
    try:
        type("Conflict", (Base, Other), {})
    except TypeError as error:
        return [type(Child).__name__, type(error).__name__]
    raise AssertionError("Expected a metaclass conflict")


if __name__ == "__main__":
    challenges = (indentation, blocks_and_frames, object_models, collection, context_manager,
                  assignment_order, generator, short_circuit, grouped_exceptions, coroutine,
                  type_parameter_defaults, package_kinds, import_finder, metaclass)
    print(json.dumps({
        "runtime": f"{platform.python_implementation()} {platform.python_version()}",
        "observations": {challenge.__name__: challenge() for challenge in challenges},
        "stdlib_cgi_file": (Path(sysconfig.get_path("stdlib")) / "cgi.py").is_file(),
        "cgi_spec_present": importlib.util.find_spec("cgi") is not None,
        "local_gil_enabled": sys._is_gil_enabled(),
        "python_h_present": (Path(sysconfig.get_path("include")) / "Python.h").is_file(),
    }, sort_keys=True, indent=2))
