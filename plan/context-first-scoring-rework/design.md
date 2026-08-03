# Context-First Scoring Rework — Software Design

## 1. Purpose and scope

This design implements the approved PRD in `plan/context-first-scoring-rework/prd.md` and the standing rules in `docs/methodology/006_context_first_scoring_rules.md`. It replaces the default path for new candidate scoring with a declaration-driven pipeline while preserving every historical candidate and every frozen model byte for byte.

The base candidate answers only three questions:

- defense: worn armor;
- attack: validated direct melee or bow/crossbow output;
- general capability: the defense and attack components side by side.

The base candidate does not use speed, troop skill, weapon skill, reach, damage type multipliers, shields, mounts, harnesses, charge, reliability, perks, mobility, or a default general-capability blend. `mount_state` remains a required context selector, but mount attributes never become score inputs. Throwing weapons, slings, and other ranged families are unsupported by this candidate and are reported as unrankable instead of being mapped to the bow/crossbow formula.

All implementation PRs target `main`. The repository default remote branch is `origin/main`; `dev` is not part of this delivery.

## 2. Current-state diagnosis

### 2.1 Existing scoring paths answer broader or different questions

`scripts/scoring/generate_vanilla_role_scores.py`:

- zero-fills numeric parse failures through pandas coercion;
- mixes worn armor, shields, mounts, harnesses, movement, skills, and offensive proxies;
- picks favorable roster outputs with `max`;
- uses crafting-template classes as melee damage proxies;
- includes speed, accuracy, missile speed, and ammunition caps in ranged output;
- normalizes and blends before a context, question, attack mode, or mount state is declared.

`scripts/scoring/generate_defensive_role_scores_v2.py` is reproducible but historical. It:

- mixes armor with shield and mounted durability in protection;
- adds mobility and melee skill to defensive utility;
- divides populations into mounted and unmounted lanes rather than selecting battle context first;
- converts unresolved non-mount item evidence to a documented proxy zero;
- writes directly into the candidate directory.

The frozen v7.1, v7.2, and v7.3 paths contain general/burst blends, reliability, damage type, mounted, charge, speed, and other drivers that are explicitly outside this candidate. They remain evidence to audit, not code to reuse or alter.

The checkout contains committed v7.2/v7.3 summaries and compact outputs, but no
v7.1 file and no full v7.3 model CSV even though scripts and documentation
reference them. D1 records those absent repository artifacts as explicit
`SOURCE_ARTIFACT_ABSENT` audit findings and audits the surviving formulas and
derivative columns; it does not invent or retrieve missing model bytes. The
v7.3 builder also falls back from tooltip damage to `primary_throw_damage`
(`model_proxy`) and blends skill, ammunition, mounted, damage-type, reliability,
and v7.1 defense fields, all of which are departures from the new base model.

### 2.2 Useful existing patterns

The new path should reuse these verified repository conventions:

- `survivability_armor_v71 = 0.35*head + 0.55*body + 0.05*arm + 0.05*leg`;
- ordinary-troop filtering by `is_soldier`, `is_hero`, and `mp_` identity;
- mod-track filtering through the versioned `<track>_override_report.csv`;
- arithmetic means for alternative equipment and roster choices;
- six-decimal publication with rank ties determined at published precision;
- UTF-8, LF line endings, explicit CSV field order, sorted JSON keys, and SHA-256 manifests;
- deterministic crafted reconstruction from `scripts/normalization/reconstruct_crafted_weapon_stats.py`;
- battle-level aggregation and deterministic bootstrap uncertainty;
- stable, explicit review queues and non-zero exits for structurally unsafe runs.

### 2.3 Input contracts available today

The versioned track audits expose:

- troop equipment:
  `troop_id, roster_index, slot, item_id, equipment_source, item_found, item_kind, type, item_name, crafting_template, crafted_stats_reconstructed, score_usage_status, weapon_class, stack_amount, speed_rating, missile_speed, accuracy, weapon_length, swing_damage, swing_damage_type, thrust_damage, thrust_damage_type, hit_points, shield_armor, head_armor, body_armor, arm_armor, leg_armor, horse_speed, horse_maneuver, horse_charge_damage, horse_extra_health, troop_name, level, occupation, culture, default_group, OneHanded, TwoHanded, Polearm, Bow, Crossbow, Throwing, Riding, Athletics, tree_root_id, upgrade_depth, tree_tier, line_status, line_status_corrected`;
- troops:
  `troop_id, name_raw, name, level, occupation, culture, default_group, is_basic_troop, is_hero, is_template, OneHanded, TwoHanded, Polearm, Bow, Crossbow, Throwing, Riding, Athletics, upgrade_targets, has_upgrade_targets, is_soldier`;
- overrides:
  `troop_id, winner_module, defining_modules, overridden_modules, definition_count, change_type`;
- crafted composition:
  `item_id, piece_id, piece_type, scale_factor`;
- crafted items:
  `item_id, name, item_kind, type, crafting_template, culture, modifier_group, source_xml, piece_ids, crafted_stats_reconstructed, score_usage_status`;
- roster audit summary:
  `troop_id, troop_name, level, upgrade_depth, tree_tier, line_status, culture, default_group, roster_index, items, weapon_items, direct_weapon_items, crafted_weapon_items, crafted_templates, has_bow, has_crossbow, has_arrows, has_bolts, has_shield, has_horse, has_horse_harness, has_throwing, armor_total, shield_hp_max, horse_speed_max, horse_charge_max, horse_harness_armor_max, crafted_weapon_stat_status, unknown_item_count`.

The equipment audit is sufficient for armor, roster membership, item family, and ammunition stack assignments. It is not a component-level weapon contract: its scalar `swing_damage`/`thrust_damage` cells can be overwritten while normalization iterates multiple XML `<Weapon>` components, so they cannot prove FR-4's “every attack row” requirement. D4 must add `data/<track>/audit/<track>_weapon_attack_rows.csv` with one source-provenanced row per XML attack component before attack scoring can rank.

The repository currently retains raw-XML manifests and source-package hashes while XML bodies may be local-only. The D4 extractor accepts only XML reconstructed from the recorded source package or an exact PC module root whose files verify against `data/<track>/raw_xml/manifest.csv`. If neither is available, D4 emits an acquisition request and stops; it must not reverse-engineer missing component rows from scalar audit cells.

The equipment audit also does not carry a machine-readable tooltip-validation verdict for reconstructed crafted items. Therefore reconstructed output is eligible only when a separate, hash-pinned validation receipt proves that the exact reconstructed file and tested item passed. A console message from reconstruction is not evidence. D4 adds a deterministic receipt producer that consumes the reconstructed CSV plus repository-addressable per-item tooltip comparisons; it never derives a pass from aggregate console counts.

The resolver looks for normalization evidence at the fixed paths
`data/<track>/audit/<track>_weapon_attack_rows.csv`,
`data/<track>/audit/<track>_crafted_weapon_stats.csv`, and
`data/<track>/audit/<track>_crafted_weapon_tooltip_validation_receipt.json`.
Their absence is a row-level crafted-evidence blocker, not a candidate-generation
failure. The first and third producers are part of D4; actual PC catalogs and tooltip observations remain operator-provided evidence.

### 2.4 Empirical limitations

The legacy strict baseline is player-side and keyed by provisional name slug. New promotion validation may join only through a verified `canonical_troop_id` in versioned batch analysis. Current evidence has no eligible siege-defense troop, incomplete canonical coverage, and no completed grouped out-of-sample or controlled-evidence gate. Candidate generation must therefore complete with honest blank attack/general rows where required, while promotion is expected to publish `status=blocked` until external evidence exists.

## 3. Architecture and dependency direction

The implementation is a source-level Python component under `scripts/scoring/`. It uses frozen dataclasses and pure functions for policy, with CSV/JSON/filesystem handling at the outer boundary.

```text
context_first_contract
        ^
        |
context_first_equipment <--- reconstruct_crafted_weapon_stats output contract
        ^            ^
        |            |
context_first_ranged |
        ^            |
        +------ context_first_engine
                       ^
                       |
          generate_context_first_scores
                       ^
              +--------+---------+
              |                  |
write_context_first_reports  validate_context_first_candidate
              ^
              |
 build_context_first_candidate ---> context_first_publication
```

Rules:

