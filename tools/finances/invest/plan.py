"""Investment plan for excess savings (Oct 2026): buckets, sample allocations, projections, FI years.

Recommendations only. Every input is dated below; update them and re-run:
    python3 plan.py [out.json]
Prints the tables shown in the report and writes the figures to out.json (default: plan.json).
"""
import json, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else 'plan.json'

# ---------- position (finance review, 2026-10-13; eToro snapshot 2026-08-27, connector needs re-auth) ----------
CASH = {'Rippling wallet': 21103.63, 'Payoneer USD': 11426.50, 'Payoneer EUR': 128.96, 'Wise USD': 3000.00, 'Wallbit USD': 1145.51,
        'eToro cash (uninvested)': 2809.55, 'Bancolombia savings': 227.58}
MONTHLY_OUTFLOW = 3214.33          # spending $2,406 + net payouts, 12-month average
MONTHLY_SAVING = 1800.0            # review: ~$1,795/month
INCOME_YEAR = 2307.69 * 26         # Rippling, biweekly
HOLDINGS = {'NVDA': 2903.42, 'GOOG': 2279.91, 'QQQ': 1705.58, 'AAPL': 1594.61, 'VOO': 1592.51,
            'AMZN': 368.86, 'TSLA': 355.58, 'Copy-trade': 200.00}
SINGLE = ['NVDA', 'GOOG', 'AAPL', 'AMZN', 'TSLA']
WALLBIT_INVESTED = 100.0
FI_TARGET = 964_000                # 25x current annual outflow (4% rule), today's dollars

# ---------- market inputs (dated; sources in the report) ----------
TRM = 3194.44                      # COP/USD, 2026-10-13
UVT = 52_374                       # COP, tax year 2026 (DIAN Res. 000238, 2025-12-15)
CDT_360 = 0.1325                   # 1-year CDT, top issuers 13.0-13.49% EA (SFC cut 2026-10-01)
CAJITA = 0.0925                    # Nu Cajitas, last confirmed rate (2026-04-09)
CO_CPI = 0.0629                    # DANE, Sep 2026
TBILL_NOW = 0.0373                 # SGOV 30-day SEC yield, 2026-10-12
TBILL_LR = 0.0325                  # assumed 20-year average for short USD Treasuries
EQ_NOM = 0.065                     # assumed global equity nominal return (VCMM-style range 4-7%)
EQ_LOW, EQ_HIGH = 0.045, 0.085     # sensitivity band
US_INFL = 0.025                    # long-run US inflation assumption for real figures
GLOBAL_DIV_YIELD = 0.018           # approx. VWRA/VT dividend yield
US_SHARE = 0.62                    # US weight in a global index
TER_UCITS = 0.0022                 # VWRA (0.19-0.22% depending on source); conservative
CO_MARGINAL = 0.28                 # Art. 241 ET bracket 1,700-4,100 UVT (computed below)
GO_RATE = 0.15                     # ganancia ocasional on assets held >= 2 years (confirm with contador)
FPV_FEE = 0.018                    # typical FPV admin fee (third-party comparison, verify per fund)

# ---------- 1. buckets ----------
total_cash = sum(CASH.values())
ops = MONTHLY_OUTFLOW
ef_6m = 6 * MONTHLY_OUTFLOW
ef = ef_6m - ops
excess = total_cash - ef_6m
invested_now = sum(HOLDINGS.values()) + WALLBIT_INVESTED

# ---------- 2. after-tax expected returns per vehicle (nominal, in its own currency) ----------
tbill_after_tax = TBILL_LR * (1 - CO_MARGINAL)          # interest = ordinary income in Colombia
eq_drag = TER_UCITS + GLOBAL_DIV_YIELD * US_SHARE * 0.15  # Irish fund: 15% US withholding inside the fund
us_etf_drag = 0.0003 + GLOBAL_DIV_YIELD * 0.30          # US ETF (VT) for a non-treaty resident: 30% withheld
                                                         # (Colombian tax on the dividend, net of credit, ignored)
def eq_net(nom): return nom - eq_drag

