# First-release research audit

The campaign started from the 26 provisional profiles on `fb221d9141f529a8ef99f2a928f3ed89f362d973`. Fifteen profiles had structured claims. The other eleven had historical or publisher citations in prose. Claim and candidate reviews follow SCES-1.0. The discovery cutoff remains November 22, 2026 in America/Chicago.

## Structured profile audit

| Profile | Original scope | Gate or remaining question |
| --- | --- | --- |
| Python | 3.13.0 identity and name binding | Keep the pilot's corrected identity binding. The extended review excluded `nonlocal` revision 2 and the import-finder revision 1. Independently verified successors explicitly scope out implicit class cells and name lookup that stops before a finder search. |
| ECMAScript | 15th-edition declaration grammar and evaluation | Both original subject IDs were malformed. The new research uses immutable successors and examines ordinary declarations separately from loop-head productions. The original `OrdinaryGet` condition was withheld because the descriptor lookup belongs to the `[[GetOwnProperty]]` suboperation. |
| Go | Go 1.23 source-file structure and slice storage | Reverify both exact original claims. Larger edition and implementation history remains outside the original profile. |
| Lua | 5.4 types, metatables and memory | Reverify applicability within the documented 5.4 language and distinguish behavior governed by the manual from a particular execution. |
| Haskell | 2010 typing, evaluation and modules | Reverify against the language report. Compiler-specific extensions require separate records. |
| XML | XML 1.0 Fifth Edition syntax and processor obligations | A reviewed successor limits character delivery to included and processed data and preserves the non-validating processor's external-entity exception. Earlier broad revisions remain excluded. |
| XPath | 3.1 map and array expressions | The Recommendation and its publisher announcement support the version-specific source association for the existing XPath lead. |
| Ada | Ada 2022 packages and tasking | Three proposed claims cited deleted paragraphs in the annotated manual. The identity and package revisions use active text. The verified tasking successor covers ordinary queue insertion and leaves exceptional removal and completion scoped separately. |
| Rust | Modules and drop scopes, with one Rust 2024 distinction | Resolve edition-specific applicability and keep compiler and Cargo conventions separate. |
| Kotlin | Nullability and class inheritance | Isolate special treatment of sealed classes and keep interoperability platform-specific. |
| Scala | 2.13 lazy values and object definitions | Restrict the source to Scala 2.13. Scala 3 relations and compiler lowering need separate evidence. |
| Clojure | JVM 1.12 core macros and atom APIs | Distinguish Clojure identity from the JVM host and pin implementation/API claims to the documented distribution. |
| PostgreSQL SQL | 17.0 table inheritance and partition declarations | The command reference supports version-specific behavior. An independent review links the dialect to the SQL identity using publisher documentation. |
| SQLite SQL | 3.46.0 parser grammar and table options | Parser evidence and a release-specific reproduction establish recognized options. Publisher documentation supports the scoped dialect relationship. Storage behavior remains outside the parser claims. |
| Visual Basic for .NET | Source compilation, Option Strict, and imports | Microsoft separately documents VB6 and VBA. A shared display name does not establish an alias or edition relation. The independent review also observed that the tested Roslyn compiler accepted a mixed-width keyword that the pinned grammar excludes. The scope of the selected claim is the grammar. [VB6 support statement](https://learn.microsoft.com/en-us/previous-versions/visualstudio/visual-basic-6/visual-basic-6-support-policy?view=vs-2019) · [VBA language specification](https://learn.microsoft.com/en-us/openspecs/microsoft_general_purpose_programming_languages/ms-vbal/d5418146-0bd2-45eb-9c7a-fd9502722c74) |

## Historical and enterprise profile audit

The [historical profiles](../profiles/profiles-history.md) identify eleven language or vendor-scoped candidates. The [original-source reacquisition record](historical-sources-2026-11-22.json) preserves ten accessible responses and two direct HTTP 403 responses. Alternate official IBM archives supplied a V6R1 RPG IV reference and the fourth-edition Enterprise COBOL 6.4 reference. The original IBM i 7.5 RPG lead retains its distinct edition. Captured bytes establish document identity and availability. Each later claim still requires scoped assessment and separate verification.

| Profile | Source boundary retained |
| --- | --- |
| NESL | CMU report 93-129 identifies version 2.6. Other technical descriptions may concern 2.4 or 3.1. |
| Argus | The 1983 design paper and 1987 manual represent different documents and revision scopes. |
| Napier88 | Reference manual 2.2.1 distinguishes language facilities and the persistent environment. |
| SIMULA | The 1986 text identifies SIMULA 67 and distinguishes SIMULA I and implementation conventions. |
| MUMPS | Handbook 118 binds the original specification and its component dates. Later M naming and ANSI editions need their own sources. |
| RPG IV | Distinguish the RPG IV language and its ILE implementation. The alternate IBM V6R1 reference is a separate release from the earlier 7.5 scope. [IBM V6R1 manual](https://public.dhe.ibm.com/systems/power/docs/systemi/v6r1/en_US/sc092508.pdf) |
| PeopleCode | The publisher's PeopleTools 8.60 manual supplies a dated application-host scope. |
| COBOL | IBM's alternate z/OS 6.4 reference identifies fourth-edition document SC27-8713-03 and the June 2024 update. Its vendor implementation scope leaves broader COBOL standards and lineage open. [IBM language reference](https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf) |
| CLU | The MIT history documents design and team recollection. Use the relevant language manual for normative claims. |
| Icon | The project retains a Version 9 author overview. Detailed version and lineage claims need other documents. |
| Modula-3 | The archived scan includes the revised 1989 report and separately dated changes. Citations must identify which section and revision controls. |

## Reproduced exclusions

Two Python challenge sets ran on CPython 3.13.5. The reviewer checked the 3.13.0 reference and compiler source separately. A method nested in a class can obtain the implicit `__class__` binding through `nonlocal`, even without a textually enclosing function binding. Attempting to import a missing submodule can fail while resolving its parent, before a finder examines the requested submodule. These observations challenge the frozen applicability conditions. They do not extend the stated interpreter observations to other implementations. [Probe sources and recorded results](python-313-probes/)

The first `OrdinaryGet` revision says its operation returns no own property descriptor. One review applied that phrase to the nested `[[GetOwnProperty]]` step and supported the intended scope. A separate reading identified the misleading literal attribution. An independently verified successor names `[[GetOwnProperty]]` and confines the result to normal prototype retrieval. [ECMA-262, §10.1.8.1](https://262.ecma-international.org/15.0/index.html#sec-ordinaryget)

## Exact discovery matches

The prospective registry links the existing XPath, NESL, PeopleCode, SIMULA, Napier88, and Argus candidates to reviewed language identities. The W3C Recommendation supplies XPath edition context. MIT's Handle and the Argus discovery URL returned identical catalog bytes with SHA-256 `da467e82208b651a5e1a622f548d8ebc762dff9dd09e4888c995aa22d439b927`. The other four candidate locators are exact identity sources. SIMULA is resolved in the sense defined by the 1986 source. The NIST-hosted Handbook 118 supports the MUMPS identity, while the Bitsavers discovery copy returned HTTP 403. That copy remains an unresolved crosswalk.

The SQL parent uses the public 2023 Framework preview's identity and scope. Detailed clauses and the full corrigendum are outside the selection. The PostgreSQL 17.0 and SQLite 3.46.0 dialect relationships refer to their separately documented vendor boundaries. The qualified relationships carry no general conformance finding.

The release cohort uses exact selected claims and directly inspected sources. Unreviewed profiles, unresolved lead matches, and candidate-era draft claims remain research records. The cohort establishes neither a closed population nor complete technical or historical coverage of an included language.
