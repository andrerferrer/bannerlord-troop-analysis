#!/usr/bin/env python3
"""Audit historical scoring paths against the context-first methodology.

This command is intentionally read-only with respect to historical candidates,
model versions, theoretical exports, and their scoring scripts.  It publishes a
deterministic finding report plus the immutable byte-level baseline consumed by
later context-first slices.
"""

from __future__ import annotations

import argparse
import csv
import errno
import hashlib
import io
import os
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence


AUDIT_FIELDS = (
    "model_or_candidate",
    "source_path",
    "source_sha256",
    "context_declared",
    "question_declared",
    "attack_mode_declared",
    "mount_state_declared",
    "departure_code",
    "field_or_formula",
    "evidence",
)

BASELINE_FIELDS = ("path", "bytes", "sha256", "immutability_class")

AUDITED_SOURCES = (
    "analysis/model/v7_2_context_scoring/build_v72_context_scores.py",
    "scripts/scoring/generate_vanilla_role_scores.py",
    "scripts/scoring/run_theoretical_role_scores.py",
    "scripts/scoring/generate_defensive_role_scores_v2.py",
    "scripts/build_v72_burst_score.py",
    "scripts/build_v73_tooltip_damage_burst.py",
    "scripts/normalization/reconstruct_crafted_weapon_stats.py",
)

EXPECTED_V71_MODEL = (
    "analysis/model_versions/v7.1/"
    "bannerlord_v71_head_weighted_model_all_official_troops.csv"
)

EXPECTED_V72_MODEL = (
    "analysis/model_versions/v7.2_burst_score/"
    "bannerlord_v72_burst_model_all_official_troops.csv"
)

EXPECTED_ABSENT_V72_BURST_OUTPUTS = (
    EXPECTED_V72_MODEL,
    "analysis/model_versions/v7.2_burst_score/bannerlord_v72_top_burst_units_regular_combined.csv",
    "analysis/model_versions/v7.2_burst_score/bannerlord_v72_top40_burst_units_regular_combined.csv",
    "analysis/model_versions/v7.2_burst_score/vanilla_v72_top_burst_units_regular.csv",
    "analysis/model_versions/v7.2_burst_score/warsails_v72_top_burst_units_regular.csv",
)

EXPECTED_V73_MODEL = (
    "analysis/model_versions/v7.3_tooltip_damage_burst/"
    "bannerlord_v73_tooltip_damage_burst_model_all_official_troops.csv"
)

EXPECTED_ABSENT_V73_BURST_OUTPUTS = (
    EXPECTED_V73_MODEL,
    "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top_burst_units_regular_combined.csv",
    "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top40_burst_units_regular_combined.csv",
    "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top20_burst_units_regular_combined.csv",
    "analysis/model_versions/v7.3_tooltip_damage_burst/vanilla_v73_top_burst_units_regular.csv",
    "analysis/model_versions/v7.3_tooltip_damage_burst/warsails_v73_top_burst_units_regular.csv",
    "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_key_burst_cases.csv",
    "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_comparison_v72_vs_v73_burst_regular.csv",
)

EXPECTED_V721_TOOLTIP_MODEL = (
    "analysis/model_versions/v7.2.1_tooltip_throw_validation/"
    "bannerlord_v721_tooltip_throw_model_all_official_troops.csv"
)

EXPECTED_V72_CONTEXT_OUTPUTS = (
    "analysis/model/v7_2_context_scoring/bannerlord_v72_context_scores_all_official_troops.csv",
    "analysis/model/v7_2_context_scoring/bannerlord_v72_top40_burst_regular.csv",
    "analysis/model/v7_2_context_scoring/bannerlord_v72_top40_short_engagement_regular.csv",
    "analysis/model/v7_2_context_scoring/bannerlord_v72_top40_siege_defense_regular.csv",
    "analysis/model/v7_2_context_scoring/bannerlord_v72_top40_throwing_burst_regular.csv",
    "analysis/model/v7_2_context_scoring/empirical_v72_context_validation.csv",
)


class AuditError(RuntimeError):
    """Raised when an audited source or immutable baseline is unsafe."""


@dataclass(frozen=True)
class AuditFinding:
    model_or_candidate: str
    source_path: str
    source_sha256: str
    context_declared: str
    question_declared: str
    attack_mode_declared: str
    mount_state_declared: str
    departure_code: str
    field_or_formula: str
    evidence: str


@dataclass(frozen=True)
class BaselineRow:
    path: str
    bytes: int
    sha256: str
    immutability_class: str


@dataclass(frozen=True)
class FindingSpec:
    model_or_candidate: str
    source_path: str
    context_declared: bool
    question_declared: bool
    attack_mode_declared: bool
    mount_state_declared: bool
    departure_code: str
    field_or_formula: str
    evidence: str


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _truth(value: bool) -> str:
    return "true" if value else "false"


