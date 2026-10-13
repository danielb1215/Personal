"""Finance review: computes every figure shown on the dashboard from the finances_unified ledger."""
import json, re, sys
import pandas as pd, numpy as np

W = sys.argv[1]  # work folder: reads W/ledger.json (Transactions!A1:T from get_values), writes W/data.json
raw = json.load(open(f'{W}/ledger.json'))['values']
h = raw[0]
df = pd.DataFrame([r + [''] * (len(h) - len(r)) for r in raw[1:]], columns=h)
df['usd'] = pd.to_numeric(df.amount_usd, errors='coerce')
df['amt'] = pd.to_numeric(df.amount, errors='coerce')
df = df[df.is_duplicate != 'yes']

# ---------- fixed inputs (sources listed in the dashboard) ----------
TODAY = '2026-10-13'
CPI_CO = 0.0629          # DANE, Sep 2026 annual
CPI_US = 0.034           # BLS, Aug 2026 annual (Sep due 2026-10-14)
TRM_NOW, TRM_YAGO = 3194.44, 3913.24   # TRM 2026-10-13 and 2025-10-13 (-18.37%)
BAL = {  # Balances tab (Sheet), eToro from 2026-08-27 snapshot (connector needs re-auth)
    'Rippling wallet': (21103.63, '2026-10-01', 0.0),
    'Payoneer USD': (11426.50, '2026-10-09', 0.0),
    'Payoneer EUR': (128.96, '2026-10-07', 0.0),
    'Wise USD': (3000.00, '2026-10-13', 0.0),
    'Wallbit USD': (1145.51, '2026-09-30', 0.0),
    'Bancolombia savings 6948': (227.58, '2026-10-13', 0.0),
    'eToro cash (uninvested)': (2809.55, '2026-08-27', 0.0),
}
ETORO_TOTAL, WALLBIT_INV = 13810.02, 100.0
CARD_OWED = 292.60  # Sep statement 907,035 COP; paid from 6948 on 2026-10-12 (row BC 2026-10-12 -292.60)

M12 = [str(p) for p in pd.period_range('2025-10', '2026-09', freq='M')]
M24 = [str(p) for p in pd.period_range('2024-10', '2026-09', freq='M')]
d12 = df[df.month.isin(M12)]

out = {}
# ---------- cash position ----------
cash = {k: v[0] for k, v in BAL.items()}
out['cash'] = {'accounts': [{'account': k, 'usd': v[0], 'as_of': v[1]} for k, v in BAL.items()],
               'total_cash': round(sum(cash.values()), 2),
               'card_owed_paid': CARD_OWED,
               'invested': round(ETORO_TOTAL - cash['eToro cash (uninvested)'] + WALLBIT_INV, 2)}
out['cash']['net_worth'] = round(out['cash']['total_cash'] + out['cash']['invested'], 2)

# ---------- income / outflows, 12 months ----------
inc = d12[d12.summary_group == 'Income'].usd.sum()
spend = -d12[d12.summary_group == 'Spending'].usd.sum()
payouts = -d12[d12.summary_group == 'Payouts'].usd.sum()
payins = d12[d12.summary_group == 'Payins'].usd.sum()
invest = -d12[d12.summary_group == 'Investments'].usd.sum()
outflow = spend + payouts - payins
out['flows12'] = {k: round(v, 2) for k, v in dict(income=inc, spending=spend, payouts=payouts, payins=payins,
                  net_outflow=outflow, saved=inc - outflow, invested=invest).items()}
out['flows12'].update(monthly_income=round(inc / 12, 2), monthly_outflow=round(outflow / 12, 2),
                      monthly_spending=round(spend / 12, 2), monthly_saved=round((inc - outflow) / 12, 2),
                      savings_rate=round((inc - outflow) / inc, 4))

