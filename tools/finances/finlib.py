"""Parsers, classification and transfer matching for Daniel's unified transaction table.

Every parser returns a list of row dicts with the columns in COLS (plus private
"_" fields used during matching). The same functions serve the one-off full
rebuild (build_full.py) and the monthly incremental sync (monthly.py).
"""
import collections
import csv
import difflib
import hashlib
import json
import os
import re
import statistics
import unicodedata
from datetime import date, datetime, timedelta

COLS = ["txn_id", "date", "account", "currency", "amount", "amount_usd", "fx_note", "flow_type", "category",
        "description", "counterparty", "match_id", "match_account", "est_other_ccy", "is_duplicate",
        "needs_review", "notes", "source_file"]


def new_row(**kw):
    base = dict(txn_id="", date="", account="", currency="", amount=0.0, amount_usd="", fx_note="",
                flow_type="", category="", description="", counterparty="", match_id="", match_account="",
                est_other_ccy="", is_duplicate="no", needs_review="", notes="", source_file="", _fx_rate=None)
    base.update(kw)
    return base


def add_note(r, text):
    r["notes"] = (r["notes"] + "; " if r["notes"] else "") + text


def dt(s):
    return date.fromisoformat(s)


def short_hash(*parts):
    return hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:10]


def num(s):
    s = str(s).strip().replace(",", "")
    return float(s) if s not in ("", "-") else 0.0


# ---------------------------------------------------------------- Rippling wallet
# The Rippling export has no direction column. Known payroll amounts are pay-ins;
# anything else is treated as a payout unless no matching deposit turns up (see match_rippling).
PAY_IN = {2307.69, 2308.00, 2357.69, 1813.19, 494.50}


def parse_rippling(path, source_name):
    rows = []
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        a = num(r["amount"])
        d = r["date & time"][:10]
        common = dict(txn_id="RIP-" + r["transaction ID"], date=d, account="Rippling wallet", currency="USD",
                      source_file=source_name, notes="direction inferred: export has no in/out column")
        if a in PAY_IN:
            rows.append(new_row(amount=a, description="Crowd Cow payroll deposit",
                                counterparty="Crowd Cow (via Rippling)", flow_type="income", category="Salary",
                                **common))
        else:
            rows.append(new_row(amount=-a, description="Payout from Rippling wallet",
                                flow_type="internal_transfer", category="Transfer", _rip_abs=a, **common))
    return rows


# ---------------------------------------------------------------- Payoneer
OWN_WITHDRAW = re.compile(r"Withdrawal to (.+)")
PAY_TO = re.compile(r"Payment to (.+)")
PAY_FROM = re.compile(r"Payment from (.+)")


def payoneer_id(cur, d, t, amt, bal, desc, n):
    return f"PAY-{cur}-{d}-{short_hash(cur, d, t, f'{amt:.2f}', bal, desc)}" + (f"-{n}" if n > 1 else "")


def parse_payoneer(path, source_name):
    """Accepts the native Payoneer export (Currency, Transaction date, ...) or the normalized
    columns currency,date,time,credit,debit,balance,description."""
    rows = []
    seen = collections.Counter()
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        if "Transaction date" in r:
            if r.get("Status") and r["Status"] != "Completed":
                continue
            cur, ds, t = r["Currency"], r["Transaction date"], r["Transaction time"]
            amt = num(r["Credit amount"]) + num(r["Debit amount"])
            bal, desc = r["Running balance"], r["Description"]
        else:
            cur, ds, t = r["currency"], r["date"], r["time"]
            amt = num(r["credit"]) + num(r["debit"])
            bal, desc = r["balance"], r["description"]
        d = datetime.strptime(ds, "%m-%d-%Y").date().isoformat()
        key = (cur, d, t, round(amt, 2), bal, desc)
        seen[key] += 1
        kw = dict(txn_id=payoneer_id(cur, d, t, amt, bal, desc, seen[key]), date=d, account="Payoneer " + cur,
                  currency=cur, amount=amt, description=desc, source_file=source_name, _time=t,
                  _balance=num(bal))
        classify_payoneer(kw, desc, amt)
        rows.append(new_row(**kw))
    return rows


def classify_payoneer(kw, desc, amt):
    if desc.startswith("Card charge"):
        m = re.match(r"Card charge \((.*)\)", desc)
        kw["counterparty"] = m.group(1) if m else desc
        kw["flow_type"] = "spending" if amt < 0 else "refund"
    elif desc.startswith("Transfer between balances"):
        kw["flow_type"] = "fx_conversion"; kw["category"] = "FX USD->EUR"
    elif OWN_WITHDRAW.match(desc):
        kw["counterparty"] = OWN_WITHDRAW.match(desc).group(1)
        kw["flow_type"] = "internal_transfer"; kw["category"] = "Transfer"
    elif PAY_TO.match(desc):
        kw["counterparty"] = PAY_TO.match(desc).group(1)
        kw["flow_type"] = "payment_to_third_party"; kw["category"] = "Payments to people/accounts"
        kw["needs_review"] = "who is this account? (Payoneer 'Payment to' = not your registered account)"
    elif desc.startswith("Payment refund"):
        kw["counterparty"] = desc; kw["flow_type"] = "payment_to_third_party"
        kw["category"] = "Payments to people/accounts"; kw["notes"] = "refund of a payment"
    elif PAY_FROM.match(desc):
        cp = PAY_FROM.match(desc).group(1)
        kw["counterparty"] = cp
        if "RIPPLING" in cp:
            kw["flow_type"] = "internal_transfer"; kw["category"] = "Transfer"
        elif "ETORO" in cp:
            kw["flow_type"] = "investment_withdrawal"; kw["category"] = "Investments"
        elif "WISE" in cp:
            kw["flow_type"] = "internal_transfer"; kw["category"] = "Transfer"
            kw["match_account"] = "Wise"
        else:
            kw["flow_type"] = "income"
            kw["category"] = "Salary" if "Brimak" in cp else "Side income / contract"
    elif desc.startswith("Maintenance fee"):
        kw["flow_type"] = "fee"; kw["category"] = "Bank fees & interest"
    elif desc.startswith("Reward") or desc.startswith("Credit from"):
        kw["flow_type"] = "income"; kw["category"] = "Rewards & credits"
    else:
        kw["flow_type"] = "other"


