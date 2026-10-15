"""Builds a synthetic passes23-like SQLite file. All values are invented."""
import sqlite3
from datetime import datetime, timezone

COCOA = datetime(2001, 1, 1, tzinfo=timezone.utc)


def cocoa(iso):
    return (datetime.fromisoformat(iso).replace(tzinfo=timezone.utc) - COCOA).total_seconds()


PASSES = [  # pid, unique_id, organization_name, fpan_suffix, dpan_suffix
    (1, "pass-bdb", "Banco de Bogota", "9001", "5555"),
    (2, "pass-pay", "Payoneer", "9002", "6666"),
    (3, "pass-bc", "Bancolombia", "9003", "7777"),
    (4, "pass-boarding", "Some Airline", None, None),   # not a payment card
]

# pid, identifier, source_pid, date (UTC), merchant, amount, currency, status, type
TXNS = [
    (1, "T-1", 1, "2026-09-02T15:00:00", "SYNTH CAFE", 1250000, "COP", 1, 0),          # integer, scale 10000 -> 125.00
    (2, "T-2", 1, "2026-09-05T20:30:00", "SYNTH BOOKS ONLINE", "45.90", "EUR", 1, 0),   # decimal string
    (3, "T-3", 2, "2026-09-07T12:00:00", "SYNTH AIRLINE", "310.00", "USD", 1, 0),
    (4, "T-4", 2, "2026-09-08T12:00:00", "SYNTH AIRLINE", "-310.00", "USD", 1, 0),      # refund stored negative
    (5, "T-5", 3, "2026-09-10T18:00:00", "SYNTH MARKET", 880000000, "COP", 1, 0),       # 88,000.00
    (6, "T-6", 1, "2026-09-11T18:00:00", "SYNTH DECLINED", 990000, "COP", 2, 0),        # declined
    (7, "T-7", 1, "2026-09-28T23:59:00", "SYNTH PENDING", "12.00", "USD", 0, 0),
    (8, "T-8", 1, "2026-07-01T10:00:00", "SYNTH OLD", "1.00", "USD", 1, 0),             # before --since
    (9, "T-9", 2, "2026-09-12T09:00:00", "SYNTH ODD", "5.00", "USD", 9, 0),             # unknown status code
]


def build(path):
    c = sqlite3.connect(path)
    c.executescript("""
    CREATE TABLE pass (pid INTEGER PRIMARY KEY, unique_id TEXT, organization_name TEXT, pass_type_id TEXT);
    CREATE TABLE payment_application (pid INTEGER PRIMARY KEY, pass_pid INTEGER, fpan_suffix TEXT, dpan_suffix TEXT);
    CREATE TABLE transaction_source (pid INTEGER PRIMARY KEY, payment_application_pid INTEGER, type INTEGER);
    CREATE TABLE payment_transaction (pid INTEGER PRIMARY KEY, identifier TEXT, transaction_source_pid INTEGER,
        transaction_date REAL, merchant_name TEXT, locality TEXT, amount, currency_code TEXT,
        transaction_status INTEGER, transaction_type INTEGER, location_latitude REAL,
        foreign_currency_amount INTEGER DEFAULT 777001, is_online INTEGER DEFAULT 1);
    CREATE TABLE unrelated_table (pid INTEGER PRIMARY KEY, note TEXT);
    """)
    for pid, uid, org, f4, d4 in PASSES:
        c.execute("INSERT INTO pass VALUES (?,?,?,?)", (pid, uid, org, "pass.synthetic"))
        if f4:
            c.execute("INSERT INTO payment_application VALUES (?,?,?,?)", (pid, pid, f4, d4))
            c.execute("INSERT INTO transaction_source VALUES (?,?,?)", (pid, pid, 0))
    for pid, ident, src, d, m, a, cur, st, ty in TXNS:
        c.execute("INSERT INTO payment_transaction (pid, identifier, transaction_source_pid, transaction_date, "
                  "merchant_name, locality, amount, currency_code, transaction_status, transaction_type, "
                  "location_latitude) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (pid, ident, src, cocoa(d), m, "SYNTH CITY", a, cur, st, ty, 4.6))
    c.execute("INSERT INTO unrelated_table VALUES (1, 'SYNTH PRIVATE NOTE')")
    c.commit()
    c.close()
    return path
