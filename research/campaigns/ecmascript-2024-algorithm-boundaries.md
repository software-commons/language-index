# ECMAScript 2024 algorithm boundaries

The successor keeps the independently supported OrdinaryGet revision 2 already included in rc.3. Its broader predecessor retains the earlier disposition. A fresh research and independent review pair matched the exact fifteenth-edition document and supported seven additional normative records.

| Dimension | Reviewed scope |
| --- | --- |
| Objects and evaluation | Own accessor receiver handling and the distinct base and receiver of applicable super property references. |
| Name binding | The environment-chain search and the `@@unscopables` branch of a with environment record. |
| Modules and state | The own descriptor of a normally retrieved string export in a module namespace and that object's assignment boundary. |
| Error handling | The original throw's precedence in IteratorClose when return-method lookup or invocation also throws. |
| Values and comparison | The signed-zero boundary in the Number branches for SameValueZero and SameValue. |

The dispositions cover the indicated algorithms in ECMAScript 2024. Implementation observations, later editions and broader profile dimensions remain open. [Controlling specification](https://262.ecma-international.org/15.0/index.html)
