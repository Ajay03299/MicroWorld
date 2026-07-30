# Phase 2 — The Neural Network Game Structure (NNGS)

**Status: design document.** Nothing in this file is implemented, and that
is deliberate. Phase 2 begins when two resources exist that do not exist
today: the cleaned multi-type data panel and H200-class training compute
(see [RESOURCES.md](../RESOURCES.md)). Until then, this document is the
specification we hold ourselves to — written down in public, before the
hardware arrives, so the idea has a timestamp.

*[README](../README.md) · [The journey that led here](JOURNEY.md)*

---

## 1 · Why Phase 1 is a game-theory engine, not a neural network

Phase 1 — everything currently in this repository — solves the market as a
hierarchical mean-field game: coupled HJB–FPK systems, an operator algebra
for events, seven proven theorems. It is deliberately *mathematical
structure first, learning second*, for one reason: **data scarcity is not a
temporary inconvenience; at today's access level it is binding.** When you
cannot estimate millions of parameters, you must get the same behavior from
structure — and Theorem 1 (the dual Cramér-Rao bound) says something
stronger: part of the residual can *never* be estimated away with more
data, only explained by a model of the mechanism. Phase 1 is the
mechanism, written in PDEs because PDEs are what run on a laptop.

So the honest description of the current stage is: **the game-theoretic
core is the data-efficient regime of the world model.** It is not the
final form.

## 2 · The Phase 2 thesis: neurons that play, not neurons that fire

Everyone else who models markets builds a mathematical model *of* the
agents. Phase 2 builds the agents *as the network*:

> **A neural network in which each neuron is itself a small neural
> network — one per institution or retail cohort — with its own objective,
> its own information set, and its own strategy. The connections between
> neurons are not weights that passively mix signals; they are strategic
> couplings: each unit's forward pass is a best response to the others.
> We call this the Neural Network Game Structure (NNGS).**

The units are, in a precise sense, *personified*: a neuron here does not
"fire", it *decides*. Where a GNN node aggregates its neighbors' messages,
an NNGS node responds to its neighbors' strategies — the difference between
diffusion and game play. This is the same distinction that separates this
repo from swarm models (see the MicroFish comparison in the README), now
pushed down into the architecture itself.

### Two representational choices, both admissible

1. **Agents-as-neurons (the primary design).** Each of the ~11 agent
   classes (6 institutional + 5 retail, [`agents/`](../agents/)) is
   instantiated as a population of small networks, fully connected across
   the graph, each carrying its own recurrent state.
2. **Levels-as-layers (the fallback).** The four levels L0–L3 become four
   layers of one large network, with within-layer competition expressed via
   lateral connections. Coarser, cheaper, less faithful — but trainable
   sooner.

These are two encodings of the same object; which one wins is an empirical
question (experiment **E9** below), not an aesthetic one.

## 3 · The constraint structure — why this is not a free-form black box

An unconstrained network-of-networks would forfeit the one thing Phase 1
paid for: interpretability. NNGS keeps it through **constraints that are
facts about the world, imposed as architecture**:

- **Regulatory weight sharing.** All agents of one type live under the same
  regulator — every bank under Basel III, every mutual fund under UCITS/40-Act
  limits, every insurer under Solvency-style capital rules. Architecturally:
  agents of a type share a constraint module (projection layer onto the
  feasible set), exactly as the Phase 1 taxonomy shares Merton-style
  constraint sets. The shared module *is* the regulator.
- **Budget and leverage feasibility** as hard projection layers, not soft
  penalties — an agent cannot learn its way out of a balance sheet.
- **Information stratification** ([`state/information.py`](../state/information.py)):
  each neuron sees only its type's filtration. A retail cohort cannot
  attend to order-flow features it would not observe in reality.
- **The mean-field anchor.** The Phase 1 equilibrium is retained as a
  regularizer: population-level statistics of NNGS play must stay within a
  Wasserstein ball of the MFG equilibrium μ*, unless data demands
  otherwise. Phase 1 becomes the prior; Phase 2 the posterior.

The result is a *constrained* neural network whose every departure from
equilibrium is attributable — to an agent type, a constraint, or an
information set. Explanations survive the scaling-up.

## 4 · One network or two? — an experiment, not a debate

Two candidate macro-architectures:

