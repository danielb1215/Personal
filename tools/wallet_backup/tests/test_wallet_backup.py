"""python3 -m unittest discover -s tools/wallet_backup/tests"""
import contextlib
import csv
import io
import os
import sys
import tempfile
import time
import unittest
from datetime import date
from decimal import Decimal
from unittest import mock

os.environ["TZ"] = "UTC"
time.tzset()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import backup  # noqa: E402
import fixture  # noqa: E402
import wallet_backup  # noqa: E402
import walletdb  # noqa: E402

CODES = {"amount_integer_scale": 10000, "status": {"0": "pending", "1": "settled", "2": "declined"},
         "refund_types": [], "skip_types": []}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = fixture.build(os.path.join(self.tmp.name, "passes23.sqlite"))

    def tearDown(self):
        self.tmp.cleanup()


class ValueTests(unittest.TestCase):
    def test_amount_integer_scaled(self):
        self.assertEqual(walletdb.to_amount(1250000, 10000), Decimal("125"))
        self.assertEqual(walletdb.to_amount("1250000", 100), Decimal("12500"))

    def test_amount_decimal_string_not_scaled(self):
        self.assertEqual(walletdb.to_amount("45.90", 10000), Decimal("45.90"))
        self.assertEqual(walletdb.to_amount(b"-3.5", 10000), Decimal("-3.5"))
        self.assertEqual(walletdb.to_amount(12.5, 10000), Decimal("12.5"))

    def test_amount_garbage(self):
        self.assertIsNone(walletdb.to_amount(None, 1))
        self.assertIsNone(walletdb.to_amount("abc", 1))

    def test_dates(self):
        self.assertEqual(walletdb.to_datetime(fixture.cocoa("2026-09-02T15:00:00")).isoformat(), "2026-09-02T15:00:00")
        self.assertEqual(walletdb.to_datetime(1790000000).year, 2026)          # Unix seconds
        self.assertEqual(walletdb.to_datetime(1790000000000).year, 2026)       # milliseconds
        self.assertEqual(walletdb.to_datetime("2026-01-02T03:04:05").day, 2)

    def test_default_since(self):
        self.assertEqual(wallet_backup.default_since(date(2026, 10, 15)), date(2026, 9, 1))
        self.assertEqual(wallet_backup.default_since(date(2026, 1, 3)), date(2025, 12, 1))


class ReadTests(Base):
    def rows(self, **kw):
        return {r["merchant"]: r for r in walletdb.read_transactions(walletdb.connect(self.db), CODES, **kw)}

    def test_schema_discovery(self):
        conn = walletdb.connect(self.db)
        path = walletdb.path_to(conn, "payment_transaction", "pass")
        self.assertEqual([p[2] for p in path], ["transaction_source", "payment_application", "pass"])

    def test_fields(self):
        r = self.rows()
        cafe = r["SYNTH CAFE"]
        self.assertEqual((cafe["date"], cafe["time"], cafe["card_name"], cafe["card_last4"]),
                         ("2026-09-02", "15:00:00", "Banco de Bogota", "9001"))  # fpan, not dpan
        self.assertEqual(cafe["amount"], Decimal("-125"))
        self.assertEqual(cafe["status"], "settled")
        self.assertTrue(cafe["wallet_txn_id"].startswith("APW-"))
        self.assertEqual(r["SYNTH MARKET"]["amount"], Decimal("-88000"))
        self.assertEqual(r["SYNTH BOOKS ONLINE"]["currency"], "EUR")

    def test_refund_pending_declined_unknown(self):
        r = self.rows()
        airline = [(x["amount"], x["status"]) for x in walletdb.read_transactions(walletdb.connect(self.db), CODES)
                   if x["merchant"] == "SYNTH AIRLINE"]
        self.assertEqual(sorted(airline), [(Decimal("-310.00"), "settled"), (Decimal("310.00"), "refund")])
        self.assertEqual(r["SYNTH PENDING"]["status"], "pending")
        self.assertEqual(r["SYNTH DECLINED"]["status"], "declined")
        self.assertEqual(r["SYNTH ODD"]["status"], "unknown")

    def test_refund_by_type_code(self):
        codes = dict(CODES, refund_types=[0])
        r = {x["merchant"]: x for x in walletdb.read_transactions(walletdb.connect(self.db), codes)}
        self.assertEqual(r["SYNTH CAFE"]["amount"], Decimal("125"))
        self.assertEqual(r["SYNTH CAFE"]["status"], "refund")

    def test_since(self):
        self.assertNotIn("SYNTH OLD", self.rows(since=date(2026, 9, 1)))
        self.assertIn("SYNTH OLD", self.rows())

    def test_ids_stable(self):
        a = sorted(r["wallet_txn_id"] for r in walletdb.read_transactions(walletdb.connect(self.db), CODES))
        b = sorted(r["wallet_txn_id"] for r in walletdb.read_transactions(walletdb.connect(self.db), CODES))
        self.assertEqual(a, b)
        self.assertEqual(len(set(a)), len(a))


