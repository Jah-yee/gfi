# gfi — Good First Issue Finder

Search and filter GitHub issues for contributors. Built for autonomous workflows and humans alike.

## Install

```bash
pip install -e .
```

## Usage

```bash
# Search globally
gfi search --language python --stars-min 100 --limit 10

# Search a specific repo
gfi repo anchore/grype --limit 5

# Trending issues across popular repos
gfi trending --limit 10

# Fresh feed of unseen issues
gfi feed --limit 20

# JSON output
gfi search --json-output > issues.json

# Open issue in browser
gfi open owner/repo 123
```

## Why

Tools like `gh search` are powerful but verbose. `gfi` focuses on the contributor workflow:

- Auto-filters by `good first issue` label
- Tracks seen issues to avoid repetition
- Trending mode scans popular repos
- JSON output for automation

## License

MIT
