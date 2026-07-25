"""
Generator for the interactive 3D four-level universe (docs/).

Computes a deterministic 3D layout — L0 market cores on an inner sphere,
L1 / L2 / L3 on expanding spherical shells inside each market's cone —
plus the full story payload for every clickable agent, and writes:

    docs/data.js                    (positions, edges, stories)
    figures/network3d_preview.png   (static preview card for the README)

Run:  python scripts/make_network3d.py
"""
import json
import os
import numpy as np

rng = np.random.default_rng(2026)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
FIGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

# ── markets: name, polar deg, azimuth deg, weight, story ───────────────────────
MARKETS = [
    ("US", 42,   0, 0.30, ["Equity float ≈ $50T · S&P 500 · NASDAQ · NYSE",
                           "Fed = the world's rate-setter · reserve currency",
                           "Game: MFC (stability) ∩ MFG (capital attraction)",
                           "Γᵁˢ = (SPX, r_fed, DXY)"]),
    ("EU", 75,  60, 0.18, ["Equity float ≈ $14T · STOXX 600 · DAX · CAC",
                           "ECB: negative-rate pioneer · Basel III home",
                           "Game: MFC bloc + MFG vs US/CN",
                           "Γᴱᵁ = (STOXX, r_ecb, EURUSD)"]),
    ("CN", 105, 140, 0.22, ["Equity float ≈ $11T · CSI 300 · HSI · STAR",
                           "PBOC: FX controls + RRR lever · semi-closed capital account",
                           "Game: MFC dominant (state-directed)",
                           "Γᶜᴺ = (CSI300, r_pboc, USDCNY)"]),
    ("JP", 80, 220, 0.10, ["Equity float ≈ $6T · TOPIX · Nikkei 225",
                           "BOJ: YCC + the world's carry-trade funding source",
                           "Negative real rates → yen carry → global spillover",
                           "Γᴶᴾ = (Nikkei, r_boj, USDJPY)"]),
    ("HK", 112, 280, 0.08, ["Equity float ≈ $4.5T · HSI · Connect gateway",
                           "USD peg: imports Fed policy, prices China risk",
                           "Game: the arbitrage hinge between CN and the world",
                           "Γᴴᴷ = (HSI, HIBOR, USDHKD)"]),
    ("EM", 60, 320, 0.12, ["Equity float ≈ $8T · MSCI EM · IN · BR · KR · TW",
                           "Hot-money target: highest beta to global risk appetite",
                           "Game: MFG price-takers — Lévy events on carry unwinds",
                           "Γᴱᴹ = (MSCI_EM, spreads, carry)"]),
]

TYPES = [
    ("CB/Gov",   "MFC (planner)",        "MAX", "Confidential macro + flow data · rate decisions are Mode II operators", 1,  "#0B1F3A"),
    ("CommBank", "MFG (lending rates)",  "HIGH","Deposit flows, loan books · NIM + credit risk · Basel-constrained",     10, "#1D4ED8"),
    ("InvBank",  "MFG (prop+facilit.)",  "HIGH","Client order flow — the most informative signal · owns M&A (Mode III)",  8, "#2563EB"),
    ("QuantHF",  "MFG (alpha race)",     "HIGH","Alt data · stat arb momentum vol arb · zero-sum vs peers · ν_η spikes", 15, "#3B82F6"),
    ("PE/HF",    "MFG (value+macro)",    "HIGH","5–10yr horizons · private-market info universe · LP capital game",      11, "#60A5FA"),
    ("MutFund",  "MFC (passive)",        "MED", "Public filings + 13F · predictable rebalance → front-run by QuantHF",    7, "#93C5FD"),
    ("Retail",   "MFG (noise+momentum)", "LOW", "Public news hours late · LLM homogenization → increasingly legible",     0, "#EF4444"),
]

FIRMS = {
    "QuantHF":  ["Jane Street", "Citadel", "Two Sigma", "Renaissance", "D.E. Shaw", "Millennium"],
    "InvBank":  ["Goldman Sachs", "JPMorgan", "Morgan Stanley", "UBS"],
    "CommBank": ["JPM Chase", "Bank of America", "HSBC", "ICBC"],
    "MutFund":  ["BlackRock", "Vanguard", "Fidelity", "State Street"],
    "PE/HF":    ["Blackstone", "KKR", "Bridgewater", "Soros Fund"],
    "CB/Gov":   ["The central bank"],
}
PROFILE = {"QuantHF": ("$10–60B", "5–15×", "5 days", "10 ms"),
           "InvBank": ("$40–55B rev", "12×", "intraday–weeks", "1 ms"),
           "CommBank": ("$0.3–4T assets", "10×", "quarters", "1 s"),
           "MutFund": ("$1–10T", "1×", "1–5 yr", "days"),
           "PE/HF":  ("$0.1–1T", "2–5×", "5–10 yr", "weeks"),
           "CB/Gov": ("∞ (printing press)", "—", "decades", "real-time")}
