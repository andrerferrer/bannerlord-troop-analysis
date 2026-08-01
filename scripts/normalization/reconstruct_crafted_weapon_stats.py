#!/usr/bin/env python3
"""Reconstruct crafted-weapon stats from a real crafting-piece stats catalog.

Context
-------
Every `item_kind == "CraftedItem"` row in `<track>_troop_equipment_audit.csv` ships
with blank `swing_damage` / `thrust_damage` and `crafted_stats_reconstructed=False`
(3,619 vanilla / 3,723 nightmare_sails / 9,648 realm_of_thrones / 6,663 taom rows in
`export_20260731_150800`). The repository holds the crafted-item *composition*
(`data/<track>/audit/<track>_crafted_item_pieces.csv`: `item_id, piece_id, piece_type,
scale_factor`) but **no piece physics/damage stats at all**. Those live only in
`crafting_pieces*.xml` / `crafting_templates*.xml` on the Bannerlord PC.

This script is the consumer that unblocks the moment those catalogs exist. It refuses
to run without them. It never fabricates, zero-fills, or interpolates a damage number.

See `docs/handoff/PC_CRAFTING_PIECES_EXPORT_PROMPT.md` for how to produce the inputs.

Stdlib only (no pandas in this environment). Deterministic: identical inputs produce a
byte-identical output file.

Formula
-------
`formula_version = "piece_composition_v1"`.

Every coefficient comes from the input catalogs. There are no hardcoded damage
constants in this file. For a crafted item with pieces P (from the repo's
`crafted_item_pieces.csv`), where `s_p = scale_factor_p / 100` (blank -> 1.0):

    blade          = the piece_type == "Blade" member of P
                     (deterministic tie-break: highest swing_damage_factor,
                      then lowest piece_id)
    weapon_length  = round( sum over p in P of length_p * s_p )
    weight         = sum over p in P of weight_p * s_p            (6 decimals)
    swing_damage   = floor( template.swing_damage_base  * blade.swing_damage_factor  * s_blade )
    thrust_damage  = floor( template.thrust_damage_base * blade.thrust_damage_factor * s_blade )
    speed_rating   = round( template.speed_rating_base  * blade.swing_speed_factor   * s_blade )
    swing_damage_type  = blade.swing_damage_type  (else template.swing_damage_type)
    thrust_damage_type = blade.thrust_damage_type (else template.thrust_damage_type)
    weapon_class       = template.weapon_class

`piece_composition_v1` is an **approximation** of TaleWorlds' internal `WeaponDesign`
math, expressed so that every input is auditable. It MUST be validated against in-game
tooltips before any score consumes it -- pass `--tooltip-validation` (precedent:
`analysis/item_validation/2026-06-05_throwing_tooltips/`). Until that gate passes,
downstream consumers should keep treating crafted melee/thrown damage as a proxy.

Honesty rules enforced by the code
----------------------------------
* Missing catalog file, or catalog missing a required column -> exit 2 with
  `blocked: missing crafting piece catalog (...)`. No output file is written.
* A stat that cannot be computed from real inputs is written as an **empty cell**,
  never 0.
* `crafted_stats_reconstructed=True` only when swing_damage AND thrust_damage were
  both computed from a real blade piece plus a real template row.
* Every row carries `stat_source`, `piece_catalog_sha256`, `template_catalog_sha256`,
  `formula_version`, `export_id`, `track`.

Exit codes
----------
0  output written
2  blocked: a required input is absent or structurally insufficient
3  tooltip validation failed (only with --require-tooltip-validation)
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import sys
from pathlib import Path

FORMULA_VERSION = "piece_composition_v1"
DEFAULT_EXPORT_ID = "export_20260731_150800"
TRACKS = ("vanilla", "nightmare_sails", "realm_of_thrones", "taom")

# --- input contracts -------------------------------------------------------
# Keep these in lockstep with docs/handoff/PC_CRAFTING_PIECES_EXPORT_PROMPT.md.

PIECE_REQUIRED_COLUMNS = (
    "piece_id",
    "piece_type",
    "length",
    "weight",
    "swing_damage_factor",
    "thrust_damage_factor",
    "swing_damage_type",
    "thrust_damage_type",
    "swing_speed_factor",
    "source_xml",
    "source_module",
)

TEMPLATE_REQUIRED_COLUMNS = (
    "template_id",
    "weapon_class",
    "swing_damage_base",
    "thrust_damage_base",
    "speed_rating_base",
    "swing_damage_type",
    "thrust_damage_type",
    "source_xml",
    "source_module",
)

PIECES_JOIN_COLUMNS = ("item_id", "piece_id", "piece_type", "scale_factor")

OUTPUT_COLUMNS = (
    "item_id",
    "item_name",
    "crafting_template",
    "weapon_class",
    "swing_damage",
    "swing_damage_type",
    "thrust_damage",
    "thrust_damage_type",
    "speed_rating",
    "weapon_length",
    "weight",
    "blade_piece_id",
    "piece_count",
    "pieces_resolved",
    "crafted_stats_reconstructed",
    "stat_source",
    "blocked_reason",
    "track",
    "export_id",
    "formula_version",
    "piece_catalog_sha256",
    "template_catalog_sha256",
)

# stat_source vocabulary
SRC_FULL = "piece_catalog+template_catalog"
SRC_PIECE_ONLY = "piece_catalog_only"
SRC_UNRESOLVED_PIECES = "unresolved_pieces"
SRC_NO_BLADE = "no_blade_piece"
SRC_NO_TEMPLATE = "template_row_absent"


class Blocked(Exception):
    """A required input is absent or structurally insufficient."""


# --- small helpers ---------------------------------------------------------


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def num(value):
    """Parse a numeric cell. Blank / unparseable -> None (never 0)."""
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def text(value) -> str:
    return "" if value is None else str(value).strip()


def read_csv_rows(path: Path, required: tuple[str, ...], label: str) -> list[dict[str, str]]:
    if not path.is_file():
        raise Blocked(
            f"missing crafting piece catalog ({label} not found at {path}; "
            "see docs/handoff/PC_CRAFTING_PIECES_EXPORT_PROMPT.md)"
        )
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    missing = [name for name in required if name not in fieldnames]
    if missing:
        raise Blocked(
            f"missing crafting piece catalog ({label} at {path} lacks required "
            f"columns: {', '.join(missing)}; got: {', '.join(fieldnames) or '<no header>'})"
        )
    if not rows:
        raise Blocked(f"missing crafting piece catalog ({label} at {path} has no data rows)")
    return rows


def fmt_int(value) -> str:
    return "" if value is None else str(int(value))


def fmt_float(value, places: int = 6) -> str:
    if value is None:
        return ""
    return f"{value:.{places}f}"


# --- catalog loading -------------------------------------------------------


def load_piece_catalog(path: Path) -> dict[str, dict[str, str]]:
    rows = read_csv_rows(path, PIECE_REQUIRED_COLUMNS, "crafting piece stats catalog")
    catalog: dict[str, dict[str, str]] = {}
    for row in rows:
        piece_id = text(row.get("piece_id"))
        if not piece_id:
            continue
        # Deterministic last-writer-wins is unsafe here; keep the first occurrence
        # and require the exporter to have already applied load order.
        catalog.setdefault(piece_id, row)
    if not catalog:
        raise Blocked(
            f"missing crafting piece catalog ({path} has rows but no usable piece_id values)"
        )
    usable = sum(
        1
        for row in catalog.values()
        if text(row.get("piece_type")) == "Blade"
        and num(row.get("swing_damage_factor")) is not None
    )
    if usable == 0:
        raise Blocked(
            f"missing crafting piece catalog ({path} has no Blade row carrying a numeric "
            "swing_damage_factor, so no damage can be reconstructed)"
        )
    return catalog


def load_template_catalog(path: Path | None) -> tuple[dict[str, dict[str, str]], str]:
    if path is None:
        return {}, ""
    rows = read_csv_rows(path, TEMPLATE_REQUIRED_COLUMNS, "crafting template stats catalog")
    catalog: dict[str, dict[str, str]] = {}
    for row in rows:
        template_id = text(row.get("template_id"))
        if template_id:
            catalog.setdefault(template_id, row)
    if not catalog:
        raise Blocked(
            f"missing crafting piece catalog ({path} has rows but no usable template_id values)"
        )
    return catalog, sha256_file(path)


def load_item_pieces(path: Path) -> dict[str, list[dict[str, str]]]:
    if not path.is_file():
        raise Blocked(
            f"missing crafting piece catalog (track composition file {path} not found; "
            "rebuild the track audit first)"
        )
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    missing = [name for name in PIECES_JOIN_COLUMNS if name not in fieldnames]
    if missing:
        raise Blocked(
            f"missing crafting piece catalog ({path} lacks required columns: {', '.join(missing)})"
        )
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        item_id = text(row.get("item_id"))
        if item_id:
            grouped.setdefault(item_id, []).append(row)
    if not grouped:
        raise Blocked(f"missing crafting piece catalog ({path} has no crafted item rows)")
    return grouped


def load_crafted_items(path: Path) -> dict[str, dict[str, str]]:
    """Optional: supplies item_name + crafting_template. Absent -> blank columns."""
    if not path.is_file():
        return {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return {text(row.get("item_id")): row for row in rows if text(row.get("item_id"))}


# --- the formula -----------------------------------------------------------


def scale_of(row: dict[str, str]) -> float:
    value = num(row.get("scale_factor"))
    if value is None or value <= 0:
        return 1.0
    return value / 100.0


def pick_blade(members: list[tuple[dict[str, str], dict[str, str]]]):
    """Deterministically choose the damage-bearing Blade piece.

    members: list of (join_row, catalog_row) pairs already filtered to piece_type Blade.
    Tie-break: highest swing_damage_factor, then lowest piece_id.
    """
    if not members:
        return None
    return sorted(
        members,
        key=lambda pair: (
            -(num(pair[1].get("swing_damage_factor")) or 0.0),
            text(pair[1].get("piece_id")),
        ),
    )[0]


def reconstruct_item(
    item_id: str,
    join_rows: list[dict[str, str]],
    piece_catalog: dict[str, dict[str, str]],
    template_catalog: dict[str, dict[str, str]],
    crafted_items: dict[str, dict[str, str]],
) -> dict[str, str]:
    item_meta = crafted_items.get(item_id, {})
    template_id = text(item_meta.get("crafting_template"))
    template = template_catalog.get(template_id) if template_id else None

    resolved: list[tuple[dict[str, str], dict[str, str]]] = []
    for join_row in join_rows:
        catalog_row = piece_catalog.get(text(join_row.get("piece_id")))
        if catalog_row is not None:
            resolved.append((join_row, catalog_row))

    out = {name: "" for name in OUTPUT_COLUMNS}
    out["item_id"] = item_id
    out["item_name"] = text(item_meta.get("name"))
    out["crafting_template"] = template_id
    out["piece_count"] = str(len(join_rows))
    out["pieces_resolved"] = str(len(resolved))
    out["crafted_stats_reconstructed"] = "False"

    if not resolved:
        out["stat_source"] = SRC_UNRESOLVED_PIECES
        out["blocked_reason"] = "no piece_id of this item exists in the piece stats catalog"
        return out

    # Geometry / mass: piece-only, no template needed.
    lengths = [
        (num(cat.get("length")), scale_of(join))
        for join, cat in resolved
        if num(cat.get("length")) is not None
    ]
    if lengths:
        out["weapon_length"] = fmt_int(round(sum(value * scale for value, scale in lengths)))
    weights = [
        (num(cat.get("weight")), scale_of(join))
        for join, cat in resolved
        if num(cat.get("weight")) is not None
    ]
    if weights:
        out["weight"] = fmt_float(sum(value * scale for value, scale in weights))

    blades = [pair for pair in resolved if text(pair[1].get("piece_type")) == "Blade"]
    blade_pair = pick_blade(blades)
    if blade_pair is None:
        out["stat_source"] = SRC_NO_BLADE
        out["blocked_reason"] = "item has no resolved Blade piece; damage is not derivable"
        return out

    blade_join, blade = blade_pair
    blade_scale = scale_of(blade_join)
    out["blade_piece_id"] = text(blade.get("piece_id"))
    out["swing_damage_type"] = text(blade.get("swing_damage_type"))
    out["thrust_damage_type"] = text(blade.get("thrust_damage_type"))

    if template is None:
        out["stat_source"] = SRC_PIECE_ONLY if template_catalog else SRC_NO_TEMPLATE
        out["blocked_reason"] = (
            "no template stats row for "
            f"crafting_template={template_id or '<blank>'}; absolute damage not derivable"
        )
        return out

    out["weapon_class"] = text(template.get("weapon_class"))
    if not out["swing_damage_type"]:
        out["swing_damage_type"] = text(template.get("swing_damage_type"))
    if not out["thrust_damage_type"]:
        out["thrust_damage_type"] = text(template.get("thrust_damage_type"))

    swing_base = num(template.get("swing_damage_base"))
    thrust_base = num(template.get("thrust_damage_base"))
    speed_base = num(template.get("speed_rating_base"))
    swing_factor = num(blade.get("swing_damage_factor"))
    thrust_factor = num(blade.get("thrust_damage_factor"))
    speed_factor = num(blade.get("swing_speed_factor"))

    if swing_base is not None and swing_factor is not None:
        out["swing_damage"] = fmt_int(math.floor(swing_base * swing_factor * blade_scale))
    if thrust_base is not None and thrust_factor is not None:
        out["thrust_damage"] = fmt_int(math.floor(thrust_base * thrust_factor * blade_scale))
    if speed_base is not None and speed_factor is not None:
        out["speed_rating"] = fmt_int(round(speed_base * speed_factor * blade_scale))

    if out["swing_damage"] and out["thrust_damage"]:
        out["stat_source"] = SRC_FULL
        out["crafted_stats_reconstructed"] = "True"
    else:
        out["stat_source"] = SRC_PIECE_ONLY
        missing = [
            name
            for name, value in (
                ("swing_damage", out["swing_damage"]),
                ("thrust_damage", out["thrust_damage"]),
            )
            if not value
        ]
        out["blocked_reason"] = (
            "catalog lacked numeric inputs for: " + ", ".join(missing)
        )
    return out


# --- tooltip validation gate ----------------------------------------------


def validate_against_tooltips(
    rows: list[dict[str, str]], path: Path, tolerance: float
) -> tuple[list[str], int]:
    """Compare reconstructed damage against observed in-game tooltip values.

    Expected columns: item_id, observed_swing_damage, observed_thrust_damage.
    Blank observed cells are skipped. Returns (failure messages, compared count).
    """
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        observed_rows = list(reader)
    required = ("item_id", "observed_swing_damage", "observed_thrust_damage")
    missing = [name for name in required if name not in fieldnames]
    if missing:
        raise Blocked(
            f"tooltip validation file {path} lacks required columns: {', '.join(missing)}"
        )
    by_item = {row["item_id"]: row for row in rows}
    failures: list[str] = []
    compared = 0
    for observed in observed_rows:
        item_id = text(observed.get("item_id"))
        row = by_item.get(item_id)
        if row is None:
            failures.append(f"{item_id}: not present in reconstructed output")
            continue
        for stat, column in (
            ("swing_damage", "observed_swing_damage"),
            ("thrust_damage", "observed_thrust_damage"),
        ):
            want = num(observed.get(column))
            if want is None:
                continue
            got = num(row.get(stat))
            if got is None:
                failures.append(f"{item_id}.{stat}: expected {want:g}, reconstruction is blank")
                continue
            compared += 1
            if abs(got - want) > tolerance:
                failures.append(
                    f"{item_id}.{stat}: expected {want:g}, got {got:g} "
                    f"(tolerance {tolerance:g})"
                )
    return failures, compared


# --- driver ---------------------------------------------------------------


def build_rows(
    track: str,
    audit_dir: Path,
    piece_catalog_path: Path,
    template_catalog_path: Path | None,
    export_id: str,
) -> list[dict[str, str]]:
    piece_catalog = load_piece_catalog(piece_catalog_path)
    piece_sha = sha256_file(piece_catalog_path)
    template_catalog, template_sha = load_template_catalog(template_catalog_path)
    item_pieces = load_item_pieces(audit_dir / f"{track}_crafted_item_pieces.csv")
    crafted_items = load_crafted_items(audit_dir / f"{track}_items_crafted.csv")

    rows: list[dict[str, str]] = []
    for item_id in sorted(item_pieces):
        row = reconstruct_item(
            item_id,
            item_pieces[item_id],
            piece_catalog,
            template_catalog,
            crafted_items,
        )
        row["track"] = track
        row["export_id"] = export_id
        row["formula_version"] = FORMULA_VERSION
        row["piece_catalog_sha256"] = piece_sha
        row["template_catalog_sha256"] = template_sha
        rows.append(row)
    return rows


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(OUTPUT_COLUMNS), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--track", required=True, choices=list(TRACKS))
    parser.add_argument(
        "--piece-catalog",
        type=Path,
        required=True,
        help="Crafting piece stats catalog CSV (see PC_CRAFTING_PIECES_EXPORT_PROMPT.md)",
    )
    parser.add_argument(
        "--template-catalog",
        type=Path,
        default=None,
        help="Crafting template stats catalog CSV. Without it, absolute damage is not "
        "derivable and every row stays crafted_stats_reconstructed=False.",
    )
    parser.add_argument("--audit-dir", type=Path, default=None, help="Default: data/<track>/audit")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--export-id", default=DEFAULT_EXPORT_ID)
    parser.add_argument("--tooltip-validation", type=Path, default=None)
    parser.add_argument("--tolerance", type=float, default=1.0)
    parser.add_argument(
        "--require-tooltip-validation",
        action="store_true",
        help="Exit 3 when any validated item disagrees beyond --tolerance.",
    )
    args = parser.parse_args(argv)

    repo = Path(__file__).resolve().parents[2]
    audit_dir = args.audit_dir or repo / "data" / args.track / "audit"
    output = args.output or audit_dir / f"{args.track}_crafted_weapon_stats.csv"

    try:
        rows = build_rows(
            args.track,
            audit_dir,
            args.piece_catalog,
            args.template_catalog,
            args.export_id,
        )
    except Blocked as error:
        print(f"blocked: {error}", file=sys.stderr)
        return 2

    validation_note = ""
    if args.tooltip_validation is not None:
        try:
            failures, compared = validate_against_tooltips(
                rows, args.tooltip_validation, args.tolerance
            )
        except Blocked as error:
            print(f"blocked: {error}", file=sys.stderr)
            return 2
        validation_note = f"tooltip_validation: compared={compared} failures={len(failures)}"
        if failures and args.require_tooltip_validation:
            print(validation_note, file=sys.stderr)
            for message in failures:
                print(f"  tooltip mismatch: {message}", file=sys.stderr)
            print(
                "refusing to publish reconstructed stats that disagree with in-game tooltips",
                file=sys.stderr,
            )
            return 3

    write_rows(output, rows)

    reconstructed = sum(1 for row in rows if row["crafted_stats_reconstructed"] == "True")
    print(f"track={args.track}")
    print(f"formula_version={FORMULA_VERSION}")
    print(f"crafted_items={len(rows)}")
    print(f"reconstructed={reconstructed}")
    print(f"not_reconstructed={len(rows) - reconstructed}")
    if validation_note:
        print(validation_note)
    print(f"output={output}")
    if reconstructed:
        print(
            "reminder: data/<track>/audit/*.csv is hash-pinned -- re-run "
            "scripts/normalization/build_xml_ssot_package_hashes.py before scoring, "
            "or run_theoretical_role_scores.py will fail its preflight."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
