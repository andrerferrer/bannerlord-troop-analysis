# ADR-002: Combat screenshot evidence storage

- **Status:** Proposed; external action pending
- **Date:** 2026-07-24
- **Scope:** Raw combat screenshots and normalized batch artifacts

## Context

The 2026-07-23 source ZIP is approximately 85 MB. It is absent from normal Git history and could not be found locally or in GitHub releases. The committed normalized Base64 bundle is corrupt and cannot reproduce its recorded SHA-256.

Durable evidence storage must preserve the source ZIP hash:

```text
00f83754687fe769fdfdea1bda0b68b4d7801c25195ff803aa1a1b35fa15d69f
```

and the per-image hashes in `screenshots_manifest.csv` after that manifest is recovered.

## Options considered

| Option | Stable retrieval | Integrity | Repository impact | Automation | Cost/privacy | Portability |
|---|---|---|---|---|---|---|
| Git LFS | Good while LFS quota/account remains active | Git object pointer plus SHA-256 manifest | Keeps binary out of normal history but affects every LFS-aware clone | Good | Quota/bandwidth may cost; visibility follows repository | Requires Git LFS |
| GitHub release asset | Good through a versioned release/tag | Must be enforced by committed SHA-256; assets are administratively replaceable | No clone/history cost | Good through `gh`/API | Usually no added cost at this size; visibility follows repository | Browser/CLI download |
| External immutable archive | Potentially best if retention and immutability are contractual | Provider checksum plus committed SHA-256 | None | Provider-dependent | May cost; can preserve privacy | Provider dependency |
| Local archive plus redundant backup | Weak without a documented backup owner/location | Strong locally with SHA-256 | None | Weak unless backup is automated | Private and low cost | Poor for collaborators |

## Decision

Recommend a **versioned GitHub release asset plus committed SHA-256/per-image manifests** when the screenshots are approved for repository-level visibility. It avoids ordinary clone/history growth, supports scripted retrieval, and is adequate for an 85 MB source ZIP.

If the screenshots must remain private, use an access-controlled immutable archive instead and commit only retrieval instructions, opaque artifact identity, and hashes.

Do not use local-only storage as the sole source. Do not use the current chunked Base64 representation as the primary distribution format.

For normalized outputs, prefer readable JSONL/CSV/JSON committed directly when recovered and reasonably sized. A compact release asset is the second choice. Chunked Base64 is only a fallback and must always be reconstructed and exact-hash verified by the repository CLI.

## Pending external action

No upload or release was performed. Completion requires:

1. recovering a ZIP whose SHA-256 exactly matches the recorded source hash;
2. confirming that its contents may be published at repository visibility;
3. explicit authorization to create the release/upload;
4. downloading the uploaded asset again and verifying the same SHA-256;
5. committing its stable retrieval command and per-image manifest.

Proposed commands, to run only after those gates:

```bash
shasum -a 256 "/path/to/Configurações 23_07_2026 17_42_29.zip"
gh release create combat-evidence-2026-07-23 \
  --repo andrerferrer/bannerlord-troop-analysis \
  --title "Combat evidence 2026-07-23" \
  --notes "Raw evidence; verify against the committed SHA-256 manifest." \
  "/path/to/Configurações 23_07_2026 17_42_29.zip"
gh release download combat-evidence-2026-07-23 \
  --repo andrerferrer/bannerlord-troop-analysis \
  --pattern "Configurações 23_07_2026 17_42_29.zip" \
  --dir /path/to/verification
shasum -a 256 "/path/to/verification/Configurações 23_07_2026 17_42_29.zip"
```

## Consequences

- Raw evidence remains outside normal Git history.
- A cryptographic manifest, not “the file opens,” is the integrity authority.
- Release deletion/replacement remains an administrative risk mitigated by the committed hash and an optional independent backup.
- Until the source archive is recovered and authorized, production image review and canonical generation remain blocked.
