# Next troop and context

## Stop the current test

The Lannister Prideknight field test is sufficient:

- battles: `8` (minimum `5`);
- deployed: `19 + 37 + 39 + 53 + 56 + 76 + 93 + 94 = 467`;
- kills: `23 + 50 + 53 + 67 + 28 + 114 + 71 + 88 = 494`;
- kills/deployed: `494 / 467 = 1.057816`;
- player-side kills: `687 + 267 + 677 + 500 + 181 + 248 + 130 + 191 = 2,881`;
- kill share: `494 / 2,881 = 0.171468`;
- share-adjusted impact: `(494 / 467) × (494 / 2,881) = 0.181382`.

No more field Prideknight battles are needed. Siege attack remains a separate
one-battle diagnostic: `42 / 85 = 0.494118`, requiring `5 - 1 = 4` more siege
attacks only if that context is deliberately pursued.

## Next dedicated test

**Test `mallister_knight` (Mallister Eagle Knight) in field battles now.** The
user explicitly chose to retest it, and this supplied batch accidentally tested
Lannister Prideknight instead. The one enemy Eagle Knight at 19:27 is excluded.

Mallister already has incidental compatible history of `8` field battles,
`177` deployed and `165` kills (`165 / 177 = 0.932203`), but not a clean
dedicated cohort. Run a fresh dedicated block:

- `5` independent field battles;
- at least `20` Mallister Eagle Knights deployed per battle;
- practical new minimum: `5 × 20 = 100` deployments;
- make Eagle Knight the only/main T6 melee cavalry and avoid Lannister
  Prideknight or Arryn Winged Knight in the same formation;
- keep the support composition and tactical orders as stable as practical.

The model-derived queue still retains `arryn_moonknight` (Arryn Winged Knight)
after this user-priority retest. Arryn's current compatible field evidence is
`2` battles / `13` deployed / `12` kills, so it remains `5 - 2 = 3` battles and
`20 - 13 = 7` deployments below the display gate.
