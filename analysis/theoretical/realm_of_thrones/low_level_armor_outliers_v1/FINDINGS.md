# Realm of Thrones low-level armor outliers

## Result

The Pentoshi T3 observation is confirmed structurally. Within the 138 ordinary,
dismounted T3 infantry/ranged troops in scope, median body-zone armor is 28.
Both `pentoshi_pikeman` and `pentoshi_soldier` have 48:

```text
absolute advantage = 48 - 28 = 20
relative advantage = 20 / 28 = 71.43%
body-zone rank = tied 3rd
body-zone percentile = 98.55
```

The same value is also above the T4 cohort median of 40:

```text
cross-band advantage = 48 - 40 = 8
relative advantage = 8 / 40 = 20%
```

This is why the Pentoshi T3 line looks like a false tier. Its torso protection
is not merely good for T3; it is above the typical T4 in this dismounted screen.

## Pentoshi split

The two T3s use the same `pentoshi_armor` (`Pentoshi Plate`) with 48 body armor,
but they are not defensively identical.

| troop | body | arms | head | legs | shield HP / armor | interpretation |
|---|---:|---:|---:|---:|---:|---|
| Pentoshi Pikeman | 48 | 32 | 39 | 32 | — | balanced worn armor; strongest clean armor outlier |
| Pentoshi Soldier | 48 | 8 | 39 | 28 | 360 / 9 | torso-and-shield specialist with exposed arms |

The Pikeman's strong limbs come from plated boots and bracers. The Soldier
trades that coverage for the shield. They should remain separate empirical
rows even though their body item is identical.

## Highest-value candidates

These are structural test targets, not proven field rankings.

| priority | troop | band | body | arms | head | legs | shield HP / armor | reason |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | Hightower Soldier | T3 | 50 | 12 | 36 | 32 | 350 / 1 | closest replication of the early heavy-body-armor mechanism |
| 2 | Yronwood Man at Arms | T3 | 46 | 31 | 37 | 25 | 345 / 1 | best balanced T3 alternative with both limb coverage and shield |
| 3 | Myrish Crossbowman | T3 | 48 | 10 | 40 | 31 | — | Pentoshi-grade torso armor on a ranged unit |
| 4 | Valyrian Soldier | T3 | 51 | 10 | 36 | 30 | 400 / 7 | highest total body-zone value in the T3 dismounted cohort |
| 5 | Lannister Levy | T2 | 42 | 6 | 32 | 20 | 305 / 1 | extreme cheap-body-armor outlier, but very uneven coverage |

The next controlled test should start with `hightower_soldier`. It tests the
same mechanism as Pentos with even higher body armor. `yronwood_man_at_arms`
should be second because it tests whether balanced coverage beats a larger
torso spike. `myrish_crossbowman` is the third target because survival has a
different payoff for a ranged troop.

## T4 benchmark ceiling

The strongest ordinary T4 dismounted references are:

| troop | body | arms | head | legs | shield HP / armor |
|---|---:|---:|---:|---:|---:|
| Casterly Rock Pikeman | 68 | 47 | 44 | 38 | 400 / 8 |
| Tyrell Man at Arms | 65 | 37 | 37 | 30 | 430 / 1 |
| Qohorik Swordsman | 64 | 41 | 42 | 29 | 380 / 9 |
| Pentoshi Pike Warrior | 64 | 40 | 39 | 32 | 360 / 9 |

These are useful upper controls, not substitutes for the T3 candidate search.

## Evidence boundary

- Source: Realm of Thrones v8.1.6 versioned equipment audit, built 2026-07-31.
- Evidence basis: XML structural; empirical combat evidence is not asserted.
- Alternative rosters use their arithmetic mean.
- Cavalry and horse archers are excluded from this dismounted screen.
- Shield values are displayed but do not affect armor ranks.
- `bracken_archer` remains outside the map because `kg_gloves` is unresolved;
  it is preserved in `review_queue.csv` rather than scored as zero.
