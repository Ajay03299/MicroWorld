"""
The market as a four-layer neural network — figures/four_level_network.png

Replaces the earlier hairball network graphic with the diagram the framework
actually implies: four layers of *agent-neurons*. Every neuron is an agent
(a market, an institution type, an institution, a desk); every edge is a
strategic coupling, not a passive weight; neurons in the same regulatory
class share a constraint module (the dashed group boxes). The magnifier
inset makes the Phase 2 claim visual: each neuron is itself a small neural
network with its own objective — it doesn't fire, it decides.

Run:  python scripts/make_four_layer_nn.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(os.path.dirname(HERE), "figures")

ULTRA = "#2563EB"                       # brand ultramarine
INK, MUTE, GRID = "#111827", "#6B7280", "#E5E7EB"
# Okabe-Ito per institution type
C_CB, C_BANK, C_QUANT = "#D55E00", "#0072B2", "#009E73"
C_AM, C_MM, C_RETAIL  = "#CC79A7", "#E69F00", "#56B4E9"

fig, ax = plt.subplots(figsize=(13.2, 7.8))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
fig.patch.set_facecolor("white")

# ── layer definitions ──────────────────────────────────────────────────────────
X = [0.09, 0.35, 0.63, 0.90]            # column x for L0..L3
LAYER_LABEL = [
    "L0 · markets\n(cross-market flows)",
    "L1 · institution types\n(one mean field each)",
    "L2 · institutions\n(within-type Nash)",
    "L3 · desks & individuals\n(intra-institution game)",
]
l0_names = ["US equities", "US Treasuries", "US credit", "US money mkts"]
l1_specs = [("central banks", C_CB), ("commercial banks", C_BANK),
            ("quant funds", C_QUANT), ("asset managers", C_AM),
            ("market makers", C_MM), ("retail cohorts", C_RETAIL)]
# L2: institutions grouped by parent type (type index into l1_specs)
l2_parent = [0, 1, 1, 2, 2, 2, 3, 3, 4, 5, 5]
n_l3 = 14

def ys(n, lo, hi):
    return np.linspace(hi, lo, n)

y0 = ys(4,  0.34, 0.72)
y1 = ys(6,  0.22, 0.80)
y2 = ys(len(l2_parent), 0.17, 0.78)
y3 = ys(n_l3, 0.16, 0.76)
R = [0.030, 0.024, 0.0165, 0.011]       # neuron radii per layer
l2_colors = [l1_specs[p][1] for p in l2_parent]

cols = [
    [(X[0], y, INK)   for y in y0],
    [(X[1], y, c)     for y, (_, c) in zip(y1, l1_specs)],
    [(X[2], y, c)     for y, c in zip(y2, l2_colors)],
    [(X[3], y, MUTE)  for y in y3],
]

# ── edges: consecutive layers, faint; a few highlighted strategic couplings ────
for li in range(3):
    for (xa, ya, _) in cols[li]:
        for (xb, yb, _) in cols[li + 1]:
            ax.plot([xa, xb], [ya, yb], color="#94A3B8", lw=0.55,
                    alpha=0.15, zorder=1)
# highlight: quant-fund type -> its institutions -> their desks (the game lit up)
qf = cols[1][2]
for j, p in enumerate(l2_parent):
    if p == 2:
        xb, yb, _ = cols[2][j]
        ax.plot([qf[0], xb], [qf[1], yb], color=C_QUANT, lw=1.4,
                alpha=0.75, zorder=2)
for (xb, yb, _) in cols[3][4:9]:
    ax.plot([cols[2][4][0], xb], [cols[2][4][1], yb], color=C_QUANT,
            lw=0.9, alpha=0.45, zorder=2)

# lateral (within-layer) competition arcs on L1 — strategic, not associative
for i in range(len(cols[1]) - 1):
    xa, ya, _ = cols[1][i]; xb, yb, _ = cols[1][i + 1]
    ax.add_patch(FancyArrowPatch((xa - 0.028, ya), (xb - 0.028, yb),
                 connectionstyle="arc3,rad=0.55", arrowstyle="<->",
                 mutation_scale=6, lw=0.7, color=MUTE, alpha=0.45, zorder=2))

# ── constraint group boxes on L2 (same regulator → shared constraint module) ──
groups = {}
for j, p in enumerate(l2_parent):
    groups.setdefault(p, []).append(j)
for p, idxs in groups.items():
    if len(idxs) < 2:
        continue
    ytop = y2[idxs[0]] + 0.030; ybot = y2[idxs[-1]] - 0.030
    ax.add_patch(FancyBboxPatch((X[2] - 0.028, ybot), 0.056, ytop - ybot,
                 boxstyle="round,pad=0.004,rounding_size=0.012",
                 fill=False, edgecolor=l1_specs[p][1], lw=1.1,
                 linestyle=(0, (3, 2)), alpha=0.85, zorder=3))
# annotation sits in the empty band between the L1 and L2 columns
ax.annotate("same regulator →\nshared constraint module\n(weight sharing)",
            xy=(X[2] - 0.030, (y2[3] + y2[5]) / 2), xytext=(0.485, 0.895),
            fontsize=8.6, color=C_QUANT, fontweight="bold", ha="center",
            va="top",
            arrowprops=dict(arrowstyle="->", color=C_QUANT, lw=1.0,
                            connectionstyle="arc3,rad=0.22"))

# ── neurons ────────────────────────────────────────────────────────────────────
for li, col in enumerate(cols):
    for (x, y, c) in col:
        ax.add_patch(Circle((x, y), R[li], facecolor="white",
                            edgecolor=c, lw=1.8 if li < 3 else 1.2, zorder=4))
        ax.add_patch(Circle((x, y), R[li] * 0.45, facecolor=c,
                            edgecolor="none", alpha=0.85, zorder=5))

for name, (x, y, _) in zip(l0_names, cols[0]):
    ax.text(x - 0.042, y, name, fontsize=8.6, color=INK, ha="right",
            va="center")
for (name, c), (x, y, _) in zip(l1_specs, cols[1]):
    ax.text(x, y - 0.050, name, fontsize=8.0, color=c, ha="center",
            fontweight="bold")

# layer captions — band below the node area, above the feedback arrow
for x, lab in zip(X, LAYER_LABEL):
    ax.text(x, 0.115, lab, fontsize=8.8, color=INK, ha="center",
            va="top", fontweight="bold")

# ── reflexivity feedback arrow (its own band at the very bottom) ───────────────
ax.add_patch(FancyArrowPatch((X[3] - 0.01, 0.042), (X[0] + 0.01, 0.042),
             connectionstyle="arc3,rad=0.0", arrowstyle="->",
             mutation_scale=15, lw=1.8, color=ULTRA, alpha=0.9, zorder=6))
ax.text(0.5, 0.012, "prices & mean-field feedback — reflexivity closes the loop",
        fontsize=8.8, color=ULTRA, ha="center", fontstyle="italic")

# ── magnifier inset: a neuron is itself a small network ───────────────────────
tx, ty, tr = cols[2][3][0], cols[2][3][1], R[2]
ix, iy, ir = 0.885, 0.87, 0.080
# tangent cone from the target neuron to the lens
for s in (+1, -1):
    ax.plot([tx + tr * 0.7, ix - ir * 0.55 * s],
            [ty + tr * s, iy - ir * 0.9],
            color=C_QUANT, lw=0.9, alpha=0.55, zorder=6)
ax.add_patch(Circle((ix, iy), ir, facecolor="#F8FAFC", edgecolor=C_QUANT,
                    lw=1.6, zorder=7))
mlp_x = [ix - 0.050, ix, ix + 0.050]
mlp_ys = [np.linspace(iy - 0.036, iy + 0.036, 3),
          np.linspace(iy - 0.044, iy + 0.044, 4),
          np.linspace(iy - 0.024, iy + 0.024, 2)]
for a_i in range(2):
    for ya_ in mlp_ys[a_i]:
        for yb_ in mlp_ys[a_i + 1]:
            ax.plot([mlp_x[a_i], mlp_x[a_i + 1]], [ya_, yb_],
                    color=MUTE, lw=0.6, alpha=0.6, zorder=8)
for x_, ys_ in zip(mlp_x, mlp_ys):
    for y_ in ys_:
        ax.add_patch(Circle((x_, y_), 0.0068, facecolor=C_QUANT,
                            edgecolor="white", lw=0.5, zorder=9))
ax.text(ix, iy + ir + 0.010,
        "each neuron is itself a small network with its own\nobjective $J_i$ — it doesn't fire, it decides",
        fontsize=8.6, color=INK, ha="center", va="bottom", fontweight="bold")

# ── titles (top-left band, kept clear of the inset) ────────────────────────────
ax.text(0.012, 0.995, "The market as a four-layer neural network",
        fontsize=15.5, fontweight="bold", color=INK, va="top")
ax.text(0.012, 0.942,
        "every neuron an agent · every edge a strategic coupling · dashed groups share their regulator's constraints\n"
        "Phase 1 solves this graph as a hierarchical mean-field game — Phase 2 trains it directly (NNGS)",
        fontsize=9.2, color=MUTE, va="top")

fig.savefig(os.path.join(FIGS, "four_level_network.png"), dpi=200,
            bbox_inches="tight", facecolor="white")
print("✓ figures/four_level_network.png")
