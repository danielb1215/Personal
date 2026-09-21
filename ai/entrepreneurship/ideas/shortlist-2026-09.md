# Ranked Shortlist — September 2026

Ten remote, skills-based ideas run through `../scoring-filter.md`.
Fork setting: **remote-and-slower** (location independence is a hard veto; 12–18 month ramp accepted).

> **Revised 2026-09-21** after the challenge *"with AI most companies can do that."* The challenge held up, criterion **C9 (commoditization resistance)** was added, and all ten ideas were rescored out of **90**. The original #1 fell to #3. See *What the AI Objection Changed* below.

---

## Ranking

| # | Idea | C1 Skill | C2 Async | C3 Ceiling | C4 Speed | C5 Cap | C6 Durable | C7 Valid. | C8 Energy | C9 AI-proof | **Total** | Prev. |
|---|------|---|---|---|---|---|---|---|---|---|---|---|
| **1=** | **Warehouse cost reduction — *implemented*** | 5 | 3 | 5 | 4 | 5 | 4 | 4 | 3 | **4** | **75** | — |
| **1=** | **DTC attribution & analytics retainer** | 5 | 3 | 5 | 4 | 5 | 4 | 4 | 3 | **4** | **75** | #2 |
| **3** | **Micro-SaaS: warehouse cost monitoring** | 5 | 5 | 5 | 1 | 3 | 5 | 2 | 3 | **4** | **73** | #3 |
| 4 | Warehouse cost audit — *report only* | 5 | 4 | 4 | 5 | 5 | 3 | 5 | 3 | **2** | **72** | **#1** ⬇ |
| 5 | AI/LLM-for-analytics implementation | 4 | 3 | 5 | 4 | 5 | 2 | 4 | 4 | **5** | **71** | #7 ⬆ |
| 6 | Looker / LookML freelancing | 5 | 3 | 4 | 5 | 5 | 1 | 5 | 2 | **3** | **66** | #8 ⬆ |
| 7= | Async dbt / data-model code review sub | 5 | 5 | 3 | 3 | 5 | 3 | 4 | 3 | **1** | **65** | #4 ⬇ |
| 7= | Spanish-language analytics-eng content | 4 | 5 | 4 | 1 | 4 | 5 | 2 | 4 | **2** | **65** | #5 |
| 9= | DTC dbt marts + attribution templates | 5 | 5 | 2 | 3 | 5 | 4 | 3 | 3 | **1** | **63** | #6 ⬇ |
| 9= | Snowflake→BigQuery migration projects | 5 | 2 | 5 | 3 | 5 | 2 | 2 | 2 | **4** | **63** | #9 |
| 11 | Cycling carbon-wheel data / comparison site | 3 | 5 | 2 | 1 | 5 | 4 | 2 | 5 | **2** | **56** | #10 |

Weights: C1×3 · C2×3 · C3×3 · C4×2 · C5×1 · C6×2 · C7×1 · C8×1 · **C9×2** — max 90. Arithmetic verified.

---

## What the AI Objection Changed

**The challenge was correct about the thing it named.** A written cost-optimization report is substantially commoditized. An LLM knows partition pruning, clustering, slot reservations vs. on-demand, materialized views, BI Engine — all of it, instantly, free. The information asymmetry that consulting used to sell is largely gone.

That is why **#1 fell to #4.** The original offer sold a *document*, and documents are now cheap.

**What it was wrong about is the word "can."**

| AI commoditized | AI did not touch |
|-----------------|------------------|
| Knowing what to optimize | **Access** — warehouse, billing export, `INFORMATION_SCHEMA.JOBS`, dbt repo |
| Writing the analysis | **Context** — which of 400 models is business-critical vs. abandoned |
| Producing the report | **Accountability** — who owns the risk when revenue reporting breaks |
| Explaining best practice | **Continuity** — the always-on watcher with historical baselines |

BigQuery's optimization docs have been free for ten years and went unread. Not for lack of information — because nobody's job title said *"go find 30% of warehouse waste."* The data team is shipping what the CEO asked for. AI changes what a team **could** do; it does not create slack in their week, and it does not make anyone willing to own a risky change to the pipeline feeding the CFO's dashboard.

**So the fix is the deliverable, not the idea.** Stop selling the finding; sell the lower bill.

