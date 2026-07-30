# The Journey — From World-Model Skeptic to This Repository

*HongJin HE · Alpha Flow Research · July 2026*

*[README](../README.md) · [中文](../README_CN.md)*

---

## I did not believe in world models

For a long time I thought "world model" was a marketing term, and I had two
objections that felt unanswerable.

**The precision objection.** Quantum mechanics puts a hard floor under how
precisely the state of a physical system can be known — and chaotic dynamics
amplify any microscopic uncertainty exponentially. If you cannot pin down the
state, how can you claim to model the world that generates it?

**The storage objection.** Even granting perfect knowledge, a faithful
simulation of the world explodes combinatorially. Every naive estimate of
"simulate the environment" lands orders of magnitude beyond any hardware
roadmap. A world model, I concluded, was either a toy or a fantasy.

I was wrong about both — but it took watching three fields succeed in
parallel to see why.

## What changed my mind

**Robots that dream.** The lineage that started with Ha & Schmidhuber's
[World Models](https://worldmodels.github.io/) (2018) — an agent learning
inside its own compressed dream of the environment — became Hafner's
[Dreamer](https://arxiv.org/abs/1912.01603) line, and by
[DreamerV3](https://github.com/danijar/dreamerv3) (2023) a single
configuration was mastering 150+ domains from pixels. The result that
genuinely shook me was
[DayDreamer](https://danijar.com/project/daydreamer/) (Wu, Escontrela,
Hafner, Abbeel & Goldberg, CoRL 2022): a *physical* quadruped learning to
walk in about one hour, because it practiced inside a learned latent model
instead of on its own legs. No atom of the robot's world was simulated. Only
what the task needed was kept.

**Cars that predict.** Wayve's [GAIA-1](https://arxiv.org/abs/2309.17080)
(2023) and [GAIA-2](https://wayve.ai/thinking/gaia-2/) (2025) generate
coherent futures of driving scenes — not because they track every photon on
the road, but because they learned the *distribution of plausible futures*
at exactly the abstraction level where driving decisions live. Autonomous
driving stopped asking "what is the exact state of the world?" and started
asking "what happens next, at the resolution that matters?"

**Agents that imagine.** DeepMind's [Genie](https://arxiv.org/abs/2402.15391)
(ICML 2024) through [Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)
(2025) learn playable, interactive worlds from video; agents make decisions
by *imagining* rollouts. [NVIDIA Cosmos](https://github.com/NVIDIA/Cosmos)
(2025) industrialized the recipe into world foundation models for physical
AI. And Yann LeCun's position paper,
[A Path Towards Autonomous Machine Intelligence](https://openreview.net/forum?id=BZ5a1r-kVsf)
(2022), together with Meta's [V-JEPA 2](https://arxiv.org/abs/2506.09985)
(2025), articulated the principle underneath all of it: **predict in
representation space, not in pixel space**. You do not model the world.
You model the *sufficient statistics* of the world for the decisions you
need to make.

That principle dissolved both of my objections at once:

- The **storage objection** dies because compression is the whole point.
  A world model is not a simulation of the world; it is the smallest state
  that makes the future predictable. (In this repo, that state is 5
  dimensions per asset plus a distribution — not a tick-by-tick replay.)
- The **precision objection** dies because prediction never needed
  microscopic precision. Boltzmann could not track a single molecule, and
  kinetic theory works anyway: at the population level, dynamics become
  *more* lawful as N grows, not less. Quantum indeterminacy lives twenty
  orders of magnitude below the level where any decision — a lane change, a
  portfolio weight — actually happens.

I was an exchange student at Stanford while much of this was in the air —
the [spatial intelligence](https://www.ted.com/talks/fei_fei_li_with_spatial_intelligence_ai_will_understand_the_real_world)
conversation around Fei-Fei Li and [World Labs](https://www.worldlabs.ai/)
made it feel less like a research direction and more like a consensus
forming in real time: *world models are how agents will understand
everything*. The question I could not put down was: **everything — except
markets?**

## The second thread: a violation of first principles

At the same time I was working through quantitative finance coursework and
reading the empirical asset-pricing literature, and I hit something I still
find astonishing: **the dominant paradigm of quantitative finance is not
even trying to predict the market.**

Factor models ask which characteristics *correlate* with cross-sectional
returns. The literature documented 600+ of them — Cochrane called it the
["factor zoo"](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2011.01671.x)
in his 2011 AFA presidential address — and when
[Harvey, Liu & Zhu](https://academic.oup.com/rfs/article/29/1/5/1843824)
audited the zoo, most factors failed to replicate.
[López de Prado](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086)
catalogued the same pathology from inside the industry: backtest overfitting
as standard practice.

From first principles this is upside down. A model of the market should
model *the market* — the thing that generates prices — not mine correlations
from the residue prices leave behind. History's data does not repeat: every
factor decays the moment it is crowded (the Lucas critique, measured).
But history itself — the *structure* that generates the data: institutions,
constraints, incentives, the game — does repeat. If you want factors that
mean something, you have to go back to the world that produces them.

That sentence, I realized, had a name. It was a world model.

## The merge

Two threads, one collision:

- Robotics, driving, and agent research proved that **compressed world
  models predict well** at the abstraction level that matters.
- Quantitative finance was stuck mining patterns precisely because it had
  **no world model** — no representation of the thing generating the data.

But markets add one twist that Dreamer never faced: **the "physics" of a
market is other agents' strategies.** A road does not replan when GAIA-1
predicts it; a market does — every fund that discovers a pattern destroys
it by trading on it. So the transition network of a financial world model
cannot be learned dynamics; it must be an **equilibrium solver**. The
environment *is* the fixed point of every agent's best response to everyone
else.

That single substitution — replace the learned transition model with a
hierarchical mean-field game — is this entire repository. The encoder
compresses the market panel into a latent state (the JEPA lesson). The Game
module solves for the equilibrium instead of extrapolating history (the
Lucas lesson). The controller acts on the equilibrium drift (the Dreamer
lesson). And the residual that no data can remove — behavioral noise — is
not swept under the carpet but bounded by theorem
([Theorem 1](../README.md#component-2--dual-noise-decomposition-theorem-1),
the dual Cramér-Rao bound): the honest descendant of my old precision
objection.

## What I believe now

World models are not a technique that happens to work in robotics. They are
the first-principles form of prediction in any domain: find the level of
description at which dynamics are lawful, compress to it, and model the
generator — not the residue it leaves in a dataset. Finance was simply the
domain where nobody had done it yet, because in finance the generator
fights back.

MicroWorld is the bet that modeling the generator anyway — as a game, with
proofs — is worth more than one more decade of factor mining.

---

*Back to the [README](../README.md) · the mathematics starts
[here](../README.md#the-mathematical-framework-two-threads-one-theory) ·
what comes after the mathematics is [Phase 2](PHASE2_NEURAL_GAME.md).*
