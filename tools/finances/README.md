# Finances pipeline

Keeps the `finances_unified` Google Sheet (and the dashboard that reads it) up to date.

## Daniel's monthly checklist (~10 min, by the 5th)

Drop these into Drive → `economics/inbox` (any file name):

1. **Banco de Bogotá Visa 2320** — last month's card statement PDF (app or portal → Extractos).
2. **Payoneer** — Activity → Download → CSV, last month, USD and EUR.
3. **Wallbit** — last month's statement PDF.
4. **Rippling** — wallet transactions CSV export (whole history is fine).
5. **Wise** — balance statement CSV, only if Wise was used that month.

Every quarter (Jan, Apr, Jul, Oct): run the local Bancolombia extractor on the new
statement and drop its `transactions.csv` in the same folder. It checks the closing balance and
picks up the interest and fees that the alert emails don't mention.

Bancolombia day to day needs nothing: its alert emails are read automatically.

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

Rows in the Sheet are never rewritten except to add a transfer match, or to swap a Bancolombia
alert-email row (`BCE-…`) for the statement row it turned into. Edits you make to categories and
notes stay.
