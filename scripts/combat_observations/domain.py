from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import unicodedata
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable, Iterator, Mapping

from .bundle import BundleError, sha256_file


NUMERIC_FIELDS = ("survivors", "kills", "upgrade_ready", "deaths", "wounded", "routed")
RANKING_CRITICAL_FIELDS = ("survivors", "kills", "deaths", "wounded", "canonical_troop_id")
BATTLE_CONTEXTS = ("field", "siege_attack", "siege_defense", "undefined")
ROW_TYPES = ("side_total", "party", "troop", "player", "hero", "artifact")
RELATIONSHIPS = ("player_party", "allied_party", "enemy_party", "unknown")
REVIEW_STATUSES = ("reviewed", "canonical", "excluded", "unresolved", "not_applicable")


class DomainError(BundleError):
    """Raised when an observation violates the canonical semantic contract."""


def stable_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def stable_id(prefix: str, *parts: object) -> str:
    payload = "\x1f".join(stable_json(part) for part in parts)
    return f"{prefix}_{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:20]}"


def normalize_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    asciiish = "".join(char for char in normalized if not unicodedata.combining(char))
    return " ".join(re.findall(r"[a-z0-9]+", asciiish.casefold()))


def parse_nullable_nonnegative_int(value: object, *, field: str, record_id: str) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise DomainError(f"{record_id}: {field} must be a non-negative integer or null")
    try:
        converted = int(value)
    except (TypeError, ValueError) as error:
        raise DomainError(f"{record_id}: {field} must be a non-negative integer or null") from error
    if converted < 0 or str(value).strip() not in {str(converted), f"{converted}.0"}:
        raise DomainError(f"{record_id}: {field} must be a non-negative integer or null")
    return converted


def safe_rate(numerator: int | None, denominator: int | None) -> str | None:
    if numerator is None or denominator is None or denominator == 0:
        return None
    return format((Decimal(numerator) / Decimal(denominator)).quantize(Decimal("0.000000")), "f")


def derived_metrics(record: Mapping[str, object]) -> dict[str, object]:
    record_id = str(record.get("observation_id") or record.get("consolidated_id") or "record")
    values = {
        field: parse_nullable_nonnegative_int(record.get(field), field=field, record_id=record_id)
        for field in NUMERIC_FIELDS
    }
    primary = [values["survivors"], values["deaths"], values["wounded"]]
    deployed = sum(primary) if all(value is not None for value in primary) else None
    casualties = (
        values["deaths"] + values["wounded"]
        if values["deaths"] is not None and values["wounded"] is not None
        else None
    )
    return {
        **values,
        "deployed": deployed,
        "casualties": casualties,
        "kills_per_deployed": safe_rate(values["kills"], deployed),
        "survival_rate": safe_rate(values["survivors"], deployed),
        "death_rate": safe_rate(values["deaths"], deployed),
        "wounded_rate": safe_rate(values["wounded"], deployed),
        "casualty_rate": safe_rate(casualties, deployed),
        "routed_rate": safe_rate(values["routed"], deployed),
    }


def evidence_grade(total_deployed: int, battle_count: int) -> str:
    if battle_count < 1:
        raise DomainError("evidence grade requires at least one battle")
    if total_deployed >= 100 and battle_count >= 5:
        return "high"
    if total_deployed >= 30 and battle_count >= 3:
        return "medium"
    if total_deployed >= 10 and battle_count >= 2:
        return "low"
    return "exploratory"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    records = []
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                value = json.loads(
                    line,
                    parse_constant=lambda constant: (_ for _ in ()).throw(
                        ValueError(f"non-standard JSON constant {constant}")
                    ),
                )
                if not isinstance(value, dict):
                    raise DomainError(f"{path}:{line_number}: JSONL record must be an object")
                records.append(value)
    except ValueError as error:
        line_number = getattr(error, "lineno", line_number if "line_number" in locals() else 1)
        raise DomainError(f"{path}:{line_number}: malformed JSONL: {error}") from error
    return records


