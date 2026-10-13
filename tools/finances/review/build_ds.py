"""Turns data.json (from analyze.py) plus dated market inputs into the dashboard's dataset files."""
import json, sys
W = sys.argv[1]
D = json.load(open(f'{W}/data.json'))
r = lambda x, n=0: round(float(x), n) if n else int(round(float(x)))
f, inf, ef, g = D['flows12'], D['inflation'], D['emergency'], D['goals']
fl = D['idle_floors']
spread = sum(s['spread'] for s in D['fx_conv']['spread_checks']) / 2
cats = {c['category']: c for c in D['categories']}
by = lambda name: cats[name]

def K(metric, value, label, how):
    return dict(metric=metric, value=value, label=label, how=how)
L = 'Oct 2025 – Sep 2026'
kpis = [
 K('cash_total', r(D['cash']['total_cash']), 'Cash across all accounts (USD)', 'Sum of Balances tab cash rows (Rippling, Payoneer USD/EUR, Wise, Wallbit, Bancolombia) + eToro uninvested cash from the 2026-08-27 snapshot'),
 K('cash_excl_etoro', r(D['cash']['total_cash'] - 2809.55), 'Cash outside eToro (USD)', 'Balances tab, Cash total'),
 K('etoro_cash', r(2809.55), 'eToro uninvested cash (USD)', 'eToro snapshot 2026-08-27 in ai/persona/finances.md (connector needs sign-in)'),
 K('invested', r(D['cash']['invested']), 'Invested (USD)', 'eToro positions ($13,810.02 total − $2,809.55 cash) + Wallbit investing $100'),
 K('net_worth', r(D['cash']['net_worth']), 'Net worth (USD)', 'Cash + invested. September card bill ($292.60) already paid from Bancolombia on 2026-10-12'),
 K('idle_cash', r(inf['idle']), 'Cash earning ~0%', 'Every cash account: Bancolombia paid 369 COP (≈$0.12) interest in 12 months; Rippling, Payoneer, Wise, Wallbit pay none'),
 K('rippling', r(21103.63), 'Rippling wallet (USD)', 'Balances tab, as of 2026-10-01'),
 K('rippling_floor_3m', r(fl['3']['Rippling wallet']), 'Rippling: never below, last 3 months', 'Lowest daily balance since 2026-07-13, rebuilt from the Transactions ledger'),
 K('payoneer_floor_12m', r(fl['12']['Payoneer USD']), 'Payoneer: never below, last 12 months', 'Lowest daily balance since 2025-10-13, rebuilt from the Transactions ledger'),
 K('payoneer_floor_6m', r(fl['6']['Payoneer USD']), 'Payoneer: never below, last 6 months', 'Lowest daily balance since 2026-04-13'),
 K('wise_months', 11, 'Months Wise $3,000 has sat', 'Rippling → Wise $3,000 on 2025-11-17; balance confirmed $3,000 on 2026-10-13'),
 K('cpi_co', 6.29, 'Colombia inflation, Sep 2026 (%)', 'DANE IPC, 12 months to Sep 2026'),
 K('cpi_us', 3.4, 'US inflation, Aug 2026 (%)', 'BLS CPI-U, 12 months to Aug 2026 (Sep release due 2026-10-14)'),
 K('banrep', 12.25, 'BanRep policy rate (%)', 'Banco de la República, 2026-09-30 decision'),
 K('trm_now', 3194.44, 'TRM 2026-10-13 (COP per USD)', 'Superfinanciera TRM via dolar-colombia.com'),
 K('trm_yago', 3913.24, 'TRM 2025-10-13 (COP per USD)', 'TRM today + 718.80 year-on-year drop reported for the same date'),
 K('fx_change', r(inf['fx_change_12m'] * 100, 1), 'COP per USD, change in 12 months (%)', 'TRM now ÷ TRM a year ago − 1'),
 K('real_cop_change', r(inf['real_cop_change_12m'] * 100, 1), 'Bogotá buying power of $1 held 12 months (%)', '(1 + FX change) ÷ (1 + 6.29%) − 1'),
 K('infl_cost_yr', r(inf['cost_co_year']), 'Yearly loss to Colombian inflation (USD)', 'Idle cash × 6.29%, at today\'s exchange rate'),
 K('infl_cost_mo', r(inf['cost_co_month']), 'Monthly loss to Colombian inflation (USD)', 'Idle cash × 6.29% ÷ 12'),
 K('infl_cost_us_yr', r(inf['cost_us_year']), 'Yearly loss to US inflation (USD)', 'Idle cash × 3.4%: the loss measured in dollars'),
 K('payoneer_floor_loss', r(D['payoneer_floor_loss']), 'Bogotá buying power lost by Payoneer\'s untouched $8,151 (USD)', 'Payoneer 12-month floor × 23.2%'),
 K('income_12m', r(f['income']), f'Income, {L}', 'Transactions with summary_group = Income (26 Crowd Cow payrolls of $2,307.69 + $60 Retail AWare)'),
 K('income_mo', r(f['monthly_income']), 'Average monthly income', 'Income ÷ 12'),
 K('spending_12m', r(f['spending']), f'Spending, {L}', 'summary_group = Spending (spending, fees, refunds); excludes duplicates and moves between own accounts'),
 K('spending_mo', r(f['monthly_spending']), 'Average monthly spending', 'Spending ÷ 12'),
 K('payouts_net_12m', r(f['payouts'] - f['payins']), f'Net payouts to people, {L}', 'Payouts $10,802 − payins $1,105'),
 K('outflow_mo', r(f['monthly_outflow']), 'Average monthly outflow', '(Spending + payouts − payins) ÷ 12'),
 K('saved_12m', r(f['saved']), f'Saved, {L}', 'Income − spending − net payouts'),
 K('saved_mo', r(f['monthly_saved']), 'Average saved per month', 'Saved ÷ 12'),
 K('savings_rate', r(f['savings_rate'] * 100, 1), 'Savings rate (%)', 'Saved ÷ income'),
 K('invested_12m', r(f['invested']), f'New investments, {L}', 'investment_contribution rows: Wallbit investing $100 + Fiduciaria Popular $21.70'),
 K('invested_pct', r(g['invest']['pct'] * 100, 1), 'Share of savings invested (%)', 'New investments ÷ saved'),
 K('ef_target', r(ef['target_6m']), 'Emergency fund, 6 months of outflow', '6 × average monthly outflow'),
 K('ef_floor', r(ef['floor_3m_essentials']), 'Bare minimum, 3 months of essentials', '3 × (utilities, health, phone, groceries, transport, fuel, taxes, bills, bank fees + Scotiabank/Nequi payouts)'),
 K('ef_pct', r(g['emergency']['pct'] * 100), 'Emergency fund funded (%)', 'Cash ÷ 6-month target'),
 K('excess', r(ef['excess']), 'Cash above the 6-month fund', 'Cash − 6-month target'),
 K('ef_invest_part', r(ef['target_6m'] - ef['monthly_outflow']), 'Emergency fund beyond 1 month of operating cash', '6-month target − 1 month kept in everyday accounts'),
 K('fi_target', r(g['fi']['target']), 'Financial-independence number', 'Monthly outflow × 12 ÷ 4% withdrawal rate'),
 K('fi_pct', r(g['fi']['pct_invested'] * 100, 1), 'Of FI number invested (%)', 'Invested ÷ FI number'),
 K('fi_years', g['fi']['years_invested_5real'], 'Years to FI if savings are invested', 'Net worth today + $21.5k a year, growing 5% a year after inflation'),
 K('fi_cash_ceiling', r(g['fi']['cash_ceiling']), 'Most you can ever reach saving in cash', 'At 0% interest and 3.4% US inflation, $21.5k a year levels off at $21.5k ÷ 3.29%'),
 K('single_stock', r(D['etoro']['single_stock_pct'] * 100), 'eToro in single stocks (%)', 'NVDA, GOOG, AAPL, AMZN, TSLA ÷ all eToro positions (2026-08-27)'),
 K('fx_spread', r(spread * 100, 1), 'Wallbit rate below TRM (%)', 'Average of 2 checks: 2026-08-20 (0.84%) and 2026-09-08 (1.58%)'),
 K('fx_conv_mo', r(D['fx_conv']['monthly']), 'USD converted to COP per month', 'USD legs of Payoneer/Wallbit → Bancolombia transfers ÷ 12'),
 K('fx_cost_yr', r(D['fx_conv']['usd_12m'] * spread), 'Yearly cost of that spread (USD)', 'USD converted in 12 months × average spread'),
 K('review_rows', D['needs_review']['rows'], 'Rows flagged for review', 'Transactions with needs_review set, last 12 months'),
 K('review_usd', r(D['needs_review']['usd']), 'Money in flagged rows (USD)', 'Sum of outgoing flagged rows'),
]
km = {k['metric']: k['value'] for k in kpis}

