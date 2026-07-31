"""
Generator for the interactive 3D layered US market (docs/).

A 3D neural-network layout of the REAL US market structure — capital-flow
layers 0-6 as columns, the proprietary/HFT parallel layer above the 4-5
gap, and the two outer rings (information & rules) encircling the chain.
Every named node is a real institution; every node AND every edge is
clickable and returns the single most important reading for that entity /
relationship on the snapshot date 2026-05-01.

Honesty: the readings are MODEL-INFERRED snapshots generated from public
role structure plus the repo's own real-data replay (the frozen-recipe Λ
for the memory basket exited its 6-month crisis regime on 2026-04-23 —
demo/hindcast_memory_2026.py). They are illustrative model output, not
statements of fact about the named institutions, and the page says so.

Writes:
    docs/data.js                    (positions, layers, stories, edge stories)
    figures/network3d_preview.png   (static preview card for the README)

Run:  python scripts/make_network3d.py
"""
import json
import os
import numpy as np

rng = np.random.default_rng(20260501)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
FIGS = os.path.join(ROOT, "figures")

SNAP = "2026-05-01"
LAM_FACT = ("Repo's own replay (demo/hindcast_memory_2026.py): the frozen-recipe Λ for "
            "the memory basket sat above its crisis threshold for 126 sessions from "
            "Oct 22, 2025 and exited on Apr 23, 2026 — eight days before this snapshot.")

# ── layer geometry ─────────────────────────────────────────────────────────────
LX = {0: -2.7, 1: -1.8, 2: -0.9, 3: 0.0, 4: 0.9, 5: 1.8, 6: 2.7}
CHIP = {0: "L0", 1: "L1", 2: "L2", 3: "L3", 4: "L4", 5: "L5", 6: "L6",
        7: "∥", 8: "◎1", 9: "◎2", 10: "R"}
LAYER_NAME = {0: "surplus sector", 1: "asset owners", 2: "allocation & conduits",
              3: "asset managers", 4: "sell side & intermediaries",
              5: "infrastructure", 6: "issuers", 7: "prop / HFT (own capital)",
              8: "information ring", 9: "rules ring", 10: "retail field"}

P, LVL, SIZE, STORY, NAME = [], [], [], [], []

def add(pos, lvl, size, name, lines):
    P.append([round(float(pos[0]), 4), round(float(pos[1]), 4), round(float(pos[2]), 4)])
    LVL.append(lvl); SIZE.append(size); NAME.append(name)
    STORY.append({"t": name, "c": CHIP[lvl],
                  "l": lines + [f"— model-inferred snapshot · {SNAP} · illustrative"]})
    return len(P) - 1

def col_pos(lvl, k, n, r=0.72):
    a = 2 * np.pi * k / n + (lvl * 0.7)
    rr = r * (0.55 + 0.45 * ((k * 7919) % 100) / 100)
    return np.array([LX[lvl] + rng.normal(0, 0.05),
                     rr * np.cos(a), rr * np.sin(a)])

def m1(read):   # standard "May 1 read" line
    return f"May 1 read: {read}"

