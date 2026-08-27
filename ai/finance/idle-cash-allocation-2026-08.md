# Idle Cash Allocation — $32,000

**Date:** 2026-08-27 · **Revised:** 2026-08-27 (rev. 2) · **For:** Daniel Bolivar
**Status:** Recommendation

> **Revision 4 reverses rev. 2 and reinstates Interactive Brokers.** Daniel pushed
> back: if the 30% is refunded, isn't SGOV at IBKR simply the best option? It is —
> that was never in dispute. Rev. 2 weighed the $91.80/yr gap against setup friction
> and called it not worth it. That reasoning was too anchored on today's balance. See
> §3.2 for what changed: the refund is automatic and in-account (verified), the gap
> scales with a portfolio growing $2,100/month, and **IBKR is the only realistic venue
> for the Irish-domiciled UCITS funds that solve the US estate-tax and dividend-
> withholding problems flagged in §4c.**
>
> **Revision 3 corrects a comparison error in rev. 2.** Rev. 2 claimed SGOV at eToro
> nets 2.52% and is therefore "worse than Wallbit" — that compared a post-*US*-tax
> figure against a pre-*Colombian*-tax figure. Once Art. 254 ET's foreign tax credit
> is applied, un-reclassified SGOV still beats Wallbit. See §6.2. The headline
> recommendation is unchanged; the eToro option is better than rev. 2 said.
>
> **Revision 2 changed the recommendation.** Daniel confirmed Wallbit's rate from
> the source (2.85% APY, Alpaca FDIC Bank Sweep) and pointed out that the Wallbit
> FAQ states the sweep *"elimina la retención automática del 30%"* the IRS applies
> to non-residents. That is correct and it is decisive — see §2.2. Combined with
> his existing Wallbit → Bancolombia COP route, **the Interactive Brokers leg and
> the Colombian peso leg are both dropped.** Rev. 1 is in git history.

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

Two ways to read it. The first is what you can capture **today**, with no new
accounts, by moving everything into Wallbit's remunerated balance:

```
$32,000 × 0.0285  =  $912.00 / year  =  $76.00 / month  =  $2.50 / day
```

The second is what the recommended plan (§4) actually does — $22,000 earning 2.85%
and $10,000 invested:

```
$22,000 × 0.0285  =  $627.00 / year  =  $52.25 / month
$10,000            →  equities, not a yield line
```

The cash figure is lower because $10,000 stops being cash. That's the point, not a
cost.

Over your stated 3-year horizon, the pure-cash version compounds to:
`$32,000 × (1.0285)³ − $32,000 = $32,000 × 1.087972 − $32,000 = $2,815.10`

$76/month is ~3.0% of your monthly expenses ($2,500 midpoint) and ~3.6% of your
monthly savings surplus ($2,100 midpoint). Not life-changing. Also free, requiring no
risk you aren't already taking and about twenty minutes of transfers.

### A note on APY vs SEC yield

Wallbit's 2.85% is an **APY** — compounding is already baked in, so `$32,000 × 0.0285`
is the correct first-year figure, not an approximation.

SGOV's 3.60% is a **30-day SEC yield**, which is simple-annualised. Reinvested monthly
it compounds slightly higher:

```
(1 + 0.036/12)^12 − 1  =  (1.003)^12 − 1  =  3.65995%
```

Worth knowing when comparing the two numbers — they aren't quoted on the same basis,
and the real gap is marginally wider than 3.60 − 2.85 suggests. It doesn't change the
conclusion in §3.2.

---

## 2. Wallbit, assessed specifically

### 2.1 Rate confirmed: 2.85% APY

Confirmed by Daniel from Wallbit's own site on 2026-08-27. Rev. 1 flagged this as
unverified because `wallbit.io` is blocked by this environment's egress proxy and
the search-result summaries quoted 2.00%/3.50% and 3.00%–3.75%. Those were wrong or
stale. **The rate is 2.85%**, and no plan upgrade is needed to get it — which also
retires the paid-plan break-even question from rev. 1.

### 2.2 Resolved: Alpaca FDIC Bank Sweep — and it is exempt from US withholding

Wallbit's FAQ settles the DGCXX-vs-sweep ambiguity from rev. 1:

> *"Los ingresos generados por la cuenta remunerada provienen del **Programa Alpaca
> FDIC Bank Sweep**, de Alpaca Securities. […] Esta **elimina la retención
> automática del 30%** a los ingresos que aplica el Servicio de Impuestos Internos
> (IRS) de EE.UU. a no residentes."*

**Both halves matter, and the second half is the one that changes the
recommendation.**