accounts = []
yields = {'Rippling wallet': 'Payroll wallet, no interest', 'Payoneer USD': 'No interest', 'Payoneer EUR': 'No interest',
          'Wise USD': 'No interest for Colombia residents', 'Wallbit USD': 'No interest on cash',
          'Bancolombia savings 6948': '369 COP interest in 12 months', 'eToro cash (uninvested)': '0–1% depending on Club tier'}
for a in D['cash']['accounts']:
    n = a['account']; key = {'Wise USD': 'Wise USD'}.get(n, n)
    accounts.append(dict(account=n, usd=r(a['usd']), as_of=a['as_of'], interest=yields[n],
        floor_3m=r(fl['3'].get(n, 0)) if n in fl['3'] else None, floor_12m=r(fl['12'].get(n, 0)) if n in fl['12'] else None))

hist = []
for row in D['usd_cash_month_end']:
    for acct in ('Rippling wallet', 'Payoneer USD', 'Wise USD', 'Wallbit USD'):
        hist.append(dict(month=row['month'], account=acct, usd=max(0, r(row[acct]))))

monthly = [dict(month=m['month'], spending=r(m['spending']), card_estimate=r(m['card_est']),
                payouts_net=r(m['payouts_net']), income=r(m['income'])) for m in D['monthly24']]

