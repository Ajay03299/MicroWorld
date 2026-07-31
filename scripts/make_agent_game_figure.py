"""
figures/agent_game_inference.png — the MVP's second figure.

A journal-style (Nature/NeurIPS conventions) three-panel schematic of how
the fully connected agent network infers the July 2026 memory unwind:

  (a) the agent interaction graph — every agent-neuron coupled to every
      other (faint), with the five PRINCIPAL couplings highlighted, PCA-
      loading style: the handful of edges that carry the prediction;
  (b) the loadings themselves — each principal coupling's share of the
      predicted behavioral-wedge variance;
  (c) the inferred unwind mechanism — the state trajectories (κ, f, w)
      those couplings generate, with the 2026 event dates marked.

Synthetic scenario, schematic couplings: the Phase-1 mean-field
simplification of the fully connected network (NNGS). US market only.

Run:  python scripts/make_agent_game_figure.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, RegularPolygon
import matplotlib.dates as mdates
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(os.path.dirname(HERE), "figures")

# ── journal conventions ────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 7, "axes.labelsize": 7, "axes.titlesize": 7,
    "xtick.labelsize": 6.2, "ytick.labelsize": 6.2,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.2, "ytick.major.size": 2.2,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white",
})
INK, MUTE = "#1A1A1A", "#8A8F98"
C_INFO, C_INST, C_RET = "#D55E00", "#0072B2", "#56B4E9"
C_MM, C_FIELD, C_SELL = "#E69F00", "#009E73", "#CC79A7"

fig = plt.figure(figsize=(7.1, 2.95), dpi=300)
gs = fig.add_gridspec(1, 3, width_ratios=[0.40, 0.21, 0.39],
                      left=0.015, right=0.985, top=0.86, bottom=0.15,
                      wspace=0.34)

# ══ (a) agent interaction graph ═══════════════════════════════════════════════
ax = fig.add_subplot(gs[0]); ax.set_xlim(-1.28, 1.28); ax.set_ylim(-1.22, 1.22)
ax.axis("off"); ax.set_aspect("equal")

AG = {   # name: (angle°, color, two-line label)
    "info":   (108, C_INFO, "supply-chain\nsignal"),
    "sell":   (155, C_SELL, "sell-side\nresearch"),
    "quant":  (207, C_INST, "quant\nfunds"),
    "multi":  (258, C_INST, "multi-strat\nHFs"),
    "index":  (308, C_INST, "long-only\n/ index"),
    "mm":     (355, C_MM,   "market\nmakers"),
    "pb":     (45,  C_MM,   "prime\nbrokers"),
    "retail": (72,  C_RET,  "retail cohort\n(LLM-fed)"),
}
R = 0.92
P = {k: (R * np.cos(np.deg2rad(a)), R * np.sin(np.deg2rad(a)))
     for k, (a, _, _) in AG.items()}
P["field"] = (0.0, 0.0)

# faint full connectivity (the network is fully connected; these edges exist)
keys = list(AG.keys())
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        x1, y1 = P[keys[i]]; x2, y2 = P[keys[j]]
        ax.plot([x1, x2], [y1, y2], color="#B9BEC7", lw=0.35, alpha=0.35,
                zorder=1)
for k in keys:
    ax.plot([P[k][0], 0], [P[k][1], 0], color="#B9BEC7", lw=0.35, alpha=0.35,
            zorder=1)

# principal couplings, PCA-loading style
PRINCIPAL = [   # (src, dst, w, color, rad)
    ("info",   "quant",  0.34, C_INFO, 0.18),
    ("quant",  "field",  0.27, C_INST, 0.10),
    ("field",  "retail", 0.19, C_RET,  0.22),
    ("retail", "field",  0.12, C_RET, -0.16),
    ("mm",     "field",  0.08, C_MM,   0.14),
]
for s, d, w, c, rad in PRINCIPAL:
    ax.add_patch(FancyArrowPatch(P[s], P[d],
                 connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                 mutation_scale=6, lw=0.8 + 7.5 * w, color=c, alpha=0.92,
                 shrinkA=7, shrinkB=9, zorder=3))
lab_off = {("info", "quant"): (-0.56, -0.10), ("quant", "field"): (-0.44, -0.32),
           ("field", "retail"): (0.42, 0.44), ("retail", "field"): (0.10, 0.42),
           ("mm", "field"): (0.62, -0.16)}
for n, (s, d, w, c, _) in enumerate(PRINCIPAL, 1):
    x, y = lab_off[(s, d)]
    ax.text(x, y, f"$w_{n}$", fontsize=6.4, color=c, ha="center",
            va="center", fontweight="bold", zorder=6)

# nodes: agents are small networks — draw as double circle (body + core)
lab_pos = {"mm": (0.80, -0.38)}          # keep inside the panel, off panel b
for k, (a, c, lab) in AG.items():
    x, y = P[k]
    ax.add_patch(Circle((x, y), 0.115, facecolor="white", edgecolor=c,
                        lw=1.0, zorder=4))
    ax.add_patch(Circle((x, y), 0.052, facecolor=c, edgecolor="none",
                        alpha=0.9, zorder=5))
    lx, ly = lab_pos.get(k, (x * 1.335, y * 1.335))
    ax.text(lx, ly, lab, fontsize=5.8, color=INK, ha="center", va="center",
            zorder=6, linespacing=1.15)
# the mean field at the center
ax.add_patch(RegularPolygon((0, 0), 6, radius=0.155, orientation=np.pi / 6,
             facecolor="#E7F0EA", edgecolor=C_FIELD, lw=1.1, zorder=4))
ax.text(0, -0.005, "price\nfield", fontsize=5.8, color=C_FIELD, ha="center",
        va="center", fontweight="bold", zorder=5, linespacing=1.1)

# ══ (b) principal-coupling loadings ═══════════════════════════════════════════
ax = fig.add_subplot(gs[1])
names = [r"$w_1$  info $\to$ quant" + "\n(asymmetry entry)",
         r"$w_2$  quant $\to$ field" + "\n(de-crowding flow)",
         r"$w_3$  field $\to$ retail" + "\n(momentum chase)",
         r"$w_4$  retail $\to$ field" + "\n(wedge support)",
         r"$w_5$  MM $\to$ field" + "\n(inventory / gap)"]
vals = [p[2] for p in PRINCIPAL]
cols = [p[3] for p in PRINCIPAL]
ypos = np.arange(len(vals))[::-1]
ax.barh(ypos, vals, height=0.52, color=cols, alpha=0.88, lw=0)
for y, v in zip(ypos, vals):
    ax.text(v + 0.012, y, f"{v:.2f}", fontsize=6.0, va="center", color=INK)
ax.set_yticks(ypos); ax.set_yticklabels(names, fontsize=5.6, linespacing=1.1)
ax.set_xlim(0, 0.42); ax.set_xticks([0, 0.2, 0.4])
ax.set_xlabel("coupling loading\n(share of predicted wedge variance)",
              fontsize=6.2, labelpad=2)
ax.tick_params(axis="y", length=0)
ax.spines.left.set_visible(False)

# ══ (c) the inferred unwind mechanism ═════════════════════════════════════════
ax = fig.add_subplot(gs[2])
dates = pd.bdate_range("2026-04-01", "2026-07-29")
n = len(dates); t = np.arange(n)
i_snap = dates.get_loc(pd.Timestamp("2026-05-01"))
i_guid = dates.get_loc(pd.Timestamp("2026-07-13"))
i_cap  = dates.get_loc(pd.Timestamp("2026-07-28"))
rng = np.random.default_rng(7)

kappa = 0.88 - 0.02 / (1 + np.exp(-(t - i_guid + 25) / 6))     # slow top
kappa[i_guid - 4:] -= np.linspace(0, 0.42, n - i_guid + 4) ** 1.2 * 0.9
kappa = np.clip(kappa + rng.normal(0, 0.006, n), 0.15, 0.95)
f = 0.55 + 0.25 / (1 + np.exp(-(t - i_snap - 20) / 9))
f[i_guid:i_cap] += 0.08
f[i_cap:] = -0.85
f = np.clip(f + rng.normal(0, 0.02, n), -1, 1)
w = 0.20 + 0.07 / (1 + np.exp(-(t - i_snap - 25) / 10))
w[i_cap - 2:] = np.linspace(w[i_cap - 3], -0.02, n - i_cap + 2)
w = w + rng.normal(0, 0.004, n)

ax.plot(dates, kappa, color=C_INST, lw=1.1, label=r"institutional crowding  $\kappa_t$")
ax.plot(dates, f, color=C_RET, lw=1.1, label=r"retail flow  $f_t$")
ax.plot(dates, w * 3.2, color=C_INFO, lw=1.1,
        label=r"behavioral wedge  $w_t$ (scaled)")
ax.set_ylim(-1.05, 1.30)
for x_, lab, ha, dx in [(dates[i_snap], "May 1\nsnapshot", "center", 0),
                        (dates[i_guid], "Jul 13\nguidance", "right", -1),
                        (dates[i_cap], "Jul 28\ncapitulation", "left", 1)]:
    ax.axvline(x_, color=MUTE, lw=0.6, ls=(0, (2, 2)))
    ax.text(x_ + pd.Timedelta(days=dx), 1.08, lab, fontsize=5.6, color=MUTE,
            ha=ha, va="bottom", linespacing=1.1)
ax.set_ylabel("state (normalized)", fontsize=6.4)
ax.legend(loc="lower left", fontsize=5.6, frameon=False,
          handlelength=1.4, borderaxespad=0.2)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.xaxis.set_major_locator(mdates.MonthLocator())

# ── panel letters + footer ─────────────────────────────────────────────────────
for x, s in [(0.012, "a"), (0.415, "b"), (0.635, "c")]:
    fig.text(x, 0.955, s, fontsize=9, fontweight="bold", color=INK)
fig.text(0.012, 0.015,
         "Synthetic scenario; schematic couplings. The fully connected agent network is solved in Phase 1 as its mean-field "
         "simplification and trained directly in Phase 2 (NNGS). US market only.",
         fontsize=5.4, color=MUTE)

fig.savefig(os.path.join(FIGS, "agent_game_inference.png"),
            bbox_inches="tight", facecolor="white")
print("✓ figures/agent_game_inference.png")
