"""Allow `python -m gfi` to run the GitHub CLI extension entry point.

This is what the root `gh-gfi` script extension shells out to when gfi is not
installed as a console script. Keeping the logic in `__main__.py` (instead of
`python -m gfi.gh_extension`) avoids importing `gfi.gh_extension` twice, which
otherwise emits a RuntimeWarning and can run `main()` unpredictably.
"""
from gfi.gh_extension import main

if __name__ == "__main__":
    main()