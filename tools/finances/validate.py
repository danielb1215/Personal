"""Checks a hand-transcribed statement before it goes into the sync.

python validate.py wallbit FILE        running balance must add up row by row
python validate.py bdb FILE            prints totals per statement cut to compare with the PDF summary
"""
import collections
import csv
import sys


def wallbit(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    bad, prev = [], None
    for i, r in enumerate(rows, start=2):
        a, b = float(r["amount_usd"] or 0), float(r["balance_usd"] or 0)
        if prev is not None and abs(prev + a - b) > 0.011:
            bad.append(f"line {i}: {prev:.2f} + {a:.2f} != {b:.2f} ({r['date']} {r['description']})")
        prev = b
    opening = float(rows[0]["balance_usd"]) - float(rows[0]["amount_usd"]) if rows else 0
    print(f"{len(rows)} rows, opening {opening:,.2f}, closing {prev or 0:,.2f}")
    print("OK" if not bad else "BALANCE ERRORS:\n" + "\n".join(bad))
    return not bad


def bdb(path):
    t = collections.defaultdict(lambda: collections.Counter())
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        a = float(r["amount_cop"])
        k = "payments" if r["description"].startswith("PAGO T.CREDITO") else ("credits" if a < 0 else "charges")
        t[r["statement_cut"]][k] += a
        t[r["statement_cut"]]["rows"] += 1
    for cut, c in sorted(t.items()):
        print(f"cut {cut}: rows {c['rows']}, charges {c['charges']:,.0f}, payments {c['payments']:,.0f}, credits {c['credits']:,.0f}")
    print("Compare charges with the PDF's 'Compras del mes' plus interest/insurance lines, and payments with 'Pagos'.")
    return True


if __name__ == "__main__":
    ok = {"wallbit": wallbit, "bdb": bdb}[sys.argv[1]](sys.argv[2])
    sys.exit(0 if ok else 1)
