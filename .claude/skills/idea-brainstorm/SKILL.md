---
name: idea-brainstorm
description: Daily brainstorm of side-business ideas for Daniel. Picks the next lens in a fixed rotation, researches it on the web, adds 3 new ideas to the business_ideas Google Sheet and logs the run. Use when Daniel asks for new business ideas, or when the daily scheduled brainstorm fires.
---

# Daily business idea brainstorm

Produces **3 new, concrete side-business ideas** a day for Daniel, each written as a row in the
`business_ideas` Google Sheet. Ideas are not scored here; `/idea-rank` does that.

Daniel describes himself as not very creative at idea generation, so this skill does the
divergent part for him: a different **lens** each day forces new territory, and web research
grounds each idea in what people pay for today.

## Fixed IDs

| What | Value |
|---|---|
| Sheet `business_ideas` | `1N0iOhnKfQDXhDDsYEAGle0jGTp9qMmpRIPL8AglxEIM` |
| Link | https://docs.google.com/spreadsheets/d/1N0iOhnKfQDXhDDsYEAGle0jGTp9qMmpRIPL8AglxEIM |
| Tabs | `Ideas` (one row per idea), `Ranking` (formula view, never write), `Rubric`, `Runs` (log) |

## Rules

- Only add rows. Never edit or delete existing rows in `Ideas` or `Runs`.
- Never write to the `Ranking` tab or to `Ideas` column W (`score`): both are formulas.
- Leave the score columns (N:V, X:Z) empty. Scoring is `/idea-rank`'s job.
- Don't commit anything to the repo. The Sheet is the record.

## Steps

1. **Context.** Read `ai/persona/profile.md`, `skills.md`, `hobbies.md` and `finances.md`.
   The constraints in `finances.md` (10-15 h/week, async, revenue in 3-6 months, $2-3k MRR goal,
   staged capital up to $5-10k) and the knockouts on the `Rubric` tab (A12:D17) are hard limits.

2. **Read the Sheet.** `get_values` on `Ideas!A:M` (existing ideas, to avoid duplicates and to find
   the next empty row), `Runs!A:F` (past lenses) and `Ranking!A1:H11` (current top 10).

3. **Pick the lens.** Take the last `Runs` row with type `brainstorm`, and use the next lens in the
   table below (after 12, wrap to 1). If there are no brainstorm runs yet, start at 1. If the user
   names a lens or topic, use that instead.

   | # | Lens | Prompt to yourself |
   |---|---|---|
   | 1 | Own-job pain | What costs data teams like his hours or money every week? Productize the fix, with no Crowd Cow data, code or clients. |
   | 2 | Tool ecosystems | Gaps around dbt, BigQuery, Looker, Fivetran, Datastream: missing packages, plugins, audits, migrations, templates. |
   | 3 | Cost cutting as a service | He cut data-ops costs 67.5% in a Snowflake to BigQuery migration. Who overpays for warehouses, ETL or BI seats now? |
   | 4 | AI and agents | What do small companies need now that LLMs, agents and MCP exist: data prep for AI, MCP servers, LLM pipelines, evals? |
   | 5 | Underserved verticals | Industries with data but no analysts: DTC e-commerce, subscriptions, gyms, clinics, restaurants, agencies, especially in LatAm. |
   | 6 | LatAm arbitrage | US prices with a Bogotá cost base; bilingual delivery; LatAm companies adopting a modern data stack; nearshore teams. |
   | 7 | Hobbies x data | Cycling, scuba, freediving, hiking, house and techno festivals, travel: data products or tools for those communities. |
   | 8 | Content and education | Courses, cohort classes, templates, newsletters or YouTube in Spanish or English on data engineering and analytics. |
   | 9 | Demand mining | Search Upwork and Contra job posts, r/dataengineering, r/analytics, Indie Hackers for repeated requests people pay for. |
   | 10 | Unbundle a winner | Find a profitable micro-SaaS or agency in data or analytics and design a narrower, cheaper version for one niche. |
   | 11 | Bogotá local | Physical-world businesses in Bogotá that a data-minded operator could run part-time (like the B2B coffee idea). |
   | 12 | Remix | Combine two existing ideas, aim the top-ranked idea at a new customer, or fix why a killed idea died. |

4. **Research.** Run 3 to 5 web searches for the lens (standard mode), aimed at evidence of
   spending: pricing pages, job posts with budgets, complaints about existing tools, revenue
   reports from founders. Keep the URLs you actually use.

5. **Generate 3 ideas.** Draft about 8 privately, then keep the 3 that are most specific and best
   fit Daniel. Each kept idea must:
   - name a specific customer ("Shopify brands doing $1-10M/year", not "businesses"),
   - charge money in a clear way, with a price,
   - have a first test Daniel can run within a week for under $100 (landing page, 10 outreach
     messages, a post in a community, a pre-sale),
   - not duplicate an existing row (same customer and same offer is a duplicate; a new customer
     segment for an existing offer is fine if you say so in the pitch),
   - pass every knockout on the `Rubric` tab.

6. **Write the rows.** Find the first empty row after the last `idea_id` in `Ideas!A:A` and write
   `A{n}:M{n+2}` with `update_values` (explicit range, not `append_values`). Columns:

   | Col | Field | How to fill |
   |---|---|---|
   | A | idea_id | `I-YYMMDD-k`, k = 1, 2, 3 (today's date) |
   | B | added | today as `YYYY-MM-DD` |
   | C | lens | lens name from the table |
   | D | title | under 70 characters |
   | E | pitch | one or two sentences: what it is and who pays |
   | F | customer | the specific buyer |
   | G | problem | the pain, in the customer's terms |
   | H | why_daniel | which of his skills, experience or network makes him credible |
   | I | revenue_model | retainer, subscription, one-off project, course, marketplace fee, etc. |
   | J | price | e.g. `$1,500 one-off audit` or `$49/month`; prefix with `'` if it starts with `=` or looks like a number |
   | K | first_test | the one-week, under-$100 test |
   | L | sources | the URLs that support the idea, separated by spaces |
   | M | status | `new` |

7. **Log the run.** Write one row to the next empty row of `Runs!A:F`:
   `date, brainstorm, <lens>, <comma-separated idea_ids>, <search queries used, separated by ; >, <one line: what you noticed>`.

8. **Verify.** `get_values` the rows you wrote and check every column landed where it should.

9. **Report.** The final message (emailed to Daniel on scheduled runs) has:
   - today's lens,
   - the 3 ideas: title, pitch, price and first test, one short block each,
   - the current top 3 from the `Ranking` tab with scores, and how many ideas are still unscored,
   - the Sheet link, and a reminder that `/idea-rank` scores the new ideas.

   Keep it short and plain; no tables wider than a phone screen.