class CliTests(Base):
    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = wallet_backup.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_probe_prints_no_personal_values(self):
        code, out, _ = self.run_cli("--db", self.db, "probe")
        self.assertEqual(code, 0)
        self.assertIn("payment_transaction [9 rows]", out)
        self.assertIn("transaction -> card path: payment_transaction.transaction_source_pid", out)
        self.assertIn("2026-07-01 to 2026-09-28", out)
        self.assertIn("amount storage:", out)
        self.assertIn("is_online: 1=9", out)          # tap vs online style flags are shown
        for secret in ("SYNTH CAFE", "SYNTH CITY", "SYNTH PRIVATE NOTE", "125", "45.90", "310", "4.6", "880000000",
                       "777001", "T-1"):
            self.assertNotIn(secret, out, secret)

    def test_export(self):
        out_dir = os.path.join(self.tmp.name, "inbox")
        code, out, _ = self.run_cli("--db", self.db, "export", "--since", "2026-09-01", "--out", out_dir)
        self.assertEqual(code, 0)
        with open(os.path.join(out_dir, wallet_backup.OUT_NAME)) as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(list(rows[0].keys()), walletdb.CSV_COLS)
        merchants = [r["merchant"] for r in rows]
        self.assertNotIn("SYNTH DECLINED", merchants)
        self.assertNotIn("SYNTH OLD", merchants)
        self.assertEqual(len(rows), 7)
        cafe = next(r for r in rows if r["merchant"] == "SYNTH CAFE")
        self.assertEqual((cafe["amount"], cafe["currency"], cafe["card_last4"]), ("-125.00", "COP", "9001"))
        self.assertEqual(os.listdir(out_dir), [wallet_backup.OUT_NAME])   # no leftover temp file
        self.assertIn("skipped 1 declined", out)

    def test_export_feeds_finances_sync(self):
        out_dir = os.path.join(self.tmp.name, "inbox")
        self.run_cli("--db", self.db, "export", "--since", "2026-09-01", "--out", out_dir)
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "finances"))
        import finlib
        rows, skipped = finlib.parse_wallet(os.path.join(out_dir, wallet_backup.OUT_NAME), "x.csv")
        accounts = sorted({r["account"] for r in rows})
        self.assertEqual(accounts, ["Banco de Bogotá Visa 2320", "Payoneer USD"])  # Bancolombia 9003 = debit, ignored
        self.assertEqual(dict(skipped), {})
        with open(os.path.join(out_dir, wallet_backup.OUT_NAME)) as f:
            self.assertTrue(f.readline().startswith("wallet_txn_id,date,time,card_name"))  # monthly.py sniff

    def test_default_out_falls_back(self):
        with mock.patch.object(wallet_backup, "DRIVE_INBOX_GLOBS", [os.path.join(self.tmp.name, "nope")]):
            self.assertEqual(wallet_backup.default_out(), os.path.join(os.getcwd(), "out"))
        drive = os.path.join(self.tmp.name, "GoogleDrive-x", "My Drive", "economics", "inbox")
        os.makedirs(drive)
        with mock.patch.object(wallet_backup, "DRIVE_INBOX_GLOBS", [os.path.join(self.tmp.name, "GoogleDrive-*", "My Drive", "economics", "inbox")]):
            self.assertEqual(wallet_backup.default_out(), drive)


