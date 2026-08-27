# Idle Cash Allocation — $32,000

**Date:** 2026-08-27 · **Author:** Claude (analysis) for Daniel Bolivar
**Status:** Recommendation, pending verification of the items in "Open Questions"

> I'm not a licensed financial advisor and this isn't regulated financial advice.
> Recommendation follows anyway.

---

## 0. Starting position

| Account | Balance | Yield | Currency |
|---|---:|---|---|
| Rippling | $14,000 | 0% | USD |
| Payoneer | $15,000 | 0% | USD |
| Wise | $3,000 | 0% | USD |
| **Idle total** | **$32,000** | **0%** | |

Plus, live from eToro (2026-08-27):

| eToro | Amount |
|---|---:|
| Total account value | $13,815.32 |
| Available (idle) cash | $2,809.55 |
| Used margin (positions) | $6,103.46 |
| Unrealized P/L | $4,902.31 |

So the true idle-cash problem is **$34,809.55**, not $32,000. The $2,809.55 at eToro
is earning little or nothing and is discussed in §6.

**Note on the repo:** `ai/persona/finances.md` already documents Rippling → Wallbit
→ Colombian bank as the existing payroll route, at $0 fee. A Wallbit account
therefore already exists — this is not a new-vendor decision, only a
which-product-inside-Wallbit decision.

---

## 1. Opportunity cost of 0%

All figures = $32,000 × rate. APY/E.A. figures already include compounding, so the
simple product is the correct first-year number. SEC yields are simple annualized;
where reinvested monthly they compound slightly higher (shown separately).

| Option | Rate | Per year | Per month |
|---|---:|---:|---:|
| Status quo (all three accounts) | 0.00% | $0.00 | $0.00 |
| **IBKR cash sweep, at your account size** | **0.69%** | **$220.35** | **$18.36** |
| Wallbit Standard plan (per ES source) | 2.00% | $640.00 | $53.33 |
| **Wallbit @ your quoted 2.85%** | **2.85%** | **$912.00** | **$76.00** |
| Wallbit Premium plan (per ES source) | 3.50% | $1,120.00 | $93.33 |
| eToro, top advertised (EU/UK only) | 3.55% | $1,136.00 | $94.67 |
| **SGOV (0–3mo T-bill ETF), 30-day SEC yield** | **3.60%** | **$1,152.00** | **$96.00** |
| SGOV, reinvested monthly | 3.66% eff. | $1,171.18 | $97.60 |
| DGCXX (BNY Govt MMF), 7-day yield | 3.61% | $1,155.20 | $96.27 |
| VMFXX (Vanguard Federal MMF), 7-day | 3.69% | $1,180.80 | $98.40 |
| 3-month T-bill, direct | 3.79% | $1,212.80 | $101.07 |
| US HYSA best-in-market (**not open to you**) | 4.21% | $1,347.20 | $112.27 |
| Colombian HYSA — Ualá, COP | 10.50% E.A. | $3,360.00* | $280.00* |
| Lulo Bank CDT 540d, COP | 12.00% E.A. | $3,840.00* | $320.00* |

\* at a constant COP/USD rate — see §3.4, this is not a free lunch.

### The headline number

Leaving $32,000 at 0% instead of ~3.6% in T-bills costs you:

- **$1,152 per year**
- **$96 per month**
- **$3.16 per day**
- Over your stated 3-year horizon, compounded at 3.6%:
  `$32,000 × (1.036)³ − $32,000 = $32,000 × 1.111934 − $32,000 = $3,581.89`

$96/month is ~3.8% of your monthly expenses ($2,500 midpoint), and ~4.6% of your
monthly savings surplus ($2,100 midpoint). It is not life-changing. It is also
free, requires no risk you aren't already taking, and takes about two hours of
setup once.

### Reinvestment compounding, shown

SGOV pays monthly. Reinvesting: `(1 + 0.036/12)^12 − 1 = (1.003)^12 − 1 = 3.65995%`
→ `$32,000 × 0.0365995 = $1,171.18`, i.e. **$19.18/yr more** than the simple figure.
Small, but it is the reason to hold SGOV rather than spend the distributions.

---

## 2. Wallbit, assessed specifically

### 2.1 Your 2.85% figure does not match any rate I could verify

Three different published figures, none of them 2.85%:

| Source | Rate |
|---|---|
| Wallbit help centre (ES), via search snippet | 2.00% Estándar / 3.50% Premium |
| Wallbit help centre (EN), via search snippet | 3.00% – 3.75%, by plan |
| Your brief | 2.85% |