DESKS = ["Quant Equity desk · VaR $120M/day · Sharpe > threshold → more capital",
         "Global Macro desk · reacts to Level 0 in milliseconds",
         "HFT / market-making · symmetric spread equilibrium (s* = 2c/Q)",
         "Risk management · the MFC enforcer — implements Λₜ in production",
         "Research / ML · produces the I^(priv) advantage · internal credit game",
         "Execution desk · Almgren-Chriss scheduling vs adverse selection"]
RETAIL_ARCH = ["Passive indexer — 'should I rebalance?'",
               "Active follower — 'what's hot today?'",
               "News reactor — trades the headline, hours late",
               "DIY quant — backtests factors in a spreadsheet",
               "Meme trader — all-in on the squeeze"]

def sph(r, polar_deg, azim_deg):
    t, p = np.radians(polar_deg), np.radians(azim_deg)
    return np.array([r*np.sin(t)*np.cos(p), r*np.cos(t), r*np.sin(t)*np.sin(p)])

def cone_dir(u, half_deg):
    """random unit vector within half_deg of unit vector u"""
    while True:
        v = rng.normal(size=3); v /= np.linalg.norm(v)
        w = u + v * np.tan(np.radians(half_deg)) * rng.random()
        w /= np.linalg.norm(w)
        if np.dot(w, u) > np.cos(np.radians(half_deg)):
            return w

P, S = [], []          # positions, sizes
LVL = []               # level per node
STORY = []             # story dict per node (L3 stories procedural client-side → None)
E, RED, ORANGE = [], [], []

def add(pos, size, lvl, story):
    P.append(pos); S.append(size); LVL.append(lvl); STORY.append(story)
    return len(P) - 1

for mi, (mname, pol, azi, w, mstory) in enumerate(MARKETS):
    u = sph(1.0, pol, azi)
    i0 = add(u*0.18, 0.038 + 0.075*w, 0,
             {"t": f"{mname} — Level 0 market", "c": "L0", "l": mstory})
    for ti, (tname, game, snr, desc, n2base, _col) in enumerate(TYPES):
        d1 = cone_dir(u, 16)
        i1 = add(d1*rng.normal(0.36, 0.008), 0.022, 1,
                 {"t": f"{mname} · {tname}", "c": "L1",
                  "l": [f"Game: {game} · SNR: {snr}", desc,
                        "Same-type: MFG competition · cross-type: capital + info coupling"]})
        E.append((i0, i1))
        n2 = max(0, int(round(n2base * (0.5 + 1.8*w) + rng.normal(0, 0.8))))
        firms = FIRMS.get(tname, [])
        for k in range(n2):
            d2 = cone_dir(d1, 9)
            name = firms[k] if mi == 0 and k < len(firms) else f"{tname} fund #{k+1}"
            aum, lev, hold, lat = PROFILE.get(tname, ("—",)*4)
            i2 = add(d2*rng.normal(0.66, 0.020), 0.012, 2,
                     {"t": f"{name}", "c": "L2",
                      "l": [f"{mname} · {tname} · AUM {aum} · leverage {lev}",
                            f"holding {hold} · info latency {lat}",
                            "Nash: diversify until marginal α = txn cost",
                            "strategy overlap with siblings → correlated-unwind risk (Quant Quake '07)"]})
            E.append((i1, i2))
            for _ in range(int(rng.integers(4, 9))):
                d3 = cone_dir(d2, 6)
                i3 = add(d3*rng.normal(1.00, 0.025), 0.005, 3, None)
                E.append((i2, i3))
        if tname == "Retail":
            for _ in range(int(160 + 900*w)):
                d3 = cone_dir(u, 30)
                i3 = add(d3*rng.normal(1.06, 0.035), 0.004, 3, None)
                if rng.random() < 0.08:
                    E.append((i1, i3))

P = np.array(P)
# red cascade: US L0 → its L1s → 45% of their L2s → 20% of those L2s' L3s
us0 = 0
l1_us = [j for j, (a, b) in enumerate(E) if a == us0]
for _, b in [E[j] for j in l1_us]:
    RED.append((us0, b))
    kids = [e[1] for e in E if e[0] == b and LVL[e[1]] == 2]
    for k in kids:
        if rng.random() < 0.45:
            RED.append((b, k))
            gk = [e[1] for e in E if e[0] == k]
            for g in gk:
                if rng.random() < 0.20:
                    RED.append((k, g))
