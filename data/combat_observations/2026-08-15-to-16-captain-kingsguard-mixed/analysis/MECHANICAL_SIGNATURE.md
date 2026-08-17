# Mechanical signature and next-candidate decision

This is a descriptive audit comparison, not a combat model and not causal evidence.

The canonical `mounted_kingsguard` is level 31 cavalry with OneHanded/TwoHanded/Polearm **270/270/270**, Riding **250**, Athletics **270**, armor total **211**, a **370 HP** shield, horse speed/charge **64/32**, and harness armor **80**. Its loadout audit combines a one-handed sword, shield, two-handed polearm/lance, and two-handed sword. The versioned equipment audit identifies the Western Destrier at speed 64, maneuver 68, charge 32 and extra health 60. Crafted weapon stats remain `not_reconstructed`; no damage, speed, or hit-to-kill claim is made.

Mechanically, the audited combination supports a cautious interpretation: unusually high multi-mode melee and athletics, mounted mobility, a shield, and high rider/horse protection make the unit flexible across mounted and dismounted phases. This is a plausible mechanism, not proof that these properties caused the observed kills or survival.

`goldcloak_master_archer` is level 26 ranged infantry with Bow 140, OneHanded 110, Athletics 120 and armor total 141. The direct equipment audit records item `glen_ranger_bow` (display name `Longbow`; speed 85, missile speed 70, accuracy 88, length 111, thrust/pierce 51) and two 32-arrow bodkin stacks. Again, this describes capacity and does not establish causality.

## Deterministic neighbor rule

For each requested candidate, distance is the sum of absolute Captain differences divided by fixed scales: OneHanded/40, TwoHanded/50, Polearm/40, Riding/20, Athletics/50, armor/40, shield HP/100, harness armor/20, horse speed/10, horse charge/20, plus 0.75 for each symmetric-difference crafted template and 0.5 for a throwing-loadout mismatch. Lower is more similar. This one-off descriptive rule did not edit `analysis/model_versions/` and is not used as an effectiveness score.

Arryn Winged Knight ranks first at **5.250000** and is the next dedicated test: its existing field evidence is only 2 battles/13 deployed, and its exact-context siege-attack evidence totals only 2 battles/11 deployed. Mallister Eagle Knight is the closest tested contrast (rank 2, 5.925000), but is not next because its compatible field and siege-attack evidence already clear the gate. See `candidate_similarity.csv` for the full ranking.

Audit SHA-256: `589bbbea64e78c912a8b3d5f484177473c4618dd45af55609a262075b4fec540` roster summary; `ec46e71b1c877c9ec4ed0fa1b4649496f7e9f0ebc8bd247ec035a476a1a9d3ce` tree tiers; `e08edca636e27df34fbb00fb7d6fc6f83f974846374fb286740460aa540a678f` equipment; `63ea983998e25aa0e6f8c0747bf42e44440f695bbe1fec717074e7ba64e42810` troops.