# ── the node universe (name, role line, May-1 model read) ─────────────────────
L0 = [
 ("US households (aggregate)", "Layer 0 — the original surplus: wages → 401(k)s, brokerage, deposits",
  "savings still flowing to index sleeves; the AI-memory complex is the year's most-owned retail theme"),
 ("US retail cohort (self-directed)", "Dual-listed L0+L3: the self-directed crowd, increasingly LLM-fed",
  "query concentration around 'AI memory' names at sample highs — the legible-crowd channel (Day 16)"),
 ("Apple treasury", "Corporate surplus: ~$160B-scale liquidity book run like an asset manager",
  "corporate cash remains a structural bid for short-duration paper, not equities"),
 ("Microsoft treasury", "Corporate surplus: mega-cap cash generation, AI capex offset",
  "capex absorbs surplus — the AI buildout is partly self-funded, shrinking net financial savings"),
 ("Berkshire Hathaway (cash book)", "The discretionary surplus pool the market watches most",
  "a record cash pile is itself a signal: the deepest-pocket value buyer is not chasing this tape"),
 ("Treasury General Account", "Government cash balance at the Fed — fiscal flow node",
  "TGA swings move system liquidity mechanically; the model treats it as an L0 exogenous flow"),
 ("Foreign official inflows (aggregate)", "Cross-border savings entering US assets",
  "foreign demand for USD assets steady; the marginal buyer of Treasuries, not of crowded semis"),
]
L1 = [
 ("CalPERS", "Largest US public pension — liability-driven, consultant-gated",
  "equity sleeve overweight semis by index drift after the memory rally; rebalance = mechanical selling of winners"),
 ("CalSTRS", "US public pension — long-horizon, benchmark-anchored",
  "same drift-overweight condition as every indexed owner; patience is the mandate, not conviction"),
 ("NY State Common", "US public pension fund",
  "policy-portfolio bands stretched by the AI complex; a band-triggered trim is a κ-reducing flow"),
 ("GPIF (US sleeve)", "World's largest pension's US allocation",
  "passive by design — its flows are calendar-predictable, and the model treats them as such"),
 ("Norway GPFG (US sleeve)", "Sovereign fund, ~70% equities, rules-based",
  "rules-based rebalancing leans against whatever ran — a slow contrarian current under the mania"),
 ("GIC (US sleeve)", "Singapore sovereign capital in US markets",
  "long-horizon capital with optionality; the model reads sovereigns as stabilizers until regime breaks"),
 ("MetLife", "Life insurer — liability-matching, credit-heavy",
  "duration needs dominate; equity risk budget small — insurers are not in the crowded trade"),
 ("Prudential Financial", "Insurer / asset owner-manager hybrid",
  "liability constraints bind allocation; the constraint module is the story, not the view"),
 ("Harvard endowment", "University endowment — illiquidity-tolerant",
  "private-heavy book; public-equity sleeve small — spectator to the memory episode"),
 ("Yale endowment", "The endowment-model archetype",
  "alternatives-first allocation: public crowding matters via its managers, not directly"),
]
L2 = [
 ("Mercer", "Investment consultant — gatekeeper of institutional mandates",
  "gatekeepers reallocate slowly; no mandate churn on a theme this young — inertia is information"),
 ("Cambridge Associates", "Consultant to endowments/foundations",
  "client questions about 'AI concentration risk' rising — the advice channel precedes the flow channel"),
 ("Aon", "Consultant / OCIO provider",
  "OCIO books mirror policy portfolios; drift-trims queued, not discretionary sells"),
 ("Morgan Stanley Wealth Mgmt", "Largest US advisor network by assets",
  "advisor allocations to semis at multi-year highs — the wealth channel is fully participating"),
 ("Merrill (BofA) Wealth", "Wirehouse wealth channel",
  "model portfolios overweight the AI complex via growth sleeves; late-cycle participation pattern"),
 ("UBS Wealth USA", "Global wealth manager, US arm",
  "CIO desk flagging concentration; client flows ignoring the flag — a classic wedge input"),
 ("Charles Schwab (platform)", "Retail brokerage + RIA custody platform",
  "retail margin balances elevated; platform data is the cleanest window into the L0 crowd"),
 ("Fidelity (platform)", "Retail + workplace platform giant",
  "401(k) default flows keep buying the index — the passive conveyor belt runs regardless of price"),
 ("Betterment", "Robo-advisor — algorithmic allocation for retail",
  "robo rebalancing is counter-cyclical by construction — a small, systematic κ-reducer"),
 ("JPMorgan Private Bank", "HNW channel of the universal bank",
  "structured-product demand on AI names rising — the derivative wrapper stage of a theme"),
]
L3 = [
 ("BlackRock", "Largest asset manager; iShares ETF complex",
  "index flows are the crowding's autopilot: inclusion weights, not views, set the marginal buy"),
 ("Vanguard", "Index giant — the passive conveyor",
  "flows structурally price-insensitive; the model treats passive as a field, not an agent with a view"),
 ("State Street GA", "Index manager + SPDR ETFs",
  "sector-SPDR creations in semis at highs — retail and advisor demand made visible in primary flows"),
 ("Capital Group", "Active long-only at scale",
  "active share drifting toward the benchmark's AI weight — career risk disciplines even conviction"),
 ("T. Rowe Price", "Active growth manager",
  "growth mandates fully invested in the theme; redemption sensitivity is the fragility to watch"),
 ("Citadel (hedge fund)", "Multi-strategy — the fast institutional money",
  "model-inferred: crowding metrics on memory names at internal limits; de-grossing has a trigger, not a date"),
 ("Millennium", "Multi-manager pod platform",
  "pod risk limits make de-grossing mechanical once vol rises — the κ-rotation transmission belt"),
 ("Point72", "Multi-strategy platform",
  "semis pods at sector-exposure caps (inferred from platform norms) — no room to add, room to cut"),
 ("Two Sigma", "Quant/systematic manager",
  "momentum sleeves long the theme by construction; the signal that built the wedge will also unwind it"),
 ("Renaissance", "The quant benchmark (Medallion external opacity)",
  "opaque by design; the model carries it as a high-turnover liquidity taker in the same field"),
 ("D.E. Shaw", "Quant + multi-strategy",
  "stat-arb books mean-revert; extended dislocations in memory pairs are inventory, not conviction"),
 ("AQR", "Systematic factor manager",
  "value sleeves short the theme's multiple expansion — the factor world's built-in skeptic"),
 ("Bridgewater", "Global macro at scale",
  "macro lens: an AI-capex cycle meeting a liquidity plateau — regime risk, not stock story"),
 ("Elliott", "Activist / event-driven",
  "event capital watches for the post-break restructuring, not the melt-up"),
 ("Blackstone", "Private markets — buyout/credit/real assets",
  "private valuations lag public manias; dry powder is the counter-cyclical reserve"),
 ("KKR", "Private markets platform",
  "deployment discipline read: public multiples too high to take companies out — a valuation signal in itself"),
 ("Apollo", "Private credit at scale",
  "private credit funds the capex boom one layer removed — exposure without the equity beta"),
]
L4 = [
 ("Goldman Sachs", "Full-stack investment bank; the flow-information node",
  "client-flow data is the market's best real-time census — model-inferred: institutional net selling of memory into strength since April"),
 ("Morgan Stanley (IB)", "Investment bank + research franchise",
  "sell-side semis coverage near max-bullish — a contrarian input the model weights explicitly"),
 ("JPMorgan (IB)", "Universal bank's markets division",
  "financing books (PB + swaps) show gross leverage on the theme at highs — the fuel gauge"),
 ("BofA Securities", "Bank sell-side / flows research",
  "its own flow monitors show retail buying vs. institutional distribution — the handoff pattern"),
 ("Citi (markets)", "Global markets division",
  "derivatives desks pricing rich call skew on semis — the options market is charging for the crowd"),
 ("Jefferies", "Mid-tier IB — sentiment barometer",
  "ECM calendar filling with AI-adjacent deals — issuance is how manias monetize themselves"),
 ("Robinhood", "Retail broker — the L0 crowd's order-flow gateway",
  "top-traded lists dominated by AI/memory names; PFOF exhaust makes the retail field measurable"),
 ("Interactive Brokers", "Active-trader broker",
  "margin loan growth tracking the theme — leverage in the retail field, the ν_η amplifier"),
 ("Goldman Prime", "Prime brokerage — the leverage ledger",
  "PB data = the closest thing to observing κ directly; crowding reports flagged memory names all spring"),
 ("TP ICAP", "Inter-dealer broker",
  "dealer-to-dealer risk transfer quiet — stress has not yet reached the plumbing layer"),
 ("Cantor Fitzgerald", "Dealer / Treasury specialist",
  "rates desks see no funding stress; whatever breaks will start as an equity-crowding event, not a funding one"),
]
PAR = [
 ("Citadel Securities", "Largest US equity market maker — the parallel layer's anchor",
  "internalizes a third of retail flow; its inventory is the shock absorber that will set the gap size"),
 ("Jane Street", "Global market maker / ETF arb",
  "ETF arb keeps index and single-name prices lashed together — the transmission cable of any unwind"),
 ("Virtu", "HFT market maker",
  "quoting is regime-dependent: liquidity that is deepest at the top thins exactly when needed (w₅)"),
 ("Jump Trading", "HFT / prop",
  "latency arms race irrelevant to the weekly story; matters enormously on capitulation day"),
 ("XTX Markets", "Quant market maker",
  "non-bank liquidity now prices most of the tape; its risk limits are undisclosed — a structural unknown"),
 ("Optiver", "Options market maker",
  "vol desks short the rich call skew retail buys — positioned to profit from the crowd twice"),
 ("SIG (Susquehanna)", "Options/prop firm",
  "the options complex is where the wedge's leverage hides; gamma profiles steepen into the break"),
 ("DRW", "Prop trading across assets",
  "prop capital has no client-redemption channel — the only truly discretionary money at this layer"),
]
L5 = [
 ("NYSE", "Primary listing venue",
  "auction volumes orderly; the venue layer is a thermometer, not an actor — until halts matter"),
 ("Nasdaq", "Where the AI complex trades",
  "memory names' share of tape at cycle highs — concentration of volume mirrors concentration of belief"),
 ("CME", "Futures & options exchange",
  "equity-index futures open interest at highs — the macro hedging layer is active even as cash chases"),
 ("CBOE", "Options exchange — the vol venue",
  "0DTE activity on semis elevated; the crowd's timeframe is compressing, a late-cycle marker"),
 ("IEX", "Alternative venue",
  "speed-bump venues gain share when adverse selection rises — a microstructure canary"),
 ("DTCC", "Clearing & settlement core (NSCC/DTC)",
  "settlement volumes at records; the plumbing is sized for stress the price layer hasn't priced yet"),
 ("OCC (options clearing)", "Options CCP",
  "margin models will procyclically tighten on the first vol spike — a mechanical accelerant the model includes"),
 ("BNY Mellon", "World's largest custodian",
  "custody sees positions, not intentions; its lending desk sees shorts building — slowly"),
 ("State Street (custody)", "Custodian + securities lending",
  "sec-lending utilization on memory names creeping up — informed dissent is expensive but present"),
 ("Fedwire", "The dollar's settlement rail",
  "no stress observable at the money layer — this is an equity-crowding episode, not (yet) a funding one"),
]
L6 = [
 ("US Treasury (issuance)", "The risk-free curve's supplier",
  "coupon sizes set the gravity every risky asset trades against; steady issuance = stable backdrop"),
 ("Micron", "US memory issuer — HBM cycle epicenter (US-listed)",
  "trading at cycle-high multiples on HBM scarcity narrative; the equilibrium track sits far below spot (see MVP)"),
 ("Western Digital", "Storage issuer",
  "NAND pricing narrative extended; capex guidance the next Mode-I event on the calendar"),
 ("SanDisk", "NAND pure-play (post-spinoff)",
  "highest-beta member of the basket — the wedge's amplifier and, later, its fastest casualty"),
 ("Seagate", "HDD/storage issuer",
  "the 'old storage' discount vs. AI-storage premium is itself a crowding measurement"),
 ("NVIDIA", "The AI complex's anchor issuer",
  "the gravitational center the memory trade orbits; its guidance moves the whole field's μ"),
 ("Apple (issuer)", "Mega-cap issuer (dual role with treasury)",
  "boring is information: the non-AI mega-caps are the market's implicit hedge"),
 ("Fannie Mae", "MBS issuance machine",
  "securitization keeps household credit flowing back into markets — the L6→L0 loop closed"),
 ("Tesla", "Retail-favorite issuer",
  "shares retail attention with the AI complex — attention is the scarce resource μ_retail allocates"),
]
RING1 = [
 ("MSCI", "Index provider — the shadow allocator",
  "index weights ARE the passive allocation; a rebalance date moves more money than most active views"),
 ("S&P DJI", "Index provider (S&P 500)",
  "inclusion mechanics turned the memory rally into forced passive buying — rule-driven flow, fully modelable"),
 ("Moody's", "Rating agency",
  "credit lens quiet on the equity mania — ratings constrain the debt channel, not the crowding"),
 ("S&P Global Ratings", "Rating agency",
  "no rating actions pending on the basket; the rules ring is silent, which is itself a reading"),
 ("Bloomberg", "The market's shared information surface",
  "terminal-chat consensus is a homogenization channel for professionals — the institutional c_t"),
 ("FactSet", "Data/analytics vendor",
  "everyone screens the same factors on the same data — correlated discovery, correlated exit"),
 ("GLG (expert networks)", "Where channel checks are bought",
  "expert-call volume on HBM supply chains spiked through spring — information asymmetry's retail entrance is here"),
 ("ISS", "Proxy advisor",
  "governance ring orthogonal to this episode; included because the map is complete, not because it moves"),
 ("CNBC / financial media", "The retail information surface",
  "airtime share of AI-memory stories at highs — media attention lags smart money, leads retail money"),
 ("WSJ / financial press", "Agenda-setting press",
  "the narrative layer: by the time crowding is a headline, the informed are already rotating"),
]
RING2 = [
 ("Federal Reserve", "Monetary anchor · lender of last resort",
  "policy path data-dependent; the Fed put exists below, far below, the current tape"),
 ("SEC", "Securities regulator",
  "13F/short-interest disclosure cadence defines what the public can see, and when — the information clock"),
 ("CFTC", "Derivatives regulator",
  "futures positioning data (COT) is one of E7's ground truths — the regulator as data source"),
 ("FINRA", "Broker SRO",
  "margin statistics published monthly — the retail leverage gauge, weeks delayed"),
 ("FDIC", "Deposit insurance",
  "banking layer calm; no deposit channel to this episode"),
 ("OCC (bank regulator)", "National bank supervisor",
  "bank capital rules cap dealer balance sheets — a hard constraint on liquidity provision in a break"),
 ("SIPC", "Broker-failure insurance",
  "invisible until it matters; part of the confidence floor under retail participation"),
 ("BIS", "Central banks' central bank",
  "quarterly reviews flagged AI-equity concentration globally — the rules ring can see wedges too"),
]

