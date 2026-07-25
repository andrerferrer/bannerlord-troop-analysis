# Empirical analysis status

Status: `PRODUCTION_BLOCKED`

No production empirical ranking or model residual was generated. The committed normalized archive fails the exact SHA-256 and XZ integrity gates, and the verified source screenshot ZIP is unavailable. Producing rows from the recorded summary counts would fabricate source-level evidence.

The offline analysis tooling is fixture-tested and keeps the frozen models separate:

- v7.1 remains the authoritative general battlefield model.
- v7.3 remains the authoritative tooltip-validated throwing-burst model.
- evidence grade and sample size are emitted beside every comparison;
- incomplete committed model universes are labeled provisional.

Resume after recovery by building canonical v2, then run `compare-models` against verified v7.1 and v7.3 inputs.
