# Bannerlord Troop Analysis

Data-driven troop analysis framework for Mount & Blade II: Bannerlord.

## Start here

For the complete project state, model history, current rankings, validated findings, known limitations, and exact next steps, read:

- [`docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md`](docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md)
- [`docs/handoff/NEW_CHAT_STARTER.md`](docs/handoff/NEW_CHAT_STARTER.md)

Current authoritative models:

```txt
v7.1 — general battlefield score
v7.3 — tooltip-validated throwing burst score
```

## Goal

Create an interpretable troop analysis pipeline for vanilla Bannerlord, using XML-exported game data and practical battlefield modeling.

The project should avoid shallow tier lists based only on raw stats. The target is to estimate practical combat value using:

- hits to kill
- expected kills per minute
- melee/ranged split offense
- defensive durability
- reliability and AI usability
- tier-by-tier progression analysis
- empirical battle validation

## Primary target

The main target is vanilla Bannerlord.

Realm of Thrones work is kept only as reference material because it helped develop the methodology.

## Analysis pipeline

```txt
XML export
→ normalization
→ weapon and armor extraction
→ effective damage calculation
→ HTK calculation
→ KPM calculation
→ offense / defense / reliability scoring
→ tier-by-tier rankings
→ empirical validation
```

## Current model direction

The preferred offense model is based on HTK/KPM:

```txt
HTK = effective_enemy_hp / effective_damage
KPM = attempts_per_minute × hit_chance ÷ HTK
```

For troops with both ranged and melee capability, the model separates:

```txt
melee_kpm
ranged_kpm
throwing_kpm
```

Then it blends them according to expected battlefield usage.

## Vanilla output priorities

Because vanilla has fewer troops than overhaul mods, the main output should not only be a final Top 20.

Primary outputs:

- Tier 2 rankings
- Tier 3 rankings
- Tier 4 rankings
- Tier 5 rankings
- Tier 6 rankings
- role-specific rankings
- overall rankings

Tier-by-tier analysis matters because campaign progression depends on what is strong at each upgrade stage.

## Repository layout

```txt
docs/
  handoff/
  methodology/
  vanilla/
  rot_reference/

data/
  vanilla/
  rot_reference/

analysis/
  empirical/
  item_validation/
  model_versions/

scripts/
  export/
  normalization/
  scoring/

research/
```
