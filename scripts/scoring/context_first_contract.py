#!/usr/bin/env python3
"""Strict declaration contract for the context-first scoring candidate."""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
from enum import Enum
from pathlib import Path
from typing import Mapping, Sequence


SCHEMA_VERSION = "context-first-scoring-declaration:v1"
CANDIDATE_ID = "context_first_scores_v1"
SUPPORTED_TRACKS = ("nightmare_sails", "realm_of_thrones", "taom", "vanilla")
DECIMAL_QUANTUM = Decimal("0.000001")
DECIMAL_ROUNDING = ROUND_HALF_EVEN

DECL_MISSING_FIELD = "DECL_MISSING_FIELD"
DECL_UNKNOWN_FIELD = "DECL_UNKNOWN_FIELD"
DECL_INVALID_ENUM = "DECL_INVALID_ENUM"
DECL_INVALID_DRIVER_SET = "DECL_INVALID_DRIVER_SET"
DECL_INVALID_ARMOR_CONTRACT = "DECL_INVALID_ARMOR_CONTRACT"
DECL_INVALID_WEAPON_CONTRACT = "DECL_INVALID_WEAPON_CONTRACT"
DECL_AMMUNITION_POLICY_MISMATCH = "DECL_AMMUNITION_POLICY_MISMATCH"
DECL_SIEGE_DEFENSE_MUST_DISMOUNT = "DECL_SIEGE_DEFENSE_MUST_DISMOUNT"
DECL_GENERAL_BLEND_FORBIDDEN = "DECL_GENERAL_BLEND_FORBIDDEN"
DECL_NONFINITE_NUMBER = "DECL_NONFINITE_NUMBER"

# Public review and promotion reason vocabulary for schema v1.
SOURCE_ARTIFACT_ABSENT = "SOURCE_ARTIFACT_ABSENT"
CONTEXT_UNDECLARED = "CONTEXT_UNDECLARED"
QUESTION_MIXED = "QUESTION_MIXED"
ATTACK_MODE_UNDECLARED = "ATTACK_MODE_UNDECLARED"
MOUNT_STATE_UNDECLARED = "MOUNT_STATE_UNDECLARED"
IRRELEVANT_DRIVER_INCLUDED = "IRRELEVANT_DRIVER_INCLUDED"
TEMPLATE_PROXY_USED = "TEMPLATE_PROXY_USED"
MISSING_VALUE_ZERO_FILLED = "MISSING_VALUE_ZERO_FILLED"
AMMUNITION_POLICY_UNDECLARED = "AMMUNITION_POLICY_UNDECLARED"
MOUNTED_INPUT_NON_APPLICABLE = "MOUNTED_INPUT_NON_APPLICABLE"

TROOP_ROSTER_MISSING = "TROOP_ROSTER_MISSING"
MOUNT_STATE_ROSTER_MISSING = "MOUNT_STATE_ROSTER_MISSING"
MOUNT_STATE_EVIDENCE_UNRESOLVED = "MOUNT_STATE_EVIDENCE_UNRESOLVED"
ARMOR_ITEM_ID_MISSING = "ARMOR_ITEM_ID_MISSING"
ARMOR_ITEM_UNRESOLVED = "ARMOR_ITEM_UNRESOLVED"
ARMOR_REGION_MISSING = "ARMOR_REGION_MISSING"
ARMOR_VALUE_INVALID = "ARMOR_VALUE_INVALID"
WEAPON_ITEM_ID_MISSING = "WEAPON_ITEM_ID_MISSING"
WEAPON_ITEM_UNRESOLVED = "WEAPON_ITEM_UNRESOLVED"
WEAPON_ATTACK_ROW_MISSING = "WEAPON_ATTACK_ROW_MISSING"
WEAPON_DAMAGE_INVALID = "WEAPON_DAMAGE_INVALID"
CRAFTED_RECONSTRUCTION_MISSING = "CRAFTED_RECONSTRUCTION_MISSING"
CRAFTED_RECONSTRUCTION_INCOMPLETE = "CRAFTED_RECONSTRUCTION_INCOMPLETE"
CRAFTED_PROVENANCE_INCOMPLETE = "CRAFTED_PROVENANCE_INCOMPLETE"
CRAFTED_TOOLTIP_RECEIPT_MISSING = "CRAFTED_TOOLTIP_RECEIPT_MISSING"
CRAFTED_TOOLTIP_RECEIPT_HASH_MISMATCH = "CRAFTED_TOOLTIP_RECEIPT_HASH_MISMATCH"
CRAFTED_TOOLTIP_VALIDATION_MISSING = "CRAFTED_TOOLTIP_VALIDATION_MISSING"
CRAFTED_TOOLTIP_VALIDATION_FAILED = "CRAFTED_TOOLTIP_VALIDATION_FAILED"
RANGED_FAMILY_UNSUPPORTED = "RANGED_FAMILY_UNSUPPORTED"
RANGED_PROJECTILE_MISSING = "RANGED_PROJECTILE_MISSING"
RANGED_PROJECTILE_INCOMPATIBLE = "RANGED_PROJECTILE_INCOMPATIBLE"
RANGED_PROJECTILE_DAMAGE_MISSING = "RANGED_PROJECTILE_DAMAGE_MISSING"
RANGED_AMMO_COUNT_MISSING = "RANGED_AMMO_COUNT_MISSING"
RANGED_AMMO_COUNT_INVALID = "RANGED_AMMO_COUNT_INVALID"

