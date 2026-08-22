# D4 acquisition request — exact weapon evidence

## Status

D4 is blocked before implementation may normalize weapon attack components.
The repository contains identity manifests but not the XML bodies they identify,
and this machine has no matching source package or Bannerlord module root.
Equipment-audit scalar swing/thrust cells are intentionally insufficient and
must not be substituted.

## Required raw source package

Provide the source ZIP with SHA-256:

```text
307d9eab533b1b83bb76545141226f86144af6712ed0b64b29e3efc3e23f3ad8
```

or an extracted module root whose every consumed XML byte verifies against all
four committed manifests:

| Track | Files | manifest.csv SHA-256 | manifest_modules.csv SHA-256 |
|---|---:|---|---|
| vanilla | 3,380 | `4580c757629a314a1064cd3201571ceabcb0e2f55d7bc7e302b38e45fc00381d` | `67140067424f0ada0b90e8725d29695ec68041f97845a55872ace96e9550d4ab` |
| nightmare_sails | 3,432 | `d0734fb7ca60c5a239c9c975065177ddc97f67fd50420664dd2f9f668326139f` | `303317e380a0b16bc818938163684668e1ac3374645ee0043bde37b7e8cde500` |
| realm_of_thrones | 3,525 | `0548bac357940d79eb04619af8bd8913c535c36d41ba4a4b7ce4b02d5daf0b69` | `939cd3f7a73db039538c551af10b9085bfcfc4d01ebe894a5b33cd183cc9887b` |
| taom | 3,718 | `2f30a1e5f37142a45ac130cffcb884ddbbc60cf9053f36cdba7528eb53b83307` | `354d6841d2735b26a4e54e759323200e5b7bade0a322bb9ea62b3d9eb5c45c48` |

Load order must match each committed `data/<track>/raw_xml/manifest_modules.csv`.
The highest verified module definition wins; duplicate definitions inside that
winning module remain a hard failure.

## Required crafted-weapon inputs

For every track, provide repository-addressable files with the contracts in
`docs/handoff/PC_CRAFTING_PIECES_EXPORT_PROMPT.md`:

- `<track>_crafting_piece_stats_catalog.csv`;
- `<track>_crafting_template_stats_catalog.csv`;
- per-item tooltip observations containing `item_id`,
  `observed_swing_damage`, and `observed_thrust_damage`.

Current crafted evidence needing the gate:

| Track | Unique crafted items | Equipment occurrences |
|---|---:|---:|
| vanilla | 308 | 3,619 |
| nightmare_sails | 370 | 3,723 |
| realm_of_thrones | 409 | 9,648 |
| taom | 545 | 6,663 |

The unchanged `reconstruct_crafted_weapon_stats.py` must generate and hash-pin
`<track>_crafted_weapon_stats.csv`. D4 then produces the validation receipt and
shared-schema crafted attack rows. Missing observations stay blank; an empty
passing receipt is forbidden.

## Resume command after acquisition

First verify the source ZIP hash or every XML against the committed manifests.
Then resume Step 4 from `plan/context-first-scoring-rework/execution-plan.md`,
using the two-agent evidence-batch workflow in `AGENTS.md` if the acquired files
are committed as a new evidence batch.
