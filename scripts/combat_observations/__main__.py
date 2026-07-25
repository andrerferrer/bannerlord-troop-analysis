from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analysis import (
    build_tier_role_views,
    calibration_decision,
    compare_models,
)
from .archive_input import prepare_input, safe_extract_zip
from .bundle import (
    EXPECTED_ARCHIVE_SHA256,
    BundleError,
    atomic_write_json,
    build_forensic_report,
    discover_parts,
    reconstruct_and_verify,
    sha256_file,
    validate_extracted_outputs,
)
from .canonical import build_canonical_dataset
from .domain import raw_snapshot, read_jsonl, validate_occurrence
from .model_assisted import MODES, prepare_extraction_queue
from .review import triage_review_queue
from .schema_validation import validate_jsonl_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="combat-observations")
    subcommands = parser.add_subparsers(dest="command", required=True)

    reconstruct = subcommands.add_parser(
        "reconstruct-bundle",
        help="Strictly reconstruct, hash-verify, safely extract, and parse a normalized bundle.",
    )
    reconstruct.add_argument("--bundle-dir", type=Path, required=True)
    reconstruct.add_argument("--archive", type=Path, required=True)
    reconstruct.add_argument("--extract-dir", type=Path, required=True)
    reconstruct.add_argument("--report", type=Path, required=True)
    reconstruct.add_argument("--forensic-report", type=Path)
    reconstruct.add_argument("--expected-sha256", default=EXPECTED_ARCHIVE_SHA256)

    verify = subcommands.add_parser("verify-bundle", help="Verify an existing archive hash and extracted payload.")
    verify.add_argument("--archive", type=Path, required=True)
    verify.add_argument("--extract-dir", type=Path, required=True)
    verify.add_argument("--report", type=Path, required=True)
    verify.add_argument("--expected-sha256", default=EXPECTED_ARCHIVE_SHA256)

    manifest = subcommands.add_parser(
        "manifest-images",
        help="Safely stage a ZIP or inventory a screenshot directory and write hashes.",
    )
    manifest.add_argument("--input", type=Path, required=True)
    manifest.add_argument("--output-dir", type=Path, required=True)
    manifest.add_argument("--max-members", type=int, default=10_000)
    manifest.add_argument("--max-uncompressed-bytes", type=int, default=1_000_000_000)
    manifest.add_argument("--max-compression-ratio", type=float, default=1_000.0)

    stage = subcommands.add_parser(
        "stage-normalized-zip",
        help="Safely extract a ZIP containing normalized outputs without treating it as an image batch.",
    )
    stage.add_argument("--input", type=Path, required=True)
    stage.add_argument("--output-dir", type=Path, required=True)
    stage.add_argument("--report", type=Path, required=True)
    stage.add_argument("--max-members", type=int, default=10_000)
    stage.add_argument("--max-uncompressed-bytes", type=int, default=1_000_000_000)
    stage.add_argument("--max-compression-ratio", type=float, default=1_000.0)

    extract = subcommands.add_parser(
        "extract-combat-screens",
        help="Prepare a resumable extraction queue for offline, host-vision, or API mode.",
    )
    extract.add_argument("--manifest", type=Path, required=True)
    extract.add_argument("--output-dir", type=Path, required=True)
    extract.add_argument("--mode", choices=MODES, required=True)
    extract.add_argument("--authorize-paid-api", action="store_true")
    extract.add_argument("--estimated-cost-per-image", type=float)

    triage = subcommands.add_parser("triage-review-queue", help="Categorize and prioritize review rows.")
    triage.add_argument("--input", type=Path, required=True)
    triage.add_argument("--output-dir", type=Path, required=True)

    review = subcommands.add_parser("review-extractions", help="Alias for deterministic review-queue triage.")
    review.add_argument("--input", type=Path, required=True)
    review.add_argument("--output-dir", type=Path, required=True)

    canonical = subcommands.add_parser(
        "build-canonical-dataset",
        help="Build canonical v2 data from immutable raw JSONL plus explicit review decisions.",
    )
    canonical.add_argument("--raw-occurrences", type=Path, required=True)
    canonical.add_argument("--troop-registry", type=Path, required=True)
    canonical.add_argument("--corrections", type=Path)
    canonical.add_argument("--aliases", type=Path)
    canonical.add_argument("--schemas-dir", type=Path)
    canonical.add_argument("--fuzzy-threshold", type=float, default=0.94)
    canonical.add_argument("--fuzzy-margin", type=float, default=0.05)
    canonical.add_argument("--output-dir", type=Path, required=True)

    validate = subcommands.add_parser(
        "validate-canonical-dataset",
        help="Validate canonical JSONL against v2 schemas and semantic occurrence rules.",
    )
    validate.add_argument("--canonical-dir", type=Path, required=True)
    validate.add_argument("--schemas-dir", type=Path, required=True)
    validate.add_argument("--report", type=Path, required=True)

    rankings = subcommands.add_parser(
        "build-empirical-rankings",
        help="Build tier and role views from canonical historical aggregates.",
    )
    rankings.add_argument("--aggregates", type=Path, required=True)
    rankings.add_argument("--troop-metadata", type=Path, required=True)
    rankings.add_argument("--output-dir", type=Path, required=True)

    comparison = subcommands.add_parser("compare-models", help="Compare canonical empirical results with frozen models.")
    comparison.add_argument("--aggregates", type=Path, required=True)
    comparison.add_argument("--general-model", type=Path, required=True)
    comparison.add_argument("--burst-model", type=Path, required=True)
    comparison.add_argument("--output-dir", type=Path, required=True)

    calibration = subcommands.add_parser("calibration-decision", help="Apply the evidence gate before model changes.")
    calibration.add_argument("--analysis-summary", type=Path, required=True)
    calibration.add_argument("--aggregates", type=Path, required=True)
    calibration.add_argument("--output", type=Path, required=True)

    snapshot = subcommands.add_parser("snapshot-raw", help="Hash immutable first-pass source files.")
    snapshot.add_argument("--raw-root", type=Path, required=True)
    snapshot.add_argument("--output", type=Path, required=True)
    return parser


