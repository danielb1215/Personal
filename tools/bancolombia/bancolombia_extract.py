#!/usr/bin/env python3
"""Unlock and parse password-protected Bancolombia PDF statements.

Runs locally. The password comes from the BANCOLOMBIA_PDF_PASSWORD env var or
an interactive getpass prompt; it is never accepted as an argument, printed,
logged or written anywhere.

Outputs (under --output):
  unlocked/              password-free copies of each PDF (same filename)
  text/                  raw text dump per PDF (+ layout/table dumps with --dump-text)
  transactions.csv       one row per parsed movement
  statements.csv         one row per PDF (per currency section) with reconciliation
  unparsed_lines.csv     lines that look like movements but did not parse

Adding a new layout: subclass BaseParser (see SavingsParser / CreditCardParser),
implement detect(), map_header(), fields_from_cells(), fields_from_line(),
signed_amount() and reconcile(), then append it to PARSERS.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import getpass
import hashlib
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path

PASSWORD_ENV = "BANCOLOMBIA_PDF_PASSWORD"
TOLERANCE = Decimal("1.00")

TXN_COLUMNS = [
    "txn_id", "date", "account", "account_type", "currency", "amount", "description",
    "branch", "document_ref", "balance_after", "statement_period_start",
    "statement_period_end", "source_file", "page", "parse_confidence", "raw_line",
    # extra card columns (empty for savings)
    "installment", "original_amount", "rate_ea",
]
STATEMENT_COLUMNS = [
    "source_file", "account", "account_type", "parser", "currency",
    "statement_period_start", "statement_period_end",
    "opening_balance", "closing_balance", "printed_total_debits", "printed_total_credits",
    "parsed_total_debits", "parsed_total_credits", "parsed_net", "n_transactions",
    "n_unparsed", "reconciles", "unlocked", "error",
]
UNPARSED_COLUMNS = ["source_file", "page", "line_index", "currency", "raw_line"]
UNIFIED_COLUMNS = [
    "txn_id", "date", "account", "currency", "amount", "flow_type", "category",
    "description", "counterparty", "match_id", "match_account", "est_other_ccy",
    "is_duplicate", "needs_review", "notes", "source_file",
]

# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def norm(text: str) -> str:
    """Upper-case, accent-free, single-spaced text for keyword matching."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text).strip().upper()


def prep_line(line: str) -> str:
    """Glue '$ 1,000.00' -> '$1,000.00' and '- 5.00' -> '-5.00' so amounts are one token."""
    line = (line or "").replace("−", "-").replace("\xa0", " ")
    line = re.sub(r"\$\s+", "$", line)
    line = re.sub(r"(?<!\S)-\s+(?=[$\d])", "-", line)
    return re.sub(r"\s+", " ", line).strip()


def parse_amount(text) -> Decimal | None:
    """Parse '1,234,567.89', '1.234.567,89', '-50,000.00', '$ 1.000', '(12.00)', '5.00-'."""
    if text is None:
        return None
    s = str(text).strip().replace("−", "-")
    s = re.sub(r"(?i)\s|\$|COP|USD", "", s)
    if not s:
        return None
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg, s = True, s[1:-1]
    if s.endswith("-"):
        neg, s = True, s[:-1]
    if s.startswith("-"):
        neg, s = True, s[1:]
    elif s.startswith("+"):
        s = s[1:]
    if not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        return None
    last_dot, last_comma = s.rfind("."), s.rfind(",")
    if last_dot >= 0 and last_comma >= 0:
        dec = "." if last_dot > last_comma else ","
    elif last_comma >= 0:
        dec = None if re.fullmatch(r"\d{1,3}(,\d{3})+", s) else ","
    elif last_dot >= 0:
        dec = None if re.fullmatch(r"\d{1,3}(\.\d{3})+", s) else "."
    else:
        dec = None
    if dec:
        thousands = "," if dec == "." else "."
        int_part, _, frac = s.rpartition(dec)
        int_part = int_part.replace(thousands, "")
        if dec in int_part or not frac:
            return None
        s = f"{int_part or '0'}.{frac}"
    else:
        s = s.replace(",", "").replace(".", "")
    try:
        value = Decimal(s)
    except InvalidOperation:
        return None
    return -value if neg else value


def fmt_amount(value: Decimal | None) -> str:
    return "" if value is None else f"{value:.2f}"


# A printed money amount always has exactly two decimals in Bancolombia statements.
MONEY_TOKEN = re.compile(r"^\(?[-+]?\$?[-+]?(?:\d{1,3}(?:[.,]\d{3})+|\d+)[.,]\d{2}-?\)?$")
MONEY_IN_TEXT = re.compile(r"[-+]?\$?\s?(?:\d{1,3}(?:[.,]\d{3})+|\d+)[.,]\d{2}(?!\d)-?")
PCT_TOKEN = re.compile(r"^\d{1,3}[.,]\d{1,6}%$|^\d{1,3}[.,]\d{3,6}$")
CUOTA_TOKEN = re.compile(r"^\d{1,3}/\d{1,3}$")
INT_TOKEN = re.compile(r"^\d{1,12}$")
DATE_TOKEN = re.compile(
    r"^(?:\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)$"
)
TXN_LIKE = re.compile(
    r"^(?:[A-Z0-9]{3,10}\s+)?(?:\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)\s.*"
    r"(?:\d{1,3}(?:[.,]\d{3})+|\d+)[.,]\d{2}(?!\d)",
    re.I,
)

