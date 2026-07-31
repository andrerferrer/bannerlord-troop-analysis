# Human input required

Agent can keep shipping theoretical overviews and gates without these.
The items below are blocked on Andre (or new PC exports / battles).

## Blockers

1. **TAOM item XML export** — current zip has almost no TAOM `Item`/`CraftedItem`
   definitions, so melee/armor overview is hollow (2243 allowlisted IDs).
   Need a new export that includes TAOM item modules/files.
2. **RoT field empiria to display gate** — need ≥5 independent field battles
   and ≥20 deployed for the priority S-tier set (Ravens, Goldenheart, Myrish,
   Celtigar, Lyseni Enforcer, Mahout, Sarnori Spider, Hammerknight).
   Current follow-up is only 2 battles / 0 reliable rows.
3. **NS empiria expansion (optional)** — 7 reliable rows exist; more battles
   improve intervals and cover naval/marine lines if those are the goal.
4. **V4.4 / exact-item profiles** — dedicated model-change PR + profiles;
   not required for role_scores_v1 overview.

## Not blocked (agent can do)

- Refresh filtered `OVERVIEW.md` after audit/score rebuilds
- Unknown-item gate / catalog maintenance when XML is present
- NS theory↔field join notes when names match reliable empiria rows
