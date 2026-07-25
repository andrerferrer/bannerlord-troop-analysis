# Bannerlord Troop Analysis

Data-driven troop analysis framework for Mount & Blade II: Bannerlord.

## Start here

For the complete project state, model history, current rankings, validated findings, known limitations, and exact next steps, read:

- [`TODO.md`](TODO.md) — operational next steps and completion criteria
- [`docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md`](docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md)
- [`docs/handoff/NEW_CHAT_STARTER.md`](docs/handoff/NEW_CHAT_STARTER.md)
- [`docs/methodology/ADR-001-combat-image-normalization.md`](docs/methodology/ADR-001-combat-image-normalization.md)

Current authoritative models:

```txt
v7.1 — general battlefield score
v7.3 — tooltip-validated throwing burst score
```

## Combat screenshot pipeline status

The deterministic P0–P8 continuation is implemented locally, but the 2026-07-23 production data remains blocked:

- all 11 committed Base64 parts exist, but the stream contains a missing character, oversized/overlapping parts, and intermediate padding;
- strict reconstruction fails before the exact archive hash gate;
- stripping padding produces SHA-256 `a472fbc0751a2c74440be9bced56af52db0531199786e0f121fc4fa90e5816ee`, not the documented hash, and the output is not a valid XZ stream;
- the source ZIP with SHA-256 `00f83754687fe769fdfdea1bda0b68b4d7801c25195ff803aa1a1b35fa15d69f` was not found locally or in releases;
- no production image review, canonical v2 record, empirical ranking, or model calibration is claimed.

Start with:

- [`docs/combat_observations/CLI.md`](docs/combat_observations/CLI.md)
- [`.agents/skills/analyze-bannerlord-combat-zip/SKILL.md`](.agents/skills/analyze-bannerlord-combat-zip/SKILL.md)
- [`data/combat_observations/2026-07-23/reports/p0_recovery_audit.json`](data/combat_observations/2026-07-23/reports/p0_recovery_audit.json)
- [`data/combat_observations/2026-07-23/reports/execution_state.json`](data/combat_observations/2026-07-23/reports/execution_state.json)
- [`docs/methodology/ADR-002-combat-evidence-storage.md`](docs/methodology/ADR-002-combat-evidence-storage.md)

Run the offline test suite:

```bash
python3 -m unittest discover -v
```

## Portable combat-analysis skill

The repository includes the portable Agent Skill
`analyze-bannerlord-combat-zip`. In Codex, invoke it explicitly with:

```text
$analyze-bannerlord-combat-zip
```

The skill accepts a screenshot ZIP/directory or a normalized combat-observation
input exposed as a local path. It delegates formulas, schemas, matching,
deduplication, validation, and rankings to this repository's CLI.

Host paths, invocation syntax, local version checks, and a safe adapter dry run
are documented in
[`references/platform-adapters.md`](.agents/skills/analyze-bannerlord-combat-zip/references/platform-adapters.md).
No global adapter installation, upload, paid API call, or ChatGPT web plugin
publication was performed.

## Goal

Create an interpretable troop analysis pipeline for vanilla Bannerlord, using XML-exported game data and practical battlefield modeling.

The project should avoid shallow tier lists based only on raw stats. The target is to estimate practical combat value using:

- hits to kill
- expected kills per minute
- melee/ranged split offense
- defensive durability
- reliability and AI usability
- tier-by-tier progression analysis
- empirical battle validation

## Primary target

The main target is vanilla Bannerlord.

Realm of Thrones work is kept only as reference material because it helped develop the methodology.

## Analysis pipeline

```txt
XML export
→ normalization
→ weapon and armor extraction
→ effective damage calculation
→ HTK calculation
→ KPM calculation
→ offense / defense / reliability scoring
→ tier-by-tier rankings
→ empirical validation
```

## Current model direction

The preferred offense model is based on HTK/KPM:

```txt
HTK = effective_enemy_hp / effective_damage
KPM = attempts_per_minute × hit_chance ÷ HTK
```

For troops with both ranged and melee capability, the model separates:

```txt
melee_kpm
ranged_kpm
throwing_kpm
```

Then it blends them according to expected battlefield usage.

## Vanilla output priorities

Because vanilla has fewer troops than overhaul mods, the main output should not only be a final Top 20.

Primary outputs:

- Tier 2 rankings
- Tier 3 rankings
- Tier 4 rankings
- Tier 5 rankings
- Tier 6 rankings
- role-specific rankings
- overall rankings

Tier-by-tier analysis matters because campaign progression depends on what is strong at each upgrade stage.

## Repository layout

```txt
docs/
  handoff/
  methodology/
  vanilla/
  rot_reference/

data/
  vanilla/
  rot_reference/

analysis/
  empirical/
  item_validation/
  model_versions/

scripts/
  export/
  normalization/
  scoring/

research/
```
