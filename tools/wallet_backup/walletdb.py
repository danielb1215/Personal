"""Reads Apple Wallet card transactions from a passes23.sqlite file.

Everything that is not documented by Apple is discovered from the schema, not hard-coded:
- transactions live in `payment_transaction` (confirmed by iLEAPP on iOS 13-18);
- the link from a transaction to its card is found by following `<table>_pid` columns
  (e.g. payment_transaction.transaction_source_pid -> transaction_source.pid -> ... -> pass);
- the card name and last 4 digits are taken from whichever known column names exist
  in the tables reached that way.
Status/type codes and the integer amount scale come from wallet_codes.json, because Apple
does not document them; `probe` prints the codes seen so they can be confirmed.
"""
import collections
import hashlib
import json
import os
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation

HERE = os.path.dirname(os.path.abspath(__file__))
TXN_TABLE = "payment_transaction"
CARD_TABLE = "pass"
COCOA_EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)

CSV_COLS = ["wallet_txn_id", "date", "time", "card_name", "card_last4", "merchant", "amount", "currency",
            "status", "source", "billed_amount", "billed_currency"]

# Candidate column names, first match wins. Prefixed with the table they are looked up in.
DATE_COLS = ["transaction_date", "date", "transaction_posted_date", "location_date"]
MERCHANT_COLS = ["merchant_name", "merchant_display_name", "display_name", "merchant_raw_name", "raw_merchant_name",
                 "merchant.display_name", "merchant.name", "merchant.raw_name", "peer_payment_counterpart_handle",
                 "locality"]
CARD_NAME_COLS = ["pass.organization_name", "pass.localized_description", "pass.description", "pass.logo_text",
                  "payment_application.display_name", "payment_application.card_name"]
# fpan = the number printed on the card; dpan = the device number Apple Pay uses (fallback only)
LAST4_COLS = ["fpan_suffix", "primary_account_number_suffix", "primary_account_suffix", "pan_suffix",
              "account_suffix", "card_suffix", "suffix", "dpan_suffix"]
ID_COLS = ["identifier", "service_identifier", "unique_id", "transaction_identifier"]


def load_codes(path=None):
    with open(path or os.path.join(HERE, "wallet_codes.json")) as f:
        return json.load(f)


# ---------------------------------------------------------------- schema helpers
def tables(conn):
    return [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]


def columns(conn, table):
    return [(r[1], (r[2] or "").upper(), r[5]) for r in conn.execute(f'PRAGMA table_info("{table}")')]


def pk(conn, table):
    pks = [c for c, _, is_pk in columns(conn, table) if is_pk]
    if len(pks) == 1:
        return pks[0]
    names = [c for c, _, _ in columns(conn, table)]
    return "pid" if "pid" in names else ("Z_PK" if "Z_PK" in names else "rowid")


def fk_edges(conn):
    """Forward links: (table, column, target_table) for every `<target>_pid` / `<target>_id` column."""
    tset = set(tables(conn))
    out = []
    for t in tset:
        for c, _, _ in columns(conn, t):
            m = re.fullmatch(r"(.+?)_(pid|id|fk)", c, re.I)
            if m and m.group(1).lower() in tset and m.group(1).lower() != t:
                out.append((t, c, m.group(1).lower()))
    return out


def path_to(conn, start, goal, max_hops=4):
    """Shortest chain of joins from `start` to `goal`, following forward links and reverse links.
    Returns [(from_table, from_col, to_table, to_col), ...] or None."""
    edges = collections.defaultdict(list)
    for t, c, target in fk_edges(conn):
        edges[t].append((t, c, target, pk(conn, target)))              # t.c -> target.pk
        edges[target].append((target, pk(conn, target), t, c))         # target.pk -> t.c (reverse)
    queue, seen = collections.deque([(start, [])]), {start}
    while queue:
        cur, path = queue.popleft()
        if cur == goal:
            return path
        if len(path) >= max_hops:
            continue
        for e in edges[cur]:
            if e[2] not in seen:
                seen.add(e[2])
                queue.append((e[2], path + [e]))
    return None