1. `context_first_contract.py` imports only the standard library and knows nothing about CSV paths.
2. `context_first_equipment.py` depends on declaration/domain contracts and resolves direct evidence. It does not rank or render.
3. `context_first_ranged.py` depends on typed weapon evidence and ammunition policy. It does not read files.
4. `context_first_engine.py` applies context policy first, calls resolvers, aggregates, and returns typed results. It does not publish files.
5. CLI modules are adapters. They read pinned inputs and invoke policy; only the D8 build adapter publishes the committed candidate root transactionally.
6. Reporting reads the generated typed artifact contract; it does not recalculate armor or weapon formulas. `build_context_first_candidate.py` orchestrates core generation then rendering, while both adapters share publication primitives from `context_first_publication.py`; core generation never imports the renderer.
7. Validation reads candidate artifacts and canonical empirical artifacts; it cannot mutate candidate scores or frozen models.

This follows SRP by separating declaration, evidence, context, scoring, rendering, and validation. It follows DIP by keeping policy independent of path and serialization details. Shared parsing, decimal publication, ranking, reason vocabulary, and hashing each have one implementation. No plugin framework or class hierarchy is introduced; that would be unnecessary generality for one versioned candidate.

## 4. Python module contracts

### 4.1 Declaration and common types

`scripts/scoring/context_first_contract.py` owns:

```python
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Mapping, Sequence

class BattleContext(str, Enum):
    FIELD = "field"
    SIEGE_ATTACK = "siege_attack"
    SIEGE_DEFENSE = "siege_defense"

class TroopQuestion(str, Enum):
    DEFENSE = "defense"
    ATTACK = "attack"
    GENERAL = "general"

class AttackMode(str, Enum):
    MELEE = "melee"
    RANGED = "ranged"

class MountState(str, Enum):
    MOUNTED = "mounted"
    DISMOUNTED = "dismounted"

class AmmunitionPolicy(str, Enum):
    FINITE = "finite"
    UNLIMITED = "unlimited"
    NOT_APPLICABLE = "not_applicable"

@dataclass(frozen=True)
class ArmorAggregation:
    aggregation_id: str
    head_weight: Decimal
    body_weight: Decimal
    arm_weight: Decimal
    leg_weight: Decimal

@dataclass(frozen=True)
class ScoringDeclaration:
    schema_version: str
    candidate_id: str
    track: str
    context: BattleContext
    question: TroopQuestion
    attack_mode: AttackMode
    mount_state: MountState
    primary_drivers: tuple[str, ...]
    ammunition_policy: AmmunitionPolicy
    secondary_drivers: tuple[str, ...]
    armor_source_fields: tuple[str, ...]
    armor_aggregation: ArmorAggregation | None
    weapon_damage_source_fields: tuple[str, ...]
    projectile_contribution: str
    roster_aggregation: str
    combination_rule: str

@dataclass(frozen=True)
class ContractIssue:
    code: str
    field: str
    message: str

class DeclarationError(ValueError):
    issues: tuple[ContractIssue, ...]

def load_declaration(path: Path) -> ScoringDeclaration: ...
def parse_declaration(value: Mapping[str, object]) -> ScoringDeclaration: ...
def validate_declaration(value: Mapping[str, object]) -> tuple[ContractIssue, ...]: ...
```

### 4.2 Evidence contracts

`scripts/scoring/context_first_equipment.py` owns:

```python
@dataclass(frozen=True)
class SourceRef:
    path: str
    sha256: str
    row_number: int
    item_id: str

@dataclass(frozen=True)
class ReviewReason:
    code: str
    scope: str
    troop_id: str
    roster_index: str
    item_id: str
    source: SourceRef | None
    detail: str

@dataclass(frozen=True)
class ArmorItemEvidence:
    troop_id: str
    roster_index: str
    slot: str
    alternative_index: int
    item_id: str
    head_armor: Decimal
    body_armor: Decimal
    arm_armor: Decimal
    leg_armor: Decimal
    source: SourceRef

@dataclass(frozen=True)
class ArmorRosterEvidence:
    troop_id: str
    roster_index: str
    head_armor: Decimal | None
    body_armor: Decimal | None
    arm_armor: Decimal | None
    leg_armor: Decimal | None
    armor_output: Decimal | None
    source_item_ids: tuple[str, ...]
    reasons: tuple[ReviewReason, ...]

@dataclass(frozen=True)
class WeaponAttackRow:
    troop_id: str
    roster_index: str
    slot: str
    alternative_index: int
    item_id: str
    item_kind: str
    weapon_family: str
    attack_kind: str
    damage: Decimal | None
    reconstructed: bool
    reconstruction_status: str
    tooltip_validation_status: str
    source: SourceRef
    reasons: tuple[ReviewReason, ...]

@dataclass(frozen=True)
class WeaponChoiceEvidence:
    troop_id: str
    roster_index: str
    item_id: str
    weapon_family: str
    selected_attack_kind: str
    selected_damage: Decimal | None
    selected_source: SourceRef | None
    reasons: tuple[ReviewReason, ...]

@dataclass(frozen=True)
class TooltipValidationReceipt:
    schema_version: str
    track: str
    reconstructed_stats_path: str
    reconstructed_stats_sha256: str
    tooltip_source_path: str
    tooltip_source_sha256: str
    tolerance: Decimal
    compared_items: tuple[str, ...]
    passed_items: tuple[str, ...]
    failed_items: tuple[str, ...]
    status: str

def resolve_armor_rosters(...) -> tuple[ArmorRosterEvidence, ...]: ...
def resolve_weapon_choices(...) -> tuple[WeaponChoiceEvidence, ...]: ...
def load_tooltip_validation_receipt(path: Path) -> TooltipValidationReceipt: ...
```

The implementation may add private helpers, but these public types and entry points are the cross-module contract.

### 4.3 Ranged contracts

`scripts/scoring/context_first_ranged.py` owns:

```python
@dataclass(frozen=True)
class ProjectileStack:
    troop_id: str
    roster_index: str
    slot: str
    alternative_index: int
    item_id: str
    projectile_family: str
    projectile_damage: Decimal | None
    stack_count: int | None
    source: SourceRef
    reasons: tuple[ReviewReason, ...]

@dataclass(frozen=True)
class RangedPairing:
    pairing_id: str
    loadout_id: str
    troop_id: str
    roster_index: str
    weapon_item_id: str
    projectile_item_id: str
    weapon_family: str
    projectile_family: str
    weapon_damage: Decimal | None
    projectile_damage: Decimal | None
    per_shot_output: Decimal | None
    usable_ammunition_count: int | None
    finite_stack_capacity: Decimal | None
    ammunition_policy: AmmunitionPolicy
    weapon_source: SourceRef
    projectile_source: SourceRef
    reasons: tuple[ReviewReason, ...]

@dataclass(frozen=True)
class RangedWeaponOutput:
    troop_id: str
    roster_index: str
    loadout_id: str
    weapon_item_id: str
    output: Decimal | None
    pairings: tuple[RangedPairing, ...]
    reasons: tuple[ReviewReason, ...]

def build_projectile_stacks(...) -> tuple[ProjectileStack, ...]: ...
def build_ranged_pairings(...) -> tuple[RangedPairing, ...]: ...
def aggregate_ranged_weapon(...) -> RangedWeaponOutput: ...
```

`stack_count` is the validated domain value parsed from the equipment-audit column `stack_amount`; there is no input column named `stack_count`. The adapter preserves finite, non-negative integral numeric values (for example `35.0 -> 35`) and otherwise emits `RANGED_AMMO_COUNT_INVALID`. Zero is preserved only so unlimited mode can ignore it; finite mode rejects zero with `RANGED_AMMO_COUNT_INVALID` before multiplication, so missing ammunition never becomes a legitimate numeric output of zero.

### 4.4 Engine contracts

`scripts/scoring/context_first_engine.py` owns:

