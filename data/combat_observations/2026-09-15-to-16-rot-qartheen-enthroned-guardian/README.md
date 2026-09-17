# Phase 1 — Qartheen Enthroned Guardian evidence (2026-09-15 to 2026-09-16)

This directory is the **normalization-only checkpoint** for ten directly uploaded Realm of Thrones battle-result screenshots. The operator upload establishes **Qartheen Enthroned Guardian** as the dedicated empirical target, but Phase 1 publishes no performance verdict.

## Scope

- Source screenshots: **10**
- Unique battles: **10**
- Final victories: **10**
- Field battles: **9**
- Siege attacks: **1**
- Internal same-battle duplicates: **0**
- Ordinary troop rows retained: **79**
- Character rows retained outside ordinary rankings: **74**
- Partially clipped ordinary rows: **2**
- Game track/version: `realm_of_thrones` / `1.4.x`

## Normalization rules

Columns are `survivors, kills, upgrade_ready, deaths, wounded, routed`. Visibly blank numeric cells are zero; clipped cells are `null` and are never imputed. Characters are retained as source evidence and excluded from ordinary troop rankings. Field and siege attack remain separate.

Every source PNG is pinned by exact SHA-256 and byte size. Raw PNG bytes are not committed; the deterministic normalized archive, member hashes, host-upload provenance, and rebuild instructions are committed instead.

Historical exact-hash search was unavailable because the GitHub code-search connector returned HTTP 502. The source dates are later than every merged screenshot batch, and a full visual audit found ten distinct final results, so Phase 1 records a low-risk external-search limitation rather than inventing a clean search result.

## Phase boundary

Phase 2 must verify the archive and hashes, keep normalized evidence immutable, resolve identities conservatively against the pinned track audit, analyze all visible player-side ordinary troops, perform the Qartheen focus deep dive, update the authoritative queue, and complete the pull-request merge gates.
