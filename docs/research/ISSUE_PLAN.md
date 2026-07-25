# GitHub issue plan

The execution tracker is decomposed into the following work items:

1. Complete P1 image-backed review of 94 player-side rows.
2. Resolve provisional troop labels to verified Bannerlord 1.4.x + War Sails IDs.
3. Build canonical empirical dataset v1 and validation report.
4. Publish five-battle ranking-stability analysis.
5. Expand siege-attack and siege-defense evidence.
6. Design and execute the controlled weapon-speed versus raw-damage experiment.
7. Integrate canonical empirical rows with troop/equipment features.
8. Fit and validate battle-grouped explanatory models.

Dependencies:

```text
P1 review ─┐
           ├─> canonical dataset v1 ─> descriptive stability report
ID mapping ┘                          └─> feature integration ─> modeling

additional siege collection ─> stronger context-specific reporting
controlled experiments ──────> causal/mechanistic validation
```