MONTHS = {
    "ENE": 1, "JAN": 1, "FEB": 2, "MAR": 3, "ABR": 4, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AGO": 8, "AUG": 8, "SEP": 9, "SET": 9, "OCT": 10, "NOV": 11, "DIC": 12, "DEC": 12,
}
_DATE_NUM = r"\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
_DATE_TXT = r"\d{1,2}\s*(?:DE\s+)?[A-Z]{3,10}\.?\s*(?:DE\s+|DEL\s+)?\d{4}"
DATE_ANY = rf"(?:{_DATE_NUM}|{_DATE_TXT})"


def parse_full_date(text: str) -> dt.date | None:
    """Parse a date that carries its own year (several numeric and Spanish formats)."""
    s = norm(text)
    try:
        m = re.fullmatch(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", s)
        if m:
            return dt.date(int(m[1]), int(m[2]), int(m[3]))
        m = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", s)
        if m:
            year = int(m[3]) + (2000 if len(m[3]) == 2 else 0)
            return dt.date(year, int(m[2]), int(m[1]))
        m = re.fullmatch(r"(\d{1,2})\s*(?:DE\s+)?([A-Z]{3,10})\.?\s*(?:DE\s+|DEL\s+)?(\d{4})", s)
        if m and m[2][:3] in MONTHS:
            return dt.date(int(m[3]), MONTHS[m[2][:3]], int(m[1]))
    except ValueError:
        return None
    return None


def find_period(text: str) -> tuple[dt.date | None, dt.date | None]:
    """Find the statement period (DESDE/HASTA, PERIODO ... AL ..., or FECHA DE CORTE)."""
    t = norm(text)
    patterns = [
        rf"DESDE\W{{0,5}}({DATE_ANY})\W{{0,5}}HASTA\W{{0,5}}({DATE_ANY})",
        rf"PERIODO(?: FACTURADO)?\W{{0,5}}(?:DEL?|DESDE)?\W{{0,3}}({DATE_ANY})\W{{0,5}}(?:AL|A|HASTA|-)\W{{0,3}}({DATE_ANY})",
    ]
    for pat in patterns:
        m = re.search(pat, t)
        if m:
            start, end = parse_full_date(m[1]), parse_full_date(m[2])
            if start and end and start <= end:
                return start, end
    m = re.search(rf"FECHA DE CORTE\W{{0,5}}({DATE_ANY})", t)
    if m:
        end = parse_full_date(m[1])
        if end:
            prev_month_end = end.replace(day=1) - dt.timedelta(days=1)
            start_day = min(end.day, prev_month_end.day)
            return prev_month_end.replace(day=start_day) + dt.timedelta(days=1), end
    return None, None


def currency_header(line: str) -> str | None:
    """Return 'USD'/'COP' if the line is a section header announcing a currency."""
    if MONEY_IN_TEXT.search(line) or len(line) > 80:
        return None
    n = norm(line)
    if re.search(r"\b(DOLARES|USD|US\$|MONEDA EXTRANJERA)\b", n):
        return "USD"
    if re.search(r"\b(PESOS|COP|MONEDA LEGAL)\b", n):
        return "COP"
    return None


def last_currency_header(lines) -> str | None:
    found = None
    for line in lines:
        found = currency_header(line) or found
    return found


# --------------------------------------------------------------------------
# Filename / account helpers
# --------------------------------------------------------------------------

FILENAME_RE = re.compile(
    r"^(?P<year>\d{4})-(?P<month>\d{2})_Bancolombia_"
    r"(?P<type>CuentaAhorros|Visa|AmericanExpress|MasterCard|Extracto)_(?P<last4>\d{4})\.pdf$",
    re.I,
)
# filename type -> (account_type, brand)
FILE_TYPES = {
    "cuentaahorros": ("savings", ""),
    "visa": ("credit_card", "Visa"),
    "mastercard": ("credit_card", "Mastercard"),
    "americanexpress": ("credit_card", "Amex"),
    "extracto": ("", ""),
}


@dataclass
class FileInfo:
    year: int
    month: int
    file_type: str  # as in filename, e.g. "CuentaAhorros"
    account_type: str  # "savings" | "credit_card" | "" (unknown)
    brand: str
    last4: str


def parse_filename(name: str) -> FileInfo | None:
    m = FILENAME_RE.match(Path(name).name)
    if not m:
        return None
    account_type, brand = FILE_TYPES[m["type"].lower()]
    return FileInfo(int(m["year"]), int(m["month"]), m["type"], account_type, brand, m["last4"])


def detect_brand(norm_text: str) -> str:
    if re.search(r"AMERICAN EXPRESS|\bAMEX\b", norm_text):
        return "Amex"
    if re.search(r"MASTER ?CARD", norm_text):
        return "Mastercard"
    if re.search(r"\bVISA\b", norm_text):
        return "Visa"
    return ""


def detect_last4(norm_text: str) -> str:
    patterns = [
        r"(?:\*|X){2,}[\s*X-]*(\d{4})\b",
        r"(?:CUENTA|TARJETA)[A-Z ]{0,20}(?:NO\.?|NUMERO|NRO\.?|N°)?\s*:?\s*([\d -]{6,})",
        r"NUMERO\s*:?\s*([\d-]{6,})",
    ]
    for pat in patterns:
        m = re.search(pat, norm_text)
        if m:
            digits = re.sub(r"\D", "", m[1])
            if len(digits) >= 4:
                return digits[-4:]
    return ""


def account_label(account_type: str, brand: str, last4: str) -> str:
    if account_type == "savings":
        kind = "savings"
    elif account_type == "credit_card":
        kind = brand or "credit card"
    else:
        kind = "account"
    return f"Bancolombia {kind} {last4}".strip()


def txn_id(source_file: str, page: int, key: str) -> str:
    return hashlib.sha1(f"{source_file}|{page}|{key}".encode()).hexdigest()[:16]


# --------------------------------------------------------------------------
# PDF access
# --------------------------------------------------------------------------


class PasswordProvider:
    """Asks for the password lazily (only if some PDF is encrypted) and caches it in memory."""

    def __init__(self):
        self._password: str | None = None

    def get(self) -> str:
        if self._password is None:
            pw = os.environ.get(PASSWORD_ENV)
            if not pw:
                pw = getpass.getpass("Bancolombia PDF password (input hidden): ")
            self._password = pw
        return self._password


def unlock_pdf(src: Path, dst: Path, passwords: PasswordProvider) -> None:
    """Write a password-free copy of src to dst. Raises ValueError on a wrong password."""
    import pikepdf

    try:
        pdf = pikepdf.open(src)
    except pikepdf.PasswordError:
        try:
            pdf = pikepdf.open(src, password=passwords.get())
        except pikepdf.PasswordError:
            raise ValueError("wrong password (or PDF uses a different password)") from None
    dst.parent.mkdir(parents=True, exist_ok=True)
    with pdf:
        pdf.save(dst)  # saving without an `encryption` argument drops encryption


@dataclass
class TableData:
    rows: list
    text_above: list  # lines printed above the table on the same page


@dataclass
class PageData:
    number: int
    text: str
    lines: list
    tables: list


def read_pages(path: Path) -> list[PageData]:
    import pdfplumber

    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            tables = []
            try:
                for table in page.find_tables():
                    top = table.bbox[1]
                    above = page.crop((0, 0, page.width, top)).extract_text() if top > 1 else ""
                    tables.append(TableData(table.extract(), (above or "").splitlines()))
            except Exception:  # table detection is best-effort
                tables = []
            pages.append(PageData(i, text, text.splitlines(), tables))
    return pages


def dump_text(path: Path, pages: list[PageData], out_dir: Path, extended: bool) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    with open(out_dir / f"{stem}.txt", "w", encoding="utf-8") as fh:
        for p in pages:
            fh.write(f"===== page {p.number} =====\n{p.text}\n")
    if not extended:
        return
    import pdfplumber

    with pdfplumber.open(path) as pdf, open(out_dir / f"{stem}.layout.txt", "w", encoding="utf-8") as fh:
        for i, page in enumerate(pdf.pages, start=1):
            fh.write(f"===== page {i} (layout) =====\n{page.extract_text(layout=True) or ''}\n")
    with open(out_dir / f"{stem}.tables.txt", "w", encoding="utf-8") as fh:
        for p in pages:
            for t_idx, table in enumerate(p.tables):
                fh.write(f"===== page {p.number} table {t_idx} =====\n")
                for row in table.rows:
                    fh.write(" | ".join("" if c is None else str(c).replace("\n", " ") for c in row) + "\n")


# --------------------------------------------------------------------------
# Parsing core
# --------------------------------------------------------------------------


@dataclass
class Txn:
    date: dt.date | None
    amount: Decimal
    description: str
    currency: str
    page: int
    key: str
    confidence: str
    raw_line: str
    branch: str = ""
    document_ref: str = ""
    balance_after: Decimal | None = None
    installment: str = ""
    original_amount: Decimal | None = None
    rate_ea: str = ""
    debt_delta: Decimal | None = None  # card only: change in total debt caused by this row


@dataclass
class ParseResult:
    txns: list = field(default_factory=list)
    unparsed: list = field(default_factory=list)  # (page, line_index, currency, raw)
    summaries: dict = field(default_factory=dict)  # currency -> {opening, closing, debits, credits}
    warnings: list = field(default_factory=list)


@dataclass
class StatementContext:
    source_file: str
    pages: list
    full_text: str
    norm_text: str
    info: FileInfo | None
    period_start: dt.date | None
    period_end: dt.date | None

    def resolve_date(self, token: str) -> tuple[dt.date | None, bool]:
        """Return (date, confident). Handles d/mm without year using the statement period."""
        full = parse_full_date(token)
        if full:
            return full, True
        m = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})", token.strip())
        if not m:
            return None, False
        day, month = int(m[1]), int(m[2])
        if self.period_start and self.period_end:
            best, best_dist = None, None
            for year in range(self.period_start.year - 1, self.period_end.year + 2):
                try:
                    d = dt.date(year, month, day)
                except ValueError:
                    continue
                if self.period_start <= d <= self.period_end:
                    dist = 0
                else:
                    dist = min(abs((d - self.period_start).days), abs((d - self.period_end).days))
                if best_dist is None or dist < best_dist:
                    best, best_dist = d, dist
            return best, best is not None and best_dist <= 31
        if self.info:
            year = self.info.year - (1 if month > self.info.month else 0)
            try:
                return dt.date(year, month, day), False
            except ValueError:
                return None, False
        return None, False


