# RESOURCES — What This Project Needs, Priced

Two things stand between the current repository and a validated instrument:
**cleaned data** and **training compute**. This file prices both. It is
simultaneously the project's internal shopping list and — for a potential
partner or investor — the use-of-funds statement. Experiment-level detail
for the data lives in [DATA_REQUIREMENTS.md](DATA_REQUIREMENTS.md); the
Phase 2 architecture that consumes the compute lives in
[docs/PHASE2_NEURAL_GAME.md](docs/PHASE2_NEURAL_GAME.md).

---

## 1 · Pillar one: cleaned, *typed* data

The framework does not want "more data" — it wants **each agent type's
behavior observed at the level that type actually acts**. That is a
different shopping list from a factor shop's, organized by which term of
the model each stream feeds:

| Agent type / model term | Data | Source | Cost tier |
|---|---|---|---|
| Physical vs behavioral noise (Thm 1) | Intraday trades & quotes, 500 equities × 10 yr | WRDS TAQ / Polygon | academic access / ~$2k·yr |
| Event operators (all 22) | Corporate actions, M&A, IPO, delistings, earnings | CRSP + SDC + I/B/E/S | academic access |
| Institutional mean field μ* (L1–L2) | Quarterly 13F holdings, futures COT positioning | EDGAR (free) + CFTC (free) | free |
| Retail cohort policies (Day 16) | **The E5 LLM query atlas** — stratified audit of consumer AI investment advice; the dataset exists nowhere and we create it | consumer LLM APIs | ~$200 |
| Funding / stress channel (Λₜ) | FRED spreads, FINRA margin, OFR indices, CBOE | public | free |
| Cross-market L0 | TIC flows, dollar indices | public | free |
| Alt-data layer (later) | News embeddings, positioning surveys | vendor | deferred |

**The punchline stays the same as DATA_REQUIREMENTS.md:** experiments
E1 + E2 + E4 + E5 — enough for the first real-data paper — are executable
in one quarter by one person inside any research group with WRDS access
plus about **$200** of API budget. The scarce resource is access, not money.

### E7 — the real-data denoised-price validation (To-C line)

The synthetic concept demo ([`demo/denoised_price_2026.py`](demo/denoised_price_2026.py))
graduates to a real-data experiment:

> **E7.** Reconstruct the denoised equilibrium track P^eq for the memory
> sector through the July 2026 unwind (SOX −19%, worst month since 2008)
> using only point-in-time data: prices (CRSP/Polygon), institutional
> positioning (13F + COT), retail-flow proxies, and the E5 retail-AI
> kernel. Measure: did divergence D_t cross threshold, with the
> institutional field rotating out, materially before July 24? Deliverable:
> a walk-forward figure exactly like the 2008 hindcast — same honesty
> rules, no look-ahead.

Data unlock: same as E1–E3 (nothing new to buy). Priority: **P0 for the
product line** — this is the first exhibit any retail-facing partner will
ask for. A first price-only step already ships in the repo:
[`demo/hindcast_memory_2026.py`](demo/hindcast_memory_2026.py) replays the
frozen 2008 Λₜ recipe on real vendored memory-sector data (alarm
2025-10-22, 232 trading days before the July 2026 capitulation — and the
basket rose another +446% first, which is precisely why E7's κ-rotation
half is needed).

## 2 · Pillar two: training compute

Phase 1 (everything in this repo) runs on a laptop; that was the point.
Phase 2 — the [Neural Network Game Structure](docs/PHASE2_NEURAL_GAME.md),
where every neuron is itself a small network — is where the compute bill
arrives. Costs below are honest ranges at mid-2026 cloud prices, not
precision estimates:

| Stage | What runs | Hardware | Est. cost |
|---|---|---|---|
| Phase 1 (today) | HJB–FPK solvers, demos, 50 tests | laptop / free Colab | ~$0 |
| Real-data Phase 1 (E1–E7) | Encoder training on real panel, walk-forward backtests | 1× consumer GPU or A100 spot | $1–3k |
| Phase 2 pilots (E8–E10) | Architecture ablations on synthetic market, ~10² agent-networks | 1× H100/H200 | $5–15k |
| Phase 2 full train (E11) | L1+L2 NNGS: ~10³ neuron-networks × 10⁵–10⁶ params, adversarial co-training + reflexivity loop | **8× H200 node, weeks-scale runs** | $100–250k per campaign |
| Type 2 sandbox (Horizon 3+) | Agent-level "capitalism simulator" disciplined by the Type 1 equilibrium | multi-node cluster | deferred until E11 says it's earned |

Why it squares: each unit's learning signal depends on every other unit's
current policy (non-stationary co-training), and the units themselves are
models — see the complexity-wall section of the
[Phase 2 design doc](docs/PHASE2_NEURAL_GAME.md#5--the-complexity-wall--and-the-four-tools-against-it)
for the four reductions (mean-field factorization, latent embeddings,
hierarchy-as-curriculum, sparse strategic attention) that keep the bill in
five figures for pilots rather than seven.

## 3 · Use of funds, by scenario

| Scenario | Budget | Buys |
|---|---|---|
| **Bootstrap** (status quo) | ~$500 | E5 atlas ($200) + Polygon starter + misc. Everything else free/academic. |
| **Seed research grant** | ~$25k | All of the above + real-data Phase 1 (E1–E7) + Phase 2 pilots (E8–E10) on rented H100/H200. Output: the NeurIPS-workshop paper *and* the E7 product exhibit. |
| **Partner / pre-seed** | ~$300k | One full NNGS training campaign (E11) + one year of data subscriptions + paper-trading infrastructure live (Airflow + Alpaca, already scaffolded in [`online/`](online/)). |

No headcount is priced in: the maintainer cost of this project is one
student who refuses to stop.

---

*Offering access, compute, or capital: see
[Partnerships & Contact](README.md#partnerships--contact) — or open an
issue.*
