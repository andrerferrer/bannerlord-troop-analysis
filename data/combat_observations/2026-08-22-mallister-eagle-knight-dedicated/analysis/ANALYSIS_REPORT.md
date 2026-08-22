# Phase 2 analysis — combat_2026-08-22_mallister_eagle_knight_dedicated

## Result

The dedicated Mallister Eagle Knight field retest is **complete and below the target's prior incidental estimate**. Five independent field battles and 159 new deployments clear the repository display gate.

All 18 supplied images were audited before extraction. Eleven are historical duplicates and were skipped: the two Stark captures already normalized in PR #78 and the nine Lannister captures already normalized in PR #80. The remaining seven Mallister captures are new independent battles.

## New accepted evidence

- 7 battles: 5 field, 2 siege attack.
- 6 final scoreboards and 1 readable active/right-censored Eyrie scoreboard.
- 78 visible player-party ordinary-troop rows.
- Verified positive player-side kill totals in all 7 battles.
- 22 distinct troop labels; 17 exact canonical IDs and 5 conservative unresolved labels.
- 4 field troop/context rows clear the 5-battle / 20-deployed gate; no siege row clears it.

## Reliable field ranking

| Reliable rank | Complete efficiency rank | Impact rank | Troop | Battles | Deployed | Kills | Kills/deployed | Player-side kill share | Share-adjusted impact | Casualty rate |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | Ravens' Teeth [T6] | 5 | 170 | 281 | 1.653 | 27.3% | 0.451 | 1.8% |
| 2 | 7 | 3 | Mallister House Guard [T5] | 5 | 153 | 179 | 1.170 | 17.4% | 0.204 | 6.5% |
| 3 | 12 | 13 | Mallister Knight [T5] | 5 | 37 | 30 | 0.811 | 2.9% | 0.024 | 16.2% |
| 4 | 14 | 6 | Mallister Eagle Knight [T6] | 5 | 159 | 102 | 0.642 | 9.9% | 0.064 | 28/159 = 17.6% |

Complete-table ranks include below-gate diagnostics; reliable ranks include only rows that clear the gate.

## Mallister Eagle Knight deep dive

### Dedicated field retest

- deployed: `12 + 12 + 43 + 46 + 46 = 159`
- kills: `6 + 11 + 12 + 21 + 52 = 102`
- efficiency: `102 / 159 = 0.641509`
- verified player-side kills: `211 + 307 + 102 + 124 + 285 = 1,029`
- kill share: `102 / 1,029 = 0.099125`
- share-adjusted impact: `0.641509 × 0.099125 = 0.063590`
- deaths: `9 / 159 = 0.056604`
- casualties: `(9 + 19) / 159 = 0.176101`
- 95% battle bootstrap interval: `0.352941–1.031250`
- reliable efficiency rank: **4/4**
- complete-table efficiency rank: **14/18**
- complete-table impact rank: **6/18**

The last field battle produced 52 of the 102 kills. The other four produced 50 kills from 113 deployments (`0.442478`), so the pooled result is not a stable high-output signature hidden by one bad fight; it is a low-to-moderate baseline with one strong spike.

### Historical comparison

The prior compatible field evidence was incidental/co-observational:

- prior: `165 / 177 = 0.932203` across 8 battles
- dedicated retest: `102 / 159 = 0.641509` across 5 battles
- change: `-0.290694` kills/deployed, **31.2% lower**
- compatible combined estimate: `267 / 336 = 0.794643` across 13 battles

The dedicated block is the more relevant estimate for the intended test protocol. The compatible combined estimate remains useful as a broad campaign descriptor, but it does not erase the protocol difference.

Compared with the Lannister Prideknight field result from PR #80 (`1.057816` kills/deployed, `17.1468%` kill share, `0.181382` impact), Prideknight delivered **1.65×** the efficiency and **2.85×** the share-adjusted impact of this dedicated Eagle Knight block.

### Siege diagnostic

Two siege attacks provide 55 deployments and 59 kills:

- efficiency: `59 / 55 = 1.072727`
- verified player-side kills: `555 + 365 = 920`
- kill share: `59 / 920 = 0.064130`
- share-adjusted impact: `0.068794`
- casualties: `9 / 55 = 0.163636`

This remains below gate and includes one right-censored active Eyrie scoreboard. It is a diagnostic only, not a siege conclusion.

## Decision

**Stop testing Mallister Eagle Knight in the field.** The dedicated evidence gate is satisfied. It is not Captain-like, not an S-tier field carry, and not competitive with Prideknight on contribution. In this batch Ravens' Teeth and Mallister House Guard are the materially stronger Mallister-side performers.

## Next test

Run **Arryn Winged Knight** next: five independent field battles, at least 20 per battle, Arryn Winged Knight as the only/main T6 melee cavalry, stable support and orders, and no siege screens in the dedicated block.

## Limitations

These are descriptive campaign observations, not causal equipment tests. Army composition, enemies, terrain, orders, reinforcement timing, and partial row visibility remain confounders. The active Eyrie scoreboard is right-censored. Historical kill-share denominators were not reconstructed, so the compatible 13-battle join reports efficiency and casualties only.
