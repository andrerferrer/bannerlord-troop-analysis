# Weapon-first audit gauntlet

Base: `9311f5596aabc04974d5fe4d7113f1088454143f`.

Operator instruction: execute the weapon comparison, review/fix/retest loop and publication without waiting; the operator will test Yi Ti Mounted Shi meanwhile.

## Acceptance criteria

1. Record `yiti_samurai / field` as the operator-selected active empirical target. This overrides its parked scheduling state, not its missing weapon evidence. Preserve every unrelated queue entry and completed result.
2. Inspect repository-addressable weapon, roster and prior-model sources. Separate direct values, validated reconstructions, templates and unvalidated proxies; never treat them as interchangeable.
3. Compare weapon damage and the corresponding attack speed together, with relevant skills last. Do not invent an unapproved damage-times-speed ranking or measured DPS. Preserve per-usage, per-roster, context and track boundaries.
4. Publish source-pinned extracted observations, a reproducible evidence audit/comparison and explicit unresolved inputs. A partial coverage report must never imply exhaustive all-troop ranking.
5. Run a gauntlet of semantic review, adversarial tests and deterministic regeneration; correct findings and rerun. Record actual tests and limitations, not simulated independent agents.
6. Publish all deliverables in this PR, self-review its final head, merge when these task-specific gates pass and verify the result. Raw battle evidence and frozen model outputs are outside this change.

Initial environment check: the local container cannot resolve github.com for git clone. Authenticated GitHub connector reads/writes work; use supported connector reads and local extracted fixtures without claiming a full checkout or a full repository test run.