# ---------------------------------------------------------------- Wallbit (transcribed statement)
# Columns: date,description,counterparty,status,operation_id,amount_usd,balance_usd,note
def parse_wallbit(path, source_name="Wallbit monthly statements"):
    rows = []
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        a = num(r["amount_usd"])
        cp = r["counterparty"]
        note = r.get("note", "")
        kw = dict(txn_id="WAL-" + r["operation_id"][:13], date=r["date"], account="Wallbit USD", currency="USD",
                  amount=a, description=r["description"], counterparty=cp, source_file=source_name,
                  notes=(r["status"] + ("; " + note if note else "")) if r["status"] != "Completed" or note else "",
                  _balance=num(r.get("balance_usd", "")))
        if r["status"] in ("Failed", "Not settled"):
            kw["flow_type"] = "not_settled"; kw["is_duplicate"] = "n/a"
        elif "RIPPLING" in cp:
            kw["flow_type"] = "internal_transfer"; kw["category"] = "Transfer"
        elif "Daniel Alejandro" in cp:
            kw["flow_type"] = "internal_transfer"; kw["category"] = "Transfer"
            kw["needs_review"] = "USD->COP to your own Colombian account; confirm which (likely Bancolombia 6948)"
        elif "investment" in cp.lower():
            kw["flow_type"] = "investment_contribution"; kw["category"] = "Investments"
        elif "adjustment" in r["description"].lower():
            kw["flow_type"] = "fee"; kw["category"] = "Bank fees & interest"
        else:
            kw["flow_type"] = "payment_to_third_party"; kw["category"] = "Payments to people/accounts"
            kw["needs_review"] = "label this person (rent? family? services?)"
        rows.append(new_row(**kw))
    return rows


# ---------------------------------------------------------------- Banco de Bogotá Visa 2320 (transcribed statement)
# Columns: statement_cut,comprobante,description,date_txn,date_post,plazo,amount_cop,cuota_mes,cuotas_pend,saldo_pend
def parse_bdb(path):
    rows = []
    cc = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    cc.sort(key=lambda r: (r["statement_cut"], r["date_txn"]))
    seen = set()
    for r in cc:
        a = num(r["amount_cop"])
        k = (r["comprobante"], r["date_txn"], a)
        dup = k in seen
        seen.add(k)
        desc = r["description"]
        kw = dict(txn_id=f"BDB-{r['statement_cut'][:7]}-{r['comprobante']}", date=r["date_txn"],
                  account="Banco de Bogotá Visa 2320", currency="COP", amount=-a, description=desc,
                  counterparty=desc, source_file=f"Extracto_Cuenta_CCA cut {r['statement_cut']}",
                  is_duplicate="yes" if dup else "no",
                  notes=("installments: " + r["plazo"]) if r["plazo"] not in ("00", "01") else "")
        if dup:
            kw["notes"] = "re-listed from previous statement (same comprobante)"
        if desc.startswith("PAGO T.CREDITO"):
            kw["flow_type"] = "card_payment"; kw["category"] = "Transfer"
            kw["needs_review"] = "paid from which account? (expected Bancolombia 6948)"
        elif a < 0:
            kw["flow_type"] = "refund"
        elif "SEG DEUD" in desc or "INTERESES" in desc:
            kw["flow_type"] = "fee"; kw["category"] = "Bank fees & interest"
        else:
            kw["flow_type"] = "spending"
        rows.append(new_row(**kw))
    return rows


# ---------------------------------------------------------------- Bancolombia (statement extractor output)
COMPANY = re.compile(r"\b(S\.?A\.?S?|ESP|LTDA|E\.S\.P|SA ESP)\b|EMPRESA|ACUEDUCTO|ALCANOS|ENEL|VANTI|COMUNICACION|CELULA")


def bc_classify(desc, amt, acct_type):
    d = desc.upper()
    if acct_type != "savings":
        if "ABONO" in d or "PAGO" in d and amt > 0:
            return "card_payment", "Transfer", "paid from Bancolombia 6948 ('PAGO SUC VIRT TC')"
        if "INTERES" in d or "CUOTA DE MANEJO" in d:
            return "fee", "Bank fees & interest", ""
        return ("spending" if amt < 0 else "refund"), "", ""
    if "INTERES" in d and "AHORROS" in d:
        return "income", "Interest", ""
    if "TRANSF INTERNACIONAL RECIBIDA" in d:
        return "internal_transfer", "Transfer", ""
    if "PEXTO" in d:
        return "internal_transfer", "Transfer", "" if amt > 0 else "COP sent to Pexto (Wallbit's local partner) - top-up of Wallbit?"
    if d.startswith("PAGO DE NOM") or "ONTOP DIGITAL" in d:
        return "income", "Salary", ""
    if "TRANSFERENCIA VIRTUAL PYME" in d:
        return "income", "Side income / contract", "company transfer (PYME) - confirm what it was"
    if "BANCO DE BOGOTA" in d:
        return "card_payment", "Transfer", ""
    if "PAGO SUC VIRT TC" in d:
        return "card_payment", "Transfer", ""
    if "SALDO A FAVOR TARJETA" in d:
        return "internal_transfer", "Transfer", "credit-card overpayment returned"
    if "TRANSF QR DANIEL ALEJANDRO" in d:
        return "internal_transfer", "Transfer", "from another account of yours"
    if "NEQUI" in d:
        return ("payment_to_third_party" if amt < 0 else "received_from_third_party"), "Nequi transfers", \
            "Nequi: your own wallet or other people? (if yours, this is a transfer, not spending)"
    if "TRANSFERENCIA CTA SUC VIRTUAL" in d or d.startswith("TRANSF QR") or "PAGO INTERBANC LUISA" in d:
        return ("payment_to_third_party" if amt < 0 else "received_from_third_party"), "Payments to people/accounts", \
            "Bancolombia transfer to/from another account - label it"
    if d.startswith("TRANSF DE ") and amt > 0:  # Bre-B / llave transfer from a person
        return "received_from_third_party", "Payments to people/accounts", \
            "Bancolombia transfer to/from another account - label it"
    if d.startswith("TRANSF A ") and amt < 0 and not COMPANY.search(d):
        return "payment_to_third_party", "Payments to people/accounts", \
            "Bancolombia transfer to/from another account - label it"
    if "PAGO INTERBANC RAPPI" in d:
        return "refund", "Food delivery", "Rappi refund/payout"
    if "CONSIGNACION" in d:
        return "received_from_third_party", "Cash deposits", "cash deposited at a correspondent"
    if "RETIRO" in d:
        return "cash_withdrawal", "Cash withdrawals", ""
    if "EPREPAGO" in d or "E-PREPAGO" in d:
        return ("spending" if amt < 0 else "refund"), "Prepaid card (e-prepago)", \
            "Bancolombia e-prepago loads: purchases made with it aren't itemized"
    if "SKANDIA" in d or "FIDUCIARIA" in d:
        return "investment_contribution", "Investments", "voluntary pension / fund"
    if re.search(r"PAGO PSE (BANCO|BANCOLOMBIA|DAVIVIENDA)", d):
        return "spending", "Bills & online payments (PSE)", ""  # Daniel: these are bill payments
    if "4X" in d or "CUOTA MANEJO" in d or "MANEJO T" in d or "GRAVAMEN" in d or "IMPTO" in d:
        return "fee", "Bank fees & interest", ""
    if "AJUSTE INTERES" in d:
        return "fee", "Bank fees & interest", ""
    return ("spending" if amt < 0 else "refund"), "", ""