# ── build nodes ────────────────────────────────────────────────────────────────
def build_layer(items, lvl, size):
    idxs = []
    n = len(items)
    for k, (name, role, read) in enumerate(items):
        p = col_pos(lvl, k, n)
        idxs.append(add(p, lvl, size, name, [role, m1(read), LAM_FACT if lvl in (3, 6) and k < 2 else
                                             f"Layer {CHIP[lvl]} · {LAYER_NAME[lvl]}"]))
    return idxs

I0 = build_layer(L0, 0, 0.030)
I1 = build_layer(L1, 1, 0.026)
I2 = build_layer(L2, 2, 0.024)
I3 = build_layer(L3, 3, 0.028)
I4 = build_layer(L4, 4, 0.026)
I5 = build_layer(L5, 5, 0.026)
I6 = build_layer(L6, 6, 0.028)

IP = []
for k, (name, role, read) in enumerate(PAR):
    a = 2 * np.pi * k / len(PAR)
    p = np.array([1.35 + 0.5 * np.cos(a), 1.55 + 0.18 * np.sin(2*a), 0.5 * np.sin(a)])
    IP.append(add(p, 7, 0.024, name, [role, m1(read), "Parallel layer · own capital only · interfaces at L4–L5"]))

IR1, IR2 = [], []
for k, (name, role, read) in enumerate(RING1):
    a = 2 * np.pi * k / len(RING1) + 0.3
    p = np.array([2.9 * np.cos(a), 1.95, 1.5 * np.sin(a)])
    IR1.append(add(p, 8, 0.024, name, [role, m1(read), "Outer ring 1 · information & pricing — touches no money, steers it"]))