REVIEW_REASON_CODES = (
    TROOP_ROSTER_MISSING, MOUNT_STATE_ROSTER_MISSING, MOUNT_STATE_EVIDENCE_UNRESOLVED,
    ARMOR_ITEM_ID_MISSING, ARMOR_ITEM_UNRESOLVED, ARMOR_REGION_MISSING,
    ARMOR_VALUE_INVALID, WEAPON_ITEM_ID_MISSING, WEAPON_ITEM_UNRESOLVED,
    WEAPON_ATTACK_ROW_MISSING, WEAPON_DAMAGE_INVALID, CRAFTED_RECONSTRUCTION_MISSING,
    CRAFTED_RECONSTRUCTION_INCOMPLETE, CRAFTED_PROVENANCE_INCOMPLETE,
    CRAFTED_TOOLTIP_RECEIPT_MISSING, CRAFTED_TOOLTIP_RECEIPT_HASH_MISMATCH,
    CRAFTED_TOOLTIP_VALIDATION_MISSING, CRAFTED_TOOLTIP_VALIDATION_FAILED,
    RANGED_FAMILY_UNSUPPORTED, RANGED_PROJECTILE_MISSING,
    RANGED_PROJECTILE_INCOMPATIBLE, RANGED_PROJECTILE_DAMAGE_MISSING,
    RANGED_AMMO_COUNT_MISSING, RANGED_AMMO_COUNT_INVALID,
)

PROMOTION_CANONICAL_JOIN_INCOMPLETE = "PROMOTION_CANONICAL_JOIN_INCOMPLETE"
PROMOTION_EMPIRICAL_GATE_INSUFFICIENT = "PROMOTION_EMPIRICAL_GATE_INSUFFICIENT"
PROMOTION_GROUPED_OOS_MISSING = "PROMOTION_GROUPED_OOS_MISSING"
PROMOTION_CONTROLLED_EVIDENCE_MISSING = "PROMOTION_CONTROLLED_EVIDENCE_MISSING"
PROMOTION_REPRODUCIBILITY_FAILED = "PROMOTION_REPRODUCIBILITY_FAILED"
PROMOTION_LIMITATIONS_REVIEW_MISSING = "PROMOTION_LIMITATIONS_REVIEW_MISSING"
PROMOTION_BOUNDARY_VIOLATION = "PROMOTION_BOUNDARY_VIOLATION"

PROMOTION_REASON_CODES = (
    PROMOTION_CANONICAL_JOIN_INCOMPLETE, PROMOTION_EMPIRICAL_GATE_INSUFFICIENT,
    PROMOTION_GROUPED_OOS_MISSING, PROMOTION_CONTROLLED_EVIDENCE_MISSING,
    PROMOTION_REPRODUCIBILITY_FAILED, PROMOTION_LIMITATIONS_REVIEW_MISSING,
    PROMOTION_BOUNDARY_VIOLATION,
)


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


@dataclass(frozen=True, order=True)
class ContractIssue:
    code: str
    field: str
    message: str


class DeclarationError(ValueError):
    def __init__(self, issues: Sequence[ContractIssue]):
        self.issues = tuple(sorted(issues, key=lambda issue: (issue.field, issue.code, issue.message)))
        super().__init__("\n".join(_format_issue(issue) for issue in self.issues))


class _DuplicateKeyError(ValueError):
    def __init__(self, key: str):
        self.key = key
        super().__init__(f"duplicate JSON key: {key}")