# ---------- monthly series (24 m) ----------
d24 = df[df.month.isin(M24)]
ser = []
for m in M24:
    x = d24[d24.month == m]
    est_card = -x[(x.flow_type == 'card_payment') & x.match_account.str.contains('not in Drive')].usd.sum()
    ser.append(dict(month=m,
        spending=round(-x[x.summary_group == 'Spending'].usd.sum(), 0),
        card_est=round(est_card, 0),
        payouts_net=round(-x[x.summary_group == 'Payouts'].usd.sum() - x[x.summary_group == 'Payins'].usd.sum(), 0),
        income=round(x[x.summary_group == 'Income'].usd.sum(), 0)))
out['monthly24'] = ser

# ---------- categories (12 m) ----------
sp = d12[d12.summary_group == 'Spending']
cat = sp.pivot_table(index='category', columns='month', values='usd', aggfunc='sum').reindex(columns=M12).fillna(0) * -1
cats = []
for c, row in cat.iterrows():
    h1, h2 = row[M12[:6]].mean(), row[M12[6:]].mean()
    cats.append(dict(category=c, total=round(row.sum(), 0), avg=round(row.mean(), 0), median=round(row.median(), 0),
                     h1=round(h1, 0), h2=round(h2, 0), growth=round((h2 - h1) / h1, 3) if h1 > 0 else None,
                     months=[round(v, 0) for v in row.values]))
out['categories'] = sorted(cats, key=lambda c: -c['total'])
out['months12'] = M12

# ---------- recurring charges ----------
def norm(s):
    s = re.sub(r'\*.*$', '', s.upper()); s = re.sub(r'[^A-Z ]', ' ', s)
    s = re.sub(r'\b(PAGO|PROGRAMADO|PSE|SV|TRANSF A)\b', ' ', s); return ' '.join(s.split()[:2])
sp = sp.assign(key=sp.counterparty.map(norm))
rec = []
for k, g in sp.groupby('key'):
    by_m = g.groupby('month').usd.sum() * -1
    if by_m.size >= 4 and g.category.iloc[-1] not in ('Restaurants, cafés & bars', 'Groceries', 'Transport',
            'Fuel & car', 'Shopping (online)', 'Food delivery', 'Travel (flights & lodging)', 'Cycling & sport'):
        first, last = by_m.iloc[:2].mean(), by_m.iloc[-2:].mean()
        rec.append(dict(merchant=k.title(), category=g.category.iloc[-1], months=int(by_m.size),
                        avg=round(by_m.mean(), 2), first=round(first, 2), latest=round(by_m.iloc[-1], 2),
                        last_month=by_m.index[-1], change=round((last - first) / first, 3), annual=round(by_m.sum(), 0)))
sub = sp[sp.category == 'Subscriptions & software']
for k, g in sub.groupby('key'):
    if k not in [norm(r['merchant']) for r in rec] and not any(r['merchant'].upper() == k for r in rec):
        by_m = g.groupby('month').usd.sum() * -1
        rec.append(dict(merchant=k.title(), category='Subscriptions & software', months=int(by_m.size),
                        avg=round(by_m.mean(), 2), first=round(by_m.iloc[0], 2), latest=round(by_m.iloc[-1], 2),
                        last_month=by_m.index[-1], change=None, annual=round(by_m.sum(), 0)))
out['recurring'] = sorted(rec, key=lambda r: -r['annual'])

# ---------- unusual ----------
big = d12[(d12.summary_group.isin(['Spending', 'Payouts'])) & (d12.usd < -400)].sort_values('usd')
out['unusual'] = [dict(date=r.date, account=r.account, usd=round(-r.usd, 2), category=r.category,
                       counterparty=r.counterparty, review=r.needs_review) for r in big.itertuples()]
rev = d12[d12.needs_review != '']
out['needs_review'] = dict(rows=int(len(rev)), usd=round(-rev[rev.usd < 0].usd.sum(), 0))
p = d12[d12.summary_group == 'Payouts']
out['payouts_top'] = (p.groupby('counterparty').usd.agg(['sum', 'count']).sort_values('sum').head(8)
                      .reset_index().assign(sum=lambda x: -x['sum'].round(0)).to_dict('records'))

