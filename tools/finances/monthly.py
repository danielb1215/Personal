"""Monthly incremental sync for the finances_unified Google Sheet.

The Sheet's Transactions tab is the ledger: rows already there are never rewritten,
except to fill in a transfer match or to swap a stand-in row for the statement row it turned
into: Bancolombia alert emails (BCE-) and Apple Wallet card purchases (APW-). New rows are appended.

Usage: python monthly.py WORK_DIR
WORK_DIR/
  ledger.json            get_values response for Transactions!A1:R (required)
  balances_current.json  get_values response for Balances!A1:G20 (required)
  bc_alerts.json         [{"id","date","text"}] Bancolombia alert emails (optional)
  statement_balances.json [{"account","balance","as_of","source"}] closing balances read from PDFs (optional)
  inbox/                 the month's files (Payoneer/Rippling/Wise CSV exports, transcribed
                         wallbit*.csv and cc_bdb*.csv, Bancolombia transactions.csv, and
                         apple_wallet_transactions.csv from tools/wallet_backup)
Writes WORK_DIR/out/: append.json, updates.json, balances_updates.json, fx_values.json,
new_rows.csv, summary.md
"""
import collections
import copy
import csv
import json
import os
import re
import sys
from datetime import date

import finlib as F

WORK = sys.argv[1]
OUT = os.path.join(WORK, "out")
os.makedirs(OUT, exist_ok=True)
MATCH_FIELDS = ("match_id", "match_account", "est_other_ccy", "counterparty")


def load_values(name):
    a = json.load(open(os.path.join(WORK, name)))
    return a.get("values", a) if isinstance(a, dict) else a


# ---------------------------------------------------------------- ledger
vals = load_values("ledger.json")
head = vals[0]
assert head[:len(F.COLS)] == F.COLS, f"unexpected Transactions header: {head[:18]}"
ledger = []
for i, v in enumerate(vals[1:], start=2):
    if not v or not v[0]:
        continue
    v = list(v) + [""] * (len(F.COLS) - len(v))
    r = F.new_row(**dict(zip(F.COLS, v[:len(F.COLS)])))
    r["amount"] = F.num(r["amount"])
    r["_row"] = i
    ledger.append(r)
ledger_ids = {r["txn_id"] for r in ledger}
snap = {r["_row"]: copy.deepcopy(r) for r in ledger}
bc_stmt_end = max((r["date"] for r in ledger if r["txn_id"].startswith("BC-")
                   and r["account"] == "Bancolombia savings 6948"), default="")

# ---------------------------------------------------------------- inbox
def sniff(path):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        h = f.readline()
    if h.startswith("Currency,Payout method") or h.startswith("currency,date,time,credit"):
        return "payoneer"
    if h.startswith("transaction ID,date & time"):
        return "rippling"
    if h.startswith("date,description,counterparty,status,operation_id"):
        return "wallbit"
    if h.startswith("statement_cut,comprobante"):
        return "bdb"
    if "account_type" in h and "balance_after" in h:
        return "bancolombia"
    if "TransferWise ID" in h or "Running Balance" in h:
        return "wise"
    if h.startswith("wallet_txn_id,date,time,card_name"):
        return "wallet"
    return None


new, received, unknown_files = [], collections.defaultdict(list), []
wallet_skipped = collections.Counter()
inbox = os.path.join(WORK, "inbox")
for f in sorted(os.listdir(inbox)) if os.path.isdir(inbox) else []:
    p = os.path.join(inbox, f)
    kind = sniff(p) if f.lower().endswith(".csv") else None
    if kind == "payoneer":
        rs = F.parse_payoneer(p, f)
    elif kind == "rippling":
        rs = F.parse_rippling(p, f)
    elif kind == "wallbit":
        rs = F.parse_wallbit(p, f)
    elif kind == "bdb":
        rs = F.parse_bdb(p)
    elif kind == "bancolombia":
        rs = F.parse_bancolombia(p)
    elif kind == "wise":
        rs = F.parse_wise(p, f)
    elif kind == "wallet":
        rs, skipped = F.parse_wallet(p, f)
        wallet_skipped.update(skipped)
    else:
        unknown_files.append(f)
        continue
    received[kind].append(f)
    new += rs