**It's a bank deposit, so FDIC applies.** Cash is swept to participating FDIC-insured
banks — $250,000 per bank, up to ~$1,000,000 aggregate. Your $22,000 sits far inside
that. This is not a money market fund; there is no NAV to break.

**It's a bank deposit, so US withholding does not apply.** Under **IRC §871(i)(2)(A)**,
interest on deposits with US banks paid to a non-resident alien is not subject to US
tax when it isn't effectively connected with a US trade or business. Wallbit's claim
is a correct statement of the law, not marketing.

This is a **structural** exemption, and that is worth more than the 0.75pp headline
gap to SGOV suggests:

| | Wallbit sweep | SGOV (a bond ETF) |
|---|---|---|
| Legal basis | §871(i)(2)(A) — bank deposit interest | §871(k) — qualified interest income |
| When it applies | At source, permanently | Withheld at 30%, **reclassified later** |
| Depends on | Nothing further | iShares publishing QII **and** your broker applying it |
| Cash-flow effect | None | Up to a year of 30% withheld before refund |

IBKR's own documentation confirms the SGOV mechanics: distributions are *"initially
classified as ordinary dividends and subject to U.S. withholding tax at the time of
payment — even if the underlying holdings (like U.S. Treasury Bills) are exempt,"*
then reclassified once the issuer supplies final classification, with the
over-withholding adjusted. You get the money, late. On a platform that doesn't run
that reclassification, you don't get it at all.

**Net effect: 2.85% at Wallbit is a clean 2.85%.** Nothing is withheld and nothing
needs reclaiming.

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

### 2.5 Paid plans — moot

Rev. 1 computed a break-even balance for upgrading to a paid tier. With 2.85%
confirmed as the rate you already receive, there is nothing to buy. Stay where you
are.

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

### 3.2 SGOV at IBKR — the recommended home for the yield bucket

SGOV is a security, not a cash balance, so neither the $10,000 exclusion nor the NAV
scaling in §3.1 applies to it.

| | 30-day SEC yield | US withholding | Net | Friction |
|---|---|---|---|---|
| Wallbit remunerated | 2.85% | 0%, permanently | 2.85% | none — account open |
| **SGOV at IBKR** | **3.60%** | 30%, auto-refunded Jan–Mar | **~3.60%** | new account, W-8BEN |
| SGOV at eToro | 3.60% | 30%; reclassification unconfirmed | 2.52%–3.60% | account open |

```
On $17,000, after Colombian tax at 28%:
  SGOV at IBKR   $612.00 × 0.72  =  $440.64
  Wallbit        $484.50 × 0.72  =  $348.84
                                    ────────
  Difference                        $ 91.80 / yr  =  $7.65 / month
```

Rev. 2 called $7.65/month too small to justify opening an account. **That was the
wrong frame.** Three corrections:

#### The refund is automatic and in-account — verified

IBKR reclassifies prior-year distributions **between January and March**, credits the
account, and reports it in the Year-to-Date Activity Statement and Dividend Report.
**No Form 1040-NR, no claim to file, nothing to chase.**

Cash-flow cost of the lag:
```
$183.60 withheld, held ~9 months on average
$183.60 × 0.0285 × 9/12  =  $3.92 / yr     — negligible
```

**One real caveat:** once IBKR files the 1042-S in March, they can no longer refund —
recovery would then require a 1040-NR you file yourself, not worth it at these
amounts. For SGOV, a large iShares fund publishing QII annually, the reclassification
is routine. It is a dependency, not a guarantee.

#### The gap scales with the balance

$7.65/month is today's figure against a $2,100/month savings rate:
```
At $50,000 in cash-equivalents:  $50,000 × 0.75% × 0.72  =  $270 / yr
```
The account is a one-time cost. The benefit compounds.

#### IBKR is where the UCITS funds are — the real argument

IBKR offers Irish-domiciled UCITS ETFs to Latin American residents and has the widest
UCITS selection of any retail broker. eToro almost certainly does not.

That matters because of §4c: your US-situs assets cross the **$60,000 US estate-tax
threshold** within about two years at your savings rate, and you pay **30% on US
dividends** with no treaty. **VWRA** fixes both — not US-situs, 15% at fund level under
the US–Ireland treaty, and *accumulating*, so it distributes nothing and defers the
Colombian tax too.

**If IBKR is open anyway, bucket (c) belongs there as VWRA** rather than VT at eToro —
starting in the right structure instead of migrating out of the wrong one later.

#### Why IBKR rather than eToro — the question, answered

SGOV **is** available on eToro at $0 commission, so eToro can technically do it. The
distinction is withholding handling:

- **IBKR** runs the reclassification cycle above, automatically.
- **eToro's** published guidance cites the 15% *treaty* rate — and Colombia has no US
  treaty, so you'd get 30% — with no mention of QII reclassification for bond ETFs.