```python
@dataclass(frozen=True)
class EffectiveContext:
    declared_context: BattleContext
    declared_mount_state: MountState
    effective_mount_state: MountState
    ammunition_policy: AmmunitionPolicy

@dataclass(frozen=True)
class TroopScore:
    candidate_id: str
    track: str
    context: BattleContext
    question: TroopQuestion
    attack_mode: AttackMode
    declared_mount_state: MountState
    effective_mount_state: MountState
    troop_id: str
    troop_name: str
    roster_count: int
    armor_output: Decimal | None
    weapon_output: Decimal | None
    combined_output: None
    armor_rank: int | None
    weapon_rank: int | None
    combined_rank: None
    rankable: bool
    reasons: tuple[ReviewReason, ...]

@dataclass(frozen=True)
class CandidateResult:
    declaration: ScoringDeclaration
    scores: tuple[TroopScore, ...]
    armor_rosters: tuple[ArmorRosterEvidence, ...]
    attack_rows: tuple[WeaponAttackRow, ...]
    ranged_pairings: tuple[RangedPairing, ...]
    reasons: tuple[ReviewReason, ...]

def derive_effective_context(declaration: ScoringDeclaration) -> EffectiveContext: ...
def select_population(...) -> tuple[...]: ...
def score_candidate(...) -> CandidateResult: ...
def add_competition_ranks(scores: Sequence[TroopScore]) -> tuple[TroopScore, ...]: ...
```

`combined_output` and `combined_rank` are intentionally typed as `None` in v1. A later candidate that defines a blend must introduce a new declaration schema and result contract rather than silently populating these fields.

## 5. Declaration schema

Declarations are strict JSON files under:

```text
analysis/model_candidates/context_first_scores_v1/declarations/
  <track>__<context>__<question>__<attack_mode>__<mount_state>.json
```

Canonical JSON shape:

```json
{
  "schema_version": "context-first-scoring-declaration:v1",
  "candidate_id": "context_first_scores_v1",
  "track": "realm_of_thrones",
  "context": "siege_defense",
  "question": "defense",
  "attack_mode": "melee",
  "mount_state": "dismounted",
  "primary_drivers": ["worn_armor"],
  "ammunition_policy": "not_applicable",
  "secondary_drivers": [],
  "armor_source_fields": [
    "head_armor",
    "body_armor",
    "arm_armor",
    "leg_armor"
  ],
  "armor_aggregation": {
    "aggregation_id": "survivability_armor_v71",
    "weights": {
      "head_armor": "0.35",
      "body_armor": "0.55",
      "arm_armor": "0.05",
      "leg_armor": "0.05"
    }
  },
  "weapon_damage_source_fields": [],
  "projectile_contribution": "not_applicable",
  "roster_aggregation": "arithmetic_mean",
  "combination_rule": "not_applicable"
}
```

Validation rejects unknown keys and applies these cross-field rules before opening any audit CSV:

1. `schema_version` and `candidate_id` must equal the exact v1 values.
2. `track` must be one of `vanilla`, `nightmare_sails`, `realm_of_thrones`, or `taom`.
3. `secondary_drivers` must be empty in v1.
4. Defense requires `primary_drivers=["worn_armor"]`, armor fields/aggregation above, `ammunition_policy=not_applicable`, empty weapon fields, `projectile_contribution=not_applicable`, and `combination_rule=not_applicable`.
5. Melee attack requires `primary_drivers=["weapon_output"]`, `weapon_damage_source_fields=["swing_damage","thrust_damage"]`, no armor aggregation, `ammunition_policy=not_applicable`, `projectile_contribution=not_applicable`, and `combination_rule=not_applicable`.
6. Ranged attack requires `primary_drivers=["weapon_output"]`, the same weapon fields, `projectile_contribution=not_included`, and `combination_rule=not_applicable`.
7. General melee requires `primary_drivers=["worn_armor","weapon_output"]`, both armor and weapon contracts, `ammunition_policy=not_applicable`, `projectile_contribution=not_applicable`, and `combination_rule=none`.
8. General ranged requires both drivers, `projectile_contribution=not_included`, and `combination_rule=none`.
9. Ranged field/siege attack requires `ammunition_policy=finite`.
10. Ranged siege defense requires `ammunition_policy=unlimited`.
11. Siege defense requires `mount_state=dismounted`; a mounted declaration is invalid rather than silently accepted.
12. Non-ranged declarations cannot use finite or unlimited ammunition.
13. `roster_aggregation` must equal `arithmetic_mean`.
14. `projectile_contribution` accepts only `not_applicable` when no projectile exists and `not_included` for ranged candidate v1, where a projectile exists but its damage is inert.
15. `combination_rule=not_applicable` means a single-component question has nothing to combine; `combination_rule=none` means a general question intentionally publishes two components without combining them. No other value is valid in schema v1.
16. No numeric value may be non-finite.

Declaration errors are sorted by `(field, code, message)`, printed one per line, and cause exit 2 before any scoring input is read.

## 6. Population and context algorithm

1. Load the declaration and validate it.
2. Load and hash the exact track troop, equipment, and override CSVs.
3. Keep rows where `is_soldier=true`, `is_hero=false`, and `troop_id` does not start with `mp_`.
4. For non-vanilla tracks, require the override report and exclude `change_type=inalterado`. A missing troop override is a structural error.
5. Require at least one equipment roster for every eligible troop. Missing rosters produce a complete unrankable troop row with `TROOP_ROSTER_MISSING`; they do not remove the troop. A wholly absent/malformed audit file remains a fatal run error.
6. Determine whether each roster is mounted from a resolved `Horse` row. Unresolved horse identity is relevant only to mount-state population selection outside siege defense; it never becomes a scoring value.
7. Outside siege defense:
   - `mount_state=mounted` uses only mounted rosters and retains a troop if at least one exists;
   - `mount_state=dismounted` uses only horseless rosters and retains a troop if at least one exists;
   - a troop with no roster in the selected state remains in complete output with `MOUNT_STATE_ROSTER_MISSING`.
8. In siege defense, include every eligible roster, set `effective_mount_state=dismounted`, and remove `Horse` and `HorseHarness` rows before evidence selection. Riding, speed, maneuver, charge, mount health, and harness armor are never read by a scorer.
9. Ranks are computed only inside one exact `(track, context, question, attack_mode, effective_mount_state)` declaration population.

## 7. Armor algorithm

Worn slots are exactly `Head`, `Body`, `Gloves`, `Leg`, and `Cape`. `Item*`, `Horse`, and `HorseHarness` rows never contribute armor.

For each troop/roster:

1. Group worn rows by slot. Preserve input row number as `alternative_index` after sorting by `(slot, item_id, source row number)`.
2. A slot with no row means no item is worn and contributes numeric zero to all four regions.
3. Every present alternative must have `item_found=true`, a non-empty `item_id`, and finite non-negative values in all four armor fields. A blank field is unknown, not zero.
4. If any present alternative is unresolved or malformed, publish all known item rows but make the entire roster armor result blank with the applicable review reasons.
5. Otherwise compute the arithmetic mean of alternatives within each slot for each region.
6. Sum the five slot means to produce roster head/body/arm/leg totals.
7. Apply only the declaration's aggregation. For v1:

```text
armor_output =
    0.35 * head_armor
  + 0.55 * body_armor
  + 0.05 * arm_armor
  + 0.05 * leg_armor
```

8. A troop armor component is the arithmetic mean of all selected roster `armor_output` values. If any selected roster is blank, the troop armor component is blank. Unknown roster probability is not grounds to discard the incomplete roster.
9. Publish the item evidence, roster regional totals, roster output, and troop mean before ranking.

Shields and mounted equipment are inert even if their fields are populated.

## 8. Weapon and CraftedItem algorithm

### 8.1 Direct evidence

For the selected attack mode, consider only:

- melee: resolved non-shield, non-projectile weapon items with an authorized swing and/or thrust damage row;
- ranged: resolved `Bow` and `Crossbow` items.

For every considered equipment occurrence, join by track and `item_id` to the winning D4 attack-row definition. The extractor resolves duplicate definitions using the verified module order from `raw_xml/manifest_modules.csv`: the highest `load_order_index` wins, superseded definitions are retained only in the normalization audit, and duplicate definitions inside the same winning module fail closed. Equipment `equipment_source` is roster provenance and must never be treated as an item-definition module. The scalar damage cells in the equipment audit are classification/debug context only and must not be promoted into `WeaponAttackRow` evidence.

For every normalized attack-row occurrence:

1. Publish exactly one `WeaponAttackRow` for each normalized component record, using its `attack_kind`, `damage`, and source provenance. Never re-derive rows from the equipment audit's scalar swing/thrust cells.
2. Reject blank, malformed, negative, or non-finite damage. Numeric zero is valid only when explicitly present in the source; it cannot be created from a blank.
3. Select the maximum valid damage for the item. Tie-break by `attack_kind` in lexical order, then source row number.
4. Preserve selected attack kind and `SourceRef`.
5. If no valid attack row exists, leave the item output blank.

