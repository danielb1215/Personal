---
name: idea-brainstorm
description: Daily demand-first idea run for Daniel. Listens to one community a day (forums, blogs, social, app reviews, news), logs real complaints with links in the Pains tab of the business_ideas Google Sheet, and turns only repeated or paid-for pains into business ideas. Use when Daniel asks for new business ideas, pain points or demand research, or when the daily scheduled run fires.
---

# Daily demand-first idea run

Ideas come **from evidence of demand, not from Daniel's CV**. Each day:

1. listen to one community where people complain, ask for help or say what they pay for,
2. log every real pain with a link in the `Pains` tab,
3. turn a pain into an idea only when it repeats or people already spend money on it.

A day with good pains and no new idea is a good day. Never invent a pain to justify an idea.

## Fixed IDs

| What | Value |
|---|---|
| Sheet `business_ideas` | `1N0iOhnKfQDXhDDsYEAGle0jGTp9qMmpRIPL8AglxEIM` |
| Link | https://docs.google.com/spreadsheets/d/1N0iOhnKfQDXhDDsYEAGle0jGTp9qMmpRIPL8AglxEIM |
| Tabs | `Ranking` (formula), `Ideas`, `Pains` (evidence), `Pain clusters` (formula), `Rubric`, `Runs` (log) |

## Rules

- Only add rows. Never edit or delete existing rows, except filling `idea_ids` (K) on `Pains` rows
  that a new idea uses.
- Never write to `Ranking`, `Pain clusters` or `Ideas` column X (`score`): they are formulas.
- Every `Pains` row needs a real, working `source_url` you actually saw in a search result or page.
  Put verbatim words in double quotes; otherwise start with `[paraphrase]`. No made-up quotes.
- Prefer recent evidence (last 2 years). Vendor blogs and listicles that sell a fix are not evidence
  of pain; forum posts, reviews, comments, job posts and news are.
- Don't commit anything to the repo. The Sheet is the record.

## Steps

1. **Context.** Read `ai/persona/finances.md` for the hard limits (10-15 h/week, async, revenue in
   3-6 months, $2-3k/month goal, $5-10k staged capital) and the knockouts on `Rubric!A13:D18`.
   Read the other persona files only at step 6, after the pains are collected, so they don't steer
   what you look for.

2. **Read the Sheet.** `get_values` on `Pains!A:K`, `'Pain clusters'!A:D`, `Ideas!A:M`, `Runs!A:F`
   and `Ranking!A1:H11`.

3. **Pick where to listen.** Take the last `Runs` row with type `brainstorm` and use the next
   community below (after 12, wrap to 1); if its `lens` isn't a community name from this table,
   start at 1. If Daniel names a community, topic or pain, use that.

   | # | Community | Where to look |
   |---|---|---|
   | 1 | Road cyclists and bike owners | Bike Forums, TrainerRoad forum, Weight Weenies, RoadBikeReview, Slowtwitch, BikeRadar and road.cc comments |
   | 2 | Bike shops, brands and the bike trade | Bicycle Retailer, Bike Europe, BikeBiz, NBDA, shop-owner forums |
   | 3 | Divers and freedivers | ScubaBoard, DeeperBlue, dive-travel reviews |
   | 4 | Travellers and nomads in Latin America | Nomad List, travel forums, expat forums for Colombia and Mexico, TripAdvisor forums |
   | 5 | Electronic music fans, DJs and promoters | Resident Advisor, DJ forums, festival reviews and news |
   | 6 | Small online sellers | Shopify Community, Seller Central forums, ecommerce blogs' comment threads |
   | 7 | Small businesses in Colombia and Latin America | Colombian business news, emprendimiento blogs, Mercado Libre seller forums |
   | 8 | Freelancers and remote workers paid in USD | freelancer forums, Upwork Community, fintech reviews (Trustpilot) |
   | 9 | Data and analytics people | dbt Discourse, Locally Optimistic, Hacker News, Stack Overflow |
   | 10 | Hikers, campers and outdoor people | Backpacker forums, AllTrails reviews, outdoor gear reviews |
   | 11 | App and software reviews | 1-3 star reviews on the App Store, Google Play, G2, Capterra, Trustpilot for popular tools in communities 1-10 |
   | 12 | Endurance athletes and coaches | TrainerRoad, Slowtwitch, TrainingPeaks forum, running forums |

