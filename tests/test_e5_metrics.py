"""
Tests for E5 response-kernel statistics.

These encode the counterexamples from #8. Several assert *discrimination*
between cases rather than exact values: the point is that unanimous
concentrated advice and unanimous diversified advice must not receive the
same score, which is precisely where cosine similarity and entropy fail.
"""

import numpy as np
import pytest

from e5.metrics import (
    concentration,
    consensus,
    crowding_index,
    drift,
    model_effect,
    spread,
)

N = 4
ALL_IN = [1.0, 0.0, 0.0, 0.0]
OTHER = [0.0, 1.0, 0.0, 0.0]
THIRD = [0.0, 0.0, 1.0, 0.0]
UNIFORM = [0.25] * 4


def panel(bases, sigma=0.02, repeats=8, seed=0):
    """Build (n_models, repeats, N) with each model noisy around its base."""
    rng = np.random.default_rng(seed)
    out = []
    for b in bases:
        x = np.abs(np.array(b, float) + rng.normal(0, sigma, (repeats, N)))
        out.append(x / x.sum(1, keepdims=True))
    return np.stack(out)


class TestValidation:
    def test_rejects_wrong_ndim(self):
        with pytest.raises(ValueError, match="n_models"):
            spread(np.ones((3, N)) / N)

    def test_rejects_unnormalized(self):
        with pytest.raises(ValueError, match="sum to 1"):
            spread(np.ones((2, 2, N)))

    def test_rejects_negative(self):
        bad = np.tile([1.5, -0.5, 0.0, 0.0], (2, 2, 1))
        with pytest.raises(ValueError, match="negative"):
            spread(bad)

    def test_rejects_nan(self):
        bad = panel([ALL_IN, OTHER]).copy()
        bad[0, 0, 0] = np.nan
        with pytest.raises(ValueError, match="NaN"):
            spread(bad)


class TestConsensus:
    def test_is_a_simplex_point(self):
        c = consensus(panel([ALL_IN, OTHER, THIRD]))
        assert c.shape == (N,)
        assert (c >= 0).all()
        np.testing.assert_allclose(c.sum(), 1.0)

    def test_recovers_the_common_vector(self):
        np.testing.assert_allclose(
            consensus(panel([ALL_IN] * 3, sigma=0.0)), ALL_IN, atol=1e-9
        )


class TestSpread:
    def test_zero_when_identical(self):
        assert spread(panel([ALL_IN] * 3, sigma=0.0)) == pytest.approx(0.0, abs=1e-12)

    def test_increases_with_disagreement(self):
        assert spread(panel([ALL_IN] * 3)) < spread(panel([ALL_IN, OTHER, THIRD]))

    def test_increases_with_noise(self):
        assert spread(panel([ALL_IN] * 3, sigma=0.02)) < spread(
            panel([ALL_IN] * 3, sigma=0.40)
        )


class TestConcentration:
    def test_zero_for_equal_weight(self):
        assert concentration(panel([UNIFORM] * 3, sigma=0.0)) == pytest.approx(0.0, abs=1e-9)

    def test_one_for_all_in(self):
        assert concentration(panel([ALL_IN] * 3, sigma=0.0)) == pytest.approx(1.0, abs=1e-9)

    def test_disjoint_bets_average_out(self):
        """Three models each all-in on a different name yields a diffuse
        consensus — the case where entropy of the mean is misleading."""
        assert concentration(panel([ALL_IN, OTHER, THIRD], sigma=0.0)) < 0.2


class TestModelEffect:
    def test_calibrated_under_null(self):
        """Under H0 the p-value must be roughly uniform, not concentrated near
        0. A raw effect size fails this: the max(0, .) clip makes it bimodal."""
        ps = [
            model_effect(panel([ALL_IN] * 3, seed=s), rng=np.random.default_rng(0))[0]
            for s in range(20)
        ]
        assert sum(p < 0.05 for p in ps) <= 4, f"too many false positives: {ps}"
        assert max(ps) > 0.5, "p-values never reach the upper range"

    def test_detects_house_views(self):
        p, effect = model_effect(panel([ALL_IN, OTHER, THIRD]), rng=np.random.default_rng(0))
        assert p <= 0.01
        assert effect > 0.8

    def test_noise_alone_is_not_structure(self):
        """High noise but no house views must not register as model-specific."""
        p, _ = model_effect(
            panel([ALL_IN] * 3, sigma=0.40, repeats=64), rng=np.random.default_rng(0)
        )
        assert p > 0.05

    def test_requires_two_models(self):
        with pytest.raises(ValueError, match="at least 2"):
            model_effect(panel([ALL_IN]))

    def test_reproducible_given_seed(self):
        R = panel([ALL_IN, OTHER, THIRD])
        a = model_effect(R, n_permutations=200, rng=np.random.default_rng(3))
        b = model_effect(R, n_permutations=200, rng=np.random.default_rng(3))
        assert a == b


class TestCrowdingIndex:
    def test_separates_the_two_unanimous_cases(self):
        """THE counterexample from #8: cosine similarity scores both of these
        1.000, but only one is a crowding event."""
        assert crowding_index(panel([ALL_IN] * 3)) > 0.8
        assert crowding_index(panel([UNIFORM] * 3)) < 0.1

    def test_low_under_disagreement(self):
        assert crowding_index(panel([ALL_IN, OTHER, THIRD])) < 0.2

    def test_bounded(self):
        for bases in ([ALL_IN] * 3, [UNIFORM] * 3, [ALL_IN, OTHER, THIRD]):
            assert 0.0 <= crowding_index(panel(bases)) <= 1.0


class TestDrift:
    def test_zero_for_identical(self):
        assert drift(UNIFORM, UNIFORM) == pytest.approx(0.0)

    def test_positive_when_consensus_moves(self):
        assert drift(ALL_IN, OTHER) > 1.0

    def test_symmetric(self):
        assert drift(ALL_IN, UNIFORM) == pytest.approx(drift(UNIFORM, ALL_IN))

    def test_shape_mismatch_raises(self):
        with pytest.raises(ValueError, match="shape mismatch"):
            drift([0.5, 0.5], [0.3, 0.3, 0.4])
