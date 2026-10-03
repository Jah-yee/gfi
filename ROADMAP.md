# Roadmap — gfi

## How to read this

- **Shipping now** — see the [open issues](https://github.com/yunaremaia/gfi/issues)
  and the [CHANGELOG](https://github.com/yunaremaia/gfi/blob/main/CHANGELOG.md).
  Those are real, scoped, and have acceptance criteria.
- **Proposed work** — collected below. Ideas that were filed but never
  prioritised. They are *not* commitments. Open an issue or a PR to move one
  into the shipping column; first PR naming a roadmap entry gets review
  attention.

## Proposed work

Consolidated from the 25 issues closed in the 2026-10-02 backlog triage — all
25 were closed on that single day. Entries whose work is already present in
`main` are not repeated here; they are listed under "Already on `main`" instead.
The original discussion stays reachable on each issue number.

### Features & CI

- [gfi] Add GitHub Actions for automated release to PyPI (was #33)

### CLI & UX

- [good-first-issue] Add label filter presets and search history (was #23)
- feat: add configuration file support (was #25)

### Integrations

- docs: add API reference documentation (was #26)
- feat: replace gh CLI dependency with direct GitHub API calls (was #38)
- feat: add webhook-based real-time notifications for new good-first-issue
  opportunities (was #60; still tracked by open #61)

### Export & output formats

- [gfi] Add SARIF 2.1.0 output format for CI integration (was #37)

### Performance & scalability

- feature: add TTL-based cache for GitHub API responses (was #40)
- feat: add rate-limit-aware search with retry and backoff for multi-repo
  queries (was #47; duplicated by #63)

### Documentation

- [gfi] docs: add output format comparison and examples to README (was #22)
- [gfi] docs: add usage examples and search query reference (was #18)
- [gfi] docs: add SECURITY.md with security policies and reporting procedures
  (was #21)

## Already on `main` (not proposed work)

These came from the same triage batch, but the work is already merged. They are
recorded here so the list above stays a list of things that still need doing.

- CI workflow gating on pull requests — `.github/workflows/ci.yml` (was #11;
  delivered by #10, in the #15 commit `cffceeb`)
- `CONTRIBUTING.md` with development setup and contribution guidelines (was
  #28; delivered by #15)
- `FUNDING.yml` for GitHub Sponsors (was #19)
- `CHANGELOG.md` tracking releases and changes (was #16)
- `.github/CODE_OF_CONDUCT.md` with community standards (was #35)
- GitHub CLI extension `gh gfi` — `src/gfi/gh_extension.py` (was #2; delivered
  by #31)
- `--version` flag (was #24)
- Unit tests for issue search and filtering — `tests/test_search.py` (was #27,
  #29; original request #17)
- Persistent seen-issue tracking and deterministic result ordering (was #42;
  #44 closed as completed)

## Dropped

- `[gfi] Resolve merge conflicts on open PRs #8 and #9` (was #32) — removed as
  stale bookkeeping. PR #9 does not exist and PR #8 is closed unmerged, so
  there is no conflict left to resolve.
- `chore: consolidate duplicate seen-issue tracking issues (#42, #44) into
  single design issue` (was #58) — removed as a meta-chore about the triage
  batch itself, not a unit of project work.