# ---------------------------------------------------------------- value helpers
def to_datetime(v):
    """Wallet stores Core Data timestamps (seconds since 2001-01-01 UTC). Also accepts Unix seconds,
    milliseconds and ISO strings, in case a future iOS changes it. Returns local naive datetime."""
    if v in (None, ""):
        return None
    if isinstance(v, (bytes, str)):
        s = v.decode() if isinstance(v, bytes) else v
        try:
            v = float(s)
        except ValueError:
            try:
                d = datetime.fromisoformat(s.replace("Z", "+00:00"))
                return d.astimezone().replace(tzinfo=None) if d.tzinfo else d
            except ValueError:
                return None
    v = float(v)
    if v > 1e11:            # milliseconds
        v /= 1000.0
    if v >= 1.5e9:          # Unix seconds (2017+); Core Data seconds stay below that until 2048
        d = datetime.fromtimestamp(v, tz=timezone.utc)
    else:
        d = COCOA_EPOCH + timedelta(seconds=v)
    return d.astimezone().replace(tzinfo=None)


def to_amount(v, integer_scale):
    """Decimal strings ("12.50") and REAL values are taken as they are; integers are scaled
    (iLEAPP divides by 10000). Returns Decimal or None."""
    if v is None or v == "":
        return None
    if isinstance(v, bytes):
        try:
            v = v.decode()
        except UnicodeDecodeError:
            return None
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return Decimal(v) / Decimal(integer_scale)
    if isinstance(v, float):
        return Decimal(repr(v))
    s = str(v).strip().replace(",", "")
    if re.fullmatch(r"-?\d+", s):
        return Decimal(s) / Decimal(integer_scale)
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def amount_kind(v):
    """Storage class of an amount value, for probe (never the value itself)."""
    if v is None:
        return "null"
    if isinstance(v, int):
        return "integer" + (" (multiple of 100)" if v % 100 == 0 else "")
    if isinstance(v, float):
        return "real" + (" (whole number)" if v == int(v) else "")
    if isinstance(v, bytes):
        return "blob"
    s = str(v).strip()
    if re.fullmatch(r"-?\d+", s):
        return "text integer"
    if re.fullmatch(r"-?\d+\.\d+", s):
        return "text decimal"
    return "text other"


def pick(row, names):
    for n in names:
        if n in row and row[n] not in (None, ""):
            return row[n]
        if "." not in n:
            for k, v in row.items():
                if k.endswith("." + n) and v not in (None, ""):
                    return v
    return None


# ---------------------------------------------------------------- reading
def forward_links(conn):
    fwd = collections.defaultdict(list)
    for t, c, target in fk_edges(conn):
        fwd[t].append((c, target, pk(conn, target)))
    return fwd


def _linked_rows(conn, fwd, start_table, start_row):
    """Flat dict of start_row plus every row reachable from it by forward links (up to 3 hops).
    Keys are '<column>' for the start row and '<table>.<column>' for all."""
    flat = {f"{start_table}.{k}": v for k, v in start_row.items()}
    flat.update(start_row)
    frontier = [(start_table, start_row)]
    visited = {start_table}
    for _ in range(3):
        nxt = []
        for t, row in frontier:
            for c, target, tpk in fwd[t]:
                if target in visited or row.get(c) is None:
                    continue
                r = conn.execute(f'SELECT * FROM "{target}" WHERE "{tpk}" = ?', (row[c],)).fetchone()
                if r:
                    r = dict(r)
                    visited.add(target)
                    flat.update({f"{target}.{k}": v for k, v in r.items()})
                    nxt.append((target, r))
        frontier = nxt
    return flat


def card_info(conn):
    """{pass pk: {'card_key','card_name','card_last4'}} for every pass that looks like a payment card."""
    if CARD_TABLE not in tables(conn):
        return {}
    ppk = pk(conn, CARD_TABLE)
    apps = collections.defaultdict(list)
    tset = set(tables(conn))
    if "payment_application" in tset:
        cols = [c for c, _, _ in columns(conn, "payment_application")]
        link = next((c for c in cols if c in ("pass_pid", "pass_id")), None)
        if link:
            for r in conn.execute('SELECT * FROM payment_application'):
                r = dict(r)
                apps[r[link]].append(r)
    out = {}
    for r in conn.execute(f'SELECT * FROM "{CARD_TABLE}"'):
        r = dict(r)
        flat = {f"pass.{k}": v for k, v in r.items()}
        for a in apps.get(r[ppk], []):
            for k, v in a.items():
                flat.setdefault(f"payment_application.{k}", v)
        flat.update({k: v for k, v in r.items() if k not in flat})
        last4 = pick(flat, [f"payment_application.{c}" for c in LAST4_COLS] + [f"pass.{c}" for c in LAST4_COLS])
        name = pick(flat, CARD_NAME_COLS)
        key = pick(flat, ["pass.unique_id", "pass.serial_number", "pass.pass_type_id"]) or r[ppk]
        out[r[ppk]] = {"card_key": hashlib.sha1(str(key).encode()).hexdigest()[:8],
                       "card_name": str(name or "unknown card"),
                       "card_last4": (re.sub(r"\D", "", str(last4))[-4:] if last4 else "")}
    return out


