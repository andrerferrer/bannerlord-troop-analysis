#!/usr/bin/env python3
"""Direct equipment evidence resolution for context-first scoring."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Mapping, Sequence

from context_first_contract import (
    ARMOR_FIELDS,
    ARMOR_ITEM_ID_MISSING,
    ARMOR_ITEM_UNRESOLVED,
    ARMOR_REGION_MISSING,
    ARMOR_VALUE_INVALID,
    DECIMAL_QUANTUM,
    DECIMAL_ROUNDING,
    ArmorAggregation,
)


WORN_SLOTS = ("Head", "Body", "Gloves", "Leg", "Cape")


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
class ArmorResolution:
    items: tuple[ArmorItemEvidence, ...]
    rosters: tuple[ArmorRosterEvidence, ...]


def _text(value: object) -> str:
    return "" if value is None else str(value).strip()


def _source(row: Mapping[str, object], source_path: str, source_sha256: str, fallback: int) -> SourceRef:
    raw_number = row.get("source_row_number", fallback)
    try:
        row_number = int(str(raw_number))
    except (TypeError, ValueError):
        row_number = fallback
    return SourceRef(source_path, source_sha256, row_number, _text(row.get("item_id")))


def _item_found(value: object) -> bool:
    if value is True:
        return True
    return _text(value).lower() == "true"


def _armor_value(value: object) -> tuple[Decimal | None, str | None]:
    text = _text(value)
    if not text:
        return None, ARMOR_REGION_MISSING
    try:
        parsed = Decimal(text)
    except InvalidOperation:
        return None, ARMOR_VALUE_INVALID
    if not parsed.is_finite() or parsed < 0:
        return None, ARMOR_VALUE_INVALID
    return parsed, None


def _reason(code: str, troop_id: str, roster_index: str, item_id: str, source: SourceRef, detail: str) -> ReviewReason:
    return ReviewReason(code, "armor_item", troop_id, roster_index, item_id, source, detail)


def _quantize(value: Decimal) -> Decimal:
    return value.quantize(DECIMAL_QUANTUM, rounding=DECIMAL_ROUNDING)


def resolve_armor_evidence(
    rows: Sequence[Mapping[str, object]],
    *,
    source_path: str,
    source_sha256: str,
    aggregation: ArmorAggregation,
) -> ArmorResolution:
    """Resolve worn armor without reading shields, weapons, mounts, or skills."""
    grouped: dict[tuple[str, str], list[tuple[Mapping[str, object], SourceRef]]] = defaultdict(list)
    for fallback, row in enumerate(rows, start=2):
        source = _source(row, source_path, source_sha256, fallback)
        grouped[(_text(row.get("troop_id")), _text(row.get("roster_index")))].append((row, source))

    all_items: list[ArmorItemEvidence] = []
    rosters: list[ArmorRosterEvidence] = []
    for (troop_id, roster_index), group in sorted(grouped.items()):
        worn = [(row, source) for row, source in group if _text(row.get("slot")) in WORN_SLOTS]
        worn.sort(key=lambda pair: (_text(pair[0].get("slot")), _text(pair[0].get("item_id")), pair[1].row_number))
        alternatives: dict[str, list[ArmorItemEvidence]] = defaultdict(list)
        reasons: list[ReviewReason] = []
        source_item_ids: list[str] = []
        slot_indexes: dict[str, int] = defaultdict(int)

        for row, source in worn:
            slot = _text(row.get("slot"))
            item_id = _text(row.get("item_id"))
            alternative_index = slot_indexes[slot]
            slot_indexes[slot] += 1
            if item_id:
                source_item_ids.append(item_id)
            if not item_id:
                reasons.append(_reason(ARMOR_ITEM_ID_MISSING, troop_id, roster_index, item_id, source, f"{slot} row has no item_id"))
                continue
            if not _item_found(row.get("item_found")):
                reasons.append(_reason(ARMOR_ITEM_UNRESOLVED, troop_id, roster_index, item_id, source, "item_found is not true"))
                continue

            values: dict[str, Decimal] = {}
            invalid = False
            for field in ARMOR_FIELDS:
                parsed, code = _armor_value(row.get(field))
                if code is not None:
                    reasons.append(_reason(code, troop_id, roster_index, item_id, source, f"{field} is {'blank' if code == ARMOR_REGION_MISSING else 'invalid'}"))
                    invalid = True
                else:
                    values[field] = parsed
            if invalid:
                continue
            evidence = ArmorItemEvidence(
                troop_id, roster_index, slot, alternative_index, item_id,
                values["head_armor"], values["body_armor"], values["arm_armor"], values["leg_armor"], source,
            )
            alternatives[slot].append(evidence)
            all_items.append(evidence)

        sorted_reasons = tuple(sorted(reasons, key=lambda reason: (
            reason.item_id, reason.code, reason.source.path if reason.source else "",
            reason.source.row_number if reason.source else -1,
        )))
        if sorted_reasons:
            rosters.append(ArmorRosterEvidence(
                troop_id, roster_index, None, None, None, None, None,
                tuple(sorted(set(source_item_ids))), sorted_reasons,
            ))
            continue

        totals = {field: Decimal("0") for field in ARMOR_FIELDS}
        for slot in WORN_SLOTS:
            choices = alternatives.get(slot, [])
            if not choices:
                continue
            for field in ARMOR_FIELDS:
                totals[field] += sum((getattr(choice, field) for choice in choices), Decimal("0")) / Decimal(len(choices))
        output = (
            aggregation.head_weight * totals["head_armor"]
            + aggregation.body_weight * totals["body_armor"]
            + aggregation.arm_weight * totals["arm_armor"]
            + aggregation.leg_weight * totals["leg_armor"]
        )
        rosters.append(ArmorRosterEvidence(
            troop_id, roster_index,
            _quantize(totals["head_armor"]), _quantize(totals["body_armor"]),
            _quantize(totals["arm_armor"]), _quantize(totals["leg_armor"]),
            _quantize(output), tuple(sorted(set(source_item_ids))), (),
        ))

    return ArmorResolution(
        tuple(sorted(all_items, key=lambda item: (item.troop_id, item.roster_index, item.slot, item.alternative_index, item.item_id, item.source.row_number))),
        tuple(rosters),
    )


def resolve_armor_rosters(
    rows: Sequence[Mapping[str, object]],
    *,
    source_path: str,
    source_sha256: str,
    aggregation: ArmorAggregation,
) -> tuple[ArmorRosterEvidence, ...]:
    return resolve_armor_evidence(
        rows, source_path=source_path, source_sha256=source_sha256, aggregation=aggregation
    ).rosters