class PasswordTests(unittest.TestCase):
    def test_keychain_success_not_printed(self):
        fake = mock.Mock(returncode=0, stdout="s3cret-synthetic\n")
        out = io.StringIO()
        with mock.patch("subprocess.run", return_value=fake) as run, contextlib.redirect_stdout(out):
            self.assertEqual(backup.password("keychain"), "s3cret-synthetic")
        self.assertIn(backup.KEYCHAIN_SERVICE, run.call_args[0][0])
        self.assertEqual(out.getvalue(), "")

    def test_keychain_missing(self):
        with mock.patch("subprocess.run", return_value=mock.Mock(returncode=44, stdout="")):
            with self.assertRaises(backup.BackupError):
                backup.password("keychain")

    def test_prompt_uses_getpass(self):
        with mock.patch("sys.stdin") as stdin, mock.patch("getpass.getpass", return_value="x") as gp:
            stdin.isatty.return_value = True
            self.assertEqual(backup.password("prompt"), "x")
            gp.assert_called_once()

    def test_newest_backup(self):
        with tempfile.TemporaryDirectory() as root:
            for i, name in enumerate(["old", "new"]):
                os.makedirs(os.path.join(root, name))
                p = os.path.join(root, name, "Manifest.db")
                open(p, "w").close()
                os.utime(p, (1000 + i * 100, 1000 + i * 100))
            os.makedirs(os.path.join(root, "not-a-backup"))
            self.assertTrue(backup.newest_backup(root).endswith("new"))

    def test_extract_copies_db_and_journal(self):
        files = [("HomeDomain", "Library/Passes/passes23.sqlite"), ("HomeDomain", "Library/Passes/passes23.sqlite-wal"),
                 ("HomeDomain", "Library/Passes/passes23.sqlite-shm")]

        class FakeBackup:
            calls = []

            def __init__(self, backup_directory, passphrase):
                assert passphrase == "pw"

            def test_decryption(self):
                return True

            @contextlib.contextmanager
            def manifest_db_cursor(self):
                cur = mock.Mock()
                cur.fetchall.return_value = files
                yield cur

            def extract_file(self, relative_path, domain_like, output_filename):
                FakeBackup.calls.append((domain_like, relative_path, os.path.basename(output_filename)))

        fake = mock.Mock(EncryptedBackup=FakeBackup)
        with mock.patch.dict(sys.modules, {"iphone_backup_decrypt": fake}), tempfile.TemporaryDirectory() as out:
            db, seen = backup.extract_wallet_db("/b", "pw", out)
        self.assertEqual(db, os.path.join(out, "passes23.sqlite"))
        self.assertEqual(sorted(c[2] for c in FakeBackup.calls),
                         ["passes23.sqlite", "passes23.sqlite-shm", "passes23.sqlite-wal"])

    def test_wrong_password_message(self):
        class IncorrectPassphraseError(Exception):
            pass

        class FakeBackup:
            def __init__(self, backup_directory, passphrase):
                raise IncorrectPassphraseError("bad " + passphrase)

        with mock.patch.dict(sys.modules, {"iphone_backup_decrypt": mock.Mock(EncryptedBackup=FakeBackup)}):
            with self.assertRaises(backup.BackupError) as cm:
                backup.extract_wallet_db("/b", "hunter2-synthetic", "/tmp")
        self.assertEqual(str(cm.exception), "wrong backup password")
        self.assertIsNone(cm.exception.__cause__)

    def test_no_backup(self):
        with tempfile.TemporaryDirectory() as root, self.assertRaises(backup.BackupError):
            backup.newest_backup(root)


if __name__ == "__main__":
    unittest.main()