Weapon speed, reach/length, damage type, skills, accuracy, missile speed, and reliability remain published only in the source audit; they are not copied into score formulas.

### 8.2 CraftedItem gate

An item whose `item_kind=CraftedItem` is eligible only when all conditions hold:

1. a reconstructed row exists for the same `track` and `item_id`;
2. `crafted_stats_reconstructed=True`;
3. `stat_source=piece_catalog+template_catalog`;
4. both catalog SHA-256 fields are present;
5. `formula_version=piece_composition_v1`;
6. reconstructed swing and thrust cells are finite and non-blank;
7. a tooltip receipt pins the exact reconstructed output SHA-256;
8. the receipt has `status=passed`, the item is in `passed_items`, and it is absent from `failed_items`;
9. D4 converted the receipt-validated reconstructed swing and thrust cells into the shared attack-row schema, with `evidence_kind=reconstructed_crafted` and both the reconstructed-output and receipt SHA-256 values pinned.

The crafting template name is never read as damage evidence. Missing catalogs, missing reconstruction, incomplete composition, absent validated crafted attack rows, missing receipt, hash mismatch, or failed tooltip validation leaves the item blank and queues it.

The reconstruction script remains an unchanged normalization producer. D4 does not change its arithmetic, CLI behavior, or historical tests. D4 adds `build_crafted_weapon_validation_receipt.py`, which consumes the reconstructed output and a repository-addressable per-item tooltip-comparison CSV, verifies both hashes, rejects duplicate/missing item verdicts, and atomically writes both the receipt and `data/<track>/audit/<track>_crafted_weapon_attack_rows.csv`. That CSV emits at most one swing and one thrust row per passed item and points back to the reconstructed CSV, its source catalogs, and the validation receipt. Direct XML rows and validated crafted rows are then unioned under the shared `WeaponAttackRow` contract; neither is inferred from equipment-audit scalars. Missing tooltip observations keep the gate blocked; the producer never manufactures them.

### 8.3 Roster and troop melee output

All eligible melee weapon items in a roster are alternative offensive choices. Publish each item output, then compute the roster arithmetic mean. A relevant unresolved weapon choice makes that roster blank rather than allowing a favorable known weapon to stand in for it. The troop melee output is the arithmetic mean across selected rosters; any blank selected roster makes the troop output blank.

## 9. Ranged algorithm

Compatibility is intentionally narrow and auditable:

- audit literal `Bow` pairs only with audit literal `Arrow`;
- audit literal `Crossbow` pairs only with audit literal `Bolt`;
- all other families receive `RANGED_FAMILY_UNSUPPORTED`.

For every selected roster:

1. Group relevant equipment rows by slot and enumerate deterministic loadouts that select exactly one alternative from each occupied slot. Rows from distinct slots are simultaneously carried; alternatives from the same slot never are.
2. Within each loadout, resolve each selected bow/crossbow as a separate weapon choice.
3. Resolve each selected compatible ammunition row as a separate projectile stack. Candidate v1 may publish observed projectile damage for audit context, but `projectile_contribution=not_included` makes it inert.
4. Build one pairing for every compatible `(loadout, weapon occurrence, projectile stack occurrence)`, with:

```text
per_shot_output = weapon_damage
```

5. In field or siege attack (`finite`):

```text
usable_ammunition_count = sum(stack_count for compatible stacks selected in distinct slots of this loadout)
finite_stack_capacity = per_shot_output * stack_count  # published per pairing
weapon_output = per_shot_output * usable_ammunition_count
```

This exactly implements bow/crossbow damage times compatible usable ammunition. Projectile damage cannot change candidate-v1 output. The same ammunition stack may appear in each selected weapon's published pairings, but weapon outputs are averaged within a loadout; they are never summed as simultaneous fire. Same-slot projectile alternatives produce separate loadouts and therefore are averaged rather than summed.

6. In siege defense (`unlimited`), ignore `stack_count` and leave `usable_ammunition_count` and `finite_stack_capacity` blank:

```text
weapon_output = weapon_damage
```

No numeric infinity is serialized.

7. A weapon with no compatible projectile row is blank and queued.
8. Finite mode requires a positive integer `stack_count` for every compatible stack. Blank, malformed, fractional, negative, or zero counts are unrankable.
9. Unlimited mode does not validate or use stack count.
10. Projectile stacks, loadouts, and weapon alternatives remain separate published pairings even though projectile damage is inert in v1.
11. A loadout output is the arithmetic mean of its alternative weapon outputs. Roster ranged output is the arithmetic mean across enumerated loadouts, and troop output is the arithmetic mean across selected rosters. Any relevant blank choice/loadout/roster makes the containing aggregate blank.

## 10. Score and rank behavior

Defense:

- `armor_output` is populated when complete;
- `armor_rank` is a descending competition rank;
- weapon and combined fields remain blank.

Attack:

- `weapon_output` is populated when complete;
- `weapon_rank` is a descending competition rank;
- armor and combined fields remain blank.

General:

- armor and weapon outputs are evaluated independently;
- each component receives its own rank among rows eligible for that component;
- one missing component does not erase the other component or its rank;
- `combined_output` and `combined_rank` are always blank;
- `rankable=true` means at least one declared component is rankable, while `fully_evidenced=true` in CSV means both are rankable.

All calculation uses `Decimal` parsed from source text. Published decimals are quantized to six places with `ROUND_HALF_EVEN`. Rank/tie comparison uses the quantized value. Competition ranking yields `1,1,3`; ties are then ordered by `troop_id`. No min-max normalization or cross-population rank comparison is performed.

## 11. Stable reason and error codes

Codes are constants in `context_first_contract.py`; code strings are public artifact API and must not be renamed within schema v1.

Audit departure codes:

- `SOURCE_ARTIFACT_ABSENT`
- `CONTEXT_UNDECLARED`
- `QUESTION_MIXED`
- `ATTACK_MODE_UNDECLARED`
- `MOUNT_STATE_UNDECLARED`
- `IRRELEVANT_DRIVER_INCLUDED`
- `TEMPLATE_PROXY_USED`
- `MISSING_VALUE_ZERO_FILLED`
- `AMMUNITION_POLICY_UNDECLARED`
- `MOUNTED_INPUT_NON_APPLICABLE`

Declaration errors:

- `DECL_MISSING_FIELD`
- `DECL_UNKNOWN_FIELD`
- `DECL_INVALID_ENUM`
- `DECL_INVALID_DRIVER_SET`
- `DECL_INVALID_ARMOR_CONTRACT`
- `DECL_INVALID_WEAPON_CONTRACT`
- `DECL_AMMUNITION_POLICY_MISMATCH`
- `DECL_SIEGE_DEFENSE_MUST_DISMOUNT`
- `DECL_GENERAL_BLEND_FORBIDDEN`
- `DECL_NONFINITE_NUMBER`

Review-queue reasons:

- `TROOP_ROSTER_MISSING`
- `MOUNT_STATE_ROSTER_MISSING`
- `MOUNT_STATE_EVIDENCE_UNRESOLVED`
- `ARMOR_ITEM_ID_MISSING`
- `ARMOR_ITEM_UNRESOLVED`
- `ARMOR_REGION_MISSING`
- `ARMOR_VALUE_INVALID`
- `WEAPON_ITEM_ID_MISSING`
- `WEAPON_ITEM_UNRESOLVED`
- `WEAPON_ATTACK_ROW_MISSING`
- `WEAPON_DAMAGE_INVALID`
- `CRAFTED_RECONSTRUCTION_MISSING`
- `CRAFTED_RECONSTRUCTION_INCOMPLETE`
- `CRAFTED_PROVENANCE_INCOMPLETE`
- `CRAFTED_TOOLTIP_RECEIPT_MISSING`
- `CRAFTED_TOOLTIP_RECEIPT_HASH_MISMATCH`
- `CRAFTED_TOOLTIP_VALIDATION_MISSING`
- `CRAFTED_TOOLTIP_VALIDATION_FAILED`
- `RANGED_FAMILY_UNSUPPORTED`
- `RANGED_PROJECTILE_MISSING`
- `RANGED_PROJECTILE_INCOMPATIBLE`
- `RANGED_PROJECTILE_DAMAGE_MISSING`
- `RANGED_AMMO_COUNT_MISSING`
- `RANGED_AMMO_COUNT_INVALID`