def split_line(line: str):
    """Split '[auth] DATE description ... trailing numeric tokens'.

    Returns (auth, date_token, description, tail) where tail is a list of
    (kind, token) with kind in money/pct/cuota/int, or None if no leading date.
    """
    tokens = line.split()
    if len(tokens) < 3:
        return None
    i, auth = 0, ""
    if (re.fullmatch(r"[A-Z0-9]{3,10}", tokens[0], re.I) and not DATE_TOKEN.match(tokens[0])
            and DATE_TOKEN.match(tokens[1])):
        auth, i = tokens[0], 1
    if not DATE_TOKEN.match(tokens[i]):
        return None
    date_token = tokens[i]
    i += 1
    tail, j = [], len(tokens)
    while j > i:
        t = tokens[j - 1]
        if MONEY_TOKEN.match(t):
            kind = "money"
        elif PCT_TOKEN.match(t):
            kind = "pct"
        elif CUOTA_TOKEN.match(t):
            kind = "cuota"
        elif INT_TOKEN.match(t):
            kind = "int"
        else:
            break
        tail.insert(0, (kind, t))
        j -= 1
    return auth, date_token, " ".join(tokens[i:j]), tail


def clean_cell(cell) -> str:
    return re.sub(r"\s+", " ", "" if cell is None else str(cell)).strip()