catrows = []
for c in D['categories']:
    row = dict(category=c['category'], total_12m=r(c['total']), avg_month=r(c['avg']), oct_mar=r(c['h1']), apr_sep=r(c['h2']),
               change=None if c['growth'] is None else r(c['growth'] * 100))
    for m, v in zip(D['months12'], c['months']): row[m] = r(v)
    catrows.append(row)

flags = {'Apple Com': 'Up from $15.76 to $67.96 a month', 'Compensar Oi': 'Social-security contribution; follows declared income',
         'Colmedica Med': 'Prepaid health plan, up 36% in a year', 'Open Inc': 'Unidentified $8/month since at least Oct 2025',
         'Gopro Com': 'New in Sep 2026', 'Brave': 'Trial turned paid (Aug)', 'Brave Com': 'Billed again in Sep',
         'Openai': 'Stopped Feb 2026 (replaced by Claude)', 'Amazon Prime': 'Stopped Feb 2026', 'Movistar Pagosepayco': 'Internet or second line? Both Movistar and Claro are paid monthly',
         'Comcel S': 'Claro mobile', 'Intereses Corrientes': 'Card interest: a statement was not paid in full', 'Gigsky Inc': 'Travel eSIM'}
recurring = [dict(merchant=x['merchant'], category=x['category'], months_billed=x['months'], first=r(x['first'], 2),
                  latest=r(x['latest'], 2), last_month=x['last_month'], annual=r(x['annual']), note=flags.get(x['merchant'], ''))
             for x in D['recurring'] if x['annual'] >= 10]

unusual = [dict(date=u['date'], counterparty=u['counterparty'], category=u['category'], account=u['account'], usd=r(u['usd']),
                note=u['review'] or '') for u in D['unusual']]
notes_u = {'aliexpress': 'Three charges on 2025-11-19 total $2,502', 'MISSING STATEMENT': 'June 2026 card statement not in Drive'}
for u in unusual:
    for k, v in notes_u.items():
        if k.lower() in u['counterparty'].lower() and not u['note']: u['note'] = v

ex = km['excess']
O = lambda option, cur, lo, hi, liquidity, risk, notes, source: dict(option=option, currency=cur, yield_lo=lo, yield_hi=hi,
        usd_yr_lo=r(ex * lo / 100), usd_yr_hi=r(ex * hi / 100), real_vs_cpi_co=r(((1 + lo / 100) / 1.0629 - 1) * 100, 1),
        liquidity=liquidity, risk=risk, notes=notes, source=source)
