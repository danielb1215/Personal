import csv
from decimal import Decimal

import pikepdf
import pytest

import bancolombia_extract as be
from make_fixtures import DUMMY_PASSWORD


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


@pytest.fixture
def run(fixtures, tmp_path, password_env):
    def _run(*extra):
        out = tmp_path / "out"
        input_dir = next(iter(fixtures.values())).parent
        code = be.main(["--input", str(input_dir), "--output", str(out), *extra])
        return code, out
    return _run


# --- filename parsing -------------------------------------------------------

@pytest.mark.parametrize("name,expected", [
    ("2026-09_Bancolombia_CuentaAhorros_6948.pdf", (2026, 9, "savings", "", "6948")),
    ("2020-11_Bancolombia_MasterCard_6879.pdf", (2020, 11, "credit_card", "Mastercard", "6879")),
    ("2024-03_Bancolombia_AmericanExpress_1234.pdf", (2024, 3, "credit_card", "Amex", "1234")),
    ("2024-03_Bancolombia_Visa_7380.PDF", (2024, 3, "credit_card", "Visa", "7380")),
    ("2024-03_Bancolombia_Extracto_0001.pdf", (2024, 3, "", "", "0001")),
])
def test_parse_filename(name, expected):
    info = be.parse_filename(name)
    assert (info.year, info.month, info.account_type, info.brand, info.last4) == expected


def test_parse_filename_rejects_other_names():
    assert be.parse_filename("statement.pdf") is None
    assert be.parse_filename("2024-03_Bancolombia_Other_1234.pdf") is None


def test_account_label():
    assert be.account_label("savings", "", "6948") == "Bancolombia savings 6948"
    assert be.account_label("credit_card", "Visa", "7380") == "Bancolombia Visa 7380"


# --- number / date helpers --------------------------------------------------

@pytest.mark.parametrize("text,value", [
    ("1,234,567.89", "1234567.89"),
    ("-50,000.00", "-50000.00"),
    ("1.234.567,89", "1234567.89"),
    ("-250.000,00", "-250000.00"),
    ("$ 1,000.00", "1000.00"),
    ("$1.000", "1000"),
    ("12.34", "12.34"),
    ("12,34", "12.34"),
    ("(5.00)", "-5.00"),
    ("5.00-", "-5.00"),
])
def test_parse_amount(text, value):
    assert be.parse_amount(text) == Decimal(value)


@pytest.mark.parametrize("text", ["", "abc", "1/12", None])
def test_parse_amount_rejects(text):
    assert be.parse_amount(text) is None


def test_find_period_variants():
    assert be.find_period("DESDE: 2025/11/01 HASTA: 2026/01/31") == (
        be.dt.date(2025, 11, 1), be.dt.date(2026, 1, 31))
    assert be.find_period("Periodo facturado desde 16/01/2025 hasta 15/02/2025")[1] == be.dt.date(2025, 2, 15)
    assert be.find_period("Fecha de corte: 15/03/2025") == (be.dt.date(2025, 2, 16), be.dt.date(2025, 3, 15))


def test_year_inference_across_year_boundary():
    ctx = be.StatementContext("x.pdf", [], "", "", None, be.dt.date(2025, 11, 1), be.dt.date(2026, 1, 31))
    assert ctx.resolve_date("15/12") == (be.dt.date(2025, 12, 15), True)
    assert ctx.resolve_date("5/01") == (be.dt.date(2026, 1, 5), True)


def test_year_inference_from_filename_without_period():
    info = be.parse_filename("2026-01_Bancolombia_CuentaAhorros_6948.pdf")
    ctx = be.StatementContext("x.pdf", [], "", "", info, None, None)
    assert ctx.resolve_date("20/12") == (be.dt.date(2025, 12, 20), False)


# --- unlock -----------------------------------------------------------------

def test_unlock_encrypted_pdf(fixtures, tmp_path, password_env):
    src = fixtures["savings_table"]
    with pytest.raises(pikepdf.PasswordError):
        pikepdf.open(src)
    dst = tmp_path / src.name
    be.unlock_pdf(src, dst, be.PasswordProvider())
    with pikepdf.open(dst) as pdf:
        assert not pdf.is_encrypted


def test_unlock_wrong_password(fixtures, tmp_path, monkeypatch):
    monkeypatch.setenv(be.PASSWORD_ENV, "not-the-password")
    with pytest.raises(ValueError, match="wrong password"):
        be.unlock_pdf(fixtures["savings_table"], tmp_path / "x.pdf", be.PasswordProvider())


def test_password_prompt_used_when_env_missing(fixtures, tmp_path, monkeypatch):
    monkeypatch.delenv(be.PASSWORD_ENV, raising=False)
    monkeypatch.setattr(be.getpass, "getpass", lambda prompt: DUMMY_PASSWORD)
    be.unlock_pdf(fixtures["savings_table"], tmp_path / "x.pdf", be.PasswordProvider())


def test_unlock_only(run):
    code, out = run("--unlock-only")
    assert code == 0
    assert len(list((out / "unlocked").glob("*.pdf"))) == 3
    assert not (out / "transactions.csv").exists()


def test_password_never_written(run, capsys):
    _, out = run("--dump-text")
    assert DUMMY_PASSWORD not in capsys.readouterr().out
    for f in out.rglob("*"):
        if f.is_file() and f.suffix in (".csv", ".txt"):
            assert DUMMY_PASSWORD not in f.read_text(encoding="utf-8")