TOP_LEVEL_FIELDS = {
    "schema_version", "candidate_id", "track", "context", "question", "attack_mode",
    "mount_state", "primary_drivers", "ammunition_policy", "secondary_drivers",
    "armor_source_fields", "armor_aggregation", "weapon_damage_source_fields",
    "projectile_contribution", "roster_aggregation", "combination_rule",
}
ARMOR_FIELDS = ("head_armor", "body_armor", "arm_armor", "leg_armor")
WEAPON_FIELDS = ("swing_damage", "thrust_damage")
ARMOR_WEIGHTS = {
    "head_armor": Decimal("0.35"), "body_armor": Decimal("0.55"),
    "arm_armor": Decimal("0.05"), "leg_armor": Decimal("0.05"),
}


def _issue(code: str, field: str, message: str) -> ContractIssue:
    return ContractIssue(field=field, code=code, message=message)


def _format_issue(issue: ContractIssue) -> str:
    return f"error_code={issue.code} field={issue.field} detail={issue.message}"


def _reject_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(key)
        result[key] = value
    return result


def _string_list(value: object) -> tuple[str, ...] | None:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        return None
    return tuple(value)


def _decimal(value: object, field: str, issues: list[ContractIssue]) -> Decimal | None:
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        issues.append(_issue(DECL_INVALID_ARMOR_CONTRACT, field, "must be a decimal value"))
        return None
    if isinstance(value, float) and not math.isfinite(value):
        issues.append(_issue(DECL_NONFINITE_NUMBER, field, "must be finite"))
        return None
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError):
        issues.append(_issue(DECL_INVALID_ARMOR_CONTRACT, field, "must be a decimal value"))
        return None
    if not parsed.is_finite():
        issues.append(_issue(DECL_NONFINITE_NUMBER, field, "must be finite"))
        return None
    return parsed


def _enum_value(value: object, enum_type: type[Enum], field: str, issues: list[ContractIssue]) -> str | None:
    allowed = tuple(member.value for member in enum_type)
    if not isinstance(value, str) or value not in allowed:
        issues.append(_issue(DECL_INVALID_ENUM, field, f"must be one of {','.join(allowed)}"))
        return None
    return value


