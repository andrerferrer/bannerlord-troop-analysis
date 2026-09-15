# Phase 1 — ROT mixed campaign screenshots (2026-09-12 to 2026-09-14)

This directory is a **normalization-only checkpoint** for 16 uploaded screenshots grouped into 15 battle events.

## Scope and counts

- Source PNGs: **16**
- Unique events: **15** (`16 files - 1 extra view of the same 2026-09-14 20:57 battle = 15`)
- Final victories: **9**
- Completed `Retreated to the keep!` outside-stage transitions: **3**
- In-progress/right-censored snapshots: **3**
- Field events: **8**
- Siege attacks: **7**

The event partition reconciles as `9 + 3 + 3 = 15`, and the context partition as `8 + 7 = 15`.

## Normalization contract

Columns are `survivors, kills, upgrade_ready, deaths, wounded, routed`. Visible blank numeric cells are zero. Occluded/clipped cells are `null`. Hero upgrade icons are retained as `upgrade_marker_visible` rather than converted into a number. Every visible player-side troop row is preserved, including allied player parties.

The two screenshots at `2026-09-14 20:57:47` and `20:57:51` are one deduplicated battle because duration and both side totals are identical while the scroll positions expose complementary parties.

`Retreated to the keep!` is recorded as a successful completed outside-wall siege stage, not a defeat. Active snapshots remain right-censored.

## Files

- `source_manifest.json` — source filenames, SHA-256, byte sizes, timestamps, dimensions, and event links.
- `source_inventory.csv` — compact review inventory.
- `normalized/events.jsonl` — one record per unique battle event.
- `normalized/party_summaries.jsonl` — player-side party totals and row-coverage deltas.
- `normalized/player_rows.jsonl` — all visible player-side rows.
- `integrity_report.json` — deterministic validation output.
- `phase1_checkpoint.json` / `batch_state.json` — workflow checkpoint.
- `handoff/ANALYSIS_PROMPT.md` — Phase 2 instructions for a separate downstream agent.
- `handoff/ANALYSIS_TASK_V1.json` — machine-readable Phase 2 task.

## Gate

No performance verdict, tier change, evidence-gate decision, or test-queue mutation is included. Repository policy requires Phase 2 to run under a different downstream analysis agent, so this batch remains in a **draft PR** until that phase is completed.

Raw PNG bytes are not copied into Git. The manifest pins the exact uploaded files by SHA-256; pixel-level reinspection later requires the matching upload.
