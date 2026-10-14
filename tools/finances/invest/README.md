# Investment plan for excess savings (Oct 2026)

Script behind the report https://claude.ai/artifact/KQY5fkoP6KcP2GwYmo5sT1.
Recommendations only: it reads no account and changes nothing.

    python3 plan.py [out.json]

Computes, from the dated inputs at the top of the file:
- the three buckets (operating cash, emergency fund, excess) from the Oct 2026 finance review;
- after-tax expected returns per vehicle and a COP CDT's return in USD under FX moves;
- Colombian income tax (Art. 241 ET) with and without voluntary pension (FPV/AFC) contributions,
  applying the 25% labor exemption (790 UVT) and the 40% / 1,340 UVT overall cap;
- three sample allocations (conservative, balanced, growth): 10- and 20-year value of the
  $1,800/month, years to the $964k FI target, sensitivity to equity returns, and how many months
  of new money it takes to dilute single stocks below 30% and 20% of the eToro portfolio;
- FPV vs a taxable UCITS ETF for the same yearly amount.

Update balances, rates, UVT and TRM before re-running. Tax figures are estimates to check with a contador.
