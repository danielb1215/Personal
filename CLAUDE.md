# Personal Repo — Claude Instructions

## Who This Repo Is For

This is **Daniel Bolivar's** personal workspace. See `ai/CONTEXT.md` for full orientation.

## Always Start Here

Before any task in this repo, read:
- `ai/persona/profile.md`
- `ai/persona/skills.md`
- `ai/persona/hobbies.md` (once filled)

This context shapes every recommendation — business ideas, plans, and experiments should fit *Daniel's* specific skills, lifestyle, and goals.

## Primary Mission

Find and build a **parallel income stream or side business** that:
- Leverages Daniel's 5+ years of data engineering expertise
- Can run part-time alongside his current job at Crowd Cow
- Has real revenue potential within 3–6 months of starting

## Personal Finances Database

Daniel's finances live in the Google Sheet **`finances_unified`**:
https://docs.google.com/spreadsheets/d/1YeZ1p34fgsvv1sDIuNFrausv0FE0lFLG86AVsfwrdd8

Read it with the Google Sheets connector (connect it at claude.ai/customize/connectors before the session starts). Read-only unless Daniel asks for changes; never rewrite or delete existing rows.

- **Transactions** — one row per movement across Bancolombia, Banco de Bogotá Visa, Payoneer, Rippling, Wallbit and Wise. Columns A:R: `txn_id, date, account, currency, amount, amount_usd, fx_note, flow_type, category, description, counterparty, match_id, match_account, est_other_ccy, is_duplicate, needs_review, notes, source_file`; S = `month`, T = `summary_group` (formulas).
  - Compare across currencies with `amount_usd`.
  - When totalling spending, skip `is_duplicate = yes` and moves between his own accounts (`flow_type` `internal_transfer`, `fx_conversion`, `card_payment`).
- **Balances** — latest balance per account; USD in column F, cash total F13, net worth F14.
- **Monthly (USD equiv)**, **Spending by cat (USD)**, **Payouts by recipient**, **FX rates**, **Needs review** — summary tabs built from Transactions.
- Dashboard (reads the Sheet): https://claude.ai/artifact/X45ZBs1U67E9in6MeZHf9P
- How the data is built and kept up to date: `tools/finances/README.md`. A scheduled run on the 6th follows `tools/finances/RUNBOOK.md`.

## Business Ideas Pipeline

- Backlog and ranking live in the Google Sheet **`business_ideas`**:
  https://docs.google.com/spreadsheets/d/1N0iOhnKfQDXhDDsYEAGle0jGTp9qMmpRIPL8AglxEIM
- `/idea-brainstorm` — adds 3 ideas using the next lens in the rotation (runs daily as a scheduled task)
- `/idea-rank` — scores unscored ideas against the `Rubric` tab; pass idea ids, `all` or `stale` to re-score
- See `ai/entrepreneurship/README.md` for the full process.

## Spec-Kit Skills Available

- `/speckit-specify` — define a business idea as a spec
- `/speckit-plan` — create an implementation/launch plan
- `/speckit-tasks` — generate actionable task lists
- `/speckit-implement` — execute tasks
- `/speckit-clarify` — ask structured questions to sharpen ideas
- `/speckit-analyze` — validate consistency across plans

## Working Principles

- Ground all suggestions in Daniel's **actual skills** — no generic advice
- Prefer **low-capital, high-skill** business models (consulting, tools, content)
- Validate demand before building — research first, build second
- Keep experiments small and testable before committing significant time
