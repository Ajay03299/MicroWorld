"""
Regression tests for retail AI query -> allocation determinism.

Guards #6: stub_llm_response seeded its RNG from builtin hash(), which Python
randomizes per process (PEP 456), so mu_retail was irreproducible across runs.
The determinism test therefore runs in subprocesses -- an in-process test would
have passed even with the bug.
"""

import subprocess
import sys

import numpy as np
import pytest

from agents.retail_ai import (
    InvestorType,
    RetailQuery,
    aggregate_retail_strategy,
    stable_seed,
    stub_llm_response,
)

TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA"]

SNIPPET = """
from agents.retail_ai import RetailQuery, InvestorType, stub_llm_response
T = ['AAPL', 'MSFT', 'NVDA', 'TSLA']
q = RetailQuery(InvestorType.{arch}, T, 'Should I buy the dip?', 0.5)
print(','.join(f'{{x:.10f}}' for x in stub_llm_response(q, T)))
"""


def _run(arch: str) -> str:
    r = subprocess.run(
        [sys.executable, "-c", SNIPPET.format(arch=arch)],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


class TestCrossProcessDeterminism:
    @pytest.mark.parametrize("arch", ["DIY_QUANT", "MEME_TRADER", "PASSIVE_INDEX"])
    def test_identical_across_processes(self, arch):
        """The core guard for #6. DIY_QUANT draws from the RNG, so it is the
        archetype that actually exercised the randomized-hash seed."""
        assert len({_run(arch) for _ in range(3)}) == 1


class TestStableSeed:
    def test_deterministic(self):
        assert stable_seed("buy the dip") == stable_seed("buy the dip")

    def test_salt_changes_output(self):
        assert stable_seed("x", salt=0) != stable_seed("x", salt=1)

    def test_fits_in_uint32(self):
        assert 0 <= stable_seed("anything") < 2**32


class TestSeedOverride:
    def test_explicit_seed_wins(self):
        a, b = (
            stub_llm_response(
                RetailQuery(InvestorType.DIY_QUANT, TICKERS, ctx, 0.5, seed=99),
                TICKERS,
            )
            for ctx in ("question one", "a totally different question")
        )
        np.testing.assert_allclose(a, b)

    def test_different_seeds_differ(self):
        a, b = (
            stub_llm_response(
                RetailQuery(InvestorType.DIY_QUANT, TICKERS, "same", 0.5, seed=s),
                TICKERS,
            )
            for s in (1, 2)
        )
        assert not np.allclose(a, b)

    def test_seed_defaults_to_none(self):
        assert RetailQuery(InvestorType.PASSIVE_INDEX, TICKERS, "c", 0.5).seed is None


class TestAllocationContract:
    @pytest.mark.parametrize("arch", list(InvestorType))
    def test_is_a_simplex_point(self, arch):
        """Every archetype must return a valid allocation over the full universe."""
        alloc = stub_llm_response(
            RetailQuery(arch, ["AAPL"], "Should I buy the dip?", 0.5), TICKERS
        )
        assert alloc.shape == (len(TICKERS),)
        assert (alloc >= 0).all()
        np.testing.assert_allclose(alloc.sum(), 1.0, atol=1e-9)


class TestMuRetailReproducible:
    def test_same_queries_same_mu(self):
        """The property that actually matters: mu_retail is the mean-field
        quantity behind Component 4c, so it must be reproducible."""
        qs = [
            RetailQuery(t, TICKERS, "Should I buy the dip?", 0.5)
            for t in InvestorType
        ]
        np.testing.assert_allclose(
            aggregate_retail_strategy(qs, TICKERS),
            aggregate_retail_strategy(qs, TICKERS),
        )
