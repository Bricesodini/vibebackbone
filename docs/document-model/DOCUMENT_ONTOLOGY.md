# Documentary Ontology

## Purpose

The ontology qualifies an artefact on independent axes. It answers what it may
prescribe, its governed lifecycle, the periods it describes, its dominant
function, and when an agent should load it. It neither establishes identity
nor creates authority.

## Tuple and values

```
(authority, lifecycle, temporality, primary_function, secondary_functions, load_policy)
```

| Axis | Allowed values |
| --- | --- |
| Authority | `CANONICAL`, `SCOPED_AUTHORITY`, `NON_AUTHORITATIVE`, `UNASSESSED` |
| Lifecycle | `PROPOSED`, `ACTIVE`, `TRANSITIONAL`, `SUPERSEDED`, `RETIRED` |
| Temporality | `CURRENT`, `PAST`, `FUTURE`, `MULTI_PERIOD`, `UNDATED` |
| Primary function | `NORMATIVE`, `REFERENCE`, `EVIDENCE`, `DECISION_RECORD`, `RUN_ARTIFACT`, `GENERATED`, `NAVIGATION` |
| Secondary functions | Zero or more function values |
| Load policy | `ALWAYS`, `ON_ROUTE`, `ON_DEMAND`, `NEVER_BY_DEFAULT` |

`MULTI_PERIOD` means a consultable artefact explicitly covers several periods.
It is neither historical nor an authority or lifecycle value; each statement
within it can still be current, past, or future.

## Invariants

1. Exactly one primary function is required; secondary functions are optional,
   unordered, and cannot contradict it.
2. Authority comes only from the authority axis and observable governance;
   neither a function nor a citation confers it.
3. `EVIDENCE` as secondary function is not sufficient proof of a rule, and
   `NORMATIVE` as secondary function cannot hide prescription in a
   non-authoritative artefact.
4. A non-editable derived projection keeps `GENERATED` as primary function.
5. A decision record has normative scope only through its authority value.
6. `MULTI_PERIOD` must not leave the currently applicable rule ambiguous.
7. `ALWAYS` requires an explicit boot requirement and never promotes an artefact.
8. Insufficiently evidenced combinations remain `UNASSESSED` or `UNKNOWN`.

Lifecycle transitions require governing evidence. Authority, function,
temporal content, and load policy are independently re-qualified when evidence
changes.