**I could not verify any of these directly.** `wallbit.io`, `help.wallbit.io` and
several review sites are blocked by this environment's network egress proxy, so
everything below is from search-result summaries of those pages, not from the pages
themselves. Treat the rate as **unverified**. Open the app and read the number
next to your own balance before acting.

### 2.2 How the yield is generated — and this changed

This is the most important finding in the whole analysis, and it's a discrepancy:

- One Wallbit help-centre summary says idle USD is invested in **DGCXX**, the
  Dreyfus/BNY Government Cash Management fund (7-day yield 3.61%, expense ratio
  0.21%) — i.e. a **money market fund**.
- A more recent summary says the remunerated account's income "**now** comes from
  the **Alpaca FDIC Bank Sweep Program**, from Alpaca Securities" — i.e. a **bank
  deposit sweep**.

These are **different products with different protection**:

| | Money market fund (DGCXX) | FDIC bank sweep (Alpaca) |
|---|---|---|
| What you own | Fund shares | A deposit claim on partner banks |
| FDIC | **No** | Yes, $250k per bank, up to ~$1,000,000 aggregate |
| SIPC | Yes — as a security in custody | Only the brokerage account, not the deposit |
| Can lose value | Yes, in theory (NAV break) | No, within FDIC limits |
| Who pays you | The fund's T-bill portfolio | The banks, minus Alpaca's and Wallbit's cut |

**Find out which one your balance is actually in.** If it's the sweep, your $32,000
would be comfortably inside FDIC limits. If it's the MMF, FDIC does not apply at all
and the marketing language about FDIC is about a different product.

### 2.3 The counterparty stack

```
You (Colombia, no US residency)
  └─ Wallbit            ← fintech app. NOT a bank. NOT a broker-dealer.
      └─ Alpaca Securities LLC   ← SEC-registered, FINRA member, SIPC member
          ├─ FDIC sweep banks    ← FDIC $250k/bank, ~$1M aggregate
          └─ or DGCXX (BNY)      ← MMF, SIPC custody only
```

**The weak link is Wallbit, not Alpaca.** SIPC protects you if *Alpaca* fails and
assets are missing. FDIC protects you if a *sweep bank* fails. Neither is designed
for the case where the fintech layer in front of them has bad records, freezes
withdrawals, or fails operationally. FDIC pass-through insurance depends on
accurate "for benefit of" account records maintained by the intermediary — that
requirement is exactly what went wrong for depositors in the 2024 Synapse
failure. This is the risk you are actually taking, and it is not zero.

Also note: **"Excess SIPC up to $75 million per account"** is marketing that does
not mean what it sounds like. Excess SIPC covers custody failure, not investment
loss, and the aggregate policy limit is shared across all of the broker's clients —
it is not a $75M guarantee to you.

### 2.4 What Wallbit is good at

Genuinely good, and your repo already relies on it:

- **Rippling → Wallbit: $0, ACH, 1–2 business days.** Nothing beats free.
- **Colombia withdrawal: ~$0.35 fixed**, minimum $5, USD→COP in minutes.
- **Wallbit Pro** (salary ≥ $1,500/mo received through Wallbit — you qualify at
  $4,600/mo) reduces withdrawal fees further.
- Instant movement between the remunerated account and checking, and the balance
  stays available to buy securities on-platform.

### 2.5 Is a paid plan worth it?

Break-even balance for a plan costing $X/month that lifts your rate by Δ:

```
B = (12 × X) / Δ
```

If Pro costs $5/mo and takes you 2.00% → 3.50% (Δ = 0.015):
`B = (12 × 5) / 0.015 = $4,000`

So a paid tier pays for itself above ~$4,000 held in the remunerated account —
**if** those are the real prices, which I could not verify. Note this cuts against
the allocation in §4: it puts only **$2,000** in Wallbit, which is *below* that
break-even. **Under my recommendation, stay on the free tier.** Only pay for a
Wallbit plan if you decide to keep the bulk of the cash there (§5, Option B).

### 2.6 Soft negative signal

TradersUnion's Wallbit review reports predominantly negative user reviews and
recommends against the company. TradersUnion is a low-authority affiliate site and
I could not access the page directly to see what the complaints are. I'm noting it
because it exists, not because it's evidence. Do not act on it alone — but it does
argue against concentrating $32,000 in one fintech.

---

## 3. The realistic alternatives

### 3.1 Interactive Brokers cash sweep — a trap at your size

IBKR's advertised 3.13% is for accounts with NAV ≥ $100,000. Below that, two rules
bite, and together they are brutal:

1. **No interest on the first $10,000** of cash.
2. **NAV < $100,000 → the rate is scaled by NAV/$100,000.**

