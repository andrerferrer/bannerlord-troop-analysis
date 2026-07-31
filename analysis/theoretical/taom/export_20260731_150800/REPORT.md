# Theoretical analysis — `taom` / `export_20260731_150800`

## Labels

- Evidence basis: `xml_structural` (ADR-004)
- Empirical: `false`
- Model: `role_scores_v1` conservative proxy (not HTK/V4.x/V7.x)
- Combat display gate (≥5 battles / ≥20 troops): applies to empirical
  combat outputs only (ADR-004); this package has zero battle-derived quantities.

## Inputs

- Export: `export_20260731_150800`
- Package digest: `9444e75330ea380c75a06492e6b9b4cbda89582223e079437ba48d976f547db4`
- Track audit files verified against `artifact_hashes.csv`: 15

## Outputs

- Soldier/troop role rows scored: **1239**
- Entrypoint: `scripts/scoring/generate_vanilla_role_scores.py` (unchanged scoring logic)

## Sanity / anchors

No canonical mod-track control set yet — treat rankings as **proxy-only**. Vanilla CONTROL_IDS do not transfer.

## Limitations

- Crafted melee uses conservative template proxy; no reconstructed HTK.
- Heroes excluded from ordinary soldier scoring inputs via `is_soldier`.
- Intra-track only; do not compare rankings across tracks.