# --- parse + reconcile ------------------------------------------------------

def test_full_run_outputs(run):
    code, out = run("--dump-text")
    assert code == 0
    for name in ("transactions.csv", "statements.csv", "unparsed_lines.csv"):
        assert (out / name).exists()
    assert (out / "text" / "2025-02_Bancolombia_Visa_7380.txt").exists()
    assert (out / "text" / "2026-01_Bancolombia_CuentaAhorros_6948.tables.txt").exists()
    assert read_csv(out / "transactions.csv")[0].keys() >= set(be.TXN_COLUMNS)


def test_savings_table_year_crossing(run):
    _, out = run()
    rows = [r for r in read_csv(out / "transactions.csv") if r["source_file"].startswith("2026-01")]
    assert [r["date"] for r in rows] == ["2025-11-05", "2025-11-20", "2025-12-15", "2025-12-31", "2026-01-05"]
    assert all(r["parse_confidence"] == "high" for r in rows)
    assert all(r["account"] == "Bancolombia savings 6948" for r in rows)
    market = rows[1]
    assert (market["amount"], market["branch"], market["document_ref"], market["balance_after"]) == (
        "-150000.50", "BOGOTA", "1001", "3349999.50")
    assert market["statement_period_start"] == "2025-11-01"


def test_savings_text_colombian_format_and_unparsed(run):
    _, out = run()
    rows = [r for r in read_csv(out / "transactions.csv") if r["source_file"].startswith("2025-06")]
    assert [(r["date"], r["amount"]) for r in rows] == [("2025-04-10", "1000000.00"), ("2025-05-15", "-250000.00")]
    assert rows[0]["account_type"] == "savings"  # detected from text: filename type is "Extracto"
    assert rows[1]["document_ref"] == "4521"
    unparsed = read_csv(out / "unparsed_lines.csv")
    assert [u["raw_line"] for u in unparsed] == ["20/06 LINEA RARA SIN FORMATO 12.000,00 XX"]


def test_credit_card_signs_currency_and_installments(run):
    _, out = run()
    rows = [r for r in read_csv(out / "transactions.csv") if "Visa" in r["source_file"]]
    by_desc = {r["description"]: r for r in rows}
    assert by_desc["RESTAURANTE CREPES"]["amount"] == "-250000.00"
    assert by_desc["ABONO SUCURSAL VIRTUAL PSE"]["amount"] == "2000000.00"
    assert by_desc["INTERESES CORRIENTES"]["amount"] == "-35000.00"
    electro = by_desc["ALMACEN ELECTRO"]
    assert (electro["amount"], electro["installment"], electro["original_amount"], electro["rate_ea"]) == (
        "-100000.00", "1/12", "1200000.00", "25.1200%")
    assert by_desc["NETFLIX.COM"]["currency"] == "USD"
    assert {r["currency"] for r in rows if r["description"] != "NETFLIX.COM"} == {"COP"}


def test_statements_reconcile(run):
    _, out = run()
    stmts = read_csv(out / "statements.csv")
    assert len(stmts) == 4  # visa has COP + USD sections
    assert all(s["reconciles"] == "yes" for s in stmts), stmts
    savings = next(s for s in stmts if s["source_file"].startswith("2026-01"))
    assert savings["opening_balance"] == "1000000.00"
    assert savings["closing_balance"] == "1950011.84"
    assert savings["parsed_total_credits"] == savings["printed_total_credits"] == "2500012.34"


def test_reconcile_detects_mismatch():
    parser = be.SavingsParser()
    txn = be.Txn(be.dt.date(2025, 1, 1), Decimal("-10.00"), "X", "COP", 1, "l0", "medium", "")
    flag, notes = parser.reconcile("COP", [txn], {"opening": Decimal("100"), "closing": Decimal("100")})
    assert flag == "no" and notes


def test_txn_ids_are_deterministic(run, tmp_path):
    _, out = run()
    first = [r["txn_id"] for r in read_csv(out / "transactions.csv")]
    _, out = run()
    assert first == [r["txn_id"] for r in read_csv(out / "transactions.csv")]
    assert len(set(first)) == len(first)


def test_merge_into(run, tmp_path):
    unified = tmp_path / "transactions_unified.csv"
    with open(unified, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow(be.UNIFIED_COLUMNS)
    run("--merge-into", str(unified))
    rows = read_csv(unified)
    assert len(rows) == 12
    flows = {r["description"]: r["flow_type"] for r in rows}
    assert flows["PAGO TARJETA VISA"] == "card_payment"
    assert flows["ABONO SUCURSAL VIRTUAL PSE"] == "card_payment"
    assert flows["TRANSFERENCIA DESDE PAYONEER"] == "internal_transfer"
    assert flows["ABONO TRANSFERENCIA DESDE WALLBIT"] == "internal_transfer"
    assert flows["RESTAURANTE CREPES"] == "spending"
    assert flows["ABONO INTERESES AHORROS"] == "income"
    run("--merge-into", str(unified))  # re-running must not duplicate rows
    assert len(read_csv(unified)) == 12


def test_default_input_dir(monkeypatch):
    monkeypatch.delenv(be.INPUT_ENV, raising=False)
    assert be.build_arg_parser().parse_args([]).input == be.DEFAULT_INPUT
    monkeypatch.setenv(be.INPUT_ENV, "/somewhere/else")
    assert str(be.build_arg_parser().parse_args([]).input) == "/somewhere/else"