for k, (name, role, read) in enumerate(RING2):
    a = 2 * np.pi * k / len(RING2) + 0.8
    p = np.array([2.9 * np.cos(a), -1.95, 1.5 * np.sin(a)])
    IR2.append(add(p, 9, 0.026, name, [role, m1(read), "Outer ring 2 · rules & last resort — spans every layer"]))

NIDX = {n: i for i, n in enumerate(NAME)}

# retail field cloud around L0
CLOUD = []
for _ in range(420):
    v = rng.normal(size=3); v /= np.linalg.norm(v)
    p = np.array([LX[0], 0, 0]) + v * (1.05 + 0.25 * rng.random())
    p[0] = LX[0] + rng.normal(-0.25, 0.22)
    CLOUD.append([round(float(p[0]), 3), round(float(p[1]), 3), round(float(p[2]), 3)])

# ── edges with per-edge May-1 stories ─────────────────────────────────────────
E, ESTORY = [], []
def edge(a, b, title, lines):
    E.append([NIDX[a], NIDX[b]])
    ESTORY.append({"t": f"{a} ↔ {b}", "c": "edge",
                   "l": [title] + lines + [f"— model-inferred snapshot · {SNAP} · illustrative"]})

def tmpl_edge(a, b, kind):
    T = {
      "fund":      ("Funding channel", [f"{a} money becomes {b} mandates.",
                    m1("drift-overweight in the AI complex passes down this pipe unexamined — allocation inertia is the wedge's permission slip")]),
      "gate":      ("Mandate gatekeeping", [f"{b} advises where {a}'s capital goes; no orders, all influence.",
                    m1("no mandate churn — gatekeeper inertia keeps crowded managers funded")]),
      "mandate":   ("Management mandate", [f"{a} capital sits in {b} vehicles.",
                    m1("the owner is drift-overweight semis via this mandate; a rebalance instruction here is mechanical selling of the theme")]),
      "pb":        ("Prime brokerage / leverage", [f"{b} finances {a}'s gross book and sees every position.",
                    m1("crowding reports on memory names circulated all spring — the informed layer knows it is crowded and stays anyway")]),
      "exec":      ("Execution & listing", [f"Order flow from {a} prints on {b}.",
                    m1("volume concentration in AI/memory names at venue highs")]),
      "clear":     ("Clearing & settlement", [f"{a}'s trades settle through {b}.",
                    m1("volumes at records; procyclical margin is the hidden accelerant in a break")]),
      "underwrite":("Underwriting relationship", [f"{a} runs {b}'s capital-markets access.",
                    m1("issuance windows wide open — manias are monetized through this edge")]),
      "index":     ("Index-tracking obligation", [f"{a} weights dictate {b}'s buying, price-blind.",
                    m1("inclusion mechanics converted the memory rally into forced passive demand")]),
      "info":      ("Information surface", [f"{a} sets what {b} (and everyone) sees first.",
                    m1("attention share of the AI-memory story at highs — narrative lag structures who sells to whom")]),
      "reg":       ("Regulatory constraint", [f"{a} writes the constraint set {b} optimizes inside.",
                    m1("the constraint module is the weight-sharing NNGS imposes: same regulator, same feasible set")]),
      "retailflow":("Retail order flow", [f"{a}'s crowd trades through {b}.",
                    m1("top-traded lists = the AI complex; the legible crowd is fully engaged")]),
      "mm":        ("Liquidity provision", [f"{b} makes the market {a} trades in.",
                    m1("depth is regime-dependent — the w₅ coupling: inventory limits set the gap size when the crowd turns")]),
      "macro":     ("Policy transmission", [f"{a} sets the discount curve {b} prices against.",
                    m1("data-dependent path; the policy put sits far below the current tape")]),
    }
    t, lines = T[kind]
    edge(a, b, t, lines)

