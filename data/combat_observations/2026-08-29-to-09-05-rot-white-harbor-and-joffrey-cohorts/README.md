# ROT campaign evidence: White Harbor and Joffrey cohorts

Phase 1 normalization for `Armoury Crate SE 03_09_2026 22_51_42.zip`.

- Input SHA-256: `198e895c17e03a9254c4d23e8611557da05271fec5a466966cffbddb36a9028a`
- Track/version: `realm_of_thrones` / `1.4.x`
- Pipeline/schema: `0.4.0` / `2.0.0`
- Provenance: `GPT-5.6 Pro`, host-vision, prompt `combat-v2`
- Input images: 38
- Independent battles: 27
- Visual same-table duplicates: 3
- Excluded non-evidence images: 8
- Last-readable active/interrupted scoreboards: 2
- Complete player-side ordinary troop occurrences: 355
- Unresolved clipped rows: 3

This commit is deliberately normalization-only. It publishes direct source and screenshot manifests for future deduplication, the explicit review queues, and a deterministic normalized bundle. It does not publish the provisional host-side rankings as completed Phase 2 analysis.

Reconstruct the immutable normalized input with `bundle/README.md`, then follow `handoff/ANALYSIS_PROMPT.md` from a distinct Phase 2 agent.