| | **A — Unified** | **B — Dual (environment + population)** |
|---|---|---|
| Structure | One network: agents and environment dynamics entangled in a single graph | Network 1: a trained environment/world model (the neuralized **E**). Network 2: the population of agent-neurons playing inside it (the neuralized **Game**) |
| Lineage | End-to-end world models (Dreamer-style) | E-Game-C itself — B is its native neuralization |
| Risk | Attribution becomes murky; environment leaks into strategy | Interface mismatch: the population's actions must feed back into the environment model consistently (reflexivity must close the loop) |
| Prior | — | Phase 1 MFG initializes Network 2; the Phase 1 encoder initializes Network 1 |

Design B is the default because it inherits E-Game-C directly and keeps the
reflexivity loop explicit (price-belief feedback as the interface between
the two networks). But the choice is assigned to experiment **E8**, run
first at toy scale — the answer we publish will be measured, not asserted.

## 5 · The complexity wall — and the four tools against it

Honesty first: training a model whose parameters are themselves models
roughly **squares the training difficulty**. N agents with pairwise
strategic coupling is O(N²) in interactions before anything recurses, and
each unit's learning signal depends on every other unit's current policy —
the non-stationarity that makes multi-agent RL notoriously unstable, at a
scale multi-agent RL has not attempted. This is exactly why Phase 2 waits
for hardware, and why the design leans on four reductions:

1. **Mean-field factorization.** Within a type, agents couple to the
   *distribution* of their type, not to each individual — O(N²) → O(N·K)
   for K types. This is not an approximation bolted on: Phase 1 *proved*
   (Theorem 7.4, propagation of chaos) that it is the correct N→∞ limit.
2. **Latent agent embeddings.** Each neuron's policy conditions on a
   low-dimensional embedding of its identity (d ≈ 16–64), so populations
   share one policy network modulated per agent — the DreamerV3 trick of
   one configuration spanning many domains, applied within one market.
3. **Hierarchy as curriculum.** Train L1 (type-level) frozen-environment
   first, unfreeze L2 (institution-level), then L3 — the four-level
   structure is not just descriptive, it is the training schedule.
4. **Sparse strategic attention.** Full connectivity is the specification,
   not the runtime: a learned top-k attention over counterparties captures
   the empirically sparse strategic graph (a fund responds to its actual
   competitors, not to all 50,000 institutions).

## 6 · Compute and data triggers

- **Compute.** The E8/E9 toy-scale ablations run on a single H100/H200.
  A credible full-scale L1+L2 NNGS train (≈10³ neuron-networks, each
  10⁵–10⁶ parameters, adversarial co-training) is an H200-cluster problem
  — the training-run budget lives in [RESOURCES.md](../RESOURCES.md).
- **Data.** The cleaned, typed panel of DATA_REQUIREMENTS.md (13F/COT
  positioning for institutional ground truth, the E5 LLM-query atlas for
  retail policy priors). NNGS without agent-level ground truth would be a
  simulator, not a world model.

## 7 · Phase 2 experiments

Continuing the E-numbering from [DATA_REQUIREMENTS.md](../DATA_REQUIREMENTS.md)
(E1–E6) and [RESOURCES.md](../RESOURCES.md) (E7):

| ID | Experiment | Question it settles | Scale |
|---|---|---|---|
| **E8** | Unified vs dual architecture on the synthetic market ([`demo/synthetic_market.py`](../demo/synthetic_market.py)) | One network or two? | 1 GPU |
| **E9** | Agents-as-neurons vs levels-as-layers, same data, same budget | Which encoding of the game? | 1 GPU |
| **E10** | MFG-distillation: initialize NNGS from the Phase 1 equilibrium vs cold start | Is Phase 1 a useful prior (we predict: decisively yes)? | 1 GPU → cluster |
| **E11** | Constrained vs unconstrained NNGS on real panel | Do the regulatory constraints help or hurt fit? (The thesis: they *are* the alpha) | cluster |

## 8 · The larger claim

If NNGS works for markets, nothing about it is market-specific. Any
real-world graph whose nodes have objectives — supply chains, electricity
markets, ecosystems of platforms, geopolitical blocs — admits the same
construction: **model each node as a small neural network with a stake,
and the graph as their game.** Markets are simply the best first target:
the players are catalogued, the constraints are written law, and the
scoreboard prints every millisecond.

That is the Phase 2 bet. The mathematics of Phase 1 is how we earn the
right to place it.

---

*Questions, objections, or compute to offer: see
[Partnerships](../README.md#partnerships--contact).*