stmt_rows = [r for r in new if r["txn_id"].startswith("BC-") and r["account"] == "Bancolombia savings 6948"]
stmt_end = max([r.get("_period_end") or r["date"] for r in stmt_rows] + [bc_stmt_end])

# Bancolombia alert emails: only for days the statements don't cover yet
alert_rows, unparsed_alerts, foreign_alerts = [], [], []
if os.path.exists(os.path.join(WORK, "bc_alerts.json")):
    alert_rows, unparsed_alerts, foreign_alerts = F.parse_bc_alerts(os.path.join(WORK, "bc_alerts.json"))
    received["bancolombia alerts"].append(f"{len(alert_rows)} movements")
    alert_rows = [r for r in alert_rows if r["date"] > stmt_end]
new += alert_rows

# A new Bancolombia statement replaces the alert rows already in the sheet for its period
updates = {}
superseded, alert_not_in_stmt = 0, []
if stmt_rows:
    open_alerts = [r for r in ledger if r["txn_id"].startswith("BCE-") and r["date"] <= stmt_end]
    taken = set()
    for s in sorted(stmt_rows, key=lambda r: r["date"]):
        cand = [a for a in open_alerts if id(a) not in taken and abs(a["amount"] - s["amount"]) < 1
                and abs((F.dt(a["date"]) - F.dt(s["date"])).days) <= 3]
        if not cand:
            continue
        a = min(cand, key=lambda a: abs((F.dt(a["date"]) - F.dt(s["date"])).days))
        taken.add(id(a))
        a.update(txn_id=s["txn_id"], date=s["date"], description=s["description"], source_file=s["source_file"],
                 notes=a["notes"].replace("from alert email; replaced by the statement row when the quarterly "
                                          "statement arrives", "alert email confirmed by statement").strip("; "))
        updates[a["_row"]] = a
        s["_drop"] = True
        superseded += 1
    alert_not_in_stmt = [a for a in open_alerts if id(a) not in taken]
    for a in alert_not_in_stmt:
        a["needs_review"] = "alert email row not found in the Bancolombia statement - duplicate or reversed?"
        updates[a["_row"]] = a

# Apple Wallet rows stand in for card purchases until the card statement / Payoneer CSV covers them
cop0, _, eur0 = F.fx_tables(ledger)
wallet_updates, wallet_stats = F.reconcile_wallet(ledger, new, cop0, eur0)
for a in wallet_updates:
    updates[a["_row"]] = a

# Payoneer rows loaded before the stable IDs (PAY-CUR-YYYY-MM-DD-HHMMSS-n) are recognised by content.
OLD_PAY = re.compile(r"^PAY-(USD|EUR)-(\d{4}-\d{2}-\d{2})-(\d{6})-\d+$")
pay_seen = collections.Counter()
for r in ledger:
    m = OLD_PAY.match(r["txn_id"])
    if m:
        t = m.group(3)
        r["_time"] = f"{t[:2]}:{t[2:4]}:{t[4:]}"
        pay_seen[(r["currency"], r["date"], r["_time"], round(r["amount"], 2), r["description"])] += 1
seen = set(ledger_ids) | {a["txn_id"] for a in updates.values()}
fresh = []
for r in new:
    if r.get("_drop") or r["txn_id"] in seen:
        continue
    if r["txn_id"].startswith("PAY-"):
        k = (r["currency"], r["date"], r["_time"], round(r["amount"], 2), r["description"])
        if pay_seen[k] > 0:
            pay_seen[k] -= 1
            continue
    seen.add(r["txn_id"])
    fresh.append(r)
new = fresh

# ---------------------------------------------------------------- classify + match
F.categorize(new)
combined = ledger + new
F.match_all(combined, unmatched_cop_msg="USD side not found yet - load this month's Wallbit statement / Payoneer CSV")
F.label_unmatched_card_payments(new)
for r in new:
    if r["flow_type"] == "card_payment" and not r["match_account"]:
        r["match_account"] = "UNKNOWN"
    if r["needs_review"].startswith("card payment with no matching card-statement row"):
        r["needs_review"] = "waiting for this month's card statement"
        r["match_account"] = "card statement not loaded yet"
F.apply_rules(new)

