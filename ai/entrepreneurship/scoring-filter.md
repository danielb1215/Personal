# Idea Scoring Filter

Purpose: stop evaluating ideas one at a time and discovering at the end that they were never going to fit. Every idea runs through **hard vetoes first**, then weighted scoring. Anything that fails a veto is eliminated without scoring — no partial credit, no "but what if."

Derived from `../persona/finances.md`, `../persona/hobbies.md`, and the constitution in `.specify/memory/constitution.md`.

---

## Resolved Strategic Fork (2026-09-21)

Two constraints in `finances.md` were in direct contradiction and were quietly vetoing every idea generated:

- "Must work async / remotely — no location dependency"
- "Revenue should be visible within 3–6 months"

Fast revenue in Colombia means a local physical business (inventory, delivery, in-person service). That anchors Daniel to Bogotá — which defeats the stated *purpose* of the whole exercise: financial freedom to travel and explore nature full-time.

**Decision: remote-and-slower.**

Location independence is now a **hard veto**, not a preference. The 3–6 month revenue target is downgraded to a **scoring criterion** (Time to First Dollar), not a gate. Accepted ramp: **12–18 months to $2–3k/month.**

> ⚠️ Note: "slower" describes the *accepted worst case*, not the target. It does not mean choosing the slowest idea. A remote productized service can still produce revenue in 60–90 days — see the shortlist.

---

## Stage 1 — Hard Vetoes

Any single failure eliminates the idea. No scoring, no exceptions.

| # | Veto | Rationale |
|---|------|-----------|
| **V1** | **Requires physical presence in a specific city** | The fork decision. Defeats the travel goal that motivates everything. |
| **V2** | Requires >$10,000 to reach first revenue | Hard budget ceiling from `finances.md` |
| **V3** | Requires >15h/week sustained | Full-time job at Crowd Cow; Tue/Thu rides + weekend rides are non-negotiable |
| **V4** | Carries bodily-injury / safety-critical liability | Uninsurable from Colombia; risks personal assets. Killed the wheel brand. |
| **V5** | Requires holding physical inventory | Capital lockup + storage + customs + anchoring. Follows partly from V1 but is independently disqualifying. |
| **V6** | Requires a new skill needing 6+ months before earning | Constitution III: monetize existing expertise, no learning curve to start earning |
| **V7** | Structurally cannot reach $2,000/month | That is the goal. An idea that caps below it is a hobby, not a business. |

### Already eliminated by Stage 1

| Idea | Fails | Note |
|------|-------|------|
| Carbon wheel own brand | V2, V4, V5 | See `ideas/carbon-wheels-brand-vs-dealer.md` |
| Carbon wheel Colombia dealer | V1, V5 | Economics worked; the model anchors him |
| Cycling apparel brand | V1, V5 | Also saturated, but the veto is structural |
| **B2B coffee Bogotá** | **V1** | ⚠️ Economics were validated at ~16 offices for $2k/month and supply is solved via cousin's roastery — but it is Bogotá offices with Bogotá delivery routes. **Funds travel by preventing travel.** Retained on file in case the fork is ever revisited. |
| Bike fitting studio | V1, V6 | |
| Local bike shop / stocked e-commerce | V1, V5 | |

---

## Stage 2 — Weighted Scoring

Score each surviving idea **1–5** per criterion. Weighted total out of **90**.

| # | Criterion | Weight | 5 = | 1 = |
|---|-----------|--------|-----|-----|
| **C1** | **Skill leverage** | ×3 | Directly sells dbt / BigQuery / SQL / dimensional modeling / Looker | Unrelated to his expertise |
| **C2** | **Async / location independence** | ×3 | Zero scheduled calls; works from a dive boat | Fixed hours in a client's timezone |
| **C3** | **Revenue ceiling** | ×3 | Can exceed $10k/month | Barely clears $2k/month |
| **C4** | **Time to first dollar** | ×2 | Under 30 days | 12+ months |
| **C5** | **Capital efficiency** | ×1 | Under $500 to first revenue | Near the $10k ceiling |
| **C6** | **Durability / compounding** | ×2 | Asset earns while he sleeps | Stops earning the day he stops working |
| **C7** | **Validation speed** | ×1 | Falsifiable in a week for $0 | Months and real money to know |
| **C8** | **Energy fit** | ×1 | Varied, energizing | More of the desk grind that already drains him |
| **C9** | **Commoditization resistance** | ×2 | Value is access, accountability, continuous state or trust — an LLM makes the *provider* faster but cannot substitute for them | The deliverable is information the buyer can now generate themselves in an afternoon |