class BaseParser:
    """One subclass per statement layout. Subclasses override the hooks below."""

    name = "base"
    account_type = ""
    summary_labels: dict = {}  # key -> list of regexes in priority order

    @classmethod
    def detect(cls, ctx: StatementContext) -> int:
        """Return a score; the highest-scoring parser handles the statement."""
        return 0

    # --- hooks -----------------------------------------------------------
    def map_header(self, cells: list[str]) -> dict | None:
        """Map table header cells -> {field: column index}; None if not a movement header."""
        return None

    def fields_from_cells(self, cells: list[str], mapping: dict) -> dict | None:
        return None

    def fields_from_line(self, line: str) -> dict | None:
        return None

    def signed_amount(self, fields: dict) -> Decimal | None:
        return fields.get("amount")

    def postprocess(self, res: ParseResult) -> None:
        pass

    def reconcile(self, currency: str, txns: list, summary: dict) -> tuple[str, list]:
        return "unknown", []

    # --- shared machinery --------------------------------------------------
    def parse(self, ctx: StatementContext) -> ParseResult:
        res = ParseResult()
        currency = "COP"
        for page in ctx.pages:
            page_txns = []
            for t_idx, table in enumerate(page.tables):
                cur = last_currency_header(table.text_above) or currency
                page_txns += self._parse_table(table.rows, ctx, page.number, t_idx, cur)
            if page_txns:
                res.txns += page_txns
            else:
                cur = currency
                for idx, raw in enumerate(page.lines):
                    line = prep_line(raw)
                    if not line:
                        continue
                    header = currency_header(line)
                    if header:
                        cur = header
                        continue
                    txn = None
                    fields = self.fields_from_line(line)
                    if fields:
                        txn = self._build(fields, ctx, page.number, f"l{idx}", cur, "medium", raw)
                    if txn:
                        res.txns.append(txn)
                    elif TXN_LIKE.match(line):
                        res.unparsed.append((page.number, idx, cur, raw))
            currency = last_currency_header(page.lines) or currency
        res.summaries = self.extract_summaries(ctx)
        self.postprocess(res)
        return res

    def _parse_table(self, rows, ctx, page_no, t_idx, currency) -> list:
        out, mapping = [], None
        for r_idx, row in enumerate(rows):
            cells = [clean_cell(c) for c in row]
            header = self.map_header(cells)
            if header:
                mapping = header
                continue
            if mapping is None or not any(cells):
                continue
            fields = self.fields_from_cells(cells, mapping)
            if fields:
                txn = self._build(fields, ctx, page_no, f"t{t_idx}r{r_idx}", currency, "high",
                                  " | ".join(cells))
                if txn:
                    out.append(txn)
        return out

    def _build(self, fields, ctx, page_no, key, currency, confidence, raw) -> Txn | None:
        date, sure = ctx.resolve_date(fields.get("date", ""))
        amount = self.signed_amount(fields)
        if date is None or amount is None:
            return None
        if not sure or fields.get("guessed"):
            confidence = "low"
        return Txn(
            date=date, amount=amount, description=fields.get("description", ""),
            currency=currency, page=page_no, key=key, confidence=confidence, raw_line=raw,
            branch=fields.get("branch", ""), document_ref=fields.get("document_ref", ""),
            balance_after=fields.get("balance"), installment=fields.get("installment", ""),
            original_amount=fields.get("original_amount"), rate_ea=fields.get("rate_ea", ""),
            debt_delta=fields.get("debt_delta"),
        )

    def extract_summaries(self, ctx: StatementContext) -> dict:
        """Find printed totals (opening/closing/debits/credits) per currency section."""
        tagged, cur = [], "COP"
        for page in ctx.pages:
            for raw in page.lines:
                line = prep_line(raw)
                cur = currency_header(line) or cur
                tagged.append((cur, norm(line)))
        out: dict = {}
        # Case 1: "LABEL ... $1,234.56" on one line
        for key, patterns in self.summary_labels.items():
            for pat in patterns:
                rx = re.compile(rf"^[+\-=:\s]*(?:{pat})\b[^0-9$\-]{{0,40}}?({MONEY_IN_TEXT.pattern})")
                for cur, line in tagged:
                    if key in out.get(cur, {}) or DATE_TOKEN.match(line.split(" ")[0] if line else ""):
                        continue
                    m = rx.search(line)
                    if m:
                        out.setdefault(cur, {})[key] = parse_amount(m[1])
        # Case 2: a header line with several labels and the values on the next line
        for i in range(len(tagged) - 1):
            cur, line = tagged[i]
            if MONEY_IN_TEXT.search(line):
                continue
            hits = []
            for key, patterns in self.summary_labels.items():
                for pat in patterns:
                    m = re.search(rf"\b(?:{pat})\b", line)
                    if m:
                        hits.append((m.start(), key))
                        break
            if len(hits) < 2:
                continue
            values = MONEY_IN_TEXT.findall(tagged[i + 1][1])
            if len(values) == len(hits):
                for (_, key), value in zip(sorted(hits), values):
                    out.setdefault(cur, {}).setdefault(key, parse_amount(value))
        return out