At a $32,000 NAV:

```
Scaled rate      = 3.13% × (32,000 / 100,000) = 3.13% × 0.32 = 1.0016%
Eligible balance = $32,000 − $10,000          = $22,000
Interest         = $22,000 × 0.010016         = $220.35 / year
Effective yield  = $220.35 / $32,000          = 0.6886%
                                              = $18.36 / month
```

**0.69%.** Worse than Wallbit at any of its quoted rates. Do not hold cash as cash
at IBKR.

### 3.2 …but IBKR is still the right venue, because SGOV is not cash

The workaround is complete: **SGOV is a security, not a cash balance.** Buy it and
neither the $10,000 exclusion nor the NAV scaling applies. You get the full
3.60%.

| | SGOV at IBKR |
|---|---|
| 30-day SEC yield | **3.60%** (as of 2026-08-25) |
| What it holds | US Treasury bills, 0–3 months |
| Credit risk | US Treasury only — the cleanest available |
| Liquidity | Sell any market day, T+1 settlement |
| Expense ratio | ~0.09% — **already deducted** from the SEC yield |
| IBKR availability to Colombians | Yes, confirmed available as of 2026 |
| Minimum | No minimum for a Cash Account |

Duration risk is close to zero: an ETF of 0–3 month bills reprices with the front
end of the curve. If the Fed cuts, your yield falls — it does not mean a capital
loss.

Alternatives in the same slot, if you prefer: **BIL** (1–3 month, slightly higher
fee), **USFR** (floating-rate notes), **VMFXX** at 3.69% (Vanguard MMF, but Vanguard
generally does not open accounts for Colombian residents — IBKR does).

### 3.3 Direct T-bills

3-month T-bill at **3.79%** (2026-08-26) — the highest USD rate on this list,
because you skip the fund's fee and the broker's spread. Buyable at IBKR through
their bond desk.

`$32,000 × 0.0379 = $1,212.80/yr` — **$60.80/yr more than SGOV**.

Not worth it for you. You'd manage a manual ladder, lose the ability to sell in one
click, and pick up $5/month. Take SGOV.

### 3.4 US high-yield savings accounts — mostly not available to you

Best US HYSA rates in August 2026 run **4.10%–4.34%** (Axos 4.21%, Elevault 4.34%,
Newtek 4.20% but waitlisted). This is the highest-yielding column in the table and
it is **almost certainly closed to you**: US retail banks generally require a
Social Security Number or ITIN and a US residential address. Wallbit and similar
fintechs exist precisely because this door is shut to LatAm contractors. I'm listing
these rates for completeness, not as an option. If you have an ITIN, revisit.

### 3.5 Colombian COP options — the highest nominal yields, and a real decision

| Product | Rate (E.A.) |
|---|---|
| Ualá savings | 10.50% |
| Nu savings | 8.79% |
| Nu CDT | 9.00% – 9.70% |
| Lulo Bank savings | 7.84% |
| Lulo Bank CDT (540 days) | up to 12.00% |
| Banco de la República policy rate | 12.00% |
| Colombian inflation (July 2026, annual) | 6.03% |
| BanRep 2026 year-end inflation forecast | 6.90% |

**Real yield in COP** at Ualá:
```
(1 + 0.1050) / (1 + 0.0603) − 1 = 1.105 / 1.0603 − 1 = 4.2158%
```
That is a genuinely good real return — better than the USD real return at 3.6%
nominal.

**But you are not comparing 10.5% to 3.6%. You are comparing 10.5% in a
depreciating currency to 3.6% in a stable one.** The break-even:

```
Break-even COP depreciation = (1 + 0.1050) / (1 + 0.0360) − 1
                            = 1.105 / 1.036 − 1
                            = 6.660% per year
```

At ~3,100 COP/USD today, COP has to weaken past **~3,306 COP/USD within a year**
before the USD option wins. Below that, the COP option wins.

The market prices this gap deliberately (uncovered interest parity) — the 6.9pp
spread *is* the expected depreciation. Nobody is handing you 6.9% free. What you're
deciding is whether you want the exposure.

**My read for you specifically:** hold COP for money you will spend in COP, and USD
for everything else. Your income is USD, your rent and groceries are COP, and your
stated life goal — full-time travel — is a USD/EUR expense. Do not chase the
Colombian rate with money earmarked for a plane ticket. Do take the Colombian rate
on the slice you'd spend in Bogotá anyway, because for that slice there is no FX
risk at all — the "risk" is just your actual currency of consumption.

### 3.6 eToro cash interest — probably not available to you at a good rate

