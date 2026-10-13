# Finance review (Oct 2026)

Scripts behind the dashboard https://claude.ai/artifact/83Z3NBvdoFkP7Me7vUto6M.

1. Save `Transactions!A1:T` from the Sheet (`get_values`) as `W/ledger.json`.
2. `python3 analyze.py W` computes cash, idle-cash floors, inflation cost, 12-month flows,
   categories, recurring charges, emergency fund and goal figures into `W/data.json`.
3. `python3 build_ds.py W` turns that plus the dated market inputs into the dashboard's
   dataset files in `W/ds/`.

Fixed inputs (balances, CPI, TRM, yields, eToro snapshot) sit at the top of each script with
their dates; update them before re-running.