class SavingsParser(BaseParser):
    """Estado de cuenta - Cuenta de Ahorros (quarterly). Columns:
    FECHA (d/mm) | DESCRIPCIÓN | SUCURSAL | DCTO. | VALOR | SALDO."""

    name = "savings"
    account_type = "savings"
    summary_labels = {
        "opening": [r"SALDO ANTERIOR"],
        "credits": [r"TOTAL ABONOS", r"ABONOS", r"TOTAL CREDITOS"],
        "debits": [r"TOTAL CARGOS", r"CARGOS", r"TOTAL DEBITOS"],
        "closing": [r"SALDO ACTUAL", r"SALDO FINAL", r"NUEVO SALDO"],
    }

    @classmethod
    def detect(cls, ctx):
        score = 100 if ctx.info and ctx.info.account_type == "savings" else 0
        t = ctx.norm_text
        score += 20 * bool(re.search(r"CUENTA DE AHORROS|AHORROS", t))
        score += 5 * bool(re.search(r"\bSUCURSAL\b", t)) + 5 * bool(re.search(r"\bDCTO\b", t))
        return score

    def map_header(self, cells):
        mapping = {}
        for i, cell in enumerate(cells):
            c = norm(cell)
            if not c:
                continue
            if c.startswith("FECHA") and "date" not in mapping:
                mapping["date"] = i
            elif "DESCRIP" in c:
                mapping["description"] = i
            elif "SUCURSAL" in c or "OFICINA" in c:
                mapping["branch"] = i
            elif c.startswith("DCTO") or "DOCUMENTO" in c:
                mapping["document_ref"] = i
            elif c.startswith("VALOR"):
                mapping["amount"] = i
            elif c.startswith("SALDO"):
                mapping["balance"] = i
        return mapping if {"date", "amount"} <= mapping.keys() else None

    def fields_from_cells(self, cells, mapping):
        get = lambda k: cells[mapping[k]] if k in mapping and mapping[k] < len(cells) else ""
        if not DATE_TOKEN.match(get("date")):
            return None
        amount = parse_amount(get("amount"))
        if amount is None:
            return None
        return {
            "date": get("date"), "description": get("description"), "branch": get("branch"),
            "document_ref": get("document_ref"), "amount": amount,
            "balance": parse_amount(get("balance")),
        }

    def fields_from_line(self, line):
        parts = split_line(line)
        if not parts:
            return None
        _, date_token, desc, tail = parts
        money = [t for k, t in tail if k == "money"]
        if not money or not desc or any(k in ("pct", "cuota") for k, _ in tail):
            return None
        ints = [t for k, t in tail if k == "int"]
        amount_tok, balance_tok = (money[-2], money[-1]) if len(money) >= 2 else (money[0], None)
        return {
            "date": date_token, "description": desc, "document_ref": ints[-1] if ints else "",
            "amount": parse_amount(amount_tok), "balance": parse_amount(balance_tok),
        }

    def postprocess(self, res):
        """Use the running SALDO column to verify (and if needed flip) each row's sign."""
        by_cur: dict = {}
        for t in res.txns:
            by_cur.setdefault(t.currency, []).append(t)
        for cur, txns in by_cur.items():
            prev = res.summaries.get(cur, {}).get("opening")
            mismatches = 0
            for t in txns:
                if t.balance_after is None:
                    prev = None
                    continue
                if prev is not None:
                    if abs(prev + t.amount - t.balance_after) <= TOLERANCE:
                        pass
                    elif abs(prev - t.amount - t.balance_after) <= TOLERANCE:
                        t.amount = -t.amount
                        t.confidence = "low"
                    else:
                        t.confidence = "low"
                        mismatches += 1
                prev = t.balance_after
            if mismatches:
                res.warnings.append(f"{cur}: {mismatches} row(s) disagree with the running SALDO column")

    def reconcile(self, currency, txns, summary):
        notes = []
        opening, closing = summary.get("opening"), summary.get("closing")
        net = sum((t.amount for t in txns), Decimal(0))
        credits = sum((t.amount for t in txns if t.amount > 0), Decimal(0))
        debits = -sum((t.amount for t in txns if t.amount < 0), Decimal(0))
        if summary.get("credits") is not None and abs(abs(summary["credits"]) - credits) > TOLERANCE:
            notes.append(f"{currency}: printed credits {summary['credits']} != parsed {credits}")
        if summary.get("debits") is not None and abs(abs(summary["debits"]) - debits) > TOLERANCE:
            notes.append(f"{currency}: printed debits {summary['debits']} != parsed {debits}")
        if opening is None or closing is None:
            return "unknown", notes + [f"{currency}: opening/closing balance not found"]
        if abs(opening + net - closing) <= TOLERANCE:
            return "yes", notes
        return "no", notes + [f"{currency}: opening {opening} + movements {net} != closing {closing}"]


CARD_CREDIT_WORDS = re.compile(r"\b(ABONO|PAGO|PAGOS|DEVOLUCION|REVERSO|REVERSION|NOTA CREDITO|AJUSTE A FAVOR)\b")