def parse_bancolombia(path):
    rows = []
    seen = {}
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        a = num(r["amount"])
        key = (r["account"], r["currency"], r["date"], a, r["description"])
        dup = key in seen and seen[key] != r["source_file"]
        seen.setdefault(key, r["source_file"])
        flow, cat, review = bc_classify(r["description"], a, r["account_type"])
        acct = r["account"] + (" (USD)" if r["account_type"] != "savings" and r["currency"] == "USD" else "")
        note = []
        if r.get("installment"):
            note.append("installment " + r["installment"])
        if r.get("original_amount") and r["original_amount"] not in ("", r["amount"]):
            note.append("original " + r["original_amount"])
        if r.get("parse_confidence") and r["parse_confidence"] != "high":
            note.append("parse " + r["parse_confidence"])
        rows.append(new_row(
            txn_id="BC-" + r["txn_id"], date=r["date"], account=acct, currency=r["currency"], amount=a,
            description=r["description"], counterparty=r["description"], flow_type=flow, category=cat,
            source_file=r["source_file"], is_duplicate="yes" if dup else "no",
            needs_review=review if review and flow not in ("income", "fee") or "PYME" in r["description"] else "",
            notes="; ".join(note), _balance=num(r.get("balance_after", "")),
            _period_end=r.get("statement_period_end", "")))
    return rows


# ---------------------------------------------------------------- Bancolombia alert emails
# Input: JSON list of {"id", "date" (ISO), "text"} where text is the email snippet/body.
# Each alert is rewritten into the wording the statement uses, so bc_classify and the
# category rules treat it exactly like a statement row.
_AMT = r"\$\s?([\d.,]+)"


def _cop(s):
    s = s.strip()
    if re.search(r",\d{2}$", s):          # 79.726,00
        s = s.replace(".", "").replace(",", ".")
    else:                                 # 1745250.00 / 300000
        s = s.replace(",", "")
    return float(s)


ALERT_RULES = [
    # (regex, sign, statement-style description template, kind)
    (re.compile(r"Pagaste " + _AMT + r" a Banco de Bogota", re.I), -1, "PAGO PSE Banco de Bogota", "pse"),
    (re.compile(r"Pagaste " + _AMT + r" a (.+?) desde tu producto", re.I), -1, "PAGO PSE {0}", "pse"),
    (re.compile(r"pago Factura Programada (.+?) Ref \S+ por " + _AMT, re.I), -1, "PAGO PROGRAMADO {0}", "bill"),
    (re.compile(r"Transferiste " + _AMT + r" por Boton Bancolombia a (.+?) desde", re.I), -1, "TRANSF A {0}", "boton"),
    (re.compile(r"transferiste " + _AMT + r" a la llave \S+ desde tu cuenta \*?\d+ a (.+?) el ", re.I), -1,
     "TRANSF A {0}", "breb"),
    (re.compile(r"Transferiste " + _AMT + r" desde tu cuenta \*?\d+ a la cuenta \*?(\d+)", re.I), -1,
     "TRANSFERENCIA CTA SUC VIRTUAL a *{0}", "out_transfer"),
    (re.compile(r"pagaste " + _AMT + r" por codigo QR desde tu cuenta \*?\d+ a la llave (\S+)", re.I), -1,
     "PAGO QR {0}", "qr"),
    (re.compile(r"recibiste una transferencia de (.+?) por " + _AMT, re.I), +1, "TRANSF DE {0}", "in_transfer"),
    (re.compile(r"Recibiste una transferencia por " + _AMT + r" de (.+?) en tu cuenta", re.I), +1,
     "TRANSFERENCIA CTA SUC VIRTUAL de {0}", "in_transfer"),
    (re.compile(r"Recibiste una consignacion por " + _AMT + r" desde el corresponsal (.+?) en", re.I), +1,
     "CONSIGNACION CORRESPONSAL {0}", "deposit"),
    (re.compile(r"Compraste " + _AMT + r" en (.+?) con tu", re.I), -1, "COMPRA EN {0}", "purchase"),
    (re.compile(r"Retiraste " + _AMT + r" en (.+?)[\.,]", re.I), -1, "RETIRO CAJERO {0}", "atm"),
]
ALERT_IGNORE = re.compile(r"está lista para que la pagues|Inscribiste|Programaste la factura|registraste tu llave|"
                          r"en una transferencia internacional", re.I)
ALERT_FOREIGN = re.compile(r"Recibiste ([\d.,]+)USD en una transferencia internacional", re.I)


_DATE_IN_TEXT = re.compile(r"\b(\d{2})/(\d{2})/(\d{4}|\d{2})\b")


def alert_date(text, iso_utc):
    """Date of the movement: the dd/mm/yy(yy) in the alert text, else the email time in Colombia (UTC-5)."""
    m = _DATE_IN_TEXT.search(text)
    if m:
        d, mo, y = m.groups()
        y = int(y) + (2000 if len(y) == 2 else 0)
        try:
            return date(y, int(mo), int(d)).isoformat()
        except ValueError:
            pass
    t = datetime.fromisoformat(iso_utc.replace("Z", "+00:00"))
    return (t - timedelta(hours=5)).date().isoformat()