If eToro doesn't reclassify, Art. 254 ET recovers most of it on the Colombian side
(§6.4), so it isn't a disaster — but it depends on your contador filing the credit,
and it's 2 points worse than IBKR even when it works. **IBKR is the cleaner venue and
now the recommended one.**

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

### 3.5 Colombian COP — dropped, and Daniel is right to drop it

> **Daniel's objection:** *"The $3,000 in Nu COP — better to have it anywhere else?
> For the COP I need to spend, I send from Wallbit to Bancolombia."*

**Agreed. Cut it.** The rev. 1 case for a COP leg assumed pre-converting bought you
liquidity for local emergencies. It doesn't — your Wallbit → Bancolombia route already
clears in minutes for ~$0.35. Pre-converting buys you a yield spread and nothing else,
while adding an account, an FX conversion, standing COP exposure, and a Colombian tax
line.

```
Gross give-up:  $3,000 × 10.50%  =  $315.00 / yr
Less Colombian tax and the componente inflacionario question,
call it roughly $200–230 / yr of real give-up.
```

That is the price of not holding a currency you don't need to hold yet. Pay it.

Two things worth keeping from the analysis anyway:

- **Don't park COP at Bancolombia either.** Bancolombia savings pays **0.05%–0.07%
  E.A.** — functionally zero, and below the monthly cuota de manejo on some plans.
  Converting on demand is strictly better than pre-parking there.
- **Do keep a small COP float.** Not for yield — as insurance against the one risk
  §2.3 identifies. If Wallbit is ever unreachable for a week, you want rent money in
  a Colombian bank you can touch. Roughly a month of COP expenses, which you probably
  already hold. That's not an allocation decision; it's just not running Bancolombia
  to zero.

The rate table and FX break-even below are retained for reference — revisit them if
you ever plan to hold COP deliberately.

#### Reference: the rates you're passing on

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

## 4. Recommended allocation (revised)

Sizing logic is unchanged from rev. 1:

- **Emergency fund $15,000** — 6 months × $2,500. Six, not three, because you're an
  independent contractor in Colombia: no severance, no unemployment insurance, no
  notice period. Your income has one point of failure and no statutory cushion.
- **Business capital $7,000** — your repo commits $5,000–$10,000, staged, to a side
  business. Midpoint, parked where it earns while it waits.
- **Long-term $10,000** — the remainder. You're 27, 3+ year horizon, moderate risk,
  $2,100/mo refilling the tank.

| Bucket | Amount | % | Where | Rate |
|---|---:|---:|---|---|
| **(a) Instant-access** | $5,000 | 15.6% | Wallbit remunerated | 2.85% |
| **(b) Yield-bearing cash** | $17,000 | 53.1% | **SGOV at IBKR** | 3.60% |
| **(c) Invested** | $10,000 | 31.3% | **VWRA at IBKR**, staged | equity |
| **Total** | **$32,000** | **100%** | | |

```
Cash yield:   $5,000 × 0.0285  =  $142.50
             $17,000 × 0.0360  =  $612.00
                                  ───────
                                  $754.50 / yr   vs $627.00 all-Wallbit
                                                 vs $  0.00 today
```

Keep $5,000 at Wallbit: SGOV settles T+1 and then needs a withdrawal, so you still
want something instant. Everything else moves to IBKR.

### Why the last 75 basis points are worth chasing after all

Rev. 2 routed everything to Wallbit on the grounds that $7.65/month didn't justify a
new account. §3.2 sets out why that was the wrong frame: the refund is automatic, the
gap scales with a balance growing $2,100/month, and IBKR is the only realistic venue
for the UCITS funds that fix the estate-tax and dividend-withholding problems below.

The concentration argument now cuts the same way. Rev. 2 flagged $22,000 behind a
single fintech intermediary as the residual risk in §2.3. Splitting across Wallbit and
IBKR addresses it as a side effect rather than as a deliberate cost.

**What you give up by moving $17,000 out of Wallbit:** instant liquidity on that
tranche (T+1 plus withdrawal instead of instant), and a dependency on IBKR's Jan–March
reclassification. Bucket (a) covers the same-day case; the reclassification is routine
for SGOV. Both are acceptable.

### (c) The $10,000 — what it is and why

> **Daniel:** *"and C 10k not understand that"*

Fair — rev. 1 assumed too much. Plainly:

**What you'd buy.** One fund, one ticker, that owns a slice of thousands of public
companies worldwide. **VWRA** (Vanguard FTSE All-World UCITS, Irish-domiciled, USD,
accumulating — ISIN IE00BK5BQT80) holds roughly 3,600 companies across the US, Europe,
Japan and emerging markets. Buying it once gives you the whole global stock market.

