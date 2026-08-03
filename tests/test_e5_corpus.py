"""
Tests for the E5 audit grid.

The properties that matter are the ones the harness depends on: the grid is
enumerable, query_ids are stable across processes (so recorded responses can
be matched to prompts on a later run), and the cross-product axes actually
vary the prompt.
"""

import subprocess
import sys
from datetime import date

import pytest

from agents.retail_ai import InvestorType
from e5.corpus import (
    CALM,
    CRISIS,
    DEFAULT_CONDITIONS,
    PROMPT_TEMPLATES,
    MarketCondition,
    build_corpus,
)

TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA"]
DATES = [date(2026, 8, 1), date(2026, 8, 2)]


def corpus(**kw):
    kw.setdefault("max_ticker_groups", 3)
    return build_corpus(TICKERS, DATES, **kw)


class TestGridShape:
    def test_size_is_the_cross_product(self):
        c = corpus()
        assert len(c) == len(InvestorType) * 3 * len(DEFAULT_CONDITIONS) * len(DATES)

    def test_every_axis_is_present(self):
        c = corpus()
        assert {i.archetype for i in c} == set(InvestorType)
        assert {i.condition.name for i in c} == {x.name for x in DEFAULT_CONDITIONS}
        assert {i.as_of for i in c} == set(DATES)

    def test_group_size_controls_tickers_per_prompt(self):
        assert all(len(i.tickers) == 3 for i in corpus(group_size=3))

    def test_archetype_subset_is_honored(self):
        c = corpus(archetypes=(InvestorType.MEME_TRADER,))
        assert {i.archetype for i in c} == {InvestorType.MEME_TRADER}


class TestQueryIds:
    def test_unique_across_the_grid(self):
        ids = [i.query_id for i in corpus()]
        assert len(set(ids)) == len(ids)

    def test_stable_across_processes(self):
        """Same reason as #7: a per-process hash would make recorded fixtures
        unmatchable on a later run."""
        snippet = (
            "from datetime import date;"
            "from e5.corpus import build_corpus;"
            "c=build_corpus(['AAPL','MSFT','NVDA','TSLA'],"
            "[date(2026,8,1),date(2026,8,2)],max_ticker_groups=3);"
            "print(','.join(i.query_id for i in c))"
        )
        outs = set()
        for _ in range(3):
            r = subprocess.run([sys.executable, "-c", snippet],
                               capture_output=True, text=True, timeout=60)
            assert r.returncode == 0, r.stderr
            outs.add(r.stdout.strip())
        assert len(outs) == 1

    def test_id_changes_with_each_coordinate(self):
        """A collision on any axis would silently merge two cells."""
        base = corpus()[0]
        others = corpus(archetypes=(InvestorType.MEME_TRADER,))
        assert base.query_id not in {o.query_id for o in others}


class TestPrompts:
    def test_condition_changes_the_prompt(self):
        c = corpus(archetypes=(InvestorType.PASSIVE_INDEX,))
        by_cond = {i.condition.name: i.prompt for i in c if i.as_of == DATES[0]
                   and i.tickers == ("AAPL", "MSFT")}
        assert len(set(by_cond.values())) == len(DEFAULT_CONDITIONS)

    def test_tickers_appear_in_prompt(self):
        for i in corpus():
            for t in i.tickers:
                assert t in i.prompt

    def test_every_archetype_condition_pair_has_a_template(self):
        for arch in InvestorType:
            for cond in DEFAULT_CONDITIONS:
                assert cond.name in PROMPT_TEMPLATES[arch]

    def test_query_context_matches_prompt(self):
        """The RetailQuery handed to the stub must carry the same text sent
        to a live model, or stub and live runs aren't comparable."""
        assert all(i.query.context == i.prompt for i in corpus())


class TestValidation:
    def test_empty_tickers(self):
        with pytest.raises(ValueError, match="empty ticker"):
            build_corpus([], DATES)

    def test_no_dates(self):
        with pytest.raises(ValueError, match="no dates"):
            build_corpus(TICKERS, [])

    def test_duplicate_tickers(self):
        with pytest.raises(ValueError, match="duplicate"):
            build_corpus(["AAPL", "AAPL"], DATES)

    def test_group_size_too_large(self):
        with pytest.raises(ValueError, match="exceeds universe"):
            build_corpus(TICKERS, DATES, group_size=99)

    def test_stress_out_of_range(self):
        with pytest.raises(ValueError, match=r"\[0,1\]"):
            MarketCondition("bad", 1.5)


class TestStubBaseline:
    def test_stub_response_is_fixed_per_cell(self):
        """The corpus seeds each query from its coordinates, so the stub is a
        zero-variance baseline — otherwise stub noise and a live model's
        sampling temperature are indistinguishable."""
        import numpy as np
        from agents.retail_ai import stub_llm_response

        item = corpus()[0]
        a = stub_llm_response(item.query, TICKERS)
        b = stub_llm_response(item.query, TICKERS)
        np.testing.assert_allclose(a, b)