### C9 was added 2026-09-21

Added after a direct challenge: *"with AI most companies can do that."* Largely correct, and the filter had no way to see it — it screened for whether **Daniel** could deliver something, never for whether a **buyer with a good LLM** still needed him to.

The distinction C9 enforces:

| AI has commoditized | AI has not touched |
|---------------------|--------------------|
| Knowing *what* to optimize | **Access** to the warehouse, billing export, `INFORMATION_SCHEMA`, dbt repo |
| Writing the analysis | **Context** — which of 400 models is business-critical vs. abandoned |
| Producing the report | **Accountability** — someone owns the risk when revenue reporting breaks |
| Explaining best practice | **Continuity** — being the always-on watcher with historical baselines |
| | **Doing it** — companies could always read the free docs; they didn't |

The load-bearing point: **"can" and "does" are different businesses.** BigQuery optimization docs have been free for a decade and went unread, not for lack of information but because nobody's job title said "go find 30% of warehouse waste." AI changes what a team *could* do. It does not give anyone slack in their week, nor willingness to own a risky change.

**Honest limit on C9:** these positions erode slowest, not permanently. If implementation itself automates, the whole services category compresses. That is an argument for reaching a product with state and MRR *sooner*, not for treating any service as safe.

### Weighting rationale

- **C1, C2, C3 at ×3** — these are the strategy. Skills are the unfair advantage, async is the fork decision, and the revenue ceiling is the actual goal.
- **C4 at ×2** — demoted from a gate to a criterion by the fork, but cash-now still has real strategic value: it funds the slow asset.
- **C5 at ×1** — deliberately low. Nearly every software/service idea scores 4–5 here, so it barely discriminates. A criterion that doesn't separate candidates shouldn't carry weight.
- **C6 at ×2** — the difference between a second job and a business. Underweighting this is how people end up freelancing forever.
- **C7, C8 at ×1** — real but secondary tiebreakers.
- **C9 at ×2** — material, but deliberately not ×3. An idea that is AI-proof and also unsellable is worth nothing; resistance to commoditization matters only on top of real skill leverage and a real ceiling.

### Interpretation bands

| Score | Meaning |
|-------|---------|
| **78–90** | Start now |
| **69–77** | Strong — viable primary candidate |
| **60–68** | Conditional — needs a specific angle to work |
| **Below 60** | Park it |

Rescaled from /80 when C9 was added.

---

## How to Use

1. Run Stage 1. Eliminate ruthlessly — the veto list is the point of this document.
2. Score survivors on all 8 criteria. Write the reasoning per score, not just the number.
3. Read the ranking as **input, not verdict.** Two ideas within ~3 points are a tie; break it on C6 (durability) and C8 (energy fit), because those determine whether he's still doing it in 18 months.
4. Check the **shape** of the top scores, not just the order. A ranking full of services means fast cash but no asset; a ranking full of products means an asset with no runway. The right move is usually to pair one of each — see the shortlist.
5. Only after a ranked shortlist: `/speckit-specify` on the winner.

## Known Blind Spots

- **Scores are estimates, not measurements.** They encode judgment about markets that haven't been tested. Treat a 68 vs. a 65 as noise.
- **The filter cannot detect "no demand."** Every idea here can score well and still have nobody willing to pay. Only customer conversations and money settle that.
- **C8 is self-reported.** Daniel may discover that client work drains him far more than a 3 predicts, which would reorder everything.
- **The filter scores ideas, not offers.** C9 exposed this: the *same* idea scored 72 as a report and 75 as an implementation engagement. How a thing is packaged can matter more than which thing it is — so score the specific offer, not the category.
- **A missing criterion is invisible.** C9 didn't exist for the first run and silently mis-ranked the list. Re-challenge the criteria themselves, not just the scores.