Promotion reasons:

- `PROMOTION_CANONICAL_JOIN_INCOMPLETE`
- `PROMOTION_EMPIRICAL_GATE_INSUFFICIENT`
- `PROMOTION_GROUPED_OOS_MISSING`
- `PROMOTION_CONTROLLED_EVIDENCE_MISSING`
- `PROMOTION_REPRODUCIBILITY_FAILED`
- `PROMOTION_LIMITATIONS_REVIEW_MISSING`
- `PROMOTION_BOUNDARY_VIOLATION`

Review rows sort by `(troop_id, roster_index, item_id, code, source.path, source.row_number)`. Human-readable `detail` may improve without changing the stable code.

## 12. CLI entry points and exit codes

### 12.0 Weapon normalization prerequisites

```bash
python3 scripts/normalization/extract_weapon_attack_rows.py \
  --track <track> \
  --xml-root <verified-reconstructed-or-PC-module-root> \
  --raw-manifest data/<track>/raw_xml/manifest.csv \
  --module-manifest data/<track>/raw_xml/manifest_modules.csv \
  --output data/<track>/audit/<track>_weapon_attack_rows.csv

python3 scripts/normalization/build_crafted_weapon_validation_receipt.py \
  --reconstructed data/<track>/audit/<track>_crafted_weapon_stats.csv \
  --tooltip-observations <repository-addressable-tooltip-observations.csv> \
  --tolerance 1.0 \
  --receipt-output data/<track>/audit/<track>_crafted_weapon_tooltip_validation_receipt.json \
  --attack-row-output data/<track>/audit/<track>_crafted_weapon_attack_rows.csv
```

The attack-row CSV schema is:

```text
track,item_id,evidence_kind,component_index,attack_index,attack_kind,damage,damage_type,
source_module,source_relative_path,source_file_sha256,source_locator,definition_status,
reconstructed_stats_sha256,tooltip_receipt_sha256
```

Rows are ordered by `(track,item_id,evidence_kind,component_index,attack_index,attack_kind,source_relative_path,source_locator)`. The extractor rejects any XML file whose hash does not match the raw manifest or any module list whose order differs from `manifest_modules.csv`. For duplicate item IDs it marks lower-load-order rows `superseded`, emits only the highest-load-order definition as scoring input, and rejects ambiguous duplicates within that winning module. Exit 0 publishes atomically; exit 2 publishes nothing and names the missing/mismatched source.

The tooltip observations reuse the existing columns `item_id,observed_swing_damage,observed_thrust_damage`. The receipt adds reconstructed/observation SHA-256 values, tolerance, per-item compared stats, `passed_items`, `failed_items`, and top-level `status=passed|failed`. The companion crafted attack-row CSV uses the same shared schema, sets `evidence_kind=reconstructed_crafted`, emits validated swing/thrust rows only for passed items, and pins the reconstructed file and receipt hashes. Duplicate items, an item with both observations blank, or an input-hash mismatch exits 2 without either output. Missing operator observations are a D4 evidence blocker, not permission to emit an empty passing receipt.

### 12.1 Audit

```bash
python3 scripts/scoring/audit_context_first_candidates.py \
  --repo . \
  --output analysis/model_candidates/context_first_scores_v1/CURRENT_CANDIDATE_AUDIT.md
```

Exit 0: report reproduced and immutable source hashes match the audit specification; artifacts explicitly declared absent remain stable absence findings.

Exit 2: an artifact expected present by the audit specification is missing, a classified source changed without an updated classification, or historical bytes changed.

### 12.2 Contract validation

```bash
python3 scripts/scoring/context_first_contract.py \
  analysis/model_candidates/context_first_scores_v1/declarations/<declaration>.json
```

Exit 0: valid. Exit 2: deterministic field/rule errors.

### 12.3 Core or complete generation

```bash
python3 scripts/scoring/generate_context_first_scores.py \
  --repo . \
  --declarations-dir analysis/model_candidates/context_first_scores_v1/declarations \
  --scratch-output <outside-committed-root>
```

Optional filters are `--track <track>` and `--declaration <path>`; this core adapter requires `--scratch-output <outside committed root>`. Passing the committed candidate root is rejected. The D8 build command below always regenerates every declaration so its manifest cannot mix generations.

This core-generation command does not import the report renderer, publication adapter, or D9 validator. D8's build command below is the FR-12 one-command candidate reproduction path.

Exit 0 means the scratch core package is structurally valid even when rows are unrankable. Exit 2 means declaration/input/integrity failure and no complete scratch package was produced. After D9 exists, validation remains the explicit next command below.

### 12.3a One-command candidate build

```bash
python3 scripts/scoring/build_context_first_candidate.py \
  --repo . \
  --declarations-dir analysis/model_candidates/context_first_scores_v1/declarations \
  --output-root analysis/model_candidates/context_first_scores_v1
```

The D8 build adapter creates a sibling staging root, invokes the core generator's Python API, invokes the report renderer's Python API, validates the whole package, and commits it through `context_first_publication.py`. It does not invoke D9 validation. Neither the core generator nor renderer imports the other; the build adapter owns orchestration and the shared publication module owns lock/staging/journal primitives.

### 12.4 Reports

```bash
python3 scripts/scoring/write_context_first_reports.py \
  --repo . \
  --candidate-root analysis/model_candidates/context_first_scores_v1
```

This standalone adapter verifies the existing core manifest, builds reports in a staging copy, and republishes the complete package transactionally. It never recalculates scores.

### 12.5 Promotion validation

```bash
python3 scripts/scoring/validate_context_first_candidate.py \
  --repo . \
  --candidate-root analysis/model_candidates/context_first_scores_v1 \
  --combat-root data/combat_observations
```

Exit 0 with `promotion_gate.status=passed` or `blocked` when evaluation completed honestly. Exit 2 only for malformed candidate/empirical artifacts, boundary violations, hash failures, or other invalid evaluation.

## 13. Candidate directory schema

```text
analysis/model_candidates/context_first_scores_v1/
  README.md
  CURRENT_CANDIDATE_AUDIT.md
  historical_baseline_hashes.csv
  declarations/
    <tuple>.json
  <track>/<context>/<question>/<attack_mode>/<mount_state>/
    declaration.json
    armor_items.csv
    armor_rosters.csv
    weapon_attack_rows.csv
    ranged_pairings.csv
    crafted_tooltip_validation.json
    scores_complete.csv
    scores_rankable.csv
    review_queue.csv
    metadata.json
  realm_of_thrones/
    TOP10.md
  VALIDATION_REPORT.md
  promotion_gate.json
  validation_input_hashes.csv
  input_hashes.csv
  candidate_manifest.csv
  artifact_hashes.csv
```

`declaration.json` is an exact canonicalized copy of the source declaration used for the tuple.

### 13.1 Evidence CSV schemas

`armor_items.csv`:

```text
candidate_id,track,context,question,attack_mode,declared_mount_state,effective_mount_state,troop_id,troop_name,roster_index,slot,alternative_index,item_id,head_armor,body_armor,arm_armor,leg_armor,source_path,source_sha256,source_row_number,evidence_status,reason_codes
```

`armor_rosters.csv`:

```text
candidate_id,track,context,question,attack_mode,declared_mount_state,effective_mount_state,troop_id,troop_name,roster_index,head_armor,body_armor,arm_armor,leg_armor,armor_aggregation_id,armor_output,source_item_ids,evidence_status,reason_codes
```

`weapon_attack_rows.csv`:

```text
candidate_id,track,context,question,attack_mode,declared_mount_state,effective_mount_state,troop_id,troop_name,roster_index,slot,alternative_index,item_id,item_kind,weapon_family,attack_kind,damage,reconstructed,reconstruction_status,tooltip_validation_status,selected_for_item,source_path,source_sha256,source_row_number,evidence_status,reason_codes
```

`ranged_pairings.csv`:

```text
candidate_id,track,context,question,attack_mode,declared_mount_state,effective_mount_state,pairing_id,loadout_id,troop_id,troop_name,roster_index,weapon_item_id,projectile_item_id,weapon_family,projectile_family,weapon_damage,projectile_damage,per_shot_output,usable_ammunition_count,finite_stack_capacity,ammunition_policy,weapon_source_path,weapon_source_sha256,weapon_source_row_number,projectile_source_path,projectile_source_sha256,projectile_source_row_number,evidence_status,reason_codes
```