def parse_bc_alerts(path):
    """Returns (rows, unparsed, foreign_usd_notices)."""
    rows, unparsed, foreign = [], [], []
    for m in json.load(open(path)):
        text = re.sub(r"\s+", " ", m["text"])
        fx = ALERT_FOREIGN.search(text)
        if fx:
            foreign.append({"id": m["id"], "date": m["date"][:10], "usd": fx.group(1)})
            continue
        if ALERT_IGNORE.search(text):
            continue
        for rx, sign, tmpl, kind in ALERT_RULES:
            g = rx.search(text)
            if not g:
                continue
            groups = g.groups()
            amt_i = 0 if re.fullmatch(r"[\d.,]+", groups[0]) else 1
            amount = sign * _cop(groups[amt_i])
            name = groups[1 - amt_i].strip() if len(groups) > 1 else ""
            desc = tmpl.format(name)
            flow, cat, review = bc_classify(desc, amount, "savings")
            rows.append(new_row(
                txn_id="BCE-" + m["id"], date=alert_date(text, m["date"]), account="Bancolombia savings 6948", currency="COP",
                amount=amount, description=desc, counterparty=name or desc, flow_type=flow, category=cat,
                source_file="Bancolombia alert email", needs_review=review if review and flow not in ("income", "fee") else "",
                notes="from alert email; replaced by the statement row when the quarterly statement arrives",
                _alert_kind=kind))
            break
        else:
            if re.search(r"\$\s?[\d.,]+", text):
                unparsed.append({"id": m["id"], "date": m["date"][:10], "text": text[:200]})
    return rows, unparsed, foreign


# ---------------------------------------------------------------- Wise (balance statement CSV)
def parse_wise(path, source_name):
    rows = []
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        tid = r.get("TransferWise ID") or r.get("ID") or ""
        ds = (r.get("Date") or r.get("Created on") or "")[:10]
        try:
            d = datetime.strptime(ds, "%d-%m-%Y").date().isoformat()
        except ValueError:
            d = ds
        cur = r.get("Currency") or "USD"
        a = num(r.get("Amount", 0))
        desc = r.get("Description", "")
        kw = dict(txn_id="WISE-" + (tid or short_hash(d, a, desc)), date=d, account="Wise " + cur, currency=cur,
                  amount=a, description=desc, counterparty=r.get("Merchant") or r.get("Payee Name") or
                  r.get("Payer Name") or desc, source_file=source_name, _balance=num(r.get("Running Balance", "")))
        if r.get("Merchant") or desc.lower().startswith("card transaction"):
            kw["flow_type"] = "spending" if a < 0 else "refund"
        elif "RIPPLING" in desc.upper() or "PAYONEER" in desc.upper() or "BOLIVAR" in kw["counterparty"].upper():
            kw["flow_type"] = "internal_transfer"; kw["category"] = "Transfer"
        elif a < 0:
            kw["flow_type"] = "payment_to_third_party"; kw["category"] = "Payments to people/accounts"
            kw["needs_review"] = "Wise payment: who is this?"
        else:
            kw["flow_type"] = "received_from_third_party"; kw["needs_review"] = "Wise receipt: what was it?"
        if "fee" in desc.lower():
            kw["flow_type"] = "fee"; kw["category"] = "Bank fees & interest"
        rows.append(new_row(**kw))
    return rows


# ---------------------------------------------------------------- Apple Wallet export (tools/wallet_backup)
# Columns: wallet_txn_id,date,time,card_name,card_last4,merchant,amount,currency,status,source[,billed_amount,billed_currency]
# Wallet rows (APW-) stand in for card purchases until the card statement / Payoneer CSV covers them,
# the way Bancolombia alert rows (BCE-) stand in for the savings statement. See reconcile_wallet.
WALLET_CARDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wallet_cards.json")
WALLET_NOTE = "from Apple Wallet, replaced by the statement row when it arrives"
WALLET_PENDING = "Apple Wallet: pending"