**Why VWRA rather than VT.** Rev. 2 recommended VT at eToro because IBKR wasn't in the
plan. With IBKR open, VWRA is available and is the better structure from day one — see
"Worth knowing" below. VT remains a perfectly good fallback if VWRA turns out to be
unavailable to your account.

**Why not leave it in cash.** This is the $10,000 you said you won't need for 3+
years. In Wallbit it earns 2.85%, which after Colombian tax at 28% is about 2.05% —
roughly flat against US inflation and a real loss against Colombian inflation at
6.03%. Cash is the right home for money you might need next month. It is the wrong
home for money with a three-year horizon. Over long periods global equities have
returned meaningfully more than cash — with genuine drawdowns along the way, which is
exactly the risk you're being paid to take, and which at 27 with $2,100/month of new
savings you can absorb.

**Why broad and global, not more of what you own.** Your eToro positions:

| Holding | Value |
|---|---:|
| NVDA | $2,903.42 |
| GOOG | $2,279.91 |
| QQQ | $1,705.58 |
| AAPL | $1,594.61 |
| AMZN | $368.86 |
| TSLA | $355.58 |
| **US tech / Nasdaq subtotal** | **$9,207.96** |
| VOO — your only broad holding | $1,592.51 |
| **Total positions** | **$10,800.47** |

**85% of your equity is US mega-cap tech** — and QQQ *also* holds NVDA, AAPL, GOOG
and AMZN, so you own several of those twice. If AI capex disappoints, every one of
those lines falls together. That's not seven bets; it's one bet held seven ways.

Every position being up (+$4,902) reads as confirmation. It's one factor having
worked over one period. Adding more US tech here concentrates a risk you already
carry.

**What "staged $2,000/month × 5" means.** Buy $2,000 now, $2,000 next month, and so
on for five months. This is not market timing and it will not, on average, beat
investing the lot today. It's behavioural insurance: if you deploy $10,000 and the
market drops 20% next month, the risk isn't the drawdown — it's that you sell at the
bottom. Staging makes that much less likely. If you know you won't flinch, deploy it
at once.

### Worth knowing before the portfolio gets bigger

Two US tax facts that don't bite yet but will:

- **US estate tax.** A non-US person holding US-situs assets — US stocks and
  US-domiciled ETFs like VOO, QQQ and VT — is exposed to US federal estate tax above
  a **$60,000** exemption, at rates up to 40%. Your US-situs holdings would be
  ~$10,800 today, ~$20,800 after this $10,000. Under the line, but you're adding
  $2,100/month.
- **Dividend withholding.** As a Colombian resident with no US tax treaty, you pay
  **30%** on US dividends. An investor in a treaty country pays 15%.

**Irish-domiciled UCITS ETFs fix both.** **VWRA** pays 15% at fund level under the
US–Ireland treaty instead of 30% to you, and the shares aren't US-situs, so the
estate-tax exposure disappears. It is also **accumulating** — it distributes nothing,
so there is no annual dividend to be taxed in Colombia either, and the return
compounds inside the fund until you sell.

IBKR offers Irish UCITS ETFs to Latin American residents and has the widest UCITS
selection of any retail broker. **This is the strongest single argument for opening
the account**, and it is why bucket (c) moved off eToro in rev. 4.

**One thing to confirm first:** how Colombia treats an accumulating fund. Colombia has
no PFIC-style regime, so an accumulating ETF should simply defer everything to disposal
— but I have not verified this and would not assume it. **Ask your contador before
choosing VWRA over VT.**

## 5. Mechanics

One new account, three transfers, two purchases.

| # | Move | Route | Cost | Time |
|---|---|---|---:|---|
| 1 | **Open IBKR account**, file W-8BEN | Passport + proof of address | $0 | 2–5 d |
| 2 | Rippling $14,000 → Wallbit | ACH | **$0** | 1–2 bd |
| 3 | Payoneer $15,000 → Wallbit | ACH, USD→USD | **$1.50** | 1–2 bd |
| 4 | Wise $3,000 → Wallbit | ACH, USD→USD | ~$0 | 1–2 bd |
| 5 | Confirm $5,000 sits in *remunerated*, not checking | in-app | $0 | instant |
| 6 | $27,000 → IBKR | ACH from Wallbit | $0 | 1–3 bd |
| 7 | Buy SGOV × $17,000 | IBKR | ~$1 | same day |
| 8 | Buy VWRA × $2,000, monthly × 5 | IBKR | ~$1 each | same day |
| | **Total one-time cost** | | **~$8** | |

