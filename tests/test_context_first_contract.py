from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from decimal import Decimal
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts/scoring"))
import context_first_contract as contract  # noqa: E402


def valid_declaration(
    *,
    track: str = "realm_of_thrones",
    context: str = "field",
    question: str = "defense",
    attack_mode: str = "melee",
    mount_state: str = "dismounted",
) -> dict[str, object]:
    armor = question in ("defense", "general")
    weapon = question in ("attack", "general")
    ranged_mode = attack_mode == "ranged"
    return {
        "schema_version": contract.SCHEMA_VERSION,
        "candidate_id": contract.CANDIDATE_ID,
        "track": track,
        "context": context,
        "question": question,
        "attack_mode": attack_mode,
        "mount_state": mount_state,
        "primary_drivers": (
            ["worn_armor", "weapon_output"]
            if question == "general"
            else ["worn_armor"] if question == "defense" else ["weapon_output"]
        ),
        "ammunition_policy": (
            "unlimited" if ranged_mode and context == "siege_defense"
            else "finite" if ranged_mode else "not_applicable"
        ),
        "secondary_drivers": [],
        "armor_source_fields": list(contract.ARMOR_FIELDS) if armor else [],
        "armor_aggregation": {
            "aggregation_id": "survivability_armor_v71",
            "weights": {
                "head_armor": "0.35",
                "body_armor": "0.55",
                "arm_armor": "0.05",
                "leg_armor": "0.05",
            },
        } if armor else None,
        "weapon_damage_source_fields": list(contract.WEAPON_FIELDS) if weapon else [],
        "projectile_contribution": "not_included" if ranged_mode else "not_applicable",
        "roster_aggregation": "arithmetic_mean",
        "combination_rule": "none" if question == "general" else "not_applicable",
    }