vehicles = {
    'SGOV / BIL / IB01 (USD T-bills)': dict(gross=TBILL_NOW, after_tax=TBILL_NOW * (1 - CO_MARGINAL), ccy='USD'),
    'CDT 1-year (COP)': dict(gross=CDT_360, after_tax=CDT_360 * (1 - CO_MARGINAL), ccy='COP'),
    'Nu Cajita (COP)': dict(gross=CAJITA, after_tax=CAJITA * (1 - CO_MARGINAL), ccy='COP'),
    'VWRA / global UCITS acc.': dict(gross=EQ_NOM, after_tax=eq_net(EQ_NOM), ccy='USD'),
    'VT / VOO (US-domiciled)': dict(gross=EQ_NOM, after_tax=EQ_NOM - us_etf_drag, ccy='USD'),
}

# COP CDT in USD terms under FX moves (positive = COP weakens, USD buys more COP)
fx_cases = {f'COP {"weakens" if m > 0 else "strengthens" if m < 0 else "flat"} {abs(m):.0%}':
            round((1 + CDT_360 * (1 - CO_MARGINAL)) / (1 + m) - 1, 4) for m in (-0.10, 0.0, 0.10)}
breakeven_fx = (1 + CDT_360 * (1 - CO_MARGINAL)) / (1 + TBILL_NOW * (1 - CO_MARGINAL)) - 1

# ---------- 3. Colombian income tax and the FPV/AFC deduction (Art. 241, 206-10, 126-1, 336 ET) ----------
def tax_uvt(taxable):
    t = [(1090, 0), (1700, .19), (4100, .28), (8670, .33), (18970, .35), (31000, .37), (1e12, .39)]
    tax, lo = 0.0, 0
    for hi, r in t:
        if taxable > lo:
            tax += (min(taxable, hi) - lo) * r
        lo = hi
    return tax

income_uvt = INCOME_YEAR * TRM / UVT
ss = 0.40 * (0.125 + 0.16)          # independent: health 12.5% + pension 16% on 40% of income (INCR)
net_uvt = income_uvt * (1 - ss)
cap = min(0.40 * net_uvt, 1340)     # all exempt income + deductions together

def tax_with_fpv(fpv_uvt):
    fpv = min(fpv_uvt, 0.30 * income_uvt, 3800)
    labor = min(0.25 * (net_uvt - fpv), 790)
    exempt = min(fpv + labor, cap)
    return tax_uvt(net_uvt - exempt)

base_tax = tax_with_fpv(0)
fpv_rows = []
for usd in (0, 2500, 5000, 7500, 10000, 12500, 15000):
    u = usd * TRM / UVT
    saved = (base_tax - tax_with_fpv(u)) * UVT / TRM
    fpv_rows.append(dict(fpv_usd=usd, tax_saved_usd=round(saved), rate=round(saved / usd, 3) if usd else None))
# largest contribution that still earns full marginal-rate savings per extra dollar
best = max((r for r in fpv_rows if r['fpv_usd']), key=lambda r: r['tax_saved_usd'])
efficient = [r for r in fpv_rows if r['fpv_usd'] and r['rate'] >= 0.20]
fpv_sweet = efficient[-1] if efficient else best
tax_info = dict(income_uvt=round(income_uvt), net_uvt=round(net_uvt), cap_uvt=round(cap),
                base_tax_usd=round(base_tax * UVT / TRM), fpv=fpv_rows, sweet_spot=fpv_sweet,
                gmf_exempt_cop=350 * UVT, gmf_exempt_usd=round(350 * UVT / TRM),
                estate_threshold=60_000)

# ---------- 4. sample allocations ----------
EF_SPLIT = dict(cop_cajita=3000, cop_cdt_ladder=5000)        # COP half: instant + 3/6/12-month CDTs
EF_SPLIT['usd_tbill'] = round(ef - sum(EF_SPLIT.values()))   # USD half: Wallbit yield / SGOV / IB01

