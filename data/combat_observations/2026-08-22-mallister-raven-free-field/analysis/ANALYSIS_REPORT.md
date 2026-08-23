# Phase 2 analysis — Mallister Raven-free field cohort — 2026-08-22

## Result

Four new independent Realm of Thrones 1.4.x field result tables were accepted: three victories and one defeat. Ravens' Teeth are absent, so this cohort directly addresses the suspected ranged-carry contamination. All 32 complete visible player-side ordinary-troop rows were analyzed; one partially clipped Mallister Levy row is retained in review and excluded without reconstruction.

The cohort remains **below the five-battle gate**. Rates are diagnostic until one more Raven-free field battle is supplied.

## Main Raven-free rates

| Troop | Battles | Deployed | Kills | Kills/deployed | Retention | Result |
|---|---:|---:|---:|---:|---:|---|
| Mallister Elite Archer [T5] | 3 | 129 | 302 | 2.341 | 48.8% | below gate |
| Mallister Eagle Knight [T6] | 4 | 234 | 302 | 1.291 | 56.0% | below gate |
| Mallister House Guard [T5] | 4 | 233 | 275 | 1.180 | 41.2% | below gate |
| Mallister Archer [T4] | 3 | 61 | 63 | 1.033 | 90.2% | below gate |
| Mallister Footman [T3] | 4 | 70 | 41 | 0.586 | 60.0% | below gate |

## What isolation changed

- **Mallister Elite Archer became the offensive carry:** `302 / 129 = 2.341` kills per deployed across three visible battles, including `272 / 65 = 4.185` in the defeat.
- **Mallister Eagle Knight improved sharply without Ravens:** `302 / 234 = 1.291`, versus `102 / 159 = 0.642` in the prior Raven-present dedicated field cohort. The diagnostic ratio is `1.291 / 0.642 = 2.01×`.
- **Mallister House Guard remained almost unchanged offensively:** `275 / 233 = 1.180`, versus `179 / 153 = 1.170` previously. This suggests Ravens were suppressing Eagle Knight's opportunity more than House Guard's measured output.
- A different ranged unit immediately absorbed the carry role. Removing Ravens did not remove the ranged structural advantage; it shifted the dominant output to Mallister Elite Archer.

These comparisons are not causal estimates because opponent strength and composition changed. They are strong enough to justify the isolated protocol but not to merge its rates blindly into the earlier cohort.

## Defensive readings

Pressure margins by battle were:

```text
19:52 victory: +25.00 pp
20:11 victory: +80.09 pp
20:19 victory: +95.48 pp
20:32 defeat:  -20.03 pp
```

Mean pressure margin: `45.13%`; median: `52.54%`. These are side-level descriptive values, not credit assigned to a single troop.

House Guard frontline retention was `96 / 233 = 41.20%`. The low aggregate is driven by the complete defeat and by the hard 19:52 victory, where all 61 House Guards became casualties while the army still finished at a +25 pp pressure margin. Under the provisional framework this reads as **low retention with a positive formation result**: potentially sacrificial frontline behavior, not automatically poor defense.

The 20:32 defeat is especially informative: the army reached 466 kills but ended at `0 / 220` allied retention while 117 of 584 enemies remained. High ranged output did not convert the unfavorable battle into a win, which is exactly why offensive efficiency and pressure margin must remain separate.

## Coverage

- complete visible ordinary-troop observations: 32;
- distinct complete troop labels: 13;
- reliable troop/context rows: 0;
- insufficient rows: 13;
- review rows: 1 partially clipped Mallister Levy occurrence;
- context: field only; the Garrison of The Crag battle is retained as field with medium context confidence because the screen is an open-field result but may represent a siege-related sally.

## Stop condition

Run **one more Raven-free field battle** with the same house-centered composition. That gives Eagle Knight and House Guard five independent isolated battles; Elite Archer should be kept present in sufficient numbers if its isolated gate is also intended to close.
