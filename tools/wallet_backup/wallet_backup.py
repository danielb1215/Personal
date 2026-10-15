"""Apple Wallet card transactions from an encrypted iPhone backup on this Mac.

  python3 wallet_backup.py probe                 schema + counts only (safe to paste back)
  python3 wallet_backup.py export [--since DATE] [--out DIR] [--password-from keychain]

Both read the newest backup in ~/Library/Application Support/MobileSync/Backup, or an already
decrypted database given with --db (used by the tests). See README.md.
"""
import argparse
import contextlib
import csv
import glob
import os
import sys
import tempfile
import time
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import backup  # noqa: E402
import walletdb  # noqa: E402

OUT_NAME = "apple_wallet_transactions.csv"
DRIVE_INBOX_GLOBS = [
    "~/Library/CloudStorage/GoogleDrive-*/My Drive/economics/inbox",
    "~/Library/CloudStorage/GoogleDrive-*/Mi unidad/economics/inbox",
    "/Volumes/GoogleDrive/My Drive/economics/inbox",
    "~/Google Drive/My Drive/economics/inbox",
]


def default_out():
    for g in DRIVE_INBOX_GLOBS:
        hits = sorted(glob.glob(os.path.expanduser(g)))
        if hits:
            return hits[0]
    return os.path.join(os.getcwd(), "out")


def default_since(today=None):
    """First day of the previous month: always overlaps the last monthly sync."""
    t = today or date.today()
    y, m = (t.year, t.month - 1) if t.month > 1 else (t.year - 1, 12)
    return date(y, m, 1)


@contextlib.contextmanager
def wallet_db(args):
    if args.db:
        yield args.db, []
        return
    bdir = args.backup or backup.newest_backup()
    age = (time.time() - os.path.getmtime(os.path.join(bdir, "Manifest.db"))) / 86400
    print(f"backup: {os.path.basename(bdir)[:8]}..., last updated {age:.1f} days ago", file=sys.stderr)
    if age > 3:
        print("warning: the newest backup is more than 3 days old - is the iPhone backing up to this Mac?",
              file=sys.stderr)
    with tempfile.TemporaryDirectory(prefix="wallet_") as tmp:
        os.chmod(tmp, 0o700)
        pw = backup.password(args.password_from)
        try:
            db, seen = backup.extract_wallet_db(bdir, pw, tmp)
        finally:
            del pw
        if not db:
            raise backup.BackupError("this backup has no Wallet database (passes23.sqlite). Make sure the backup is "
                                     "encrypted and finished, then back up again.")
        yield db, seen
        # temp copy (decrypted) is deleted when the block ends


def cmd_probe(args):
    codes = walletdb.load_codes(args.codes)
    with wallet_db(args) as (db, seen):
        print("# Apple Wallet probe")
        if seen:
            print("wallet files in backup: " + "; ".join(f"{d}:{p}" for d, p in seen))
        conn = walletdb.connect(db)
        print(walletdb.probe_report(conn, codes))
        conn.close()


def cmd_export(args):
    codes = walletdb.load_codes(args.codes)
    since = date.fromisoformat(args.since) if args.since else default_since()
    out_dir = args.out or default_out()
    os.makedirs(out_dir, exist_ok=True)
    with wallet_db(args) as (db, _):
        conn = walletdb.connect(db)
        rows = list(walletdb.read_transactions(conn, codes, since=since))
        conn.close()
    kept = [r for r in rows if r["status"] != "declined"]
    kept.sort(key=lambda r: (r["date"], r["time"], r["wallet_txn_id"]))
    path = os.path.join(out_dir, args.name)
    tmp = os.path.join(out_dir, "." + args.name + ".part")  # hidden until complete, then renamed
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=walletdb.CSV_COLS, extrasaction="ignore")
        w.writeheader()
        for r in kept:
            r = dict(r)
            r["amount"] = f"{r['amount']:.2f}"
            if r["billed_amount"] != "":
                r["billed_amount"] = f"{r['billed_amount']:.2f}"
            w.writerow(r)
    os.replace(tmp, path)
    unknown = sum(r["status"] == "unknown" for r in kept)
    print(f"wrote {len(kept)} transactions since {since} to {path} (skipped {len(rows) - len(kept)} declined)")
    if unknown:
        print(f"note: {unknown} rows have a status code not in wallet_codes.json (exported as 'unknown')")
    if not codes.get("confirmed"):
        print("note: wallet_codes.json is not confirmed yet - check a few rows against the Wallet app")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--backup", help="backup folder (default: newest in MobileSync/Backup)")
    p.add_argument("--db", help="use an already decrypted passes23.sqlite instead of a backup")
    p.add_argument("--password-from", choices=["prompt", "keychain"], default="prompt",
                   help=f"prompt (default) or the macOS Keychain item '{backup.KEYCHAIN_SERVICE}'")
    p.add_argument("--codes", help="status/type code mapping (default: wallet_codes.json next to this script)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe", help="print schema and counts only")
    e = sub.add_parser("export", help="write the transactions CSV")
    e.add_argument("--since", help="YYYY-MM-DD (default: first day of last month)")
    e.add_argument("--out", help="output folder (default: Google Drive economics/inbox if present, else ./out)")
    e.add_argument("--name", default=OUT_NAME, help=f"file name (default {OUT_NAME}; overwritten each run)")
    args = p.parse_args(argv)
    try:
        {"probe": cmd_probe, "export": cmd_export}[args.cmd](args)
    except backup.BackupError as ex:
        print(f"error: {ex}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
