# Current candidate audit — context-first scoring

Status: **historical audit only; non-canonical**

No rankings are published by this audit. Historical candidates, theoretical exports,
scoring sources, and frozen model versions are read and hashed but never modified.

## Scope

- Findings: 58
- Protected files: 120
- Baseline manifest SHA-256: `2128641036518bab061e390a8db0d35846a37f91d34f8e41f67c812c1ac5d113`
- Explicit absent artifacts: 4

## Departure counts

| Departure code | Count |
|---|---:|
| `AMMUNITION_POLICY_UNDECLARED` | 4 |
| `ATTACK_MODE_UNDECLARED` | 4 |
| `CONTEXT_UNDECLARED` | 4 |
| `IRRELEVANT_DRIVER_INCLUDED` | 18 |
| `MISSING_VALUE_ZERO_FILLED` | 5 |
| `MOUNTED_INPUT_NON_APPLICABLE` | 4 |
| `MOUNT_STATE_UNDECLARED` | 4 |
| `QUESTION_MIXED` | 7 |
| `SOURCE_ARTIFACT_ABSENT` | 4 |
| `TEMPLATE_PROXY_USED` | 4 |

## Finding inventory

The CSV-shaped table below is the complete reviewed inventory. `false` declaration
fields mean the historical path did not validate that dimension before reading evidence.