# ---------- idle cash history ----------
known = {'Rippling wallet': (21103.63, '2026-10-01'), 'Payoneer USD': (11426.5, '2026-10-09'),
         'Wallbit USD': (1145.51, '2026-09-30')}
hist = {}
for a, (bal, asof) in known.items():
    t = df[(df.account == a) & (df.date <= asof)]
    daily = t.groupby('date').amt.sum(); cum = daily.cumsum(); s = bal - cum.iloc[-1] + cum
    s.index = pd.to_datetime(s.index)
    hist[a] = s.reindex(pd.date_range('2024-10-01', TODAY)).ffill().fillna(bal - cum.iloc[-1])
H = pd.DataFrame(hist)
H['Wise USD'] = np.where(H.index >= '2025-11-17', 3000.0, 0.0)
floors = {}
for mths in (3, 6, 12):
    since = (pd.Timestamp(TODAY) - pd.DateOffset(months=mths))
    floors[mths] = {a: round(float(H.loc[since:, a].min()), 0) for a in H.columns}
out['idle_floors'] = floors
avg12 = H.loc[pd.Timestamp(TODAY) - pd.DateOffset(months=12):].mean()
out['avg_usd_cash_12m'] = round(float(avg12.sum()), 0)
me = H.resample('ME').last()
out['usd_cash_month_end'] = [dict(month=i.strftime('%Y-%m'), **{k: round(float(v), 0) for k, v in r.items()})
                             for i, r in me.iterrows()]

# ---------- inflation & opportunity cost ----------
idle = out['cash']['total_cash']
fx_chg = TRM_NOW / TRM_YAGO - 1
real_cop = (1 + fx_chg) / (1 + CPI_CO) - 1
out['inflation'] = dict(cpi_co=CPI_CO, cpi_us=CPI_US, idle=idle,
    cost_co_year=round(idle * CPI_CO, 0), cost_co_month=round(idle * CPI_CO / 12, 0),
    cost_us_year=round(idle * CPI_US, 0), fx_change_12m=round(fx_chg, 4), real_cop_change_12m=round(real_cop, 4),
    realized_loss_avg_balance=round(-real_cop * out['avg_usd_cash_12m'], 0))

# ---------- emergency fund ----------
ESS = ['Utilities (home)', 'Health & insurance', 'Phone & internet', 'Groceries', 'Transport', 'Fuel & car',
       'Taxes', 'Bills & online payments (PSE)', 'Bank fees & interest', 'Unknown (statement missing)']
ess = sum(c['avg'] for c in cats if c['category'] in ESS)
rec_payouts = -p[p.counterparty.str.contains('SCOTIABANK|NEQUI', regex=True)].usd.sum() / 12
mo = out['flows12']['monthly_outflow']
ef_target = round(6 * mo, 0)
liquid = idle  # all cash accounts are same-day/next-day liquid
out['emergency'] = dict(monthly_outflow=mo, essentials_monthly=round(ess + rec_payouts, 0),
    target_6m=ef_target, floor_3m_essentials=round(3 * (ess + rec_payouts), 0), liquid=liquid,
    excess=round(liquid - ef_target, 0), operating_buffer=round(mo, 0))

# ---------- yields: annual earnings on the excess ----------
ex = out['emergency']['excess']; efund = ef_target - mo
opts = [  # name, low, high (annual %, nominal)
    ('US T-bill ETF / USD money-market (e.g. on eToro)', 3.6, 3.75),
    ('eToro interest on cash (tier-dependent)', 0.5, 3.0),
    ('COP high-yield savings (Nu Cajitas, neobanks)', 9.25, 10.5),
    ('COP liquidity FIC (e.g. Fiducuenta)', 8.75, 9.5),
    ('COP CDT 360 days (Pibank, Pichincha)', 13.0, 13.49),
]
out['options_on_excess'] = [dict(option=n, lo=lo, hi=hi, yr_lo=round(ex * lo / 100, 0), yr_hi=round(ex * hi / 100, 0),
                                 real_vs_cpi_co=round(((1 + lo / 100) / (1 + CPI_CO) - 1) * 100, 2)) for n, lo, hi in opts]
