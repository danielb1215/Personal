# Daniel Bolivar — Financial Context

## Location & Currency

- Based in **Bogotá, Colombia** — earns in **USD**, spends in **COP**
- This is a significant advantage: USD income with Colombian cost of living gives strong purchasing power
- No currency conversion friction for US clients or platforms (Stripe, Gumroad, Upwork, etc.)

## Payroll & Money Flow (USD → COP)

- **Paid via Rippling** (employer's payroll platform) in USD
- Transfers from Rippling → **Wallbit** with **$0 fee**
- From Wallbit, sends to Colombian bank account and receives in **COP**
- End-to-end path: Rippling (USD) → Wallbit (USD, no fee) → Colombian bank account (COP)
- **Real cost is in the FX rate, not the fee** (checked 2026-11-02 against the official TRM):
  Wallbit → Bancolombia got on average **~1.9% below TRM** (5 transfers Jun–Sep 2026, range 0.8%–3.0%).
  Payoneer → Bancolombia (the route before Jun 2026): 8 transfers Feb–Jun 2026, $7,346.93 → **2.80% below TRM**
  ($205.84; 2% fee + ~0.8% spread; range 1.1%–4.1%), plus a $29.95/yr maintenance fee.
  Wallbit beats Payoneer, but Wise / ARQ (ex-DolarApp) may be cheaper — pending a side-by-side quote test.
- **Side-by-side test 2026-11-02, $1,400 → Bancolombia 6948:**
  Wise quote 4,453,416 COP (rate 3,229.50, fee $21.02 = 1.5%, ~1.5% total cost) vs
  Wallbit actual 4,349,170 COP (3,106.55/USD, ~3.8% below Wise's rate).
  **Wise delivered ~104k COP (~$32, 2.3%) more.** Next step: point Rippling payouts to Wise.
- **Wise Business vs Personal (checked 2026-11-02):** same conversion pricing; Business costs a one-time
  setup fee (~$31 in the US; Colombia amount unconfirmed). Wise's Acceptable Use Policy bars business /
  client income on personal accounts, and Daniel is paid as a contractor → use **Wise Business**
  (sole trader / freelancer, cédula + RUT) to avoid an account freeze; it also covers future side-business income.
- **ARQ (ex-DolarApp) vs Wise Business (checked 2026-11-02, not yet tested with real money):**
  ARQ = $3 per incoming ACH + ~0.5% built into the USDc→COP rate (published bid 3,151 on 2026-10-19 vs
  TRM 3,175 / close 3,156) → ~0.7% total on $1,400 vs Wise's 1.5%. Trade-offs: ACH takes 3–6 business days,
  balance is held as USDc (virtual asset, run by DolarApp México), not a bank balance.
  Plan: test one small Rippling payout into ARQ; if it beats Wise by ≥0.5%, use ARQ for COP conversions and
  keep Wise Business as backup / for future clients.
- **Total Wallbit cost, Jun 10 – Nov 2 2026 (checked 2026-11-02):** 10 transfers to Bancolombia 6948,
  $4,904.67 → **$112.67 lost to the rate (2.30%)**, from 0.1% to 3.8% per transfer (the Nov 2 one alone: $53.30).
  Plus ~$84–113 estimated on $4,940 of local payouts to other people (Fer, Luisa, Maribel, Valeria, Mauricio;
  their COP amounts aren't in the statements) and a $9.84 "Balance adjustment (debit)" on 2026-08-07.
  **≈ $205–235 in ~5 months on ~$9,850 moved.** (PSE 99,697 COP to "Pexto Capital SAS" on 2026-10-07 is the
  Movistar bill paid through Pexto's collection service — not a Wallbit cost; Sheet row and classifier fixed 2026-11-02.)
- **Wise fee check (2026-11-02):** $21.02 on $1,400 from USD balance = 1.50% is from Daniel's own quote (rate 3,229.50,
  locked). Second quote $2,500 → fee $36.00 (1.44%), same rate → Wise USD→COP ≈ **$1.95 fixed + 1.36%**
  (~1.75% at $500, ~1.43% at $2,900).
  Note: 2026-11-02 was a Colombian holiday (local FX market closed). Friday 10-30 close was 3,183–3,194 (TRM 3,182.99);
  Wise's 3,229.50 was ~1.2–1.5% above it (live offshore rate), while Wallbit's 3,106.55 sat ~2.4% below Friday's level.
  Re-quote both on a normal business day to confirm.
- **Wise simulated on the same 10 Wallbit transfer dates** (TRM as Wise's rate, fee $1.95 + 1.36%; Nov 2 = real quote):
  Wise total fee $86.34 (1.76%) vs Wallbit $112.67 (2.30%) → Wise +88.5k COP (~$27). But Wallbit won 6 of 10 —
  the small transfers (Wise's fixed fee) — and **Jun–Sep alone Wallbit was ~16k COP better**; the whole gap is the
  Nov 2 transfer. Batched monthly, Wise ≈1.5% vs Wallbit's Jun–Sep 1.69%: a small edge. ARQ (~0.7%) would beat both. TRM that day was 3,182.99, so on the
  TRM basis Wallbit's Nov 2 cost was ~2.4% (not 3.8%). Wise caps sends to Colombia at ~$2,900 per transfer.

## Legal / Tax Status

- **Freelancer / independent contractor** in Colombia
- Already structured to receive foreign income — no corporate setup needed to start a side business

## Existing MRR

- **$0** — salary only, no existing side income streams

## Current Income

- **Primary salary:** ~$4,600/month USD (remote job at Crowd Cow)

## Monthly Expenses

- **Range:** $2,000–$3,000/month USD
- **Surplus:** ~$1,600–$2,600/month available for saving/investing

## Investment Portfolio

Active stock portfolio on eToro (live data as of 2026-08-27) — all long positions, all profitable:
- NVDA, GOOG, QQQ, AAPL, VOO, AMZN, TSLA
- Plus one copy-trading position (AI agent-ZCAKBPQ, $200 invested)
- Trading account total value: **$13,810.02**
- Available cash: **$2,809.55**
- Total unrealized gain: **$4,897.01**
- Style: long-term growth, tech-heavy

See `hobbies.md` for full portfolio table.

## Financial Goals

Target: **$2,000–$3,000/month in passive income or MRR** from a side business.

This would either:
- Cover 100% of monthly expenses → full financial independence
- Cover 50%+ → significantly reduce dependence on primary job

**Ultimate goal:** Financial freedom to travel and explore nature full-time.

## Risk Tolerance

**Medium** — willing to invest savings into a side project, but not all at once. Prefers staged investment: test small, scale what works.

## Time Available for Side Projects

- Weekdays: evenings after 5pm (minus Tue/Thu bike rides)
- Realistically: ~2–3 hours on most weekday evenings
- Weekends: partially available (mornings often reserved for 4h bike rides or hikes)
- Practical estimate: **10–15 hours/week** for a side project

## Capital Available to Start

- **Budget: $5,000–$10,000 total**
- Preference: staged deployment, not all upfront
- Would not spend everything on one unvalidated idea

## Key Constraints for Any Business Idea

1. Must work async / remotely — no location dependency
2. Must not require more than 10–15h/week to start
3. Revenue should be visible within 3–6 months
4. Ideally leverages existing data engineering skills (no new learning curve to start earning)
5. Target: $2–3k MRR before considering leaving primary job