ALLOC = {
    'Conservative': dict(business=10000, lt_equity=0.50, monthly_equity=0.50),
    'Balanced':     dict(business=7500,  lt_equity=0.80, monthly_equity=0.80),
    'Growth':       dict(business=5000,  lt_equity=1.00, monthly_equity=1.00),
}

def blended(eq_share, eq_nom=EQ_NOM):
    return eq_share * eq_net(eq_nom) + (1 - eq_share) * tbill_after_tax

def real(r): return (1 + r) / (1 + US_INFL) - 1

def fv_monthly(pmt, r_annual, years):
    r = (1 + r_annual) ** (1 / 12) - 1
    n = years * 12
    return pmt * ((1 + r) ** n - 1) / r

def years_to_fi(start_existing, start_new, pmt, r_new_real, r_eq_real, target=FI_TARGET, cap_years=80):
    a, b = start_existing, start_new
    re, rn = (1 + r_eq_real) ** (1 / 12) - 1, (1 + r_new_real) ** (1 / 12) - 1
    for m in range(1, cap_years * 12 + 1):
        a *= 1 + re
        b = b * (1 + rn) + pmt
        if a + b >= target:
            return round(m / 12, 1)
    return None

def months_to_dilute(eq_today, monthly_eq, target_share):
    single = sum(HOLDINGS[s] for s in SINGLE)
    pot = sum(HOLDINGS.values()) + eq_today
    m = 0
    while single / pot > target_share and m < 600:
        pot += monthly_eq
        m += 1
    return m

allocs = {}
for name, a in ALLOC.items():
    lt = excess - a['business']
    eq_today = lt * a['lt_equity']
    r = blended(a['monthly_equity'])
    rr = real(r)
    proj = {}
    for y in (10, 20):
        proj[y] = dict(contrib=round(MONTHLY_SAVING * 12 * y),
                       nominal=round(fv_monthly(MONTHLY_SAVING, r, y)),
                       real=round(fv_monthly(MONTHLY_SAVING, rr, y)))
    eq_real = real(eq_net(EQ_NOM))
    fi = years_to_fi(invested_now, lt, MONTHLY_SAVING, rr, eq_real)
    sens = {}
    for label, e in (('low', EQ_LOW), ('high', EQ_HIGH)):
        sens[label] = years_to_fi(invested_now, lt, MONTHLY_SAVING, real(blended(a['monthly_equity'], e)),
                                  real(eq_net(e)))
    fi_plus1k = years_to_fi(invested_now, lt, MONTHLY_SAVING + 1000, rr, eq_real)
    fi_mrr = {k: years_to_fi(invested_now, lt, MONTHLY_SAVING + k, rr, eq_real) for k in (2000, 3000)}  # side-business MRR saved
    fi_per_2500 = round(years_to_fi(invested_now, lt - 2500, MONTHLY_SAVING, rr, eq_real) - fi, 1)  # +$2.5k to business
    fi_idle = years_to_fi(invested_now, 0, MONTHLY_SAVING, real(0.0), eq_real)  # status quo: savings sit at 0%
    single_now = sum(HOLDINGS[s] for s in SINGLE) / sum(HOLDINGS.values())
    allocs[name] = dict(
        today=dict(emergency=round(ef), business=a['business'], long_term=round(lt),
                   lt_equity=round(eq_today), lt_tbills=round(lt - eq_today)),
        monthly=dict(equity=round(MONTHLY_SAVING * a['monthly_equity']),
                     tbills=round(MONTHLY_SAVING * (1 - a['monthly_equity']))),
        exp_return_nominal=round(r, 4), exp_return_real=round(rr, 4),
        projection=proj, fi_years=fi, fi_years_low=sens['low'], fi_years_high=sens['high'],
        fi_years_plus1k=fi_plus1k, fi_years_idle=fi_idle, fi_years_mrr=fi_mrr, fi_cost_of_2500_business=fi_per_2500,
        single_share_now=round(single_now, 3),
        months_to_30pct=months_to_dilute(eq_today, MONTHLY_SAVING * a['monthly_equity'], 0.30),
        months_to_20pct=months_to_dilute(eq_today, MONTHLY_SAVING * a['monthly_equity'], 0.20),
    )

