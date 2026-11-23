# Additional provisional language profiles

These are narrow first-pass profiles drawn from directly read primary sources. No claims here have been admitted to the canonical Language Index or marked independently reviewed. Source capture hashes refer to exact retrieved bytes. The source texts are held in research scratch so later readers can reacquire them from the listed revision.

## Rust

Rust Reference snapshot `c9cc32825b03fc206d9c6fe73e9ca6a2f3576d6c`. The edition-specific facet applies to Rust 2024. The language reference is the evidence for these scoped constructs. Compiler implementation strategies, Cargo conventions, and runtime behavior need separate sources.

- **Module source layout.** An out-of-line module declaration loads its body from a file. In the absence of a path attribute, the lookup follows module paths and the documented naming and directory rules. The source distinguishes conventional module lookup from explicit path attributes. It does not establish package layout. [items.mod.outlined.intro and items.mod.outlined.search, lines 53–64](https://github.com/rust-lang/reference/blob/c9cc32825b03fc206d9c6fe73e9ca6a2f3576d6c/src/items/modules.md#L53-L64)
- **Resource lifetime.** When control flow leaves a drop scope, associated variables drop in reverse declaration order and associated temporaries in reverse creation order. This applies within the drop scope. Edition, control flow, expression kind, and special scrutinee rules matter when determining a temporary's scope. [destructors.scope.intro, lines 55–62](https://github.com/rust-lang/reference/blob/c9cc32825b03fc206d9c6fe73e9ca6a2f3576d6c/src/destructors.md#L55-L62)
- **Rust 2024 edition difference.** The reference marks extra temporary-scope narrowing for if let and block tail expressions in the 2024 edition. The rule is edition-specific. [destructors.scope.temporary.edition2024, lines 287–289](https://github.com/rust-lang/reference/blob/c9cc32825b03fc206d9c6fe73e9ca6a2f3576d6c/src/destructors.md#L287-L289)

## Kotlin

Core Kotlin language specification snapshot `0f762a2314a9304e4b3fc386b1aceef1d56c7e4c`. These are Kotlin core-language claims. A shared JVM backend or Java library does not establish a Kotlin identity merge or identical Kotlin/Native, Kotlin/JS, and Kotlin/JVM behavior.

- **Nullability.** The specification distinguishes nullable and non-nullable type universes. A value of a non-nullable type cannot contain null under the described model. The claim concerns the type model. Interop flexible types and particular runtime null failures require separate treatment. [Type-system overview, lines 96–105](https://github.com/Kotlin/kotlin-spec/blob/0f762a2314a9304e4b3fc386b1aceef1d56c7e4c/docs/src/md/kotlin.core/type-system.md#L96-L105)
- **Inheritance.** A class is closed when its declaration supplies neither open nor abstract. The source also explains the implicit abstract status of a sealed class. The rule concerns classes and includes the sealed-class qualification. Interface inheritance follows separate rules. [Inheritance, lines 12–25](https://github.com/Kotlin/kotlin-spec/blob/0f762a2314a9304e4b3fc386b1aceef1d56c7e4c/docs/src/md/kotlin.core/inheritance.md#L12-L25)

## Scala

Scala 2.13 archived language specification, Classes and Objects. Source bytes are identified in the accession table. The claims concern Scala 2.13 language forms. Scala 3 and individual JVM compiler lowering require separately scoped sources.

- **Lazy initialization.** The specification describes a lazy value as initialized on its first access. Recursive initialization may exhibit looping, and an exception has separate rules. The source does not imply eager initialization at declaration. [The lazy modifier](https://www.scala-lang.org/files/archive/spec/2.13/05-classes-and-objects.html#lazy)
- **Object definitions.** An object definition introduces a single object of a new class. This is the object-definition construct. An arbitrary class declaration or shared JVM runtime does not establish the same single-object behavior. [Object Definitions](https://www.scala-lang.org/files/archive/spec/2.13/05-classes-and-objects.html#object-definitions)

## Clojure

Clojure 1.12.0 JVM core source at `d4bb93f0d1ab2004f89c6ead1b32449fd7ed1a6d`. Source-level descriptions from the Clojure/JVM distribution establish the identified API contract. ClojureScript or other implementations need their own sources.

- **Lazy sequences.** The lazy-seq macro documents deferred realization through seq and caching of the resulting sequence. This is one Seqable value created by the macro. Evaluation of arbitrary applications is outside scope. [lazy-seq implementation and documentation, lines 685–692](https://github.com/clojure/clojure/blob/d4bb93f0d1ab2004f89c6ead1b32449fd7ed1a6d/src/clj/clojure/core.clj#L685-L692)
- **Atomic state updates.** The swap! contract documents an atomic update derived from the current atom value and warns that the update function may be called more than once. The result concerns atom updates through this API. It supplies no exactly-once guarantee for the update function's side effects. [swap! implementation and documentation, lines 2362–2372](https://github.com/clojure/clojure/blob/d4bb93f0d1ab2004f89c6ead1b32449fd7ed1a6d/src/clj/clojure/core.clj#L2362-L2372)
- **Namespaces.** The ns macro sets the current namespace by an unevaluated name, creating it when needed, and supports optional namespace clauses. Compilation-only class generation follows separate behavior. [ns implementation and documentation, lines 5817–5829](https://github.com/clojure/clojure/blob/d4bb93f0d1ab2004f89c6ead1b32449fd7ed1a6d/src/clj/clojure/core.clj#L5817-L5829)

## PostgreSQL SQL dialect

PostgreSQL 17.0 publisher-authored command reference source at `d7ec59a63d745ba74fba0e280bbf85dc6d1caa3e`. The source documents PostgreSQL commands at the named release. A generic SQL definition and the identity relationships of other dialects need their own governing evidence.

- **Table inheritance.** The optional INHERITS clause names parent tables whose columns are inherited when PostgreSQL defines the child. Its documented parent relationship is persistent. Type conflicts, declaration merging, and subsequent schema propagation have additional rules. [INHERITS, lines 354–381](https://github.com/postgres/postgres/blob/d7ec59a63d745ba74fba0e280bbf85dc6d1caa3e/doc/src/sgml/ref/create_table.sgml#L354-L381)
- **Partition declarations.** The optional PARTITION BY clause offers range, list, and hash strategies. List partitioning requires a single column or expression in the partition key. Range and hash have different key arity and operator-class constraints. The statement does not describe every data insertion outcome. [PARTITION BY, lines 411–433](https://github.com/postgres/postgres/blob/d7ec59a63d745ba74fba0e280bbf85dc6d1caa3e/doc/src/sgml/ref/create_table.sgml#L411-L433)

## SQLite SQL dialect

SQLite 3.46.0 implementation parser source at `bebe2d8be8acfd02592c4972f4ba32c3b4e4a33f`. The source supports claims about SQLite's parser at this release. It does not establish general SQL syntax or prove storage and constraint effects for executed databases.

- **Table option grammar.** For the parenthesized column-list form of CREATE TABLE, the parser accepts a table option set that can combine comma-separated options. The CREATE TABLE AS SELECT alternative is separately expressed in the grammar. [create_table_args and table_option_set productions, lines 203–214](https://github.com/sqlite/sqlite/blob/bebe2d8be8acfd02592c4972f4ba32c3b4e4a33f/src/parse.y#L203-L214)
- **Table flags.** The parser recognizes WITHOUT ROWID and STRICT table options by case-insensitive name checks and maps them to different flags. The claim excludes downstream validation and storage behavior. [table_option productions, lines 215–230](https://github.com/sqlite/sqlite/blob/bebe2d8be8acfd02592c4972f4ba32c3b4e4a33f/src/parse.y#L215-L230)

## Visual Basic for .NET

Visual Basic language-specification snapshot `0712f0b8c91dfba593fc16f846c5821ed5cad2f9`. This specification is scoped to Visual Basic for .NET. Retain classic Visual Basic 6 and Visual Basic for Applications as separate lineage investigations until exact historical crosswalks are reviewed. The .NET compilation rules do not transfer to either candidate.

- **Compilation unit and names.** Within the described compilation model, source files are processed together and their top-level declarations contribute to the implicit global namespace. The source explicitly allows the compilation environment to override the implicit namespace. [Source Files and Namespaces introduction, lines 1–25](https://github.com/dotnet/vblang/blob/0712f0b8c91dfba593fc16f846c5821ed5cad2f9/spec/source-files-and-namespaces.md#L1-L25)
- **Type checking.** An explicit Option Strict statement with no On or Off argument defaults to On. With no statement, the compilation environment selects the setting. The default for omitted statement is distinct from the default for an omitted argument. [Option Strict Statement, lines 114–124](https://github.com/dotnet/vblang/blob/0712f0b8c91dfba593fc16f846c5821ed5cad2f9/spec/source-files-and-namespaces.md#L114-L124)
- **Imports.** An Imports directive makes names available to declarations in its source file. Its scope excludes other Imports statements and other source files. The source also describes implicit imports and separate import-name resolution rules. [Imports Statement, lines 249–266](https://github.com/dotnet/vblang/blob/0712f0b8c91dfba593fc16f846c5821ed5cad2f9/spec/source-files-and-namespaces.md#L249-L266)

## Source accession

| Source | Captured SHA-256 |
| --- | --- |
| [Rust Reference: Modules](https://raw.githubusercontent.com/rust-lang/reference/c9cc32825b03fc206d9c6fe73e9ca6a2f3576d6c/src/items/modules.md) | `902fdad152919f8152a8f55dae07b5683bb2ca8a37600aaa265e92fbc5c933b2` |
| [Rust Reference: Destructors](https://raw.githubusercontent.com/rust-lang/reference/c9cc32825b03fc206d9c6fe73e9ca6a2f3576d6c/src/destructors.md) | `3dd3a9215d8d8b3bdbcf9282679f272a5c9a8a147720a448a79bbdea3f65f51b` |
| [Clojure 1.12.0 JVM core source](https://raw.githubusercontent.com/clojure/clojure/d4bb93f0d1ab2004f89c6ead1b32449fd7ed1a6d/src/clj/clojure/core.clj) | `bce3e81261ac1dbfdcdeb75a42e847dcc14a6ea3bd817c17aeb6d031d10bdaf2` |
| [Scala 2.13 specification, Classes and Objects](https://www.scala-lang.org/files/archive/spec/2.13/05-classes-and-objects.html) | `8f61a73effa8c4086fdcfe69f97bc017e042fababbfae2a807da9b72cefb6155` |
| [PostgreSQL 17.0 CREATE TABLE reference source](https://raw.githubusercontent.com/postgres/postgres/d7ec59a63d745ba74fba0e280bbf85dc6d1caa3e/doc/src/sgml/ref/create_table.sgml) | `97f8f243fb2cbf2aaa3ef9bad0fa3112d4cc2b5395e8bef266607be4515fd315` |
| [SQLite 3.46.0 parser source](https://raw.githubusercontent.com/sqlite/sqlite/bebe2d8be8acfd02592c4972f4ba32c3b4e4a33f/src/parse.y) | `6e8f340dccc258273db9efb60dd2cc034bc2f8a2b5d1d1c00c578dc28fb03d4f` |
| [Kotlin language specification, Type System](https://raw.githubusercontent.com/Kotlin/kotlin-spec/0f762a2314a9304e4b3fc386b1aceef1d56c7e4c/docs/src/md/kotlin.core/type-system.md) | `f0b9a51178b98ff722b8a2f77fee0c2c2ab0b777f92ca5784c0c9167c047fd62` |
| [Kotlin language specification, Inheritance](https://raw.githubusercontent.com/Kotlin/kotlin-spec/0f762a2314a9304e4b3fc386b1aceef1d56c7e4c/docs/src/md/kotlin.core/inheritance.md) | `543bdecae15615f39bef19cf957ee6a5c36aafe2b460c55cc496bee6ff8888bc` |
| [Visual Basic .NET language specification, General Concepts](https://raw.githubusercontent.com/dotnet/vblang/0712f0b8c91dfba593fc16f846c5821ed5cad2f9/spec/general-concepts.md) | `3771537878d33edd9351ba8163d49ebaf0f2fa4112c7569ab64c17b64507ebb0` |
| [Visual Basic .NET language specification, Source Files and Namespaces](https://raw.githubusercontent.com/dotnet/vblang/0712f0b8c91dfba593fc16f846c5821ed5cad2f9/spec/source-files-and-namespaces.md) | `b409f7229f0075747e46bdf66dc7982991cbbef07c732a9d28191df6fd3f08a1` |

Research depth remains limited to the listed facets. Each release candidate still needs a frozen claim, admissible role and scope registration, an independent source review and compliance with the applicable SCES publication gates. Preserve implementation-only and unresolved identity interpretations during adjudication.
