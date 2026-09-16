# Phase 2 handoff — 2026-09-12 to 2026-09-14 ROT mixed campaign

Continue the same branch and pull request. Read repository `AGENTS.md` and `docs/protocols/analysis-task-v1.md` before making changes.

## Immutable Phase 1 inputs

- `phase1_checkpoint.json`
- `batch_state.json`
- `source_manifest.json`
- `source_inventory.csv`
- `screenshots_manifest.csv`
- `normalized/events.jsonl`
- `normalized/party_summaries.jsonl`
- `normalized/player_rows.jsonl`
- `integrity_report.json`
- `bundle/rot_mixed_campaign_phase1.tar.xz.base64`
- `bundle/rot_mixed_campaign_phase1.tar.xz.sha256`

Do not silently rewrite normalized evidence. Record any correction in a reviewed layer with original value, corrected value, reason, and provenance.

## Required interpretation boundaries

1. Keep field and siege-attack observations separate.
2. Keep final results separate from right-censored active snapshots.
3. Treat `Retreated to the keep!` as a successful completed outside-wall siege stage, not a defeat.
4. The two screenshots captured at `2026-09-14 20:57:47` and `20:57:51` are complementary views of one battle, not two samples.
5. Never merge separate re-engagements or cleanup fights.
6. Preserve party-summary visibility deltas and do not infer clipped rows.
7. Exclude heroes/lords/companions from ordinary troop rankings.
8. Analyze every visible player-side ordinary troop/context row; no focus troop may filter the batch-wide analysis.
9. Do not infer a primary tested troop from these mixed campaign rosters.
10. Do not mutate the Realm of Thrones test queue unless the evidence gate and an approved target justify the change.

## Required outputs

Create the reviewed layer and the ordinary Phase 2 analysis outputs under `analysis/`, including validation, complete/reliable rankings, insufficient-evidence coverage, context splits, identity audit, and a human-readable report. Recompute every derived metric from the normalized inputs.

Before marking the PR ready, verify the archive hash, normalized artifact hashes, full eligible-row partition, queue consistency, and all repository tests applicable to the batch. Publish append-only `bannerlord-analysis-task:v1` state comments as work moves from `pending` to `in_progress`, then to `complete` or `blocked`.

## Repaired Phase 1 bundle identity

- Screenshot manifest SHA-256: `42edb4f73e88bad528ff318c019b561ccd3bf02b4151dd714ea08325ed0734dd`
- Archive SHA-256: `99754ec7fb614e86631bd6268c327140cd7c7882db7f612035015a6291b3adab` (12944 bytes, 11 members)
- Base64 text SHA-256: `1fe97af8dd1979f02e4c27b7e26277a80e8bde026ebc6e50d8b989adb24692d6` (17261 bytes, including the final newline)
- Rebuild verification: `python3 source/rebuild_phase1_bundle.py --check` from the batch directory.
- Game version remains `unknown`; do not infer it from neighboring batches.