def validate_declaration(value: Mapping[str, object]) -> tuple[ContractIssue, ...]:
    issues: list[ContractIssue] = []
    if not isinstance(value, Mapping):
        return (_issue(DECL_INVALID_ENUM, "$", "declaration must be a JSON object"),)

    for field in sorted(TOP_LEVEL_FIELDS - set(value)):
        issues.append(_issue(DECL_MISSING_FIELD, field, "required field is missing"))
    for field in sorted(set(value) - TOP_LEVEL_FIELDS):
        issues.append(_issue(DECL_UNKNOWN_FIELD, field, "unknown field"))

    if value.get("schema_version") != SCHEMA_VERSION:
        issues.append(_issue(DECL_INVALID_ENUM, "schema_version", f"must equal {SCHEMA_VERSION}"))
    if value.get("candidate_id") != CANDIDATE_ID:
        issues.append(_issue(DECL_INVALID_ENUM, "candidate_id", f"must equal {CANDIDATE_ID}"))
    track = value.get("track")
    if not isinstance(track, str) or track not in SUPPORTED_TRACKS:
        issues.append(_issue(DECL_INVALID_ENUM, "track", f"must be one of {','.join(SUPPORTED_TRACKS)}"))

    context = _enum_value(value.get("context"), BattleContext, "context", issues)
    question = _enum_value(value.get("question"), TroopQuestion, "question", issues)
    attack_mode = _enum_value(value.get("attack_mode"), AttackMode, "attack_mode", issues)
    mount_state = _enum_value(value.get("mount_state"), MountState, "mount_state", issues)
    ammunition = _enum_value(value.get("ammunition_policy"), AmmunitionPolicy, "ammunition_policy", issues)

    primary = _string_list(value.get("primary_drivers"))
    secondary = _string_list(value.get("secondary_drivers"))
    armor_fields = _string_list(value.get("armor_source_fields"))
    weapon_fields = _string_list(value.get("weapon_damage_source_fields"))
    for field, parsed in (("primary_drivers", primary), ("secondary_drivers", secondary)):
        if parsed is None:
            issues.append(_issue(DECL_INVALID_DRIVER_SET, field, "must be an ordered string array"))
    if secondary not in (None, ()):
        issues.append(_issue(DECL_INVALID_DRIVER_SET, "secondary_drivers", "schema v1 forbids secondary drivers"))
    if armor_fields is None:
        issues.append(_issue(DECL_INVALID_ARMOR_CONTRACT, "armor_source_fields", "must be an ordered string array"))
    if weapon_fields is None:
        issues.append(_issue(DECL_INVALID_WEAPON_CONTRACT, "weapon_damage_source_fields", "must be an ordered string array"))

    aggregation = value.get("armor_aggregation")
    parsed_weights: dict[str, Decimal] | None = None
    aggregation_id: object = None
    if aggregation is not None:
        if not isinstance(aggregation, Mapping):
            issues.append(_issue(DECL_INVALID_ARMOR_CONTRACT, "armor_aggregation", "must be null or an object"))
        else:
            allowed = {"aggregation_id", "weights"}
            for field in sorted(allowed - set(aggregation)):
                issues.append(_issue(DECL_MISSING_FIELD, f"armor_aggregation.{field}", "required field is missing"))
            for field in sorted(set(aggregation) - allowed):
                issues.append(_issue(DECL_UNKNOWN_FIELD, f"armor_aggregation.{field}", "unknown field"))
            aggregation_id = aggregation.get("aggregation_id")
            weights = aggregation.get("weights")
            if not isinstance(weights, Mapping):
                issues.append(_issue(DECL_INVALID_ARMOR_CONTRACT, "armor_aggregation.weights", "must be an object"))
            else:
                for field in sorted(set(ARMOR_FIELDS) - set(weights)):
                    issues.append(_issue(DECL_MISSING_FIELD, f"armor_aggregation.weights.{field}", "required field is missing"))
                for field in sorted(set(weights) - set(ARMOR_FIELDS)):
                    issues.append(_issue(DECL_UNKNOWN_FIELD, f"armor_aggregation.weights.{field}", "unknown field"))
                parsed_weights = {}
                for field in ARMOR_FIELDS:
                    if field in weights:
                        parsed = _decimal(weights[field], f"armor_aggregation.weights.{field}", issues)
                        if parsed is not None:
                            parsed_weights[field] = parsed

    projectile = value.get("projectile_contribution")
    if projectile not in ("not_applicable", "not_included"):
        issues.append(_issue(DECL_INVALID_ENUM, "projectile_contribution", "must be not_applicable or not_included"))
    if value.get("roster_aggregation") != "arithmetic_mean":
        issues.append(_issue(DECL_INVALID_ENUM, "roster_aggregation", "must equal arithmetic_mean"))
    combination = value.get("combination_rule")
    if combination not in ("not_applicable", "none"):
        issues.append(_issue(DECL_GENERAL_BLEND_FORBIDDEN, "combination_rule", "schema v1 permits only not_applicable or none"))

    needs_armor = question in ("defense", "general")
    needs_weapon = question in ("attack", "general")
    expected_primary = {
        "defense": ("worn_armor",),
        "attack": ("weapon_output",),
        "general": ("worn_armor", "weapon_output"),
    }.get(question)
    if expected_primary is not None and primary != expected_primary:
        issues.append(_issue(DECL_INVALID_DRIVER_SET, "primary_drivers", f"must equal {list(expected_primary)} for {question}"))

    if needs_armor:
        if armor_fields != ARMOR_FIELDS:
            issues.append(_issue(DECL_INVALID_ARMOR_CONTRACT, "armor_source_fields", f"must equal {list(ARMOR_FIELDS)}"))
        if aggregation is None or aggregation_id != "survivability_armor_v71" or parsed_weights != ARMOR_WEIGHTS:
            issues.append(_issue(DECL_INVALID_ARMOR_CONTRACT, "armor_aggregation", "must equal the survivability_armor_v71 weighted armor contract"))
    elif question == "attack":
        if armor_fields not in (None, ()):
            issues.append(_issue(DECL_INVALID_ARMOR_CONTRACT, "armor_source_fields", "attack declarations cannot include armor source fields"))
        if aggregation is not None:
            issues.append(_issue(DECL_INVALID_ARMOR_CONTRACT, "armor_aggregation", "attack declarations cannot include armor aggregation"))

    if needs_weapon:
        if weapon_fields != WEAPON_FIELDS:
            issues.append(_issue(DECL_INVALID_WEAPON_CONTRACT, "weapon_damage_source_fields", f"must equal {list(WEAPON_FIELDS)}"))
    elif question == "defense" and weapon_fields not in (None, ()):
        issues.append(_issue(DECL_INVALID_WEAPON_CONTRACT, "weapon_damage_source_fields", "defense declarations cannot include weapon inputs"))

    expected_combination = "none" if question == "general" else "not_applicable"
    if combination in ("not_applicable", "none") and question is not None and combination != expected_combination:
        issues.append(_issue(DECL_GENERAL_BLEND_FORBIDDEN, "combination_rule", f"must equal {expected_combination} for {question}"))

    if attack_mode == "ranged" and question == "defense":
        issues.append(_issue(DECL_INVALID_WEAPON_CONTRACT, "attack_mode", "defense declarations use melee mode because no weapon driver is read"))
    expected_projectile = "not_included" if attack_mode == "ranged" else "not_applicable"
    if projectile in ("not_applicable", "not_included") and attack_mode is not None and projectile != expected_projectile:
        issues.append(_issue(DECL_INVALID_WEAPON_CONTRACT, "projectile_contribution", f"must equal {expected_projectile} for {attack_mode}"))

    if attack_mode == "ranged":
        expected_ammunition = "unlimited" if context == "siege_defense" else "finite"
    else:
        expected_ammunition = "not_applicable"
    if ammunition is not None and attack_mode is not None and context is not None and ammunition != expected_ammunition:
        issues.append(_issue(DECL_AMMUNITION_POLICY_MISMATCH, "ammunition_policy", f"must equal {expected_ammunition} for {context}/{attack_mode}"))
    if context == "siege_defense" and mount_state == "mounted":
        issues.append(_issue(DECL_SIEGE_DEFENSE_MUST_DISMOUNT, "mount_state", "siege defense must be dismounted"))

    return tuple(sorted(set(issues), key=lambda issue: (issue.field, issue.code, issue.message)))


