"""Independent, bounded probes for the frozen nonlocal binding claim."""

import json
import platform
from textwrap import dedent


CASES = {
    "nearest of two function bindings": """
        def outer():
            place = 'outer'
            def middle():
                place = 'middle'
                def inner():
                    nonlocal place
                    return place
                return inner()
            return middle()
        result = outer()
    """,
    "intervening function global": """
        place = 'module'
        def outer():
            place = 'outer'
            def middle():
                global place
                def inner():
                    nonlocal place
                    return place
    """,
    "class attribute only": """
        class Holder:
            place = 'class'
            def inner(self):
                nonlocal place
                return place
    """,
    "implicit class-reference cell only": """
        class Holder:
            def inner(self):
                nonlocal __class__
                return __class__.__name__
        result = Holder().inner()
    """,
    "implicit class-reference cell versus outer local": """
        def outer():
            __class__ = 'outer'
            class Holder:
                def inner(self):
                    nonlocal __class__
                    return __class__
            return Holder().inner()
        result = outer()
    """,
    "late outer assignment after the declaration": """
        def outer():
            def inner():
                nonlocal place
                return place
            place = 'late'
            return inner()
        result = outer()
    """,
    "outer local read before assignment": """
        def outer():
            def inner():
                nonlocal place
                return place
            value = inner()
            place = 'late'
            return value
        result = outer()
    """,
    "class body declares nonlocal for an outer local": """
        def outer():
            place = 'outer'
            class Holder:
                nonlocal place
                place = 'changed'
            return place
        result = outer()
    """,
    "generic parameter blocks a same-named outer local": """
        def outer():
            T = 'outer'
            def middle[T]():
                def inner():
                    nonlocal T
                    return T
    """,
    "a local intermediate declaration restores eligibility": """
        place = 'module'
        def outer():
            global place
            def middle():
                place = 'middle'
                def inner():
                    nonlocal place
                    return place
                return inner()
            return middle()
        result = outer()
    """,
}


def probe(name, source):
    try:
        code = compile(dedent(source), f"<{name}>", "exec")
    except SyntaxError as error:
        return {"stage": "compile", "error": type(error).__name__, "message": error.msg}
    namespace = {}
    try:
        exec(code, namespace)
    except Exception as error:
        return {"stage": "execute", "error": type(error).__name__, "message": str(error)}
    value = namespace.get("result")
    return {"stage": "execute", "result": value.__name__ if isinstance(value, type) else value}


if __name__ == "__main__":
    print(json.dumps({
        "runtime": f"{platform.python_implementation()} {platform.python_version()}",
        "observations": {name: probe(name, source) for name, source in CASES.items()},
    }, sort_keys=True, indent=2))
