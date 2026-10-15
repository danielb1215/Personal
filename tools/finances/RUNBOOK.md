# Monthly finances sync — runbook for the scheduled Claude run

This runs on the 6th of every month. Follow every step in order. If a step fails, stop before
writing anything to the Sheet, and finish with a short report of what failed.

## Fixed IDs

| What | ID |
|---|---|
| Sheet `finances_unified` | `1YeZ1p34fgsvv1sDIuNFrausv0FE0lFLG86AVsfwrdd8` |
| Drive `economics/inbox` (Daniel drops files here) | `1vTMiK66f-5K8pcthbNfMyp_hh0QBuTkw` |
| Drive `economics/inbox/processed` | `1fBB32hoVMiAArtKJt7yFSkYE7DRBtTm_` |
| Dashboard | https://claude.ai/artifact/X45ZBs1U67E9in6MeZHf9P (reads the Sheet; nothing to do) |

## Rules

- Never ask for, store or print the Bancolombia PDF password. Encrypted PDFs are skipped and reported.
- Never delete Drive files or Sheet rows. Only append to `Transactions`, update the rows `updates.json`
  lists, and write the `Balances` and `FX rates` cells the script outputs.
- Keep downloaded files in a scratch work folder, never in the git repo.

## Steps

1. **Code.** `cd` into the `danielb1215/Personal` checkout (the repo's default branch, currently
   `claude/spec-kit-personal-ai-folder-se4e7v`). If `tools/finances/monthly.py` is missing there,
   `git fetch origin claude/amazing-gates-mpo7ev` and check that branch out.
   Make a work folder `W` (scratchpad) with `W/inbox/`.

2. **Ledger and balances.** `get_values` `Transactions!A1:R` (the result is saved to a file; copy that
   file to `W/ledger.json`) and `Balances!A1:G20` (write to `W/balances_current.json` as
   `{"values": [...]}`).

3. **Inbox files.** `search_files` with `parentId = '1vTMiK66f-5K8pcthbNfMyp_hh0QBuTkw'` (skip folders).
   For each file:
   - **CSV** (Payoneer, Rippling, Wise, the Bancolombia `transactions.csv` from Daniel's local tool, or
     `apple_wallet_transactions.csv` from his Mac's nightly Wallet export):
     `download_file_content`, then `python3 tools/finances/decode.py <saved result or base64 file> W/inbox/<title>`.
   - **Wallbit statement PDF:** `read_file_content`, transcribe every movement into
     `W/inbox/wallbit_<YYYY-MM>.csv` with header
     `date,description,counterparty,status,operation_id,amount_usd,balance_usd,note`
     (oldest first; amounts signed; failed/not-settled rows with amount 0 and a note).
     Run `python3 tools/finances/validate.py wallbit <file>` and fix until it prints OK and the
     closing balance equals the statement's.
   - **Banco de Bogotá card statement PDF** (`Extracto_Cuenta_CCA_*`): `read_file_content`, transcribe
     every line into `W/inbox/cc_bdb_<cut>.csv` with header
     `statement_cut,comprobante,description,date_txn,date_post,plazo,amount_cop,cuota_mes,cuotas_pend,saldo_pend`
     (payments negative, `plazo` as on the statement, e.g. `01`, `36`). Run
     `python3 tools/finances/validate.py bdb <file>` and check the totals against the PDF summary.
     Add the amount to pay to `W/statement_balances.json`:
     `[{"account": "Banco de Bogotá Visa 2320", "balance": -<total a pagar>, "as_of": "<cut date>", "source": "card statement cut <date>, due <date>"}]`.
   - **Anything else, or a PDF that comes back empty/encrypted:** leave it in the inbox and list it in the report.

4. **Bancolombia alert emails.** Find the latest date among `Transactions` rows whose `txn_id` starts
   with `BCE-` or `BC-` and account `Bancolombia savings 6948`; go back 3 days. Gmail `search_threads`
   with `from:(notificacionesbancolombia.com OR alertasynotificaciones@bancolombia.com.co) after:YYYY/MM/DD`
   (page through all results; `get_thread` for any thread with more than 5 messages, since previews
   show only the oldest 5). Write `W/bc_alerts.json` as `[{"id": <message id>, "date": <message date>, "text": <snippet>}]`
   — one entry per message, all of them; the script ignores the non-movement ones and the duplicates.

5. **Run.** `cd tools/finances && python3 monthly.py W`. Read `W/out/summary.md` and skim
   `W/out/new_rows.csv`. Stop and report instead of writing if it would append more than 600 rows,
   or if the same transaction appears twice. In particular, a card purchase must not appear both as
   an `APW-` row and as a statement/Payoneer row; `updates.json` is where Wallet rows turn into
   statement rows. Copy the summary's "Apple Wallet" and "Wallet cards with no ledger account"
   lines into the report. If `apple_wallet_transactions.csv` is missing or its newest date is more
   than 5 days old, say so in the report (the Mac's nightly export or the iPhone backup has stopped).

6. **Write to the Sheet.**
   - `append_values` range `Transactions!A1` with the `values` from `W/out/append.json`
     (in chunks of at most 500 rows; skip if empty).
   - For each entry in `W/out/updates.json`: `update_values` with its `range` and `values`.
   - For each entry in `W/out/balances_updates.json`: `update_values`.
   - `update_values` `'FX rates'!A1` with `W/out/fx_values.json`.
   - Check: `get_values` the last few rows of `Transactions` and confirm the appended rows are there.

7. **Tidy up.** Move every file you processed into `processed` (`update_file` with
   `parentId = '1fBB32hoVMiAArtKJt7yFSkYE7DRBtTm_'`).

8. **Report.** Your final message is emailed to Daniel. Make it the contents of `summary.md`, plus:
   files you couldn't read, anything you stopped on, and links to the Sheet
   (https://docs.google.com/spreadsheets/d/1YeZ1p34fgsvv1sDIuNFrausv0FE0lFLG86AVsfwrdd8) and the dashboard.
   Keep it short.