def _specs() -> tuple[FindingSpec, ...]:
    v1 = "scripts/scoring/generate_vanilla_role_scores.py"
    v2 = "scripts/scoring/generate_defensive_role_scores_v2.py"
    v72 = "scripts/build_v72_burst_score.py"
    v73 = "scripts/build_v73_tooltip_damage_burst.py"
    v72_context = "analysis/model/v7_2_context_scoring/build_v72_context_scores.py"
    findings = (
        FindingSpec("role_scores_v1", v1, False, False, False, False, "CONTEXT_UNDECLARED", "candidate declaration", "No track/battle-context declaration is validated before formulas run."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "ATTACK_MODE_UNDECLARED", "candidate declaration", "Melee, ranged, throwing, and defense paths are built together."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "MOUNT_STATE_UNDECLARED", "candidate declaration", "Roster horse presence changes formulas without a declared mount-state question."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "QUESTION_MIXED", "defensive_role_score", "Defense blends defense, crafted melee, throwing, shield, and horse inputs."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "QUESTION_MIXED", "ranged_role_score", "Ranged output blends offense, defense, mobility, horse, and shield inputs."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "QUESTION_MIXED", "offensive_melee_role_score", "Melee output also includes defense and mounted bonuses."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "QUESTION_MIXED", "skirmisher_role_score", "Throwing output also includes melee, defense, and mounted bonuses."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "defense_raw", "Shield HP/armor, harness armor, charge, horse speed, and maneuver enter defense."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "ranged_raw", "Ammunition thrust damage, weapon speed, accuracy, missile speed, and a capped stack bonus enter ranged output."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "skill and mobility factors", "Bow/Crossbow, melee, Throwing, Riding, and horse presence scale role outputs."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "TEMPLATE_PROXY_USED", "melee_proxy(crafting_template)", "Crafting-template names select fixed invented melee damage values."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "TEMPLATE_PROXY_USED", "melee_usability(crafting_template)", "Crafting-template names select a second invented melee usability multiplier."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "TEMPLATE_PROXY_USED", "throw_proxy_raw(crafting_template)", "Crafting-template names also select invented throwing damage before a fixed multiplier is applied."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "MISSING_VALUE_ZERO_FILLED", "numeric coercion", "Parsing uses errors=coerce followed by fillna(0) across score inputs."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "AMMUNITION_POLICY_UNDECLARED", "ranged_raw", "Finite stack count is used without a battle-context ammunition policy."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "AMMUNITION_POLICY_UNDECLARED", "direct_throw_raw", "Throwing stack amount enters output without a battle-context ammunition policy."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "direct_throw_raw", "Direct throwing blends swing/thrust damage with speed rating and stack amount."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "role eligibility and primary_category", "Shield, horse, and normalized defense fields decide whether and where troops rank."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "best item and roster aggregation", "Favorable item and roster outputs are selected with max instead of the context-first alternative-equipment mean."),
        FindingSpec("role_scores_v1", v1, False, False, False, False, "MOUNTED_INPUT_NON_APPLICABLE", "has_horse and mobility_factor", "Mounted bonuses can enter outputs that are not scoped away from siege defense."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "CONTEXT_UNDECLARED", "candidate declaration", "The candidate is defensive but does not select field, siege attack, or siege defense."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "ATTACK_MODE_UNDECLARED", "candidate declaration", "Melee counterpressure is read without a declared attack mode."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "MOUNT_STATE_UNDECLARED", "defensive_lane", "Mounted/unmounted lanes replace an explicit context and mount-state declaration."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "QUESTION_MIXED", "protection_score_v2 and defensive_utility_score_v2", "Protection and utility answer separate questions and utility blends mobility/melee skill."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "shield_hp_component_v2", "Shield endurance is treated as physical protection rather than a separate blocking question."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "shield_armor_component_v2", "Shield armor is included without an explicit shield-endurance question."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "harness_component_v2 and mount_health_component_v2", "Mounted durability enters a context-undeclared defense candidate."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "mobility_component_v2", "Horse speed/maneuver or Athletics enter defensive utility."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "counterpressure_component_v2", "Maximum melee skill enters defensive utility."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "MISSING_VALUE_ZERO_FILLED", "number(value, default=0.0)", "Missing/non-finite values are converted to a numeric default in historical feature helpers."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "MISSING_VALUE_ZERO_FILLED", "unresolved non-mount item evidence", "Unresolved armor, shield, or melee item evidence contributes zero while the roster remains scoreable."),
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "MOUNTED_INPUT_NON_APPLICABLE", "cavalry protection/utility lanes", "Mount and harness inputs cannot answer siege-defense defense after dismounting."),
        FindingSpec("v7.1", EXPECTED_V71_MODEL, False, False, False, False, "SOURCE_ARTIFACT_ABSENT", "general model CSV", "The repository references this v7.1 input, but its bytes are not present in the checkout."),
        FindingSpec("v7.2", EXPECTED_V72_MODEL, False, False, False, False, "SOURCE_ARTIFACT_ABSENT", "full burst model CSV", "The v7.2 builder publishes this full model output, but its bytes are not present in the checkout."),
        FindingSpec("v7.3", EXPECTED_V721_TOOLTIP_MODEL, False, False, False, False, "SOURCE_ARTIFACT_ABSENT", "v7.2.1 tooltip-throw input model CSV", "The v7.3 builder declares this model CSV as its required input, but its bytes are not present in the checkout."),
        FindingSpec("v7.3", EXPECTED_V73_MODEL, False, False, False, False, "SOURCE_ARTIFACT_ABSENT", "full tooltip-damage burst model CSV", "The v7.3 builder publishes this full model output, but its bytes are not present in the checkout."),
        FindingSpec("v7.2", v72, False, False, False, False, "CONTEXT_UNDECLARED", "burst_score_v72", "The burst label does not declare track and battle context as a validated tuple."),
        FindingSpec("v7.2", v72, False, False, False, False, "ATTACK_MODE_UNDECLARED", "burst_raw=max(throw,ranged,charge,melee)", "Four attack families compete inside one output."),
        FindingSpec("v7.2", v72, False, False, False, False, "MOUNT_STATE_UNDECLARED", "mounted_throw_bonus", "Mounted state is inferred from input rather than declared before scoring."),
        FindingSpec("v7.2", v72, False, False, False, False, "QUESTION_MIXED", "burst_score_v72", "Burst offense is blended with reliability and v7.1 defense."),
        FindingSpec("v7.2", v72, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "reliability_score and defense_score_v71", "Non-offensive composite drivers enter the burst score."),
        FindingSpec("v7.2", v72, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "throw_pressure_v7/ranged_kpm_v7/charge_impact_score_v7/melee_kpm_eff_v7", "Opaque throwing, ranged, charge, and melee composite inputs drive the four burst families."),
        FindingSpec("v7.2", v72, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "primary_throw_damage_type/category/has_crossbow", "Damage type and troop/category labels apply secondary type multipliers."),
        FindingSpec("v7.2", v72, False, False, False, False, "MISSING_VALUE_ZERO_FILLED", "burst inputs", "Missing damage/ammunition/reliability/defense values are filled with zero."),
        FindingSpec("v7.2", v72, False, False, False, False, "AMMUNITION_POLICY_UNDECLARED", "throw_ammo_factor and ranged_ammo_factor", "Finite ammunition factors are applied without a field/siege policy."),
        FindingSpec("v7.2", v72, False, False, False, False, "MOUNTED_INPUT_NON_APPLICABLE", "mounted_throw_bonus", "The mounted bonus has no siege-defense dismount boundary."),
        FindingSpec("v7.3", v73, False, False, False, False, "CONTEXT_UNDECLARED", "burst_score_v73", "The burst label does not declare track and battle context as a validated tuple."),
        FindingSpec("v7.3", v73, False, False, False, False, "ATTACK_MODE_UNDECLARED", "burst_source_v73", "Throw, ranged, charge, and melee sources compete inside one output."),
        FindingSpec("v7.3", v73, False, False, False, False, "MOUNT_STATE_UNDECLARED", "mounted_throw_bonus_v73", "Mounted state is inferred rather than declared before scoring."),
        FindingSpec("v7.3", v73, False, False, False, False, "QUESTION_MIXED", "burst_score_v73", "Burst offense is blended with reliability and v7.1 defense."),
        FindingSpec("v7.3", v73, False, False, False, False, "TEMPLATE_PROXY_USED", "throw_damage_source_v73=model_proxy", "Missing tooltip damage falls back to primary model proxy damage."),
        FindingSpec("v7.3", v73, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "throw_skill_factor_v73", "Throwing skill scales output without a declared secondary-driver candidate."),
        FindingSpec("v7.3", v73, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "throw_damage_type_factor_v73", "Damage type applies a secondary multiplier outside the base context-first attack candidate."),
        FindingSpec("v7.3", v73, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "ranged_burst_raw_v72/charge_burst_raw_v72/melee_burst_raw_v72", "Opaque v7.2 composite families are carried into v7.3."),
        FindingSpec("v7.3", v73, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "reliability_score and defense_score_v71", "Reliability and defense composites enter the final burst score."),
        FindingSpec("v7.3", v73, False, False, False, False, "MISSING_VALUE_ZERO_FILLED", "burst inputs", "Missing damage/ammunition/reliability/defense values are filled with zero."),
        FindingSpec("v7.3", v73, False, False, False, False, "AMMUNITION_POLICY_UNDECLARED", "throw_ammo_factor_v73", "Finite ammunition is used without a field/siege policy."),
        FindingSpec("v7.3", v73, False, False, False, False, "MOUNTED_INPUT_NON_APPLICABLE", "mounted_throw_bonus_v73", "The mounted bonus has no siege-defense dismount boundary."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "CONTEXT_UNDECLARED", "context score declaration", "One input produces burst, short-engagement, and siege-defense outputs without a validated track/context tuple."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "ATTACK_MODE_UNDECLARED", "burst_core=max(throw,ranged,melee,charge)", "Throwing, ranged, melee, and charge families compete inside one burst output."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "MOUNT_STATE_UNDECLARED", "throw_mounted_bonus and charge", "Mounted state is inferred from source columns instead of declared before scoring."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "QUESTION_MIXED", "general_score_v72", "A pre-existing total composite is carried forward as a general answer."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "QUESTION_MIXED", "burst_score_v72", "Burst attack is blended with reliability and v7.1 defense."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "QUESTION_MIXED", "short_engagement_score_v72", "Burst, offense, reliability, and defense are blended into one answer."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "QUESTION_MIXED", "siege_defense_score_v72", "Ranged/throwing offense, defense, reliability, ammunition, and a formation floor are blended for siege defense."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "throw_burst", "Throwing composites, three ammunition proxies, damage, damage type, skill, and mounted state enter output."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "ranged_burst", "Ranged KPM, damage, ammo, expected capacity, class bonuses, and reliability enter output."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "melee_shock", "Melee KPM, damage, reach, class, shield state, and damage type enter output."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "IRRELEVANT_DRIVER_INCLUDED", "formation_floor and composite carryover", "Category plus offense, defense, reliability, and v7.1 total composites affect context outputs."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "MISSING_VALUE_ZERO_FILLED", "num(series, default=0.0)", "Missing and non-numeric inputs are coerced and filled with zero throughout the builder."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "AMMUNITION_POLICY_UNDECLARED", "throw_ammo/ranged_ammo/ranged_siege", "Finite ammunition and capacity affect burst and siege-defense output without an explicit context policy."),
        FindingSpec("v7.2_context_scores", v72_context, False, False, False, False, "MOUNTED_INPUT_NON_APPLICABLE", "throw_mounted_bonus and charge", "Mounted bonuses can enter outputs without a siege-defense dismount boundary."),
    )
    absent_outputs = tuple(
        FindingSpec(
            "v7.2_context_scores",
            path,
            False,
            False,
            False,
            False,
            "SOURCE_ARTIFACT_ABSENT",
            Path(path).name,
            "The context-score builder declares this output filename, but no repository-addressable artifact is present in the checkout.",
        )
        for path in EXPECTED_V72_CONTEXT_OUTPUTS
    )
    historical_builder_outputs = tuple(
        FindingSpec(
            model,
            path,
            False,
            False,
            False,
            False,
            "SOURCE_ARTIFACT_ABSENT",
            Path(path).name,
            f"The {model} builder declares this output filename, but no repository-addressable artifact is present in the checkout.",
        )
        for model, paths in (
            ("v7.2", EXPECTED_ABSENT_V72_BURST_OUTPUTS[1:]),
            ("v7.3", EXPECTED_ABSENT_V73_BURST_OUTPUTS[1:]),
        )
        for path in paths
    )
    return findings + absent_outputs + historical_builder_outputs


