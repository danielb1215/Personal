---
name: idea-brainstorm
description: Daily brainstorm of side-business ideas for Daniel. Picks the next lens in a fixed rotation, researches it on the web, adds 3 new ideas to the business_ideas Google Sheet and logs the run. Use when Daniel asks for new business ideas, or when the daily scheduled brainstorm fires.
---

# Daily business idea brainstorm

Produces **3 new, concrete side-business ideas** a day for Daniel, each written as a row in the
`business_ideas` Google Sheet. Ideas are not scored here; `/idea-rank` does that.

Daniel describes himself as not very creative at idea generation, so this skill does the
divergent part for him: a different **lens** each day forces new territory, and web research
grounds each idea in what people pay for today. Most lenses deliberately ignore his data job, so
the backlog isn't just variations of data consulting.

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
   table below (after 12, wrap to 1). If there are no brainstorm runs yet, or the last lens isn't in this table, start at 1. If the user
   names a lens or topic, use that instead.

   | # | Lens | Prompt to yourself |
   |---|---|---|
   | 1 | Trends first | What is growing fast in 2026 (search trend reports, new platforms, regulation changes)? Find the businesses that growth creates before thinking about Daniel. |
   | 2 | Colombia as an advantage | What can be made, run or hosted in Colombia and sold to people abroad: manufacturing, tourism, talent, a low cost base? |
   | 3 | Cycling and outdoors | Products, travel, events, services or communities for riders, hikers and outdoor people. Not data services. |
   | 4 | Water and travel | Diving, freediving, festivals, short-trip travel: what do people in those worlds pay for and complain about? |
   | 5 | Buy instead of build | Small profitable businesses for sale (Flippa, Acquire, local businesses) that $5-10k could buy and he could grow. |
   | 6 | Physical products | Private label, Colombian-made goods, accessories, consumables sold online. |
   | 7 | Marketplaces and communities | Two groups he can reach that would pay to find each other. |
   | 8 | AI-native products | Things only possible since cheap AI models: consumer apps, tools for small businesses, automations people pay for. |
   | 9 | His own problems as a person | What annoys him as a cyclist, traveller, diver, USD earner in Colombia, gear owner? Who else has that problem? |
   | 10 | Demand mining | Upwork and Contra posts, Reddit, Indie Hackers, review sites: repeated requests people say they would pay for. |
   | 11 | Data and tech services | His day-job skills sold as consulting, audits or tools. Only this lens may produce data services. |
   | 12 | Remix and inversions | Combine two existing ideas, aim the top-ranked idea at a new customer, or fix why a killed idea died. |

4. **Research.** Run 3 to 5 web searches for the lens (standard mode), aimed at evidence of
   spending: pricing pages, job posts with budgets, complaints about existing tools, revenue
   reports from founders. Keep the URLs you actually use.

5. **Generate 3 ideas.** Draft about 8 privately from the lens and the research alone, before
   checking them against Daniel's profile: start from a market, a trend or a problem, not from his CV.
   Then keep the 3 that are most specific and most different from each other and from the existing
   rows. Rules against anchoring on his CV:
   - Outside lens 11, no idea may be a data, analytics or BI service, audit or dashboard.
   - At least one of the 3 must be something a person without his data background could also run;
     his advantage there comes from his life (Colombia, cycling, diving, travel, languages, USD
     income, savings), not his job.
   - Don't reuse phrases from his CV (job titles, "67.5%", tool names) in `why_daniel` unless the idea
     truly depends on them.

   Each kept idea must:
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
   | H | why_daniel | his unfair advantage: location, network, hobbies, languages, capital, or skills |
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
