#!/usr/bin/env python3
"""Build a strict, battle-resampled empirical baseline from normalized troop occurrences."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

KNOWN_CONTEXTS = ("field", "siege_attack", "siege_defense")
NUMERIC_FIELDS = ("survivors", "kills", "deaths", "wounded", "routed", "deployed")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on {path}:{line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"Expected object on {path}:{line_number}")
            rows.append(value)
    return rows


def is_strict_player_row(row: dict[str, Any]) -> bool:
    if row.get("analysis_status") != "included" or row.get("row_type") != "troop":
        return False
    if row.get("side") != row.get("player_side"):
        return False
    if row.get("battle_type") not in KNOWN_CONTEXTS:
        return False
    if bool(row.get("needs_review")) or bool(row.get("suspected_siege_engine_outlier")):
        return False
    if any(row.get(field) is None for field in NUMERIC_FIELDS):
        return False
    return int(row["deployed"]) > 0


def consolidate(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    result: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in rows:
        key = (str(row["battle_id"]), str(row["battle_type"]), str(row["canonical_name_slug"]))
        if key not in result:
            result[key] = {
                "battle_id": key[0],
                "context": key[1],
                "canonical_name_slug": key[2],
                "display_names": Counter(),
                **{field: 0 for field in NUMERIC_FIELDS},
            }
        target = result[key]
        target["display_names"][str(row.get("display_name_normalized") or row.get("display_name_raw") or key[2])] += 1
        for field in NUMERIC_FIELDS:
            target[field] += int(row[field])

    consolidated: list[dict[str, Any]] = []
    for target in result.values():
        target["display_name"] = target.pop("display_names").most_common(1)[0][0]
        consolidated.append(target)
    return consolidated


def bootstrap_ratio(items: list[dict[str, Any]], context: str, slug: str, repetitions: int) -> tuple[float, float]:
    seed = int(hashlib.sha256(f"{context}|{slug}".encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    samples: list[float] = []
    for _ in range(repetitions):
        sample = [items[rng.randrange(len(items))] for _ in items]
        deployed = sum(int(item["deployed"]) for item in sample)
        kills = sum(int(item["kills"]) for item in sample)
        samples.append(kills / deployed if deployed else 0.0)
    samples.sort()
    low = samples[int(0.025 * (repetitions - 1))]
    high = samples[int(0.975 * (repetitions - 1))]
    return low, high


def build_rankings(
    rows: list[dict[str, Any]],
    minimum_battles: int,
    minimum_deployed: int,
    repetitions: int,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for context in ("overall", *KNOWN_CONTEXTS):
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            if context == "overall" or row["context"] == context:
                groups[str(row["canonical_name_slug"])].append(row)

        context_rows: list[dict[str, Any]] = []
        for slug, items in groups.items():
            battle_count = len(items)
            deployed = sum(int(item["deployed"]) for item in items)
            if battle_count < minimum_battles or deployed < minimum_deployed:
                continue
            kills = sum(int(item["kills"]) for item in items)
            deaths = sum(int(item["deaths"]) for item in items)
            wounded = sum(int(item["wounded"]) for item in items)
            low, high = bootstrap_ratio(items, context, slug, repetitions)
            context_rows.append(
                {
                    "context": context,
                    "display_name": Counter(str(item["display_name"]) for item in items).most_common(1)[0][0],
                    "canonical_name_slug": slug,
                    "battle_count": battle_count,
                    "total_deployed": deployed,
                    "total_kills": kills,
                    "kills_per_deployed": kills / deployed,
                    "ci95_low": low,
                    "ci95_high": high,
                    "death_rate": deaths / deployed,
                    "casualty_rate": (deaths + wounded) / deployed,
                }
            )

        context_rows.sort(key=lambda row: (row["kills_per_deployed"], row["total_deployed"]), reverse=True)
        for rank, row in enumerate(context_rows, start=1):
            row["rank"] = rank
            output.append(row)
    return output


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = (
        "context", "rank", "display_name", "canonical_name_slug", "battle_count",
        "total_deployed", "total_kills", "kills_per_deployed", "ci95_low",
        "ci95_high", "death_rate", "casualty_rate",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: round(row[field], 6) if isinstance(row[field], float) else row[field] for field in fields})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="primary_troop_occurrences.jsonl")
    parser.add_argument("output", type=Path, help="output CSV path")
    parser.add_argument("--minimum-battles", type=int, default=5)
    parser.add_argument("--minimum-deployed", type=int, default=20)
    parser.add_argument("--bootstrap-repetitions", type=int, default=5000)
    args = parser.parse_args()

    source_rows = read_jsonl(args.input)
    strict_rows = [row for row in source_rows if is_strict_player_row(row)]
    battle_rows = consolidate(strict_rows)
    rankings = build_rankings(
        battle_rows,
        minimum_battles=args.minimum_battles,
        minimum_deployed=args.minimum_deployed,
        repetitions=args.bootstrap_repetitions,
    )
    write_csv(args.output, rankings)

    summary = {
        "source_occurrences": len(source_rows),
        "strict_occurrences": len(strict_rows),
        "strict_battle_troop_rows": len(battle_rows),
        "independent_battles": len({row["battle_id"] for row in strict_rows}),
        "provisional_troop_identifiers": len({row["canonical_name_slug"] for row in strict_rows}),
        "eligible_by_context": dict(Counter(row["context"] for row in rankings)),
        "minimum_battles": args.minimum_battles,
        "minimum_deployed": args.minimum_deployed,
        "bootstrap_repetitions": args.bootstrap_repetitions,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