**~$8 to unlock $754.50/year.** Payback in under a week.

Step 1 gates everything else — start it today; approval takes a few days and nothing
below can happen until it clears. **File the W-8BEN during onboarding**; IBKR prompts
for it. It won't reduce your 30% rate (no Colombia–US treaty) but without it the broker
must presume US status and apply 24% backup withholding on gross sale proceeds.

Step 3 caveat: Payoneer withdrawals go to an account **in your own name**. Wallbit's US
details are in your name, so this should pass — test with $100 first.

Step 5 is the one that's easy to skip and is the whole point of bucket (a): money in
Wallbit *checking* earns nothing. The 2.85% is on the **remunerated** balance.

Step 6: route through Wallbit rather than sending Payoneer → IBKR directly. Wallbit's
ACH out is free and avoids Payoneer's name-matching on a third-party brokerage.

### Fees and FX

| Route | Fee | Notes |
|---|---|---|
| Rippling → Wallbit | **$0** | Already your payroll path |
| Payoneer → USD (same currency) | **$1.50** flat | Under $50k/mo; 0.5% above |
| Payoneer → COP | ~2%, up to 3.5% | **Avoid** — $300 on $15,000 |
| Wallbit → Bancolombia (COP) | ~$0.35 + spread | Your existing route; minutes |
| Wallbit → IBKR (ACH) | $0 | |
| IBKR ACH deposit | $0 | First per month free |
| IBKR trade commission | ~$1 | Tiered/fixed minimum |

**There is no FX conversion anywhere in this plan.** The peso leg was the only one, and
dropping it removed it.

## 6. How the yield is taxed

**Two governments, two taxes, no connection between them.** This is the single point
worth getting right, because it's easy to assume that being exempt in one country
helps you in the other. It doesn't.

| | US withholding | Colombian income tax |
|---|---|---|
| Wallbit sweep interest | **0%** — §871(i)(2)(A) | **28%** — fully taxable |
| SGOV distributions | 30%, refunded at IBKR | **28%** — fully taxable |
| US stock / ETF dividends | **30%**, permanent | **28%** — fully taxable |

**Wallbit's exemption is from the American tax only.** Colombia taxes residents on
worldwide income (Art. 9 ET); interest from a US bank is foreign-source income and
enters *rentas de capital* in your cédula general exactly like any other. DIAN does
not care what the IRS did.

### 6.1 The Colombian side — where 28% comes from

Art. 241 ET as amended by Ley 2277 de 2022. UVT 2026 = **COP 52,374**:

| Renta líquida gravable | Marginal rate | Tax in UVT | In pesos |
|---|---|---|---|
| 0 – 1,090 UVT | 0% | 0 | up to $57,087,660 |
| 1,090 – 1,700 UVT | 19% | (base − 1,090) × 19% | to $89,035,800 |
| **1,700 – 4,100 UVT** | **28%** | (base − 1,700) × 28% + 116 | **to $214,733,400** |
| 4,100 – 8,670 UVT | 33% | (base − 4,100) × 33% + 788 | to $454,082,580 |
| 8,670 – 18,970 UVT | 35% | (base − 8,670) × 35% + 2,296 | — |
| 18,970 – 31,000 UVT | 37% | (base − 18,970) × 37% + 5,901 | — |
| > 31,000 UVT | 39% | (base − 31,000) × 39% + 10,352 | — |

```
Your gross:  $4,600/mo × 12 = $55,200/yr  ×  3,100  =  COP 171,120,000
After deductions the taxable base lands inside the 1,700–4,100 UVT band
                                                  →  28% marginal
```

The rate is **marginal**: your salary already fills the lower brackets, so every extra
peso of interest is taxed at the top rate you've reached — not at an average.

**Correction to rev. 1 and 2**, which said "28%, possibly 33%": **33% is impossible
for you.** It requires a taxable base above COP 214,733,400 ≈ $69,268, which exceeds
your gross income. The realistic alternative is **19%**, if deductions pull the base
below COP 89,035,800 ≈ $28,721 — a stretch at your income, but not impossible.
**Plan on 28%.**

```
On the recommended $22,000 in Wallbit:
  Gross                       $627.00
    at 28%:  tax $175.56   →  net  $451.44
    at 19%:  tax $119.13   →  net  $507.87
```

**Componente inflacionario does not help here.** The Arts. 38–41 ET relief applies
only to yields from entities supervised by the Superintendencia Financiera. A US bank
sweep is not one, so your Wallbit interest is taxable on the full nominal amount. Had
you taken the peso leg, part of that interest would have qualified — one more thing
dropping it gave up, though the 2026 reform bill proposes eliminating the relief from
tax year 2027 anyway.

