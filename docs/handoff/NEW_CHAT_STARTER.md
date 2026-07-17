# New Chat Starter — Bannerlord Troop Analysis

Paste the prompt below into a new ChatGPT conversation that has GitHub access.

---

```txt
Open the GitHub repository:

andrerferrer/bannerlord-troop-analysis

Start by reading these files in order:

1. docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md
2. README.md
3. analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_summary.md
4. analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_assumptions.md
5. analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top20_burst_units_regular_compact.csv
6. analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_findings_2026-06-04.md
7. analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_troop_aggregate_summary.csv
8. analysis/item_validation/2026-06-05_throwing_tooltips/findings.md
9. analysis/item_validation/2026-06-05_throwing_tooltips/item_tooltip_validation_20260605.csv
10. GitHub issue #2

Then summarize:

- the current authoritative general model;
- the current authoritative burst model;
- the current top general troops;
- the current top burst troops;
- the important corrected bugs;
- the remaining open validation question;
- the exact next recommended action.

Important constraints:

- v7.1 general_score remains the baseline for overall battlefield value.
- v7.3 burst_score is a separate first-contact/short-duration context score.
- Do not merge general and burst rankings.
- Do not implement boarding_score.
- Do not merge alternative EquipmentRosters into one loadout.
- Tooltip-validated item damage overrides crafted/proxy damage.
- Do not change the general model without new empirical evidence.
- The current open priority is empirical validation of Battanian Skipari's high burst ranking.

Before changing code or formulas, state which repo files support the proposed change and what uncertainty remains.
```

---

## Current one-paragraph context

The project analyzes official Bannerlord troops from vanilla and War Sails/NavalDLC. v7 fixed roster parsing, crossbow ammo overcount, low-ammo throwing inflation, and several role-classification problems. v7.1 introduced a head-weighted survivability armor proxy. v7.3 uses in-game tooltip-validated throwing damage for a separate burst ranking. Current general top 3: Khan's Guard, Fian Champion, Vanguard Faris. Current burst top 3: Vanguard Faris, Battanian Skipari, Imperial Naute. Issue #2 remains open because Skipari's loadout is validated, but its battle performance still needs controlled empirical testing.
