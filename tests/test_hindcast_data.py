"""
Regression tests for the vendored 2008 hindcast fixtures.

These guard against the failure in #1, where an unanchored `*.csv` rule in
.gitignore silently excluded demo/data/2008/, leaving demo/hindcast_2008.py
broken on every fresh clone while the test suite stayed green.

No network access required — everything here runs against tracked files.
"""

import os
import subprocess
import sys

import pandas as pd
import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "demo", "data", "2008")
DEMO = os.path.join(REPO, "demo", "hindcast_2008.py")
FIG = os.path.join(REPO, "figures", "hindcast_2008.png")

FRENCH = ["ff_factors_0309.csv", "ind10_0309.csv"]
FRED = ["ted.csv", "vix.csv"]


class TestFixturesTracked:
    @pytest.mark.parametrize("name", FRENCH + FRED)
    def test_exists(self, name):
        assert os.path.isfile(os.path.join(DATA, name)), f"{name} missing"

    @pytest.mark.parametrize("name", FRENCH + FRED)
    def test_tracked_by_git(self, name):
        """Directly guards #1: a file on disk but untracked is invisible to clones."""
        r = subprocess.run(
            ["git", "ls-files", "--error-unmatch", f"demo/data/2008/{name}"],
            cwd=REPO, capture_output=True,
        )
        assert r.returncode == 0, f"{name} is not tracked — check .gitignore"


class TestFrenchSchema:
    def test_dates_align(self):
        """
        hindcast_2008.py builds vol21 from ff and corr63 from ind, then combines
        them. Misaligned indices would reindex to NaN and silently degrade the
        composite rather than raising.
        """
        ff = pd.read_csv(os.path.join(DATA, FRENCH[0]))
        ind = pd.read_csv(os.path.join(DATA, FRENCH[1]))
        assert len(ff) == len(ind)
        assert (ff["date"].values == ind["date"].values).all()

    def test_required_columns(self):
        ff = pd.read_csv(os.path.join(DATA, FRENCH[0]))
        assert {"Mkt-RF", "RF"} <= set(ff.columns)
        ind = pd.read_csv(os.path.join(DATA, FRENCH[1]))
        assert len(ind.columns) == 11  # date + 10 industries

    @pytest.mark.parametrize("name", FRENCH)
    def test_no_missing_sentinels(self, name):
        """French encodes missing data as -99.99/-999; /100 would make these
        catastrophic fake returns rather than an obvious error."""
        df = pd.read_csv(os.path.join(DATA, name)).set_index("date")
        assert (df > -99.0).all().all(), f"{name} contains a missing-data sentinel"

    @pytest.mark.parametrize("name", FRENCH)
    def test_covers_crisis_window(self, name):
        d = pd.read_csv(os.path.join(DATA, name))["date"]
        assert d.min() <= 20050101, "needs pre-crisis burn-in for expanding z-score"
        assert d.max() >= 20091201


class TestDemoRuns:
    def test_exits_clean_and_reproduces_headline(self):
        """End-to-end smoke test. Restores the figure so the run is non-destructive."""
        before = open(FIG, "rb").read() if os.path.isfile(FIG) else None
        try:
            r = subprocess.run(
                [sys.executable, DEMO], cwd=REPO,
                capture_output=True, text=True, timeout=300,
            )
        finally:
            if before is not None:
                with open(FIG, "wb") as f:
                    f.write(before)

        assert r.returncode == 0, f"demo failed:\n{r.stderr}"
        assert "2007-08-16" in r.stdout, "sustained-signal date changed"
        assert "272 trading days before Lehman" in r.stdout
