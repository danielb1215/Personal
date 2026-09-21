# Ranked Shortlist — September 2026

Ten remote, skills-based ideas run through `../scoring-filter.md`.
Fork setting: **remote-and-slower** (location independence is a hard veto; 12–18 month ramp accepted).

---

## Ranking

| # | Idea | C1 Skill | C2 Async | C3 Ceiling | C4 Speed | C5 Capital | C6 Durable | C7 Valid. | C8 Energy | **Total** |
|---|------|---|---|---|---|---|---|---|---|---|
| **1** | **Warehouse cost-reduction audit** (productized) | 5 | 4 | 4 | 5 | 5 | 3 | 5 | 3 | **68** |
| **2** | **DTC attribution & analytics retainer** | 5 | 3 | 5 | 4 | 5 | 4 | 4 | 3 | **67** |
| **3** | **Micro-SaaS: warehouse cost monitoring** | 5 | 5 | 5 | 1 | 3 | 5 | 2 | 3 | **65** |
| **4** | Async dbt / data-model code review subscription | 5 | 5 | 3 | 3 | 5 | 3 | 4 | 3 | **63** |
| **5** | Spanish-language analytics-eng content → course | 4 | 5 | 4 | 1 | 4 | 5 | 2 | 4 | **61** |
| **6** | DTC dbt marts + attribution templates | 5 | 5 | 2 | 3 | 5 | 4 | 3 | 3 | **61** |
| **7** | AI/LLM-for-analytics implementation | 4 | 3 | 5 | 4 | 5 | 2 | 4 | 4 | **61** |
| **8** | Looker / LookML freelancing | 5 | 3 | 4 | 5 | 5 | 1 | 5 | 2 | **60** |
| **9** | Snowflake→BigQuery migration projects | 5 | 2 | 5 | 3 | 5 | 2 | 2 | 2 | **55** |
| **10** | Cycling carbon-wheel data / comparison site | 3 | 5 | 2 | 1 | 5 | 4 | 2 | 5 | **52** |

Weights: C1×3 · C2×3 · C3×3 · C4×2 · C5×1 · C6×2 · C7×1 · C8×1 — max 80.

**Ties at 61** broken per the filter on C6 then C8: **#5 Spanish content** (C6=5, C8=4) > **#6 templates** (4, 3) > **#7 AI consulting** (2, 4).

---

## The Shape of This Ranking

Read the pattern, not just the order:

- The **top 2 are services** — fast cash, weak compounding (C6 = 3 and 4).
- **#3 is the only true asset** in the top tier — C6=5, C2=5, C3=5, but C4=1. It cannot pay anything for 6+ months.

Picking either alone is a mistake. Services alone means freelancing forever. The product alone means 6–12 months of unpaid evenings with no market feedback and real burnout risk after a full day of the same work.

**The move is to pair them: #1 funds #3, and #1 literally produces #3.**

Every manual cost audit generates the queries, heuristics and customer insight that *are* the monitoring product. The audit isn't a detour from the SaaS — it's the paid R&D for it, with customers telling you what to build while they pay you to learn.

**And #5 is not a competing idea — it's #1's distribution channel.** Writing about warehouse cost optimization is lead generation for the audit. In Spanish it's a genuinely underserved niche (LatAm analytics-engineering content is thin, and he's a native speaker with senior credentials). Scored standalone it's a slow 61; scored as top-of-funnel for #1 it's free leverage.

---

## Recommended Sequence

| Phase | Months | Focus | Revenue target |
|-------|--------|-------|----------------|
| **1** | 0–6 | **#1 audits.** Land the first 3 clients manually. Publish while doing it (**#5**). | $2,500/mo by month 5–6 |
| **2** | 4–12 | Templatize the audit — queries → script → dashboard. Same fee, fewer hours. | $5,000/mo |
| **3** | 9–18 | Convert tooling + customer insight into **#3**, monitoring MRR. Audits become the sales channel. | MRR replaces service income |