# orange upward: one JP quant desk → fund → type → JP core
jp_l1 = None
for e in E:
    if LVL[e[1]] == 1 and STORY[e[1]] and STORY[e[1]]["t"] == "JP · QuantHF":
        jp_l1 = e[1]; break
jp_l2 = next(e[1] for e in E if e[0] == jp_l1 and LVL[e[1]] == 2)
jp_l3 = next(e[1] for e in E if e[0] == jp_l2)
jp0 = next(i for i, s in enumerate(STORY) if s and s["c"] == "L0" and s["t"].startswith("JP"))
ORANGE = [(jp_l3, jp_l2), (jp_l2, jp_l1), (jp_l1, jp0)]

flows = [(0, 1, "$1.9T/yr"), (0, 2, "$1.2T/yr"), (0, 3, "$0.9T/yr"),
         (0, 5, "$0.8T/yr"), (2, 4, "$0.7T/yr"), (1, 2, "$0.6T/yr"),
         (3, 5, "carry"), (4, 0, "$0.4T/yr")]
l0_idx = [i for i, s in enumerate(STORY) if s and s["c"] == "L0"]

payload = {
    "pos": np.round(P, 4).tolist(), "size": np.round(np.array(S), 4).tolist(),
    "lvl": LVL, "story": STORY,
    "edges": E, "red": RED, "orange": ORANGE,
    "l0": l0_idx, "flows": [[l0_idx[a], l0_idx[b], t] for a, b, t in flows],
    "desks": DESKS, "retail": RETAIL_ARCH,
}
with open(os.path.join(OUT, "data.js"), "w") as f:
    f.write("window.MW_DATA = " + json.dumps(payload, separators=(",", ":")) + ";")
print(f"✓ docs/data.js  nodes={len(P)} edges={len(E)} red={len(RED)}",
      f"size={os.path.getsize(os.path.join(OUT,'data.js'))//1024}KB")

# ── static preview card for the README ─────────────────────────────────────────
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(13.4, 8.0), dpi=150)
axp = fig.add_axes([0.02, 0.00, 0.96, 0.88], projection="3d")
axp.set_facecolor("#FBFBFC"); fig.patch.set_facecolor("#FBFBFC")
lvl = np.array(LVL); Pp = P
seg_idx = rng.choice(len(E), size=min(2400, len(E)), replace=False)
for j in seg_idx:
    a, b = E[j]
    axp.plot(*zip(Pp[a], Pp[b]), color="#C9CDD4", lw=0.25, alpha=0.28)
for a, b in RED:
    axp.plot(*zip(Pp[a], Pp[b]), color="#E11D48", lw=0.55, alpha=0.5)
for a, b in ORANGE:
    axp.plot(*zip(Pp[a], Pp[b]), color="#D97706", lw=2.2, alpha=0.95)
m3, m2, m1, m0 = lvl == 3, lvl == 2, lvl == 1, lvl == 0
axp.scatter(*Pp[m3].T, s=1.1, c="#9AA1AC", alpha=0.6, linewidths=0)
axp.scatter(*Pp[m2].T, s=7, c="#F97316", alpha=0.9, linewidths=0)
axp.scatter(*Pp[m1].T, s=22, c="#2563EB", alpha=0.95, linewidths=0)
axp.scatter(*Pp[m0].T, s=160, c="#0B1F3A", linewidths=0)
axp.set_axis_off(); axp.set_box_aspect((1, 1, 1))
axp.view_init(elev=16, azim=-58)
axp.set_xlim(-1.05, 1.05); axp.set_ylim(-1.05, 1.05); axp.set_zlim(-1.05, 1.05)
fig.text(0.045, 0.94, "The Four-Level Universe — interactive 3D",
         fontsize=19, fontweight="bold", color="#111827")
fig.text(0.045, 0.885, "≈3,700 agents · rotate · zoom · click any market, "
         "institution type, fund or trader for its storyline",
         fontsize=11, color="#6B7280")
fig.text(0.5, 0.075, "▶  O P E N   I N T E R A C T I V E", fontsize=15,
         color="white", ha="center", fontweight="bold",
         bbox=dict(boxstyle="round,pad=0.55", facecolor="#2563EB", edgecolor="none"))
fig.savefig(os.path.join(FIGS, "network3d_preview.png"), facecolor="#FBFBFC")
print("✓ figures/network3d_preview.png")
