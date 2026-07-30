# MicroWorld — One Pager

**A world model for equity markets: model the players, not the patterns.**
*Alpha Flow Research · HongJin HE · HKUST / Stanford IHP · July 2026*
*[github.com/hongjin-he/MicroWorld](https://github.com/hongjin-he/MicroWorld) · MIT license*

---

**The problem.** Quantitative finance's dominant paradigm — factor mining
and time-series ML — extracts patterns from historical data. But historical
*data* does not repeat: every discovered signal is destroyed by its own
adoption (alpha half-life: ~6 years in 1990 → ~11 months in 2023). What
does repeat is the *structure* that generates the data: institutions,
regulations, incentives, the game.

**The approach.** MicroWorld models that structure directly: US equity
markets as a four-level hierarchical mean-field game — cross-market flows,
institution types, individual institutions, intra-institution desks — with
a 5-dimensional state space per asset, a dual decomposition of noise into
physical and behavioral components, and a 22-operator event algebra for
M&A/IPO/policy shocks. Predictions are equilibria, not extrapolations, so
they are designed to survive their own deployment. Seven theorems proved;
50 tests passing; every demo runs on a laptop with zero API keys.

**Validation to date.**
- **2008 hindcast, public data only:** the stability indicator Λₜ entered
  its sustained crisis regime on Aug 16, 2007 — **272 trading days before
  Lehman** — with zero false alarms in 2005–06. Same signal: Feb 20, 2020.
- **Synthetic product demo:** denoised equilibrium price flags a
  crowding-driven divergence ~2 weeks before a July-2026-shaped sector
  unwind ([demo](../demo/denoised_price_2026.py)); real-data version is
  specified as experiment E7.
- **Open-source traction:** 138+ GitHub stars in the first weeks, 17-notebook
  tutorial series, interactive 3D market universe.

**Two products, one engine.**
- **To-C — the denoised price.** The MFG equilibrium track P^eq and the
  divergence D_t = P/P^eq − 1: a mid/long-horizon positioning research
  signal for retail ("are you buying value or buying crowding?"). Not
  personalized advice; an instrument-level research layer.
- **To-B — structural risk early warning.** Λₜ regime monitoring, crowding
  decomposition, and event-operator scenario analysis for funds and risk
  desks — the 2008-grade signal, live (pipeline scaffolded: Airflow +
  Alpaca paper-trading).

**The moat.** Causal explainability. Factor and time-series shops find
patterns they cannot explain and therefore cannot defend when regimes
break. Every MicroWorld output is attributable to agents, constraints, and
equilibrium conditions — the model's explanation *is* the model. The
framework is also the only one simultaneously offering strategic agents,
universe-changing events, noise decomposition with an estimation bound,
crisis early-warning, and a four-level hierarchy.

**Roadmap.** Phase 1 (now): real-data validation E1–E7 → NeurIPS-2026
workshop paper + the E7 product exhibit (~one quarter, ~$25k inc. compute).
Phase 2: the Neural Network Game Structure — every neuron an agent-network,
regulatory constraints as architecture ([design doc](PHASE2_NEURAL_GAME.md));
pilots on one H100/H200, full campaign on an 8×H200 node (~$300k scenario).
Detail: [RESOURCES.md](../RESOURCES.md).

**The ask.** Data access (WRDS-grade), compute (H100/H200 hours), or
pre-seed partnership — priced by scenario in RESOURCES.md.

**Contact.** [LinkedIn](https://www.linkedin.com/in/hongjinhe-hkust-edu) ·
[GitHub](https://github.com/hongjin-he) · [X](https://x.com/Mr_Abstractor)

---

*This document describes research software. Nothing here is investment
advice or an offer of securities.*