def _plain(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def wallet_account(card_name, last4, currency, rules):
    """Ledger account for a Wallet card, None to ignore it, or False if no rule matches."""
    for r in rules:
        if _plain(r["name_contains"]) not in _plain(card_name):
            continue
        if r.get("last4") and r["last4"] != last4:
            continue
        if r.get("account") is None:
            return None
        if "{currency}" in r["account"]:
            cur = currency if currency in r.get("currencies", [currency]) else r.get("default_currency", currency)
            return r["account"].format(currency=cur)
        if r.get("foreign_account") and currency != r.get("home_currency", currency):
            return r["foreign_account"]
        return r["account"]
    return False


def parse_wallet(path, source_name, cards_file=WALLET_CARDS):
    """Returns (rows, skipped) where skipped counts rows per card label that matched no account."""
    with open(cards_file) as f:
        rules = json.load(f)["cards"]
    rows, skipped = [], collections.Counter()
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        if r["status"] == "declined":
            continue
        acct = wallet_account(r["card_name"], r["card_last4"], r["currency"], rules)
        if not acct:
            if acct is False:
                skipped[f"{r['card_name']} ..{r['card_last4']}"] += 1
            continue
        a = num(r["amount"])
        notes = [WALLET_NOTE]
        if r["status"] == "pending":
            notes.append(WALLET_PENDING)
        kw = dict(txn_id=r["wallet_txn_id"], date=r["date"], account=acct, currency=r["currency"], amount=a,
                  description=r["merchant"], counterparty=r["merchant"], flow_type="spending" if a < 0 else "refund",
                  source_file=source_name, notes="; ".join(notes), _time=r.get("time", ""), _status=r["status"])
        if r.get("billed_amount") and r.get("billed_currency"):
            kw["est_other_ccy"] = f"{r['billed_currency']} {num(r['billed_amount']):,.2f} billed (Apple Wallet)"
        if r["status"] not in ("settled", "pending", "refund"):
            kw["needs_review"] = "Apple Wallet status not recognised - check this purchase in Wallet"
        rows.append(new_row(**kw))
    return rows, skipped


def card_family(account):
    """Accounts that hold the same card: 'Payoneer USD'/'Payoneer EUR' -> 'Payoneer', 'X (USD)' -> 'X'."""
    if account.startswith("Payoneer "):
        return "Payoneer"
    return account[:-6] if account.endswith(" (USD)") else account


def convert(amount, cur, to, month, cop_month, eur_month):
    """amount in `cur` expressed in `to`, via USD with the monthly rates; None if a rate is missing."""
    if cur == to:
        return amount
    cop, _ = _nearest(cop_month, month, 6)
    eur, _ = _nearest(eur_month, month, 30)
    usd = {"USD": lambda: amount, "COP": lambda: amount / cop if cop else None,
           "EUR": lambda: amount * eur if eur else None}.get(cur, lambda: None)()
    if usd is None:
        return None
    return {"USD": lambda: usd, "COP": lambda: usd * cop if cop else None,
            "EUR": lambda: usd / eur if eur else None}.get(to, lambda: None)()


_STOP = {"THE", "AND", "COM", "WWW", "BOGOTA", "COL", "COLOMBIA", "SAS", "LTDA", "PAYPAL", "INC", "LLC"}


def merchant_similarity(a, b):
    """0..1. Statements truncate and upper-case merchant names, Wallet cleans them up, so this takes
    the best of a token-prefix overlap and a character ratio."""
    def toks(s):
        return {t[:5] for t in re.sub(r"[^A-Z0-9]+", " ", _plain(s).upper()).split() if len(t) >= 3 and t not in _STOP}
    ta, tb = toks(a), toks(b)
    tok = len(ta & tb) / min(len(ta), len(tb)) if ta and tb else 0.0
    ca, cb = (re.sub(r"[^A-Z0-9]", "", _plain(s).upper()) for s in (a, b))
    return max(tok, difflib.SequenceMatcher(None, ca, cb).ratio() if ca and cb else 0.0)


BILLED = re.compile(r"^([A-Z]{3}) (-?[\d,]+\.?\d*) billed")


def wallet_match(w, s, cop_month, eur_month):
    """Score for 'statement row s is the same purchase as Wallet row w', or None.
    Same card, same sign, date within 3 days, and an amount that agrees: within 1% in the same currency,
    or within 8% after FX (bank rate and markup differ from the monthly median)."""
    if card_family(w["account"]) != card_family(s["account"]) or (w["amount"] < 0) != (s["amount"] < 0):
        return None
    days = abs((dt(w["date"]) - dt(s["date"])).days)
    if days > 3:
        return None
    amt, cur, tol = w["amount"], w["currency"], 0.01
    m = BILLED.match(w.get("est_other_ccy") or "")
    if cur != s["currency"] and m and m.group(1) == s["currency"]:
        amt, cur = num(m.group(2)), m.group(1)
    if cur != s["currency"]:
        amt, tol = convert(amt, cur, s["currency"], s["date"][:7], cop_month, eur_month), 0.08
        if amt is None:
            return None
    diff = abs(abs(amt) - abs(s["amount"])) / max(abs(s["amount"]), 0.01)
    if diff > tol:
        return None
    sim = merchant_similarity(w["description"], s["description"])
    if (tol > 0.01 or diff > 0.002) and sim < 0.3:   # inexact amount: the merchant has to agree too
        return None
    return (round(sim, 2), -days, -diff)


def reconcile_wallet(ledger, new, cop_month, eur_month):
    """Statement/CSV rows replace Apple Wallet rows. Mutates ledger rows in place and marks new rows
    with _drop. Returns (updated ledger rows, stats)."""
    wallet_new = [r for r in new if r["txn_id"].startswith("APW-")]
    families = {card_family(r["account"]) for r in ledger + new if r["txn_id"].startswith("APW-")}
    if not families:
        return [], {}
    stats = collections.Counter()
    by_id = {r["txn_id"]: r for r in ledger}
    open_w = [r for r in ledger if r["txn_id"].startswith("APW-")]
    stmt = [r for r in new if not r["txn_id"].startswith(("APW-", "BCE-")) and not r.get("_drop")
            and r["flow_type"] in ("spending", "refund") and card_family(r["account"]) in families]
    covered = collections.defaultdict(str)
    for r in ledger + new:
        if not r["txn_id"].startswith(("APW-", "BCE-")) and card_family(r["account"]) in families:
            f = card_family(r["account"])
            covered[f] = max(covered[f], r["date"])
    updated = {}

    # 1. the nightly export overlaps the Sheet: rows already there are dropped (a pending one takes the settled amount)
    for w in wallet_new:
        old = by_id.get(w["txn_id"])
        if old is None:
            continue
        w["_drop"] = True
        if WALLET_PENDING in old["notes"] and w["_status"] != "pending":
            old.update(date=w["date"], amount=w["amount"], amount_usd="", fx_note="",
                       notes="; ".join(n for n in old["notes"].split("; ") if n != WALLET_PENDING))
            updated[old["_row"]] = old
            stats["pending_settled"] += 1
    wallet_new = [w for w in wallet_new if not w.get("_drop")]

    # 2. pair statement rows with Wallet rows, best scores first
    pairs = []
    for s in stmt:
        for w in open_w + wallet_new:
            sc = wallet_match(w, s, cop_month, eur_month)
            if sc:
                pairs.append((sc, id(s), id(w), s, w))
    pairs.sort(key=lambda p: p[0], reverse=True)
    used = set()
    for _, si, wi, s, w in pairs:
        if si in used or wi in used:
            continue
        used |= {si, wi}
        if w.get("_row"):            # already in the Sheet: becomes the statement row, keeps your edits
            other = "" if w["currency"] == s["currency"] else f"Apple Wallet {w['currency']} {abs(w['amount']):,.2f}"
            notes = [n for n in w["notes"].split("; ") if n and n not in (WALLET_NOTE, WALLET_PENDING)]
            w.update(txn_id=s["txn_id"], date=s["date"], account=s["account"], currency=s["currency"],
                     amount=s["amount"], description=s["description"], counterparty=s["counterparty"],
                     flow_type=s["flow_type"], source_file=s["source_file"], is_duplicate=s["is_duplicate"],
                     est_other_ccy=other or s["est_other_ccy"], amount_usd="", fx_note="",
                     notes="; ".join(notes + ["Apple Wallet row confirmed by statement"] + ([s["notes"]] if s["notes"] else [])))
            if w["needs_review"].startswith("Apple Wallet"):
                w["needs_review"] = ""
            updated[w["_row"]] = w
            s["_drop"] = True
            stats["replaced"] += 1
        else:                        # both arrived this month: the statement row wins
            w["_drop"] = True
            stats["same_run"] += 1

    # 3. new Wallet rows inside a period a statement already covers, or already in Bancolombia alert emails
    bce = [r for r in ledger + new if r["txn_id"].startswith("BCE-") and r["description"].startswith("COMPRA EN")]
    for w in wallet_new:
        if w.get("_drop"):
            continue
        if w["date"] <= covered[card_family(w["account"])]:
            w["_drop"] = True
            stats["inside_statement_period"] += 1
            continue
        if any(abs(b["amount"] - w["amount"]) < 1 and abs((dt(b["date"]) - dt(w["date"])).days) <= 3
               and w["currency"] == b["currency"] and w["account"].startswith("Bancolombia") for b in bce):
            w["_drop"] = True
            stats["already_in_alert_emails"] += 1

    # 4. Wallet rows in the Sheet that the statement period passed without a match
    for w in open_w:
        if id(w) in used or w["needs_review"]:
            continue
        end = covered[card_family(w["account"])]
        if end and w["date"] <= (dt(end) - timedelta(days=3)).isoformat():
            w["needs_review"] = ("Apple Wallet row not found in the statement/CSV - reversed, declined, "
                                 "or posting next cycle?")
            updated[w["_row"]] = w
            stats["flagged"] += 1
    return list(updated.values()), stats


# ---------------------------------------------------------------- categories
CAT = [
    ("Utilities (home)", r"ENEL|VANTI|ALCANOS|ACUEDUCTO|AGUAS DE|CODENSA|GAS NATURAL|EMPRESA DE TELECOMUN"),
    ("Health & insurance", r"COMPENSAR|FARMATODO|COLMEDICA"),
    ("Transport", r"TRANSPORTE MASIVO"),
    ("Subscriptions & software", r"THESUFFERFEST"),
    ("Groceries", r"OLIMPICA|MERQUEO|CARNES FINAS"),
    ("Shopping (retail)", r"FALABELLA|HOMECENTER|ALIBABA|NEBOPET"),
    ("Entertainment & events", r"MULTIPLEX"),
    ("Taxes", r"FONDO ROTATORIO"),
    ("Groceries", r"TIENDA D1|CARULLA|JUMBO|EXITO|CARREFOUR|LIDL|CONAD|MONOPRIX|MERCADONA|SPAR|FRIGO CARNES|PINGO DOCE|AUCHAN|CONTINENTE|ALBERTSONS|FOOD LION|PICARD|SUPERMERCADO|G\.F\. MARKET|ALIPER|VIVAL|AH TO GO|ALAL SHOP|DELICIAS CAMPESINAS|MORTON WILLIAMS|COSECHAS|7-ELEVEN|OXXO|MECKLENBURG ABC|GENERAL STOR|FRUTARIA"),
    ("Food delivery", r"RAPPI"),
    ("Transport", r"UBER|BOLT\.EU|MTA\*|OMNYPYG|METRO|METROPOLITANO|SNCF|FLIX|BLABLACAR|NS AMSTERDAM|NSINTERNATIONAL|SNCB|STIB|FLIBCO|AUTOCARS|TRANSDEV|ATAC|ARRIVA|BKK BUDAPEST|CLESS TICKET|VENEZIA CIT|ALPYTRANSFERS|BSCA PARKING|PARKPLATZ|PARQ|GOPASS|FUNICULAR|CIE DU MONT BLANC|ROMA OSTIENSE|TRENITALIA|SERVICIOS POSTALES|AIRPORT CHARLEROI|OVIEDO ESTACION|CENTRO COMERCIAL|CTRE CIAL|T2A "),
    ("Fuel & car", r"\bEDS\b|ESSO|ENI \d|SHELL|CHEVRON|EXXON|CONOCO|\bBP#|Q8 |ESTACION DE SERVICIO|SERVICENTRO|AQUILA ENERGIA|MOBIL|PRIMAX|TERPEL|PETROBRAS|COMBUSCOL|E\.S\. GRUPO|QT \d|ADS GIOVE"),
    ("Travel (flights & lodging)", r"AIRBNB|BOOKING|IBERIA|LATAM|AVIANCA|WINGO|AEROREPUBLICA|RYANAIR|WIZZ|VOLOTEA|SPIRIT AI|ITA AIRWAYS|MEININGER|CLINKNOORD|HOTEL|AGRITURISMO|LA COLLINA|TICKETINGPAYMENTS|OPERATION SAN ANDRES|COMUNE DI|ASSOCIATION TMB|FFCAM|MAISON DES DRUS|POST CARRY|COORDI USA|GRNDCYN"),
    ("Health & insurance", r"COLMEDICA|CRUZ VERDE|MEDICARTE|SHAIO|PHARMACIE|FARMACIA|DROGUERIA|UNID MED|LENTESPLUS|ALLEN PHARMA|BELLA PIEL|VITALSE|SEG DEUD|CEN MED"),
    ("Subscriptions & software", r"APPLE\.COM|OPENAI|ANTHROPIC|CLAUDE|AMAZON PRIME|Amazon Prime|GOPRO|TRAINERROAD|BRAVE|OPEN INC|FACEBK|GIGSKY|SERVICIOS WEB EBANX|RMTLY"),
    ("Phone & internet", r"COMCEL|MOVISTAR|XFERA|WINDTRE"),
    ("Cycling & sport", r"BICICLETA|NITRO BIKES|3PUERTOS|PUERTOS GRAVEL|SPECIALIZED|2RUEDAS|BIKE SHELTER|CULTURE VELO|MVBIKE|DECATHLON|ADIDAS|COLUMBIA SPORTSWEAR|SUPERKARTS|SMASH MOUNTAIN|ADRENALINE|SUGAR MOUNTAIN|OUTER RANGE|WHITEWATER|MASBIC"),
    ("Entertainment & events", r"CINEMARK|CINE COLOMBIA|TU BOLETA|TAQUILLALIVE|TM \*|TICKET ZAMNA|COOPSERFUN|MUSEO|MUSEUM|ONE WORLD OBSY|TOPARA|RIFLE|PAYU\*BALOTO|NYPL|PINS MECHANICAL|RACK'EM"),
    ("Shopping (online)", r"AMAZON|AMZN|ALIEXPRESS|aliexpress|MERCADO ?PAGO|MERCADOPAGO|MERPAGO|MP\*|PAYPAL|SOUNDCORE|WOMPI|PAMPLING"),
    ("Shopping (retail)", r"MINISO|APPLE STORE|I SHOP|TITAN PLAZA BOGOTA|MACYS|DISNEY STORE|UPS SERVICIOS|FUJIFILM|SOUVENIRS|TIENDA NAT|MISCELANEA|STREET SHOP|EB \*ORBIT|INVERSIONES PRESTIGE|INVERSIONES MURCIA|VENTA\b|BUCONOS"),
    ("Taxes", r"IMPUESTO"),
    ("Bank fees & interest", r"INTERESES|Maintenance fee"),
]
CAT_RE = [(c, re.compile(p, re.I)) for c, p in CAT]


def categorize(rows):
    for r in rows:
        if r["category"]:
            continue
        if r["flow_type"] in ("spending", "refund"):
            txt = r["counterparty"] + " " + r["description"]
            for c, rx in CAT_RE:
                if rx.search(txt):
                    r["category"] = c
                    break
            else:
                if re.match(r"(PAGO PSE|PAGO PROGRAMADO|PAGO SV|TRANSF A |PAGO PROG)", r["description"]):
                    r["category"] = "Bills & online payments (PSE)"
                    continue
                r["category"] = "Restaurants, cafés & bars"  # remaining merchants are mostly food/drink
                add_note(r, "category guessed (default)")


# ---------------------------------------------------------------- transfer matching
# Every matcher skips rows that already carry a match_id, so it can run over
# (existing ledger + new rows) without disturbing earlier links.
def link(src, dst, kind, rate=None):
    mid = f"{kind}-{src['date']}-{abs(src['amount']):.0f}"
    src["match_id"] = dst["match_id"] = mid
    src["match_account"] = dst["account"]; dst["match_account"] = src["account"]
    if rate:
        src["est_other_ccy"] = f"COP {dst['amount']:,.2f} received {dst['date']} (rate {rate:,.2f} COP/USD)"
        dst["est_other_ccy"] = f"USD {-src['amount']:,.2f} sent {src['date']} (rate {rate:,.2f})"
        src["_fx_rate"] = dst["_fx_rate"] = rate
    for r in (src, dst):
        if r["needs_review"].startswith(("USD->COP", "confirm COP", "paid from which", "no matching",
                                         "Rippling deposit without", "card payment not found", "card payment with no",
                                         "foreign transfer received", "USD side not found", "COP sent to Pexto")):
            r["needs_review"] = ""


def match_rippling(rows, log):
    rip_out = [r for r in rows if r["account"] == "Rippling wallet" and r["amount"] < 0 and not r["match_id"]]
    dest = [r for r in rows if not r["match_id"] and r["amount"] > 0 and "RIPPLING" in r["counterparty"].upper()
            and r["account"] in ("Payoneer USD", "Wallbit USD", "Wise USD")]
    used = set()
    for o in rip_out:
        best = next((d for d in dest if id(d) not in used and abs(d["amount"] + o["amount"]) < 0.005
                     and 0 <= (dt(d["date"]) - dt(o["date"])).days <= 4), None)
        if best:
            used.add(id(best))
            o["match_id"] = best["match_id"] = "M-" + o["txn_id"][4:12]
            o["match_account"] = best["account"]; best["match_account"] = "Rippling wallet"
            o["counterparty"] = best["account"]
            for r in (o, best):
                if r["needs_review"].startswith(("no matching", "Rippling deposit")):
                    r["needs_review"] = ""
            log.append((o["date"], o["amount"], "Rippling wallet", best["account"], best["date"], "matched", best["notes"]))
        else:
            o["needs_review"] = o["needs_review"] or "no matching deposit found in Payoneer/Wallbit data"
            o["match_account"] = o["match_account"] or "UNKNOWN"
            log.append((o["date"], o["amount"], "Rippling wallet", "UNKNOWN", "", "unmatched", ""))
    for d in dest:
        if id(d) not in used and not d["needs_review"]:
            d["needs_review"] = "Rippling deposit without matching Rippling payout"


def match_payoneer_fx(rows):
    usd = [r for r in rows if r["account"] == "Payoneer USD" and r["flow_type"] == "fx_conversion"
           and not r["match_id"] and r.get("_time")]
    eur = [r for r in rows if r["account"] == "Payoneer EUR" and r["flow_type"] == "fx_conversion"
           and not r["match_id"] and r.get("_time")]
    secs = lambda t: int(t[:2]) * 3600 + int(t[3:5]) * 60 + int(t[6:8])
    for u in usd:
        for e in eur:
            if e["match_id"] or e["date"] != u["date"]:
                continue
            if abs(secs(u["_time"]) - secs(e["_time"])) <= 180:
                mid = "FX-" + u["date"] + "-" + u["_time"].replace(":", "")
                u["match_id"] = e["match_id"] = mid
                u["match_account"] = "Payoneer EUR"; e["match_account"] = "Payoneer USD"
                rate = -u["amount"] / e["amount"]
                u["est_other_ccy"] = f"EUR {e['amount']:.2f} (USD/EUR {rate:.4f})"
                e["est_other_ccy"] = f"USD {-u['amount']:.2f}"
                break


UNMATCHED_COP_MSG = ("foreign transfer received with no matching USD send in the exported data "
                     "(Payoneer export starts Oct 2023)")


def match_usd_to_cop(rows, log, unmatched_msg=UNMATCHED_COP_MSG):
    bc_in = [r for r in rows if r["account"] == "Bancolombia savings 6948" and r["amount"] > 0]

    def run(srcs, desc_kw, kind, max_days=10):
        for s_ in srcs:
            usd_amt = -s_["amount"]; sd = dt(s_["date"])
            cands = [b for b in bc_in if not b["match_id"] and desc_kw in b["description"].upper()
                     and -2 <= (dt(b["date"]) - sd).days <= max_days and 2800 <= b["amount"] / usd_amt <= 5200]
            if cands:
                b = min(cands, key=lambda b: abs((dt(b["date"]) - sd).days))
                rate = b["amount"] / usd_amt
                link(s_, b, kind, rate)
                log.append((s_["date"], s_["account"], usd_amt, b["date"], b["amount"], round(rate, 2), "matched"))
            else:
                s_["needs_review"] = "no matching COP credit found in Bancolombia 6948"
                log.append((s_["date"], s_["account"], usd_amt, "", "", "", "UNMATCHED"))

    pay_src = sorted([r for r in rows if r["account"] == "Payoneer USD" and not r["match_id"]
                      and r["counterparty"].startswith("BANCOLOMBIA (6948)")], key=lambda r: r["date"])
    wal_src = sorted([r for r in rows if r["account"] == "Wallbit USD" and not r["match_id"]
                      and "Daniel Alejandro" in r["counterparty"] and r["flow_type"] == "internal_transfer"],
                     key=lambda r: r["date"])
    run(pay_src, "INTERNACIONAL", "PAY>BC")
    run(wal_src, "PEXTO", "WAL>BC")
    for b in bc_in:
        if not b["match_id"] and not b["match_account"] and \
                ("INTERNACIONAL" in b["description"].upper() or "PEXTO" in b["description"].upper()):
            b["needs_review"] = unmatched_msg
            b["match_account"] = "UNKNOWN USD source"


def match_cards(rows):
    bc_out = [r for r in rows if r["account"] == "Bancolombia savings 6948" and r["amount"] < 0]

    def run(card_rows, kw, kind, exact=True, days=5):
        for c in card_rows:
            if c["match_id"]:
                continue
            cd = dt(c["date"])
            cands = [b for b in bc_out if not b["match_id"] and kw(b["description"].upper())
                     and abs((dt(b["date"]) - cd).days) <= days and (not exact or abs(b["amount"] + c["amount"]) < 1)]
            if cands:
                b = min(cands, key=lambda b: abs((dt(b["date"]) - cd).days))
                link(b, c, kind)
            else:
                c["match_account"] = c["match_account"] or "UNKNOWN"
                c["needs_review"] = "card payment not found in Bancolombia 6948 - paid from another account?"

    run([r for r in rows if r["account"] == "Banco de Bogotá Visa 2320" and r["flow_type"] == "card_payment"],
        lambda d: "BANCO DE BOGOTA" in d, "BC>BDB")
    for card, kw in (("Visa 7380", "TC VISA"), ("Mastercard 6879", "TC MASTER"), ("Amex 1326", "TC AMEX"), ("Amex 1985", "TC AMEX")):
        run([r for r in rows if r["account"] == "Bancolombia " + card and r["flow_type"] == "card_payment"],
            lambda d, kw=kw: kw in d and "DOLAR" not in d, "BC>CARD")
        run([r for r in rows if r["account"] == "Bancolombia " + card + " (USD)" and r["flow_type"] == "card_payment"],
            lambda d, kw=kw: kw in d and "DOLAR" in d, "BC>CARDUSD", exact=False, days=10)


def label_unmatched_card_payments(rows, card_statement_months=None):
    for b in rows:
        if b["account"] != "Bancolombia savings 6948" or b["flow_type"] != "card_payment" or b["match_id"] \
                or b["match_account"]:
            continue
        if "BANCO DE BOGOTA" in b["description"].upper() and b["date"] < "2025-07-01":
            b["match_account"] = "Banco de Bogotá Visa 2320 (statements before Jul 2025 not in Drive)"
            b["needs_review"] = ""
        else:
            b["match_account"] = "card statement for this month not in Drive"
            b["needs_review"] = "card payment with no matching card-statement row (that month's card statement is missing)"


def match_all(rows, unmatched_cop_msg=UNMATCHED_COP_MSG):
    """Runs every matcher. Returns logs for the report files."""
    rip_log, fx_log = [], []
    match_rippling(rows, rip_log)
    match_payoneer_fx(rows)
    match_usd_to_cop(rows, fx_log, unmatched_cop_msg)
    match_cards(rows)
    return rip_log, fx_log


# ---------------------------------------------------------------- FX and USD amounts
RATE_COP = re.compile(r"rate ([\d,]+\.?\d*) COP/USD")
RATE_EUR = re.compile(r"USD/EUR ([0-9.]+)")


def fx_tables(rows):
    """Monthly median COP/USD (from matched transfers) and USD/EUR (from Payoneer conversions)."""
    cop, eur = collections.defaultdict(list), collections.defaultdict(list)
    for r in rows:
        if r["currency"] == "USD":
            rate = r.get("_fx_rate")
            if not rate:
                m = RATE_COP.search(r["est_other_ccy"])
                rate = float(m.group(1).replace(",", "")) if m else None
            if rate:
                cop[r["date"][:7]].append(rate)
        if r["account"] == "Payoneer USD" and r["flow_type"] == "fx_conversion":
            m = RATE_EUR.search(r["est_other_ccy"])
            if m:
                eur[r["date"][:7]].append(float(m.group(1)))
    return ({m: statistics.median(v) for m, v in cop.items()}, {m: len(v) for m, v in cop.items()},
            {m: statistics.median(v) for m, v in eur.items()})


def _nearest(tbl, m, max_gap):
    if not tbl:
        return None, None
    idx = lambda x: int(x[:4]) * 12 + int(x[5:7])
    k = min(sorted(tbl), key=lambda k: abs(idx(k) - idx(m)))
    return (tbl[k], k) if abs(idx(k) - idx(m)) <= max_gap else (None, None)


def apply_usd(rows, cop_month, eur_month, only_missing=False):
    for r in rows:
        if only_missing and r["amount_usd"] not in ("", None):
            continue
        m = r["date"][:7]
        if r["currency"] == "USD":
            r["amount_usd"] = r["amount"]
        elif r["currency"] == "COP":
            rate, k = _nearest(cop_month, m, 6)
            r["amount_usd"] = round(r["amount"] / rate, 2) if rate else ""
            r["fx_note"] = f"COP/USD {rate:,.0f} ({k})" if rate else ""
        elif r["currency"] == "EUR":
            rate, k = _nearest(eur_month, m, 30)
            r["amount_usd"] = round(r["amount"] * rate, 2) if rate else ""
            r["fx_note"] = f"USD/EUR {rate:.4f} ({k})" if rate else ""


# ---------------------------------------------------------------- Daniel's standing answers (2026-10-13)
INFO_ONLY = ("paid from Bancolombia 6948", "Rappi refund", "cash deposited", "voluntary pension",
             "Bancolombia e-prepago", "credit-card overpayment", "from another account of yours")


def apply_rules(rows):
    for r in rows:
        if r["account"].startswith("Bancolombia savings"):
            d = r["description"].upper()
            src = "Nequi" if "NEQUI" in d else ("Bancolombia transfers" if (
                "TRANSFERENCIA CTA SUC VIRTUAL" in d or d.startswith("TRANSF QR") or "PAGO INTERBANC LUISA" in d
                or (r["flow_type"] in ("payment_to_third_party", "received_from_third_party")
                    and d.startswith(("TRANSF A ", "TRANSF DE ")))) else None)
            if src and r["flow_type"] in ("payment_to_third_party", "received_from_third_party"):
                out = r["amount"] < 0
                r["category"] = ("Payouts" if out else "Payins") + f" ({src})"
                r["needs_review"] = ""
                add_note(r, "payout to others (confirmed)" if out else "payin from others (confirmed)")
        if r["account"] == "Payoneer USD" and "WISE" in r["counterparty"].upper():
            r["flow_type"] = "internal_transfer"; r["category"] = "Transfer"; r["needs_review"] = ""
            r["match_account"] = r["match_account"] or "Wise"
    for r in rows:
        if r["needs_review"].startswith(INFO_ONLY):
            if not (r["needs_review"].startswith("paid from") and r["match_id"]):
                add_note(r, r["needs_review"])
            r["needs_review"] = ""


# ---------------------------------------------------------------- IO
def write_rows(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            r = dict(r)
            r["amount"] = f"{float(r['amount']):.2f}"
            w.writerow(r)


def sheet_row(r):
    """One row in Transactions!A:R order, numbers as numbers."""
    out = []
    for c in COLS:
        v = r.get(c, "")
        if c == "amount":
            v = round(float(v), 2)
        elif c == "amount_usd" and v not in ("", None):
            v = round(float(v), 2)
        out.append(v)
    return out
