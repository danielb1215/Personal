# Bancolombia statement extractor

Unlocks password-protected Bancolombia PDF statements and turns them into CSVs.
Run it **on your own computer**: Claude can't open the encrypted PDFs (the Drive
connector returns empty text for them), and the files never need to leave your machine.

The password comes from the `BANCOLOMBIA_PDF_PASSWORD` environment variable or a
hidden prompt. It is never accepted as an argument, printed, logged or saved.

## Setup (once)

macOS / Linux:
```bash
cd tools/bancolombia
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):
```powershell
cd tools\bancolombia
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

Point `--input` at the folder with the PDFs. With Google Drive for Desktop that's
usually something like `~/Library/CloudStorage/GoogleDrive-<you>/My Drive/economics/Extractos Bancolombia`
on macOS or `G:\My Drive\economics\Extractos Bancolombia` on Windows. A downloaded
and extracted zip works too.

macOS / Linux (the leading space keeps the line out of shell history in most setups;
or skip the variable and type the password at the prompt):
```bash
 export BANCOLOMBIA_PDF_PASSWORD='...'
python bancolombia_extract.py --input "/path/to/Extractos Bancolombia" --output ./bancolombia_out
unset BANCOLOMBIA_PDF_PASSWORD
```

Windows PowerShell:
```powershell
$env:BANCOLOMBIA_PDF_PASSWORD = Read-Host "Password"   # typed text is visible; or just let the tool prompt
python bancolombia_extract.py --input "G:\My Drive\economics\Extractos Bancolombia" --output .\bancolombia_out
Remove-Item Env:BANCOLOMBIA_PDF_PASSWORD
```

Useful flags:

| Flag | What it does |
|---|---|
| `--unlock-only` | Only write password-free copies to `unlocked/`. Upload those back to Drive and Claude can read them. |
| `--dump-text` | Also write `text/<file>.layout.txt` (column positions kept) and `text/<file>.tables.txt` (detected tables), so the parser can be adjusted. |
| `--recursive` | Look for PDFs in subfolders too. |
| `--merge-into PATH` | Append the rows to an existing `transactions_unified.csv` (re-runs skip rows already there, by `txn_id`). |

## Outputs (`./bancolombia_out` by default)

- `unlocked/`: password-free PDFs with the same filenames. These are written before any parsing, so they exist even if parsing fails.
- `text/`: raw text of every PDF, page by page.
- `transactions.csv`: one row per movement. `txn_id` is a stable hash of file + page + line, so re-runs give the same IDs. Extra columns `installment`, `original_amount` and `rate_ea` are filled for credit cards.
- `statements.csv`: one row per PDF **per currency section** (a card with a USD section gets a COP row and a USD row). Shows printed opening/closing balances and totals next to the parsed totals, plus `reconciles` = `yes` / `no` / `unknown` (unknown means the opening or closing balance wasn't found). The `error` column holds warnings.
- `unparsed_lines.csv`: lines that start with a date and contain an amount but didn't parse. **Check this file first** when numbers look off.
- A console summary.

The CSVs are UTF-8. In Excel, use Data → From Text/CSV so accents come through correctly.

## Conventions

- **Sign:** `amount` is from your point of view. Negative means money out (spending, withdrawals, card purchases, interest, fees). Positive means money in (deposits, card payments/abonos, refunds).
- **Savings:** `amount` is the VALOR column and `balance_after` is SALDO. Rows without a year (`d/mm`) get it from the statement period (DESDE/HASTA), including periods that cross into a new year. When the running SALDO disagrees with a row's sign, the sign is flipped and the row is marked `low`.
- **Credit cards:** `amount` is the *Cargos y abonos* column, meaning what was billed this month. For a deferred purchase (cuota 1/12) that's the installment, and the full price goes in `original_amount`. Reconciliation tries two formulas: billed (`opening − Σamount = closing`) and total debt (new deferred purchases count at full value, later installments count as 0). `yes` means either one matched, and the `error` column says which.
- **Currency:** a short line with no amounts that contains `DOLARES`/`USD` switches the section to USD, and one with `PESOS` switches it back to COP.
- **parse_confidence:** `high` = read from a detected PDF table; `medium` = regex line parser; `low` = year guessed from the filename, sign flipped, or the row disagrees with the running balance.
- **merge flow_type:** `internal_transfer` if the description contains PAYONEER, WALLBIT, LEAD BANK, TRANSFERENCIA DESDE or ABONO INTERNACIONAL; `card_payment` for PAGO TARJETA/PAGO TC on any account, or ABONO/PAGO credits on a card; otherwise `spending` (negative) or `income` (positive). `needs_review=true` for low-confidence rows.

## When a statement doesn't parse

1. Run with `--dump-text` and open `text/<file>.layout.txt`.
2. Copy a few movement lines plus the header/summary block, **replace names and account numbers with fake ones**, and paste that into a Claude session together with `unparsed_lines.csv` rows.
3. The fix normally goes in `SavingsParser` or `CreditCardParser` in `bancolombia_extract.py` (the regexes, `map_header` keywords, `summary_labels`). For a whole new layout, add a new `BaseParser` subclass and append it to `PARSERS`. Detection picks the parser with the highest `detect()` score; a known filename type adds +100.

## Tests

Tests use synthetic PDFs generated with reportlab (`tests/make_fixtures.py`). One is encrypted with the dummy password `test123`. No real statements are involved.

```bash
pip install -r requirements-dev.txt
python -m pytest tests
```

Never commit real statements or outputs. `.gitignore` in this folder ignores `*.pdf`, `*.csv`, and the output folders.
