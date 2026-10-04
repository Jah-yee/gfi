"""Regression test: unrecognised --language value must not return the unfiltered baseline.

GitHub silently ignores language qualifiers whose value it doesn't recognise, returning
the full unfiltered result set. A post-filter on the reported repo language closes the
gap without needing an up-front network call to validate the language name.

See: https://github.com/yunaremaia/gfi/issues/88
"""
import json
from unittest.mock import patch, MagicMock

import pytest

from gfi.search import GitHubSearcher

REPO_A = "psf/requests"   # language: Python
REPO_B = "microsoft/vscode"  # language: TypeScript

_ISSUE_A = {
    "number": 1,
    "title": "good first issue in psf/requests",
    "repository": {"nameWithOwner": REPO_A},
    "url": f"https://github.com/{REPO_A}/issues/1",
    "state": "open",
    "labels": [{"name": "good first issue"}],
    "assignees": [],
    "createdAt": "2026-09-01T00:00:00Z",
    "updatedAt": "2026-09-05T00:00:00Z",
    "body": "",
    "commentsCount": 0,
}

_ISSUE_B = {
    "number": 2,
    "title": "good first issue in microsoft/vscode",
    "repository": {"nameWithOwner": REPO_B},
    "url": f"https://github.com/{REPO_B}/issues/2",
    "state": "open",
    "labels": [{"name": "good first issue"}],
    "assignees": [],
    "createdAt": "2026-09-01T00:00:00Z",
    "updatedAt": "2026-09-05T00:00:00Z",
    "body": "",
    "commentsCount": 0,
}


def _result(returncode, stdout="", stderr=""):
    r = MagicMock()
    r.returncode = returncode
    r.stdout = stdout
    r.stderr = stderr
    return r


class FakeGh:
    """Fake gh for testing _search_global language post-filter.

    Simulates GitHub ignoring a bad language qualifier (returning all results)
    while _get_language correctly reports the real repo language, so the
    post-filter can do its job.
    """

    def __init__(self, language_map=None):
        self._langs = language_map or {REPO_A: "Python", REPO_B: "TypeScript"}
        self.call_log = []

    def __call__(self, cmd, *args, **kwargs):
        self.call_log.append(cmd)
        if cmd[:3] == ["gh", "search", "issues"]:
            # GitHub silently ignores the bad language, returns everything
            return _result(0, json.dumps([_ISSUE_A, _ISSUE_B]))
        if cmd[:2] == ["gh", "api"]:
            field_idx = cmd.index("--jq") + 1
            field = cmd[field_idx]
            # repos path is percent-encoded (e.g. psf%2Frequests), find it
            import urllib.parse
            repo_elem = next((c for c in cmd if c.startswith("repos/")), None)
            if repo_elem:
                repo = "/".join(urllib.parse.unquote(e) for e in repo_elem.split("/")[1:])
            else:
                repo = ""
            if field == ".stargazers_count":
                return _result(0, "100\n")
            if field == ".language":
                lang = self._langs.get(repo, "")
                return _result(0, f'"{lang}"\n')
        return _result(0, "")


@pytest.fixture
def searcher(tmp_path):
    return GitHubSearcher(cache_dir=tmp_path / "cache")


def _run_global(searcher, language):
    return list(searcher._search_global(
        query="good first issue",
        label="good first issue",
        state="open",
        language=language,
        stars_min=None,
        unassigned_only=True,
        created_after=None,
        limit=20,
    ))


class TestBadLanguagePostFilter:
    def test_bad_language_does_not_return_unfiltered_baseline(self, searcher):
        """A typo in --language must not return every issue unfiltered."""
        with patch("gfi.search.subprocess.run", FakeGh()):
            results = _run_global(searcher, "rustt")  # typo: should be "rust"
            # Neither repo is Rust, so neither issue should appear
            assert results == []

    def test_valid_language_returns_only_matching_repos(self, searcher):
        """A valid language that the repo doesn't have returns nothing."""
        with patch("gfi.search.subprocess.run", FakeGh()):
            results = _run_global(searcher, "Rust")
            # psf/requests is Python, not Rust
            assert results == []

    def test_matching_language_returns_issue(self, searcher):
        """A correctly-spelled language that matches the repo returns the issue."""
        with patch("gfi.search.subprocess.run", FakeGh()):
            results = _run_global(searcher, "Python")
            assert len(results) == 1
            assert results[0].repo == REPO_A
            assert results[0].language == "Python"

    def test_no_language_returns_all(self, searcher):
        """No language filter means all results are returned."""
        with patch("gfi.search.subprocess.run", FakeGh()):
            results = _run_global(searcher, None)
            assert len(results) == 2
