# Vanilla Tier-by-Tier Analysis

## Why tier-by-tier matters

Vanilla Bannerlord has fewer troops than overhaul mods, so it is practical to compare troops at each tier.

This is often more useful than only ranking terminal troops.

Campaign decisions usually look like:

```txt
What should I recruit or upgrade into right now?
```

not only:

```txt
What is the best final unit in the game?
```

## Planned outputs

Generate rankings for:

```txt
Tier 2
Tier 3
Tier 4
Tier 5
Tier 6
```

For each tier, produce:

```txt
Overall ranking
Infantry ranking
Cavalry ranking
Archer ranking
Crossbow ranking
Horse archer ranking
```

## Simplified vanilla categories

Use a small taxonomy.

```txt
Infantry Offensive
Infantry Defensive
Cavalry Offensive
Cavalry Defensive
Archer
Crossbow
Horse Archer
```

Avoid excessive categorization unless the data shows it is needed.

## Suggested columns

Each tier output should include:

```txt
troop_id
name
culture
tier
class
total_score
offense_score
defense_score
reliability_score
melee_kpm
ranged_kpm
throwing_kpm
primary_mode
standard_htk
heavy_htk
shield
mount
notes
```

## Interpretation

A high tier troop should not automatically win against lower tier troops.

The analysis should make it possible to identify:

- high-value low-tier troops
- weak upgrade traps
- strong midgame units
- elite units that are not worth the cost
- faction-specific progression strengths

## Future campaign-value model

Add cost and wage later.

Possible formula:

```txt
campaign_value = total_score / wage
```

But only after combat score is stable.
