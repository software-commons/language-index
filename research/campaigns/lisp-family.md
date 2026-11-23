# Scheme and Common Lisp profiles

The Scheme profile uses the original July 2013 R7RS-small report. The selected clauses concern local binding, proper tail recursion, library imports, and continuations. Later corrected reproductions and other report editions retain separate evidence scopes.

The Common Lisp profile uses LispWorks’ HyperSpec 7.0 as a derived reference. Its publisher identifies the ANSI publication as definitive. The selected claims describe exact HyperSpec clauses and keep language, package, and implementation contexts distinct.

The [Scheme classifier](https://github.com/github-linguist/linguist/blob/cfd7a0113aa1efab99faeff38756f0ed4d48add8/lib/linguist/languages.yml#L7518) resolves to the language identity across the observed edition contexts. The [Common Lisp classifier](https://github.com/github-linguist/linguist/blob/cfd7a0113aa1efab99faeff38756f0ed4d48add8/lib/linguist/languages.yml#L1470) includes ordinary Common Lisp together with S-expression data and host-specific specimens. The scoped source association is supported. The whole classifier remains unresolved.

[Lead decisions](../../sces/artifacts/lisp-family-origin-review.json) preserve the original rows, scopes, and specimen results. [Independent source witnesses](../../sces/artifacts/lisp-family-source-witnesses.json) record exact PDF pages, archive members, and native acquisitions.