class CreditCardParser(BaseParser):
    """Visa / Mastercard / Amex monthly statement. Columns roughly:
    Nº autorización | Fecha | Descripción | Valor original | Tasa pactada |
    Tasa EA facturada | Cargos y abonos | Saldo a diferir | Cuotas."""

    name = "credit_card"
    account_type = "credit_card"
    summary_labels = {
        "opening": [r"SALDO ANTERIOR"],
        "debits": [r"TOTAL CARGOS", r"COMPRAS(?: DEL (?:MES|PERIODO))?", r"CARGOS(?: DEL (?:MES|PERIODO))?"],
        "credits": [r"PAGOS(?: Y ABONOS)?", r"TOTAL ABONOS", r"ABONOS"],
        "closing": [r"SALDO TOTAL", r"DEUDA TOTAL", r"NUEVO SALDO", r"SALDO ACTUAL",
                    r"SALDO A LA FECHA", r"PAGO TOTAL"],
    }

    @classmethod
    def detect(cls, ctx):
        score = 100 if ctx.info and ctx.info.account_type == "credit_card" else 0
        t = ctx.norm_text
        score += 20 * bool(re.search(r"TARJETA DE CREDITO", t))
        score += 10 * bool(detect_brand(t))
        score += 5 * bool(re.search(r"PAGO MINIMO|CUPO|TASA (?:PACTADA|EA)|SALDO A DIFERIR", t))
        return score

    def map_header(self, cells):
        mapping = {}
        for i, cell in enumerate(cells):
            c = norm(cell)
            if not c:
                continue
            if "AUTORIZ" in c:
                mapping["auth"] = i
            elif "FECHA" in c and "date" not in mapping:
                mapping["date"] = i
            elif "DESCRIP" in c:
                mapping["description"] = i
            elif "VALOR ORIGINAL" in c or c == "VALOR":
                mapping["original_amount"] = i
            elif "PACTADA" in c:
                mapping["rate"] = i
            elif "EA" in c.split() or "FACTURADA" in c:
                mapping["rate_ea"] = i
            elif "CARGOS" in c or "ABONOS" in c:
                mapping["amount"] = i
            elif "DIFERIR" in c:
                mapping["deferred"] = i
            elif "CUOTA" in c:
                mapping["installment"] = i
        if "amount" not in mapping and "original_amount" in mapping:
            mapping["amount"] = mapping["original_amount"]
        return mapping if {"date", "amount"} <= mapping.keys() else None

    def fields_from_cells(self, cells, mapping):
        get = lambda k: cells[mapping[k]] if k in mapping and mapping[k] < len(cells) else ""
        if not DATE_TOKEN.match(get("date")):
            return None
        amount = parse_amount(get("amount"))
        if amount is None:
            return None
        return self._fields(get("date"), get("description"), amount,
                            parse_amount(get("original_amount")), get("rate_ea"),
                            parse_amount(get("deferred")), get("installment"), get("auth"))

    def fields_from_line(self, line):
        parts = split_line(line)
        if not parts:
            return None
        auth, date_token, desc, tail = parts
        if not desc or not any(k == "money" for k, _ in tail):
            return None
        kinds = [k for k, _ in tail]
        installment = next((t for k, t in tail if k == "cuota"), "")
        pcts = [t for k, t in tail if k == "pct"]
        if pcts:
            first_pct = kinds.index("pct")
            before = [t for k, t in tail[:first_pct] if k == "money"]
            after = [t for k, t in tail[first_pct:] if k == "money"]
            original = before[0] if before else None
            charge = after[0] if after else (before[-1] if before else None)
            deferred = after[1] if len(after) > 1 else None
        else:
            money = [t for k, t in tail if k == "money"]
            original, charge, deferred = None, money[0], None
            if len(money) >= 2:
                original, charge = money[0], money[1]
            if len(money) >= 3:
                deferred = money[2]
        amount = parse_amount(charge)
        if amount is None:
            return None
        return self._fields(date_token, desc, amount, parse_amount(original),
                            pcts[-1] if pcts else "", parse_amount(deferred), installment, auth)

    @staticmethod
    def _fields(date, desc, printed, original, rate_ea, deferred, installment, auth):
        credit = printed < 0 or bool(CARD_CREDIT_WORDS.search(norm(desc)))
        # Debt delta: a first installment of a deferred purchase adds the full original
        # value to the debt; later installments only move deferred debt to billed.
        debt_delta = abs(printed) * (-1 if credit else 1)
        m = re.fullmatch(r"(\d+)/(\d+)", installment or "")
        if m and not credit and int(m[2]) > 1:
            debt_delta = (abs(original) if original is not None else abs(printed)) if int(m[1]) == 1 else Decimal(0)
        return {
            "date": date, "description": desc, "printed": printed, "credit": credit,
            "original_amount": original, "rate_ea": rate_ea, "installment": installment,
            "document_ref": auth, "debt_delta": debt_delta,
            "deferred": deferred,
        }

    def signed_amount(self, fields):
        # Cardholder view: purchases/interest/fees negative, payments/credits positive.
        return abs(fields["printed"]) if fields["credit"] else -abs(fields["printed"])

    def reconcile(self, currency, txns, summary):
        notes = []
        opening, closing = summary.get("opening"), summary.get("closing")
        charges = -sum((t.amount for t in txns if t.amount < 0), Decimal(0))
        payments = sum((t.amount for t in txns if t.amount > 0), Decimal(0))
        if summary.get("debits") is not None and abs(abs(summary["debits"]) - charges) > TOLERANCE:
            notes.append(f"{currency}: printed charges {summary['debits']} != billed charges {charges} "
                         "(deferred purchases/interest may explain this)")
        if summary.get("credits") is not None and abs(abs(summary["credits"]) - payments) > TOLERANCE:
            notes.append(f"{currency}: printed payments {summary['credits']} != parsed {payments}")
        if opening is None or closing is None:
            return "unknown", notes + [f"{currency}: opening/closing balance not found"]
        billed = opening - sum((t.amount for t in txns), Decimal(0))
        debt = opening + sum((t.debt_delta or 0 for t in txns), Decimal(0))
        if abs(billed - closing) <= TOLERANCE:
            return "yes", notes
        if abs(debt - closing) <= TOLERANCE:
            return "yes", notes + [f"{currency}: reconciled using total debt (full value of new deferred purchases)"]
        return "no", notes + [f"{currency}: expected closing {billed} (billed) or {debt} (total debt), printed {closing}"]


