"""
The four-level coupled market network — a MIROFISH-style large-graph render
of the L0→L3 hierarchy, on a light background matching the README.

~5,000 nodes: 6 L0 markets (center) → 42 L1 institution types → ~450 L2
institutions → ~4,500 L3 individuals (outer cloud, incl. retail fans).
Two narrative threads:
  · red cascade  — one Fed decision (Mode II operator) propagating down all levels
  · orange trace — stress at a single L3 desk surfacing upward (the Λₜ story)

Run:  python scripts/make_network_figure.py   →  figures/four_level_network.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=3.2, foreground="#FBFBFC")]

rng = np.random.default_rng(42)

# ── palette (light theme) ──────────────────────────────────────────────────────
BG      = "#FBFBFC"
GRID    = "#D8DBE1"
C_L0    = "#0B1F3A"   # navy
C_L1    = "#2563EB"   # ultramarine
C_L2    = "#F97316"   # orange
C_L3    = "#9AA1AC"   # gray
C_EDGE  = "#C9CDD4"
C_RED   = "#E11D48"
C_ORNG  = "#D97706"
INK     = "#111827"
MUTE    = "#6B7280"

MARKETS = [("US", 90, 0.30), ("EU", 150, 0.18), ("CN", 210, 0.22),
           ("JP", 270, 0.10), ("HK", 330, 0.08), ("EM", 30, 0.12)]
TYPES = ["CB/Gov", "CommBank", "InvBank", "QuantHF", "PE/HF", "MutFund", "Retail"]
TYPE_L2 = {"CB/Gov": 2, "CommBank": 11, "InvBank": 9, "QuantHF": 16,
           "PE/HF": 12, "MutFund": 8, "Retail": 0}

def pol(r, deg):
    a = np.radians(deg)
    return np.array([r*np.cos(a), r*np.sin(a)])

nodes = {"L0": [], "L1": [], "L2": [], "L3": []}   # (x, y, size)
edges, red_edges, orange_path = [], [], []

# ── build hierarchy ────────────────────────────────────────────────────────────
l1_of, l2_of = {}, {}
for mi, (mname, mdeg, mw) in enumerate(MARKETS):
    p0 = pol(0.13, mdeg)
    nodes["L0"].append((*p0, 420 + 2400*mw, mname, mdeg))

    for ti, tname in enumerate(TYPES):
        tdeg = mdeg + (ti - 3) * 7.5 + rng.normal(0, 0.8)
        p1 = pol(rng.normal(0.36, 0.012), tdeg)
        nodes["L1"].append((*p1, 46))
        l1_of[(mi, ti)] = p1
        edges.append((p0, p1))

        n2 = max(0, int(round(TYPE_L2[tname] * (0.5 + 1.8*mw) + rng.normal(0, 1))))
        kids2 = []
        for _ in range(n2):
            p2 = pol(rng.normal(0.66, 0.030), tdeg + rng.normal(0, 2.6))
            nodes["L2"].append((*p2, 13))
            kids2.append(p2)
            edges.append((p1, p2))
            for _ in range(rng.integers(4, 11)):     # L3 staff of this institution
                p3 = pol(rng.normal(1.00, 0.035), tdeg + rng.normal(0, 3.2))
                nodes["L3"].append((*p3, 2.6))
                edges.append((p2, p3))
        l2_of[(mi, ti)] = kids2

        if tname == "Retail":                        # retail: direct L1→L3 fan
            n_ret = int(240 + 1400*mw)
            for _ in range(n_ret):
                p3 = pol(rng.normal(1.05, 0.045), mdeg + rng.normal(0, 14))
                nodes["L3"].append((*p3, 2.2))
                if rng.random() < 0.10:
                    edges.append((p1, p3))

# intra-cluster competition edges (same-type L2 pairs)
for key, kids in l2_of.items():
    for _ in range(int(len(kids) * 1.1)):
        if len(kids) >= 2:
            i, j = rng.choice(len(kids), 2, replace=False)
            edges.append((kids[i], kids[j]))

# a few cross-market information arcs at L1
for _ in range(26):
    (a, b) = rng.choice(len(nodes["L1"]), 2, replace=False)
    edges.append((np.array(nodes["L1"][a][:2]), np.array(nodes["L1"][b][:2])))

# ── red cascade: US L0 node → down all four levels ─────────────────────────────
us_p0 = np.array(nodes["L0"][0][:2])
for ti in range(len(TYPES)):
    p1 = l1_of[(0, ti)]
    red_edges.append((us_p0, p1, 1.5))
    kids = l2_of[(0, ti)]
    for k in kids:
        if rng.random() < 0.45:
            red_edges.append((p1, k, 0.7))
# red reaches a sample of the whole outer cloud on the US side
us_l3 = [n for n in nodes["L3"] if abs((np.degrees(np.arctan2(n[1], n[0])) % 360) - 90) < 26]
for n in rng.choice(len(us_l3), size=min(70, len(us_l3)), replace=False):
    src = l2_of[(0, rng.integers(1, 6))]
    if src:
        red_edges.append((src[rng.integers(len(src))], np.array(us_l3[n][:2]), 0.35))

# ── orange upward trace: one JP desk → its fund → its type → the JP market ─────
jp_kids = l2_of[(3, 3)]                              # JP QuantHF institutions
if jp_kids:
    p2 = jp_kids[0]
    p3 = pol(1.00, 270 + 1.5)
    orange_path = [(p3, p2), (p2, l1_of[(3, 3)]), (l1_of[(3, 3)], np.array(nodes["L0"][3][:2]))]

# ── render ─────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16.4, 11.2), dpi=150)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-1.52, 1.52); ax.set_ylim(-1.24, 1.24)
ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(plt.Rectangle((-1.6, -1.3), 3.2, 2.6, facecolor=BG, zorder=0))

gx, gy = np.meshgrid(np.arange(-1.5, 1.51, 0.05), np.arange(-1.22, 1.23, 0.05))
ax.scatter(gx, gy, s=1.2, color=GRID, alpha=0.55, zorder=1, linewidths=0)

ax.add_collection(LineCollection(edges, colors=C_EDGE, linewidths=0.35,
                                 alpha=0.35, zorder=2))
ax.add_collection(LineCollection([(a, b) for a, b, _ in red_edges], colors=C_RED,
                                 linewidths=[w for _, _, w in red_edges],
                                 alpha=0.45, zorder=3))
for a, b in orange_path:
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C_ORNG, lw=2.0, alpha=0.9,
            zorder=6, solid_capstyle="round")

# L0 capital-flow arcs (curved, navy)
for i in range(6):
    for j in range(i+1, 6):
        a = np.array(nodes["L0"][i][:2]); b = np.array(nodes["L0"][j][:2])
        mid = (a+b)/2 * 0.35
        t = np.linspace(0, 1, 40)[:, None]
        curve = (1-t)**2*a + 2*(1-t)*t*mid + t**2*b
        ax.plot(curve[:, 0], curve[:, 1], color=C_L0, lw=1.4, alpha=0.5, zorder=4)

x3 = np.array([(n[0], n[1]) for n in nodes["L3"]])
ax.scatter(x3[:, 0], x3[:, 1], s=[n[2] for n in nodes["L3"]], color=C_L3,
           alpha=0.75, zorder=5, linewidths=0)
x2 = np.array([(n[0], n[1]) for n in nodes["L2"]])
ax.scatter(x2[:, 0], x2[:, 1], s=[n[2] for n in nodes["L2"]], color=C_L2,
           alpha=0.92, zorder=6, linewidths=0)
x1 = np.array([(n[0], n[1]) for n in nodes["L1"]])
ax.scatter(x1[:, 0], x1[:, 1], s=[n[2] for n in nodes["L1"]], color=C_L1,
           alpha=0.95, zorder=7, linewidths=0)
for (x, y, s, mname, mdeg) in nodes["L0"]:
    ax.add_patch(Circle((x, y), np.sqrt(s)/720, facecolor=C_L0, zorder=8))
    lp = pol(np.sqrt(s)/720 + 0.045, mdeg)
    ax.text(x + lp[0], y + lp[1], mname, fontsize=9, fontweight="bold",
            color=C_L0, ha="center", va="center", zorder=9,
            family="DejaVu Sans Mono", path_effects=HALO)
# red halo on the US node
ax.add_patch(Circle(us_p0, 0.055, facecolor="none", edgecolor=C_RED,
                    lw=1.6, alpha=0.9, zorder=9))

# ── level labels along the upper-left diagonal ─────────────────────────────────
labels = [(1.00, 150, 0.82, "LEVEL 3", "individuals — desks · PMs · 500M retail"),
          (0.66, 157, 0.47, "LEVEL 2", "institutions — Nash within each type"),
          (0.36, 163, 0.14, "LEVEL 1", "institution types — multi-population MFG"),
          (0.16, 176, -0.20, "LEVEL 0", "markets & central banks — capital-flow game")]
for r, deg, ly, big, small in labels:
    p = pol(r, deg)
    ax.plot([-1.16, p[0]], [ly, p[1]], color=MUTE, lw=0.7, alpha=0.55,
            zorder=10, ls=(0, (2, 3)))
    ax.text(-1.47, ly+0.035, big, fontsize=12, fontweight="bold", color=INK,
            zorder=11, family="DejaVu Sans Mono", path_effects=HALO)
    ax.text(-1.47, ly-0.016, small, fontsize=8.2, color=MUTE, zorder=11,
            path_effects=HALO)

# narrative annotations
ax.annotate("Mode II operator: one Fed decision\nreaches all four levels within hours",
            xy=(us_p0[0]+0.02, us_p0[1]+0.04), xytext=(0.62, 1.10),
            fontsize=9, color=C_RED, fontweight="bold", zorder=11, path_effects=HALO,
            arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.1,
                            connectionstyle="arc3,rad=-0.15"))
if orange_path:
    tail = orange_path[0][0]
    ax.annotate("Λₜ: stress at one desk surfaces\nbefore prices move (Thm 8.2)",
                xy=(tail[0], tail[1]-0.02), xytext=(0.62, -1.02),
                fontsize=9, color=C_ORNG, fontweight="bold", zorder=11, path_effects=HALO,
                arrowprops=dict(arrowstyle="->", color=C_ORNG, lw=1.1,
                                connectionstyle="arc3,rad=0.18"))

# title / caption / legend
ax.text(-1.47, 1.13, "The Market as a Four-Level Coupled Game",
        fontsize=17, fontweight="bold", color=INK, zorder=11, path_effects=HALO)
ax.text(-1.47, 1.06, "≈5,000 agents rendered · 50,000 institutions · 500M retail · "
        "30 central banks — one nested mean-field game", fontsize=9.5, color=MUTE,
        zorder=11, path_effects=HALO)
ax.text(0.30, -1.165,
        "market price = the emergent four-level Nash equilibrium      "
        "P(t) = ∫∫∫∫ α*(y, x, ξ, Γ) dμ⁽³⁾ dμ⁽²⁾ dμ⁽¹⁾ dν⁽⁰⁾",
        fontsize=10, color=INK, ha="center", zorder=12,
        family="DejaVu Sans Mono", path_effects=HALO)

leg = [("L0 · markets", C_L0), ("L1 · institution types", C_L1),
       ("L2 · institutions", C_L2), ("L3 · individuals", C_L3),
       ("event cascade (down)", C_RED), ("stress signal (up)", C_ORNG)]
box = FancyBboxPatch((-1.50, -1.20), 0.86, 0.30,
                     boxstyle="round,pad=0.015,rounding_size=0.02",
                     facecolor="white", edgecolor="#E5E7EB", zorder=11, alpha=0.95)
ax.add_patch(box)
for k, (txt, c) in enumerate(leg):
    col, row = divmod(k, 3)
    x0, y = -1.455 + col*0.43, -0.975 - 0.075*row
    ax.scatter([x0], [y], s=24, color=c, zorder=12, linewidths=0)
    ax.text(x0+0.035, y, txt, fontsize=7.6, color=INK, va="center", zorder=12)

fig.savefig("figures/four_level_network.png", facecolor=BG)
import os
print("✓ figures/four_level_network.png",
      f"{os.path.getsize('figures/four_level_network.png')/1e6:.1f} MB",
      "| nodes:", sum(len(v) for v in nodes.values()), "| edges:", len(edges))
