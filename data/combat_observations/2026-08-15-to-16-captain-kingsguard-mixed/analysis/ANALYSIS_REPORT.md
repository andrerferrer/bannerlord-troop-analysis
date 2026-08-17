# Captain of the Kingsguard mixed-context analysis

## Decision

**Close the dedicated field test for `mounted_kingsguard`, but do not assign a universal tier.** The exact-compatible, field-only direct extension has 8 independent battles, 81 deployed and 257 kills (3.172840 kills/deployed), clearing the 5-battle/20-deployed gate. Death rate is 0.037037 and casualty rate 0.209877. The current batch alone has only 3 field battles; the conclusion therefore depends on the explicitly scope-limited 2026-07-23 aggregate extension. No combined bootstrap is possible because the older aggregate does not publish per-battle counts or IDs.

This supports the descriptive classification **validated elite field performer**. It does not support an S/S+ label, universal rank, siege conclusion, or causal claim. All source battles were victories; opponent/army composition, map or siege geometry, difficulty/mod settings, player tactics and other uncontrolled differences remain confounders.

## Focus performance by context

| Troop | Context | Battles | Deployed | Kills | Kills/deployed | Death rate | Casualty rate | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Captain | field, current | 3 | 58 | 133 | 2.293103 | 0.051724 | 0.258621 | below battles |
| Captain | field, compatible combined | 8 | 81 | 257 | 3.172840 | 0.037037 | 0.209877 | passes |
| Captain | siege attack | 4 | 208 | 331 | 1.591346 | 0.052885 | 0.259615 | below battles |
| Captain | siege defense, visible focus row | 1 | 44 | 91 | 2.068182 | 0.159091 | 0.863636 | below battles |
| Gold Cloak Sniper | field, current | 3 | 106 | 102 | 0.962264 | 0.009434 | 0.018868 | below battles |
| Gold Cloak Sniper | field, compatible combined | 4 | 109 | 109 | 1.000000 | 0.018349 | 0.027523 | below battles |
| Gold Cloak Sniper | siege attack | 4 | 223 | 249 | 1.116592 | 0.049327 | 0.224215 | below battles |
| Gold Cloak Sniper | siege defense, visible focus row | 1 | 23 | 48 | 2.086957 | 0.000000 | 0.086957 | below battles |

The two siege-defense battles exist at batch level, but each focus troop is visible in only one final scoreboard. No off-screen row is inferred. Contexts and sides are never pooled, and partial scoreboards preclude whole-army shares.

## Mechanical interpretation and next test

The versioned audits resolve the focus labels to `mounted_kingsguard` and `goldcloak_master_archer`. The Captain's audited 270/270/270 melee skills, Riding 250, Athletics 270, shield, armor 211, protected horse and sword/lance/two-handed-sword flexibility provide a plausible non-causal explanation for mounted/dismounted versatility and survivability. Crafted weapon stats are not reconstructed, so no damage or hit-to-kill mechanism is asserted.

The fixed descriptive neighbor rule ranks Arryn Winged Knight first (distance 5.250000). Its existing evidence is below the gate, whereas rank-2 Mallister Eagle Knight is already gate-clearing and functions as an observed contrast. **Next dedicated candidate: `arryn_moonknight` (Arryn Winged Knight).** Full formula, source hashes and limitations are in `MECHANICAL_SIGNATURE.md` and `candidate_similarity.csv`.

## Boundaries

Only visible player-side ordinary troops enter rankings; heroes and all queued rows are excluded. The reviewed layer resolves eight white icons as non-numeric indicators and leaves three cursor-covered numbers unresolved. Normalized inputs and `analysis/model_versions/` are unchanged.
