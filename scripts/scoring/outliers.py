"""Single source of truth for the "S+ / spectacle outlier" concept.

Spectacle outliers are units whose *scale* puts them outside the ordinary troop
ladder (giants, mammoths, war elephants, mumakil, chariots, trolls). They are
parked in their own S+ section and excluded from the S-D ladder so they do not
crowd ordinary troop tiers. See `docs/methodology/ADR-005-spectacle-outlier-definition.md`.

Pandas-free on purpose: everything here works on plain strings / mappings so it
stays unit-testable with stdlib `unittest`. `split_spectacle_outliers` is duck
typed and accepts either a pandas DataFrame or a list-backed test frame.

This is NOT the same concept as `scripts/melee_engine/kinetic_engine.py`'s
`TIER_TABLE`, which also contains the literal string `"S+"`. That ladder maps a
0-100 kinetic score to letters (`S+` = score >= 86) and says nothing about unit
scale. Do not merge the two.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Mapping, NamedTuple, Sequence

SPECTACLE_OUTLIER_VERSION = "v2"

# --- criterion parameters (kept as named constants so the ADR can cite them) ---

# Giants / mammoths sit outside normal troop scale. v1 regex, kept byte-identical
# so previously published tiers stay reproducible.
NAME_PATTERN = r"(?i)\bgiants?\b|\bmammoths?\b|(^|_)giant(_|$)|(^|_)mammoth(_|$)"
_NAME_RE = re.compile(NAME_PATTERN)

# Realm of Thrones prose criterion: mounts whose charge damage is off-scale.
# In RoT the only mounts at/above this are `mammoth` (400) and `elephant` (350);
# the next mount down is `unicorn1` at 90, so the threshold is not near a boundary.
OUTSIZED_MOUNT_CHARGE_THRESHOLD = 200.0

# TAOM structural criterion: explicit outsized mount ids.
OUTSIZED_MOUNT_IDS = frozenset(
    {"taom_mumakil", "taom_war_elephant", "taom_chariot_a"}
)

# TAOM structural criterion: outsized units that fight on foot (no mount to test).
OUTSIZED_FOOT_TROOP_IDS = frozenset({"cave_troll"})

# Reason strings are reportable per troop and match the `spectacle_reason`
# vocabulary already used by the published role reports.
REASON_NAME = "giant/mammoth name"
REASON_MOUNT = "outsized mount"
REASON_FOOT = "outsized foot unit"


@dataclass(frozen=True)
class TroopFacts:
    """The only inputs any criterion is allowed to look at."""

    troop_id: str = ""
    troop_name: str = ""
    mount_ids: tuple[str, ...] = ()
    mount_charge_damage: float | None = None


@dataclass(frozen=True)
class Criterion:
    """One rule that can park a troop as a spectacle outlier."""

    key: str
    reason: str
    summary: str
    default_enabled: bool
    matches: Callable[[TroopFacts], bool] = field(compare=False)


class SpectacleVerdict(NamedTuple):
    """`(is_outlier, reason)` — reason is ``None`` for ordinary troops."""

    is_outlier: bool
    reason: str | None


def _matches_name(facts: TroopFacts) -> bool:
    blob = f"{facts.troop_id or ''} {facts.troop_name or ''}"
    return bool(_NAME_RE.search(blob))


def _matches_mount_charge(facts: TroopFacts) -> bool:
    charge = facts.mount_charge_damage
    if charge is None:
        return False
    try:
        value = float(charge)
    except (TypeError, ValueError):
        return False
    if value != value:  # NaN
        return False
    return value >= OUTSIZED_MOUNT_CHARGE_THRESHOLD


def _matches_mount_id(facts: TroopFacts) -> bool:
    return any(str(m).strip() in OUTSIZED_MOUNT_IDS for m in facts.mount_ids)


def _matches_foot_id(facts: TroopFacts) -> bool:
    return str(facts.troop_id or "").strip() in OUTSIZED_FOOT_TROOP_IDS


# --- the registry: add a criterion here, nowhere else -------------------------

CRITERIA: tuple[Criterion, ...] = (
    Criterion(
        key="giant_mammoth_name",
        reason=REASON_NAME,
        summary=(
            "`troop_id` or `troop_name` matches the giant/mammoth regex "
            f"`{NAME_PATTERN}`"
        ),
        default_enabled=True,
        matches=_matches_name,
    ),
    Criterion(
        key="outsized_mount_charge",
        reason=REASON_MOUNT,
        summary=(
            "any roster mount has `horse_charge_damage` >= "
            f"{OUTSIZED_MOUNT_CHARGE_THRESHOLD:g} (RoT elephants/mammoths)"
        ),
        default_enabled=False,
        matches=_matches_mount_charge,
    ),
    Criterion(
        key="outsized_mount_id",
        reason=REASON_MOUNT,
        summary=(
            "any roster mount id is in "
            + ", ".join(f"`{m}`" for m in sorted(OUTSIZED_MOUNT_IDS))
            + " (TAOM mumakil/elephant/chariot)"
        ),
        default_enabled=False,
        matches=_matches_mount_id,
    ),
    Criterion(
        key="outsized_foot_id",
        reason=REASON_FOOT,
        summary=(
            "`troop_id` is in "
            + ", ".join(f"`{t}`" for t in sorted(OUTSIZED_FOOT_TROOP_IDS))
            + " (outsized units with no mount to test)"
        ),
        default_enabled=False,
        matches=_matches_foot_id,
    ),
)

CRITERIA_BY_KEY: dict[str, Criterion] = {c.key: c for c in CRITERIA}
ALL_CRITERIA: tuple[str, ...] = tuple(c.key for c in CRITERIA)

# Default = v1 behaviour only. Extra criteria are opt-in so published scores and
# tiers stay reproducible (ADR-005).
DEFAULT_CRITERIA: tuple[str, ...] = tuple(
    c.key for c in CRITERIA if c.default_enabled
)


def resolve_criteria(criteria: Sequence[str] | None = None) -> tuple[Criterion, ...]:
    """Map criterion keys to `Criterion` objects, rejecting unknown keys."""
    keys = DEFAULT_CRITERIA if criteria is None else tuple(criteria)
    unknown = [k for k in keys if k not in CRITERIA_BY_KEY]
    if unknown:
        raise ValueError(
            f"unknown spectacle criteria: {unknown}; known: {list(ALL_CRITERIA)}"
        )
    return tuple(CRITERIA_BY_KEY[k] for k in keys)


def classify_facts(
    facts: TroopFacts, criteria: Sequence[str] | None = None
) -> SpectacleVerdict:
    """Return `(is_outlier, reason)` for the first criterion that matches."""
    for criterion in resolve_criteria(criteria):
        if criterion.matches(facts):
            return SpectacleVerdict(True, criterion.reason)
    return SpectacleVerdict(False, None)


def matched_criteria(
    facts: TroopFacts, criteria: Sequence[str] | None = None
) -> tuple[str, ...]:
    """All criterion keys that fire for `facts` (diagnostics; order = registry)."""
    return tuple(
        c.key for c in resolve_criteria(criteria) if c.matches(facts)
    )


def classify(
    troop_id: object = "",
    troop_name: object = "",
    *,
    mount_ids: Iterable[object] = (),
    mount_charge_damage: object = None,
    criteria: Sequence[str] | None = None,
) -> SpectacleVerdict:
    """Convenience wrapper over `classify_facts` for loose column values."""
    return classify_facts(
        TroopFacts(
            troop_id=str(troop_id or ""),
            troop_name=str(troop_name or ""),
            mount_ids=tuple(str(m) for m in mount_ids if m is not None),
            mount_charge_damage=(
                None if mount_charge_damage is None else mount_charge_damage
            ),
        ),
        criteria,
    )


def is_spectacle_outlier(
    troop_id: object,
    troop_name: object,
    *,
    mount_ids: Iterable[object] = (),
    mount_charge_damage: object = None,
    criteria: Sequence[str] | None = None,
) -> bool:
    """Back-compatible boolean predicate (v1 signature, v2 owner)."""
    return classify(
        troop_id,
        troop_name,
        mount_ids=mount_ids,
        mount_charge_damage=mount_charge_damage,
        criteria=criteria,
    ).is_outlier


def spectacle_reason(
    troop_id: object,
    troop_name: object,
    *,
    mount_ids: Iterable[object] = (),
    mount_charge_damage: object = None,
    criteria: Sequence[str] | None = None,
) -> str | None:
    """Reportable reason string, or `None` when the troop is ordinary."""
    return classify(
        troop_id,
        troop_name,
        mount_ids=mount_ids,
        mount_charge_damage=mount_charge_damage,
        criteria=criteria,
    ).reason


_MOUNT_ID_COLUMNS = ("mount", "mount_id", "horse_item_id")
_MOUNT_CHARGE_COLUMNS = ("horse_charge_damage", "horse_charge", "mount_charge")


def _cell(row: Any, key: str) -> Any:
    if isinstance(row, Mapping) or hasattr(row, "get"):
        return row.get(key)
    try:
        return row[key]
    except (KeyError, IndexError, TypeError):
        return None


def facts_from_row(row: Any) -> TroopFacts:
    """Build `TroopFacts` from a mapping / pandas row.

    Mount columns are optional: rows that do not carry them simply yield no
    mount facts, so the mount criteria cannot fire on them.
    """
    mount_ids = tuple(
        str(value)
        for column in _MOUNT_ID_COLUMNS
        if (value := _cell(row, column)) not in (None, "")
    )
    charge = None
    for column in _MOUNT_CHARGE_COLUMNS:
        value = _cell(row, column)
        if value not in (None, ""):
            charge = value
            break
    return TroopFacts(
        troop_id=str(_cell(row, "troop_id") or ""),
        troop_name=str(_cell(row, "troop_name") or ""),
        mount_ids=mount_ids,
        mount_charge_damage=charge,
    )


def classify_row(
    row: Any, criteria: Sequence[str] | None = None
) -> SpectacleVerdict:
    """`(is_outlier, reason)` for a scores-CSV row."""
    return classify_facts(facts_from_row(row), criteria)


def split_spectacle_outliers(
    df: Any, criteria: Sequence[str] | None = None
) -> tuple[Any, Any]:
    """Return `(standard troops, spectacle outliers)`.

    Works on a pandas DataFrame (via `.apply`) or on the list-backed test frame
    used by `tests/test_theoretical_overview.py`.
    """
    if df is None or len(df) == 0:
        return df, df

    def _flag(row: Any) -> bool:
        return classify_row(row, criteria).is_outlier

    if hasattr(df, "apply"):
        mask = df.apply(_flag, axis=1)
        return df.loc[~mask].copy(), df.loc[mask].copy()
    # List-backed test frame
    standard_rows = [r for r in df._rows if not _flag(r)]
    outlier_rows = [r for r in df._rows if _flag(r)]
    return type(df)(standard_rows), type(df)(outlier_rows)


def describe_criteria(criteria: Sequence[str] | None = None) -> list[str]:
    """One markdown bullet per active criterion (for generated banners/docs)."""
    return [
        f"`{c.key}` → `{c.reason}`: {c.summary}"
        for c in resolve_criteria(criteria)
    ]