# chain: L0 → L1 / platforms
for owner in ["CalPERS", "CalSTRS", "NY State Common", "MetLife", "Prudential Financial"]:
    tmpl_edge("US households (aggregate)", owner, "fund")
tmpl_edge("US households (aggregate)", "Charles Schwab (platform)", "retailflow")
tmpl_edge("US households (aggregate)", "Fidelity (platform)", "retailflow")
tmpl_edge("US retail cohort (self-directed)", "Robinhood", "retailflow")
tmpl_edge("US retail cohort (self-directed)", "Interactive Brokers", "retailflow")
tmpl_edge("Treasury General Account", "Federal Reserve", "macro")
tmpl_edge("Foreign official inflows (aggregate)", "US Treasury (issuance)", "fund")

# L1 → L2 (gatekeepers)
for owner, gk in [("CalPERS", "Mercer"), ("CalSTRS", "Mercer"), ("NY State Common", "Aon"),
                  ("Harvard endowment", "Cambridge Associates"), ("Yale endowment", "Cambridge Associates")]:
    tmpl_edge(owner, gk, "gate")

# L1 → L3 (mandates)
for owner, mgr in [("CalPERS", "BlackRock"), ("CalPERS", "Blackstone"), ("CalSTRS", "Vanguard"),
                   ("NY State Common", "State Street GA"), ("GPIF (US sleeve)", "BlackRock"),
                   ("Norway GPFG (US sleeve)", "Vanguard"), ("GIC (US sleeve)", "KKR"),
                   ("MetLife", "Apollo"), ("Prudential Financial", "T. Rowe Price"),
                   ("Harvard endowment", "Bridgewater"), ("Yale endowment", "Elliott")]:
    tmpl_edge(owner, mgr, "mandate")

