"""Tests that machine-readable output stays machine-readable.

`--json-output` and `--csv` are the automation surface of this tool. A consumer
piping stdout into `jq`, a CSV reader, or a file must never receive a progress
spinner or a human-readable sentence: one stray byte makes the whole payload
unparseable. Progress and prose belong on stderr; stdout carries the payload
and nothing else.

The empty-result case matters as much as the populated one, because "no
matches" is the most common outcome in practice and is exactly when a caller
most needs a well-formed empty document rather than a sentence.
"""
import csv
import io
import json

import pytest
from click.testing import CliRunner

from gfi.cli import CSV_COLUMNS, cli
from gfi.search import Issue


def invoke(args):
    """Invoke the CLI and return (stdout, stderr) as separate streams.

    Click 8.1 exposes ``mix_stderr``; Click 8.2 removed it and always separates
    the streams. Support both so the suite passes on CI's floor (``click>=8.1``)
    and on a current interpreter.
    """
    try:
        runner = CliRunner(mix_stderr=False)
    except TypeError:  # Click >= 8.2: streams are always separate.
        runner = CliRunner()
    result = runner.invoke(cli, args)
    assert result.exit_code == 0, result.output
    return result.stdout, result.stderr


def make_fake_searcher(monkeypatch, issues):
    """Install a searcher stub that returns `issues` without touching gh."""
    class FakeSearcher:
        def __init__(self):
            self.marked = []

        def search(self, **kwargs):
            return iter(list(issues))

        def is_seen(self, issue):
            return False

        def _seen_key(self, issue):
            return issue.url or f"{issue.repo}#{issue.number}"

        def sort_deterministicly(self, issues):
            return sorted(
                issues,
                key=lambda i: (i.stars, i.created_at or ""),
                reverse=True,
            )

        def mark_seen(self, issue):
            self.marked.append(issue)

        _seen = {}

    monkeypatch.setattr("gfi.cli.GitHubSearcher", FakeSearcher)
    return FakeSearcher


@pytest.fixture
def populated():
    return [
        Issue(
            number=1,
            title="Parser handles commas, \"quotes\", and\nnewlines",
            repo="owner/project",
            url="https://github.com/owner/project/issues/1",
            state="open",
            labels=["good first issue"],
            created_at="2026-09-01T12:30:00Z",
            stars=42,
            comments=3,
        ),
    ]


# (command argv, distinctive word in that command's empty-result message)
COMMANDS = [
    (["search"], "No issues found"),
    (["repo", "owner/project"], "No good first issues found"),
    (["trending"], "No trending issues found"),
    (["feed"], "No new issues"),
]


class TestJsonOutputIsPureJson:
    """stdout must be exactly one parseable JSON document."""

    @pytest.mark.parametrize("args,message", COMMANDS)
    def test_populated_results_parse(self, monkeypatch, populated, args, message):
        make_fake_searcher(monkeypatch, populated)

        stdout, _ = invoke([*args, "--json-output"])

        parsed = json.loads(stdout)
        assert isinstance(parsed, list)
        assert parsed, f"{args} produced an empty payload despite one issue"

    @pytest.mark.parametrize("args,message", COMMANDS)
    def test_empty_results_are_an_empty_array(self, monkeypatch, args, message):
        make_fake_searcher(monkeypatch, [])

        stdout, _ = invoke([*args, "--json-output"])

        assert json.loads(stdout) == []

    @pytest.mark.parametrize("args,message", COMMANDS)
    def test_empty_message_is_not_on_stdout(self, monkeypatch, args, message):
        make_fake_searcher(monkeypatch, [])

        stdout, stderr = invoke([*args, "--json-output"])

        assert message not in stdout
        assert message in stderr


class TestCsvOutputIsPureCsv:
    """stdout must be exactly one parseable CSV table."""

    @pytest.mark.parametrize("args,message", COMMANDS)
    def test_populated_results_parse(self, monkeypatch, populated, args, message):
        make_fake_searcher(monkeypatch, populated)

        stdout, _ = invoke([*args, "--csv"])

        rows = list(csv.reader(io.StringIO(stdout)))
        assert rows[0] == list(CSV_COLUMNS)
        assert len(rows) > 1

    @pytest.mark.parametrize("args,message", COMMANDS)
    def test_empty_results_are_header_only(self, monkeypatch, args, message):
        make_fake_searcher(monkeypatch, [])

        stdout, _ = invoke([*args, "--csv"])

        rows = list(csv.reader(io.StringIO(stdout)))
        assert rows == [list(CSV_COLUMNS)]

    @pytest.mark.parametrize("args,message", COMMANDS)
    def test_empty_message_is_not_on_stdout(self, monkeypatch, args, message):
        make_fake_searcher(monkeypatch, [])

        stdout, stderr = invoke([*args, "--csv"])

        assert message not in stdout
        assert message in stderr


class TestHumanOutputUnchanged:
    """Without a machine flag, the human-facing path keeps printing to stdout."""

    @pytest.mark.parametrize("args,message", COMMANDS)
    def test_message_still_on_stdout(self, monkeypatch, args, message):
        make_fake_searcher(monkeypatch, [])

        stdout, _ = invoke(args)

        assert message in stdout

    def test_populated_table_still_on_stdout(self, monkeypatch, populated):
        make_fake_searcher(monkeypatch, populated)

        stdout, _ = invoke(["search"])

        assert "Found 1 issues" in stdout
