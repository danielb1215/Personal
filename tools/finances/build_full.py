"""Full rebuild of the unified table from every raw source file.

Used once to create the Google Sheet, and to check that finlib still reproduces it.
Usage: python build_full.py RAW_DIR OUT_DIR
RAW_DIR holds rippling.csv, payoneer_*.csv, wallbit.csv, cc_bdb.csv, bancolombia_transactions.csv.
"""
import collections
import csv
import os
import sys

import finlib as F

RAW, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

rows = []
rows += F.parse_rippling(os.path.join(RAW, "rippling.csv"), "Rippling_2025-09_to_2026-10.csv")
PAYONEER_NAMES = {"payoneer_2023-10_2024-10.csv": "Payoneer_2023-10_to_2024-10.csv",
                  "payoneer_2024-10_2025-10.csv": "Payoneer_2024-10_to_2025-10.csv",
                  "payoneer_2025-10_2026-10.csv": "Payoneer_2025-10_to_2026-10.csv"}
seen = set()
for f in sorted(os.listdir(RAW)):
    if f.startswith("payoneer_"):
        for r in F.parse_payoneer(os.path.join(RAW, f), PAYONEER_NAMES.get(f, f)):
            if r["txn_id"] in seen:
                r["is_duplicate"] = "yes"
            seen.add(r["txn_id"])
            rows.append(r)
rows += F.parse_wallbit(os.path.join(RAW, "wallbit.csv"))
rows += F.parse_bdb(os.path.join(RAW, "cc_bdb.csv"))
# Placeholder for the missing June 2026 card statement
rows.append(F.new_row(
    txn_id="BDB-2026-06-MISSING", date="2026-06-30", account="Banco de Bogotá Visa 2320", currency="COP",
    amount=-2655096.0, description="MISSING STATEMENT June 2026 (total billed, from July 'Saldo Anterior')",
    flow_type="spending", category="Unknown (statement missing)", source_file="derived",
    needs_review="upload June 2026 card statement to itemize", notes="net of any June payments/credits; includes 5,900 insurance"))
rows += F.parse_bancolombia(os.path.join(RAW, "bancolombia_transactions.csv"))

F.categorize(rows)
rip_log, fx_log = F.match_all(rows)
F.label_unmatched_card_payments(rows)
cop_month, cop_n, eur_month = F.fx_tables(rows)
F.apply_usd(rows, cop_month, eur_month)
for r in rows:
    if r["flow_type"] == "card_payment" and not r["match_account"]:
        r["match_account"] = "UNKNOWN"

# ---- one-off answers from Daniel (2026-10-13) that only apply to history
by = lambda pred: [r for r in rows if pred(r)]
for card_date, usd_date, usd_amt, conf in (("2026-05-13", "2026-05-11", 1632.65, "strong: 2 days, ~3,660 COP/USD vs month 3,614"),
                                           ("2025-08-04", "2025-07-25", 1295.92, "probable: 10 days, ~3,513 COP/USD vs month 3,988")):
    card = by(lambda r: r["account"] == "Banco de Bogotá Visa 2320" and r["flow_type"] == "card_payment"
              and r["date"] == card_date and not r["match_id"])
    src = by(lambda r: r["account"] == "Payoneer USD" and r["date"] == usd_date and abs(r["amount"] + usd_amt) < 0.01)
    if card and src:
        c, s_ = card[0], src[0]
        F.link(s_, c, "PAY>3P>BDB")
        s_["flow_type"] = "card_payment"; s_["category"] = "Transfer"
        s_["est_other_ccy"] = f"funded card payment COP {c['amount']:,.0f} on {card_date} via {s_['counterparty']} ({conf})"
        c["est_other_ccy"] = f"funded by Payoneer USD {usd_amt:,.2f} on {usd_date} via {s_['counterparty']} ({conf})"
        s_["needs_review"] = c["needs_review"] = ""
        c["match_account"] = f"Payoneer USD via {s_['counterparty']}"
for b in by(lambda r: r["match_account"] == "UNKNOWN USD source"):
    b["match_account"] = "Payoneer USD (withdrawal not in export)"
    b["needs_review"] = "" if b["date"] < "2023-10-30" else \
        "from Payoneer per Daniel, but no matching withdrawal in the Oct 2023+ export"
for r in by(lambda r: r["account"] == "Rippling wallet" and r["date"] == "2025-11-17" and abs(r["amount"] + 3000) < 0.01):
    r["match_account"] = r["counterparty"] = "Wise (not in Drive)"
    r["needs_review"] = ""; F.add_note(r, "sent to Wise (confirmed)")
for r in by(lambda r: r["account"] == "Payoneer USD" and "WISE" in r["counterparty"].upper()):
    r["match_account"] = "Wise (not in Drive)"

F.apply_rules(rows)

rows.sort(key=lambda r: (r["date"], r["account"], r["txn_id"]))
F.write_rows(os.path.join(OUT, "transactions_unified.csv"), rows)
with open(os.path.join(OUT, "fx_rates_monthly.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["month", "cop_per_usd_median", "n_transfers"])
    for m in sorted(cop_month):
        w.writerow([m, round(cop_month[m], 2), cop_n[m]])
with open(os.path.join(OUT, "usd_to_cop_matches.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["sent_date", "from", "usd", "received_date", "cop", "rate", "status"])
    w.writerows(fx_log)
with open(os.path.join(OUT, "rippling_payout_matches.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["rippling_date", "amount_usd", "from", "to", "received_date", "status", "dest_note"])
    w.writerows(rip_log)
print("rows", len(rows), collections.Counter(r["flow_type"] for r in rows).most_common(6))