def build_findings(repo: Path) -> tuple[AuditFinding, ...]:
    repo = repo.resolve()
    findings: list[AuditFinding] = []
    for spec in _specs():
        source = repo / spec.source_path
        absent = spec.departure_code == "SOURCE_ARTIFACT_ABSENT"
        if absent:
            if source.exists():
                raise AuditError(
                    f"expected absent source is now present; update the reviewed audit spec: {spec.source_path}"
                )
            source_hash = ""
        else:
            if not source.is_file():
                raise AuditError(f"audited source missing: {spec.source_path}")
            source_hash = _sha256_file(source)
        findings.append(
            AuditFinding(
                model_or_candidate=spec.model_or_candidate,
                source_path=spec.source_path,
                source_sha256=source_hash,
                context_declared=_truth(spec.context_declared),
                question_declared=_truth(spec.question_declared),
                attack_mode_declared=_truth(spec.attack_mode_declared),
                mount_state_declared=_truth(spec.mount_state_declared),
                departure_code=spec.departure_code,
                field_or_formula=spec.field_or_formula,
                evidence=spec.evidence,
            )
        )
    return tuple(
        sorted(
            findings,
            key=lambda row: (
                row.model_or_candidate,
                row.departure_code,
                row.field_or_formula,
                row.source_path,
            ),
        )
    )


