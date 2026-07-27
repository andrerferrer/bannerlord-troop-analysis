# Bannerlord combat batch — 2026-07-27

This directory is the shared work envelope for one Realm of Thrones evidence batch. Normalization and analysis remain separate phases, but both phases are completed on the same branch and pull request by different agents.

## Workflow status

| Phase | Owner | Status |
|---|---|---|
| Source retention | local machine with original ZIP | pending Git LFS upload |
| Phase 1: normalization | normalization agent | complete |
| Phase 1: structural validation | normalization agent | complete |
| Phase 1: analysis handoff | normalization agent | complete |
| Phase 2: review and analysis | local analysis agent | pending |
| Final merge gate | reviewer | blocked until Phase 2 completes |

The pull request must remain draft while any pending item above remains incomplete.

## Phase boundary

Phase 1 produced the normalized evidence and stopped before ranking, model comparison, or gameplay conclusions. These normalized artifacts are immutable inputs for Phase 2. Any correction must be added through a separate reviewed correction/exclusion layer with provenance.

The local agent must continue **the same branch and PR** using:

- [`handoff/ANALYSIS_PROMPT.md`](handoff/ANALYSIS_PROMPT.md)
- PR #23
- branch `agent/normalize-combat-batch-2026-07-27-only`

## Coverage

- Game track: `realm_of_thrones`
- Game version family: `1.4.x`
- Source ZIP SHA-256: `42d4adf2e8d9f9bce0dc90945832c673aeddf81d06044cb0e6f08a2ddb852617`
- Screenshots: **13**
- Grouped final battles: **10**
- Battle contexts: **4 field, 5 siege attack, 1 siege defense**
- Active scoreboard excluded: **1**
- Structured observations: **328**
- Player-side ordinary troop observations: **143**
- Review items: **5**
- Structural validation errors: **0**

## Repository contents

- `source/README.md` — exact original source identity and Git LFS publication instructions.
- `screenshots_manifest.csv` — image hashes, timestamps, grouping, and inclusion status.
- `review_queue.csv` — uncertain fields preserved for review rather than guessed.
- `normalization_summary.json` — batch-level counts and provenance.
- `validation_report.json` — structural validation and known limitations.
- `artifact_hashes.csv` — SHA-256 and size for normalized artifacts.
- `bundle/` — reconstructible normalized archive containing:
  - `screenshots.jsonl`;
  - `battles.jsonl`;
  - `troop_occurrences.jsonl`;
  - `primary_troop_occurrences.jsonl`;
  - `troop_battle_consolidated.jsonl`.
- `handoff/ANALYSIS_PROMPT.md` — executable contract for the local analysis agent.
- `review/` — reserved for Phase 2 reviewed decisions.
- `analysis/` — reserved for Phase 2 analytical outputs.

## Integrity

```text
Normalized-only archive SHA-256:
031a7c60d4ed239a2fcb70a81bb6edf047711c3a422ee3ba4420c4a4af534855
```

The source manifest and screenshot hashes are already versioned. The original 18,596,761-byte ZIP must still be pushed from the local machine through Git LFS, or published as an equivalent repository-reconstructible chunk package, before the PR leaves draft state.

## Analytical constraints

- Primary baseline uses player-side ordinary troop rows.
- Player and enemy rows are never pooled.
- Field, siege attack, and siege defense stay separate.
- Reliable display requires **5 independent battles and 20 deployed troops**.
- Heroes are excluded from ordinary troop rankings.
- Off-screen rows are not inferred.
- Provisional slugs are not canonical XML IDs.
- Realm of Thrones data is not mixed with vanilla/War Sails data.
- Frozen model files under `analysis/model_versions/` are not changed by this batch.