### 13.2 Score CSV schemas

Both `scores_complete.csv` and `scores_rankable.csv` use:

```text
candidate_id,track,context,question,attack_mode,declared_mount_state,effective_mount_state,troop_id,troop_name,culture,level,default_group,selected_roster_count,armor_output,weapon_output,combined_output,armor_rank,weapon_rank,combined_rank,armor_evidence_status,weapon_evidence_status,fully_evidenced,rankable,ammunition_policy,roster_aggregation,reason_codes
```

Complete output contains every ordinary eligible troop, including rows without a selected mount-state roster. Rankable output contains:

- defense: rows with armor output/rank;
- attack: rows with weapon output/rank;
- general: rows with at least one component rank.

`review_queue.csv`:

```text
candidate_id,track,context,question,attack_mode,declared_mount_state,effective_mount_state,troop_id,troop_name,roster_index,item_id,scope,reason_code,detail,source_path,source_sha256,source_row_number
```

### 13.3 Metadata and manifests

Each tuple `metadata.json` contains:

```text
schema_version, candidate_id, canonical, declaration_sha256, track, context,
question, attack_mode, declared_mount_state, effective_mount_state,
ammunition_policy, primary_drivers, secondary_drivers, armor_aggregation,
weapon_damage_source_fields, projectile_contribution, roster_aggregation,
combination_rule, decimal_policy, ranking_policy, population_policy,
input_paths, input_sha256s, counts, reason_counts, generated_artifacts
```

`canonical` is always `false`.

`input_hashes.csv`:

```text
path,bytes,sha256,purpose
```

`candidate_manifest.csv`:

```text
path,bytes,sha256
```

This immutable promotion identity covers declarations, pinned candidate inputs, normalized evidence, tuple evidence/scores/metadata, candidate README, audit, and reports. It excludes `VALIDATION_REPORT.md`, `promotion_gate.json`, `validation_input_hashes.csv`, `artifact_hashes.csv`, locks, journals, and backups. `promotion_gate.json.evaluated_candidate_manifest_sha256` hashes this file, so validation outputs can never change the identity being evaluated.

`validation_input_hashes.csv` has columns `path,bytes,sha256,purpose` and covers every D9 empirical, canonical-map, grouped-out-of-sample, controlled-evidence, and limitations-review input. It excludes itself and all generated validation outputs. `promotion_gate.json.validation_input_manifest_sha256` hashes this file, and D10 must verify both the manifest hash and every referenced input before promotion.

`artifact_hashes.csv` has the same columns as `candidate_manifest.csv` and is the outer package-integrity manifest. It excludes itself but includes `candidate_manifest.csv` and, after D9, `validation_input_hashes.csv` plus the other validation outputs. D9 regenerates it after writing validation artifacts. Because the promotion gate pins the candidate and validation-input manifests while neither manifest contains generated gate outputs, there is no hash cycle. All manifest paths are POSIX-relative to candidate root and sorted bytewise.

## 14. Determinism, serialization, hashing, and publication

1. Parse numeric source values as `Decimal`; reject non-finite or malformed required values.
2. Serialize booleans as lowercase `true`/`false`, missing values as empty CSV cells/JSON `null`, and decimals at six fixed places.
3. Use UTF-8 without BOM, LF endings, `csv.DictWriter(..., lineterminator="\n")`, fixed field lists, and no platform-dependent timestamps.
4. Serialize JSON with `indent=2`, `sort_keys=True`, `ensure_ascii=False`, separators implied by the standard pretty format, plus one trailing newline.
5. Sort every source group and output using explicit keys. Never rely on dict/set iteration or filesystem glob order.
6. `loadout_id` is the first 20 hex characters of a SHA-256 over the sorted selected `(slot, alternative_index, item_id, source_row)` tuples; `pairing_id` is `sha256(candidate_id|track|context|question|attack_mode|effective_mount_state|troop_id|roster_index|loadout_id|weapon_source_row|projectile_source_row)[:20]`.
7. Hash input bytes before parsing and verify they are unchanged immediately before publication.
8. Snapshot immutable historical/frozen paths before generation and compare after staging and after publication.

The D8 build adapter publishes through `context_first_publication.py` using an exclusive lock file adjacent to the candidate root and a recoverable directory transaction:

1. Refuse a second writer while the lock is held.
2. Build the entire candidate tree in a sibling staging directory. Copy through `CURRENT_CANDIDATE_AUDIT.md`, `historical_baseline_hashes.csv`, and `declarations/` byte for byte from their reviewed D1/D2 sources and verify their expected hashes before adding generated tuple outputs, reports, manifests, and—when invoked by D9—validation outputs. The core generator never authors or overwrites those source-owned paths or the committed candidate root.
3. Validate schemas, row counts, manifests, source hashes, and historical hashes in staging.
4. Write and fsync a transaction journal naming `old`, `staging`, and `target`.
5. Rename the current target to a sibling backup, then rename staging to target.
6. On any caught failure, restore backup before releasing the lock.
7. On startup, recover a journal deterministically: retain a validated target; otherwise restore the validated backup; never combine trees.
8. Delete backup and journal only after the target manifest verifies.

Readers in this repository must acquire the shared publication lock or verify `artifact_hashes.csv` before use. This gives all cooperating consumers an all-old or all-new package and makes interruption recoverable; no command exposes a partially written target tree. A blocked row or blocked promotion gate is valid staged content, not a publication failure.

A second unchanged run replaces the candidate-owned package with byte-identical files and hashes. A declaration/input hash mismatch exits 2 before the target rename.

## 15. Reports and Realm of Thrones top 10

`README.md` documents declarations, formulas, commands, exclusions, evidence limitations, and package layout.

`realm_of_thrones/TOP10.md` renders one section per declaration:

- defense: top ten by armor rank with raw regional armor and armor output;
- attack: top ten by weapon rank with selected item/pairing evidence and raw output;
- general: separate armor and weapon top tens side by side, with no combined ordering.

If fewer than ten rows rank, render all eligible rows and the count. If none rank, render the stable reason-code counts and explicitly state that no proxy ranking was substituted. Sections sort by `(context, question, attack_mode, mount_state)`.

The current-candidate audit is generated from a versioned table of expected departures and source hashes. It covers `role_scores_v1`, `defensive_role_scores_v2_candidate`, v7.1, v7.2, and v7.3 and records:

```text
model_or_candidate,source_path,source_sha256,context_declared,question_declared,
attack_mode_declared,mount_state_declared,departure_code,field_or_formula,evidence
```

The Markdown groups but does not hide individual findings. Required audit departures include mixed questions, irrelevant drivers, crafted template proxies, zero-filled gaps, undeclared ammunition semantics, mounted inputs in siege-relevant general paths, and absent context declarations.

## 16. Empirical validation and promotion gate

Validation discovers only repository-addressable canonical batch outputs whose manifests/hashes verify. It must not use `baseline_strict_player_side.csv` or name-based legacy aggregate CSVs as canonical joins.

Join key:

```text
(track, context, side, canonical_troop_id)
```

Rules:

1. Reject provisional slugs, display-name matches, cross-track matches, mixed contexts, and unknown/assumed sides from promotion evidence.
2. Consolidate duplicate observations within battle first.
3. Count distinct battle IDs as the independent sampling unit.
4. Display empirical comparison only at `battle_count >= 5` and `total_deployed >= 20`.
5. Compute deterministic 95% battle-bootstrap intervals with a seed derived from the full join key.
6. Keep theoretical component ranks separate. General armor and weapon components are compared independently.
7. Group train/test splits by battle. A row-level split is a fatal boundary violation.
8. Promotion requires independently supplied grouped out-of-sample results and controlled evidence; generation does not fabricate either.

`promotion_gate.json` schema:

```json
{
  "schema_version": "context-first-promotion-gate:v1",
  "candidate_id": "context_first_scores_v1",
  "candidate_generation_status": "complete",
  "status": "blocked",
  "evaluated_candidate_manifest_sha256": "<sha256>",
  "validation_input_manifest_path": "validation_input_hashes.csv",
  "validation_input_manifest_sha256": "<sha256>",
  "gates": [
    {
      "gate": "canonical_join",
      "status": "blocked",
      "reason_codes": ["PROMOTION_CANONICAL_JOIN_INCOMPLETE"],
      "evidence_paths": [],
      "details": {}
    }
  ],
  "eligible_empirical_comparisons": 0,
  "blocked_reason_codes": [],
  "frozen_models": ["v7.1", "v7.3"],
  "promotion_allowed": false
}
```

