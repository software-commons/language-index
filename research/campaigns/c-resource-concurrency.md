# C draft resource and concurrency profile

The individually reviewed details apply to the C2y working draft N3220. The associated WG14 editor report establishes the draft context. The existing C identity, its seven prior selected records, and the exact source revisions remain in history.

The batch examines the allowed one-past pointer arithmetic and the evaluated indirection restriction, the rules for const- and volatile-qualified objects, and the lifetime and failure cases of allocation functions. It also checks data-race and release-acquire rules and narrows the draft’s atomic relaxed-order note to the same object. General language rules, library functions, and explanatory notes preserve their separate roles.

The selected clauses are documentary coverage of the exact draft. Published ISO text and observed compiler or runtime behavior have separate evidence scopes. The [source witnesses](../../sces/artifacts/c-resource-concurrency-source-witnesses.json) record exact physical and printed pages for independent inspection.
