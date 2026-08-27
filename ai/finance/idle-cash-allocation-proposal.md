# Idle Cash Allocation Proposal
**Daniel Bolivar · August 2026**

---

## Executive Summary

Move **$32,000** from idle accounts (Rippling, Payoneer, Wise) into yield-bearing and invested positions, capturing **$627–$912/year** in new income depending on execution timing. Plus **$2,809** available at eToro.

**Payoneer's $15,000 has no fee-free exit.** Payoneer charges a flat **2% on every bank withdrawal, to every destination and currency** (confirmed directly in-app — not a cross-currency fee, just their standing rate). That's a one-time **$300** cost. Rippling and Wise, by contrast, already have $0-fee routes out (Rippling → Wallbit direct; Wise ACH is free), so **only the Payoneer leg pays the fee — route Rippling and Wise around Payoneer, don't consolidate through it.**

**Total opportunity:** Move **$34,809** idle → productive, net **$300** in unavoidable fees. **Net deployed: $31,700 + $2,809.55 eToro.**

---

## Allocation Plan

### Bucket A: Wallbit (Cash, FDIC Sweep)
**~$21,700 at 2.85% APY**

- **Account:** Wallbit (you already have one)
- **Product:** Standard Plan, Alpaca FDIC Bank Sweep
- **Sourcing:** $14,000 from Rippling (direct, $0 fee, existing route) + ~$7,700 net proceeds forwarded from the Payoneer withdrawal (see Bucket B sourcing and Execution Sequence)
- **Why:** 
  - US §871(i)(2)(A) exemption: 0% automatic withholding on FDIC deposits
  - No Colombian tax on US deposit income (tax-treaty treaty treatment)
  - Instant access if needed (true emergency liquidity)
- **Annual yield:** ~$618 gross (at $21,700)
- **Tax impact:** $618 × 28% Colombian tax = **$173 net tax**. After-tax yield: **~$445/year**

### Bucket B: Interactive Brokers (Equities + Treasury)
**$10,000 staged over 5 months**

**Instrument:** SGOV (iShares Short-Term Treasury ETF)
- 30-day SEC yield: 3.60%
- Tax-treaty withholding: **30% automatic** (US non-resident alien rule)
- **But:** IBKR automatically reclassifies dividends Jan–Mar → refunded to account as realized income
- Net annual yield (after US refund): ~$360
- Colombian tax: $360 × 28% = $100.80. After-tax: **$259.20/year**

**Execution (staged):**
1. Month 1: $2,000 → SGOV
2. Month 2: $2,000 → SGOV
3. Month 3: $2,000 → SGOV
4. Month 4: $2,000 → SGOV
5. Month 5: $2,000 → SGOV

**Why stage?** Behavioral hedge against panic-selling in a market drawdown. Builds conviction as positions settle.