PARSERS: list[type[BaseParser]] = [SavingsParser, CreditCardParser]


def choose_parser(ctx: StatementContext) -> BaseParser | None:
    scored = sorted(((p.detect(ctx), i, p) for i, p in enumerate(PARSERS)), key=lambda x: (-x[0], x[1]))
    if not scored or scored[0][0] <= 0:
        return None
    return scored[0][2]()


# --------------------------------------------------------------------------
# Per-file processing
# --------------------------------------------------------------------------


@dataclass
class FileOutcome:
    source_file: str
    unlocked: bool = False
    parsed: bool = False
    reconciled: str = ""  # yes/no/unknown/partial
    txn_rows: list = field(default_factory=list)
    statement_rows: list = field(default_factory=list)
    unparsed_rows: list = field(default_factory=list)
    error: str = ""


def process_file(src: Path, out_dir: Path, passwords: PasswordProvider, unlock_only: bool,
                 extended_dump: bool) -> FileOutcome:
    outcome = FileOutcome(src.name)
    info = parse_filename(src.name)
    unlocked_path = out_dir / "unlocked" / src.name
    base_row = {"source_file": src.name, "unlocked": "no"}
    try:
        unlock_pdf(src, unlocked_path, passwords)
        outcome.unlocked = True
        base_row["unlocked"] = "yes"
    except Exception as exc:  # noqa: BLE001 - report and keep going
        outcome.error = f"unlock failed: {exc}"
        outcome.statement_rows.append({**base_row, "error": outcome.error})
        return outcome
    if unlock_only:
        return outcome
    try:
        pages = read_pages(unlocked_path)
        dump_text(unlocked_path, pages, out_dir / "text", extended_dump)
        full_text = "\n".join(p.text for p in pages)
        norm_text = norm(full_text)
        start, end = find_period(full_text)
        ctx = StatementContext(src.name, pages, full_text, norm_text, info, start, end)
        parser = choose_parser(ctx)
        if parser is None:
            raise ValueError("could not detect statement type (no parser matched)")
        account_type = parser.account_type
        brand = (info.brand if info and info.brand else "") or (detect_brand(norm_text) if account_type == "credit_card" else "")
        last4 = (info.last4 if info else "") or detect_last4(norm_text)
        account = account_label(account_type, brand, last4)
        result = parser.parse(ctx)
    except Exception as exc:  # noqa: BLE001
        outcome.error = f"parse failed: {exc}"
        outcome.statement_rows.append({**base_row, "error": outcome.error})
        return outcome

    period = {"statement_period_start": start.isoformat() if start else "",
              "statement_period_end": end.isoformat() if end else ""}
    if not start:
        result.warnings.append("statement period not found; years inferred from filename")
    for t in result.txns:
        outcome.txn_rows.append({
            "txn_id": txn_id(src.name, t.page, t.key), "date": t.date.isoformat(),
            "account": account, "account_type": account_type, "currency": t.currency,
            "amount": fmt_amount(t.amount), "description": t.description, "branch": t.branch,
            "document_ref": t.document_ref, "balance_after": fmt_amount(t.balance_after),
            **period, "source_file": src.name, "page": t.page,
            "parse_confidence": t.confidence, "raw_line": t.raw_line,
            "installment": t.installment, "original_amount": fmt_amount(t.original_amount),
            "rate_ea": t.rate_ea,
        })
    for page, idx, cur, raw in result.unparsed:
        outcome.unparsed_rows.append({"source_file": src.name, "page": page, "line_index": idx,
                                      "currency": cur, "raw_line": raw})

    currencies = sorted({t.currency for t in result.txns} | set(result.summaries)) or ["COP"]
    flags = []
    for cur in currencies:
        txns = [t for t in result.txns if t.currency == cur]
        summary = result.summaries.get(cur, {})
        flag, notes = parser.reconcile(cur, txns, summary)
        flags.append(flag)
        credits = sum((t.amount for t in txns if t.amount > 0), Decimal(0))
        debits = -sum((t.amount for t in txns if t.amount < 0), Decimal(0))
        outcome.statement_rows.append({
            **base_row, "account": account, "account_type": account_type, "parser": parser.name,
            "currency": cur, **period,
            "opening_balance": fmt_amount(summary.get("opening")),
            "closing_balance": fmt_amount(summary.get("closing")),
            "printed_total_debits": fmt_amount(summary.get("debits")),
            "printed_total_credits": fmt_amount(summary.get("credits")),
            "parsed_total_debits": fmt_amount(debits), "parsed_total_credits": fmt_amount(credits),
            "parsed_net": fmt_amount(credits - debits), "n_transactions": len(txns),
            "n_unparsed": sum(1 for u in result.unparsed if u[2] == cur),
            "reconciles": flag,
            "error": "; ".join(result.warnings + notes),
        })
    outcome.parsed = bool(result.txns)
    if not result.txns:
        outcome.error = "no transactions parsed (see text/ and unparsed_lines.csv)"
        outcome.statement_rows[-1]["error"] = "; ".join(filter(None, [outcome.statement_rows[-1]["error"], outcome.error]))
    outcome.reconciled = flags[0] if len(set(flags)) == 1 else ("no" if "no" in flags else "partial")
    return outcome


# --------------------------------------------------------------------------
# Optional merge into transactions_unified.csv
# --------------------------------------------------------------------------

