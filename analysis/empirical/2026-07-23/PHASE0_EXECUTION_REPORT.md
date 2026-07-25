# Phase 0 execution report — 2026-07-23 combat batch

## Status

Phase 0 high-impact review is complete. The dataset is suitable for exploratory player-side reporting under the five-battle gate, but canonical troop-ID resolution and lower-priority review remain open.

## Verified source artifacts

### Screenshot ZIP

```text
SHA-256: 00f83754687fe769fdfdea1bda0b68b4d7801c25195ff803aa1a1b35fa15d69f
Screenshots: 60
```

### Normalized archive

```text
SHA-256: 10446ce7afb01ec35211c06468812bf2fa3d53e6091f128a7ec67ca605dea2aa
```

Both hashes match the values recorded by the original normalization work. This removes the previous source-recovery blocker and allows image-backed review.

## Methodological changes

### Five-battle gate

The minimum display threshold changed from three to five independent battles. The deployed threshold remains 20.

```text
minimum_battles = 5
minimum_deployed = 20
```

The stricter gate is intended to remove estimates driven by only three or four battle outcomes. It does not make five-battle estimates definitive; uncertainty intervals remain mandatory.

### Player-side baseline

Primary campaign rankings use only the player's side. Enemy-side rows are preserved for future matchup and defeat-side analysis.

### Battle-level uncertainty

Bootstrap intervals resample consolidated battle × troop rows. Raw OCR rows and individual soldiers are not treated as independent observations.

## Manual P0 review

The five-battle impact triage identified 50 P0 rows: player-side rows with uncertain core values that could affect troops at or near the display gate.

| Result | Rows |
|---|---:|
| Reviewed against source screenshot | 50 |
| Corrected | 28 |
| Confirmed without value change | 22 |
| Remaining P0 | 0 |

Every review record preserves original values, reviewed values, changed fields, source, reviewer, date, and a review note. The raw first-pass JSONL remains unchanged.

Examples of material corrections include:

- Queen's Man survivor, kill, and wounded values across multiple battles;
- Rhoynar Bahriyyah survivor, kill, and wounded values;
- Dragonstone Elite Halberdier wounded count;
- Stormlands Heavy Crossbowman deaths and wounded counts;
- Stormlands Elite Maceman survivor count;
- several Rhodok troop kill counts.

The complete row-level audit is in `p0_manual_corrections.csv`.

## Alias review

Two conservative aliases were approved:

| OCR/provisional slug | Canonical provisional slug | Basis |
|---|---|---|
| `stormlands_heavy_crossbowmant5` | `stormlands_heavy_crossbowman_t5` | Same visible troop name; missing separator before tier |
| `free_folkaxeman_t3` | `free_folk_axeman_t3` | Same visible troop name; missing word separator |

The OCR artifact `f_ta_gua` / `f_t_a_gua` remains unresolved and is not treated as a verified troop identity.

These are provisional canonical slugs. Final game/XML troop IDs still require track-audit matching.

## Before-and-after sample

| Measure | Before P0 review | After P0 review and safe aliases |
|---|---:|---:|
| Strict player-side occurrences | 406 | 456 |
| Independent battles | 39 | 40 |
| Provisional troop identifiers | 191 | 190 |
| Overall eligible labels | 19 under five-battle pre-review baseline | 23 |
| Field eligible labels | 13 | 17 |
| Siege-attack eligible labels | 0 | 2 |
| Siege-defense eligible labels | 0 | 0 |

The review materially changed the analyzable population. This validates the decision not to recalibrate models from the unreviewed first pass.

## Current review queue

| Tier | Meaning | Remaining rows |
|---|---|---:|
| P0 | High-impact player-side rows affecting the current display gate | 0 |
| P1 | Player-side core uncertainty below the current display gate | 94 |
| P2 | Enemy-side, undefined-context, secondary-impact, or otherwise lower-priority rows | 487 |
| **Total** |  | **581** |

The next image-backed work item is the 94-row P1 queue.

## Current five-battle baseline

### Overall — leading point estimates

| Rank | Troop | Battles | Deployed | Kills/deployed | 95% battle-bootstrap interval |
|---:|---|---:|---:|---:|---:|
| 1 | Captain of the Kingsguard [T6] | 7 | 31 | 4.516 | 1.581–9.031 |
| 2 | Celtigar Banneret [T6] | 7 | 169 | 2.444 | 0.811–3.300 |
| 3 | Baratheon Hammerknight [T6] | 5 | 159 | 2.358 | 1.129–3.770 |
| 4 | Rhoynar Bahriyyah [T5] | 16 | 253 | 2.178 | 1.435–2.932 |
| 5 | Water Gardens Sentinel [T6] | 14 | 105 | 2.095 | 1.529–2.613 |
| 6 | Queen's Man [T6] | 17 | 313 | 2.064 | 1.429–2.649 |
| 7 | Elite Hired Crossbow [T5] | 7 | 38 | 2.000 | 1.222–2.813 |
| 8 | Stormlands Elite Maceman [T5] | 5 | 75 | 1.893 | 1.167–2.452 |
| 9 | Dragonstone Elite Halberdier [T5] | 15 | 388 | 1.887 | 1.355–2.548 |
| 10 | Reach Flower Knight [T6] | 14 | 117 | 1.872 | 1.119–3.124 |

The first-place estimate remains highly uncertain because only 31 troops were deployed over seven battles. Point-estimate rank must not be read as proof of superiority.

### Field

Seventeen labels meet the display gate. The leading point estimates are Captain of the Kingsguard, Reach Flower Knight, Queen's Man, Water Gardens Sentinel, Dragonstone Elite Halberdier, and Rhoynar Bahriyyah.

### Siege attack

Only two labels currently meet the five-battle gate:

| Troop | Battles | Deployed | Kills/deployed | 95% interval |
|---|---:|---:|---:|---:|
| Rhoynar Bahriyyah [T5] | 6 | 101 | 2.446 | 1.703–3.444 |
| Stormlands Heavy Crossbowman [T5] | 7 | 228 | 1.289 | 0.773–1.726 |

### Siege defense

No label meets the gate. Additional siege-defense data is required before ranking.

## Gate decision

### Approved

- exploratory player-side reporting;
- five-battle eligibility filtering;
- context-specific descriptive comparisons;
- battle-bootstrap uncertainty intervals;
- continued image-backed review and alias resolution.

### Not approved yet

- universal tier-list claims;
- causal attribute weights;
- frozen-model recalibration;
- matchup claims without opponent composition controls;
- battle simulator training.

## Next execution sequence

1. Review the 94 P1 rows.
2. Match provisional troop labels to verified Bannerlord 1.4.x + War Sails IDs.
3. Generate a canonical dataset version.
4. Regenerate baseline and ranking-stability reports.
5. Increase siege-attack and siege-defense coverage.
6. Design controlled speed-versus-damage tests.