eToro advertises "up to 3.55%" but the eligibility is restrictive:

- **UK or EU residents**, OR **Gold-tier Club and above**.
- Gold requires $10,000 in realized equity. Your $13,815.32 clears it.
- Rates are tiered by Club level, and the headline 3.55% is quoted for EU clients.
  A Colombian resident at Gold will get less, and I could not find the tier table
  — `etoro.com` is blocked by this environment's egress proxy.

**Action:** open the app, find the interest-on-balance toggle in the Club dashboard,
and read your actual rate. If it's under ~3%, don't leave cash there.

### 3.7 Short-duration bond ETFs

You asked about these specifically. For this money: **no.**

SGOV *is* the short-duration answer with zero duration. Stepping out to 1–3 year
Treasuries (SHY, VGSH) or short corporates (VCSH, IGSB) adds duration and, for
corporates, credit risk — for maybe 10–30bp at the current curve shape. That is a
bad trade for cash you may need. If you want more return than 3.6%, take it in
equities (§4c), where you're paid properly for the risk, not in a bond fund that
gives you a third of the risk for a tenth of the reward.

---

## 4. Recommended allocation

Sizing logic first:

- **Emergency fund: $15,000.** 6 months × $2,500 (your midpoint). Six, not three,
  because you're an **independent contractor in Colombia** — no severance, no
  unemployment insurance, no notice period. Your income has a single point of
  failure (Crowd Cow) and no statutory cushion behind it.
- **Business capital: $7,000.** Your repo commits $5,000–$10,000, staged, to a side
  business. That's a real claim on this cash. I've taken the midpoint and parked it
  somewhere it earns while it waits.
- **Long-term: $10,000.** The remainder. You're 27 with a 3+ year horizon, moderate
  risk tolerance, and a $2,100/mo savings surplus refilling the tank. Holding all
  $32,000 in cash equivalents at 27 is the more expensive mistake.

### (a) Instant-access cash — $5,000 (15.6%)

| Amount | Where | Rate | Why |
|---:|---|---|---|
| $2,000 | Wallbit remunerated (USD) | ~2.85%? | Instant to checking; USD; travel and same-day needs |
| $3,000 | Ualá or Nu savings (COP) | 10.50% / 8.79% E.A. | Bogotá emergencies — no FX risk, because you'd spend it in COP anyway |

**Stay on Wallbit's free tier** — $2,000 is below the ~$4,000 break-even for a paid
plan (§2.5).

### (b) Yield-bearing cash — $17,000 (53.1%)

| Amount | Where | Rate | Why |
|---:|---|---|---|
| $17,000 | **SGOV at Interactive Brokers** | 3.60% | $10,000 emergency tier 2 + $7,000 business capital |

One position, one ticker. Sellable any market day, T+1. US Treasury credit only.
Both sub-buckets have the same requirement — safe, liquid, earning — so don't
overcomplicate it with two holdings.

### (c) Invested capital — $10,000 (31.3%)

| Amount | Where | How |
|---:|---|---|
| $10,000 | **VT**, or **VOO + VXUS**, at IBKR | $2,000/month × 5 months |

**Why broad and ex-US, specifically.** Your eToro book:

| Holding | Value |
|---|---:|
| NVDA | $2,903.42 |
| GOOG | $2,279.91 |
| QQQ | $1,705.58 |
| AAPL | $1,594.61 |
| AMZN | $368.86 |
| TSLA | $355.58 |
| **US tech / Nasdaq subtotal** | **$9,207.96** |
| VOO (broad) | $1,592.51 |
| **Total positions** | **$10,800.47** |

**85% of your equity exposure is US mega-cap tech**, and QQQ overlaps NVDA, AAPL,
GOOG and AMZN, so the true concentration is worse than the line items suggest.
Every position is up (+$4,902 unrealized), which feels like validation and is
actually just one factor having worked. Adding another dollar of US tech here is
adding risk you already own twice.

VT gives you ~9,000 companies across developed and emerging markets in one ticket.
Boring is the point. Staging over 5 months at $2,000/month is not market timing —
it's a hedge against your own regret if you deploy the lot the week before a
drawdown.

### Summary

| Bucket | Amount | % | Blended rate |
|---|---:|---:|---|
| (a) Instant-access | $5,000 | 15.6% | ~7.44% |
| (b) Yield-bearing cash | $17,000 | 53.1% | 3.60% |
| (c) Invested | $10,000 | 31.3% | equity |
| **Total** | **$32,000** | **100%** | |

