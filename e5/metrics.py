"""
E5 response-kernel statistics.

Given allocations R[i, j, :] — model i, repeat j, a point on the allocation
simplex over n assets — summarize the response kernel R̂(q).

Motivation (README Component 4c):

    μ_retail = (1 − h) · μ_idio + h · c_t

As AI adoption rises, retail allocations collapse onto a platform consensus
c_t. E5 measures c_t and h empirically instead of assuming them.

Why three statistics rather than one
------------------------------------
Single-number summaries conflate distinct situations that carry very
different systemic risk. Concretely, on 3 models × 8 repeats × 4 assets:

  case                          spread   effect   concentration
  unanimous, all-in one name    0.0006    0.000       0.905
  unanimous, index fund         0.0005    0.000       0.000
  all models differ             0.5854    0.913       0.094

The first two rows are indistinguishable on agreement alone — mean pairwise
cosine scores both 1.000 — yet unanimous "buy NVDA" is a crowding event and
unanimous "hold an index fund" is not. Only `concentration` separates them.

Conversely, normalized entropy of the mean allocation rates total
disagreement (0.613) *above* partial agreement (0.355), because averaging
disjoint concentrated bets yields a spread-out mean indistinguishable from
genuinely diversified advice.

A note on naming: `model_effect` measures model-specific structure, which is
the opposite of herding — it is high when platforms hold competing house
views. The quantity that maps to h is low `spread` together with high
`concentration`. See crowding_index().

See issue #8 for the full derivation and the estimators that were rejected.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

__all__ = [
    "consensus",
    "spread",
    "concentration",
    "model_effect",
    "crowding_index",
    "drift",
]


def _as_panel(R: ArrayLike) -> NDArray[np.float64]:
    """Validate and coerce to (n_models, n_repeats, n_assets)."""
    A = np.asarray(R, dtype=float)
    if A.ndim != 3:
        raise ValueError(f"expected (n_models, n_repeats, n_assets), got shape {A.shape}")
    if A.size == 0:
        raise ValueError("empty allocation panel")
    if not np.isfinite(A).all():
        raise ValueError("allocations contain NaN or inf")
    if (A < -1e-9).any():
        raise ValueError("allocations contain negative weights")
    sums = A.sum(axis=-1)
    if not np.allclose(sums, 1.0, atol=1e-6):
        raise ValueError(f"allocations must sum to 1 (got {sums.min():.4f}–{sums.max():.4f})")
    return A


def consensus(R: ArrayLike) -> NDArray[np.float64]:
    """The empirical c_t: mean allocation over all models and repeats."""
    A = _as_panel(R)
    return A.reshape(-1, A.shape[-1]).mean(axis=0)


def spread(R: ArrayLike) -> float:
    """
    Mean squared distance from the consensus — the disagreement level.

    0 means every response is identical. The maximum on the simplex is 2
    (two disjoint vertices), but that bound is loose in practice; interpret
    `spread` comparatively across queries rather than on an absolute scale.
    """
    A = _as_panel(R)
    flat = A.reshape(-1, A.shape[-1])
    return float(((flat - flat.mean(axis=0)) ** 2).sum(axis=1).mean())


def concentration(R: ArrayLike) -> float:
    """
    Normalized HHI of the consensus: 0 = equal-weight, 1 = all-in one asset.

        (Σ cᵢ² − 1/n) / (1 − 1/n)

    This is what distinguishes unanimous concentrated advice (a crowding
    event) from unanimous diversified advice (harmless).
    """
    c = consensus(R)
    n = len(c)
    if n == 1:
        return 1.0
    return float((np.square(c).sum() - 1.0 / n) / (1.0 - 1.0 / n))


def model_effect(
    R: ArrayLike,
    n_permutations: int = 1000,
    rng: np.random.Generator | None = None,
) -> tuple[float, float]:
    """
    Permutation test for model-specific structure.

    Returns (p_value, effect_size).

    The test statistic is the spread of per-model mean allocations around the
    grand mean. The null reassigns responses to models at random, destroying
    model-specific structure while preserving the marginal distribution of
    responses.

        p_value     P(null statistic >= observed), add-one corrected so it is
                    never exactly 0. Small p means models differ systematically.
        effect_size 1 - null_mean/observed, clipped at 0. Reports magnitude,
                    but is NOT interpretable on its own: under H0 the ratio
                    fluctuates around 1, so the clip makes the raw effect
                    bimodal (either exactly 0 or a large spurious value, roughly
                    coin-flip). Use p_value for the decision; effect_size only
                    to describe how large a detected difference is.

        p high -> models are interchangeable draws (one shared consensus)
        p low  -> each model has a distinct house view

    Note the statistic must be computed per model and then compared across
    models; a null that permutes labels a pooled statistic never reads is
    mathematically identical to the observation (see #8).
    """
    A = _as_panel(R)
    if A.shape[0] < 2:
        raise ValueError("model_effect needs at least 2 models")
    rng = rng or np.random.default_rng()

    def between(P: NDArray[np.float64]) -> float:
        grand = P.reshape(-1, P.shape[-1]).mean(axis=0)
        return float(((P.mean(axis=1) - grand) ** 2).sum(axis=1).mean())

    observed = between(A)
    flat = A.reshape(-1, A.shape[-1])
    draws = np.array([
        between(flat[rng.permutation(len(flat))].reshape(A.shape))
        for _ in range(n_permutations)
    ])
    p_value = float((1 + (draws >= observed).sum()) / (n_permutations + 1))
    effect = 0.0 if observed < 1e-12 else float(max(0.0, 1.0 - draws.mean() / observed))
    return p_value, effect


def crowding_index(R: ArrayLike) -> float:
    """
    The systemic-risk-relevant summary: consensus tightness × concentration.

        (1 − min(spread, 1)) · concentration

    High only when models agree AND the thing agreed on is concentrated —
    the configuration under which μ_retail deforms the mean field.
    """
    return float((1.0 - min(spread(R), 1.0)) * concentration(R))


def drift(c_prev: ArrayLike, c_next: ArrayLike) -> float:
    """
    L2 distance between consensus vectors on consecutive dates.

    Measured on a fixed prompt set, this is E5's day-to-day drift: how much
    the advice everyone receives moves, independent of how tightly models
    agree on any given day.
    """
    a = np.asarray(c_prev, dtype=float)
    b = np.asarray(c_next, dtype=float)
    if a.shape != b.shape:
        raise ValueError(f"shape mismatch: {a.shape} vs {b.shape}")
    return float(np.linalg.norm(a - b))