**Why IBKR + SGOV?**
- Only practical venue for Irish-domiciled UCITS (VWRA, etc.) later if you choose to add diversification
- Automatic withholding refund in-account (no paper chase, no foreign tax credits needed)
- No entity-level dividend withholding (vs. eToro's 3–5% fund-level costs)

**Sourcing:** $3,000 from Wise (direct, $0 fee) + $7,000 forwarded from Wallbit's free ACH-out, itself funded by the net Payoneer proceeds. This avoids a second 2% Payoneer withdrawal — the whole $15,000 Payoneer balance exits Payoneer once, then gets re-split for free from inside Wallbit.

### Bucket C: eToro (Hold for now)
**$2,809.55 available cash**

- **No action required now.** Keep in eToro to avoid redundant transfers.
- **Fallback use:** If any unexpected needs arise during the 5-month staging window, liquidate here first (instant access).
- **Future option:** Move to Wallbit after IBKR staging is complete (if market conditions stable).

---

## Execution Sequence

**Key change from earlier drafts: don't route Rippling or Wise through Payoneer.** Payoneer charges a flat 2% on every withdrawal regardless of destination or currency — confirmed in-app, not a cross-currency artifact. Rippling and Wise both already have $0-fee exits, so only the Payoneer balance itself should touch that 2%, and only once.

| Step | Action | Timing | Account | Amount | Notes |
|---|---|---|---|---|---|
| 1 | Transfer: Rippling → Wallbit | Day 1 | Rippling | $14,000 | Direct, $0 fee (existing payroll route per `ai/persona/finances.md`) |
| 2 | Withdraw: Payoneer → Wallbit | Day 1 (parallel) | Payoneer | $15,000 gross | **2% fee = $300.** Net $14,700 arrives at Wallbit. One withdrawal only — don't split this across two Payoneer transfers, the fee is the same either way and splitting doubles the paperwork. |
| 3 | Enable FDIC sweep | Day 4 | Wallbit | ~$28,700 (combined) | Sweep automatically invests idle balance into FDIC bank sweep while step 4 is arranged. |
| 4 | Forward: Wallbit → IBKR | Day 5 | Wallbit | $7,000 | Free ACH out — re-splits part of the Payoneer proceeds toward the IBKR target without a second Payoneer fee. |
| 5 | Transfer: Wise → IBKR | Day 1 (parallel) | Wise | $3,000 | ACH funding for IBKR, free. Leave remaining Wise balance as buffer. |
| 6 | Buy SGOV (Month 1) | Day 8 | IBKR | $2,000 | Limit order; settle T+1 automatically. |
| 7 | Buy SGOV (Month 2–5) | Monthly | IBKR | $2,000 each | Same process, recurring, from the $10,000 IBKR pool. |
| 8 | Monitor refund | Jan–Mar 2027 | IBKR | — | US withholding refund posts to account (realized income line). |

---

## Fee Summary

| Venue | Fee | Amount | Notes |
|---|---|---|---|
| Rippling → Wallbit | Flat | $0 | Existing free payroll route |
| **Payoneer → Wallbit** | **2% of balance** | **$300** | Confirmed in-app: 2% applies to every destination and currency, not just cross-currency. No fee-free exit found for this balance. |
| Wallbit → IBKR | Flat | $0 | Free ACH out, re-splits Payoneer proceeds without a second fee |
| Wise → IBKR | Flat | $0 | ACH funding, free |
| IBKR SGOV (50 shares × 5 months) | Per-trade | ~$1.00/trade | ~$5 total over 5 months |
| **Total fees** | | **~$305** | Almost entirely the unavoidable Payoneer 2% |

**Worth checking before accepting the $300:** (1) Payoneer's "Otras tarifas" tab for a rail not shown in the standard withdrawal view, (2) a direct call to Payoneer support asking whether the account qualifies for a lower ACH tier — some Payoneer account types get a $1.50 flat fee instead of 2%, this account currently doesn't. If neither pans out, $300 is a one-time cost against ~$450–900/year in new yield — well worth paying rather than leaving $15,000 at 0%.

---

## Tax Treatment

### US Tax (Non-Resident Alien)
- **FDIC deposits (Wallbit):** 0% withholding (§871(i)(2)(A))
- **SGOV dividends (IBKR):** 30% withholding at source, **refunded in-account** Jan–Mar 2027 (you receive realized income, not a refund check)
- **Capital gains:** 0% withholding on appreciation (US does not tax capital gains for non-residents)

### Colombian Tax (Resident)
- **All foreign-source income:** Flat 28% (incluye intereses y dividendos)
  - Wallbit: ~$618 × 28% = ~$173
  - IBKR SGOV: $360 × 28% = $100.80
- **Foreign tax credit (Art. 254 ET):** You may offset US withholding paid against Colombian liability (if withholding occurs before refund; after refund, no credit is needed on the US side)

**Bottom line:** After-tax yield from both sources is **~$445/year** on the ~$31,700 net deployed. The $300 Payoneer fee pays for itself in well under a year.

---

## Cash Position After Execution

| Account | Balance | Purpose |
|---|---|---|
| Rippling | $0 | (emptied) |
| Payoneer | $0 | (emptied, minus $300 fee paid) |
| Wise | $0 | (emptied) |
| Wallbit | ~$21,700 | Income generation + daily spending |
| IBKR | $10,000 (after 5 × $2,000 purchases) | Growth + diversification, staged |
| eToro | $2,809.55 | Fallback liquidity |
| **Total deployed** | **~$34,509.55** | |
| **Fee paid** | **$300** (one-time, Payoneer 2%) | |

---

## Assumptions & Risks

### Assumptions
1. **Wallbit FDIC sweep remains at 2.85% APY** during the next 12 months (may decline if Fed rates fall)
2. **SGOV yield remains ~3.60%** (Treasury yield moves daily; staging hedges timing risk)
3. **IBKR refund process is automatic and in-account** (verified; you don't file a form)
4. **Colombian tax rate remains 28%** (legislative risk, low probability in 2026–2027)
5. **No major life disruption** during 5-month staging window (emergencies use eToro fallback)

### Risks
- **Interest rate decline:** If Fed cuts rates sharply, Wallbit and SGOV both yield less. Staged purchase of SGOV mitigates timing risk.
- **Tax law change:** Colombian government could revise non-resident taxation. Unlikely but possible in future years.
- **Fraud/account freeze:** Extremely rare at established institutions (Wallbit, IBKR), but possible in edge cases (e.g., sanction list match). Mitigation: use accounts you already operate (Wallbit) and well-regulated brokers (IBKR).

---

## Next Steps

1. **Optional, before anything else:** Call Payoneer support and ask if the account qualifies for a lower ACH withdrawal tier than the standard 2%. Low probability, costs nothing to ask.
2. **Day 1:** Initiate two transfers in parallel:
   - Rippling → Wallbit ($14,000, direct, $0 fee)
   - Payoneer → Wallbit ($15,000 gross, 2% fee, $14,700 net)
   - Wise → IBKR ($3,000, direct, $0 fee)
3. **Day 4:** Enable Wallbit's FDIC sweep on the combined balance.
4. **Day 5:** Forward $7,000 from Wallbit → IBKR (free ACH out) to complete the $10,000 IBKR pool.
5. **Day 8 onward:** Monthly SGOV purchases ($2,000 each, 5 months).
6. **Jan 2027:** Monitor IBKR for US withholding refund posting.

---

## Reference Documents
- Full analysis: `ai/finance/idle-cash-allocation-2026-08.md`
- Interactive plan: [Artifact HTML]
- Tax details: `ai/finance/` (as needed)

---

**Status:** Ready to execute · **Last reviewed:** 2026-08-27