# L2 → L3
for gk, mgr in [("Mercer", "Capital Group"), ("Aon", "AQR"), ("Cambridge Associates", "Two Sigma"),
                ("Morgan Stanley Wealth Mgmt", "BlackRock"), ("Merrill (BofA) Wealth", "Capital Group"),
                ("UBS Wealth USA", "T. Rowe Price"), ("Betterment", "Vanguard"),
                ("JPMorgan Private Bank", "Blackstone")]:
    tmpl_edge(gk, mgr, "mandate")

# L3 → L4 (prime / execution)
for mgr, bank in [("Citadel (hedge fund)", "Goldman Prime"), ("Millennium", "Goldman Prime"),
                  ("Point72", "JPMorgan (IB)"), ("Two Sigma", "Morgan Stanley (IB)"),
                  ("Renaissance", "BofA Securities"), ("D.E. Shaw", "Goldman Sachs"),
                  ("AQR", "Citi (markets)"), ("Bridgewater", "JPMorgan (IB)"),
                  ("BlackRock", "BofA Securities"), ("Vanguard", "Jefferies")]:
    tmpl_edge(mgr, bank, "pb")

# L4 → L5
for bank, infra in [("Goldman Sachs", "NYSE"), ("Morgan Stanley (IB)", "Nasdaq"),
                    ("JPMorgan (IB)", "CME"), ("Citi (markets)", "CBOE"),
                    ("Robinhood", "Nasdaq"), ("Interactive Brokers", "IEX"),
                    ("BofA Securities", "DTCC"), ("Goldman Prime", "OCC (options clearing)"),
                    ("Jefferies", "DTCC"), ("Cantor Fitzgerald", "Fedwire"),
                    ("TP ICAP", "CME")]:
    tmpl_edge(bank, infra, "clear" if infra in ("DTCC", "OCC (options clearing)", "Fedwire") else "exec")