**Note the finding that contradicts the fork's own label:** choosing "remote-and-slower" did *not* force a 12–18 month wait for money. A productized remote service can produce revenue in **60–90 days**. What the fork actually bought was giving up the *local* fast-cash options (coffee, wheels), not giving up speed.

---

## #1 — Warehouse Cost-Reduction Audit (start here)

**Why this scores highest:** it sells the single most credible thing on Daniel's résumé. He migrated Snowflake + Fivetran → BigQuery with Datastream CDC and **cut monthly data-ops costs 67.5%**. That is not a claim requiring a portfolio — it's a number with a story, and it maps to a pain that a specific buyer already knows they have.

**The offer**

| Element | Spec |
|---------|------|
| Deliverable | Written audit: cost breakdown, prioritized fix list, estimated monthly savings per fix |
| Price | **$2,500** fixed |
| Turnaround | 2 weeks |
| Access needed | Read-only warehouse + billing export. No calls beyond a 45-min kickoff. |
| Risk reversal | *"If I don't identify at least 2× the fee in annualized savings, you don't pay."* |

That guarantee is cheap to offer and nearly impossible to lose — warehouse waste is close to universal at the target size — and it removes the trust barrier a solo unknown operator otherwise faces.

**Target buyer:** Series A–C startups on BigQuery or Snowflake spending **$5k–50k/month** on the warehouse, where the bill is growing faster than revenue and there's no dedicated platform engineer.

**Channels:** LinkedIn (existing profile, senior title), dbt Community Slack, r/dataengineering, targeted cold email to Heads of Data.

**Economics**

| Metric | Value |
|--------|-------|
| Fee | $2,500 |
| Work per audit | ~20–25 hours |
| Effective rate | $100–125/hr |
| 2 audits/month | **$5,000/month** at ~10–12h/week ✅ within the 15h veto |
| 1 audit/month | $2,500/month ✅ clears the goal |

**Validation — 3–4 weeks, $0:** 20 targeted outreach messages → book 5 discovery calls → close 1. If 20 messages produce zero calls, the positioning is wrong (fix the message and retry once). If 5 calls produce zero sales, the *price or the buyer* is wrong. Either way it's falsifiable in a month for nothing but time.

---

## ⚠️ Conflict-of-Interest Check — Do This First

Several of these ideas sit close to Crowd Cow's own business:

- **#2 (DTC attribution retainer)** is the highest risk — it's substantially what Daniel does for Crowd Cow, and prospective clients could be adjacent to or competing with them.
- **#1** is lower risk but still requires that no client be a Crowd Cow competitor.

**Before any outreach, review the employment agreement for:** moonlighting/outside-activity clauses, non-compete scope, IP assignment language (some agreements claim work product created during employment regardless of hardware or hours), and any client-solicitation restrictions.

This is not optional diligence. Getting it wrong risks the $4,600/month salary that funds everything.

---

## Honest Limits of This Exercise

- **No demand has been validated.** Every score here is judgment about untested markets. A 68 and a 65 are the same number in practice. Only sales conversations settle it.
- **#1 scores 68 with C6=3 and C8=3.** It is an on-ramp, not a destination. It is desk work — the exact activity `hobbies.md` lists as draining — sold at a better rate and on his own schedule. If it drains him as much as the day job does, phase 3 becomes the whole point rather than the upside.
- **The cycling idea ranks last (52) and that's correct on the numbers** — C3=2, C4=1. But it holds the only C8=5 in the list. If motivation collapses on the audit business, this is the one he'd actually keep doing. Worth keeping as a weekend outlet, not as the income plan.

## Next Steps

- [ ] Review Crowd Cow employment agreement for moonlighting / non-compete / IP clauses
- [ ] Write the audit offer as a one-page landing page
- [ ] Build the 20-prospect outreach list
- [ ] Send 20 messages; track calls booked and objections heard
- [ ] If ≥1 sale in 30 days → `/speckit-specify` the audit business and formalize the delivery process
- [ ] If 0 sales but ≥3 calls → `/speckit-clarify` on pricing and positioning, then retry once
