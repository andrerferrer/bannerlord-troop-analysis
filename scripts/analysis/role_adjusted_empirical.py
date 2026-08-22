#!/usr/bin/env python3
"""Small, role-aware helpers for empirical Bannerlord combat evaluation.

The functions in this module deliberately keep three questions separate:

* army offensive contribution (kill share versus deployment share),
* combat retention (survivors versus deployed), and
* a role-local percentile blend when enough reliable peers exist.

No function infers damage absorbed, aggro, support credit, or counterfactual kills.
"""

from __future__ import annotations

import math
from collections.abc import Iterable

ROLE_RANGED = "ranged"
ROLE_FRONTLINE_INFANTRY = "frontline_infantry"
ROLE_MELEE_CAVALRY = "melee_cavalry"
SUPPORTED_ROLES = frozenset(
    {ROLE_RANGED, ROLE_FRONTLINE_INFANTRY, ROLE_MELEE_CAVALRY}
)
MINIMUM_ROLE_ROWS = 5


def _finite(value: int | float, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric, not boolean")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _non_negative(value: int | float, name: str) -> float:
    number = _finite(value, name)
    if number < 0:
        raise ValueError(f"{name} must be non-negative")
    return number


def deployment_share(troop_deployed: int, player_side_deployed: int) -> float:
    """Return the troop's share of all directly verified side deployments."""
    troop = _non_negative(troop_deployed, "troop_deployed")
    side = _non_negative(player_side_deployed, "player_side_deployed")
    if side <= 0:
        raise ValueError("player_side_deployed must be positive")
    if troop > side:
        raise ValueError("troop_deployed cannot exceed player_side_deployed")
    return troop / side


def offensive_contribution_ratio(
    player_side_kill_share: float,
    player_side_deployment_share: float,
) -> float:
    """Return kill share divided by deployment share.

    Values above 1 mean the troop produced more kills than its manpower share;
    values below 1 mean it produced less. This is an offensive composition
    diagnostic, not a support or defensive score.
    """
    kill_share = _non_negative(player_side_kill_share, "player_side_kill_share")
    deployed_share = _non_negative(
        player_side_deployment_share, "player_side_deployment_share"
    )
    if kill_share > 1:
        raise ValueError("player_side_kill_share cannot exceed 1")
    if deployed_share <= 0 or deployed_share > 1:
        raise ValueError("player_side_deployment_share must be in (0, 1]")
    return kill_share / deployed_share


def offensive_share_gap(
    player_side_kill_share: float,
    player_side_deployment_share: float,
) -> float:
    """Return kill share minus deployment share as a proportion."""
    kill_share = _non_negative(player_side_kill_share, "player_side_kill_share")
    deployed_share = _non_negative(
        player_side_deployment_share, "player_side_deployment_share"
    )
    if kill_share > 1 or deployed_share > 1:
        raise ValueError("shares cannot exceed 1")
    return kill_share - deployed_share


def retention_rate(
    deployed: int,
    deaths: int,
    wounded: int,
) -> float:
    """Return survivors/deployed, treating dead and wounded as combat losses.

    Routed remains a separate field under the repository combat schema.
    """
    total = _non_negative(deployed, "deployed")
    dead = _non_negative(deaths, "deaths")
    hurt = _non_negative(wounded, "wounded")
    if total <= 0:
        raise ValueError("deployed must be positive")
    if dead + hurt > total:
        raise ValueError("deaths plus wounded cannot exceed deployed")
    return (total - dead - hurt) / total


def role_from_default_group(default_group: str, context: str) -> str:
    """Map the versioned troop group into a role-local empirical bucket."""
    group = default_group.strip().lower()
    normalized_context = context.strip().lower()
    if normalized_context not in {"field", "siege_attack", "siege_defense"}:
        raise ValueError(f"unsupported battle context: {context}")
    if group in {"ranged", "horsearcher", "horse_archer"}:
        return ROLE_RANGED
    if group == "infantry":
        return ROLE_FRONTLINE_INFANTRY
    if group == "cavalry":
        return (
            ROLE_FRONTLINE_INFANTRY
            if normalized_context == "siege_defense"
            else ROLE_MELEE_CAVALRY
        )
    raise ValueError(f"unsupported default group: {default_group}")


def midrank_percentile(
    value: float,
    peer_values: Iterable[float],
    minimum_rows: int = MINIMUM_ROLE_ROWS,
) -> float | None:
    """Return a 0-100 midrank percentile or None below the role-row gate."""
    values = [_finite(item, "peer value") for item in peer_values]
    if minimum_rows < 2:
        raise ValueError("minimum_rows must be at least 2")
    if len(values) < minimum_rows:
        return None
    current = _finite(value, "value")
    lower = sum(item < current for item in values)
    equal = sum(item == current for item in values)
    if equal == 0:
        raise ValueError("value must be present in peer_values")
    return 100.0 * (lower + 0.5 * (equal - 1)) / (len(values) - 1)


def role_adjusted_score(
    offense_percentile: float | None,
    defense_percentile: float | None,
    role: str,
) -> float | None:
    """Blend role-local percentiles with one dominant 2:1 role weight.

    Frontline infantry and melee cavalry weight defense twice. Ranged troops
    weight offense twice. The result is meaningful only inside the same track,
    context, and role bucket.
    """
    if offense_percentile is None or defense_percentile is None:
        return None
    if role not in SUPPORTED_ROLES:
        raise ValueError(f"unsupported role: {role}")
    offense = _finite(offense_percentile, "offense_percentile")
    defense = _finite(defense_percentile, "defense_percentile")
    if not 0 <= offense <= 100 or not 0 <= defense <= 100:
        raise ValueError("percentiles must be in [0, 100]")
    if role == ROLE_RANGED:
        return (2 * offense + defense) / 3
    return (offense + 2 * defense) / 3