```csv
model_or_candidate,source_path,source_sha256,context_declared,question_declared,attack_mode_declared,mount_state_declared,departure_code,field_or_formula,evidence
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,ATTACK_MODE_UNDECLARED,candidate declaration,Melee counterpressure is read without a declared attack mode.
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,CONTEXT_UNDECLARED,candidate declaration,"The candidate is defensive but does not select field, siege attack, or siege defense."
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,counterpressure_component_v2,Maximum melee skill enters defensive utility.
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,harness_component_v2 and mount_health_component_v2,Mounted durability enters a context-undeclared defense candidate.
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,mobility_component_v2,Horse speed/maneuver or Athletics enter defensive utility.
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,shield_armor_component_v2,Shield armor is included without an explicit shield-endurance question.
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,shield_hp_component_v2,Shield endurance is treated as physical protection rather than a separate blocking question.
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,MISSING_VALUE_ZERO_FILLED,"number(value, default=0.0)",Missing/non-finite values are converted to a numeric default in historical feature helpers.
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,MISSING_VALUE_ZERO_FILLED,unresolved non-mount item evidence,"Unresolved armor, shield, or melee item evidence contributes zero while the roster remains scoreable."
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,MOUNTED_INPUT_NON_APPLICABLE,cavalry protection/utility lanes,Mount and harness inputs cannot answer siege-defense defense after dismounting.
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,MOUNT_STATE_UNDECLARED,defensive_lane,Mounted/unmounted lanes replace an explicit context and mount-state declaration.
defensive_role_scores_v2_candidate,scripts/scoring/generate_defensive_role_scores_v2.py,5acbb9e94929e10df67ab3ef03993f4b207126e108233b5301f54e1836eb8aa0,false,false,false,false,QUESTION_MIXED,protection_score_v2 and defensive_utility_score_v2,Protection and utility answer separate questions and utility blends mobility/melee skill.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,AMMUNITION_POLICY_UNDECLARED,direct_throw_raw,Throwing stack amount enters output without a battle-context ammunition policy.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,AMMUNITION_POLICY_UNDECLARED,ranged_raw,Finite stack count is used without a battle-context ammunition policy.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,ATTACK_MODE_UNDECLARED,candidate declaration,"Melee, ranged, throwing, and defense paths are built together."
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,CONTEXT_UNDECLARED,candidate declaration,No track/battle-context declaration is validated before formulas run.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,best item and roster aggregation,Favorable item and roster outputs are selected with max instead of the context-first alternative-equipment mean.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,defense_raw,"Shield HP/armor, harness armor, charge, horse speed, and maneuver enter defense."
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,direct_throw_raw,Direct throwing blends swing/thrust damage with speed rating and stack amount.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,ranged_raw,"Ammunition thrust damage, weapon speed, accuracy, missile speed, and a capped stack bonus enter ranged output."
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,role eligibility and primary_category,"Shield, horse, and normalized defense fields decide whether and where troops rank."
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,skill and mobility factors,"Bow/Crossbow, melee, Throwing, Riding, and horse presence scale role outputs."
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,MISSING_VALUE_ZERO_FILLED,numeric coercion,Parsing uses errors=coerce followed by fillna(0) across score inputs.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,MOUNTED_INPUT_NON_APPLICABLE,has_horse and mobility_factor,Mounted bonuses can enter outputs that are not scoped away from siege defense.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,MOUNT_STATE_UNDECLARED,candidate declaration,Roster horse presence changes formulas without a declared mount-state question.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,QUESTION_MIXED,defensive_role_score,"Defense blends defense, crafted melee, throwing, shield, and horse inputs."
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,QUESTION_MIXED,offensive_melee_role_score,Melee output also includes defense and mounted bonuses.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,QUESTION_MIXED,ranged_role_score,"Ranged output blends offense, defense, mobility, horse, and shield inputs."
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,QUESTION_MIXED,skirmisher_role_score,"Throwing output also includes melee, defense, and mounted bonuses."
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,TEMPLATE_PROXY_USED,melee_proxy(crafting_template),Crafting-template names select fixed invented melee damage values.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,TEMPLATE_PROXY_USED,melee_usability(crafting_template),Crafting-template names select a second invented melee usability multiplier.
role_scores_v1,scripts/scoring/generate_vanilla_role_scores.py,0bada51e5fb830b1f2efcc5f31b0c1ca0844df2ad0363010bc312244fe3d90b3,false,false,false,false,TEMPLATE_PROXY_USED,throw_proxy_raw(crafting_template),Crafting-template names also select invented throwing damage before a fixed multiplier is applied.
v7.1,analysis/model_versions/v7.1/bannerlord_v71_head_weighted_model_all_official_troops.csv,,false,false,false,false,SOURCE_ARTIFACT_ABSENT,general model CSV,"The repository references this v7.1 input, but its bytes are not present in the checkout."
v7.2,scripts/build_v72_burst_score.py,96e1273aa0a0cc00dab6e5fdcebf5cf6cc427f7f7b572a2afa5a70034bbc5e9c,false,false,false,false,AMMUNITION_POLICY_UNDECLARED,throw_ammo_factor and ranged_ammo_factor,Finite ammunition factors are applied without a field/siege policy.
v7.2,scripts/build_v72_burst_score.py,96e1273aa0a0cc00dab6e5fdcebf5cf6cc427f7f7b572a2afa5a70034bbc5e9c,false,false,false,false,ATTACK_MODE_UNDECLARED,"burst_raw=max(throw,ranged,charge,melee)",Four attack families compete inside one output.
v7.2,scripts/build_v72_burst_score.py,96e1273aa0a0cc00dab6e5fdcebf5cf6cc427f7f7b572a2afa5a70034bbc5e9c,false,false,false,false,CONTEXT_UNDECLARED,burst_score_v72,The burst label does not declare track and battle context as a validated tuple.
v7.2,scripts/build_v72_burst_score.py,96e1273aa0a0cc00dab6e5fdcebf5cf6cc427f7f7b572a2afa5a70034bbc5e9c,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,primary_throw_damage_type/category/has_crossbow,Damage type and troop/category labels apply secondary type multipliers.
v7.2,scripts/build_v72_burst_score.py,96e1273aa0a0cc00dab6e5fdcebf5cf6cc427f7f7b572a2afa5a70034bbc5e9c,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,reliability_score and defense_score_v71,Non-offensive composite drivers enter the burst score.
v7.2,scripts/build_v72_burst_score.py,96e1273aa0a0cc00dab6e5fdcebf5cf6cc427f7f7b572a2afa5a70034bbc5e9c,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,throw_pressure_v7/ranged_kpm_v7/charge_impact_score_v7/melee_kpm_eff_v7,"Opaque throwing, ranged, charge, and melee composite inputs drive the four burst families."
v7.2,scripts/build_v72_burst_score.py,96e1273aa0a0cc00dab6e5fdcebf5cf6cc427f7f7b572a2afa5a70034bbc5e9c,false,false,false,false,MISSING_VALUE_ZERO_FILLED,burst inputs,Missing damage/ammunition/reliability/defense values are filled with zero.
v7.2,scripts/build_v72_burst_score.py,96e1273aa0a0cc00dab6e5fdcebf5cf6cc427f7f7b572a2afa5a70034bbc5e9c,false,false,false,false,MOUNTED_INPUT_NON_APPLICABLE,mounted_throw_bonus,The mounted bonus has no siege-defense dismount boundary.
v7.2,scripts/build_v72_burst_score.py,96e1273aa0a0cc00dab6e5fdcebf5cf6cc427f7f7b572a2afa5a70034bbc5e9c,false,false,false,false,MOUNT_STATE_UNDECLARED,mounted_throw_bonus,Mounted state is inferred from input rather than declared before scoring.
v7.2,scripts/build_v72_burst_score.py,96e1273aa0a0cc00dab6e5fdcebf5cf6cc427f7f7b572a2afa5a70034bbc5e9c,false,false,false,false,QUESTION_MIXED,burst_score_v72,Burst offense is blended with reliability and v7.1 defense.
v7.2,analysis/model_versions/v7.2_burst_score/bannerlord_v72_burst_model_all_official_troops.csv,,false,false,false,false,SOURCE_ARTIFACT_ABSENT,full burst model CSV,"The v7.2 builder publishes this full model output, but its bytes are not present in the checkout."
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,AMMUNITION_POLICY_UNDECLARED,throw_ammo_factor_v73,Finite ammunition is used without a field/siege policy.
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,ATTACK_MODE_UNDECLARED,burst_source_v73,"Throw, ranged, charge, and melee sources compete inside one output."
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,CONTEXT_UNDECLARED,burst_score_v73,The burst label does not declare track and battle context as a validated tuple.
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,ranged_burst_raw_v72/charge_burst_raw_v72/melee_burst_raw_v72,Opaque v7.2 composite families are carried into v7.3.
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,reliability_score and defense_score_v71,Reliability and defense composites enter the final burst score.
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,throw_damage_type_factor_v73,Damage type applies a secondary multiplier outside the base context-first attack candidate.
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,IRRELEVANT_DRIVER_INCLUDED,throw_skill_factor_v73,Throwing skill scales output without a declared secondary-driver candidate.
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,MISSING_VALUE_ZERO_FILLED,burst inputs,Missing damage/ammunition/reliability/defense values are filled with zero.
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,MOUNTED_INPUT_NON_APPLICABLE,mounted_throw_bonus_v73,The mounted bonus has no siege-defense dismount boundary.
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,MOUNT_STATE_UNDECLARED,mounted_throw_bonus_v73,Mounted state is inferred rather than declared before scoring.
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,QUESTION_MIXED,burst_score_v73,Burst offense is blended with reliability and v7.1 defense.
v7.3,analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_tooltip_damage_burst_model_all_official_troops.csv,,false,false,false,false,SOURCE_ARTIFACT_ABSENT,full tooltip-damage burst model CSV,"The v7.3 builder publishes this full model output, but its bytes are not present in the checkout."
v7.3,analysis/model_versions/v7.2.1_tooltip_throw_validation/bannerlord_v721_tooltip_throw_model_all_official_troops.csv,,false,false,false,false,SOURCE_ARTIFACT_ABSENT,v7.2.1 tooltip-throw input model CSV,"The v7.3 builder declares this model CSV as its required input, but its bytes are not present in the checkout."
v7.3,scripts/build_v73_tooltip_damage_burst.py,5e271377113963f2bfce019d326bb1e4c486a15febe9c37f9d4ec6cd044645dd,false,false,false,false,TEMPLATE_PROXY_USED,throw_damage_source_v73=model_proxy,Missing tooltip damage falls back to primary model proxy damage.
```

## Interpretation boundary

These findings explain why the historical paths are not defaults for new scoring.
They do not invalidate historical reproduction, change any old rank, or establish a
replacement ranking. Later context-first slices must verify
`historical_baseline_hashes.csv` before publishing candidate output.
