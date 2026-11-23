# Provisional historical, academic, and enterprise profiles

This research pass inspected public primary reports, reference manuals, and author documentation on 2026-11-22. Each profile names the version or document scope for the observations below. The findings support candidate investigation. They await separately recorded review, scope adjudication, and SCES qualification before canonical use.

## NESL

- **Identity and edition.** Guy E. Blelloch's April 1993 Carnegie Mellon report identifies NESL 2.6 and explicitly distinguishes it from the report for 2.4. The revision note attributes additions for polymorphic types and I/O, and a syntax change, to 2.6. [CMU-CS-93-129, citation block and revision note](https://www.cs.cmu.edu/~scandal/papers/CMU-CS-93-129.html)
- **Design and implementation.** The report describes an applicative data-parallel language with nested sequences. Its sequence operation can apply a function across elements, including functions that perform parallel work of their own. The compiler described in this report targets the intermediate language Vcode. [CMU-CS-93-129, abstract](https://www.cs.cmu.edu/~scandal/papers/CMU-CS-93-129.html)
- **Remaining work.** Compare the 2.4, 2.6, and 3.1 reports and distinguish their type systems, cost models, and supported implementations. Benchmark and runtime claims need independent investigation.

## Argus

- **Identity and intent.** The November 1987 MIT manual describes Argus as an experimental language and system for distributed services that need to protect online data from concurrent activity and failures, within its stated timing assumptions. [MIT-LCS-TR-400, issue date and abstract](https://hdl.handle.net/1721.1/149664)
- **Program structure and execution.** The 1983 design paper decomposes a distributed program into guardians that control access to resources through handlers. It distinguishes stable guardian state, recorded on top-level commit, from volatile state that an application may have to recreate after recovery. [Liskov and Scheifler, *Guardians and Actions*, §3.1, printed pages 388–389](https://pdos.csail.mit.edu/archive/6.824-2007/papers/liskov-argus.pdf)
- **Remaining work.** Check the 1987 syntax and exact transaction semantics against its manual. The 1983 design account gives no independent operational measurement of recovery or environmental guarantees.

## Napier88

- **Identity and edition.** The July 1996 manual identifies release 2.2.1. Its introduction relates the system to the PISA research project and distinguishes the persistent environment from the language changes since 1.0, including type operators. [Napier88 Reference Manual 2.2.1, cover and introduction, PDF pages 1 and 7](https://archive.cs.st-andrews.ac.uk/papers/download/MBC%2B96b.pdf#page=7)
- **Persistence and types.** The authors explain which objects persist using reachability from a root object in the persistent environment. The type overview defines environments as collections of bindings and describes `any` as carrying a value and a representation of its type. [Reference Manual, introduction and type overview, PDF pages 5 and 9](https://archive.cs.st-andrews.ac.uk/papers/download/MBC%2B96b.pdf#page=9)
- **Remaining work.** Inspect the separate standard-library manual and the compiler-to-Persistent Abstract Machine rules before stating execution or library guarantees. Compare related S-algol and PS-algol identities independently.

## SIMULA

- **Identity and authority.** The 1986 standard specifies that its use of SIMULA refers to SIMULA 67 and identifies SIMULA I as a predecessor. Its scope covers language syntax, semantics, representation, and conformance criteria for programs and processors. [University of Oslo's copy of the 1986 standard, chapter 0, Introduction and Scope](https://www.mn.uio.no/english/services/it/simula/versions/simula-1986/chap_0.htm)
- **Standards and implementation boundaries.** Chapter 0 distinguishes requirements stated by the standard, conventions each implementation must document, and matters left to the implementor. It gives explicit conditions for an implementation to support extensions while claiming conformity. [1986 standard, chapter 0, Definitions, Conformity, and Extensions](https://www.mn.uio.no/english/services/it/simula/versions/simula-1986/chap_0.htm)
- **Remaining work.** Read the class, process, and simulation descriptions in the language chapters and compare with the Common Base Language and SIMULA I publications. No particular compiler's conformance has been assessed.

## MUMPS

- **Identity and edition.** The January 1976 NBS Handbook 118 publishes a MUMPS Development Committee specification, transition diagrams, and portability requirements, with distinct committee release dates. These are identifiable components of this specific handbook. [NBS Handbook 118, title and foreword, PDF pages 3–5](https://nvlpubs.nist.gov/nistpubs/Legacy/hb/nbshandbook118.pdf#page=5)
- **Source structure and value model.** The specification describes a routine as a series of lines that may carry labels for control transfer. It specifies numeric interpretation of string values used in arithmetic while allowing an implementation to choose internal representations. [Handbook 118, part I §§1.2.2 and 1.2.4, PDF pages 15 and 17](https://nvlpubs.nist.gov/nistpubs/Legacy/hb/nbshandbook118.pdf#page=15)
- **Remaining work.** Compare later ANSI revisions, the use of the name M, and implementation-specific global storage and transaction behavior. The 1976 description alone does not resolve those questions.

## RPG IV in IBM ILE RPG

- **Identity and implementation scope.** IBM's manual states that it covers RPG IV as implemented by the ILE RPG compiler on IBM i. Keep this release-scoped language evidence distinct from the compiler product and other RPG generations. [IBM *ILE RPG Reference*, introduction, document SC09-2508](https://www.ibm.com/docs/zh/ssw_ibm_i_75/pdf/sc092508.pdf)
- **Modularity and execution model.** The manual illustrates the same kind of subprocedure definition in free-form and fixed-form source. Its module description distinguishes a cycle-main procedure that follows the RPG cycle from a linear-main procedure declared using the `MAIN` control keyword. [IBM *ILE RPG Reference*, Subprocedures and Cycle/Linear Module sections](https://www.ibm.com/docs/zh/ssw_ibm_i_75/pdf/sc092508.pdf)
- **Remaining work.** Verify original RPG generations and precise availability by compiler release. Study the documentation of built-in functions and platform conventions separately.

## PeopleCode

- **Identity and product scope.** Oracle's July 2024 PeopleTools 8.60 reference describes PeopleCode language constructs and built-in functions for this PeopleSoft product baseline. [Oracle *PeopleCode Language Reference*, PeopleTools 8.60, title and chapter 1](https://docs.oracle.com/cd/G10811_01/psft/pdf/pt860tpcl-b072024.pdf)
- **Scope and host events.** A component variable declared using the `Component` statement remains in scope for the life of its component. Each PeopleCode program that uses it must declare it. The reference's `DoSave` section also names the events where that operation is allowed, illustrating a rule tied to application lifecycle. [PeopleCode reference, `Component` and `DoSave` sections, PDF pages 139 and 292](https://docs.oracle.com/cd/G10811_01/psft/pdf/pt860tpcl-b072024.pdf#page=139)
- **Remaining work.** Check how these rules vary by PeopleTools release, and inspect the separate developer guide before formalizing the comprehensive event and object models.

## COBOL in IBM Enterprise COBOL

- **Identity and edition.** The source describes COBOL as implemented by IBM Enterprise COBOL for z/OS 6.4. This supplies vendor-scoped evidence for COBOL. The compiler name alone supplies no evidence for a separate language identity. [IBM *Enterprise COBOL for z/OS, V6.4 Language Reference*, preface](https://www.ibm.com/docs/es/SS6SG3_6.4.0/pdf/lrmvs.pdf)
- **Program structure and runtime terminology.** The IBM manual organizes most source material into identification, environment, data, and procedure divisions, explicitly identifying exceptions. It also uses *run unit* for one or more cooperating object programs at runtime, separate from a source program's divisions. [IBM language reference, COBOL program structure, printed page 83](https://www.ibm.com/docs/es/SS6SG3_6.4.0/pdf/lrmvs.pdf)
- **Remaining work.** Separate standardized syntax from IBM extensions and documented vendor behavior. Obtain the relevant COBOL standards editions, and check versioned divergences with other implementations.

## CLU

- **Identity and history.** Barbara Liskov's retrospective associates the name CLU with the team's cluster concept and dates the choice of name to fall 1973. The retrospective is evidence for this project account. [Liskov, *A History of CLU*, MIT-LCS-TR-561, printed page 3](https://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-561.pdf)
- **Abstraction and control flow.** The report describes clusters as modules that define an abstract type's operations and private representation, with type checking enforcing the access boundary. Its iterator section describes a `for` loop executing its body on each yield, then resuming the iterator. [MIT-LCS-TR-561, §§3.4 and 3.10, printed pages 9 and 16–17](https://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-561.pdf)
- **Remaining work.** Locate the relevant reference manual edition for normative and implementation claims. Independently check the historical naming date and the relationship between CLU and other abstraction mechanisms.

## Icon

- **Identity and scope.** The University of Arizona project hosts Ralph Griswold's Version 9 overview, IPD266. Treat the overview as an author description of the stated version. [Griswold, *An Overview of the Icon Programming Language*, publication heading](https://www2.cs.arizona.edu/icon/docs/ipd266.htm)
- **Evaluation and text model.** A generator can produce successive values as its context demands, and a procedure can suspend to supply a value and resume later. String-scanning expressions operate with a subject and a current position, which matching operations can change. [IPD266, Generators and String Scanning sections](https://www2.cs.arizona.edu/icon/docs/ipd266.htm)
- **Remaining work.** Check the full reference against scope and evaluation order, compare language revisions, and investigate implementation boundaries with descendants separately.

## Modula-3

- **Identity and edition.** The November 1989 revised report distinguishes itself from the August 1988 release of the report. Its preface attributes the work to the DEC and Olivetti research efforts and identifies several predecessors, including Modula-2 and Mesa. [SRC Research Report 52, title and preface](https://softwarepreservation.computerhistory.org/modula3/doc/SRC-RR-52.pdf)
- **Design and decomposition.** The preface identifies explicitly declared interfaces between modules as an inherited design feature and notes language features including exceptions, garbage collection, and threads. The same scan appends a separately dated 1990 change description, which must be treated separately when comparing revisions. [SRC Research Report 52, preface, Modules and Interfaces, and appended changes](https://softwarepreservation.computerhistory.org/modula3/doc/SRC-RR-52.pdf)
- **Remaining work.** Pin the individual base report or amendment for each normative assertion. Investigate the implementation versions and the applicability of later changes before describing portability.

## Coverage and verification

These 11 profiles cover identity or source scope and at least one design, execution, standards, or language-structure dimension for each candidate. They leave open version differences, population completeness, and most implementation and usage claims. The notes retain public locators and paraphrased findings. They contain no SCES acceptance, claims of independent verification, or reconstructed execution receipts.