4. **Mine for pain.** Run 6-10 web searches (standard mode; extended for niche or Spanish-language
   sources) that pair the community with pain phrases, for example: `"is there an app"`,
   `"I wish there was"`, `"I'd pay for"`, `"so frustrating"`, `"anyone else"`, `"how do you deal with"`,
   `"alternative to"`, `"scam"`, `"waste of money"`, or in Spanish `"ojalá existiera"`, `"alguien sabe"`,
   `"estafa"`, `"me cobraron"`. Search in Spanish for Colombian and Latin American communities.
   If `WebFetch` or `curl` can open a thread, read it for exact quotes and reply counts.
   Reddit, X and some forums are blocked in some environments; don't retry blocked hosts, use what
   search returns.

5. **Log pains.** Write 6-15 rows to the next empty rows of `Pains!A:K` with `update_values`:

   | Col | Field | How to fill |
   |---|---|---|
   | A | pain_id | `P-YYMMDD-k`, k counting up from the day's last id |
   | B | found | today, `YYYY-MM-DD` |
   | C | community | who has the pain |
   | D | pain | a short label in the customer's terms. Reuse an existing label exactly when it's the same pain, so `Pain clusters` counts it |
   | E | what_they_said | verbatim in quotes, or `[paraphrase] ...`; include engagement (replies, votes) when known |
   | F | source_url | the thread, review or article |
   | G | source_type | forum, social, app review, blog, news, job post, video, conversation |
   | H | posted_year | number, blank if unknown |
   | I | paying_now | `yes` if they already pay or try to pay for a fix (tools, services, fees), `no`, or `unclear` |
   | J | workaround | what they do today |
   | K | idea_ids | leave blank unless an idea uses it |

6. **Turn strong pains into ideas.** Now read `ai/persona/profile.md`, `skills.md` and `hobbies.md`.
   A pain qualifies when `Pain clusters` (after your writes) shows 3 or more pieces of evidence, or 2 with
   `paying_now = yes`. For each qualifying pain without an idea yet, design 0-3 ideas:
   - the idea must remove that pain for that community, priced against what they pay today;
   - any business model is allowed (service, product, marketplace, physical goods, travel, software,
     content, buying a business); don't default to data consulting;
   - name a specific customer, a price, and a first test Daniel can run in a week for under $100;
   - check the knockouts and his time and capital limits;
   - no duplicates of existing `Ideas` rows (same customer and offer).

   Write each idea to the next empty row of `Ideas!A:M` (A `I-YYMMDD-k`, B today, C `Pain: <pain label>`,
   D title, E pitch, F customer, G problem in the customer's words, H his unfair advantage,
   I revenue model, J price, K first test, L the pain_ids then key URLs separated by spaces, M `new`).
   Fill `idea_ids` (K) on the `Pains` rows it uses. Leave scores to `/idea-rank`.

7. **Log the run.** Next empty row of `Runs!A:F`: `date, brainstorm, <community name>,
   <idea_ids or blank>, <searches separated by ; >, <one line: strongest pain and how often it appeared>`.

8. **Verify.** `get_values` the rows you wrote and `'Pain clusters'!A1:D15`; fix anything misplaced.

9. **Report.** The final message (emailed on scheduled runs), short enough for a phone:
   - today's community and the 3 strongest pains, each with one quote and link,
   - pains that are getting close to qualifying (2 pieces of evidence),
   - new ideas, if any: title, the pain behind it, price, first test,
   - the current top 3 from `Ranking`, how many ideas are unscored, and the Sheet link.
