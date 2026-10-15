"""python3 -m unittest discover -s tools/finances/tests   (synthetic data only)"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

FIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FIN)
import finlib as F  # noqa: E402

WALLET_HEAD = ["wallet_txn_id", "date", "time", "card_name", "card_last4", "merchant", "amount", "currency",
               "status", "source", "billed_amount", "billed_currency"]
COP_RATE, USD_PER_EUR = 4000.0, 1.10
PRE_WALLET_COMMIT = "a9135c1"   # last commit before the Apple Wallet integration


def L(**kw):
    """One ledger row as the Sheet returns it (strings)."""
    r = F.new_row(**kw)
    return [str(r[c]) for c in F.COLS]


def base_ledger():
    """FX context (one matched USD->COP transfer, one USD->EUR conversion) and a BdB statement up to 2026-08-25."""
    return [
        L(txn_id="PAY-USD-1", date="2026-08-10", account="Payoneer USD", currency="USD", amount=-1000,
          flow_type="internal_transfer", est_other_ccy=f"COP 4,000,000.00 received 2026-08-11 (rate {COP_RATE:,.2f} COP/USD)",
          match_id="PAY>BC-x"),
        L(txn_id="PAY-USD-2", date="2026-08-12", account="Payoneer USD", currency="USD", amount=-110,
          flow_type="fx_conversion", est_other_ccy=f"EUR 100.00 (USD/EUR {USD_PER_EUR:.4f})", match_id="FX-x"),
        L(txn_id="BDB-2026-08-000111", date="2026-08-25", account="Banco de Bogotá Visa 2320", currency="COP",
          amount=-50000, flow_type="spending", description="SYNTH SHOP", source_file="Extracto cut 2026-08-28"),
        L(txn_id="PAY-USD-3", date="2026-08-30", account="Payoneer USD", currency="USD", amount=-5,
          flow_type="spending", description="Card charge (SYNTH SNACK)"),
    ]


def wallet_csv(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(WALLET_HEAD)
        for r in rows:
            w.writerow(r + [""] * (len(WALLET_HEAD) - len(r)))


class Work:
    def __init__(self, ledger_rows):
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, "inbox"))
        json.dump({"values": [F.COLS] + ledger_rows}, open(os.path.join(self.dir, "ledger.json"), "w"))
        json.dump({"values": [["account", "type", "currency", "balance", "as_of", "usd", "source"],
                              ["Payoneer USD", "", "USD", "100", "2026-08-31", "", ""]]},
                  open(os.path.join(self.dir, "balances_current.json"), "w"))

    def inbox(self, name):
        return os.path.join(self.dir, "inbox", name)

    def run(self, script=os.path.join(FIN, "monthly.py")):
        p = subprocess.run([sys.executable, script, self.dir], cwd=FIN, capture_output=True, text=True)
        assert p.returncode == 0, p.stderr
        out = os.path.join(self.dir, "out")
        return (json.load(open(os.path.join(out, "append.json")))["values"],
                json.load(open(os.path.join(out, "updates.json"))),
                open(os.path.join(out, "summary.md")).read())

    def close(self):
        shutil.rmtree(self.dir)


def as_dicts(values):
    return [dict(zip(F.COLS, v)) for v in values]


class UnitTests(unittest.TestCase):
    rules = json.load(open(F.WALLET_CARDS))["cards"]

    def test_mapping(self):
        acc = lambda n, l4, c: F.wallet_account(n, l4, c, self.rules)
        self.assertEqual(acc("Banco de Bogotá", "1234", "EUR"), "Banco de Bogotá Visa 2320")
        self.assertEqual(acc("BANCO DE BOGOTA VISA", "", "COP"), "Banco de Bogotá Visa 2320")
        self.assertEqual(acc("Payoneer", "9", "EUR"), "Payoneer EUR")
        self.assertEqual(acc("Payoneer", "9", "GBP"), "Payoneer USD")
        self.assertEqual(acc("Bancolombia", "7380", "COP"), "Bancolombia Visa 7380")
        self.assertEqual(acc("Bancolombia", "7380", "USD"), "Bancolombia Visa 7380 (USD)")
        self.assertIsNone(acc("Bancolombia", "0000", "COP"))          # debit card: ignored on purpose
        self.assertIs(acc("Other Bank", "1111", "COP"), False)        # unknown: reported

    def test_family(self):
        self.assertEqual(F.card_family("Payoneer EUR"), "Payoneer")
        self.assertEqual(F.card_family("Bancolombia Visa 7380 (USD)"), "Bancolombia Visa 7380")
        self.assertEqual(F.card_family("Banco de Bogotá Visa 2320"), "Banco de Bogotá Visa 2320")

    def test_convert(self):
        cop, eur = {"2026-08": COP_RATE}, {"2026-08": USD_PER_EUR}
        self.assertAlmostEqual(F.convert(10, "EUR", "COP", "2026-09", cop, eur), 44000)
        self.assertAlmostEqual(F.convert(44000, "COP", "EUR", "2026-09", cop, eur), 10)
        self.assertIsNone(F.convert(10, "GBP", "COP", "2026-09", cop, eur))

    def test_similarity(self):
        self.assertGreater(F.merchant_similarity("Synth Books Online", "SYNTH BOOKS*ONL MADRID"), 0.5)
        self.assertLess(F.merchant_similarity("Synth Books", "FARMACIA CENTRAL"), 0.3)

    def test_match_rules(self):
        cop, eur = {"2026-08": COP_RATE}, {"2026-08": USD_PER_EUR}
        w = F.new_row(account="Banco de Bogotá Visa 2320", date="2026-09-05", currency="EUR", amount=-45.90,
                      description="Synth Books Online")
        s = F.new_row(account="Banco de Bogotá Visa 2320", date="2026-09-06", currency="COP", amount=-205000,
                      description="SYNTH BOOKS ONL")
        self.assertIsNotNone(F.wallet_match(w, s, cop, eur))                  # 1.5% FX difference
        self.assertIsNone(F.wallet_match(w, dict(s, amount=-250000), cop, eur))      # 24% off
        self.assertIsNone(F.wallet_match(w, dict(s, date="2026-09-10"), cop, eur))   # 5 days
        self.assertIsNone(F.wallet_match(w, dict(s, description="FARMACIA"), cop, eur))  # FX + other merchant
        self.assertIsNone(F.wallet_match(w, dict(s, amount=205000), cop, eur))       # refund vs purchase
        self.assertIsNone(F.wallet_match(w, dict(s, account="Payoneer USD"), cop, eur))
        same = dict(w, currency="COP", amount=-125000.0, description="Synth Cafe")
        self.assertIsNotNone(F.wallet_match(same, dict(s, amount=-125000.0, description="PAGO XYZ 123"), cop, eur))
        billed = dict(w, est_other_ccy="COP 204,100.00 billed (Apple Wallet)")
        self.assertIsNotNone(F.wallet_match(billed, dict(s, amount=-204100.0, description="ZZZ"), cop, eur))

    def test_parse_wallet(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "w.csv")
        wallet_csv(p, [["APW-a", "2026-09-03", "10:00:00", "Banco de Bogota", "9001", "SYNTH CAFE", "-125000.00", "COP", "settled", "apple_wallet"],
                       ["APW-b", "2026-09-04", "10:00:00", "Payoneer", "9002", "SYNTH X", "-3.00", "EUR", "pending", "apple_wallet"],
                       ["APW-c", "2026-09-04", "10:00:00", "Payoneer", "9002", "SYNTH Y", "-3.00", "USD", "declined", "apple_wallet"],
                       ["APW-d", "2026-09-04", "10:00:00", "Other Bank", "1111", "SYNTH Z", "-3.00", "USD", "settled", "apple_wallet"],
                       ["APW-e", "2026-09-04", "10:00:00", "Payoneer", "9002", "SYNTH R", "8.00", "USD", "refund", "apple_wallet"]])
        rows, skipped = F.parse_wallet(p, "w.csv")
        shutil.rmtree(d)
        self.assertEqual([r["txn_id"] for r in rows], ["APW-a", "APW-b", "APW-e"])
        self.assertEqual(rows[1]["account"], "Payoneer EUR")
        self.assertIn(F.WALLET_PENDING, rows[1]["notes"])
        self.assertEqual(rows[2]["flow_type"], "refund")
        self.assertEqual(dict(skipped), {"Other Bank ..1111": 1})


class SyncTests(unittest.TestCase):
    def month1(self):
        w = Work(base_ledger())
        wallet_csv(w.inbox("apple_wallet_transactions.csv"), [
            ["APW-old", "2026-08-20", "10:00:00", "Banco de Bogota", "9001", "SYNTH OLD", "-9000.00", "COP", "settled", "apple_wallet"],
            ["APW-gone", "2026-09-01", "10:00:00", "Banco de Bogota", "9001", "SYNTH REVERSED", "-7000.00", "COP", "settled", "apple_wallet"],
            ["APW-cafe", "2026-09-03", "10:00:00", "Banco de Bogota", "9001", "Synth Cafe", "-125000.00", "COP", "settled", "apple_wallet"],
            ["APW-books", "2026-09-05", "20:00:00", "Banco de Bogota", "9001", "Synth Books Online", "-45.90", "EUR", "settled", "apple_wallet"],
            ["APW-air", "2026-09-07", "12:00:00", "Payoneer", "9002", "Synth Airline", "-310.00", "USD", "pending", "apple_wallet"],
            ["APW-other", "2026-09-07", "12:00:00", "Other Bank", "1111", "SYNTH Z", "-3.00", "USD", "settled", "apple_wallet"],
            ["APW-debit", "2026-09-07", "12:00:00", "Bancolombia", "0000", "SYNTH D", "-3000.00", "COP", "settled", "apple_wallet"],
        ])
        return w

    def test_first_month_appends_wallet_rows_after_statement_period(self):
        w = self.month1()
        try:
            append, updates, summary = w.run()
        finally:
            w.close()
        rows = {r["txn_id"]: r for r in as_dicts(append)}
        self.assertEqual(sorted(rows), ["APW-air", "APW-books", "APW-cafe", "APW-gone"])
        self.assertEqual(updates, [])
        self.assertEqual(rows["APW-books"]["account"], "Banco de Bogotá Visa 2320")
        self.assertEqual(rows["APW-books"]["currency"], "EUR")
        self.assertAlmostEqual(rows["APW-books"]["amount_usd"], -50.49, places=2)
        self.assertEqual(rows["APW-cafe"]["amount_usd"], -31.25)
        self.assertEqual(rows["APW-air"]["account"], "Payoneer USD")
        self.assertIn("Wallet rows skipped (a statement already covers those days): 1", summary)
        self.assertIn("Other Bank ..1111 (1 rows)", summary)

    def test_second_month_statement_replaces_wallet_rows(self):
        ledger = base_ledger()
        apw = []
        for tid, d, acct, cur, amt, m, notes in (
                ("APW-gone", "2026-09-01", "Banco de Bogotá Visa 2320", "COP", -7000, "SYNTH REVERSED", F.WALLET_NOTE),
                ("APW-cafe", "2026-09-03", "Banco de Bogotá Visa 2320", "COP", -125000, "Synth Cafe", F.WALLET_NOTE),
                ("APW-books", "2026-09-05", "Banco de Bogotá Visa 2320", "EUR", -45.90, "Synth Books Online", F.WALLET_NOTE),
                ("APW-air", "2026-09-07", "Payoneer USD", "USD", -310, "Synth Airline", F.WALLET_NOTE + "; " + F.WALLET_PENDING),
                ("APW-late", "2026-09-29", "Banco de Bogotá Visa 2320", "COP", -1000, "SYNTH LATE", F.WALLET_NOTE)):
            apw.append(L(txn_id=tid, date=d, account=acct, currency=cur, amount=amt, description=m, counterparty=m,
                         flow_type="spending", category="My own category", notes=notes, amount_usd="-1"))
        w = Work(ledger + apw)
        with open(w.inbox("cc_bdb_2026-09.csv"), "w") as f:
            f.write("statement_cut,comprobante,description,date_txn,date_post,plazo,amount_cop,cuota_mes,cuotas_pend,saldo_pend\n"
                    "2026-09-28,000201,SYNTH CAFE BOGOTA,2026-09-03,2026-09-04,01,125000,,,\n"
                    "2026-09-28,000202,SYNTH BOOKS*ONL MADRID,2026-09-06,2026-09-07,01,205000,,,\n"
                    "2026-09-28,000203,SYNTH NEW ITEM,2026-09-20,2026-09-21,01,30000,,,\n")
        with open(w.inbox("payoneer_usd.csv"), "w") as f:
            f.write("currency,date,time,credit,debit,balance,description\n"
                    "USD,09-08-2026,09:00:00,,-310.00,500.00,Card charge (SYNTH AIRLINE)\n"
                    "USD,09-09-2026,09:00:00,,-20.00,480.00,Card charge (SYNTH ONLY IN CSV)\n")
        wallet_csv(w.inbox("apple_wallet_transactions.csv"), [   # nightly export overlaps the Sheet
            ["APW-air", "2026-09-07", "12:00:00", "Payoneer", "9002", "Synth Airline", "-310.00", "USD", "settled", "apple_wallet"],
            ["APW-late", "2026-09-29", "10:00:00", "Banco de Bogota", "9001", "SYNTH LATE", "-1000.00", "COP", "settled", "apple_wallet"],
            ["APW-oct", "2026-10-02", "10:00:00", "Banco de Bogota", "9001", "SYNTH OCT", "-2000.00", "COP", "settled", "apple_wallet"],
            ["APW-in-csv", "2026-09-09", "10:00:00", "Payoneer", "9002", "Synth Only In Csv", "-20.00", "USD", "settled", "apple_wallet"],
        ])
        try:
            append, updates, summary = w.run()
        finally:
            w.close()
        appended = {r["txn_id"]: r for r in as_dicts(append)}
        # statement rows that replaced a Wallet row are not appended; Wallet duplicates are not appended
        self.assertEqual(sorted(appended), ["APW-oct", "BDB-2026-09-000203",
                                            sorted(k for k in appended if k.startswith("PAY-"))[0]])
        self.assertEqual(appended[next(k for k in appended if k.startswith("PAY-"))]["description"],
                         "Card charge (SYNTH ONLY IN CSV)")
        up = {u["range"]: dict(zip(F.COLS, u["values"][0])) for u in updates}
        rows = {r["txn_id"]: r for r in up.values()}
        self.assertEqual(sorted(k for k in rows if not k.startswith("APW")),
                         ["BDB-2026-09-000201", "BDB-2026-09-000202", sorted(k for k in rows if k.startswith("PAY-"))[0]])
        books = rows["BDB-2026-09-000202"]
        self.assertEqual((books["currency"], books["amount"], books["date"]), ("COP", -205000, "2026-09-06"))
        self.assertEqual(books["est_other_ccy"], "Apple Wallet EUR 45.90")
        self.assertEqual(books["category"], "My own category")                # Daniel's edit kept
        self.assertAlmostEqual(books["amount_usd"], -51.25, places=2)          # recomputed in COP
        self.assertIn("Apple Wallet row confirmed by statement", books["notes"])
        self.assertNotIn(F.WALLET_NOTE, books["notes"])
        self.assertTrue(rows["APW-gone"]["needs_review"].startswith("Apple Wallet row not found"))
        self.assertNotIn("APW-late", rows)                                     # after the cut: still waiting
        self.assertIn("Wallet rows replaced by statement rows: 3", summary)
        self.assertIn("Wallet rows missing from the statement (flagged): 1", summary)
        self.assertNotIn("SYNTH AIRLINE", json.dumps(append))                  # no double count

    def test_pending_settles_in_place(self):
        row = L(txn_id="APW-p", date="2026-09-10", account="Banco de Bogotá Visa 2320", currency="COP", amount=-80000,
                description="SYNTH BAR", flow_type="spending", notes=F.WALLET_NOTE + "; " + F.WALLET_PENDING, amount_usd="-20")
        w = Work(base_ledger() + [row])
        wallet_csv(w.inbox("apple_wallet_transactions.csv"), [
            ["APW-p", "2026-09-10", "22:00:00", "Banco de Bogota", "9001", "SYNTH BAR", "-92000.00", "COP", "settled", "apple_wallet"]])
        try:
            append, updates, summary = w.run()
        finally:
            w.close()
        self.assertEqual(append, [])
        self.assertEqual(len(updates), 1)
        r = dict(zip(F.COLS, updates[0]["values"][0]))
        self.assertEqual((r["amount"], r["amount_usd"], r["notes"]), (-92000, -23.0, F.WALLET_NOTE))

    def test_same_month_statement_wins(self):
        w = Work(base_ledger())
        wallet_csv(w.inbox("apple_wallet_transactions.csv"), [
            ["APW-x", "2026-09-03", "10:00:00", "Banco de Bogota", "9001", "Synth Cafe", "-125000.00", "COP", "settled", "apple_wallet"],
            ["APW-y", "2026-10-01", "10:00:00", "Banco de Bogota", "9001", "Synth Later", "-1000.00", "COP", "settled", "apple_wallet"]])
        with open(w.inbox("cc_bdb_2026-09.csv"), "w") as f:
            f.write("statement_cut,comprobante,description,date_txn,date_post,plazo,amount_cop,cuota_mes,cuotas_pend,saldo_pend\n"
                    "2026-09-28,000201,SYNTH CAFE BOGOTA,2026-09-03,2026-09-04,01,125000,,,\n")
        try:
            append, updates, _ = w.run()
        finally:
            w.close()
        self.assertEqual(sorted(r[0] for r in append), ["APW-y", "BDB-2026-09-000201"])


class RegressionTests(unittest.TestCase):
    """Without a Wallet file, monthly.py gives the same output as before this change."""

    def test_same_output_as_previous_version(self):
        try:
            old_src = subprocess.run(["git", "show", f"{PRE_WALLET_COMMIT}:tools/finances/monthly.py"],
                                     cwd=FIN, capture_output=True, text=True, check=True).stdout
        except (subprocess.CalledProcessError, OSError):
            self.skipTest("previous monthly.py not available from git")
        old_script = os.path.join(FIN, "_monthly_previous_test.py")
        open(old_script, "w").write(old_src)
        try:
            outs = []
            for script in (old_script, os.path.join(FIN, "monthly.py")):
                w = Work(base_ledger() + [L(txn_id="BCE-1", date="2026-09-02", account="Bancolombia savings 6948",
                                            currency="COP", amount=-5000, description="COMPRA EN SYNTH")])
                with open(w.inbox("cc_bdb_2026-09.csv"), "w") as f:
                    f.write("statement_cut,comprobante,description,date_txn,date_post,plazo,amount_cop,cuota_mes,cuotas_pend,saldo_pend\n"
                            "2026-09-28,000201,SYNTH CAFE BOGOTA,2026-09-03,2026-09-04,01,125000,,,\n"
                            "2026-09-28,000209,PAGO T.CREDITO,2026-09-10,2026-09-10,00,-500000,,,\n")
                with open(w.inbox("payoneer_usd.csv"), "w") as f:
                    f.write("currency,date,time,credit,debit,balance,description\n"
                            "USD,09-08-2026,09:00:00,,-310.00,500.00,Card charge (SYNTH AIRLINE)\n")
                try:
                    a, u, s = w.run(script)
                    outs.append((a, u, s.replace(os.path.basename(script), "")))
                finally:
                    w.close()
            self.assertEqual(outs[0], outs[1])
        finally:
            os.remove(old_script)


if __name__ == "__main__":
    unittest.main()
