# GitHub CLI Extension: Install `gh gfi`

You can use `gfi` as a [GitHub CLI extension](https://cli.github.com/manual/gh) so it lives alongside your other `gh` commands — type `gh gfi` instead of `gfi` directly.

## Install

From the upstream repository:

```bash
gh extension install yunaremaia/gfi
```

Once installed, the same commands are available under the `gh` namespace:

```bash
gh gfi search --limit 3
gh gfi --help
```

## Uninstall

```bash
gh extension uninstall gfi
```

## Local development install

If you cloned the repo and want to test the extension locally before pushing:

```bash
cd /path/to/gfi
gh extension install .
```

This points `gh gfi` at your working tree, so changes to `src/gfi/cli.py` are picked up on the next invocation (no reinstall needed).

## How it works

gfi ships two entry points, and they do different jobs.

**`gh-gfi` in the repository root** is the extension itself. `gh extension install`
clones this repository and looks for an executable named `gh-<name>` in the root,
so the root `gh-gfi` script is what makes `gh gfi` work. It prefers an installed
`gfi` console script and otherwise runs the module straight from the checkout:

```bash
# installed: delegate to the console script
exec gfi "$@"
# otherwise: run from this checkout
PYTHONPATH="$SCRIPT_DIR/src" python3 -m gfi "$@"
```

Without that root script the extension installs but every invocation fails with
`fork/exec .../gh-gfi: no such file or directory`.

**`gh-gfi` in `pyproject.toml`** is the console script pip installs, which is
what lets `gfi` (and `gh-gfi`) run without `gh` at all:

```toml
[project.scripts]
gfi = "gfi.cli:cli"
gh-gfi = "gfi.gh_extension:main"
```

Both entry points call the same `gfi.gh_extension:main`, so `gh gfi` and `gfi`
accept the same flags and behave identically.

## Pattern reference: `aipr`

This follows the same pattern as [`yunaremaia/aipr`](https://github.com/yunaremaia/aipr), which ships as `gh aipr`. See commit [df67b96](https://github.com/yunaremaia/aipr/commit/df67b96) ("feat: add GitHub CLI extension wrapper (gh aipr)") for the canonical implementation.

Both projects share the same author and the same extension-discovery convention, so once you've installed one, the other feels familiar.
