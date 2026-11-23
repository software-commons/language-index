# Targeted discovery of historical and underobserved languages

**Discovery cutoff** 2026-11-22

This public-source pass supplements broad catalog discovery with historically specific and less commonly indexed leads. It did not use the access-controlled Atlas overlay. Every imported row remains provisional until identity, scope, and evidence are independently assessed.

## Routes

| Route | Lead rows | Method and starting points |
| --- | ---: | --- |
| Software preservation | 87 | Traverse the [Computer History Museum Software Preservation Group collections](https://softwarepreservation.computerhistory.org/), follow the ALGOL, Lisp, Mesa, Prolog, SETL, and functional-programming document indexes, and select anchored entries that name a program notation, candidate variant, edition, or adjacent implementation. Verify section anchor names against the HTML. |
| Enterprise and vendor manuals | 19 | Query publisher documentation for language reference titles, platform release versions, and document IDs. Keep vendor scope visible, including [ILE RPG](https://www.ibm.com/docs/en/i/7.5.0?topic=rpg-ile-reference), [PeopleCode](https://docs.oracle.com/cd/G10811_01/psft/pdf/pt860tpcl-b072024.pdf), [enterprise COBOL](https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf), and the original [MUMPS language standard](https://www.bitsavers.org/pdf/mumps/NBS_Handbook_118_MUMPS_Language_Standard_Jan1976.pdf). |
| Academic and formal languages | 17 | Search university, national laboratory, and design-team repositories for named language reports. Examples include the [CMU NESL report](https://www.cs.cmu.edu/~scandal/papers/CMU-CS-93-129.html), [Argus reference manual](https://dspace.mit.edu/entities/publication/9c3ffb1f-5047-459b-b628-150206b2450b), [Napier88 reference manual](https://archive.cs.st-andrews.ac.uk/papers/download/MBC%2B96b.pdf), and [1986 SIMULA standard](https://www.mn.uio.no/english/services/it/simula/versions/simula-1986/chap_0.htm). |
| Non-English sources | 5 | Search in Japanese, Simplified Chinese, and Portuguese and retain source-language labels where helpful. Use the [Nadeshiko manuals](https://nadesi.com/man/index.php?EVAL=&search=), [易语言 author documentation](https://www.eyuyan.com/help/zlsc/day/index.htm), and Brazilian [VisuAlg](https://www.cin.ufpe.br/~rrbs/AC_/LinguagemPortuguesEstruturado/VisualG_Tutorial.pdf) and [PortuCol](https://professores.dcc.ufla.br/~terra/publications_files/2016_wei_portucol.pdf) materials. |
| **Total** | **128** | One row per selected public origin, including document URL, recorded release, repository item identifier, or precise section anchor when available. |

## Reproduction and adjudication

Start with the linked collection indexes and manuals. Search with the source-family names and terms such as “language reference”, “technical report”, “historical archive”, `日本語 プログラミング言語`, `易语言 语法`, and `Portugol linguagem`. Record the exact document or collection section used for discovery. The candidate ledger carries those locators. Deduplicate exact locators and inspect similar labels as potential conflicts. Preserve distinct locators whenever there is an unresolved scope or identity question.

An archive heading can name several entities together or mix a language with a compiler, system, edition, or application. For example, NIL and S-1 Lisp, the Backus Red and FP names, and multiple ALGOL 68 and SETL variants need follow-up. Treat release-specific vendor manuals within their stated product scope. Product names and shared runtimes do not establish identity. External preservation pages are discovery pointers to underlying artifacts and may be updated. Qualification requires the precise controlling material and its captured bytes or documented preservation limits under SCES.

## Limits

This sample reflects publicly listed materials. A direct retrieval check reached 54 of the 60 distinct document URLs. Five IBM Documentation URLs returned 403 and the MIT parallel-language bibliography timed out. Public search entries identified the pointers, which remain unresolved leads pending direct inspection. Holdings and preservation effort are uneven by institution, region, era, documentation language, and vendor. Proprietary internal systems, non-digitized documents, and gaps in non-English coverage were not systematically enumerated. The route counts describe discovery rows in this pass and may overlap other campaigns. They do not estimate unique language identities, indicate use or popularity, or substantiate coverage completeness. Follow-up should review vendor-specific boundaries, identify more original manuals and papers, and add further regional searches with local-language source terms.