**Yield on the cash portion ($22,000):**
```
Wallbit    $2,000 × 0.0285 = $ 57.00
COP HYSA   $3,000 × 0.1050 = $315.00
SGOV      $17,000 × 0.0360 = $612.00
                              -------
                              $984.00 / year
Blended:   $984.00 / $22,000 = 4.4727%
```

Note what this beats: **$984/yr on $22,000 of cash > $912/yr on all $32,000 in
Wallbit.** The recommended split earns more money on $10,000 less capital, and puts
that $10,000 to work in equities. That is the entire argument in one line.

---

## 5. Mechanics

### 5.1 Execution order

| # | Move | Route | Cost | Time |
|---|---|---|---:|---|
| 1 | Open IBKR account | Online, Colombian passport + proof of address | $0 | 2–5 days |
| 2 | Rippling $14,000 → Wallbit | ACH | **$0** | 1–2 bd |
| 3 | Payoneer $15,000 → Wallbit or Wise (USD→USD) | ACH | **$1.50** | 1–2 bd |
| 4 | $17,000 → IBKR | ACH from Wallbit/Wise USD | $0 | 1–3 bd |
| 5 | $10,000 → IBKR | same, staged | $0 | — |
| 6 | Buy SGOV × $17,000 | IBKR | ~$1 | same day |
| 7 | Wise $3,000 → Ualá/Nu (USD→COP) | Wise | **$10–60** | 1–2 bd |
| 8 | Keep $2,000 in Wallbit remunerated | — | $0 | instant |
| | **Total one-time cost** | | **~$15–65** | |

**~$15–65 to unlock ~$984/year. Payback in under a month.**

On step 3: Payoneer withdrawals go to a bank account **in your own name**. IBKR ACH
details may or may not pass Payoneer's name-matching. Routing through Wallbit or
Wise first is the safer path — both give you US account details in your name. Test
with $100 before moving $15,000.

### 5.2 Fees and FX, itemised

| Route | Fee | Notes |
|---|---|---|
| Rippling → Wallbit | **$0** | Already your payroll path |
| Payoneer → USD bank (same currency) | **$1.50** flat | Under $50k/month; 0.5% above |
| Payoneer → COP (cross-currency) | **~2%, up to 3.5%** | **Avoid.** $300 on $15,000 |
| Wise → COP | 0.33%–~2% | Mid-market rate, no markup; fee varies by funding method |
| Wallbit → Colombian bank | **~$0.35** + spread | Spread not published |
| IBKR ACH deposit | $0 | First per month free |

**The only FX conversion in this plan is $3,000 USD→COP.** Everything else stays in
USD. Get a live quote from both Wise and Wallbit for that exact $3,000 and take the
better one — Wise publishes its fee up front, Wallbit's spread isn't published, so
compare the COP you'd actually receive, not the advertised fee.

Even at the worst case it pays back fast:
```
Payback (months) = (FX cost % / 10.5%) × 12
  at 2.0%:  (0.020 / 0.105) × 12 = 2.29 months
  at 0.5%:  (0.005 / 0.105) × 12 = 0.57 months
```

### 5.3 Tax

**Colombian tax on the interest.** Interest and financial yields — including foreign
ones — go into **rentas de capital** within the **cédula general**, taxed at the
Art. 241 progressive table (0%–39%, Ley 2277 de 2022). At ~$4,600/mo
(≈COP 171M/yr at 3,100), your marginal bracket is most likely **28%**, possibly
**33%** after deductions land.

```
Gross cash yield          $984.00
  at 28% marginal:  tax   $275.52  →  net $708.48
  at 33% marginal:  tax   $324.72  →  net $659.28
```

**Componente inflacionario.** Colombian residents can exclude the inflation
component of financial yields (Arts. 38–41 ET) — but **only for yields from entities
supervised by the Superintendencia Financiera**. That means:

- **COP interest (Ualá/Nu): partly exempt.** With inflation at 6.03% against a
  10.5% nominal rate, a substantial share may be non-taxable. **Do not compute this
  yourself** — DIAN sets the percentage annually by decree. Ask your contador for
  the 2026 figure.
- **USD interest (SGOV, Wallbit): fully taxable.** No relief. This narrows the COP
  vs USD gap further in COP's favour, after tax.
- **Watch this:** the 2026 tax reform bill proposes **eliminating** the componente
  inflacionario exclusion, effective from tax year 2027. If it passes, the COP leg
  gets worse.

**US withholding on SGOV.** Colombia has **no tax treaty with the US**, so the
default NRA withholding is **30%** — which would gut a 3.6% yield to 2.52%. The
escape is **IRC §871(k)**: distributions designated as *Qualified Interest Income*
(QII) are exempt from NRA withholding, and a 0–3 month T-bill fund's distributions
are overwhelmingly QII. iShares publishes QII percentages annually.

