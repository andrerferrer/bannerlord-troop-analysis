# Phase 1 — Qartheen Enthroned Guardian field follow-up (2026-09-16)

This directory is the **normalization-only checkpoint** for two uploaded Realm of Thrones final scoreboards.

## Scope

- Source PNGs: **2**
- Independent battle events: **2**
- Context: **field**
- Result state: **2 completed victories**
- Player party: **Egon Emeros' Party**
- Opponents: **Forim's Party** and **Deserters**
- Visible player-side rows: **31** total = **13 ordinary troops + 18 characters**
- Exact game/mod build: **unknown**

The primary visible troop in both battles is `Qartheen Enthroned Guardian [T6]`, but Phase 1 makes **no performance verdict and no queue mutation**.

## Column contract

The scoreboard columns are normalized as:

```text
survivors, kills, upgrade_ready, deaths, wounded, routed
```

`deployed = survivors + deaths + wounded + routed`.

Blank numeric cells on a fully visible row are normalized as zero. A label hidden by the chat overlay remains unresolved rather than guessed. Lower rows outside the scoreboard viewport are never inferred.

## Reconciliation

- `18:49:55`: visible rows account for all **96** player-party kills and every casualty; **4 survivors** remain offscreen.
- `18:59:05`: visible rows account for all **64** player-party kills and every casualty; **18 survivors** and **2 upgrade-ready counts** remain offscreen.
- One label-occluded ordinary row has the visible numeric pattern `0 survivors / 1 wounded`; its identity is intentionally blank.
- `Dornish Archer [T3]` is retained as a provisional raw transcription because the chat overlay clips the label prefix.

## Raw-source retention

The PNG bytes remain session-local and are not copied into Git. Exact filenames, byte sizes, dimensions, timestamps, SHA-256 hashes, and 64-bit difference hashes are committed. This is permitted by ADR-002 after deterministic normalization, but later pixel-level rereview requires the matching upload.

## Files

- `source_manifest.json` — source provenance and retention status.
- `source_inventory.csv` — compact source inventory.
- `screenshots_manifest.csv` — source-to-battle mapping.
- `normalized/events.jsonl` — battle events and side totals.
- `normalized/party_summaries.jsonl` — visible-row coverage and unaccounted offscreen totals.
- `normalized/player_rows.jsonl` — every visible player-side row.
- `review_queue.csv` — unresolved identity and metadata questions.
- `screenshot_deduplication_audit.csv` — within-batch dedupe and battle-separation decision.
- `correspondence_check.json` / `integrity_report.json` — structural validation.
- `phase1_checkpoint.json` / `batch_state.json` — workflow state.
- `handoff/ANALYSIS_PROMPT.md` / `handoff/ANALYSIS_TASK_V1.json` — Phase 2 contract.
- `bundle/` — deterministic Base64-encoded normalized archive and checksums.
- `source/rebuild_phase1_bundle.py` — deterministic rebuild/check command.

## Phase boundary

The normalized evidence is immutable after this handoff. Phase 2 must be performed by a separate analysis agent on the same branch and pull request, verify the archive and member hashes first, preserve unresolved labels, analyze all visible ordinary rows, compare the Guardian follow-up with the merged Sep 12–14 cohort without silently mixing contexts, and update the authoritative Realm of Thrones queue if the completed evidence changes test status.
