"""Kinetic melee effectiveness engine -- faithful port of the scoring logic from
Bill Wavey's 1H Sword Grader ("Kinetic Momentum Engine v2.9").

Source & attribution: https://billwavey.github.io/sword-calc.html (Bill Wavey).
Formula extracted from the page's JavaScript on 2026-07-23 and reimplemented
from scratch (clean-room port of the functional form; no page content copied).

Design principle -- logic vs calibration:
  * The FUNCTIONAL FORM (effective damage vs armour, stagger term, reach
    collision penalty, speed/handling/weight curves, AI thrust penalty,
    skill scaling, expected-kills normalization) is ported faithfully.
  * All NUMERIC CONSTANTS live in `EngineCalibration` and default to the
    author's values, which were calibrated for AI-wielded one-handed swords
    (presumably vanilla Bannerlord). They are initial values, not ground
    truth: recalibrations must be created as NEW named calibrations, never
    by silently editing `WAVEY_V29`.

Known modeling caveats (documented, intentionally preserved in v1):
  * Armour is a flat subtraction (armour * armour_pen), which DIVERGES from
    this repo's damage model (multiplicative 100/(100+armor) curve,
    docs/methodology/001_damage_model.md). Reconciliation is a calibration
    decision, out of scope for the faithful port.
  * Weight has a POSITIVE exponent ("momentum"): heavier scores higher.
  * The thrust penalty models the AI's swing/thrust animation switching for
    one-handed swords. Confidence degrades outside that weapon class and
    likely inverts for thrust-primary polearms.
"""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class EngineCalibration:
    """All tunable constants of the engine. Defaults = Bill Wavey v2.9."""

    scale: float = 13.38
    armour_pen: float = 0.52
    dmg_curve: float = 1.50
    stagger_curve: float = 0.79
    reach_curve: float = 0.76
    speed_curve: float = 1.0
    handling_curve: float = 0.91
    weight_curve: float = 0.20
    weight_ref: float = 1.5
    thrust_penalty_base: float = 0.77
    enemy_hp: float = 100.0
    reach_soft_cap: float = 110.0
    reach_penalty_floor: float = 0.5
    armour_light: float = 15.0
    armour_heavy: float = 45.0
    max_kills_light: float = 26.0
    max_kills_heavy: float = 20.0
    level_speed_mult: float = 0.0007
    level_damage_mult: float = 0.0015
    weight_light: float = 0.3
    weight_heavy: float = 0.7

    def derive(self, **overrides: float) -> "EngineCalibration":
        """New named calibration derived from this one (explicit overrides)."""
        return replace(self, **overrides)


WAVEY_V29 = EngineCalibration()


@dataclass(frozen=True)
class WeaponProfile:
    """Melee weapon stats as shown on in-game tooltips / item XML."""

    swing_damage: float
    swing_speed: float
    handling: float
    reach: float
    weight: float
    has_thrust: bool = False
    thrust_damage: float = 0.0
    thrust_speed: float = 0.0


@dataclass(frozen=True)
class GradeResult:
    vs_light: int
    vs_heavy: int
    final: int
    tier: str
    kills_light: float
    kills_heavy: float


TIER_TABLE: tuple[tuple[int, str], ...] = (
    (86, "S+"), (82, "S"), (78, "S-"), (74, "A+"), (70, "A"), (65, "A-"),
    (60, "B+"), (55, "B"), (50, "B-"), (45, "C+"), (40, "C"), (35, "C-"),
    (25, "D"),
)


def tier_for(final_score: int) -> str:
    for threshold, tier in TIER_TABLE:
        if final_score >= threshold:
            return tier
    return "F"


def base_kills(
    weapon: WeaponProfile,
    armour: float,
    mod_speed: float,
    mod_damage: float,
    cal: EngineCalibration = WAVEY_V29,
) -> float:
    """Expected kills for an AI wielder vs a target with the given armour.

    Faithful port of `getBaseKills` from the source JS.
    """
    eff_sd = max(1.0, weapon.swing_damage * mod_damage - armour * cal.armour_pen)

    if weapon.has_thrust:
        thrust_ratio = min(
            1.0,
            (weapon.thrust_damage / weapon.swing_damage)
            * (weapon.thrust_speed / weapon.swing_speed),
        )
        thrust_mult = cal.thrust_penalty_base + (1.0 - cal.thrust_penalty_base) * thrust_ratio
    else:
        thrust_mult = 1.0

    stagger = min(1.0, eff_sd / cal.enemy_hp) ** cal.stagger_curve
    reach_penalty = max(
        cal.reach_penalty_floor,
        1.0 - max(0.0, weapon.reach - cal.reach_soft_cap) / 100.0,
    )

    return max(
        1.0,
        cal.scale
        * (eff_sd / 100.0) ** cal.dmg_curve
        * ((weapon.reach / 100.0) * reach_penalty) ** cal.reach_curve
        * (weapon.swing_speed * mod_speed / 100.0) ** cal.speed_curve
        * (weapon.handling / 100.0) ** cal.handling_curve
        * (weapon.weight / cal.weight_ref) ** cal.weight_curve
        * stagger
        * thrust_mult,
    )


def grade(
    weapon: WeaponProfile,
    skill_level: float,
    cal: EngineCalibration = WAVEY_V29,
) -> GradeResult:
    """Grade a melee weapon for an AI wielder with the given weapon skill.

    `skill_level` is the wielder's skill in the weapon's tree (0-330);
    for troops, use the troop's One Handed / Two Handed / Polearm skill.
    """
    mod_speed = 1.0 + skill_level * cal.level_speed_mult
    mod_damage = 1.0 + skill_level * cal.level_damage_mult

    kl = base_kills(weapon, cal.armour_light, mod_speed, mod_damage, cal)
    kh = base_kills(weapon, cal.armour_heavy, mod_speed, mod_damage, cal)

    vs_light = round(kl / cal.max_kills_light * 100.0)
    vs_heavy = round(kh / cal.max_kills_heavy * 100.0)
    final = round(vs_light * cal.weight_light + vs_heavy * cal.weight_heavy)

    return GradeResult(
        vs_light=vs_light,
        vs_heavy=vs_heavy,
        final=final,
        tier=tier_for(final),
        kills_light=kl,
        kills_heavy=kh,
    )
