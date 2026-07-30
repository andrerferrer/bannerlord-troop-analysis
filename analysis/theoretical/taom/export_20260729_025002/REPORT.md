# Theoretical analysis — `taom` / `export_20260729_025002`

## Labels

- Evidence basis: `xml_structural` (ADR-004)
- Empirical: `false`
- Model: `role_scores_v1` conservative proxy (not HTK/V4.x/V7.x)
- Combat display gate (≥5 battles / ≥20 troops): applies to empirical
  combat outputs only (ADR-004); this package has zero battle-derived quantities.

## Inputs

- Export: `export_20260729_025002`
- Package digest: `afef4c8483d4d27a228f13c78ed84f89fd624f9e7103d2801b1cec065eee767f`
- Track audit files verified against `artifact_hashes.csv`: 15

## Outputs

- Soldier/troop role rows scored: **1237**
- Entrypoint: `scripts/scoring/generate_vanilla_role_scores.py` (unchanged scoring logic)

## Sanity / anchors

No canonical mod-track control set yet — treat rankings as **proxy-only**. Vanilla CONTROL_IDS do not transfer.

## Limitations

- Crafted melee uses conservative template proxy; no reconstructed HTK.
- Heroes excluded from ordinary soldier scoring inputs via `is_soldier`.
- Intra-track only; do not compare rankings across tracks.