def transaction_card_map(conn):
    """{transaction pk: pass pk} using the shortest join path, or {} if none is found."""
    path = path_to(conn, TXN_TABLE, CARD_TABLE)
    if not path:
        return {}
    tpk = pk(conn, TXN_TABLE)
    sql = f'SELECT t0."{tpk}", t{len(path)}."{pk(conn, CARD_TABLE)}" FROM "{TXN_TABLE}" t0'
    for i, (_, fcol, to_t, tcol) in enumerate(path, start=1):
        sql += f' JOIN "{to_t}" t{i} ON t{i}."{tcol}" = t{i - 1}."{fcol}"'
    out = {}
    for tid, pid in conn.execute(sql):
        out.setdefault(tid, pid)
    return out


def connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def read_transactions(conn, codes, since=None):
    """Yields dicts with CSV_COLS (amount as Decimal, signed: money out negative) plus '_status_code',
    '_type_code' and '_card_key'. Declined rows are included with status 'declined'; the caller skips them."""
    if TXN_TABLE not in tables(conn):
        raise SystemExit(f"table {TXN_TABLE} not found in this database - run `probe` and send the output")
    scale = int(codes.get("amount_integer_scale", 10000))
    status_map = {str(k): v for k, v in codes.get("status", {}).items() if not k.startswith("_")}
    refund_types = {str(x) for x in codes.get("refund_types", [])}
    skip_types = {str(x) for x in codes.get("skip_types", [])}
    cards = card_info(conn)
    tmap = transaction_card_map(conn)
    fwd = forward_links(conn)
    tpk = pk(conn, TXN_TABLE)
    tcols = [c for c, _, _ in columns(conn, TXN_TABLE)]
    alt = [(c, c[:-len("amount")] + "currency_code") for c in tcols
           if c.endswith("_amount") and c[:-len("amount")] + "currency_code" in tcols]
    for r in conn.execute(f'SELECT *, "{tpk}" AS _pk FROM "{TXN_TABLE}"').fetchall():
        r = dict(r)
        flat = _linked_rows(conn, fwd, TXN_TABLE, r)
        when = to_datetime(pick(flat, DATE_COLS))
        if when is None or (since and when.date() < since):
            continue
        status_code = r.get("transaction_status")
        type_code = r.get("transaction_type")
        if str(type_code) in skip_types:
            continue
        status = status_map.get(str(status_code), "unknown")
        amt = to_amount(r.get("amount"), scale)
        if amt is None:
            continue
        # Wallet shows purchases as positive amounts; the ledger wants money out negative.
        is_refund = str(type_code) in refund_types or amt < 0
        signed = abs(amt) if is_refund else -abs(amt)
        if status not in ("declined", "unknown") and is_refund:
            status = "refund"
        card = cards.get(tmap.get(r["_pk"]), {"card_key": "", "card_name": "unknown card", "card_last4": ""})
        ident = pick(r, ID_COLS)
        if ident is None:   # not stable if a pending amount changes; documented in README
            ident = f"{card['card_key']}|{when.isoformat()}|{pick(flat, MERCHANT_COLS)}|{amt}"
        billed_amt, billed_cur = "", ""
        cur = (r.get("currency_code") or "").upper()
        for ac, cc in alt:
            a2, c2 = to_amount(r.get(ac), scale), (r.get(cc) or "").upper()
            if a2 is not None and c2 and c2 != cur:
                billed_amt, billed_cur = (abs(a2) if is_refund else -abs(a2)), c2
                break
        yield {
            "wallet_txn_id": "APW-" + hashlib.sha1(str(ident).encode()).hexdigest()[:12],
            "date": when.date().isoformat(),
            "time": when.strftime("%H:%M:%S"),
            "card_name": card["card_name"],
            "card_last4": card["card_last4"],
            "merchant": str(pick(flat, MERCHANT_COLS) or "").strip(),
            "amount": signed,
            "currency": cur,
            "status": status,
            "source": "apple_wallet",
            "billed_amount": billed_amt,
            "billed_currency": billed_cur,
            "_status_code": status_code,
            "_type_code": type_code,
            "_card_key": card["card_key"],
        }


