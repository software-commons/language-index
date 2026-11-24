# Core language profiles

This document records provisional research from the initial core-editions pass. The [Python qualification pilot](../reviews/python-pilot.md) identifies the two revised claims selected for a later qualification and preserves the remaining limitation.

## Python 3.13.0

- **Identity.** The Introduction and Alternate Implementations sections identify Python as the programming language and CPython as one implementation. The source is a language reference distributed with CPython. Implementation notes do not extend the language claim to every compiler or runtime. [Introduction, lines 4–53](https://github.com/python/cpython/blob/60403a5409ff2c3f3b07dd2ca91a7a3e096839c7/Doc/reference/introduction.rst#L4-L53)
- **Local name binding.** A function-scope reference to an as-yet unbound local produces `UnboundLocalError`. An unresolved name that is outside that condition can follow a different path. [Execution model, lines 119–134](https://github.com/python/cpython/blob/60403a5409ff2c3f3b07dd2ca91a7a3e096839c7/Doc/reference/executionmodel.rst#L119-L134)
- **Enclosing bindings.** The original claim about `nonlocal` remains insufficient. The controlling passage describes the nearest enclosing binding and a syntax error when no such binding exists. Independent verification found that the claim needs an explicit lexical-visibility condition. [Simple statements, lines 1008–1023](https://github.com/python/cpython/blob/60403a5409ff2c3f3b07dd2ca91a7a3e096839c7/Doc/reference/simple_stmts.rst#L1008-L1023) · [Review finding](../reviews/python-pilot.md)

## ECMAScript 2024

- **Declaration grammar.** An ordinary `const` lexical declaration of a plain identifier requires an initializer. Separate loop productions need separate treatment. [ECMA-262, 15th edition, §14.3.1.1](https://262.ecma-international.org/15.0/index.html#sec-let-and-const-declarations-static-semantics-early-errors)
- **Evaluation.** An ordinary `let` binding identifier without an initializer receives `undefined` when that binding is evaluated. The claim does not imply access before evaluation. [ECMA-262, 15th edition, §14.3.1.2](https://262.ecma-international.org/15.0/index.html#sec-let-and-const-declarations-runtime-semantics-evaluation)

These are language-edition statements. Identify JavaScript naming, host APIs, and runtime implementation behaviors separately. No engine observation was used as support.

## Go 1.23

- **Source structure.** The package clause starts the grammatical source-file structure and identifies the package. Comments, whitespace, and build constraints are outside this narrow claim. [Go specification, lines 7867–7894](https://github.com/golang/go/blob/6885bad7dd86880be6929c02085e5c7a67ff2887/doc/go_spec.html#L7867-L7894)
- **Memory.** A valid slice expression with a non-nil slice operand that yields a slice shares the operand's underlying array. String slicing and allocations by later operations such as append need separate claims. [Go specification, lines 4047–4052](https://github.com/golang/go/blob/6885bad7dd86880be6929c02085e5c7a67ff2887/doc/go_spec.html#L4047-L4052)

The specification labels this language edition `go1.23`. The source commit is the `go1.23.0` release source. The claims cover the edition's specification.

## Provenance and follow-up

The research execution directly retrieved five pinned documents over HTTPS and captured their byte digests. The claim input package preserves the exact source identifiers, per-claim locators, scopes, limitations, and claim byte hashes. A reviewer should reacquire the source bytes, challenge the ordinary-scope and loop-production boundaries, and keep language claims separate from implementation claims.

Rust, Kotlin, Scala, Clojure, PostgreSQL, SQLite, and Visual Basic had primary documents retrieved during this execution. Their byte captures remain research inputs pending facet inspection and independent review.