options = [
 O('Leave it where it is', 'USD', 0, 0, 'Same day', 'None on paper; loses 3.4% a year to US inflation and moves with the peso', 'What happens today', 'Balances tab'),
 O('eToro interest on uninvested cash', 'USD', 0.5, 3.0, 'Same day', 'Very low; broker, not a bank deposit', 'Rate depends on Club tier (equity $10k / $25k / $50k). Moving more cash in raises the tier. Confirm the live table in the app', 'etoro.com/investing/interest-on-balance'),
 O('US T-bill ETF on eToro (e.g. SGOV, BIL)', 'USD', 3.6, 3.75, '1–2 days to sell', 'Very low credit risk; price barely moves', 'Keeps dollars. No US–Colombia tax treaty: distributions may face 30% US withholding unless the broker applies the interest exemption. Check your eToro statement', '3-month T-bill 3.75%, Treasury MMF 7-day yield ~3.3% (Aug 2026)'),
 O('COP liquidity fund (FIC, e.g. Fiducuenta)', 'COP', 8.75, 9.5, '1 business day', 'Low; not covered by Fogafín', 'Converts to pesos. Interest taxable; 4×1000 on withdrawals unless the account is your exempt one', 'Bancolombia Fiducuenta 8.75% EA, 365-day, 2026-08-30'),
 O('COP high-yield savings (Nu Cajitas, neobanks)', 'COP', 9.25, 10.5, 'Same day', 'Low; Fogafín covers COP 50M per bank', 'Converts to pesos. Nu was 9.25% EA after April; BanRep has hiked since, so check today\'s rate', 'Nu Colombia, Apr 2026'),
 O('COP CDT, 360 days (Pibank, Pichincha)', 'COP', 13.0, 13.49, 'Locked 12 months', 'Low credit risk; Fogafín covers COP 50M per bank', 'Highest yield, no access for a year. 4% withholding on interest. Peso is near a 7-year high vs the dollar, so a weaker peso could erase part of the gain in dollars', 'Rankia / Superfinanciera, Oct 2026'),
 O('Invest long term (VOO, broad index)', 'USD', 0, 0, '1–2 days, but price can be down', 'High in the short run', 'For money you will not need for 5+ years. Expected return is higher than cash but not a yield; shown as 0 here', 'Not a yield product'),
]

goals = [
 dict(goal='Emergency fund: 6 months of outflow', target=km['ef_target'], current=km['cash_total'], unit='USD',
      status='Ahead', gap=km['excess'], note='Fully funded twice over, but none of it earns anything', assumed='Assumed: you left the goals blank'),
 dict(goal='Side-business capital: $5k–$10k ready', target=10000, current=0, unit='USD', status='Not set aside',
      gap=10000, note='The excess cash covers it, but nothing is earmarked', assumed='From ai/persona/finances.md'),
 dict(goal='Side-business income: $2k–$3k a month', target=2000, current=5, unit='USD/mo', status='Behind',
      gap=1995, note='$60 of side income in 12 months (Retail AWare)', assumed='From ai/persona/finances.md'),
 dict(goal='Invest the monthly surplus', target=km['saved_12m'], current=km['invested_12m'], unit='USD/yr', status='Behind',
      gap=km['saved_12m'] - km['invested_12m'], note='Saved $21.5k in 12 months, invested $122', assumed='Assumed: you left the goals blank'),
 dict(goal='Financial independence (4% rule)', target=km['fi_target'], current=km['invested'], unit='USD', status='Long road',
      gap=km['fi_target'] - km['invested'], note='About 22 years if savings are invested; unreachable if kept in cash', assumed='Your stated driving goal'),
]

