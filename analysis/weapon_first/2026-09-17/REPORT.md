# Weapon-first audit — 2026-09-17

## Outcome

Full pinned ROT scope: **865 troops**, **1151 alternative rosters**, **1724 melee/unresolved slots**.
**0 verified usage-specific damage/speed pairs**. No skill-based or template-based ranking was substituted.

The operator-selected active test is **Yi Ti Mounted Shi**. Testing may proceed; its selection is explicit, not a claim that the missing weapon data was validated.

## Carried weapons — not a performance order

| Troop | Roster / slot | Item | Family | Damage / matching speed |
|---|---|---|---|---|
| Captain of the Kingsguard | 0 / Item0 | `vlandia_sword_3_t4` | melee | unavailable / unavailable |
| Captain of the Kingsguard | 0 / Item1 | `bracketed_heater_shield` | non_melee | see raw source row; no melee inference |
| Captain of the Kingsguard | 0 / Item2 | `vlandia_lance_3_t5` | melee | unavailable / unavailable |
| Captain of the Kingsguard | 0 / Item3 | `vlandia_2hsword_1_t5` | melee | unavailable / unavailable |
| Norvoshi Grand Bearded Priest | 0 / Item0 | `norvoshi_long_axe` | melee | unavailable / unavailable |
| Norvoshi Grand Bearded Priest | 0 / Item1 | `dorne_sword` | melee | unavailable / unavailable |
| Norvoshi Grand Bearded Priest | 0 / Item3 | `battania_shield_targe_a` | non_melee | see raw source row; no melee inference |
| Sarnori Spider | 0 / Item0 | `khuzait_polearm_1_t4` | melee | unavailable / unavailable |
| Sarnori Spider | 0 / Item1 | `eastern_javelin_3_t4` | thrown | unavailable / unavailable |
| Sarnori Spider | 0 / Item2 | `eastern_javelin_3_t4` | thrown | unavailable / unavailable |
| Sarnori Spider | 0 / Item3 | `eastern_javelin_3_t4` | thrown | unavailable / unavailable |
| Stormlands Thunder Knight | 0 / Item0 | `western_2hsword_t4` | melee | unavailable / unavailable |
| Stormlands Thunder Knight | 0 / Item1 | `vlandia_lance_3_t5` | melee | unavailable / unavailable |
| Yi Ti Mounted Shi | 0 / Item0 | `yiti_sword` | melee | unavailable / unavailable |
| Yi Ti Mounted Shi | 0 / Item1 | `yiti_qinglongji` | melee | unavailable / unavailable |
| Yi Ti Mounted Shi | 0 / Item2 | `empire_throwingknife_t5` | thrown | unavailable / unavailable |
| Yi Ti Mounted Shi | 0 / Item3 | `empire_throwingknife_t5` | thrown | unavailable / unavailable |

Yi Ti carries **two distinct melee weapons** (`yiti_sword` and `yiti_qinglongji`) and **two throwing-knife slots**. Two slots do not establish ammunition quantity, firing frequency, or which weapon the AI used. Its battle kills must not be attributed to the sword alone.

## Evidence and source limits

- Snapshot `9311f5596aabc04974d5fe4d7113f1088454143f`, package `export_20260731_150800`, game version `v1.4.7`. Compatibility with the currently running installation is not independently verified.
- The normalized roster audit and analysis_pack mirrors were checked against the package hashes.
- Crafted composition is available, but no exact weapon physics/profile is supplied by those rows. The existing reconstruction script calls its formula an approximation and requires tooltip validation.
- All 20 preserved V4.4 sensitivity rows were kept outside this comparison; the exact-profile template contains 0 data rows.
- The direct audit retains a generic speed_rating, not separate swing/thrust speed or a full weapon-usage record. It is not copied into both modes.
- Untouched vanilla entries are excluded from the ROT candidate domain. Weapon slots and roster alternatives are retained, never added into a fictional combined loadout.

## Comparator

Verified compatible pairs are compared on damage and matching attack speed together. Improvement in both dimensions gives pairwise dominance; a damage/speed trade-off remains unordered. Different damage types, weapon classes, attack usages, mount states, contexts or profiles remain incomparable. This is not DPS and does not choose a universal troop winner. Skills never repair a missing primary input.

## Reproduce

```bash
python3 -m unittest discover -s tests -p "test_weapon_first_*.py" -v
python3 scripts/analysis/weapon_first_audit.py --repo . --output analysis/weapon_first/2026-09-17
```

The output includes every scoped troop, explicit missing-data requests per weapon, retained legacy priors with rejection reasons, and source hashes. The battle evidence and frozen models remain unchanged.