def _tracked_files(repo: Path) -> tuple[str, ...]:
    result = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise AuditError(f"cannot enumerate repository-addressable files: {detail}")
    try:
        paths = tuple(
            item.decode("utf-8")
            for item in result.stdout.split(b"\0")
            if item
        )
    except UnicodeDecodeError as error:
        raise AuditError("tracked path is not valid UTF-8") from error
    if not paths:
        raise AuditError("repository has no tracked files")
    return paths


def _historical_output(relative: str) -> bool:
    parts = relative.split("/")
    return (
        len(parts) > 4
        and parts[:2] == ["analysis", "theoretical"]
        and parts[3] == "export_20260731_150800"
    )


def _lstat_repository_path(
    repo: Path,
    path: Path,
    *,
    leaf_label: str = "path",
) -> os.stat_result | None:
    try:
        relative = path.relative_to(repo)
    except ValueError as error:
        raise AuditError(f"protected path is outside repository: {path}") from error
    if not relative.parts:
        raise AuditError(f"protected path is the repository root: {repo}")

    current = repo
    for part in relative.parts:
        current /= part
        try:
            status = os.lstat(current)
        except FileNotFoundError:
            return None
        except OSError as error:
            raise AuditError(
                f"cannot scan protected path: {current}: {error}"
            ) from error
        current_relative = current.relative_to(repo).as_posix()
        if stat.S_ISLNK(status.st_mode):
            label = f"protected {leaf_label}" if current == path else "protected ancestor"
            raise AuditError(f"{label} is a symlink: {current_relative}")
        if current != path and not stat.S_ISDIR(status.st_mode):
            raise AuditError(
                f"protected ancestor is not a directory: {current_relative}"
            )
    return status


def _read_repository_file(repo: Path, path: Path) -> bytes:
    """Read a regular repository file without following symlink components."""
    try:
        relative = path.relative_to(repo)
    except ValueError as error:
        raise AuditError(f"protected path is outside repository: {path}") from error
    repo = repo.resolve()
    path = repo / relative
    if not relative.parts:
        raise AuditError(f"protected path is the repository root: {repo}")

    initial = _lstat_repository_path(repo, path, leaf_label="file")
    if initial is None:
        raise AuditError(
            f"protected file disappeared before reading: {relative.as_posix()}"
        )
    if not stat.S_ISREG(initial.st_mode):
        raise AuditError(f"protected path is not a regular file: {relative.as_posix()}")

    directory_flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0)
    file_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
        file_flags |= os.O_NOFOLLOW

    descriptors: list[int] = []
    try:
        directory_fd = os.open(repo, directory_flags)
        descriptors.append(directory_fd)
        for component in relative.parts[:-1]:
            directory_fd = os.open(
                component,
                directory_flags,
                dir_fd=directory_fd,
            )
            descriptors.append(directory_fd)
        file_fd = os.open(relative.parts[-1], file_flags, dir_fd=directory_fd)
        descriptors.append(file_fd)

        before = os.fstat(file_fd)
        if not stat.S_ISREG(before.st_mode):
            raise AuditError(
                f"protected path is not a regular file: {relative.as_posix()}"
            )
        chunks: list[bytes] = []
        while True:
            try:
                chunk = os.read(file_fd, 1024 * 1024)
            except InterruptedError:
                continue
            if not chunk:
                break
            chunks.append(chunk)
        content = b"".join(chunks)
        after = os.fstat(file_fd)
        identity = lambda value: (
            value.st_dev,
            value.st_ino,
            value.st_mode,
            value.st_size,
            value.st_mtime_ns,
            value.st_ctime_ns,
        )
        if identity(before) != identity(after) or len(content) != after.st_size:
            raise AuditError(
                f"protected file changed while reading: {relative.as_posix()}"
            )
        current = _lstat_repository_path(repo, path, leaf_label="file")
        if current is None or identity(current) != identity(after):
            raise AuditError(
                f"protected file changed while reading: {relative.as_posix()}"
            )
        return content
    except AuditError:
        raise
    except OSError as error:
        raise AuditError(
            f"cannot read protected file: {relative.as_posix()}: {error}"
        ) from error
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _protected_paths(repo: Path) -> Iterable[tuple[Path, str]]:
    v1_candidate_prefix = "data/vanilla/role_scores/"
    candidate_prefix = "analysis/model_candidates/role_scores_v2_defense/"
    model_prefix = "analysis/model_versions/"
    audited = set(AUDITED_SOURCES)
    observed_classes: set[str] = set()
    observed_sources: set[str] = set()

    for relative in _tracked_files(repo):
        classification = ""
        if relative.startswith(v1_candidate_prefix):
            classification = "historical_candidate"
        elif relative.startswith(candidate_prefix):
            classification = "historical_candidate"
        elif relative.startswith(model_prefix):
            classification = "frozen_model"
        elif _historical_output(relative):
            classification = "historical_output"
        elif relative in audited:
            classification = "audited_source"
            observed_sources.add(relative)
        if not classification:
            continue

        path = repo / relative
        status = _lstat_repository_path(repo, path)
        if status is None or not stat.S_ISREG(status.st_mode):
            raise AuditError(f"tracked protected file missing: {relative}")
        observed_classes.add(classification)
        yield path, classification

    required_classes = {
        "historical_candidate",
        "frozen_model",
        "historical_output",
        "audited_source",
    }
    if observed_classes != required_classes:
        missing = ",".join(sorted(required_classes - observed_classes))
        raise AuditError(f"protected classes have no tracked files: {missing}")
    if observed_sources != audited:
        missing = ",".join(sorted(audited - observed_sources))
        raise AuditError(f"audited source is not tracked: {missing}")


def build_historical_baseline(repo: Path) -> tuple[BaselineRow, ...]:
    repo = repo.resolve()
    rows: dict[str, BaselineRow] = {}
    for path, classification in _protected_paths(repo):
        relative = path.relative_to(repo).as_posix()
        if relative in rows:
            raise AuditError(f"protected path classified twice: {relative}")
        content = _read_repository_file(repo, path)
        rows[relative] = BaselineRow(
            path=relative,
            bytes=len(content),
            sha256=_sha256_bytes(content),
            immutability_class=classification,
        )
    return tuple(rows[path] for path in sorted(rows))