Every `evidence_paths` entry must occur exactly once in the sorted `validation_input_hashes.csv`; a missing, extra, duplicate, or hash-mismatched input makes evaluation invalid. Top-level and per-gate `status` values are exactly `passed` or `blocked`. `promotion_allowed` is derived and may be `true` only when the top-level status and every gate status are `passed`, the evaluated `candidate_manifest.csv` hash matches the current package, the validation-input manifest and every referenced byte match, and no blocked reason remains. D10 requires all checks; no alias such as `pass` is accepted.

Gate order is:

1. `canonical_join`;
2. `empirical_display`;
3. `grouped_out_of_sample`;
4. `controlled_evidence`;
5. `reproducibility`;
6. `limitations_review`.

Missing or insufficient external evidence sets the relevant gate to `blocked`, keeps `candidate_generation_status=complete`, exits 0, and publishes the candidate honestly. It also stops the locked rework execution at D9: a generated candidate is not a completed rework. Malformed evidence or a boundary violation sets evaluation invalid and exits 2. Only all `passed` gates may produce `promotion_allowed=true`; D10 is the separate dedicated model-change PR that performs promotion for the exact approved hashes.

## 17. Historical and frozen immutability

D1 creates `historical_baseline_hashes.csv` from every file under:

- `analysis/model_candidates/role_scores_v2_defense/`;
- `analysis/model_versions/`;
- committed `analysis/theoretical/**/export_20260731_150800/` role-score artifacts;
- the historical scoring/reconstruction scripts audited by D1.

Schema:

```text
path,bytes,sha256,immutability_class
```

Classes are `historical_candidate`, `frozen_model`, `historical_output`, and `audited_source`. The hash file is generated once in D1, reviewed, and thereafter treated as a checked-in assertion, not regenerated automatically. Every D2-D10 focused integration test and the full generator verifies it. A mismatch exits 2 and prevents publication. `analysis/model_versions/` is not an output path or write target during D1-D9. At D10, promotion may add exactly one new version directory after a passing exact-hash gate; every pre-existing path remains protected by the D1 baseline.

## 18. Tests and observability

Every deliverable follows test-first development: add a failing behavior test, run it and confirm the intended failure, implement the smallest change, then run focused and repository validation.

Required test modules:

- `tests/test_audit_context_first_candidates.py`: expected audit findings, source hashes, no historical writes;
- `tests/test_context_first_contract.py`: complete enum/cross-field/error ordering matrix and validation-before-I/O;
- `tests/test_context_first_armor.py`: shield/mount/skill inertness, blank-vs-zero, slot alternatives, roster means, incomplete roster propagation;
- `tests/test_context_first_weapon_evidence.py`: attack-row publication/tie-break, module-override winner selection, direct damage, receipt-validated CraftedItem conversion, every CraftedItem failure path, receipt hash pinning;
- `tests/test_context_first_ranged.py`: compatibility, distinct-slot stack summation, same-slot alternative loadouts, different projectile values, alternative weapons, finite/unlimited behavior, no infinity;
- `tests/test_context_first_engine.py`: population filters, mount-state roster selection, siege dismount transformation, context isolation;
- `tests/test_context_first_scores.py`: complete/rankable/review contracts, component ranks, tie behavior, general blank blend, cross-track isolation;
- `tests/test_context_first_reports.py`: exact schemas, RoT sections, blocked tables, manifests, two-run byte equality, interrupted-transaction recovery;
- `tests/test_context_first_validation.py`: canonical-only joins, track/context/side boundaries, battle grouping, bootstrap determinism, blocked external gates;
- existing `tests/test_gate_status.py`: remains green and supplies minimum-gate regression coverage;
- existing `tests/test_reconstruct_crafted_weapon_stats.py`: remains green and unchanged; D4 tests the separate receipt-consumer contract in `tests/test_context_first_weapon_evidence.py`.

The end-to-end feature test in `tests/test_context_first_scores.py` uses two equal-armor troops whose shields, skills, mounts, and crafting templates differ. It proves the old composite/proxy path would separate them while context-first defense keeps them equal, and proves unvalidated crafted melee is blank/queued rather than proxied.

CLI stdout is deterministic `key=value` lines:

```text
candidate=context_first_scores_v1
declarations=<count>
tuples_published=<count>
complete_rows=<count>
rankable_rows=<count>
review_rows=<count>
promotion_status=<not_run|passed|blocked>
output=<repo-relative-path>
```

Fatal errors go to stderr as `error_code=<CODE> field=<field> detail=<message>` and exit 2. Metadata carries per-code counts; reports surface them. No network, clock time, random UUID, or paid inference is used.

At D8, before a gate exists, the build adapter emits `promotion_status=not_run`. Once D9 has published a gate, the build adapter may report its verified status by reading the gate as data; it must not import or invoke the validator. The D9 validator has its own deterministic stdout and is the only command that changes the verdict.

Repository acceptance command:

```bash
python3 -m unittest discover -v
python3 scripts/scoring/build_context_first_candidate.py --repo .
python3 scripts/scoring/build_context_first_candidate.py --repo .
```

The second generation must leave `git diff --exit-code -- analysis/model_candidates/context_first_scores_v1` clean and all historical/frozen hash checks green.

## 19. Migration and cutover

1. D1 records current departures and immutable baselines without changing behavior.
2. D2-D6 add a parallel context-first policy/evidence path. Existing commands continue unchanged.
3. D7 publishes candidate score artifacts under the new root; nothing is canonical.
4. D8 establishes the new one-command candidate report entry point and updates the root README to present it as non-canonical evaluation work.
5. D9 publishes a blocked or passed promotion verdict independently of generation success.
6. If D9 is blocked, execution stops there with an exact evidence-acquisition request and does not cut consumers over.
7. After D9 passes for the exact candidate hashes, D10 adds one new immutable version package and updates `README.md` and `docs/research/EXECUTION_TRACKER.md` so new scoring/report requests point to the promoted context-first version. Historical reproduction commands stay documented and executable.
8. D10 removes only temporary scaffolding introduced in D1-D9. It does not rename, delete, or rewrite historical scripts, candidates, or pre-existing model versions.
9. Candidate-to-version copy is verified byte for byte (apart from explicitly version-owned metadata); no alias or unverified copy may make a candidate appear canonical.

## 20. File ownership by deliverable

### D1 — Current-candidate audit

Owns:

- `scripts/scoring/audit_context_first_candidates.py`
- `tests/test_audit_context_first_candidates.py`
- `analysis/model_candidates/context_first_scores_v1/CURRENT_CANDIDATE_AUDIT.md`
- `analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv`

It may read but not edit historical scripts/artifacts.

### D2 — Declaration contract

Owns:

- `scripts/scoring/context_first_contract.py`
- `tests/test_context_first_contract.py`
- `docs/methodology/007_context_first_scoring_candidate.md`
- `analysis/model_candidates/context_first_scores_v1/declarations/*.json`

It defines all stable enums, reason constants, decimal policy, declaration dataclasses, and validation.

### D3 — Armor lane

Owns the armor types/functions in:

- `scripts/scoring/context_first_equipment.py`
- `tests/test_context_first_armor.py`
- `tests/fixtures/context_first/armor/`

It must not add weapon formulas.

### D4 — Weapon normalization, evidence, and CraftedItem gate

Owns:

- `scripts/normalization/extract_weapon_attack_rows.py`
- `scripts/normalization/build_crafted_weapon_validation_receipt.py`
- `tests/test_extract_weapon_attack_rows.py`
- `tests/test_crafted_weapon_validation_receipt.py`
- `scripts/scoring/context_first_equipment.py`
- `tests/test_context_first_weapon_evidence.py`
- `tests/fixtures/context_first/weapons/`

It must not edit `scripts/normalization/reconstruct_crafted_weapon_stats.py`, change reconstruction arithmetic, accept unverified XML, infer source attack components from scalar audit cells, manufacture tooltip observations, or accept template proxies.

### D5 — Ranged policies

Owns:

- `scripts/scoring/context_first_ranged.py`
- `tests/test_context_first_ranged.py`
- `tests/fixtures/context_first/ranged/`

It supports only bows/arrows and crossbows/bolts.

### D6 — Context engine

Owns:

- `scripts/scoring/context_first_engine.py`
- `tests/test_context_first_engine.py`

