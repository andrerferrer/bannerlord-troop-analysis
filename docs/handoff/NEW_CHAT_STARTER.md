# New Chat Starter — Bannerlord Troop Analysis

## Current continuation priority

Before working on model issue #2, inspect `TODO.md` and `data/combat_observations/2026-07-23/reports/execution_state.json`. The 2026-07-23 normalized bundle is corrupt and the exact source ZIP is missing. Do not claim production image review or canonical rankings. Resume by supplying an artifact with one of the recorded exact SHA-256 values and running the reconstruction/validation CLI. v7.1 and v7.3 remain frozen.

Paste the prompt below into a new Codex/agent conversation with access to the
checkout and, if available, the recovered evidence file.

---

```txt
Open the andrerferrer/bannerlord-troop-analysis checkout.

Read, in order:

1. TODO.md
2. data/combat_observations/2026-07-23/README.md
3. data/combat_observations/2026-07-23/bundle/README.md
4. docs/combat_observations/CLI.md
5. data/combat_observations/2026-07-23/reports/execution_state.json
6. data/combat_observations/2026-07-23/reports/p0_recovery_audit.json
7. docs/methodology/COMBAT_IMAGE_NORMALIZATION_RULES.md
8. docs/methodology/ADR-001-combat-image-normalization.md
9. docs/methodology/ADR-002-combat-evidence-storage.md
10. .agents/skills/analyze-bannerlord-combat-zip/SKILL.md

The production normalized bundle is corrupt. Do not weaken its integrity gate
or generate production canonical records from it. Resume only from either:

- source screenshot ZIP SHA-256
  00f83754687fe769fdfdea1bda0b68b4d7801c25195ff803aa1a1b35fa15d69f
- normalized archive SHA-256
  10446ce7afb01ec35211c06468812bf2fa3d53e6091f128a7ec67ca605dea2aa

If one exact-hash artifact is available, use the documented CLI or
$analyze-bannerlord-combat-zip to verify it, resume image/review work, build
canonical v2 outputs, validate them, and only then run empirical comparisons.
If neither is available, report COMPLETE_WITH_EXTERNAL_BLOCKERS and do not
repeat bounded recovery searches already recorded in p0_recovery_audit.json
unless new evidence exists.

Keep v7.1 general and v7.3 burst separate and frozen. Do not integrate the Wavey
melee-engine branch or change formulas without new medium/high canonical
evidence and explicit user direction.
```

---

## Current one-paragraph context

The project analyzes official Bannerlord troops from vanilla and War Sails/NavalDLC. v7 fixed roster parsing, crossbow ammo overcount, low-ammo throwing inflation, and several role-classification problems. v7.1 introduced a head-weighted survivability armor proxy. v7.3 uses in-game tooltip-validated throwing damage for a separate burst ranking. Current general top 3: Khan's Guard, Fian Champion, Vanguard Faris. Current burst top 3: Vanguard Faris, Battanian Skipari, Imperial Naute. Issue #2 remains open because Skipari's loadout is validated, but its battle performance still needs controlled empirical testing.
