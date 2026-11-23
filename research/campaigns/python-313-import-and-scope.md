# Python 3.13.0 import and scope investigation

The rc.3 selection already includes the qualified `python-313-nonlocal-nearest-binding` revision 3 and `python-313-import-finder-hooks` revision 2. The earlier revisions retain their original dispositions. The newer research isolates the behavior outside those two selected claims.

| Dimension | Independently supported finding |
| --- | --- |
| Modules and import state | Scoped findings cover the `None` cache sentinel, parent path discovery, the path argument when a meta finder is called, and initial-load cache cleanup. |
| Type system and evaluation | The pinned language reference describes immediate class namespace access from the applicable annotation scope, lazy alias values, and the type-parameter boundary for `nonlocal`. |
| Implementation relationships | The implicit `__class__` finding concerns CPython 3.13.0 and the stated Windows AMD64 probe. It remains distinct from the ordinary language-reference scope rule. |

The fresh review matched four exact source revisions and reproduced the implementation challenge on the official CPython 3.13.0 Windows AMD64 build. The challenge also confirmed lazy alias evaluation against a conflicting reading of the illustrative pseudocode. [Probe result](../../sces/artifacts/goal-python-313-independent-probe.json)

These eight records refine import, annotation, evaluation and implementation coverage. Other implementations, later editions, the complete annotation model, and the remaining history, resource, grammar and concurrency dimensions still require separate investigation.