| | Report *(#4, 72)* | Implemented *(#1=, 75)* |
|---|---|---|
| Deliverable | Prioritized fix list | Fixes shipped, savings verified on the next invoice |
| Access | Read-only | Write, or PRs into their dbt repo |
| Pricing | $2,500 fixed | $4,000–6,000, or fee + share of verified savings |
| C9 | 2 — they can generate this | 4 — requires access, judgment, accountability |
| Cost of the change | Harder sale, more trust needed, less async (C2 4→3, C4 5→4) | |

**And AI is Daniel's advantage here, not his threat.** `skills.md` already lists Claude Code, MCP integrations, LLM-powered pipelines. If an LLM does the analysis in two hours instead of fifteen, his effective rate goes *up* — he keeps the fee and loses the labor. The consultant who loses is the one whose entire product was knowing things.

### Secondary effects worth noting

- **AI/LLM-for-analytics implementation jumped #7 → #5** (C9=5, highest on the board). It's the only idea that gets *stronger* as AI improves, because the trend is the product. Under-rated in the first pass.
- **Async code review collapsed #4 → #7=** (C9=1). Most exposed idea on the list — AI review bots already exist, work well, and cost almost nothing.
- **dbt templates also hit C9=1.** "Generate me a dbt mart for DTC ecommerce attribution" is now a prompt. Selling that artifact is selling something free.
- **The top three are unchanged in substance.** The ranking bent but did not break — a decent sign it isn't fragile.

---

## The Genuine Tie at #1

**Cost reduction (implemented)** and **DTC attribution retainer** both score 75, with identical C6 (4) and C8 (3) — so the filter's own tiebreak can't separate them.

Break it on the **conflict-of-interest risk** already flagged: the DTC attribution retainer is substantially what Daniel does for Crowd Cow, for buyers who may be adjacent to or competing with them. Cost optimization is domain-neutral — it applies to a fintech, a marketplace, a health startup, nobody near the meat business.

**→ Start with cost reduction, implemented.** Not because it scores higher, but because it carries less risk to the salary funding everything.

---

## Recommended Sequence *(revised)*

| Phase | Months | Focus | Revenue target |
|-------|--------|-------|----------------|
| **1** | 0–6 | Cost reduction, **implemented** — 2–3 clients. Use AI to compress delivery; keep the fee. | $3–4k per engagement |
| **2** | 4–12 | Templatize detection into tooling. Convert 1–2 clients to a monitoring retainer. | $3–5k/mo |
| **3** | 9–18 | Tooling + insight → **micro-SaaS (#3)**. Highest C6 *and* C9 in the list. | MRR replaces service income |

**The objection strengthens the case for reaching Phase 3 faster.** If AI eventually compresses implementation too, the defensible position is the product that holds *state* — historical baselines, continuous monitoring, alerting — which is precisely what a one-off engagement and an LLM both lack. The services phase is the funded on-ramp, and the argument for not lingering in it just got better.

---

## The Offer *(revised)*

| Element | Spec |
|---------|------|
| Deliverable | Fixes **shipped**, savings verified against the following month's invoice |
| Price | **$4,000–6,000**, or $2,000 + 25% of verified 12-month savings |
| Duration | 3–4 weeks |
| Access | Read-only warehouse + billing export; PRs into their dbt repo |
| Risk reversal | *"You pay the success component only on savings you can see on your own invoice."* |

Credibility rests on one line from `profile.md`: migrated Snowflake + Fivetran → BigQuery with Datastream CDC and **cut monthly data-ops costs 67.5%**. Not a claim needing a portfolio — a number with a story.

**Target buyer:** Series A–C on BigQuery or Snowflake, **$5k–50k/month** warehouse spend, bill growing faster than revenue, no dedicated platform engineer.

**Economics**

| Metric | Value |
|--------|-------|
| Fee | $4,000–6,000 |
| Work per engagement | ~35–45 hours (less with AI assistance) |
| Effective rate | $110–170/hr |
| 1 engagement/month | **$4,000–6,000/month** ✅ clears the goal at ~10–12h/week |

**Validation — 3–4 weeks, $0:** 20 targeted messages → 5 discovery calls → 1 close. Zero calls means the positioning is wrong. Five calls and no close means the price or the buyer is wrong.

Add one question to every call, because it tests the objection directly rather than assuming an answer: *"Have you already tried to solve this with an LLM or the built-in recommender? What happened?"* If most say "yes, and it worked," the offer is dead and this file should be updated to say so. The likelier answer — based on the "can vs. does" gap — is *"we've been meaning to look at it for eight months."*

---

## ⚠️ Conflict-of-Interest Check — Still Blocking

Before any outreach, review the Crowd Cow employment agreement for: moonlighting / outside-activity clauses, non-compete scope, IP assignment (some agreements claim work product created during employment regardless of hours or hardware), and client-solicitation restrictions.

Getting this wrong risks the $4,600/month salary that funds everything. The DTC attribution retainer is the highest-exposure idea on the list; cost optimization is the lowest.

---

## Honest Limits

- **No demand has been validated.** Every score is judgment about untested markets. 75 vs. 73 is noise. Only sales conversations settle it.
- **C9 erodes, it doesn't hold.** Access, accountability and continuity resist commoditization *slowest* — not permanently. Treating any service as durably safe is the mistake the objection was warning about.
- **The winner still scores 3 on energy fit.** It's desk work — the exact activity `hobbies.md` names as draining — at a better rate on his own schedule. Phase 3 is the point, not the bonus.
- **The cycling idea ranks last (56) and that is correct on the numbers** — but it holds the only C8=5 on the board. Keep it as a weekend outlet, not the income plan.

## Next Steps

- [ ] Review Crowd Cow employment agreement (blocking)
- [ ] Rewrite the offer as implementation, not audit — one-page landing page
- [ ] Build the 20-prospect list: Series A–C, BigQuery/Snowflake, no platform engineer
- [ ] Send 20 messages; on every call ask the "have you tried an LLM for this?" question and log the answers
- [ ] ≥1 close in 30 days → `/speckit-specify` the engagement and formalize delivery
- [ ] 0 closes but ≥3 calls → `/speckit-clarify` on pricing and positioning, retry once
- [ ] If buyers genuinely report AI already solved this → update this file and promote **AI/LLM-for-analytics implementation** (#5, C9=5), which profits from that same trend
