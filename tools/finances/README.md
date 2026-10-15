# Finances pipeline

Keeps the `finances_unified` Google Sheet (and the dashboard that reads it) up to date.

## Daniel's monthly checklist (~10 min, by the 5th)

Drop these into Drive → `economics/inbox` (any file name):

1. **Banco de Bogotá Visa 2320** — last month's card statement PDF (app or portal → Extractos).
   Once the Apple Wallet export runs (below), purchases arrive without it. The statement is still
   what confirms the total and brings interest, insurance, installments and payments, so drop it
   whenever you have it. Wallet rows are swapped for statement rows when it comes.
2. **Payoneer** — Activity → Download → CSV, last month, USD and EUR. Card purchases arrive earlier
   through Wallet; the CSV still brings balances, transfers and conversions.
3. **Wallbit** — last month's statement PDF.
4. **Rippling** — wallet transactions CSV export (whole history is fine).
5. **Wise** — balance statement CSV, only if Wise was used that month.

Every quarter (Jan, Apr, Jul, Oct): run the local Bancolombia extractor on the new
statement and drop its `transactions.csv` in the same folder. It checks the closing balance and
picks up the interest and fees that the alert emails don't mention.

Bancolombia day to day needs nothing: its alert emails are read automatically.

**Apple Wallet (automatic once set up):** a nightly job on the Mac reads card purchases from the
encrypted iPhone backup and writes `apple_wallet_transactions.csv` into the inbox. Setup:
[`tools/wallet_backup/README.md`](../wallet_backup/README.md). Which Wallet card goes to which
ledger account is in [`wallet_cards.json`](wallet_cards.json).

On the 6th a scheduled Claude run follows [RUNBOOK.md](RUNBOOK.md), appends the new rows,
updates balances and FX rates, moves the files to `inbox/processed`, and emails a summary.

## Files

| File | What it does |
|---|---|
| `finlib.py` | Parsers for each source, categories, transfer matching, FX |
| `monthly.py` | Incremental sync: Sheet ledger + new files → rows to append and update |
| `build_full.py` | Full rebuild from every raw file (how the Sheet was first built) |
| `validate.py` | Checks hand-transcribed Wallbit / Banco de Bogotá statements |
| `decode.py` | Turns a Drive download (base64) back into the file |
| `wallet_cards.json` | Apple Wallet card → ledger account (edit when a card changes) |
| `tests/` | `python3 -m unittest discover -s tests` (synthetic data; includes a check that the sync without Wallet files behaves as before) |

Rows in the Sheet are never rewritten except to add a transfer match, or to swap a stand-in row
for the statement row it turned into: a Bancolombia alert-email row (`BCE-…`) or an Apple Wallet
row (`APW-…`). Edits you make to categories and notes stay.

### How Apple Wallet rows are reconciled

Wallet rows (`APW-…`) only cover days the card's own source doesn't cover yet: the Banco de
Bogotá statement, the Payoneer CSV, or the Bancolombia card statement. For each card, "covered"
means up to the latest date of a non-Wallet row in that card's accounts.

- When a statement/CSV row arrives, it is matched to an open Wallet row with the same card, the
  same sign, a date within ±3 days, and an amount within 1% in the same currency or within 8% after
  FX. Banco de Bogotá bills a EUR purchase in COP, so the Wallet amount is converted with the
  sheet's monthly COP/USD and USD/EUR medians. When the amount isn't exact, the merchant names must
  also agree. The Wallet row in the Sheet is then **updated in place** into the statement row:
  id, date, amount, currency, description. Your category and notes are kept, and
  `est_other_ccy` records the Wallet amount, for example `Apple Wallet EUR 45.90`.
- If both arrive in the same month, the statement row is used and the Wallet row isn't added.
- Wallet rows dated inside an already covered period aren't added.
- A Wallet row that the statement passed by more than 3 days without a match is flagged in
  `needs_review` (reversed, declined, or posting next cycle). It stays open, so a later
  statement can still match it.
- Pending Wallet rows are updated to the settled amount on a later export.
- Payoneer USD and EUR count as one card, so a EUR purchase charged to the USD balance still matches.
- Bancolombia card purchases that already came in as alert emails (`COMPRA EN …`) are skipped.
  The Bancolombia debit card is ignored in `wallet_cards.json` because the savings statement and
  the alerts already have it.