# Existing rows may only gain a match; anything else the matchers touched is put back.
for r in ledger:
    before = snap[r["_row"]]
    if r["_row"] in updates:
        continue
    if before["match_id"] == "" and r["match_id"]:
        keep = {k: r[k] for k in MATCH_FIELDS}
        cleared = before["needs_review"] and not r["needs_review"]
        r.clear(); r.update(copy.deepcopy(before)); r.update(keep)
        if cleared:
            r["needs_review"] = ""
        updates[r["_row"]] = r
    else:
        r.clear(); r.update(copy.deepcopy(before))

cop_month, cop_n, eur_month = F.fx_tables(combined)
F.apply_usd(new, cop_month, eur_month, only_missing=True)
F.apply_usd(wallet_updates, cop_month, eur_month, only_missing=True)
new.sort(key=lambda r: (r["date"], r["account"], r["txn_id"]))

# ---------------------------------------------------------------- outputs
json.dump({"range": "Transactions!A1", "values": [F.sheet_row(r) for r in new]}, open(os.path.join(OUT, "append.json"), "w"))
json.dump([{"range": f"Transactions!A{row}:R{row}", "values": [F.sheet_row(r)]} for row, r in sorted(updates.items())],
          open(os.path.join(OUT, "updates.json"), "w"))
fx_vals = [["month", "cop_per_usd_median", "n_transfers"]] + \
          [[m, round(cop_month[m], 2), cop_n[m]] for m in sorted(cop_month)]
json.dump({"range": "'FX rates'!A1", "values": fx_vals}, open(os.path.join(OUT, "fx_values.json"), "w"))
F.write_rows(os.path.join(OUT, "new_rows.csv"), new)

# ---------------------------------------------------------------- balances
bal_vals = load_values("balances_current.json")
bal_rows = {v[0]: i for i, v in enumerate(bal_vals, start=1) if v and v[0] and i > 1}
current = {v[0]: v for v in bal_vals[1:] if v and v[0]}
bal = {}


def last_by(rows, key):
    rows = [r for r in rows if r.get("_balance") not in (None, "")]
    return max(rows, key=key) if rows else None


for cur in ("USD", "EUR"):
    r = last_by([x for x in new if x["account"] == "Payoneer " + cur], lambda x: (x["date"], x.get("_time", "")))
    if r:
        bal["Payoneer " + cur] = (r["_balance"], r["date"], "Payoneer export running balance")
wal = [x for x in F.parse_wallbit(os.path.join(inbox, received["wallbit"][-1]))] if received["wallbit"] else []
if wal:
    bal["Wallbit"] = (wal[-1]["_balance"], wal[-1]["date"], "Wallbit statement closing balance")
rip = [x for x in combined if x["account"] == "Rippling wallet"]
if received["rippling"]:
    bal["Rippling wallet"] = (round(sum(x["amount"] for x in rip), 2), max(x["date"] for x in rip),
                              "sum of every Rippling wallet movement since Sep 2025")
r = last_by([x for x in new if x["account"].startswith("Wise ")], lambda x: x["date"])
if r:
    bal["Wise"] = (r["_balance"], r["date"], "Wise statement running balance")
if stmt_rows:
    last = max(stmt_rows, key=lambda x: x["date"])
    alerts_after = [x for x in new if x["txn_id"].startswith("BCE-") and x["date"] > stmt_end]
    b = last["_balance"] + sum(x["amount"] for x in alerts_after)
    bal["Bancolombia savings 6948"] = (round(b, 2), max([stmt_end] + [x["date"] for x in alerts_after]),
                                       "Bancolombia statement closing balance + alert emails since")
elif alert_rows and "Bancolombia savings 6948" in current:
    c = current["Bancolombia savings 6948"]
    added = [x for x in new if x["txn_id"].startswith("BCE-")]
    if added:
        b = F.num(c[3]) + sum(x["amount"] for x in added)
        bal["Bancolombia savings 6948"] = (round(b, 2), max(x["date"] for x in added),
                                           "previous balance + alert emails (interest and fees arrive with the quarterly statement)")
sb = os.path.join(WORK, "statement_balances.json")
if os.path.exists(sb):
    for x in json.load(open(sb)):
        bal[x["account"]] = (x["balance"], x["as_of"], x["source"])