### 6.2 The US side — what it is, and what it is not

**It is a withholding, not a filing obligation.** You never file a US tax return,
never send money to the IRS, never interact with them. The broker deducts it before
the money reaches your account. It is automatic and invisible.

**It applies to dividends and interest only — not to capital gains.** A non-resident
alien present in the US fewer than 183 days in the year is **not subject to US tax on
capital gains from US stocks, bonds or funds** (IRC §871(a)(2); withholding does not
reach gains). Your **+$4,902.31 unrealized gain owes the IRS nothing**, now or on
sale.

#### What you are actually paying on eToro today

| Holding | Value | Div. yield | Dividends/yr | 30% withheld |
|---|---:|---:|---:|---:|
| NVDA | $2,903.42 | 0.48% | $13.94 | $4.18 |
| VOO | $1,592.51 | 1.04% | $16.56 | $4.97 |
| QQQ | $1,705.58 | 0.42% | $7.16 | $2.15 |
| GOOG | $2,279.91 | 0.25% | $5.70 | $1.71 |
| AAPL | $1,594.61 | 0.35% | $5.58 | $1.67 |
| AMZN + TSLA | $724.44 | — | $0.00 | $0.00 |
| **Total** | | | **$48.94** | **$14.68** |

**$14.68 per year — about $1.22 per month.** The portfolio is tech-heavy, and tech
pays almost nothing in dividends, so a 30% rate lands on a very small base. Adding
$10,000 of VT (1.55% yield → $155/yr) takes the total to roughly **$61/yr**.

*Yields as of Aug 2026. AMZN and TSLA shown at zero — verify AMZN, whose policy I
could not confirm for 2026.*

#### The same mechanism at IBKR — but it comes back

SGOV distributions have the same 30% deducted at payment. The difference is that they
are *interest*, so once iShares publishes the QII classification, IBKR reclassifies and
refunds. **Net US tax $0**, with up to a year's lag. That is the entire distinction
behind §3.2.

#### The W-8BEN — check it is on file

It does **not** lower your rate: Colombia has no US treaty, so you stay at 30%
regardless. What it does is certify that you are **not** a US person. Without a valid
one, the broker is legally required to presume US status and apply **24% backup
withholding on gross sale proceeds** — the whole sale amount, not the gain. Selling
$10,000 of NVDA would have $2,400 taken.

eToro presents the form the first time you buy a US stock, so you have almost
certainly signed it. Confirm it exists and your NIT is entered.

### 6.3 Capital gains — where your real liability sits

The US ignores your gains. **Colombia does not**, and the rate turns entirely on
holding period:

| Holding period | Treatment | Rate |
|---|---|---|
| **≥ 2 years** | Ganancia ocasional (Art. 314 ET) | **15%** |
| **< 2 years** | Ordinary income, cédula general | **28%** (your marginal) |

```
On the current $4,902.31 unrealized gain:
  Held ≥ 2 years:  $4,902.31 × 0.15  =  $  735.35
  Held < 2 years:  $4,902.31 × 0.28  =  $1,372.65
                                        ─────────
  Difference                             $  637.30
```

**$637 decided purely by when you sell** — and more than the entire US withholding bill
several times over. NVDA's $108.89 average cost against $225.44 today suggests some
positions are already past the two-year mark. **Check open dates per position before
selling anything.**

This also argues for the staged VT purchases in §4c starting their own two-year clocks
now rather than later.

### 6.4 Why the 28% cancels out of the IBKR comparison

Because the Colombian 28% applies to **both** options, it shrinks the gap between
them by 28% rather than favouring either:

```
SGOV     $612.00 gross  → −28% →  $440.64 net
Wallbit  $484.50 gross  → −28% →  $348.84 net
                                  ────────
Difference                         $91.80 / yr  ( = $127.50 × 0.72 )
                                 = $7.65 / month
```

That is the arithmetic behind §3.2's conclusion. It is unaffected by the correction
below.

#### Art. 254 ET — the foreign tax credit, and rev. 2's error

Rev. 2 said SGOV at eToro nets 2.52% and is "worse than Wallbit." **That was wrong.**
It compared a post-US-tax figure against a pre-Colombian-tax figure.

**Art. 254 ET** lets a Colombian resident credit income tax paid abroad against the
Colombian tax on that same foreign income, **capped at the Colombian tax attributable
to it**. Excess is neither refundable nor carried forward. So a permanent 30% US
withholding is not a straight loss — it displaces the Colombian liability:

