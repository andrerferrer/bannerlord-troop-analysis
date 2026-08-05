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
import hashlib
import io
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


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

EXPECTED_V73_MODEL = (
    "analysis/model_versions/v7.3_tooltip_damage_burst/"
    "bannerlord_v73_tooltip_damage_burst_model_all_official_troops.csv"
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
    return (
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
        FindingSpec("role_scores_v1", v1, False, False, False, False, "ALTERNATIVE_POLICY_UNDECLARED", "best item and roster aggregation", "Favorable item and roster outputs are selected with max instead of a declared alternative-equipment mean."),
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
        FindingSpec("defensive_role_scores_v2_candidate", v2, False, False, False, False, "MOUNTED_INPUT_NON_APPLICABLE", "cavalry protection/utility lanes", "Mount and harness inputs cannot answer siege-defense defense after dismounting."),
        FindingSpec("v7.1", EXPECTED_V71_MODEL, False, False, False, False, "SOURCE_ARTIFACT_ABSENT", "general model CSV", "The repository references this v7.1 input, but its bytes are not present in the checkout."),
        FindingSpec("v7.3", EXPECTED_V73_MODEL, False, False, False, False, "SOURCE_ARTIFACT_ABSENT", "full tooltip-damage burst model CSV", "The v7.3 builder and documentation reference this full model output, but its bytes are not present in the checkout."),
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
    )


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


def _protected_paths(repo: Path) -> Iterable[tuple[Path, str]]:
    candidate_prefix = "analysis/model_candidates/role_scores_v2_defense/"
    model_prefix = "analysis/model_versions/"
    audited = set(AUDITED_SOURCES)
    observed_classes: set[str] = set()
    observed_sources: set[str] = set()

    for relative in _tracked_files(repo):
        classification = ""
        if relative.startswith(candidate_prefix):
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
        if path.is_symlink():
            raise AuditError(f"protected path is a symlink: {relative}")
        if not path.is_file():
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
        content = path.read_bytes()
        rows[relative] = BaselineRow(
            path=relative,
            bytes=len(content),
            sha256=_sha256_bytes(content),
            immutability_class=classification,
        )
    return tuple(rows[path] for path in sorted(rows))


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
    repo: Path, baseline_path: Path
) -> tuple[BaselineRow, ...]:
    repo = repo.resolve()
    baseline_path = (
        baseline_path
        if baseline_path.is_absolute()
        else repo / baseline_path
    ).resolve()
    rows = build_historical_baseline(repo)
    if not baseline_path.is_file():
        raise AuditError(f"historical baseline missing: {baseline_path}")
    if baseline_path.read_bytes() != _baseline_bytes(rows):
        raise AuditError(
            "existing historical baseline differs from current protected bytes"
        )
    return rows


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


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(content)
    os.replace(temporary, path)


def _validate_output_paths(
    repo: Path, report_output: Path, baseline_output: Path
) -> tuple[Path, Path]:
    report = report_output.resolve()
    baseline = baseline_output.resolve()
    if report == baseline:
        raise AuditError("report and baseline outputs must be distinct")

    protected_roots = {
        (repo / "analysis/model_candidates/role_scores_v2_defense").resolve(),
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
    return report, baseline


def write_audit(
    repo: Path,
    report_output: Path,
    baseline_output: Path,
    *,
    initialize_baseline: bool = False,
) -> tuple[tuple[AuditFinding, ...], tuple[BaselineRow, ...]]:
    repo = repo.resolve()
    report_output, baseline_output = _validate_output_paths(
        repo, report_output, baseline_output
    )
    findings = build_findings(repo)
    baseline_rows = build_historical_baseline(repo)
    baseline = _baseline_bytes(baseline_rows)
    report = _report_bytes(findings, baseline_rows, baseline)

    if initialize_baseline:
        if baseline_output.exists():
            raise AuditError("historical baseline already exists; refusing initialization")
    else:
        if not baseline_output.is_file():
            raise AuditError("historical baseline missing; use --initialize-baseline once")
        if baseline_output.read_bytes() != baseline:
            raise AuditError(
                "existing historical baseline differs from current protected bytes; refusing to rewrite it"
            )

    _atomic_write(report_output, report)
    if initialize_baseline:
        _atomic_write(baseline_output, baseline)

    if build_historical_baseline(repo) != baseline_rows:
        raise AuditError("protected bytes changed while publishing the audit")
    return findings, baseline_rows


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
        )
    except AuditError as error:
        print(f"error_code=AUDIT_INTEGRITY_FAILURE detail={error}", file=sys.stderr)
        return 2
    print("candidate=context_first_scores_v1")
    print(f"audit_findings={len(findings)}")
    print(f"protected_files={len(rows)}")
    print(f"output={report.relative_to(repo).as_posix() if report.is_relative_to(repo) else report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
