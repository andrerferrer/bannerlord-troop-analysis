# Realm Paladin historical evidence search

## Scope

This log records the evidence-recovery searches performed while preparing PR
#95. It distinguishes a negative result in the currently accessible sources from
proof that no old local file exists anywhere.

## Repository and pull-request history

Search terms:

```text
Realm Paladin
realm_paladin
```

Confirmed results:

- PR #71 contains the structural Captain-like near-match shortlist. It is not a
  Realm Paladin combat-evidence batch.
- Merged PR #92 contains the compatible four-battle Realm Paladin aggregate now
  pinned and copied by this consolidation.
- No dedicated Realm Paladin combat-evidence PR was found through the available
  pull-request history search.
- A recursive tree-path inspection of the pinned `main` revision found no path
  whose name contains `realm_paladin`.

GitHub code-search requests returned upstream `502` errors during this audit.
They are recorded as unavailable checks, not as evidence that no matching file
content exists.

## User File Library

The connected File Library was searched for combinations of:

```text
Realm Paladin
realm_paladin
Bannerlord Realm Paladin screenshot
Realm Paladin ZIP battle results
```

No old Realm Paladin screenshot, ZIP, normalized package, or dedicated report
was returned. The relevant result set contained only:

- the current mobile Codex screenshot documenting the dispatcher failure; and
- unrelated Bannerlord screenshots/files.

This File Library result is useful negative evidence, but it is not an exhaustive
search of every device, unuploaded local directory, deleted conversation, or
external backup.

## Current conclusion

The currently recoverable repository-addressable numeric evidence remains:

```text
4 field battles
70 deployed
159 kills
```

No additional compatible battle was found in the repository history or File
Library sources available to this audit. Therefore:

- no fifth battle is inferred;
- no remembered number is promoted into the dataset;
- Realm Paladin remains under `do_not_retest` verification hold;
- the known four-battle aggregate remains valid and auditable;
- the consolidation task remains discoverable so a later agent can retry the
  search if new sources become available.

If previously unpublished raw screenshots or a ZIP are recovered later, they
must pass the ordinary evidence-ingestion workflow before they can change these
totals.
