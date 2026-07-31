"""
figures/four_level_network.png — the market as a LAYERED neural network.

The upgraded structure of docs/MARKET_LAYERS.md drawn as one network:
capital-flow layers 0-6 as columns of agent-neurons, the prop/HFT parallel
layer above the L4-L5 gap, and the two outer rings — information (top) and
rules (bottom) — that never touch the money but steer and constrain every
edge. Same conventions as the rest of the repo's figures (journal style),
same per-layer palette as the interactive 3D (docs/index.html).

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

INK, MUTE = "#111827", "#6B7280"
ULTRA = "#2563EB"
LCOL = {0: "#0B1F3A", 1: "#1D4ED8", 2: "#60A5FA", 3: "#2563EB",
        4: "#7C3AED", 5: "#F97316", 6: "#059669"}
C_PAR, C_R1, C_R2 = "#D97706", "#DB2777", "#DC2626"

plt.rcParams.update({"font.family": ["Helvetica", "Arial", "DejaVu Sans"],
                     "font.size": 8, "figure.facecolor": "white"})
fig, ax = plt.subplots(figsize=(13.2, 7.6))
ax.set_xlim(0, 1.10); ax.set_ylim(0, 1.02); ax.axis("off")

XL = [0.055 + 0.132 * l for l in range(7)]          # column x
NN = [4, 5, 4, 6, 5, 4, 4]                          # neurons per column
YLO, YHI = 0.27, 0.70
COLS = []
for l in range(7):
    ys = np.linspace(YHI, YLO, NN[l])
    COLS.append([(XL[l], y) for y in ys])

# ── faint adjacent-layer full connectivity ────────────────────────────────────
for l in range(6):
    for (xa, ya) in COLS[l]:
        for (xb, yb) in COLS[l + 1]:
            ax.plot([xa, xb], [ya, yb], color="#B9BEC7", lw=0.45,
                    alpha=0.30, zorder=1)

# the capital chain, highlighted through the top neurons
chain = [COLS[l][0] for l in range(7)]
for (xa, ya), (xb, yb) in zip(chain[:-1], chain[1:]):
    ax.add_patch(FancyArrowPatch((xa, ya), (xb, yb), arrowstyle="-|>",
                 mutation_scale=9, lw=2.0, color=ULTRA, alpha=0.85,
                 shrinkA=6, shrinkB=6, zorder=3))
ax.text((XL[0] + XL[1]) / 2, YHI + 0.033, "the capital chain →",
        fontsize=7.6, color=ULTRA, ha="center", fontweight="bold")

# neurons
for l in range(7):
    for (x, y) in COLS[l]:
        ax.add_patch(Circle((x, y), 0.0185, facecolor="white",
                            edgecolor=LCOL[l], lw=1.6, zorder=4))
        ax.add_patch(Circle((x, y), 0.0085, facecolor=LCOL[l],
                            edgecolor="none", alpha=0.9, zorder=5))

# constraint group box on L3 (hedge-fund neurons share their regulator)
gx = XL[3]
gy_top, gy_bot = COLS[3][2][1] + 0.030, COLS[3][4][1] - 0.030
ax.add_patch(FancyBboxPatch((gx - 0.029, gy_bot), 0.058, gy_top - gy_bot,
             boxstyle="round,pad=0.004,rounding_size=0.012", fill=False,
             edgecolor=C_R2, lw=1.1, linestyle=(0, (3, 2)), alpha=0.9,
             zorder=3))
ax.text(gx + 0.038, (gy_top + gy_bot) / 2,
        "same regulator →\nshared constraint\nmodule (◎2)",
        fontsize=6.2, color=C_R2, ha="left", va="center", fontweight="bold",
        linespacing=1.25, zorder=6)

# column captions
CAPT = [("L0 · surplus sector", "households · treasuries\nforeign savings"),
        ("L1 · asset owners", "pensions · insurers\nSWFs · endowments"),
        ("L2 · allocation", "consultants · wealth\nchannels · bank conduit"),
        ("L3 · asset managers", "index · active\nhedge funds · private"),
        ("L4 · sell side", "IBs · brokers\nprime · dealers"),
        ("L5 · infrastructure", "venues · CCP/CSD\ncustody · payments"),
        ("L6 · issuers", "corporates · Treasury\nsecuritization SPVs")]
for l, (t1, t2) in enumerate(CAPT):
    ax.text(XL[l], 0.228, t1, fontsize=8.0, color=INK, ha="center",
            va="top", fontweight="bold")
    ax.text(XL[l], 0.201, t2, fontsize=6.4, color=MUTE, ha="center",
            va="top", linespacing=1.25)

# ── parallel layer: prop/HFT above the L4–L5 gap ──────────────────────────────
px_c = (XL[4] + XL[5]) / 2
PAR = [(px_c - 0.030, 0.785), (px_c + 0.030, 0.785), (px_c, 0.750)]
for (x, y) in PAR:
    ax.plot([x, XL[4] + 0.010], [y, COLS[4][0][1] + 0.010], color=C_PAR,
            lw=0.8, alpha=0.55, zorder=2)
    ax.plot([x, XL[5] - 0.010], [y, COLS[5][0][1] + 0.010], color=C_PAR,
            lw=0.8, alpha=0.55, zorder=2)
for (x, y) in PAR:
    ax.add_patch(Circle((x, y), 0.0145, facecolor="white", edgecolor=C_PAR,
                        lw=1.5, zorder=4))
    ax.add_patch(Circle((x, y), 0.0066, facecolor=C_PAR, edgecolor="none",
                        alpha=0.9, zorder=5))
ax.text(px_c, 0.822, "∥ prop / HFT — own capital only, liquidity between L4–L5",
        fontsize=6.8, color=C_PAR, ha="center", fontweight="bold")

# ── outer ring 1 (top): information & pricing ─────────────────────────────────
R1Y = 0.872
R1 = [(0.100, "media"), (0.270, "data &\nresearch"),
      (0.455, "index\nproviders"), (0.630, "rating\nagencies")]
ax.add_patch(FancyBboxPatch((0.060, R1Y - 0.028), 0.640, 0.056,
             boxstyle="round,pad=0.004,rounding_size=0.02", fill=False,
             edgecolor=C_R1, lw=1.0, linestyle=(0, (4, 3)), alpha=0.7,
             zorder=2))
for (x, lab) in R1:
    ax.add_patch(Circle((x, R1Y), 0.0120, facecolor="white", edgecolor=C_R1,
                        lw=1.4, zorder=4))
    ax.add_patch(Circle((x, R1Y), 0.0054, facecolor=C_R1, edgecolor="none",
                        alpha=0.9, zorder=5))
    ax.text(x + 0.019, R1Y, lab, fontsize=6.2, color=C_R1, ha="left",
            va="center", linespacing=1.15)
ax.text(0.715, R1Y, "◎1 · information ring —\nsteers money it never touches",
        fontsize=7.0, color=C_R1, ha="left", va="center", fontweight="bold",
        linespacing=1.25)
# short vertical information arrows: index → L3 · media → L0
ax.add_patch(FancyArrowPatch((0.455, R1Y - 0.031), (XL[3], YHI + 0.026),
             arrowstyle="-|>", mutation_scale=7, lw=1.0, color=C_R1,
             linestyle=(0, (4, 2)), alpha=0.75, zorder=2))
ax.add_patch(FancyArrowPatch((0.100, R1Y - 0.031), (XL[0] + 0.006, YHI + 0.026),
             arrowstyle="-|>", mutation_scale=7, lw=1.0, color=C_R1,
             linestyle=(0, (4, 2)), alpha=0.75, zorder=2))

# ── outer ring 2 (bottom): rules & last resort ────────────────────────────────
R2Y = 0.045
R2 = [(0.100, "Fed"), (0.270, "SEC · CFTC"), (0.450, "Basel · OCC"),
      (0.600, "FDIC · SIPC")]
ax.add_patch(FancyBboxPatch((0.060, R2Y - 0.028), 0.640, 0.056,
             boxstyle="round,pad=0.004,rounding_size=0.02", fill=False,
             edgecolor=C_R2, lw=1.0, linestyle=(0, (4, 3)), alpha=0.7,
             zorder=2))
for (x, lab) in R2:
    ax.add_patch(Circle((x, R2Y), 0.0120, facecolor="white", edgecolor=C_R2,
                        lw=1.4, zorder=4))
    ax.add_patch(Circle((x, R2Y), 0.0054, facecolor=C_R2, edgecolor="none",
                        alpha=0.9, zorder=5))
    ax.text(x + 0.019, R2Y, lab, fontsize=6.6, color=C_R2, ha="left",
            va="center")
ax.text(0.715, R2Y, "◎2 · rules ring — the constraint\narchitecture (weight sharing)",
        fontsize=7.0, color=C_R2, ha="left", va="center", fontweight="bold",
        linespacing=1.25)
# one dashed constraint arrow: the ring reaches up into the L3 shared box
ax.add_patch(FancyArrowPatch((0.530, R2Y + 0.031), (gx + 0.022, gy_bot - 0.006),
             arrowstyle="-|>", mutation_scale=7, lw=1.1, color=C_R2,
             linestyle=(0, (4, 2)), alpha=0.8,
             connectionstyle="arc3,rad=-0.07", zorder=2))

# ── returns flow back (reflexivity) ───────────────────────────────────────────
ax.add_patch(FancyArrowPatch((XL[6], 0.128), (XL[0], 0.128),
             arrowstyle="-|>", mutation_scale=13, lw=1.7, color=ULTRA,
             alpha=0.85, connectionstyle="arc3,rad=0.03", zorder=3))
ax.text((XL[0] + XL[6]) / 2, 0.098,
        "returns — dividends, interest, buybacks — flow back along the same path · reflexivity closes the loop",
        fontsize=7.2, color=ULTRA, ha="center", fontstyle="italic")

# ── magnifier inset: a neuron is itself a small network ───────────────────────
tx, ty = COLS[3][3]
ix, iy, ir = 0.985, 0.60, 0.075
for s in (+1, -1):
    ax.plot([tx + 0.016, ix - ir * 0.6 * s], [ty + 0.012 * s, iy - ir * 0.85],
            color=LCOL[3], lw=0.8, alpha=0.5, zorder=6)
ax.add_patch(Circle((ix, iy), ir, facecolor="#F8FAFC", edgecolor=LCOL[3],
                    lw=1.5, zorder=7))
mlp_x = [ix - 0.045, ix, ix + 0.045]
mlp_ys = [np.linspace(iy - 0.032, iy + 0.032, 3),
          np.linspace(iy - 0.040, iy + 0.040, 4),
          np.linspace(iy - 0.021, iy + 0.021, 2)]
for a_i in range(2):
    for ya_ in mlp_ys[a_i]:
        for yb_ in mlp_ys[a_i + 1]:
            ax.plot([mlp_x[a_i], mlp_x[a_i + 1]], [ya_, yb_], color=MUTE,
                    lw=0.55, alpha=0.6, zorder=8)
for x_, ys_ in zip(mlp_x, mlp_ys):
    for y_ in ys_:
        ax.add_patch(Circle((x_, y_), 0.0062, facecolor=LCOL[3],
                            edgecolor="white", lw=0.5, zorder=9))
ax.text(ix, iy - ir - 0.015,
        "each neuron is itself a small\nnetwork with its own objective $J_i$ —\nit doesn't fire, it decides",
        fontsize=6.8, color=INK, ha="center", va="top", fontweight="bold",
        linespacing=1.25)

# ── titles (top band, kept clear of the information ring) ─────────────────────
ax.text(0.012, 1.015, "The market as a layered neural network",
        fontsize=15.5, fontweight="bold", color=INK, va="top")
ax.text(0.012, 0.966,
        "capital-flow layers 0–6 · every neuron an agent · the ∥ layer plays with its own capital · the two rings never touch the money · "
        "Phase 1 solves the four-level\ngame projection of this graph — Phase 2 trains it directly (NNGS, docs/PHASE2_NEURAL_GAME.md) · US market",
        fontsize=8.4, color=MUTE, va="top", linespacing=1.4)

fig.savefig(os.path.join(FIGS, "four_level_network.png"), dpi=200,
            bbox_inches="tight", facecolor="white")
print("✓ figures/four_level_network.png")
