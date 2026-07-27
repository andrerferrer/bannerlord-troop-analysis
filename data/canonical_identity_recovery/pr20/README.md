# PR #20 canonical identity recovery

This directory preserves the exact body of historical pull request
[#20](https://github.com/andrerferrer/bannerlord-troop-analysis/pull/20) in
`SOURCE_PR_BODY.md` and the exact name-to-`troop_id` relationships published
there.

The source snapshot reports that these relationships were produced by unique exact
normalized display-name matches against audits generated from the installed game.
The attempted Base64 transport of the complete audit bundle was corrupt and the
full audit CSVs were never merged. These compact recovery tables therefore preserve
only the published exact matches; they are not substitutes for the missing
all-troop audits and must not be used for attribute or equipment joins.

## Source snapshot

| Field | Value |
|---|---|
| PR | `andrerferrer/bannerlord-troop-analysis#20` |
| Title | `Resolve canonical troop identities from local track audits` |
| Created | `2026-07-26T21:41:05Z` |
| Closed | `2026-07-26T23:10:19Z` |
| Versioned source snapshot | `SOURCE_PR_BODY.md` |
| PR body UTF-8 bytes | `6927` |
| PR body SHA-256 | `fe9090c797081893358f849d7be8b9c4711c287891f9b6a7a38a5d0423e3ae08` |

The PR recorded these installed module versions:

- Native, Sandbox, SandboxCore, and StoryMode: `v1.4.7`;
- NavalDLC (War Sails): `v1.2.7`;
- ROT-Core, ROT-Content, ROT-Map, and ROT-Dragon: `v8.1.6`.

It also recorded the missing full-audit hashes:

| Track | Reported rows | Full audit SHA-256 |
|---|---:|---|
| `vanilla` | 1,937 | `669e57b2338f90615517466dff4a1baf0b9540c02cc093124ab1c8520d363df3` |
| `realm_of_thrones` | 6,187 | `88cc5ab6c3f9a0cb0164e36a1df8a8887e6cdc900ccf7b5c718c2c522861c903` |

## Scope and gate

- `realm_of_thrones_exact_matches.csv` contains the 15 published Realm of
  Thrones relationships.
- `vanilla_exact_matches.csv` contains the published base-game relationship.
- `war_sails_exact_matches.csv` contains the published NavalDLC relationship.
  PR #20 grouped both under its generated `vanilla` audit; the recovery keeps
  the repository's existing `war_sails_official` track boundary explicit.
  `manifest.json` records both the published `source_track` and the effective
  repository `track`, including the reason for this one intentional override.
- The five Rhodok-labelled rows and the two near-miss-only rows remain
  unresolved.
- Every compact row is tagged `historical_pr_reported_exact`; this distinguishes
  the versioned historical report from a directly available complete track audit
  in machine-readable resolver output.
- A complete track audit is still required before feature joins or full
  canonical-dataset promotion.