def run_reconstruct(args: argparse.Namespace) -> int:
    try:
        report = reconstruct_and_verify(
            args.bundle_dir,
            args.archive,
            args.extract_dir,
            expected_sha256=args.expected_sha256,
        )
    except BundleError as error:
        failure = {
            "schema_version": "1.0.0",
            "status": "failed",
            "error_type": type(error).__name__,
            "error": str(error),
            "expected_archive_sha256": args.expected_sha256,
        }
        atomic_write_json(args.report, failure)
        if args.forensic_report:
            try:
                parts = discover_parts(args.bundle_dir)
                forensic = build_forensic_report(
                    parts,
                    expected_sha256=args.expected_sha256,
                    exact_error=str(error),
                )
                atomic_write_json(args.forensic_report, forensic)
            except BundleError as forensic_error:
                atomic_write_json(
                    args.forensic_report,
                    {
                        "schema_version": "1.0.0",
                        "status": "forensic_failed",
                        "error": str(forensic_error),
                    },
                )
        print(str(error), file=sys.stderr)
        return 2
    atomic_write_json(args.report, report)
    print(f"verified archive: {report['archive_sha256']}")
    return 0


def run_verify(args: argparse.Namespace) -> int:
    actual = sha256_file(args.archive)
    if actual != args.expected_sha256:
        raise BundleError(f"archive SHA-256 mismatch: expected {args.expected_sha256}, observed {actual}")
    validation = validate_extracted_outputs(args.extract_dir)
    report = {
        "schema_version": "1.0.0",
        "status": "verified",
        "archive_sha256": actual,
        "extracted_validation": validation,
    }
    atomic_write_json(args.report, report)
    return 0


def run_validate_canonical(args: argparse.Namespace) -> int:
    pairs = (
        ("canonical_screenshots.jsonl", "screenshot.schema.json"),
        ("canonical_battles.jsonl", "battle.schema.json"),
        ("canonical_occurrences.jsonl", "troop-occurrence.schema.json"),
        ("canonical_troop_battle_consolidated.jsonl", "battle-troop-consolidation.schema.json"),
        ("canonical_historical_aggregates.jsonl", "historical-aggregate.schema.json"),
    )
    schema_errors = [
        error
        for data_name, schema_name in pairs
        for error in validate_jsonl_file(args.canonical_dir / data_name, args.schemas_dir / schema_name)
    ]
    semantic_errors = [
        error
        for record in read_jsonl(args.canonical_dir / "canonical_occurrences.jsonl")
        for error in validate_occurrence(record)
    ]
    report = {
        "schema_version": "2.0.0",
        "status": "passed" if not schema_errors and not semantic_errors else "failed",
        "schema_errors": schema_errors,
        "semantic_errors": semantic_errors,
    }
    atomic_write_json(args.report, report)
    return 0 if report["status"] == "passed" else 2


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "reconstruct-bundle":
            return run_reconstruct(args)
        if args.command == "verify-bundle":
            return run_verify(args)
        if args.command == "manifest-images":
            prepare_input(
                args.input,
                args.output_dir,
                max_members=args.max_members,
                max_uncompressed_bytes=args.max_uncompressed_bytes,
                max_compression_ratio=args.max_compression_ratio,
            )
            return 0
        if args.command == "stage-normalized-zip":
            report = safe_extract_zip(
                args.input,
                args.output_dir,
                max_members=args.max_members,
                max_uncompressed_bytes=args.max_uncompressed_bytes,
                max_compression_ratio=args.max_compression_ratio,
            )
            atomic_write_json(
                args.report,
                {
                    "schema_version": "1.0.0",
                    "status": "staged",
                    "input_sha256": sha256_file(args.input),
                    **report,
                },
            )
            return 0
        if args.command == "extract-combat-screens":
            prepare_extraction_queue(
                args.manifest,
                args.output_dir,
                mode=args.mode,
                authorize_paid_api=args.authorize_paid_api,
                estimated_cost_per_image=args.estimated_cost_per_image,
            )
            return 0
        if args.command in {"triage-review-queue", "review-extractions"}:
            triage_review_queue(args.input, args.output_dir)
            return 0
        if args.command == "build-canonical-dataset":
            validation = build_canonical_dataset(
                args.raw_occurrences,
                args.output_dir,
                args.troop_registry,
                corrections_path=args.corrections,
                aliases_path=args.aliases,
                schemas_dir=args.schemas_dir,
                fuzzy_threshold=args.fuzzy_threshold,
                fuzzy_margin=args.fuzzy_margin,
            )
            return 0 if validation["status"] != "failed" else 2
        if args.command == "validate-canonical-dataset":
            return run_validate_canonical(args)
        if args.command == "build-empirical-rankings":
            build_tier_role_views(args.aggregates, args.troop_metadata, args.output_dir)
            return 0
        if args.command == "compare-models":
            compare_models(args.aggregates, args.general_model, args.burst_model, args.output_dir)
            return 0
        if args.command == "calibration-decision":
            calibration_decision(args.analysis_summary, args.aggregates, args.output)
            return 0
        if args.command == "snapshot-raw":
            atomic_write_json(
                args.output,
                {
                    "schema_version": "1.0.0",
                    "raw_root": args.raw_root.name,
                    "files": raw_snapshot(args.raw_root),
                },
            )
            return 0
        raise AssertionError(args.command)
    except BundleError as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