# ---------------------------------------------------------------- probe (schema + counts only)
LOW_CARD_HINT = re.compile(r"status|type|kind|source|currency|category|flags|is_|has_|method|network|mode", re.I)
SAFE_TEXT = re.compile(r"currency_code|status|type$|kind$", re.I)
NEVER_SHOW = re.compile(r"amount|balance|price|total|lat|long|alt|date|time|name|handle|memo|ident|url|number|"
                        r"suffix|address|phone|email|note|desc|merchant|local|area|city|zip|postal", re.I)


def probe_report(conn, codes, card_label=True):
    """Schema, row counts and per-card counts/date ranges. Never prints amounts, merchants,
    locations, names of people or any free-text value."""
    L = []
    tl = tables(conn)
    L.append(f"tables: {len(tl)}")
    for t in tl:
        n = conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        cols = ", ".join(f"{c} {ty}".strip() + (" PK" if p else "") for c, ty, p in columns(conn, t))
        L.append(f"- {t} [{n} rows]: {cols}")
    L.append("")
    L.append("links found (<table>.<column> -> <table>):")
    for t, c, target in sorted(fk_edges(conn)):
        L.append(f"- {t}.{c} -> {target}")
    path = path_to(conn, TXN_TABLE, CARD_TABLE) if TXN_TABLE in tl and CARD_TABLE in tl else None
    L.append(f"transaction -> card path: " + (" / ".join(f"{a}.{b}={c}.{d}" for a, b, c, d in path) if path else "NOT FOUND"))
    L.append("")
    for t in [x for x in tl if "transaction" in x.lower()]:
        n = conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        L.append(f"## {t} ({n} rows)")
        if not n:
            continue
        for c, ty, _ in columns(conn, t):
            if not LOW_CARD_HINT.search(c) or (NEVER_SHOW.search(c) and not SAFE_TEXT.search(c)):
                continue
            vals = conn.execute(f'SELECT "{c}", COUNT(*) FROM "{t}" GROUP BY 1 ORDER BY 2 DESC LIMIT 13').fetchall()
            if len(vals) > 12:
                L.append(f"  {c}: more than 12 distinct values")
                continue
            if any(isinstance(v, str) for v, _ in vals) and not SAFE_TEXT.search(c):
                L.append(f"  {c}: {len(vals)} distinct text values (not shown)")
                continue
            L.append(f"  {c}: " + ", ".join(f"{v!r}={k}" for v, k in vals))
        if "amount" in [c for c, _, _ in columns(conn, t)]:
            kinds = collections.Counter(amount_kind(v) for (v,) in conn.execute(f'SELECT amount FROM "{t}"'))
            L.append("  amount storage: " + ", ".join(f"{k}={v}" for k, v in kinds.most_common()))
        if t != TXN_TABLE:
            continue
        rows = list(read_transactions(conn, codes))
        by_card = collections.defaultdict(list)
        for r in rows:
            label = (f"{r['card_name']} ..{r['card_last4']}" if card_label else "") + f" [card {r['_card_key'] or '?'}]"
            by_card[label.strip()].append(r)
        L.append(f"  readable transactions: {len(rows)} of {n}")
        for label, rs in sorted(by_card.items()):
            ds = sorted(r["date"] for r in rs)
            st = collections.Counter(r["status"] for r in rs)
            cur = collections.Counter(r["currency"] for r in rs)
            L.append(f"  card {label}: {len(rs)} txns, {ds[0]} to {ds[-1]}; status "
                     + ", ".join(f"{k}={v}" for k, v in sorted(st.items()))
                     + "; currency " + ", ".join(f"{k}={v}" for k, v in sorted(cur.items())))
            per_month = collections.Counter(d[:7] for d in ds)
            L.append("    per month: " + ", ".join(f"{m}={k}" for m, k in sorted(per_month.items())[-12:]))
            codes_seen = collections.Counter((r["_status_code"], r["_type_code"]) for r in rs)
            L.append("    (status code, type code): " + ", ".join(f"{k}={v}" for k, v in sorted(codes_seen.items(), key=str)))
    return "\n".join(L)
