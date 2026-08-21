# Next troop and context

## Current focus gate

The Stark Sworn Sword field test is sufficient for descriptive display:

- battles: `5` (minimum `5`);
- deployed: `25 + 62 + 61 + 39 + 68 = 255` (minimum `20`);
- kills: `29 + 130 + 136 + 108 + 100 = 503`;
- kills/deployed: `503 / 255 = 1.972549`;
- explicit player-side kills: `140 + 486 + 591 + 378 + 361 = 1,956`;
- kill share: `503 / 1,956 = 0.257157`;
- share-adjusted impact: `(503 / 255) × (503 / 1,956) = 0.507256`.

The siege-attack context is not sufficient: `4` battles and `191` deployed. It
already clears deployment but needs exactly `5 - 4 = 1` additional independent
siege attack. Its diagnostic-only totals are `190 / 191 = 0.994764` kills per
deployed and `190 / 1,499 = 0.126751` player-side kill share.

## Next distinct troop

**Test `arryn_moonknight` (Arryn Winged Knight) in field battles.** The versioned
mounted-melee screen ranks it first among not-yet-gate-clearing near matches to
the validated Captain of the Kingsguard signature, with descriptive distance
`5.250000`. The closer observed alternative, Mallister Eagle Knight, already
clears the field gate and is therefore a contrast rather than the next target.

Arryn currently has `2` compatible field battles and `13` deployed. The minimum
field extension is therefore:

- battles: `5 - 2 = 3` additional independent field battles;
- deployed: `20 - 13 = 7` additional deployed across those battles.

Practical target: bring at least 20 Arryn Winged Knights in each of three new
field battles. This comfortably clears both deficits without pooling siege data.

Sources: `docs/methodology/008_archer_like_mounted_melee_field_screen.md`,
`analysis/candidates/realm_of_thrones_archer_like_mounted_melee_field.csv`,
`data/combat_observations/2026-08-15-to-16-captain-kingsguard-mixed/analysis/candidate_similarity.csv`,
and `analysis/historical_reanalysis_v04/historical_kill_share_rankings.csv`.