def write_jsonl(path: Path, records: Iterable[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(stable_json(record) + "\n" for record in records)
    path.write_text(payload, encoding="utf-8", newline="\n")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if (
            not reader.fieldnames
            or any(not field.strip() for field in reader.fieldnames)
            or len(reader.fieldnames) != len(set(reader.fieldnames))
        ):
            raise DomainError(f"{path}: CSV has no header")
        rows = []
        for line_number, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise DomainError(f"{path}:{line_number}: malformed CSV row")
            rows.append(row)
        return rows


def write_csv(path: Path, rows: Iterable[Mapping[str, object]], fieldnames: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(fieldnames)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    field: stable_json(row[field]) if isinstance(row.get(field), (list, dict)) else row.get(field)
                    for field in fields
                }
            )


@dataclass(frozen=True)
class TroopCandidate:
    troop_id: str
    name: str
    normalized_name: str


class TroopMatcher:
    def __init__(
        self,
        troops: Iterable[tuple[str, str]],
        aliases: Iterable[tuple[str, str]] = (),
        *,
        fuzzy_threshold: float = 0.94,
        fuzzy_margin: float = 0.05,
    ) -> None:
        self.by_name: dict[str, TroopCandidate] = {}
        self.by_normalized: dict[str, list[TroopCandidate]] = {}
        self.by_id: dict[str, TroopCandidate] = {}
        for troop_id, name in troops:
            candidate = TroopCandidate(troop_id, name, normalize_name(name))
            if troop_id in self.by_id:
                raise DomainError(f"duplicate canonical troop ID: {troop_id}")
            self.by_id[troop_id] = candidate
            self.by_name[name] = candidate
            self.by_normalized.setdefault(candidate.normalized_name, []).append(candidate)
        self.aliases: dict[str, str] = {}
        for alias, troop_id in aliases:
            key = normalize_name(alias)
            if troop_id not in self.by_id:
                raise DomainError(f"alias target is not in troop registry: {troop_id}")
            previous = self.aliases.get(key)
            if previous and previous != troop_id:
                raise DomainError(f"alias collision for {alias}: {previous} vs {troop_id}")
            self.aliases[key] = troop_id
        self.fuzzy_threshold = fuzzy_threshold
        self.fuzzy_margin = fuzzy_margin

    def match(self, display_name: str) -> dict[str, object]:
        exact = self.by_name.get(display_name)
        if exact:
            return {"status": "accepted", "method": "exact", "troop_id": exact.troop_id, "candidates": []}
        normalized = normalize_name(display_name)
        normalized_matches = self.by_normalized.get(normalized, [])
        if len(normalized_matches) == 1:
            return {
                "status": "accepted",
                "method": "normalized_exact",
                "troop_id": normalized_matches[0].troop_id,
                "candidates": [],
            }
        if len(normalized_matches) > 1:
            return {
                "status": "ambiguous",
                "method": "normalized_collision",
                "troop_id": None,
                "candidates": [candidate.troop_id for candidate in normalized_matches],
            }
        alias_target = self.aliases.get(normalized)
        if alias_target:
            return {"status": "accepted", "method": "alias", "troop_id": alias_target, "candidates": []}
        scored = sorted(
            (
                (SequenceMatcher(None, normalized, candidate.normalized_name).ratio(), candidate)
                for candidate in self.by_id.values()
            ),
            key=lambda item: (-item[0], item[1].troop_id),
        )
        if not scored:
            return {"status": "unmatched", "method": "none", "troop_id": None, "candidates": []}
        best_score, best = scored[0]
        second_score = scored[1][0] if len(scored) > 1 else 0.0
        candidates = [
            {"troop_id": candidate.troop_id, "name": candidate.name, "score": f"{score:.6f}"}
            for score, candidate in scored[:5]
        ]
        if best_score >= self.fuzzy_threshold and best_score - second_score >= self.fuzzy_margin:
            return {
                "status": "accepted",
                "method": "conservative_fuzzy",
                "troop_id": best.troop_id,
                "score": f"{best_score:.6f}",
                "candidates": candidates,
            }
        return {
            "status": "ambiguous" if best_score >= self.fuzzy_threshold else "unmatched",
            "method": "fuzzy_review",
            "troop_id": None,
            "candidates": candidates,
        }


def load_troop_registry(path: Path) -> list[tuple[str, str]]:
    rows = read_csv(path)
    if not rows:
        raise DomainError(f"{path}: troop registry is empty")
    id_column = "troop_id" if "troop_id" in rows[0] else "canonical_troop_id"
    name_column = "name" if "name" in rows[0] else "troop_name"
    if id_column not in rows[0] or name_column not in rows[0]:
        raise DomainError(f"{path}: registry requires troop_id/name or canonical_troop_id/troop_name")
    return [(row[id_column], row[name_column]) for row in rows if row[id_column] and row[name_column]]


def load_aliases(path: Path | None) -> list[tuple[str, str]]:
    if path is None or not path.exists():
        return []
    rows = read_csv(path)
    return [(row["alias"], row["canonical_troop_id"]) for row in rows]


def raw_snapshot(root: Path) -> list[dict[str, object]]:
    entries = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        if relative.split("/", 1)[0] in {
            "canonical",
            "generated",
            "raw_extraction",
            "reports",
            "reviewed",
            "schemas",
            "staging",
        }:
            continue
        row_count = None
        if path.suffix == ".jsonl":
            row_count = len(read_jsonl(path))
        elif path.suffix == ".csv":
            row_count = len(read_csv(path))
        entries.append(
            {
                "path": relative,
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
                "row_count": row_count,
            }
        )
    return entries


def validate_occurrence(record: Mapping[str, object]) -> list[dict[str, str]]:
    record_id = str(record.get("observation_id") or "unknown")
    errors: list[dict[str, str]] = []
    for field in ("observation_id", "battle_id", "display_name_raw", "row_type", "battle_context"):
        if not record.get(field):
            errors.append({"record_id": record_id, "field": field, "error": "required"})
    if record.get("row_type") not in ROW_TYPES:
        errors.append({"record_id": record_id, "field": "row_type", "error": "invalid_enum"})
    if record.get("battle_context") not in BATTLE_CONTEXTS:
        errors.append({"record_id": record_id, "field": "battle_context", "error": "invalid_enum"})
    relationship = record.get("relationship_to_player", "unknown")
    if relationship not in RELATIONSHIPS:
        errors.append({"record_id": record_id, "field": "relationship_to_player", "error": "invalid_enum"})
    source = record.get("source")
    if not isinstance(source, dict):
        errors.append({"record_id": record_id, "field": "source", "error": "required_object"})
    else:
        if not source.get("image_file"):
            errors.append({"record_id": record_id, "field": "source.image_file", "error": "required"})
        digest = source.get("image_sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append({"record_id": record_id, "field": "source.image_sha256", "error": "invalid_sha256"})
    try:
        metrics = derived_metrics(record)
    except DomainError as error:
        errors.append({"record_id": record_id, "field": "numeric", "error": str(error)})
        return errors
    if record.get("deployed") is not None and record.get("deployed") != metrics["deployed"]:
        errors.append({"record_id": record_id, "field": "deployed", "error": "derived_value_mismatch"})
    if record.get("row_type") == "troop" and record.get("analysis_status") == "primary":
        if not record.get("canonical_troop_id"):
            errors.append({"record_id": record_id, "field": "canonical_troop_id", "error": "required_for_primary"})
        for field in ("survivors", "kills", "deaths", "wounded"):
            if metrics[field] is None:
                errors.append({"record_id": record_id, "field": field, "error": "required_for_primary"})
    return errors