```
eToro worst case — 30% withheld, never reclassified
  Gross                              $612.00
  US tax withheld (30%)              −183.60
  Colombian tax due (28% × 612)       171.36
    less Art. 254 credit             −171.36    ← capped at the Colombian tax
  Colombian tax payable                  0.00
  Excess credit lost                    12.24    ← not carried forward
                                     ────────
  Net to you                         $428.40     vs Wallbit's $348.84
```

As total effective rates:

| | US | Colombia | **Total** | Net on $17,000 |
|---|---|---|---|---|
| Wallbit | 0% | 28% | **28%** | $348.84 |
| SGOV at IBKR | 0% (after refund) | 28% | **28%** | $440.64 |
| SGOV at eToro, credit claimed | 30% | 0% | **30%** | $428.40 |
| SGOV at eToro, **credit not claimed** | 30% | 28% | **58%** | $257.04 |

**The real gap between Wallbit and un-reclassified SGOV is two percentage points, not
thirty.** Rev. 2 overstated it badly.

Two caveats that keep this from being a slam dunk:

1. **The credit has to actually be claimed.** It needs a Form 1042-S from the broker,
   documentation of foreign tax paid, and a contador who files Art. 254 correctly.
   The bottom row of that table is what happens if it isn't — and it is much worse
   than doing nothing.
2. **A lower marginal rate makes it worse, not better.** The credit is capped at your
   Colombian tax, so at 19% you could only credit $116.28 of the $183.60 — the other
   $67.32 is wasted, and SGOV's edge over Wallbit falls from ~$80 to ~$36.

#### What this changes

Nothing about the recommendation — **§3.2 routes bucket (b) to SGOV at IBKR, where the
30% is refunded and no Art. 254 claim is needed at all.** The tax path is clean:

```
SGOV at IBKR:  0% US (refunded Jan–Mar)  +  28% Colombia  =  28% total
```

The Art. 254 analysis above matters in two situations:

1. **If IBKR doesn't approve your account.** Then SGOV at eToro becomes the fallback,
   and the credit is what makes it viable — worth ~$80/yr over Wallbit *if claimed*,
   and worth −$92/yr if not. Confirm your contador files Art. 254 before taking that
   route; without it, stay entirely in Wallbit.
2. **On your equity dividends**, where the 30% is permanent rather than refunded.
   VWRA sidesteps this by holding US shares at fund level under the US–Ireland treaty
   (15%) and distributing nothing — but if you hold VT instead, the 30% withheld on
   its dividends is creditable in Colombia under Art. 254 the same way.

**Either way, ask your contador whether they file Art. 254.** It is worth real money on
the fallback path and on any US-domiciled fund you hold.

### 6.5 Formulario 160 — you are probably already required to file

Unchanged, unaffected by any of these decisions, and the most time-sensitive item in
this document.

Colombian residents holding foreign assets above **2,000 UVT** at January 1 must file
the declaración de activos en el exterior. At UVT 2026 = COP 52,374, the threshold is
**COP 104,748,000**.

```
Idle cash                       $32,000.00
eToro account                   $13,815.32
                                ──────────
                                $45,815.32
× 3,100 COP/USD          =  COP 142,027,492
Threshold                =  COP 104,748,000
                            ~36% OVER — filing obligation
```

This applies whether or not you owe income tax, and whether or not you follow this
plan. Penalties for late filing are significant. **Ask your contador whether you filed
for 2026, and for prior years.** Individual assets above 3,580 UVT (COP 187,498,920)
must be itemised — you're below that per account.

### 6.6 Cuenta de compensación

Foreign accounts used to channel mandatory-channeling FX operations must be registered
with Banco de la República within a month of opening, and generate monthly reporting to
BanRep and DIAN. Personal savings and portfolio investment abroad are generally *not*
mandatory channeling — but Colombian investment abroad has its own registration rules
and this is genuinely jurisdiction-specific. **Ask your contador. I'm flagging it, not
resolving it.**

---

## 7. The standing rule

Your **$2,100/month surplus** means this entire exercise repeats itself every fifteen
months unless you automate it. The problem you solved today is a process gap, not an
allocation gap.

### Set it once

1. Rippling → Wallbit — already automatic, $0.
2. Spending money → Wallbit checking; convert to COP at Bancolombia as needed.
3. Keep bucket (a) topped up at ~$5,000 in Wallbit **remunerated**.
4. **Everything above that → IBKR, monthly.** Split it: SGOV while you're still
   building the cash buffer, VWRA once the buffer is full.

Step 4 is the one that matters. Idle cash is a default, not a decision — the only
durable fix is making *earning* the default state instead.

### And the $2,809.55 at eToro

Still idle, still outside the $32,000. Check your Club tier's actual interest rate in
the app; if it's under 2.85% — likely, since the 3.55% headline is quoted for EU/UK
clients — move it to IBKR along with everything else.

