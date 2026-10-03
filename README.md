# gfi — Good First Issue Finder

[![CI](https://github.com/yunaremaia/gfi/actions/workflows/ci.yml/badge.svg)](https://github.com/yunaremaia/gfi/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/yunaremaia/gfi/blob/main/LICENSE)
![Stars](https://img.shields.io/github/stars/yunaremaia/gfi)

Search and filter GitHub issues for contributors. Built for autonomous workflows and humans alike.

## Install

```bash
pip install git+https://github.com/yunaremaia/gfi.git
```

Or from source:

```bash
git clone https://github.com/yunaremaia/gfi.git
cd gfi
pip install -e .
```

### GitHub CLI Extension (gh gfi)

Install gfi as a GitHub CLI extension and run it as `gh gfi`:

```bash
gh extension install yunaremaia/gfi

gh gfi search --limit 10
gh gfi trending
gh gfi feed
```

If you already have gfi installed via pip, the `gh-gfi` console script also works
on its own, without `gh`:

```bash
pip install git+https://github.com/yunaremaia/gfi.git
gh-gfi search --limit 10
```

See [gh-extensions.md](gh-extensions.md) for details.

## Features

- **Smart search**: Auto-filters by `good first issue` label
- **Seen tracking**: Tracks seen issues to avoid repetition
- **Trending mode**: Scans popular repos for new opportunities
- **JSON output**: For automation and CI integration
- **CSV output**: For spreadsheets and data pipelines
- **Rich terminal output**: Tables and panels

## Quick Start

```bash
# Search for good first issues
gfi search --language python --stars-min 100

# Search a specific repo
gfi repo anchore/grype --limit 5

# Trending issues across popular repos
gfi trending --limit 10

# Fresh feed (unseen issues only)
gfi feed --limit 20

# Open issue in browser
gfi open owner/repo 123

# Reset seen cache
gfi reset
```

## CLI Reference

### `gfi search`

Search globally for good first issues.

```bash
gfi search --language python --stars-min 100 --limit 10
gfi search --language python --stars-min 100 --csv
gfi search --repos kubernetes/kubernetes --repos microsoft/vscode
gfi search --no-assigned  # Include assigned issues
gfi search --created-after 2026-08-01  # Recent issues only
gfi search --max-age-days 30  # Issues opened in last 30 days
gfi search --repo-max-age-days 90  # Repos active in last 90 days
```

### `gfi repo REPO`

List good first issues in a specific repository.

```bash
gfi repo anchore/grype --limit 10
gfi repo yunaremaia/driftcheck --json-output
gfi repo anchore/grype --limit 5 --csv
```

### `gfi trending`

Show trending good first issues across popular repositories.

```bash
gfi trending --limit 20
gfi trending --json-output > trending.json
gfi trending --limit 10 --csv > trending.csv
```

### `gfi feed`

Show a feed of unseen good first issues. Marks issues as seen automatically.

```bash
gfi feed --limit 20
gfi feed --limit 50 --json-output
gfi feed --limit 20 --csv > feed.csv
```

### `gfi stats`

Show statistics about seen issues.

```bash
gfi stats
```

### `gfi reset`

Reset the seen issues cache. All issues become "fresh" again.

```bash
gfi reset
```

### `gfi open REPO NUMBER`

Open a GitHub issue in the browser.

```bash
gfi open yunaremaia/driftcheck 21
```

## JSON Output

All commands support `--json-output` for automation:

```bash
gfi search --limit 5 --json-output | jq '.[].title'
```

## CSV Output

The `search`, `repo`, and `trending` commands support `--csv` for spreadsheet
imports and data pipelines:

```bash
gfi search --language python --stars-min 100 --csv > issues.csv
```

`gfi feed` also supports `--csv`.

### Machine-readable output is always clean

With `--json-output` or `--csv`, **stdout carries the payload and nothing else**.
Progress spinners, status text, and "no results" messages go to stderr, so the
documented pipelines above work without any filtering:

- `--json-output` always prints a valid JSON array — an empty result set is `[]`,
  never a sentence.
- `--csv` always prints a valid table — an empty result set is just the header
  row, so readers get zero data rows rather than a parse error.

This means `gfi ... --json-output | jq` and `gfi ... --csv > out.csv` are safe to
use in cron jobs, CI steps, and pipelines without `2>/dev/null` or `grep`.

## Development

```bash
pip install -e ".[dev]"
pytest
```


If this tool is useful to you, a star helps other people find it.

## Related tools

- **[oss-contribution-finder](https://github.com/yunaremaia/oss-contribution-finder)** — find OSS projects ready to contribute to
- **[aipr](https://github.com/yunaremaia/aipr)** — pre-screen repos for AI contribution policy
- **[driftcheck](https://github.com/yunaremaia/driftcheck)** — detect version drift between docs and toolchain files
- **[tool-call-retry](https://github.com/yunaremaia/tool-call-retry)** — retry failed tool calls with backoff

Part of a family of focused, single-purpose developer tools — each one does one thing
and does it well.

## License

MIT
