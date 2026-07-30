# ADR-004 — XML-structural theoretical analysis is not combat evidence

## Status

Accepted (2026-07-29).

## Context

AGENTS.md lists mandatory analytical boundaries that include a minimum display
gate (≥5 independent battles and ≥20 deployed troops), side separation, and
battle-context separation. Those rules protect **empirical combat** rankings.

Separately, the repo publishes ordered XML audit SSOTs (`xml_ssot_package`) and
may run **theoretical** role/score models over those audits (loadout/skills/
tiers). That work produces no battle-derived quantities.

Without a scoped carve-out, executors either (a) wrongly apply the combat
display gate to XML-only outputs, or (b) waive the gate by plan fiat.

## Decision

1. The AGENTS.md display gate, side separation, and battle-context separation
   apply to **empirical combat outputs** only (batches governed by
   `bannerlord-analysis-task:v1` / ADR-002).
2. XML-structural / theoretical outputs are governed instead by:
   - machine-readable `evidence_basis=xml_structural` and `empirical=false`;
   - heroes excluded from ordinary troop rankings;
   - no silent track mixing;
   - provisional labels are never treated as canonical XML IDs;
   - no join of these rows into empirical ranking tables.
3. Theoretical outputs live under `analysis/theoretical/<track>/<export_id>/`
   and are **outside** `bannerlord-analysis-task:v1` (no protocol comment, no
   combat handoff prompt).
4. An `xml_ssot_package` is **not** an ADR-002 “normalized” combat evidence
   package. Prefer that name (or `audit_package`) over “pacote normalizado”.

## Consequences

- Fase B theoretical reports cite this ADR instead of claiming gates “do not
  apply” without governance.
- Future agents must not treat `analysis/theoretical/` as analysis-queue input.
- Combat batches remain fully bound to AGENTS.md empirical gates.