Two conditions:
1. **File a W-8BEN** with IBKR at account opening. Non-negotiable.
2. **Confirm your broker applies the QII exemption.** IBKR does. eToro — verify
   before assuming; if it doesn't, SGOV at eToro is materially worse than at IBKR.

**Formulario 160 — foreign asset declaration. You are probably already required to
file this.** Colombian residents holding foreign assets above **2,000 UVT** at
January 1 must file. UVT 2026 = **COP 52,374**, so the threshold is
**COP 104,748,000**.

```
Current foreign assets:
  Idle cash                     $32,000.00
  eToro account                 $13,815.32
                                ----------
                                $45,815.32
  × 3,100 COP/USD          = COP 142,027,492   >  COP 104,748,000  ✗ over
```

You are **~36% over the threshold**. This obligation exists independently of whether
you owe income tax, and it applies whether or not you follow this plan. Penalties
for late filing are significant. **Check with your contador whether you filed for
2026, and for prior years.** Individual assets above 3,580 UVT (COP 187,498,920)
must be itemised — you're below that per account.

**Cuenta de compensación (BanRep).** Foreign accounts used to channel
mandatory-channeling FX operations must be registered with Banco de la República
within a month of opening, and generate monthly reporting to BanRep and DIAN.
Personal savings and portfolio investment abroad are generally *not* mandatory
channeling — but Colombian investment abroad has its own registration rules and
this is genuinely jurisdiction-specific. **Ask your contador.** I'm flagging it, not
resolving it.

---

## 6. Two things outside the $32,000

**1. Your $2,809.55 idle at eToro.** Same problem, smaller. Check your actual Club
tier rate in the app. If it's under ~3%, move it to SGOV or deploy it into VT
alongside bucket (c).

**2. Your $2,100/month surplus.** This exercise repeats itself every 15 months if
you don't automate it. Set a standing rule: on payday, $X to Wallbit checking for
spending, the rest sweeps to SGOV. The problem you're solving today is really a
process gap, not an allocation gap.

---

## 7. If you don't want to open IBKR

Legitimate 20-minute fallback: **move all $32,000 into Wallbit's remunerated
account.** Zero new accounts, zero FX, uses rails you already have.

```
$32,000 × 0.0285 = $912.00 / year  =  $76.00 / month
```

That captures **79%** of the recommended plan's $1,152 SGOV-equivalent, and **93%**
of what $32,000 in SGOV alone would yield. What you give up:

- All $32,000 concentrated behind one fintech intermediary (§2.3)
- Nothing invested — $10,000 sits in cash for 3+ years at 27
- No COP leg, so no exposure to the best real yield available to you
- You'd now need a paid Wallbit plan for the good rate ($32,000 ≫ $4,000 break-even)

It's the right call **only** if the friction of opening IBKR is what's actually
stopping you from acting. Doing this today beats doing the optimal thing in
November. $76/month is $76/month.

---

## 8. Assumptions

1. "No need for 3+ years" means you will not need this money for 3+ years.
2. Monthly expenses ≈ $2,500 (midpoint of the $2,000–$3,000 in `finances.md`).
3. Emergency fund = 6 months, not 3, because you are an independent contractor
   with no severance or unemployment cover.
4. The $5,000–$10,000 business capital in `finances.md` comes **out of** this
   $32,000, not in addition to it. **If it's separate, tell me — the allocation
   changes materially.**
5. Your marginal Colombian income tax rate is 28%. Could be 33%.
6. COP/USD ≈ 3,100. Sources on 2026-08-27 ranged 3,056–3,138; I used the middle.
7. Your Wallbit rate is the 2.85% you quoted. Unverified — see §2.1.
8. Rippling, Payoneer and Wise balances are all in USD and freely withdrawable
   with no lock-up or pending-settlement holds.
9. Rippling holds a withdrawable balance (rather than being pass-through payroll) —
   implied by your $14,000 figure.
10. IBKR onboarding succeeds for you as a Colombian resident. Reported available in
    2026, but individual approval isn't guaranteed.
11. SGOV's expense ratio is ~0.09% and the quoted 3.60% SEC yield is net of it.
12. SGOV distributions qualify as QII under §871(k) and your broker applies it, so
    US withholding is ~0%.
13. Rates are as of 2026-08-25/26/27 and **all of them float**. SGOV, MMFs, Wallbit
    and the Colombian accounts will all reprice if BanRep or the Fed moves.
14. Colombian HYSA rates (Ualá 10.5%, Nu 8.79%) are as published in July 2026 and
    may carry balance caps or conditions I could not verify.