# ---------- 5. FPV vs taxable ETF, same $ per year, equity inside both ----------
def fpv_vs_etf(per_year, years):
    saved = next((r['tax_saved_usd'] for r in fpv_rows if r['fpv_usd'] == per_year), None)
    r_fpv = EQ_NOM - FPV_FEE
    r_etf = eq_net(EQ_NOM)
    fpv = sum(per_year * (1 + r_fpv) ** (years - i - 0.5) for i in range(years))
    refund = sum(saved * (1 + r_etf) ** (years - i - 1.5) for i in range(years - 1)) if saved else 0
    etf = sum(per_year * (1 + r_etf) ** (years - i - 0.5) for i in range(years))
    etf_after = etf - (etf - per_year * years) * GO_RATE
    return dict(fpv_balance=round(fpv), refunds_invested=round(refund), fpv_total=round(fpv + refund),
                etf_after_cgt=round(etf_after), advantage=round(fpv + refund - etf_after))

fpv_cmp = {y: fpv_vs_etf(fpv_sweet['fpv_usd'], y) for y in (10, 20)}

out = dict(as_of='2026-10-14', cash=dict(total=round(total_cash, 2), ops=round(ops), ef=round(ef),
           ef_6m=round(ef_6m), excess=round(excess), invested=round(invested_now)),
           ef_split=EF_SPLIT, vehicles=vehicles, cdt_usd_fx=fx_cases, cdt_breakeven_cop_weakening=round(breakeven_fx, 4),
           tax=tax_info, allocations=allocs, fpv_vs_etf=fpv_cmp,
           assumptions=dict(eq_nom=EQ_NOM, eq_low=EQ_LOW, eq_high=EQ_HIGH, eq_drag=round(eq_drag, 4),
                            us_etf_drag=round(us_etf_drag, 4), tbill_lr=TBILL_LR,
                            tbill_after_tax=round(tbill_after_tax, 4), us_infl=US_INFL, co_marginal=CO_MARGINAL,
                            fpv_fee=FPV_FEE, fi_target=FI_TARGET, monthly=MONTHLY_SAVING))
json.dump(out, open(OUT, 'w'), indent=1, default=str)

# ---------- print ----------
print(f"Cash ${total_cash:,.0f} | ops ${ops:,.0f} | EF ${ef:,.0f} | excess ${excess:,.0f} | invested ${invested_now:,.0f}")
print('EF split', EF_SPLIT)
for k, v in vehicles.items():
    print(f"  {k:34s} gross {v['gross']:.2%}  after-tax {v['after_tax']:.2%} {v['ccy']}")
print('CDT in USD terms', fx_cases, f'| breakeven COP weakening {breakeven_fx:.1%}')
print(f"Tax: income {income_uvt:,.0f} UVT, net {net_uvt:,.0f}, cap {cap:,.0f}, base tax ${base_tax*UVT/TRM:,.0f}")
for r in fpv_rows:
    print('  FPV', r)
print('FPV sweet spot', fpv_sweet, '| FPV vs ETF', fpv_cmp)
for n, a in allocs.items():
    print(f"\n{n}: today {a['today']} monthly {a['monthly']} r_nom {a['exp_return_nominal']:.2%} r_real {a['exp_return_real']:.2%}")
    print(f"  10y {a['projection'][10]}  20y {a['projection'][20]}")
    print(f"  FI years {a['fi_years']} (eq {EQ_LOW:.1%}: {a['fi_years_low']}, eq {EQ_HIGH:.1%}: {a['fi_years_high']}),"
          f" +$1k/mo: {a['fi_years_plus1k']}, MRR saved {a['fi_years_mrr']}, +$2.5k to business costs {a['fi_cost_of_2500_business']}y,"
          f" if savings stay at 0%: {a['fi_years_idle'] or 'not within 80 years'}")
    print(f"  single stocks {a['single_share_now']:.0%} -> <30% in {a['months_to_30pct']} mo, <20% in {a['months_to_20pct']} mo")