# custody
for mgr, cust in [("BlackRock", "BNY Mellon"), ("Vanguard", "State Street (custody)"),
                  ("Capital Group", "BNY Mellon")]:
    tmpl_edge(mgr, cust, "clear")

# L4/L5 → L6 (underwriting & listing)
for bank, iss in [("Goldman Sachs", "Micron"), ("Morgan Stanley (IB)", "Western Digital"),
                  ("JPMorgan (IB)", "SanDisk"), ("BofA Securities", "Seagate"),
                  ("Citi (markets)", "Fannie Mae"), ("Jefferies", "Tesla"),
                  ("Goldman Sachs", "NVIDIA")]:
    tmpl_edge(bank, iss, "underwrite")
for iss, venue in [("Micron", "Nasdaq"), ("NVIDIA", "Nasdaq"), ("Tesla", "Nasdaq"),
                   ("Western Digital", "Nasdaq"), ("Apple (issuer)", "Nasdaq"),
                   ("US Treasury (issuance)", "Fedwire")]:
    tmpl_edge(iss, venue, "exec")

# parallel layer
for pf, venue in [("Citadel Securities", "Nasdaq"), ("Jane Street", "NYSE"), ("Virtu", "NYSE"),
                  ("Jump Trading", "CME"), ("XTX Markets", "Nasdaq"), ("Optiver", "CBOE"),
                  ("SIG (Susquehanna)", "CBOE"), ("DRW", "CME")]:
    tmpl_edge(pf, venue, "mm")
tmpl_edge("Robinhood", "Citadel Securities", "retailflow")
tmpl_edge("Charles Schwab (platform)", "Citadel Securities", "retailflow")
tmpl_edge("Jane Street", "BlackRock", "mm")

# information ring
for src, dst in [("MSCI", "BlackRock"), ("MSCI", "State Street GA"), ("S&P DJI", "Vanguard"),
                 ("Bloomberg", "Goldman Sachs"), ("Bloomberg", "Citadel (hedge fund)"),
                 ("FactSet", "AQR"), ("GLG (expert networks)", "Point72"),
                 ("GLG (expert networks)", "Citadel (hedge fund)"),
                 ("CNBC / financial media", "US retail cohort (self-directed)"),
                 ("WSJ / financial press", "US households (aggregate)"),
                 ("Moody's", "US Treasury (issuance)"), ("S&P Global Ratings", "Fannie Mae"),
                 ("ISS", "BlackRock")]:
    tmpl_edge(src, dst, "index" if src in ("MSCI", "S&P DJI") else "info")

# rules ring
for reg, tgt in [("Federal Reserve", "JPMorgan (IB)"), ("Federal Reserve", "US Treasury (issuance)"),
                 ("SEC", "NYSE"), ("SEC", "Robinhood"), ("SEC", "Citadel Securities"),
                 ("SEC", "BlackRock"), ("CFTC", "CME"), ("FINRA", "Interactive Brokers"),
                 ("FINRA", "Charles Schwab (platform)"), ("FDIC", "JPMorgan Private Bank"),
                 ("OCC (bank regulator)", "Goldman Sachs"), ("SIPC", "Robinhood"),
                 ("BIS", "Federal Reserve")]:
    tmpl_edge(reg, tgt, "macro" if reg == "Federal Reserve" else "reg")

# ── the memory-crowding thread (orange) — hand-written May-1 chain ─────────────
def thread_edge(a, b, title, lines):
    edge(a, b, title, lines)
    return len(E) - 1

TH = []
TH.append(thread_edge("GLG (expert networks)", "Citadel (hedge fund)",
    "Information asymmetry's entry point (w₁)",
    ["Channel checks on HBM supply chains reach paying institutions first.",
     m1("expert-call volume on memory supply spiked through spring; what retail will read in July, this edge priced in spring")]))
TH.append(thread_edge("Citadel (hedge fund)", "Goldman Prime",
    "The leverage ledger sees the rotation (κ)",
    ["PB data shows gross exposure and its direction — before any filing.",
     m1("crowding flagged at internal limits; de-grossing is armed, awaiting a trigger — the κ-rotation half of the MVP signal")]))
TH.append(thread_edge("Two Sigma", "Micron",
    "Systematic momentum holds the wedge (w₂ arming)",
    ["Momentum sleeves are long because price went up — reflexivity in institutional form.",
     m1("the same signal that built the position will command the exit; symmetric, fast, and crowded")]))