---

## 9. Materially uncertain — verify before acting

1. **Wallbit's actual APY.** Three conflicting published figures, none matching your
   2.85%. Read it in the app.
2. **Whether Wallbit's yield is the Alpaca FDIC sweep or the DGCXX money market
   fund.** This determines whether FDIC applies at all. Sources conflict; one says
   it recently changed. **Ask Wallbit support directly, in writing.**
3. **Wallbit's plan pricing.** My $5/mo break-even example is illustrative, not a
   real price.
4. **Wallbit's regulatory status as an entity.** Alpaca Securities is SEC/FINRA
   registered and that's verifiable. What Wallbit *itself* is registered as — and
   in which jurisdiction — I could not establish.
5. **Your eToro Club tier rate as a Colombian resident.** The 3.55% headline is
   quoted for EU/UK.
6. **Wise's actual USD→COP cost on $3,000.** Quotes ranged 0.33% to ~2%. Get a live
   in-app quote.
7. **Whether Payoneer will send to IBKR directly.** Test with $100.
8. **Whether the componente inflacionario applies and at what percentage for 2026** —
   and whether the reform bill eliminating it passes.
9. **Whether you have a Formulario 160 obligation for 2026 or prior years.**
10. **Whether any BanRep cuenta de compensación registration applies to you.**

**Note on verification:** `wallbit.io`, `help.wallbit.io`, `etoro.com`,
`brokerchooser.com`, `tradersunion.com`, `docs.alpaca.markets`, `home.treasury.gov`,
`fred.stlouisfed.org` and `stockanalysis.com` were all **blocked by this
environment's network egress proxy**. Figures sourced from those domains come from
search-result summaries rather than the pages themselves, and carry correspondingly
lower confidence. The rates most worth re-checking at the primary source are
Wallbit's APY and the SGOV SEC yield.

---

## 10. What the repo is missing

Filling these would sharpen the next iteration:

1. **The $32,000 isn't in the repo at all.** `finances.md` documents income,
   expenses and eToro, but not the Rippling/Payoneer/Wise balances.
2. **No currency split on expenses.** How much of the $2,000–3,000/mo is COP vs
   USD? This directly sets the (a)-bucket split and I had to guess it.
3. **No COP-side assets.** Colombian bank accounts, existing CDTs, cash at hand.
4. **No debt.** Credit cards, loans, financing on the bike? Any balance above ~7%
   beats every investment on this page and should be paid first.
5. **No tax records.** Actual marginal rate, whether you use a contador, whether
   Formulario 160 has ever been filed.
6. **No insurance.** Health coverage and any disability/income protection change
   how big an emergency fund needs to be.
7. **Whether business capital is inside or outside this $32,000.** Assumption #4 —
   the single assumption most likely to change the answer.
8. **Your Wallbit plan tier and the rate you're actually being paid.**

---

## Sources