out['ef_yield'] = dict(amount=efund, usd_mmf=round(efund * 0.036, 0), cop_hysa=round(efund * 0.0925, 0))

# ---------- goals ----------
fi_target = round(mo * 12 / 0.04, 0)
out['goals'] = dict(
    emergency=dict(target=ef_target, have=liquid, pct=round(liquid / ef_target, 3)),
    side_capital=dict(target_lo=5000, target_hi=10000, earmarked=0, available_excess=ex),
    mrr=dict(target_lo=2000, target_hi=3000, have=60.0 / 12),
    invest=dict(saved_12m=out['flows12']['saved'], invested_12m=invest, pct=round(invest / out['flows12']['saved'], 4)),
    fi=dict(target=fi_target, invested=out['cash']['invested'], net_worth=out['cash']['net_worth'],
            pct_invested=round(out['cash']['invested'] / fi_target, 4)))

# ---------- conversions: USD->COP volume ----------
conv = df[(df.account == 'Bancolombia savings 6948') & (df.flow_type == 'internal_transfer') & (df.amt > 0) & df.month.isin(M12)]
conv_usd = conv.amt.sum() / pd.to_numeric(conv.fx_note.str.extract(r'([\d,]+) \(')[0].str.replace(',', ''), errors='coerce').mean()
out['fx_conv'] = dict(usd_12m=round(conv.usd.sum(), 0), monthly=round(conv.usd.sum() / 12, 0),
                      spread_checks=[dict(date='2026-08-20', got=3027.91, trm=3053.48), dict(date='2026-09-08', got=3076.54, trm=3126.08)])
for s in out['fx_conv']['spread_checks']: s['spread'] = round(1 - s['got'] / s['trm'], 4)

# ---------- eToro concentration (2026-08-27 snapshot) ----------
pos = {'NVDA': 2903.42, 'GOOG': 2279.91, 'QQQ': 1705.58, 'AAPL': 1594.61, 'VOO': 1592.51, 'AMZN': 368.86, 'TSLA': 355.58, 'Copy: AI agent': 200}
single = sum(v for k, v in pos.items() if k not in ('QQQ', 'VOO', 'Copy: AI agent'))
out['etoro'] = dict(positions=pos, single_stock_pct=round(single / sum(pos.values()), 3), as_of='2026-08-27')

json.dump(out, open(f'{W}/data.json', 'w'), indent=1, default=float)
print(json.dumps({k: out[k] for k in ['cash', 'flows12', 'inflation', 'emergency', 'goals', 'idle_floors', 'avg_usd_cash_12m', 'fx_conv', 'etoro', 'needs_review', 'ef_yield']}, indent=1, default=float))
print(json.dumps(out['options_on_excess'], indent=1))
for c in out['categories']: print(f"{c['category']:32s} tot {c['total']:7.0f} avg {c['avg']:5.0f} med {c['median']:5.0f} h1 {c['h1']:5.0f} h2 {c['h2']:5.0f} g {c['growth']}")
for r in out['recurring']: print(r)
print(out['payouts_top'])

# ---------- years to financial-independence number, two paths ----------
def years_to(target, start, yearly, real):
    v, n = start, 0
    while v < target and n < 80:
        v = v * (1 + real) + yearly; n += 1
    return n if v >= target else None
fi = out['goals']['fi']; yearly = out['flows12']['saved']
cash_real = (1 / (1 + CPI_US)) - 1
fi['years_invested_5real'] = years_to(fi['target'], fi['net_worth'], yearly, 0.05)
fi['years_cash'] = years_to(fi['target'], fi['net_worth'], yearly, cash_real)
fi['cash_ceiling'] = round(yearly / -cash_real, 0)
out['payoneer_floor_loss'] = round(floors[12]['Payoneer USD'] * -real_cop, 0)
json.dump(out, open(f'{W}/data.json', 'w'), indent=1, default=float)
print(fi, out['payoneer_floor_loss'])