TH.append(thread_edge("CNBC / financial media", "US retail cohort (self-directed)",
    "The late information surface (w₃)",
    ["Attention flows to what already moved; retail buys the chart's past.",
     m1("AI-memory airtime at highs — μ_retail concentration rising exactly as the informed prepare to rotate")]))
TH.append(thread_edge("US retail cohort (self-directed)", "Robinhood",
    "The crowd's order-flow gateway (w₄)",
    ["Retail flow holds the wedge up after institutions stop adding.",
     m1("top-traded lists all memory; the wedge's last owners are arriving through this edge")]))
TH.append(thread_edge("Robinhood", "Citadel Securities",
    "Where the crowd meets inventory (w₅)",
    ["Internalized retail flow ends at market-maker inventory limits.",
     m1("inventory absorbs the chase for now; on capitulation day this edge sets the gap size")]))
TH.append(thread_edge("Citadel Securities", "SanDisk",
    "The amplifier at the end of the chain",
    ["Highest-beta basket member; thinnest book relative to attention.",
     m1("the model's fragility ranking puts the post-spinoff pure-play first when the field turns")]))

# red constraint cascade: Fed → banks → dealers → liquidity
REDCHAIN = []
for a, b in [("Federal Reserve", "OCC (bank regulator)"), ("OCC (bank regulator)", "Goldman Sachs"),
             ("Goldman Sachs", "Goldman Prime"), ("Goldman Prime", "Citadel (hedge fund)")]:
    REDCHAIN.append([NIDX[a], NIDX[b]])

payload = {
    "snap": SNAP,
    "pos": P, "size": SIZE, "lvl": LVL, "story": STORY,
    "edges": E, "estory": ESTORY,
    "thread": TH,               # indices into edges: the orange memory thread
    "red": REDCHAIN,
    "cloud": CLOUD,
    "layers": [[l, LX.get(l, None), CHIP[l], LAYER_NAME[l]] for l in range(7)],
}
with open(os.path.join(OUT, "data.js"), "w") as f:
    f.write("window.MW_DATA = " + json.dumps(payload, separators=(",", ":")) + ";")
print(f"✓ docs/data.js  nodes={len(P)} edges={len(E)} cloud={len(CLOUD)}",
      f"size={os.path.getsize(os.path.join(OUT,'data.js'))//1024}KB")

# ── static preview card for the README ─────────────────────────────────────────
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLS = {0: "#0B1F3A", 1: "#1D4ED8", 2: "#60A5FA", 3: "#2563EB", 4: "#7C3AED",
        5: "#F97316", 6: "#059669", 7: "#D97706", 8: "#DB2777", 9: "#DC2626"}
Pn = np.array(P); lvl = np.array(LVL)
fig = plt.figure(figsize=(13.4, 8.0), dpi=150)
axp = fig.add_axes([0.02, 0.00, 0.96, 0.86], projection="3d")
axp.set_facecolor("#FBFBFC"); fig.patch.set_facecolor("#FBFBFC")
for (a, b) in E:
    axp.plot(*zip(Pn[a], Pn[b]), color="#C9CDD4", lw=0.35, alpha=0.35)
for k in TH:
    a, b = E[k]
    axp.plot(*zip(Pn[a], Pn[b]), color="#D97706", lw=2.4, alpha=0.95)
cl = np.array(CLOUD)
axp.scatter(*cl.T, s=1.2, c="#9AA1AC", alpha=0.5, linewidths=0)
for l in range(10):
    m = lvl == l
    if m.any():
        axp.scatter(*Pn[m].T, s=46 if l in (0, 3, 6) else 30, c=COLS[l],
                    alpha=0.95, linewidths=0)
axp.set_axis_off(); axp.set_box_aspect((2.2, 1.1, 1.0))
axp.view_init(elev=14, azim=-70)
fig.text(0.045, 0.945, "The Layered US Market — interactive 3D · snapshot 2026-05-01",
         fontsize=18, fontweight="bold", color="#111827")
fig.text(0.045, 0.895, "capital-flow layers 0–6 · prop/HFT parallel layer · information & rules rings — "
         "every node a real institution; click any node or edge for its May-1 reading",
         fontsize=10.5, color="#6B7280")
fig.text(0.5, 0.06, "▶  O P E N   I N T E R A C T I V E", fontsize=15,
         color="white", ha="center", fontweight="bold",
         bbox=dict(boxstyle="round,pad=0.55", facecolor="#2563EB", edgecolor="none"))
fig.savefig(os.path.join(FIGS, "network3d_preview.png"), facecolor="#FBFBFC")
print("✓ figures/network3d_preview.png")