- [iShares SGOV product page](https://www.ishares.com/us/products/314116/ishares-0-3-month-treasury-bond-etf) · [SGOV Aug dividend / SEC yield](https://www.gurufocus.com/news/8998979/sgov-announces-august-dividend-with-357-sec-yield-backed-by-guru-buying)
- [US 3-month bill yield](https://tradingeconomics.com/united-states/3-month-bill-yield) · [Federal Reserve H.15](https://www.federalreserve.gov/releases/h15/)
- [Wallbit investment account (help centre)](https://help.wallbit.io/es/articles/12168091-cuenta-de-inversion-de-wallbit) · [Wallbit subscription plans](https://help.wallbit.io/en/articles/11038003-wallbit-subscription-plans) · [Wallbit risks](https://help.wallbit.io/es/articles/9092861-cuales-son-los-riesgos-de-invertir-con-wallbit) · [Wallbit deposits/withdrawals Colombia](https://help.wallbit.io/es/articles/12398611-como-hacer-depositos-y-retiros-en-colombia) · [Wallbit fees vs Wise/Payoneer](https://www.wallbit.io/en/blog/wallbit-fees-wise-payoneer-comparison-2026) · [Getting paid from Rippling](https://help.wallbit.io/en/articles/15280736-how-to-get-paid-from-rippling-with-wallbit) · [Wallbit on SIPC](https://www.wallbit.io/en/blog/sipc-insurance-what-it-is-and-how-it-works) · [TradersUnion Wallbit review](https://tradersunion.com/reviews/wallbit-io/)
- [Alpaca FDIC Sweep Program](https://docs.alpaca.markets/us/docs/fdic-sweep-program) · [Alpaca FDIC Sweep FAQ](https://alpaca.markets/support/fdic-sweep-program-faq) · [Alpaca excess SIPC](https://alpaca.markets/blog/alpaca-clearing-expands-excess-sipc-coverage-strengthening-commitment-towards-enhanced-protection/)
- [IBKR interest rates](https://www.interactivebrokers.com/en/accounts/fees/pricing-interest-rates.php) · [IBKR interest calculations](https://www.interactivebrokers.com/en/pricing/pricing-calculations-int.php) · [IBKR available countries](https://www.interactivebrokers.com/en/accounts/open-account-country-list.php) · [Best international brokers in Colombia](https://brokerchooser.com/best-brokers/best-international-online-brokers-for-citizens-in-colombia)
- [eToro interest on balance](https://www.etoro.com/investing/interest-on-balance/) · [eToro help — interest on USD cash](https://help.etoro.com/s/article/What-is-interest-on-balance?language=en_GB) · [eToro Club](https://www.etoro.com/about/club/)
- [DGCXX — Dreyfus Government Cash Management](https://www.dreyfus.com/products/mm/fund/dreyfus-government-cash-management.html) · [VMFXX](https://finance.yahoo.com/quote/VMFXX/) · [SPAXX](https://finance.yahoo.com/quote/SPAXX/)
- [Best HYSA rates Aug 2026 — NerdWallet](https://www.nerdwallet.com/banking/best/high-yield-online-savings-accounts) · [CNBC Select](https://www.cnbc.com/select/best-high-yield-savings-accounts/) · [Bankrate](https://www.bankrate.com/banking/savings/best-high-yield-interests-savings-accounts/)
- [Colombian savings account rates July 2026](https://www.lafm.com.co/economia/bancos-mayor-rentabilidad-para-ahorrar-julio-2026-404660) · [Lulo Bank CDT](https://www.portafolio.co/negocios/empresas/colombianos-podran-ahorrar-en-cdt-digitales-desde-100-000-como-abrirlos-y-cual-sera-su-rentabilidad-anual-495550) · [TasasColombia](https://tasascolombia.com/)
- [BanRep inflation forecast 2026](https://www.portafolio.co/economia/crecimiento/banco-de-la-republica-estima-que-en-el-2026-la-inflacion-cerrara-en-el-6-499467) · [Policy rate at 12%](https://es-us.noticias.yahoo.com/analistas-prev%C3%A9n-tasas-inter%C3%A9s-colombia-133000786.html) · [BanRep Monetary Policy Report April 2026](https://www.banrep.gov.co/en/publications-research/monetary-policy-report/april-2026)
- [UVT 2026](https://actualicese.com/uvt-2026/) · [Formulario 160 threshold](https://rioconsultores.com/2026/02/24/declaracion-de-activos-en-el-exterior-2026-quien-debe-presentarla-umbral-2-000-uvt-formulario-160-y-sanciones-boletin-13/) · [DIAN — declaración de activos en el exterior](https://www.dian.gov.co/impuestos/sociedades/Paginas/declaracion_activos_exterior.aspx) · [Cédulas para declarar renta 2026](https://www.rankia.co/blog/dian/3984841-cedulas-para-declarar-renta) · [Tarifa marginal renta 2026](https://colombiatramita.co/dian-impuestos/tarifa-marginal-renta/) · [PwC — reforma tributaria 2026](https://www.pwc.com/co/es/pwc-insights/reforma-tributaria-2026-ley-de-financiamiento.html) · [Bancolombia — impuestos sobre inversiones en el exterior](https://www.bancolombia.com/centro-de-ayuda/preguntas-frecuentes/impuestos-inversiones-en-el-exterior)
- [BanRep — cuentas de compensación](https://www.banrep.gov.co/es/politica-monetaria-cambiaria/regulacion-operaciones-cambiarias/generalidades-cuentas-compensacion) · [BanRep — inversión colombiana en el exterior](https://www.banrep.gov.co/es/politica-monetaria-cambiaria/regulacion-operaciones-cambiarias/inversion-extranjera-colombia-colombiana-exterior)
- [Payoneer pricing](https://www.payoneer.com/about/pricing/) · [Wise fees explained 2026](https://transferfees.io/guides/wise-fees-explained/)
- [IRS — nontaxable interest for nonresident aliens](https://www.irs.gov/individuals/international-taxpayers/nontaxable-types-of-interest-income-for-nonresident-aliens) · [26 USC §871](https://www.law.cornell.edu/uscode/text/26/871) · [iShares QII percentages](https://www.ishares.com/us/literature/tax-information/ishares02022026exdatemonthlyqiimemostamped.pdf)
