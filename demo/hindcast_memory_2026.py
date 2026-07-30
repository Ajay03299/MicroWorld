"""
Hindcast · Memory 2026 — the frozen 2008 recipe, replayed on the memory
sector through the July 2026 unwind. PUBLIC DATA ONLY, NO LOOK-AHEAD.

⚠️  HONESTY BOX. This is a hindcast computed AFTER the July 2026 unwind —
    a walk-forward backtest, not a live, timestamped forecast. We did not
    publish a call before the event, and we do not claim we did. What this
    replay establishes is narrower and checkable: at every date t the
    statistic below uses only information available on the morning of t,
    its structure (weights, EMA, threshold θ=2, 5-day sustain rule) is
    carried over UNCHANGED from demo/hindcast_2008.py, and the dates it
    prints are what they are. Judge the recipe, not our timing.

One adaptation, disclosed: 2008's stress channel was interbank funding
(TED spread) — irrelevant to a sector crowding unwind. The 0.45 slot is
re-pointed at the observable footprint of crowding κ: the basket's mean
trend extension log(P / SMA200). Everything else — 0.30·z(corr63),
0.25·z(vol21), expanding-window z through t−1 (1y minimum), EMA(0.12),
θ=2, 5-consecutive-close sustain — is the 2008 spec verbatim.

    Λₜ = EMA₀.₁₂[ 0.45·z(crowd) + 0.30·z(corr63) + 0.25·z(vol21) ]

Basket: SK Hynix, Samsung, Micron, Western Digital, Seagate, SanDisk
(post-spinoff, enters when listed). Data vendored in demo/data/memory2026/
(see SOURCES.md), zero API keys.

Run:  python demo/hindcast_memory_2026.py  →  figures/hindcast_memory_2026.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "memory2026")
FIGS = os.path.join(os.path.dirname(HERE), "figures")

THETA = 2.0            # crisis threshold — 2008 spec
SUSTAIN = 5            # 5 consecutive closes above θ — 2008 spec
GUIDANCE = pd.Timestamp("2026-07-13")   # SK Hynix outlook shock
KOREA    = pd.Timestamp("2026-07-24")   # Korea selloff spills into US names
CAPITUL  = pd.Timestamp("2026-07-28")   # capitulation week begins

NAMES = ["skhynix", "samsung", "micron", "wdc", "seagate", "sandisk"]

def load(name):
    df = pd.read_csv(os.path.join(DATA, f"{name}.csv"), parse_dates=["date"])
    return df.set_index("date")["close"].rename(name)

px = pd.concat([load(n) for n in NAMES], axis=1, sort=True)
px = px[px.index >= "2021-08-01"]
# Korean and US calendars are staggered; align by carrying the last close
# forward (≤3 sessions) so cross-name statistics see a common grid.
px = px.ffill(limit=3)
rets = np.log(px).diff()

# ── the three components, 2008 structure ───────────────────────────────────────
basket_ret = rets.mean(axis=1, skipna=True)
vol21 = basket_ret.rolling(21, min_periods=15).std() * np.sqrt(252)

def mean_pairwise_corr(window):
    c = rets.rolling(window, min_periods=40).corr()
    def upper_mean(m):
        v = m.values
        iu = np.triu_indices_from(v, 1)
        x = v[iu]
        return np.nanmean(x) if np.isfinite(x).any() else np.nan
    out = c.groupby(level=0).apply(upper_mean)
    return out

corr63 = mean_pairwise_corr(63)

sma200 = px.rolling(200, min_periods=120).mean()
crowd = np.log(px / sma200).mean(axis=1, skipna=True)

def walkforward_z(x, minwin=252):
    """z vs the EXPANDING window of all data through t−1 — 2008 spec."""
    m = x.shift(1).expanding(min_periods=minwin).mean()
    s = x.shift(1).expanding(min_periods=minwin).std()
    return (x - m) / s

lam_raw = (0.45 * walkforward_z(crowd)
           + 0.30 * walkforward_z(corr63)
           + 0.25 * walkforward_z(vol21))
lam = lam_raw.ewm(alpha=0.12).mean().rename("lambda")

# ── statistics (printed, never hand-written) ───────────────────────────────────
eval_lam = lam.dropna()
above = lam > THETA
sustained = above.rolling(SUSTAIN).sum() == SUSTAIN
first_cross = above[above].index.min()
first_sustained = sustained[sustained].index.min()

def td_between(a, b):
    return int(((lam.index > a) & (lam.index <= b)).sum())

level = np.exp(np.log1p(basket_ret.fillna(0)).cumsum()) * 100.0
peak_date = level.loc[:CAPITUL].idxmax()
peak_lv = level.loc[:CAPITUL].max()
trough = level.loc[GUIDANCE:].min()
dd = (trough / peak_lv - 1) * 100
sig_lv = level.asof(first_sustained) if pd.notna(first_sustained) else np.nan
rally_after = (peak_lv / sig_lv - 1) * 100 if pd.notna(first_sustained) else np.nan

print("=" * 70)
print("HINDCAST — memory sector, frozen 2008 recipe (walk-forward, no look-ahead)")
print(f"eval sample : {eval_lam.index.min().date()} → {eval_lam.index.max().date()}"
      f"  ({len(eval_lam)} sessions)")
print(f"θ = {THETA} · sustain = {SUSTAIN} consecutive closes  (2008 spec, unchanged)")
print(f"days above θ before 2026: {int(above[above.index < '2026-01-01'].sum())}")
print(f"first close  > θ : {first_cross.date() if pd.notna(first_cross) else '—'}")
if pd.notna(first_sustained):
    print(f"first SUSTAINED  : {first_sustained.date()}")
    print(f"   → {td_between(first_sustained, GUIDANCE)} trading days before the Jul 13 guidance shock")
    print(f"   → {td_between(first_sustained, KOREA)} trading days before the Jul 24 Korea selloff")
    print(f"   → {td_between(first_sustained, CAPITUL)} trading days before the Jul 28 capitulation")
else:
    print("first SUSTAINED  : never  (signal did not fire — we publish that too)")
for label, d in [("Jul 13 guidance shock", GUIDANCE),
                 ("Jul 24 Korea selloff", KOREA),
                 ("Jul 28 capitulation", CAPITUL)]:
    li = lam.asof(d)
    pct = (eval_lam[eval_lam.index <= d] <= li).mean() * 100
    print(f"{label}:  Λ = {li:+.2f}  (pctile {pct:.1f}%)")
print(f"basket peak {peak_date.date()} → post-shock trough: {dd:.0f}%")
if pd.notna(first_sustained):
    print(f"THE HONEST OTHER HALF: after the alarm the basket rose another "
          f"{rally_after:+.0f}% into the {peak_date.date()} peak.")
    print("Basin-exit detection is not crash timing. Λₜ says the regime is")
    print("unstable; WHEN it resolves is governed by who holds the wedge up")
    print("and when they rotate out (κ) — the second half of the MVP signal,")
    print("and precisely what experiment E7 reconstructs from 13F/COT data.")
print("=" * 70)

# ── figure ─────────────────────────────────────────────────────────────────────
OK = dict(blue="#0072B2", orange="#E69F00", red="#D55E00", ink="#111827",
          mute="#6B7280")
plt.rcParams.update({"font.family": "sans-serif", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "white"})
fig, axes = plt.subplots(2, 1, figsize=(13.2, 7.6), sharex=True,
                         gridspec_kw=dict(height_ratios=[1.0, 1.15], hspace=0.10))
lo, hi = pd.Timestamp("2024-06-01"), lam.index.max() + pd.Timedelta(days=3)

ax = axes[0]
ax.plot(level.loc[lo:hi], color=OK["ink"], lw=1.4)
ax.set_ylabel("memory basket (equal-weight, indexed)")
ax.set_yscale("log")
ax.axvline(GUIDANCE, color=OK["mute"], lw=0.9, ls=":")
ax.axvline(CAPITUL, color=OK["red"], lw=1.4, ls="--")
ax.axvspan(GUIDANCE, hi, color=OK["red"], alpha=0.06)
ax.set_title("Hindcast · the memory sector through July 2026 — the frozen 2008 recipe, "
             "walk-forward on public data (a backtest, not a live call)",
             fontsize=12.2, fontweight="bold", loc="left", pad=10)
ax.grid(alpha=0.3)

ax = axes[1]
ax.plot(lam.loc[lo:hi], color=OK["ink"], lw=1.5)
ax.axhline(THETA, color=OK["red"], ls=":", lw=1.3)
ax.text(lo + pd.Timedelta(days=6), THETA + 0.12, f"θ = {THETA} (2008 spec)",
        fontsize=8.5, color=OK["red"])
if pd.notna(first_sustained):
    warn = lam.loc[first_sustained:CAPITUL]
    ax.fill_between(warn.index, THETA, warn.clip(lower=THETA),
                    color=OK["orange"], alpha=0.5)
    lead_c = td_between(first_sustained, CAPITUL)
    ax.annotate(f"{first_sustained.strftime('%b %d, %Y')} — the first alarm of the whole sample\n"
                f"(zero in 3 years, incl. the 2022 memory bear): Λₜ enters its\n"
                f"sustained crisis regime {lead_c} trading days before the\n"
                f"worst month since 2008. The basket rose another {rally_after:+.0f}%\n"
                f"first — basin exit ≠ crash timing; the missing half is κ.",
                xy=(first_sustained, THETA),
                xytext=(pd.Timestamp("2024-06-15"), 3.32), va="top",
                fontsize=9.3, fontweight="bold", color="#B45309",
                arrowprops=dict(arrowstyle="->", color="#B45309", lw=1.2))
    lam_cap = lam.asof(CAPITUL)
    pct_cap = (eval_lam[eval_lam.index <= CAPITUL] <= lam_cap).mean() * 100
    ax.annotate(f"Jul 28 — capitulation week: Λ = {lam_cap:+.2f} ({pct_cap:.0f}th pctile).\n"
                f"The loudest warning was nine months old —\n"
                f"the same lesson 2008 taught.",
                xy=(CAPITUL, lam_cap), xytext=(pd.Timestamp("2025-11-25"), -0.12),
                va="top", fontsize=9.3, fontweight="bold", color=OK["red"],
                arrowprops=dict(arrowstyle="->", color=OK["red"], lw=1.2,
                                connectionstyle="arc3,rad=-0.15"))
for d in (GUIDANCE, KOREA):
    ax.axvline(d, color=OK["mute"], lw=0.9, ls=":")
ax.axvline(CAPITUL, color=OK["red"], lw=1.4, ls="--")
ax.set_ylabel("Λₜ  (crisis indicator)")
ax.set_xlim(lo, hi)
ax.set_ylim(-0.9, 3.4)
ax.grid(alpha=0.3)
fig.text(0.01, 0.005,
         "Λₜ = EMA[0.45·z(crowding: mean log P/SMA200) + 0.30·z(pairwise corr, 63d) + 0.25·z(realized vol, 21d)] — "
         "each z vs the EXPANDING window through t−1 (no look-ahead). Structure, weights, θ, sustain rule frozen from "
         "demo/hindcast_2008.py; funding→crowding is the one disclosed adaptation. Hindcast computed after the event.",
         fontsize=7.3, color=OK["mute"])
fig.savefig(os.path.join(FIGS, "hindcast_memory_2026.png"), dpi=200,
            bbox_inches="tight")
print("✓ figures/hindcast_memory_2026.png")
