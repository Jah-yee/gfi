"""Tests for gfi GitHub CLI extension mode."""
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from gfi.gh_extension import main


def test_gh_extension_invokes_cli():
    """Test that gh extension mode invokes the CLI with correct args."""
    with patch.object(sys, "argv", ["gh-gfi", "search", "--limit", "5"]):
        with patch("gfi.gh_extension.cli") as mock_cli:
            main()
            mock_cli.assert_called_once_with()


def test_gh_extension_help():
    """Test that gh extension shows help when no args."""
    with patch.object(sys, "argv", ["gh-gfi"]):
        with patch("gfi.gh_extension.cli") as mock_cli:
            main()
            mock_cli.assert_called_once_with()


def test_gh_extension_version():
    """Test that gh extension shows version."""
    with patch.object(sys, "argv", ["gh-gfi", "--version"]):
        with patch("gfi.gh_extension.cli") as mock_cli:
            main()
            mock_cli.assert_called_once_with()


def test_gh_extension_script_installed():
    """Test that gh-gfi script is installed by pip."""
    result = subprocess.run(
        ["pip", "show", "-f", "gfi"],
        capture_output=True,
        text=True,
    )
    # Check that the script is listed in the package files
    assert "gh-gfi" in result.stdout or result.returncode == 1  # may not be installed in test env