**On eToro generally:** once IBKR is open, there's a reasonable case for consolidating
the existing $10,800 of positions there too — real share ownership, cheaper execution,
UCITS access, and one fewer platform. **Don't rush it**: selling to transfer would
realise gains and trigger the Colombian capital-gains timing question in §6.3. Check
each position's holding period first, or ask IBKR about an in-kind transfer (ACATS
doesn't apply to eToro, but they may support a manual transfer).

## 8. Assumptions

1. "No need for 3+ years" means you will not need this money for 3+ years.
2. Monthly expenses ≈ $2,500 — midpoint of the $2,000–$3,000 in `finances.md`.
3. Emergency fund = 6 months, not 3, because you're an independent contractor with
   no severance or unemployment cover.
4. **The $5,000–$10,000 business capital comes out of this $32,000, not in addition
   to it. If it's separate, tell me — the allocation changes materially.** Still the
   single assumption most likely to change the answer.
5. Your marginal Colombian income tax rate is 28% (§6.1). Could be 19% if
   deductions are aggressive; 33% is arithmetically impossible at your income.
6. Wallbit's 2.85% is variable and will move with the Fed, like every other rate
   here. It is not contractually fixed.
7. Wallbit's FDIC pass-through works as described — i.e. their "for benefit of"
   records at the sweep banks are accurate. This is the assumption §2.3 is about,
   and it is not verifiable from outside.
8. Rippling, Payoneer and Wise balances are all USD and freely withdrawable, with no
   lock-up or pending-settlement holds.
9. Rippling holds a withdrawable balance rather than being pass-through payroll —
   implied by your $14,000 figure.
10. VT is available to your eToro account. SGOV is confirmed listed; VT is very
    likely but I did not verify it specifically.
11. You keep roughly a month of COP expenses at Bancolombia as Wallbit-outage
    insurance (§3.5) — assumed already true, not funded from this $32,000.
12. Rates are as of 25–27 Aug 2026 and **all of them float**.

**Resolved since rev. 1 — no longer assumptions:** Wallbit's rate (2.85%, confirmed
by you from source), the yield source (Alpaca FDIC Bank Sweep, confirmed), and the
US withholding treatment (§871(i)(2)(A), exempt).

## 9. Materially uncertain — verify before acting

Rev. 1 listed ten. Six are resolved. What's left:

1. **Whether IBKR approves your account.** Everything else depends on it. Start the
   application first.
2. **Whether VWRA is available to your IBKR account** once open. VT is the fallback.
3. **How Colombia treats an accumulating fund** like VWRA — ask your contador before
   choosing it over VT.
4. **Whether Payoneer will send to Wallbit's US account details.** Should pass — same
   name — but test with $100.
3. **Your eToro Club tier's actual cash interest rate**, for the $2,809.55 already
   sitting there. The 3.55% headline is quoted for EU/UK.
4. **Your actual marginal Colombian rate**, and how your contador treats foreign
   interest in the cédula general.
5. **The open date on each eToro position**, to know which have crossed the two-year
   ganancia ocasional line (§6.3). Worth $637 on the current gain.
6. **That your W-8BEN is on file at eToro with your NIT entered** (§6.2).
7. **Whether your contador files the Art. 254 ET foreign tax credit.** This is the
   gate on the SGOV-at-eToro option in §6.2 — without it that option goes from
   best-available to worst-available.
8. **Whether you have a Formulario 160 obligation for 2026 or prior years** — see
   §6.5. Time-sensitive and independent of everything else here.
9. **Whether any BanRep cuenta de compensación registration applies to you.**

**Resolved in rev. 2:** Wallbit's APY; whether the yield comes from the Alpaca FDIC
sweep or a money market fund; whether US withholding applies to it; Wallbit's plan
pricing (moot); whether SGOV is available on eToro (it is); the Wise USD→COP cost
(no longer relevant — no FX conversion in the plan).

**Still not directly verifiable here:** Wallbit's own regulatory status as an entity.
Alpaca Securities is SEC/FINRA-registered and that's checkable. What Wallbit *itself*
is registered as, and where, I could not establish — `wallbit.io` remains blocked by
this environment's egress proxy. Given $22,000 now sits there, it's worth asking them
directly.

## 10. What the repo is missing

Filling these would sharpen the next iteration:

1. **The $32,000 isn't in the repo at all.** `finances.md` documents income,
   expenses and eToro, but not the Rippling/Payoneer/Wise balances.
2. **No currency split on expenses.** How much of the $2,000–3,000/mo is COP vs
   USD? Less critical now that the COP leg is dropped, but it's what would tell you
   how large the Bancolombia float in §3.5 should be.
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