bal_updates, bal_missing = [], []
for acct, (b, as_of, src) in bal.items():
    row = bal_rows.get(acct)
    if not row:
        bal_missing.append(acct)
        continue
    bal_updates.append({"range": f"Balances!D{row}:E{row}", "values": [[b, as_of]]})
    bal_updates.append({"range": f"Balances!G{row}", "values": [[src + f" (updated {date.today().isoformat()})"]]})
json.dump(bal_updates, open(os.path.join(OUT, "balances_updates.json"), "w"))

# ---------------------------------------------------------------- summary
months = collections.Counter(r["date"][:7] for r in new)
focus = max(months, key=lambda m: (months[m], m)) if months else ""
spend = collections.defaultdict(float)
for r in new:
    if r["date"][:7] == focus and r["flow_type"] in ("spending", "refund", "fee") and r["amount_usd"] not in ("", None):
        spend[r["category"] or r["flow_type"]] += float(r["amount_usd"])
expected = {"payoneer": "Payoneer CSV", "rippling": "Rippling CSV", "wallbit": "Wallbit statement",
            "bdb": "Banco de Bogotá statement"}
L = [f"# Finances sync {date.today().isoformat()}", ""]
L.append(f"- New rows appended: **{len(new)}** (" + ", ".join(f"{k}: {v}" for k, v in sorted(
    collections.Counter(r['account'] for r in new).items())) + ")")
L.append(f"- Existing rows updated: {len(updates)} (alert rows confirmed by statement: {superseded})")
L.append("- Files received: " + ("; ".join(f"{k}: {', '.join(v)}" for k, v in received.items() if v) or "none"))
missing = [v for k, v in expected.items() if not received[k]]
if missing:
    L.append("- **Not received this month:** " + ", ".join(missing))
if unknown_files:
    L.append("- Files I couldn't recognise (left in the inbox): " + ", ".join(unknown_files))
if received["wallet"]:
    WS = {"replaced": "Wallet rows replaced by statement rows",
          "same_run": "Wallet rows already in this month's statements (not added)",
          "pending_settled": "pending Wallet rows now settled",
          "inside_statement_period": "Wallet rows skipped (a statement already covers those days)",
          "already_in_alert_emails": "Wallet rows skipped (already in Bancolombia alert emails)",
          "flagged": "Wallet rows missing from the statement (flagged)"}
    L.append("- Apple Wallet: " + (", ".join(f"{WS[k]}: {v}" for k, v in wallet_stats.items() if v)
                                   or "nothing to reconcile"))
if wallet_skipped:
    L.append("- Wallet cards with no ledger account in wallet_cards.json (skipped): "
             + ", ".join(f"{k} ({v} rows)" for k, v in wallet_skipped.items()))
if focus:
    L += ["", f"## Spending in {focus} from the new rows (USD)", ""]
    for c, v in sorted(spend.items(), key=lambda kv: kv[1]):
        L.append(f"- {c}: {v:,.0f}")
    L.append(f"- **Total: {sum(spend.values()):,.0f}**")
flagged = [r for r in new if r["needs_review"]] + [r for r in updates.values() if r["needs_review"]]
if flagged:
    L += ["", f"## Needs your answer ({len(flagged)})", ""]
    for r in flagged[:40]:
        L.append(f"- {r['date']} {r['account']} {float(r['amount']):,.2f} {r['currency']} - {r['description'][:50]}: {r['needs_review']}")
if foreign_alerts:
    L += ["", "## Foreign transfers announced by email (COP amount arrives with the statement)", ""]
    L += [f"- {x['date']}: USD {x['usd']}" for x in foreign_alerts]
if unparsed_alerts:
    L += ["", "## Bancolombia emails with an amount I couldn't read", ""]
    L += [f"- {x['date']}: {x['text'][:140]}" for x in unparsed_alerts]
if bal:
    L += ["", "## Balances updated", ""]
    L += [f"- {a}: {b:,.2f} as of {d}" for a, (b, d, s) in bal.items()]
if bal_missing:
    L.append("- No row in the Balances tab for: " + ", ".join(bal_missing))
open(os.path.join(OUT, "summary.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