It is the sole owner of effective mount-state, selected roster population, and question/mode dispatch.

### D7 — Score generation

Owns:

- `scripts/scoring/generate_context_first_scores.py`
- `tests/test_context_first_scores.py`
- generated-schema fixtures under `tests/fixtures/context_first/generated/`

It owns competition ranking and complete/rankable/review serialization in temporary test/scratch roots, not report prose or committed-root publication.

### D8 — Reports and reproducibility

Owns:

- `scripts/scoring/write_context_first_reports.py`
- `scripts/scoring/build_context_first_candidate.py`
- `scripts/scoring/context_first_publication.py`
- `tests/test_context_first_reports.py`
- `analysis/model_candidates/context_first_scores_v1/README.md`
- `analysis/model_candidates/context_first_scores_v1/realm_of_thrones/TOP10.md`
- all committed tuple outputs under `analysis/model_candidates/context_first_scores_v1/<track>/<context>/<question>/<attack_mode>/<mount_state>/`
- `input_hashes.csv`, `candidate_manifest.csv`, the pre-validation `artifact_hashes.csv`, and tuple `metadata.json`
- shared lock/staging/journal helpers in `context_first_publication.py`

It renders existing score contracts and owns package publication.

### D9 — Validation and promotion gate

Owns:

- `scripts/scoring/validate_context_first_candidate.py`
- `tests/test_context_first_validation.py`
- `analysis/model_candidates/context_first_scores_v1/VALIDATION_REPORT.md`
- `analysis/model_candidates/context_first_scores_v1/promotion_gate.json`
- `analysis/model_candidates/context_first_scores_v1/validation_input_hashes.csv`
- regeneration of the outer `artifact_hashes.csv` after validation outputs are staged

It reads empirical evidence without modifying it.

### D10 — Dedicated promotion, cutover, and cleanup

Owns:

- one new immutable version directory under `analysis/model_versions/`
- context-first sections of `README.md`
- context-first status/actions in `docs/research/EXECUTION_TRACKER.md`
- deletion of only superseded D1-D9 temporary scaffolding named in the implementing PR
- final cross-module adjustments and tests required by integration

It may run only when D9 reports `promotion_allowed=true` for the exact candidate manifest. It owns no pre-existing historical/frozen file and may add, but never later mutate, the newly declared version.

## 21. Execution waves and merge order

Each deliverable is a separate reviewable PR unless two adjacent deliverables are intentionally combined before implementation and remain independently testable. Every PR targets `main`, runs its focused tests plus repository validation, pushes, self-reviews the latest pushed head, fixes actionable findings, revalidates, updates the PR body, marks ready only after gates pass, squash-merges, verifies the PR is closed, and verifies the squash commit on `main`.

### Wave 0 — Preflight

1. Create/verify one isolated worktree per deliverable branch from current `origin/main`.
2. Confirm no unrelated dirty files.
3. Run `python3 -m unittest discover -v`; baseline must be green or the exact pre-existing failure is recorded before work.
4. Confirm `historical_baseline_hashes.csv` does not yet exist before D1, then treat it as immutable assertion after D1.

### Wave 1 — Audit

1. Implement and merge D1.
2. Rebase every later branch on the D1 squash commit.

### Wave 2 — Contract

1. Implement and merge D2 after D1.
2. Rebase D3 and D4 branches on the D2 squash commit.

### Wave 3 — Parallel evidence lanes

1. Implement D3 and D4 in parallel from D2 because their tests and responsibilities are independent.
2. Merge D3 first.
3. Rebase D4 onto main, preserving D3 armor code and adding only weapon sections; resolve the shared-file integration deliberately.
4. Run both armor and weapon suites on D4 head, then merge D4.

D3 and D4 are parallel implementation lanes, not simultaneous merge lanes; `context_first_equipment.py` has one final linear history.

### Wave 4 — Ranged and context

1. Implement/merge D5 after D4.
2. Implement/merge D6 after D3, D4, and D5 are on main.

### Wave 5 — Candidate outputs

1. Implement/merge D7 after D6.
2. Implement/merge D8 after D7.

### Wave 6 — Validation, promotion, and cutover

1. Implement/merge D9 after D8. A reproducible blocked promotion gate is an acceptable D9 output but a hard stop for the overall execution; invalid candidate generation is not.
2. Implement/merge D10 only after D9 returns a passing exact-hash verdict. If D9 is blocked, record the evidence-acquisition request and wait.
3. On final main, run full tests and two complete regenerations, verify immutable hashes, verify all D1-D10 PRs are closed, and verify each squash commit is reachable from `origin/main`.

Merge order:

```text
D1 -> D2 -> D3 -> D4 -> D5 -> D6 -> D7 -> D8 -> D9 -> D10
```

## 22. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Audit rows do not represent all engine attack-row variants | Publish source occurrence and selected swing/thrust cells exactly; do not infer missing attacks; queue absent rows. |
| Crafted reconstruction says reconstructed but tooltip proof is only console text | Require a separate hash-pinned per-item validation receipt. |
| Alternative rosters/items have unknown probabilities | Use declared arithmetic means and publish every intermediate; never select the best. |
| One incomplete alternative biases a known mean | Blank the containing roster/troop component and queue the exact source gap. |
| Projectile fields tempt a future implementation to re-enter v1 output | Publish projectile damage for provenance only; v1 per-shot output remains weapon damage, same-slot alternatives remain separate loadouts, and any later projectile contribution requires a new declaration and tests. |
| Mounted declarations accidentally introduce mount stats | Mount state selects rosters only; scorer contracts contain no mount numeric fields; siege strips mount rows before resolution. |
| General output gains an implicit blend during reporting | Combined fields are structurally `None`; reports have no combined sort path. |
| Partial regeneration mixes old/new tracks | Committed-root generation always processes every declaration and publishes a validated staged tree transactionally. |
| Interrupted directory swap loses the package | Lock, journal, validated backup, startup recovery, and post-swap manifest verification. |
| Historical/frozen artifacts drift during implementation | Checked-in D1 baseline hashes are verified by every integration run and before/after publication. |
| Insufficient empirical evidence is mistaken for generation failure | Promotion uses machine-readable `blocked` status with generation complete and exit 0. |
| Name-based empirical joins leak across tracks | Require verified canonical IDs and exact track/context/side join keys. |
| D3/D4 conflict in a shared module | Parallelize implementation only, merge D3 first, rebase D4, and run both suites before D4 merge. |
| New abstractions duplicate historical helpers | Reuse behavior only through new context-first contracts; historical modules remain immutable, so small intentional duplication at the candidate boundary is safer than coupling new policy to old formulas. |

## 23. Acceptance mapping

Functional requirements:

- FR-1: D1.
- FR-2: D2.
- FR-3: D3.
- FR-4 and FR-5: D4.
- FR-6: D5.
- FR-7: D6.
- FR-8 through FR-11: D7, with D6 supplying context/population selection.
- FR-12 and FR-13: D8.
- FR-14: D9.
- FR-15: D9 owns the promotion verdict and D10 owns immutable cutover.

Acceptance criteria:

- AC-1: D1; AC-2: D2; AC-3 and AC-4: D3; AC-5 and AC-6: D4.
- AC-7 through AC-9: D5; AC-10: D6; AC-11: D7.
- AC-12: D7 owns theoretical track/context/hero/population isolation and D9 owns empirical player/enemy side proof.
- AC-13: D8; AC-14: D9; AC-15: D10 plus the per-deliverable delivery rule.
- NFR determinism, traceability, immutability, testability, offline behavior, and safe reruns: D1-D10 integration tests and D8 transaction/manifest ownership.

## 24. Explicitly out of scope

- Any edit under `analysis/model_versions/` before D10; D10 may add one new immutable version only after a passing exact-hash promotion gate.
- Regeneration or relabeling of historical role score or defense-v2 artifacts.
- Promotion that lacks a passing D9 verdict or rewrites an existing canonical version.
- A universal or general-capability numeric blend.
- Speed, skill, shields, mounts, harnesses, charge, reach, damage-type multipliers, mobility, reliability, perks, or hidden normalization.
- Throwing, slings, or ranged families other than bow/arrow and crossbow/bolt.
- Name/provisional-slug empirical joins.
- Network access, paid inference, dependency upgrades, unrelated refactors, or formatting.

Executor: read @execute-locked-plan before editing.