subs_cut = round((67.96 - 15.76) + 9.99 + 8.0 + 65.31 / 12, 0)
cuts = [
 dict(rank=1, item='Online shopping: hold at the 12-month median', monthly=r(by('Shopping (online)')['avg'] - by('Shopping (online)')['median']),
      basis='12-month average $443 vs median $207. Apr–Sep is already $186; the risk is a repeat of the $2,502 AliExpress day'),
 dict(rank=2, item='Subscriptions: undo the drift', monthly=r(subs_cut), basis='Apple back to $15.76 (now $67.96), drop Brave $9.99, find or cancel Open Inc $8, GoPro $65.31/yr'),
 dict(rank=3, item='Restaurants, cafés & bars back to Oct–Mar level', monthly=r(by('Restaurants, cafés & bars')['h2'] - by('Restaurants, cafés & bars')['h1']),
      basis='Apr–Sep $279/month vs Oct–Mar $228/month (+22%)'),
 dict(rank=4, item='Food delivery: keep the new habit', monthly=r(by('Food delivery')['avg'] - by('Food delivery')['h2']),
      basis='Apr–Sep $34/month vs 12-month average $78. Already saved; keep it'),
 dict(rank=5, item='USD→COP conversion: compare routes', monthly=r(km['fx_cost_yr'] / 12),
      basis='What the Wallbit spread costs per month now; a cheaper route saves part of it'),
]

ef_part = km['ef_invest_part']
actions = [
 dict(priority=1, action='Move the excess out of 0% accounts', detail='About $20.6k above the 6-month fund, mostly the Rippling wallet ($21.1k). Pick one or a mix from the options table',
      usd_yr_lo=r(ex * 0.036), usd_yr_hi=r(ex * 0.1349), effort='Easy', time='1–2 hours'),
 dict(priority=2, action='Put the emergency fund in a same-day yield', detail='Keep 1 month ($3.2k) in everyday accounts and the other 5 months in a USD T-bill fund or COP high-yield savings',
      usd_yr_lo=r(ef_part * 0.036), usd_yr_hi=r(ef_part * 0.0925), effort='Easy', time='1 hour'),
 dict(priority=3, action='Automate investing the monthly surplus', detail='About $1.8k saved a month, $122 invested in a year. A fixed monthly transfer to a broad index fund is what moves the FI date',
      usd_yr_lo=r(km['saved_12m'] * 0.05), usd_yr_hi=r(km['saved_12m'] * 0.05), effort='Easy', time='30 min once'),
 dict(priority=4, action='Cut the subscription drift', detail='Apple ($67.96 vs $15.76), Brave, Open Inc, GoPro',
      usd_yr_lo=r(subs_cut * 12), usd_yr_hi=r(subs_cut * 12), effort='Easy', time='15 min'),
 dict(priority=5, action='Bring restaurant spending back to the Oct–Mar level', detail='+22% in Apr–Sep, partly the Europe trip',
      usd_yr_lo=r(cuts[2]['monthly'] * 12), usd_yr_hi=r(cuts[2]['monthly'] * 12), effort='Medium', time='Habit'),
 dict(priority=6, action='Earmark $5k–$10k for the side business', detail='A separate pocket (a 6-month CDT or T-bills) so the capital goal is visibly funded and still earns',
      usd_yr_lo=None, usd_yr_hi=None, effort='Easy', time='30 min'),
 dict(priority=7, action='Point new eToro money at broad funds', detail='68% of eToro is in five single stocks; new contributions to VOO-type funds lower that without selling',
      usd_yr_lo=None, usd_yr_hi=None, effort='Easy', time='With action 3'),
 dict(priority=8, action='Check a cheaper USD→COP route', detail='Wallbit paid 0.8–1.6% under TRM in two checks; compare with Global66 or Wise on one transfer',
      usd_yr_lo=0, usd_yr_hi=r(km['fx_cost_yr']), effort='Easy', time='20 min'),
 dict(priority=9, action='Close the data gaps', detail='Label 20 flagged payouts ($9.2k, mostly Scotiabank 5256 and Fer), upload Wise and Nequi statements, sign in to eToro again',
      usd_yr_lo=None, usd_yr_hi=None, effort='Easy', time='30 min'),
]

out = dict(kpis=kpis, accounts=accounts, cash_history=hist, monthly=monthly, categories=catrows, recurring=recurring,
           unusual=unusual, options=options, goals=goals, cuts=cuts, actions=actions)
for k, v in out.items():
    json.dump(v, open(f'{W}/ds/{k}.json', 'w'), indent=0, ensure_ascii=False)
    print(k, len(v))
print({k: km[k] for k in ['cash_total', 'excess', 'infl_cost_yr', 'ef_invest_part', 'fx_cost_yr']}, subs_cut, [c['monthly'] for c in cuts])
print([(a['priority'], a['usd_yr_lo'], a['usd_yr_hi']) for a in actions])