class ContextFirstContractTests(unittest.TestCase):
    def assert_issue(self, value: dict[str, object], code: str, field: str) -> None:
        issues = contract.validate_declaration(value)
        self.assertIn((code, field), {(issue.code, issue.field) for issue in issues})

    def test_valid_defense_attack_and_general_contracts_parse(self) -> None:
        cases = (
            valid_declaration(question="defense"),
            valid_declaration(question="attack", attack_mode="melee"),
            valid_declaration(question="attack", attack_mode="ranged"),
            valid_declaration(context="siege_defense", question="general", attack_mode="ranged"),
        )
        for value in cases:
            with self.subTest(value=value):
                declaration = contract.parse_declaration(value)
                self.assertEqual(contract.CANDIDATE_ID, declaration.candidate_id)
                self.assertIsInstance(declaration.context, contract.BattleContext)

    def test_parsed_contract_is_immutable_and_uses_decimal_weights(self) -> None:
        declaration = contract.parse_declaration(valid_declaration())
        self.assertEqual(Decimal("0.55"), declaration.armor_aggregation.body_weight)
        with self.assertRaises(FrozenInstanceError):
            declaration.track = "vanilla"

    def test_missing_and_unknown_fields_are_both_reported_in_stable_order(self) -> None:
        value = valid_declaration()
        del value["track"]
        value["mystery"] = True
        issues = contract.validate_declaration(value)
        self.assertEqual(tuple(sorted(issues, key=lambda issue: (issue.field, issue.code, issue.message))), issues)
        self.assertIn((contract.DECL_MISSING_FIELD, "track"), {(issue.code, issue.field) for issue in issues})
        self.assertIn((contract.DECL_UNKNOWN_FIELD, "mystery"), {(issue.code, issue.field) for issue in issues})

    def test_exact_schema_candidate_track_and_enums_are_required(self) -> None:
        mutations = (
            ("schema_version", "v2", "schema_version"),
            ("candidate_id", "other", "candidate_id"),
            ("track", "other", "track"),
            ("context", "camp", "context"),
            ("question", "utility", "question"),
            ("attack_mode", "mixed", "attack_mode"),
            ("mount_state", "sometimes", "mount_state"),
        )
        for key, replacement, field in mutations:
            value = valid_declaration()
            value[key] = replacement
            with self.subTest(field=field):
                self.assert_issue(value, contract.DECL_INVALID_ENUM, field)

    def test_secondary_or_hidden_drivers_are_rejected(self) -> None:
        value = valid_declaration()
        value["secondary_drivers"] = ["shield_hp"]
        self.assert_issue(value, contract.DECL_INVALID_DRIVER_SET, "secondary_drivers")
        value = valid_declaration()
        value["primary_drivers"] = ["worn_armor", "riding"]
        self.assert_issue(value, contract.DECL_INVALID_DRIVER_SET, "primary_drivers")

    def test_defense_rejects_weapon_armor_or_ammunition_drift(self) -> None:
        value = valid_declaration()
        value["weapon_damage_source_fields"] = ["swing_damage", "thrust_damage"]
        self.assert_issue(value, contract.DECL_INVALID_WEAPON_CONTRACT, "weapon_damage_source_fields")
        value = valid_declaration()
        value["ammunition_policy"] = "finite"
        self.assert_issue(value, contract.DECL_AMMUNITION_POLICY_MISMATCH, "ammunition_policy")

    def test_attack_rejects_armor_and_requires_exact_weapon_fields(self) -> None:
        value = valid_declaration(question="attack")
        value["armor_aggregation"] = copy.deepcopy(valid_declaration()["armor_aggregation"])
        self.assert_issue(value, contract.DECL_INVALID_ARMOR_CONTRACT, "armor_aggregation")
        value = valid_declaration(question="attack")
        value["weapon_damage_source_fields"] = ["swing_damage"]
        self.assert_issue(value, contract.DECL_INVALID_WEAPON_CONTRACT, "weapon_damage_source_fields")

    def test_general_requires_two_separate_components_and_no_blend(self) -> None:
        value = valid_declaration(question="general")
        value["combination_rule"] = "weighted_sum"
        self.assert_issue(value, contract.DECL_GENERAL_BLEND_FORBIDDEN, "combination_rule")
        value = valid_declaration(question="general")
        value["combination_rule"] = "not_applicable"
        self.assert_issue(value, contract.DECL_GENERAL_BLEND_FORBIDDEN, "combination_rule")

    def test_ranged_policy_is_finite_outside_siege_defense(self) -> None:
        for context in ("field", "siege_attack"):
            value = valid_declaration(context=context, question="attack", attack_mode="ranged")
            value["ammunition_policy"] = "unlimited"
            with self.subTest(context=context):
                self.assert_issue(value, contract.DECL_AMMUNITION_POLICY_MISMATCH, "ammunition_policy")

    def test_ranged_siege_defense_requires_unlimited_and_dismounted(self) -> None:
        value = valid_declaration(context="siege_defense", question="attack", attack_mode="ranged")
        value["ammunition_policy"] = "finite"
        value["mount_state"] = "mounted"
        issues = {(issue.code, issue.field) for issue in contract.validate_declaration(value)}
        self.assertIn((contract.DECL_AMMUNITION_POLICY_MISMATCH, "ammunition_policy"), issues)
        self.assertIn((contract.DECL_SIEGE_DEFENSE_MUST_DISMOUNT, "mount_state"), issues)

    def test_non_ranged_never_accepts_finite_or_unlimited_ammunition(self) -> None:
        for policy in ("finite", "unlimited"):
            value = valid_declaration(question="attack")
            value["ammunition_policy"] = policy
            with self.subTest(policy=policy):
                self.assert_issue(value, contract.DECL_AMMUNITION_POLICY_MISMATCH, "ammunition_policy")

    def test_ranged_projectile_is_declared_but_inert(self) -> None:
        value = valid_declaration(question="attack", attack_mode="ranged")
        value["projectile_contribution"] = "not_applicable"
        self.assert_issue(value, contract.DECL_INVALID_WEAPON_CONTRACT, "projectile_contribution")

    def test_defense_cannot_disguise_itself_as_ranged(self) -> None:
        value = valid_declaration(question="defense", attack_mode="ranged")
        self.assert_issue(value, contract.DECL_INVALID_WEAPON_CONTRACT, "attack_mode")

    def test_armor_contract_rejects_wrong_weights_nested_unknowns_and_nonfinite_values(self) -> None:
        value = valid_declaration()
        value["armor_aggregation"]["weights"]["body_armor"] = "0.54"
        self.assert_issue(value, contract.DECL_INVALID_ARMOR_CONTRACT, "armor_aggregation")
        value = valid_declaration()
        value["armor_aggregation"]["weights"]["shield"] = "1"
        self.assert_issue(value, contract.DECL_UNKNOWN_FIELD, "armor_aggregation.weights.shield")
        value = valid_declaration()
        value["armor_aggregation"]["weights"]["head_armor"] = float("inf")
        self.assert_issue(value, contract.DECL_NONFINITE_NUMBER, "armor_aggregation.weights.head_armor")

    def test_roster_aggregation_has_no_implicit_default(self) -> None:
        value = valid_declaration()
        value["roster_aggregation"] = "maximum"
        self.assert_issue(value, contract.DECL_INVALID_ENUM, "roster_aggregation")

    def test_load_rejects_json_nonfinite_constant(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "invalid.json"
            value = valid_declaration()
            path.write_text(json.dumps(value).replace('"0.35"', "NaN"), encoding="utf-8")
            with self.assertRaises(contract.DeclarationError) as raised:
                contract.load_declaration(path)
        self.assertIn(contract.DECL_NONFINITE_NUMBER, {issue.code for issue in raised.exception.issues})

    def test_cli_returns_two_and_prints_field_specific_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "invalid.json"
            value = valid_declaration(context="siege_defense")
            value["mount_state"] = "mounted"
            path.write_text(json.dumps(value), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(REPO_ROOT / "scripts/scoring/context_first_contract.py"), str(path)],
                check=False, capture_output=True, text=True,
            )
        self.assertEqual(2, result.returncode)
        self.assertIn("error_code=DECL_SIEGE_DEFENSE_MUST_DISMOUNT field=mount_state", result.stderr)
        self.assertEqual("", result.stdout)

    def test_every_committed_declaration_has_canonical_name_and_parses(self) -> None:
        declaration_root = REPO_ROOT / "analysis/model_candidates/context_first_scores_v1/declarations"
        paths = sorted(declaration_root.glob("*.json"))
        self.assertEqual(100, len(paths))
        seen: set[tuple[str, str, str, str, str]] = set()
        for path in paths:
            declaration = contract.load_declaration(path)
            identity = (
                declaration.track, declaration.context.value, declaration.question.value,
                declaration.attack_mode.value, declaration.mount_state.value,
            )
            self.assertNotIn(identity, seen)
            seen.add(identity)
            self.assertEqual("__".join(identity) + ".json", path.name)

    def test_reason_code_vocabulary_has_no_duplicates(self) -> None:
        self.assertEqual(len(contract.REVIEW_REASON_CODES), len(set(contract.REVIEW_REASON_CODES)))
        self.assertEqual(len(contract.PROMOTION_REASON_CODES), len(set(contract.PROMOTION_REASON_CODES)))


if __name__ == "__main__":
    unittest.main()
