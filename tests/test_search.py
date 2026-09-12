"""Tests for gfi search."""
import json
from pathlib import Path

import pytest

from gfi.search import GitHubSearcher, Issue


class TestIssue:
    @pytest.fixture
    def issue(self):
        return Issue(
            number=123,
            title="Test issue",
            repo="owner/repo",
            url="https://github.com/owner/repo/issues/123",
            state="open",
            labels=["good first issue", "enhancement"],
            assignees=[],
            created_at="2026-09-01T00:00:00Z",
            updated_at="2026-09-05T00:00:00Z",
            stars=500,
            language="python",
        )

    def test_is_assigned_false(self, issue):
        assert issue.is_assigned is False

    def test_is_assigned_true(self, issue):
        issue.assignees = ["someone"]
        assert issue.is_assigned is True

    def test_created_date(self, issue):
        assert issue.created_date is not None

    def test_age_days(self, issue):
        age = issue.age_days()
        assert age is not None
        assert age > 0

    def test_age_days_none(self, issue):
        issue.created_at = ""
        assert issue.age_days() is None


class TestGitHubSearcher:
    @pytest.fixture
    def searcher(self, tmp_path):
        return GitHubSearcher(cache_dir=tmp_path / "cache")

    def test_init_creates_dir(self, searcher):
        assert searcher.cache_dir.exists()

    def test_load_seen_empty(self, searcher):
        assert len(searcher._seen) == 0

    def test_mark_seen(self, searcher):
        issue = Issue(number=1, title="test", repo="a/b", url="", state="open")
        searcher.mark_seen(issue)
        assert searcher.is_seen(issue)

    def test_filter_unseen(self, searcher):
        issues = [
            Issue(number=i, title=f"issue-{i}", repo="a/b", url="", state="open")
            for i in range(5)
        ]
        searcher.mark_seen(issues[0])
        searcher.mark_seen(issues[2])
        unseen = list(searcher.filter_unseen(iter(issues)))
        assert len(unseen) == 3


class TestSeenPersistence:
    def test_save_and_load(self, tmp_path):
        searcher1 = GitHubSearcher(cache_dir=tmp_path / "cache")
        issue = Issue(number=42, title="test", repo="x/y", url="", state="open")
        searcher1.mark_seen(issue)
        searcher2 = GitHubSearcher(cache_dir=tmp_path / "cache")
        assert searcher2.is_seen(issue)