def parse_declaration(value: Mapping[str, object]) -> ScoringDeclaration:
    issues = validate_declaration(value)
    if issues:
        raise DeclarationError(issues)
    aggregation = value["armor_aggregation"]
    parsed_aggregation = None
    if aggregation is not None:
        weights = aggregation["weights"]
        parsed_aggregation = ArmorAggregation(
            aggregation_id=str(aggregation["aggregation_id"]),
            head_weight=Decimal(str(weights["head_armor"])),
            body_weight=Decimal(str(weights["body_armor"])),
            arm_weight=Decimal(str(weights["arm_armor"])),
            leg_weight=Decimal(str(weights["leg_armor"])),
        )
    return ScoringDeclaration(
        schema_version=str(value["schema_version"]), candidate_id=str(value["candidate_id"]),
        track=str(value["track"]), context=BattleContext(str(value["context"])),
        question=TroopQuestion(str(value["question"])), attack_mode=AttackMode(str(value["attack_mode"])),
        mount_state=MountState(str(value["mount_state"])), primary_drivers=tuple(value["primary_drivers"]),
        ammunition_policy=AmmunitionPolicy(str(value["ammunition_policy"])),
        secondary_drivers=tuple(value["secondary_drivers"]), armor_source_fields=tuple(value["armor_source_fields"]),
        armor_aggregation=parsed_aggregation, weapon_damage_source_fields=tuple(value["weapon_damage_source_fields"]),
        projectile_contribution=str(value["projectile_contribution"]),
        roster_aggregation=str(value["roster_aggregation"]), combination_rule=str(value["combination_rule"]),
    )


def load_declaration(path: Path) -> ScoringDeclaration:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=lambda token: Decimal(token),
        )
    except _DuplicateKeyError as error:
        raise DeclarationError(
            (_issue(DECL_INVALID_ENUM, error.key, "duplicate JSON key is forbidden"),)
        ) from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise DeclarationError((_issue(DECL_INVALID_ENUM, "$", f"cannot load declaration: {error}"),)) from error
    return parse_declaration(value)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 1:
        print("usage: context_first_contract.py <declaration.json>", file=sys.stderr)
        return 2
    try:
        declaration = load_declaration(Path(arguments[0]))
    except DeclarationError as error:
        for issue in error.issues:
            print(_format_issue(issue), file=sys.stderr)
        return 2
    print(f"candidate_id={declaration.candidate_id}")
    print(f"tuple={declaration.track}/{declaration.context.value}/{declaration.question.value}/{declaration.attack_mode.value}/{declaration.mount_state.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