INTERNAL_TRANSFER = re.compile(r"PAYONEER|WALLBIT|LEAD BANK|TRANSFERENCIA DESDE|ABONO INTERNACIONAL")
CARD_PAYMENT_ANY = re.compile(r"PAGO (?:A )?(?:TARJETA|TC)\b|PAGO TARJ")
CARD_PAYMENT_ON_CARD = re.compile(r"\b(ABONO|PAGO)\b")


def flow_type(row: dict) -> str:
    desc = norm(row["description"])
    amount = Decimal(row["amount"])
    if INTERNAL_TRANSFER.search(desc):
        return "internal_transfer"
    if CARD_PAYMENT_ANY.search(desc):
        return "card_payment"
    if row["account_type"] == "credit_card" and amount > 0 and CARD_PAYMENT_ON_CARD.search(desc):
        return "card_payment"
    return "spending" if amount < 0 else "income"


def merge_into(path: Path, rows: list[dict]) -> int:
    existing_ids, header = set(), UNIFIED_COLUMNS
    if path.exists() and path.stat().st_size > 0:
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            header = reader.fieldnames or UNIFIED_COLUMNS
            existing_ids = {r.get("txn_id") for r in reader}
        missing = [c for c in UNIFIED_COLUMNS if c not in header]
        if missing:
            raise ValueError(f"{path} is missing columns: {', '.join(missing)}")
        write_header = False
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        write_header = True
    added = 0
    with open(path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        for r in rows:
            if r["txn_id"] in existing_ids:
                continue
            writer.writerow({
                "txn_id": r["txn_id"], "date": r["date"], "account": r["account"],
                "currency": r["currency"], "amount": r["amount"], "flow_type": flow_type(r),
                "category": "", "description": r["description"], "counterparty": "",
                "match_id": "", "match_account": "", "est_other_ccy": "", "is_duplicate": "false",
                "needs_review": "true" if r["parse_confidence"] == "low" else "false",
                "notes": f"bancolombia_extract confidence={r['parse_confidence']}",
                "source_file": r["source_file"],
            })
            added += 1
    return added


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def find_pdfs(input_dir: Path, out_dir: Path, recursive: bool) -> list[Path]:
    pattern = "**/*" if recursive else "*"
    out_resolved = out_dir.resolve()
    pdfs = []
    for p in sorted(input_dir.glob(pattern)):
        if p.is_file() and p.suffix.lower() == ".pdf" and out_resolved not in p.resolve().parents:
            pdfs.append(p)
    return pdfs


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Unlock and parse password-protected Bancolombia PDF statements. "
                    f"The password is read from ${PASSWORD_ENV} or prompted for.")
    ap.add_argument("--input", required=True, type=Path, help="folder containing the PDFs")
    ap.add_argument("--output", default=Path("./bancolombia_out"), type=Path,
                    help="output folder (default: ./bancolombia_out)")
    ap.add_argument("--unlock-only", action="store_true", help="only write unlocked/ copies")
    ap.add_argument("--dump-text", action="store_true",
                    help="also write layout-preserving text and extracted tables to text/")
    ap.add_argument("--recursive", action="store_true", help="search subfolders for PDFs")
    ap.add_argument("--merge-into", type=Path, metavar="PATH",
                    help="append parsed rows to an existing transactions_unified.csv")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if not args.input.is_dir():
        print(f"Input folder not found: {args.input}", file=sys.stderr)
        return 2
    pdfs = find_pdfs(args.input, args.output, args.recursive)
    if not pdfs:
        print(f"No PDFs found in {args.input}", file=sys.stderr)
        return 2
    args.output.mkdir(parents=True, exist_ok=True)
    passwords = PasswordProvider()
    outcomes = []
    for src in pdfs:
        outcome = process_file(src, args.output, passwords, args.unlock_only, args.dump_text)
        status = "ok" if not outcome.error else outcome.error
        print(f"  {src.name}: {status}")
        outcomes.append(outcome)

    if not args.unlock_only:
        txns = [r for o in outcomes for r in o.txn_rows]
        write_csv(args.output / "transactions.csv", TXN_COLUMNS, txns)
        write_csv(args.output / "statements.csv", STATEMENT_COLUMNS, [r for o in outcomes for r in o.statement_rows])
        write_csv(args.output / "unparsed_lines.csv", UNPARSED_COLUMNS, [r for o in outcomes for r in o.unparsed_rows])
        if args.merge_into:
            added = merge_into(args.merge_into, txns)
            print(f"Merged {added} new row(s) into {args.merge_into}")

    n = len(outcomes)
    unlocked = sum(o.unlocked for o in outcomes)
    print("\nSummary")
    print(f"  files processed : {n}")
    print(f"  unlocked        : {unlocked}")
    if not args.unlock_only:
        print(f"  parsed          : {sum(o.parsed for o in outcomes)}")
        print(f"  reconciled      : {sum(o.reconciled == 'yes' for o in outcomes)}")
        print(f"  not reconciled  : {sum(o.reconciled in ('no', 'partial') for o in outcomes)}")
        print(f"  unknown         : {sum(o.reconciled == 'unknown' for o in outcomes)}")
        print(f"  transactions    : {sum(len(o.txn_rows) for o in outcomes)}")
        print(f"  unparsed lines  : {sum(len(o.unparsed_rows) for o in outcomes)}")
    failed = [o for o in outcomes if o.error]
    print(f"  failed          : {len(failed)}")
    print(f"Output written to {args.output.resolve()}")
    return 1 if unlocked < n else 0


if __name__ == "__main__":
    sys.exit(main())
