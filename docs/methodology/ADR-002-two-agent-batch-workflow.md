# ADR-002: One batch, one PR, separate normalization and analysis agents

- Status: accepted
- Date: 2026-07-27

## Context

Combat evidence arrives as screenshots, archives, exports, or logs. Normalizing that evidence and interpreting it are different jobs with different failure modes.

Combining both jobs in one agent encourages premature conclusions and makes it harder to distinguish extracted facts from analytical choices. Splitting them into unrelated pull requests, however, creates handoff overhead and can lose the exact branch state, source hashes, review queue, or assumptions used by the normalizer.

The project therefore needs separation of responsibility without separation of delivery context.

## Decision

Each evidence batch uses **one branch and one draft pull request**, completed in two phases by different agents:

1. **Normalization agent** — archives provenance, creates deterministic normalized records, validates structure, and commits a complete analysis prompt.
2. **Local analysis agent** — checks out the same branch, verifies the handoff, and adds only reviewed and analytical layers.

The draft pull request is the shared work envelope. It stays open between phases and is not marked ready until both phases pass their gates.

## Phase boundary

Phase 1 ends only when all of the following exist in the repository:

- source evidence or a repository-reconstructible source package;
- source hashes and manifest;
- normalized structured records;
- normalization summary;
- structural validation report;
- explicit review queue;
- normalized artifact hashes;
- batch-specific `handoff/ANALYSIS_PROMPT.md`;
- draft PR checklist showing Phase 2 as pending.

At that point, normalized artifacts become immutable inputs to Phase 2.

## Source-storage policy

Everything required to reproduce the work must be repository-addressable.

Preferred order:

1. Git LFS for large binary evidence;
2. ordinary Git for suitably small files;
3. reconstructible chunked archive when direct binary publication is unavailable.

A chunked archive must include:

- deterministic part names;
- per-part hashes;
- expected reconstructed archive hash;
- Bash and PowerShell reconstruction commands;
- a README explaining the original filename and contents.

A local-only path is not sufficient evidence storage.

## Analysis-agent contract

The local analysis agent must:

- use the same branch and PR;
- verify the handoff hashes before analysis;
- preserve normalized files byte-for-byte;
- make corrections only through separate reviewed records;
- retain track, side, and battle-context boundaries;
- apply the 5-battle / 20-deployed display gate;
- keep insufficient-evidence rows visible rather than deleting them;
- record scripts, commands, generated tables, validation, and limitations in the repository;
- use explicit analysis-phase commits;
- update the PR description with findings and checks.

## Required batch outputs

A completed batch should contain:

```text
source manifest and reproducible source package
normalized records and normalization validation
review queue and reviewed correction layer, when needed
analysis prompt used by the local agent
analysis report and generated tables
analysis validation and artifact hashes
```

## Pull-request lifecycle

1. Normalization agent creates the branch and draft PR.
2. Normalization agent completes Phase 1 and commits the analysis prompt.
3. PR status becomes `awaiting local analysis` while remaining draft.
4. Local analysis agent checks out the same branch.
5. Local analysis agent verifies hashes and adds the analytical layer.
6. Local analysis agent updates the PR checklist and summary.
7. PR is marked ready only after Phase 2 validation.
8. One final review covers the full chain from evidence to conclusions.

## Consequences

### Benefits

- evidence and conclusions remain distinguishable;
- handoffs are executable instead of conversational;
- all agents work from the same immutable batch state;
- one PR preserves an end-to-end audit trail;
- local compute can perform heavier analysis without losing repository provenance;
- fewer abandoned follow-up branches and duplicated issue context.

### Costs

- draft PRs remain open longer;
- branch ownership must transfer cleanly between agents;
- binary evidence may require Git LFS or chunk reconstruction;
- normalized-data corrections require additive review layers rather than direct edits.

## Rejected alternatives

### One agent performs both phases

Rejected because extraction errors and interpretation choices become difficult to separate and review independently.

### Separate PR for normalization and analysis

Rejected as the default because the second PR must reconstruct the exact input state and frequently duplicates handoff context. A separate PR remains acceptable only when analysis is intentionally deferred across releases or requires changes outside the batch scope.

### Keep source files only on the normalizer's machine

Rejected because hashes alone prove identity but do not make the evidence recoverable.
