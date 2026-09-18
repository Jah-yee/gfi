"""gfi — Good First Issue finder for GitHub contributors."""
from gfi.search import GitHubSearcher, Issue, HotTopics
from gfi.gh_extension import main as gh_extension_main

__version__ = "0.1.0"

__all__ = ["GitHubSearcher", "Issue", "HotTopics", "gh_extension_main"]
