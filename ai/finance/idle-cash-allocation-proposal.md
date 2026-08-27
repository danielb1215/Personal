# Idle Cash Allocation Proposal
**Daniel Bolivar · August 2026**

---

## Executive Summary

Move **$32,000** from idle accounts (Rippling, Payoneer, Wise) into yield-bearing and invested positions, capturing **$627–$912/year** in new income depending on execution timing. Plus **$2,809** available at eToro.

**Total opportunity:** Move **$34,809** idle → productive.

---

## Allocation Plan

### Bucket A: Wallbit (Cash, FDIC Sweep)
**$22,000 at 2.85% APY**

- **Account:** Wallbit (you already have one)
- **Product:** Standard Plan, Alpaca FDIC Bank Sweep
- **Why:** 
  - US §871(i)(2)(A) exemption: 0% automatic withholding on FDIC deposits
  - No Colombian tax on US deposit income (tax-treaty treaty treatment)
  - Instant access if needed (true emergency liquidity)
- **Annual yield:** $627 gross
- **Tax impact:** $627 × 28% Colombian tax = **$175.56 net tax**. After-tax yield: **$451.44/year**

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

### Bucket C: eToro (Hold for now)
**$2,809.55 available cash**

- **No action required now.** Keep in eToro to avoid redundant transfers.
- **Fallback use:** If any unexpected needs arise during the 5-month staging window, liquidate here first (instant access).
- **Future option:** Move to Wallbit after IBKR staging is complete (if market conditions stable).

---

## Execution Sequence

| Step | Action | Timing | Account | Amount | Notes |
|---|---|---|---|---|---|
| 1 | Transfer: Rippling → Payoneer | Day 1 | Rippling | $14,000 | ACH, ~1–2 business days |
| 2 | Transfer: Payoneer → Wise | Day 4 | Payoneer | $14,000 + $15,000 = $29,000 | Consolidate into Wise (no fee) |
| 3 | Transfer: Wise → Wallbit | Day 6 | Wise | $22,000 | ACH, ~1–2 business days. Deposit to Wallbit checking. |
| 4 | Enable FDIC sweep | Day 8 | Wallbit | $22,000 | Sweep automatically invests idle balance into FDIC bank sweep. |
| 5 | Transfer: Wise → IBKR | Day 6 (parallel) | Wise | $7,000 | ACH funding for IBKR brokerage account. Leave $1,000 buffer in Wise. |
| 6 | Buy SGOV (Month 1) | Day 10 | IBKR | $2,000 | Limit order; settle T+1 automatically. |
| 7 | Buy SGOV (Month 2–5) | Monthly | IBKR | $2,000 each | Same process, recurring. |
| 8 | Monitor refund | Jan–Mar 2027 | IBKR | — | US withholding refund posts to account (realized income line). |

---

## Fee Summary

| Venue | Fee | Amount | Notes |
|---|---|---|---|
| Payoneer → Wise | Flat | ~$1.50 | One-time, ACH for 1099 reporting |
| Wise → Wallbit | Flat | $0 | ACH, no fee |
| Wise → IBKR | Flat | $0 | ACH funding, free |
| IBKR SGOV (50 shares × 5 months) | Per-trade | ~$1.00/trade | ~$5 total over 5 months |
| **Total fees** | | **~$6.50** | Negligible |

---

## Tax Treatment

### US Tax (Non-Resident Alien)
- **FDIC deposits (Wallbit):** 0% withholding (§871(i)(2)(A))
- **SGOV dividends (IBKR):** 30% withholding at source, **refunded in-account** Jan–Mar 2027 (you receive realized income, not a refund check)
- **Capital gains:** 0% withholding on appreciation (US does not tax capital gains for non-residents)

### Colombian Tax (Resident)
- **All foreign-source income:** Flat 28% (incluye intereses y dividendos)
  - Wallbit: $627 × 28% = $175.56
  - IBKR SGOV: $360 × 28% = $100.80
- **Foreign tax credit (Art. 254 ET):** You may offset US withholding paid against Colombian liability (if withholding occurs before refund; after refund, no credit is needed on the US side)

**Bottom line:** After-tax yield from both sources is **~$450/year** on the full $32,000.

---

## Cash Position After Execution

| Account | Balance | Purpose |
|---|---|---|
| Rippling | $0 | (emptied) |
| Payoneer | $0 | (emptied) |
| Wise | $1,000 | Emergency buffer |
| Wallbit | $22,000 | Income generation + daily spending |
| IBKR | $7,000 (after 5 × $2,000 purchases) | Growth + diversification, staged |
| eToro | $2,809.55 | Fallback liquidity |
| **Total deployed** | **$32,809.55** | |
| **Idle cash** | **$1,000** (Wise buffer) | |

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

1. **Approval:** Confirm you agree with the allocation and timing.
2. **Day 1:** Initiate Rippling → Payoneer transfer.
3. **Day 4:** Initiate Payoneer → Wise transfer (consolidation).
4. **Day 6:** Split Wise into two legs:
   - $22,000 → Wallbit (enable FDIC sweep)
   - $7,000 → IBKR ACH funding
5. **Day 10 onward:** Monthly SGOV purchases ($2,000 each, 5 months).
6. **Jan 2027:** Monitor IBKR for US withholding refund posting.

---

## Reference Documents
- Full analysis: `ai/finance/idle-cash-allocation-2026-08.md`
- Interactive plan: [Artifact HTML]
- Tax details: `ai/finance/` (as needed)

---

**Status:** Ready to execute · **Last reviewed:** 2026-08-27