def _scan_tree_fail_closed(repo: Path, root: Path) -> tuple[Path, ...]:
    root_status = _lstat_repository_path(repo, root, leaf_label="root")
    if root_status is None:
        return ()
    if not stat.S_ISDIR(root_status.st_mode):
        raise AuditError(
            f"protected root is not a directory: {root.relative_to(repo).as_posix()}"
        )

    def scan_failed(error: OSError) -> None:
        location = error.filename or str(root)
        raise AuditError(f"cannot scan protected path: {location}: {error}") from error

    observed: list[Path] = []
    for current, directory_names, file_names in os.walk(
        root,
        topdown=True,
        onerror=scan_failed,
        followlinks=False,
    ):
        current_path = Path(current)
        directory_names.sort()
        file_names.sort()
        for name in (*directory_names, *file_names):
            candidate = current_path / name
            relative = candidate.relative_to(repo).as_posix()
            if _lstat_repository_path(repo, candidate) is None:
                raise AuditError(f"protected path disappeared while scanning: {relative}")
            observed.append(candidate)
    return tuple(sorted(observed, key=lambda path: path.as_posix()))


def _build_working_tree_snapshot(repo: Path) -> tuple[BaselineRow, ...]:
    rows = {row.path: row for row in build_historical_baseline(repo)}
    roots: dict[Path, str] = {
        repo / "data/vanilla/role_scores": "historical_candidate",
        repo / "analysis/model_candidates/role_scores_v2_defense": "historical_candidate",
        repo / "analysis/model/v7_2_context_scoring": "historical_output",
        repo / "analysis/model_versions": "frozen_model",
    }
    for relative in _tracked_files(repo):
        if _historical_output(relative):
            parts = relative.split("/")
            roots[repo / "/".join(parts[:4])] = "historical_output"
    theoretical_root = repo / "analysis/theoretical"
    for candidate in _scan_tree_fail_closed(repo, theoretical_root):
        if candidate.name == "export_20260731_150800":
            status = _lstat_repository_path(repo, candidate)
            if status is None or not stat.S_ISDIR(status.st_mode):
                raise AuditError(
                    "reserved historical export path is not a directory: "
                    f"{candidate.relative_to(repo).as_posix()}"
                )
            roots[candidate] = "historical_output"

    for root, classification in sorted(
        roots.items(), key=lambda item: item[0].as_posix()
    ):
        for path in _scan_tree_fail_closed(repo, root):
            relative = path.relative_to(repo).as_posix()
            status = _lstat_repository_path(repo, path)
            if status is None:
                raise AuditError(f"protected path disappeared while scanning: {relative}")
            if stat.S_ISDIR(status.st_mode) or relative in rows:
                continue
            if not stat.S_ISREG(status.st_mode):
                raise AuditError(f"protected path is not a regular file: {relative}")
            content = _read_repository_file(repo, path)
            rows[relative] = BaselineRow(
                path=relative,
                bytes=len(content),
                sha256=_sha256_bytes(content),
                immutability_class=classification,
            )
    return tuple(rows[path] for path in sorted(rows))


def build_working_tree_baseline(repo: Path) -> tuple[BaselineRow, ...]:
    """Include untracked files and require two equal protected-tree snapshots."""
    repo = repo.resolve()
    first = _build_working_tree_snapshot(repo)
    second = _build_working_tree_snapshot(repo)
    if second != first:
        raise AuditError("protected tree changed during working-tree scan")
    return first


def _baseline_bytes(rows: Sequence[BaselineRow]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=BASELINE_FIELDS, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                "path": row.path,
                "bytes": row.bytes,
                "sha256": row.sha256,
                "immutability_class": row.immutability_class,
            }
        )
    return stream.getvalue().encode("utf-8")


def verify_historical_baseline(
    repo: Path,
    baseline_path: Path,
    *,
    allowed_new_version: str | None = None,
) -> tuple[BaselineRow, ...]:
    repo = repo.resolve()
    baseline_path = (
        baseline_path
        if baseline_path.is_absolute()
        else repo / baseline_path
    ).resolve()
    if not baseline_path.is_file():
        raise AuditError(f"historical baseline missing: {baseline_path}")
    _, committed_rows = _read_canonical_baseline(baseline_path)
    current_rows = build_working_tree_baseline(repo)
    committed = {row.path: row for row in committed_rows}
    current = {row.path: row for row in current_rows}

    for path, expected in committed.items():
        observed = current.get(path)
        if observed != expected:
            raise AuditError(
                f"existing historical baseline differs from current protected bytes: {path}"
            )

    extras = sorted(set(current) - set(committed))
    allowed_prefix = _allowed_version_prefix(allowed_new_version)
    reserved_namespaces = {
        Path(spec.source_path).parts[2]
        for spec in _specs()
        if spec.departure_code == "SOURCE_ARTIFACT_ABSENT"
        and spec.source_path.startswith("analysis/model_versions/")
    }
    if allowed_new_version in reserved_namespaces:
        raise AuditError(
            f"allowed new model version is a reserved historical namespace: {allowed_new_version}"
        )
    if allowed_prefix is not None and any(
        path.startswith(allowed_prefix) for path in committed
    ):
        raise AuditError(
            f"allowed new model version already exists in historical baseline: {allowed_new_version}"
        )
    forbidden = [
        path
        for path in extras
        if allowed_prefix is None or not path.startswith(allowed_prefix)
    ]
    if forbidden:
        raise AuditError(f"unexpected protected path: {forbidden[0]}")
    return current_rows


def _parse_baseline(content: bytes) -> tuple[BaselineRow, ...]:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AuditError("historical baseline is not valid UTF-8") from error
    rows: list[BaselineRow] = []
    try:
        reader = csv.DictReader(io.StringIO(text, newline=""))
        if reader.fieldnames != list(BASELINE_FIELDS):
            raise AuditError("historical baseline has an invalid header")
        for value in reader:
            rows.append(
                BaselineRow(
                    path=value["path"],
                    bytes=int(value["bytes"]),
                    sha256=value["sha256"],
                    immutability_class=value["immutability_class"],
                )
            )
    except (KeyError, TypeError, ValueError, csv.Error) as error:
        raise AuditError("historical baseline has an invalid row") from error
    paths = [row.path for row in rows]
    if not rows or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise AuditError("historical baseline paths must be non-empty, unique, and sorted")
    return tuple(rows)


def _read_canonical_baseline(path: Path) -> tuple[bytes, tuple[BaselineRow, ...]]:
    content = path.read_bytes()
    rows = _parse_baseline(content)
    if content != _baseline_bytes(rows):
        raise AuditError("historical baseline is not in canonical CSV form")
    return content, rows


def _allowed_version_prefix(version: str | None) -> str | None:
    if version is None:
        return None
    if not version or Path(version).name != version or version in {".", ".."}:
        raise AuditError("allowed new model version must be one directory name")
    return f"analysis/model_versions/{version}/"


def _audit_csv(findings: Sequence[AuditFinding]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=AUDIT_FIELDS, lineterminator="\n")
    writer.writeheader()
    for finding in findings:
        writer.writerow({field: getattr(finding, field) for field in AUDIT_FIELDS})
    return stream.getvalue()


def _report_bytes(
    findings: Sequence[AuditFinding], baseline_rows: Sequence[BaselineRow], baseline: bytes
) -> bytes:
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.departure_code] = counts.get(finding.departure_code, 0) + 1
    lines = [
        "# Current candidate audit — context-first scoring",
        "",
        "Status: **historical audit only; non-canonical**",
        "",
        "No rankings are published by this audit. Historical candidates, theoretical exports,",
        "scoring sources, and frozen model versions are read and hashed but never modified.",
        "",
        "## Scope",
        "",
        f"- Findings: {len(findings)}",
        f"- Protected files: {len(baseline_rows)}",
        f"- Baseline manifest SHA-256: `{_sha256_bytes(baseline)}`",
        f"- Explicit absent artifacts: {sum(row.departure_code == 'SOURCE_ARTIFACT_ABSENT' for row in findings)}",
        "",
        "## Departure counts",
        "",
        "| Departure code | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| `{code}` | {counts[code]} |" for code in sorted(counts))
    lines.extend(
        [
            "",
            "## Finding inventory",
            "",
            "The CSV-shaped table below is the complete reviewed inventory. `false` declaration",
            "fields mean the historical path did not validate that dimension before reading evidence.",
            "",
            "```csv",
            _audit_csv(findings).rstrip("\n"),
            "```",
            "",
            "## Interpretation boundary",
            "",
            "These findings explain why the historical paths are not defaults for new scoring.",
            "They do not invalidate historical reproduction, change any old rank, or establish a",
            "replacement ranking. Later context-first slices must verify",
            "`historical_baseline_hashes.csv` before publishing candidate output.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def verify_committed_report(
    repo: Path,
    report_path: Path,
    baseline_path: Path,
    *,
    allowed_new_version: str | None = None,
) -> None:
    repo = repo.resolve()
    report_path = report_path if report_path.is_absolute() else repo / report_path
    baseline_path = baseline_path if baseline_path.is_absolute() else repo / baseline_path
    if not report_path.is_file():
        raise AuditError(f"audit report missing: {report_path}")
    baseline, baseline_rows = _read_canonical_baseline(baseline_path)
    verify_historical_baseline(
        repo,
        baseline_path,
        allowed_new_version=allowed_new_version,
    )
    expected = _report_bytes(build_findings(repo), baseline_rows, baseline)
    if report_path.read_bytes() != expected:
        raise AuditError("committed audit report differs from deterministic output")


def _file_identity(status: os.stat_result) -> tuple[int, int]:
    return status.st_dev, status.st_ino


def _file_validation_state(status: os.stat_result) -> tuple[int, ...]:
    return (
        status.st_dev,
        status.st_ino,
        status.st_mode,
        status.st_size,
        status.st_mtime_ns,
        status.st_ctime_ns,
    )


def _close_descriptor_resilient(descriptor: int) -> tuple[BaseException, ...]:
    try:
        os.close(descriptor)
    except OSError as error:
        if error.errno == errno.EBADF:
            return ()
        return (error,)
    except BaseException as error:
        return (error,)
    return ()


def _read_identity_bytes(path: Path, identity: tuple[int, int]) -> bytes:
    descriptor: int | None = None
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NONBLOCK", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(path, flags)
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or _file_identity(before) != identity:
            raise AuditError(f"audit output identity changed: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        content = b"".join(chunks)
        after = os.fstat(descriptor)
        if _file_validation_state(before) != _file_validation_state(after):
            raise AuditError(f"audit output changed while validating: {path}")
        return content
    except AuditError:
        raise
    except BaseException as error:
        raise AuditError(
            f"cannot validate audit output bytes: {path}: "
            f"{type(error).__name__}: {error}"
        ) from error
    finally:
        if descriptor is not None:
            _close_descriptor_resilient(descriptor)


def _validate_staged_source(
    temporary: Path,
    identity: tuple[int, int],
    expected_sha256: str,
    expected_bytes: int,
) -> None:
    content = _read_identity_bytes(temporary, identity)
    if len(content) != expected_bytes or _sha256_bytes(content) != expected_sha256:
        raise AuditError(f"staged audit output content changed: {temporary}")


def _replacement_state(
    temporary: Path,
    path: Path,
    identity: tuple[int, int],
    expected_sha256: str,
    expected_bytes: int,
    *,
    replacement_attempted: bool,
    replacement_returned: bool,
) -> tuple[bool, bool, tuple[AuditError, ...]]:
    errors: list[AuditError] = []
    source_absent = False
    source_matches = False
    try:
        source = os.lstat(temporary)
    except FileNotFoundError:
        source_absent = True
    except BaseException as error:
        errors.append(
            AuditError(
                f"cannot inspect staged audit output: {temporary}: "
                f"{type(error).__name__}: {error}"
            )
        )
    else:
        source_matches = _file_identity(source) == identity
        if not source_matches:
            errors.append(AuditError(f"staged audit output identity changed: {temporary}"))
        else:
            try:
                _validate_staged_source(
                    temporary, identity, expected_sha256, expected_bytes
                )
            except AuditError as error:
                errors.append(error)

    destination_matches = False
    try:
        destination = os.lstat(path)
    except BaseException as error:
        if source_absent:
            errors.append(
                AuditError(
                    f"cannot inspect consumed audit destination: {path}: "
                    f"{type(error).__name__}: {error}"
                )
            )
    else:
        destination_matches = _file_identity(destination) == identity

    rollback_owned = replacement_attempted and (
        replacement_returned or destination_matches
    )
    source_consumed = source_absent
    if destination_matches and not source_absent:
        errors.append(
            AuditError(
                f"staged source still exists beside audit destination: {temporary}"
            )
        )
    if rollback_owned and not destination_matches:
        errors.append(AuditError(f"published audit output identity differs: {path}"))
    if rollback_owned and destination_matches:
        try:
            published = _read_identity_bytes(path, identity)
        except AuditError as error:
            errors.append(error)
        else:
            if (
                len(published) != expected_bytes
                or _sha256_bytes(published) != expected_sha256
            ):
                errors.append(AuditError(f"published audit output content differs: {path}"))
    if source_absent and not replacement_attempted:
        errors.append(
            AuditError(f"staged audit output disappeared before replacement: {temporary}")
        )
    if not rollback_owned and not source_matches and not errors:
        errors.append(AuditError(f"audit replacement state is unknown: {path}"))
    return rollback_owned, source_consumed, tuple(errors)


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary: Path | None = Path(temporary_name)
    descriptor_open = True
    identity: tuple[int, int] | None = None
    expected_sha256 = _sha256_bytes(content)
    try:
        identity = _file_identity(os.fstat(descriptor))
        handle = os.fdopen(descriptor, "wb")
        descriptor_open = False
        with handle:
            handle.write(content)
        _validate_staged_source(
            temporary, identity, expected_sha256, len(content)
        )
        replacement_returned = False
        try:
            os.replace(temporary, path)
        except BaseException as error:
            committed, source_consumed, state_errors = _replacement_state(
                temporary,
                path,
                identity,
                expected_sha256,
                len(content),
                replacement_attempted=True,
                replacement_returned=False,
            )
            if source_consumed:
                temporary = None
            if committed and not state_errors:
                return
            if state_errors:
                detail = "; ".join(str(item) for item in state_errors)
                raise AuditError(f"atomic replacement state invalid: {detail}") from error
            raise
        replacement_returned = True
        committed, source_consumed, state_errors = _replacement_state(
            temporary,
            path,
            identity,
            expected_sha256,
            len(content),
            replacement_attempted=True,
            replacement_returned=replacement_returned,
        )
        if source_consumed:
            temporary = None
        if not committed or state_errors:
            detail = "; ".join(str(item) for item in state_errors)
            raise AuditError(f"atomic replacement state invalid: {detail}")
    finally:
        if descriptor_open:
            _close_descriptor_resilient(descriptor)
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _publish_transaction(
    outputs: Sequence[tuple[Path, bytes]], integrity_check: Callable[[], None]
) -> None:
    snapshots: dict[Path, tuple[bool, bytes]] = {}
    staged: list[tuple[Path, Path, tuple[int, int], str, int]] = []
    pending_temporaries: set[Path] = set()
    swapped: list[Path] = []
    attempted: set[Path] = set()
    completed: set[Path] = set()

    def reconcile_consumed_temporaries() -> tuple[AuditError, ...]:
        reconciliation_errors: list[AuditError] = []
        for path, temporary, identity, expected_sha256, expected_bytes in staged:
            if path in swapped:
                continue
            rollback_owned, source_consumed, state_errors = _replacement_state(
                temporary,
                path,
                identity,
                expected_sha256,
                expected_bytes,
                replacement_attempted=path in attempted,
                replacement_returned=path in completed,
            )
            if source_consumed:
                pending_temporaries.discard(temporary)
            if rollback_owned:
                swapped.append(path)
            reconciliation_errors.extend(state_errors)
        return tuple(reconciliation_errors)

    try:
        for path, _ in outputs:
            existed = path.exists()
            snapshots[path] = (existed, path.read_bytes() if existed else b"")
        for path, content in outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
            )
            temporary = Path(temporary_name)
            pending_temporaries.add(temporary)
            descriptor_open = True
            try:
                temporary_status = os.fstat(descriptor)
                handle = os.fdopen(descriptor, "wb")
                descriptor_open = False
                with handle:
                    handle.write(content)
            finally:
                if descriptor_open:
                    _close_descriptor_resilient(descriptor)
            staged.append(
                (
                    path,
                    temporary,
                    _file_identity(temporary_status),
                    _sha256_bytes(content),
                    len(content),
                )
            )

        integrity_check()
        for path, temporary, identity, expected_sha256, expected_bytes in staged:
            _validate_staged_source(
                temporary, identity, expected_sha256, expected_bytes
            )
            attempted.add(path)
            os.replace(temporary, path)
            completed.add(path)
            state_errors = reconcile_consumed_temporaries()
            if state_errors:
                raise state_errors[0]
        integrity_check()
    except BaseException as error:
        reconciliation_errors = reconcile_consumed_temporaries()
        rollback_errors: list[BaseException] = []
        for path in reversed(swapped):
            existed, content = snapshots[path]
            try:
                if existed:
                    _atomic_write(path, content)
                else:
                    try:
                        path.unlink(missing_ok=True)
                    except NotADirectoryError:
                        pass
            except BaseException as rollback_error:
                rollback_errors.append(rollback_error)
        if reconciliation_errors and hasattr(error, "add_note"):
            detail = "; ".join(str(item) for item in reconciliation_errors)
            error.add_note(f"audit replacement reconciliation: {detail}")
        if rollback_errors:
            detail = "; ".join(
                f"{type(item).__name__}: {item}" for item in rollback_errors
            )
            raise AuditError(
                f"publication failed ({type(error).__name__}: {error}); "
                f"rollback also failed: {detail}"
            ) from error
        if isinstance(error, OSError):
            raise AuditError(f"publication filesystem failure: {error}") from error
        raise
    finally:
        primary_exception = sys.exc_info()[1]
        remaining = sorted(pending_temporaries)
        cleanup_errors: list[BaseException] = []
        for _ in range(2):
            retry: list[Path] = []
            cleanup_errors = []
            for temporary in remaining:
                try:
                    temporary.unlink(missing_ok=True)
                except BaseException as error:
                    retry.append(temporary)
                    cleanup_errors.append(error)
            remaining = retry
            if not remaining:
                break
        if cleanup_errors:
            detail = "; ".join(
                f"{type(item).__name__}: {item}" for item in cleanup_errors
            )
            if primary_exception is not None and hasattr(primary_exception, "add_note"):
                primary_exception.add_note(f"staged audit cleanup failed: {detail}")
            else:
                raise AuditError(
                    f"cannot remove staged audit output: {detail}"
                ) from cleanup_errors[0]


def _validate_output_paths(
    repo: Path, report_output: Path, baseline_output: Path
) -> tuple[Path, Path]:
    report = report_output.resolve()
    baseline = baseline_output.resolve()
    if report == baseline:
        raise AuditError("report and baseline outputs must be distinct")

    protected_roots = {
        (repo / "analysis/model_candidates/role_scores_v2_defense").resolve(),
        (repo / "analysis/model/v7_2_context_scoring").resolve(),
        (repo / "analysis/model_versions").resolve(),
    }
    for relative in _tracked_files(repo):
        if _historical_output(relative):
            parts = relative.split("/")
            protected_roots.add((repo / "/".join(parts[:4])).resolve())
    protected_sources = {(repo / relative).resolve() for relative in AUDITED_SOURCES}
    owned_outputs = {
        "report": (
            repo
            / "analysis/model_candidates/context_first_scores_v1/"
            "CURRENT_CANDIDATE_AUDIT.md"
        ).resolve(),
        "baseline": (
            repo
            / "analysis/model_candidates/context_first_scores_v1/"
            "historical_baseline_hashes.csv"
        ).resolve(),
    }

    for label, target in (("report", report), ("baseline", baseline)):
        if target in protected_sources or any(
            target == root or target.is_relative_to(root)
            for root in protected_roots
        ):
            raise AuditError(f"{label} is a protected output destination: {target}")
        if target.is_relative_to(repo) and target != owned_outputs[label]:
            raise AuditError(f"{label} is not a D1-owned output: {target}")
        if target.exists() and not target.is_file():
            raise AuditError(f"{label} output is not a regular file: {target}")
        ancestor = target.parent
        while not ancestor.exists() and ancestor != ancestor.parent:
            ancestor = ancestor.parent
        if not ancestor.is_dir():
            raise AuditError(
                f"{label} output parent is not a directory: {ancestor}"
            )
    return report, baseline


def write_audit(
    repo: Path,
    report_output: Path,
    baseline_output: Path,
    *,
    initialize_baseline: bool = False,
    allowed_new_version: str | None = None,
) -> tuple[tuple[AuditFinding, ...], tuple[BaselineRow, ...]]:
    repo = repo.resolve()
    report_output, baseline_output = _validate_output_paths(
        repo, report_output, baseline_output
    )
    findings = build_findings(repo)
    if initialize_baseline:
        if allowed_new_version is not None:
            raise AuditError("baseline initialization cannot allow a new model version")
        if baseline_output.exists():
            raise AuditError("historical baseline already exists; refusing initialization")
        baseline_rows = build_historical_baseline(repo)
        current_rows = build_working_tree_baseline(repo)
        if current_rows != baseline_rows:
            extra = sorted(
                {row.path for row in current_rows}
                - {row.path for row in baseline_rows}
            )
            if extra:
                raise AuditError(f"unexpected protected path: {extra[0]}")
            raise AuditError("protected bytes changed during baseline initialization")
        baseline = _baseline_bytes(baseline_rows)
    else:
        if not baseline_output.is_file():
            raise AuditError("historical baseline missing; use --initialize-baseline once")
        baseline, baseline_rows = _read_canonical_baseline(baseline_output)
        current_rows = verify_historical_baseline(
            repo,
            baseline_output,
            allowed_new_version=allowed_new_version,
        )
    report = _report_bytes(findings, baseline_rows, baseline)

    def history_is_unchanged() -> None:
        if build_findings(repo) != findings:
            raise AuditError("audited evidence changed while publishing the audit")
        if build_working_tree_baseline(repo) != current_rows:
            raise AuditError("protected bytes changed while publishing the audit")
        if baseline_output.exists() and baseline_output.read_bytes() != baseline:
            raise AuditError("historical baseline changed while publishing the audit")

    outputs = [(report_output, report)]
    if initialize_baseline:
        outputs.append((baseline_output, baseline))
    _publish_transaction(outputs, history_is_unchanged)
    return findings, current_rows


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "analysis/model_candidates/context_first_scores_v1/"
            "CURRENT_CANDIDATE_AUDIT.md"
        ),
    )
    parser.add_argument(
        "--baseline-output",
        type=Path,
        default=Path(
            "analysis/model_candidates/context_first_scores_v1/"
            "historical_baseline_hashes.csv"
        ),
    )
    parser.add_argument(
        "--initialize-baseline",
        action="store_true",
        help="create the D1 historical baseline once; normal runs require it",
    )
    parser.add_argument(
        "--allowed-new-version",
        help="D10 only: permit additions inside one genuinely new model-version directory",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    repo = args.repo.resolve()
    report = args.output if args.output.is_absolute() else repo / args.output
    baseline = (
        args.baseline_output
        if args.baseline_output.is_absolute()
        else repo / args.baseline_output
    )
    try:
        findings, rows = write_audit(
            repo,
            report,
            baseline,
            initialize_baseline=args.initialize_baseline,
            allowed_new_version=args.allowed_new_version,
        )
    except (AuditError, OSError) as error:
        notes: list[str] = []
        observed: set[int] = set()
        current: BaseException | None = error
        while current is not None and id(current) not in observed:
            observed.add(id(current))
            notes.extend(getattr(current, "__notes__", ()))
            current = current.__cause__
        note_detail = "" if not notes else f" notes={' | '.join(notes)}"
        print(
            f"error_code=AUDIT_INTEGRITY_FAILURE detail={error}{note_detail}",
            file=sys.stderr,
        )
        return 2
    print("candidate=context_first_scores_v1")
    print(f"audit_findings={len(findings)}")
    print(f"protected_files={len(rows)}")
    print(f"output={report.relative_to(repo).as_posix() if report.is_relative_to(repo) else report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
