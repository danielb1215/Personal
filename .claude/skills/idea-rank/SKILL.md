---
name: idea-rank
description: Score and rank Daniel's side-business ideas in the business_ideas Google Sheet against a weighted rubric (ability to execute, demand evidence from the Pains tab, time to revenue, path to $2-3k MRR, distribution, time fit, capital, lifestyle, unfair advantage). Use when Daniel asks to rank, score, compare or prioritise his business ideas, or to re-score specific ones.
---

# Rank business ideas

Scores ideas in the `business_ideas` Sheet on 9 criteria (1-5 each), applies the knockouts, and
lets the Sheet compute a 0-100 score and the ranking. The judgment is yours; the arithmetic is the
Sheet's (`Ideas!X` and the `Ranking` tab are formulas over the `Rubric` weights).

## Fixed IDs

| What | Value |
|---|---|
| Sheet `business_ideas` | `1N0iOhnKfQDXhDDsYEAGle0jGTp9qMmpRIPL8AglxEIM` |
| Link | https://docs.google.com/spreadsheets/d/1N0iOhnKfQDXhDDsYEAGle0jGTp9qMmpRIPL8AglxEIM |

## Which ideas to score

Arguments decide the set:

- none: every idea whose `ability_to_execute` (column N) is empty and whose status is not `killed`;
- idea ids (`I-261015-2 I-261016-1`): those ideas, even if already scored;
- `all`: every idea that isn't killed (use after Daniel changes the rubric anchors or his situation changes);
- `stale`: ideas with status `shortlisted` or `exploring` whose `scored_on` is more than 30 days old.

If the set is empty, say so, show the current top 5 and stop.

## Rules

- Write only columns N:W and Y:AA of the rows being scored, plus `status` (M) when a knockout kills an idea.
- Never write `Ideas!X`, the `Ranking`, `Pain clusters` or `Rubric` tabs. Never delete rows.
- Don't promote an idea to `shortlisted` or `exploring` yourself; recommend it and let Daniel decide.

## Steps

1. **Context.** Read `ai/persona/profile.md`, `skills.md`, `hobbies.md` and `finances.md`.
   Read `Rubric!A1:F26`: the weights (C2:C10) and the 1/3/5 anchors (D:F) are the scale. Daniel can
   edit them, so always read them rather than assuming.

2. **Read ideas and evidence.** `get_values` on `Ideas!A:AA`, `Pains!A:K` and `'Pain clusters'!A:D`.
   Pick the set above. An idea's pain evidence is the `Pains` rows whose ids appear in its `sources` (L)
   or whose `idea_ids` (K) name it.

3. **Research each idea** (2-3 standard web searches, more for a likely top-5 idea):
   - competitors and their public prices,
   - evidence people pay: job posts with budgets, marketplace listings, founder revenue reports,
   - where the buyers gather, for distribution.
   Reuse the URLs already in `sources` (L) and the linked `Pains` rows where they answer the question.
   If you find new pain evidence, add it to `Pains` with the row format in `/idea-brainstorm` step 5.

4. **Score.** For each criterion, choose 1-5 using the anchors (2 and 4 sit between them).
   Score against Daniel's real situation, not a generic founder's:
   - `ability_to_execute`: can he do it himself, with a partner, or with a cheap hire? Not limited to data skills.
   - `demand`: count the linked `Pains` evidence. 5 needs 3+ independent, recent sources and people
     already paying for a fix; 4 needs 3+ sources or 2 with `paying_now = yes`; an idea with no linked
     pain evidence scores at most 3, however good it sounds.
   - `unfair_advantage`: what he has that most competitors don't: living in Colombia, his cycling,
     diving and music communities, languages, USD income and savings, and his skills.
   - `time_fit` and `lifestyle_fit`: he has 10-15 h/week, evenings, travels often and wants less desk time, not more.
   - `distribution`: credit only channels he has (LinkedIn, ex-colleagues, the dbt and data communities, Bogotá network, Spanish and English).
   - Knockouts (Rubric A14:D18): if any applies, set `knockout` = `yes`, `status` = `killed`, and name the knockout in `score_notes`. Otherwise `knockout` = `no`.
   - `confidence`: `low` from reasoning only, `medium` with desk research, `high` only with a real customer signal Daniel reported.
   - `score_notes`: two or three sentences. Name the strongest and weakest criteria with the evidence behind them, then the cheapest next test that would raise confidence. Include the key URL.
   - `scored_on`: today, `YYYY-MM-DD`.

5. **Calibrate.** Before writing, put your new scores next to the already-scored ideas and check
   that a 5 in each column means the same thing across ideas. Adjust any score that's out of line
   with the anchors, and say which ones you changed and why in your report. Don't change other
   ideas' scores unless they're in the set you were asked to score.

6. **Write.** One `update_values` per contiguous block: `Ideas!N{r}:W{r}` (nine numbers 1-5 in the
   order ability_to_execute, demand, time_to_revenue, mrr_path, distribution, time_fit, capital_risk,
   lifestyle_fit, unfair_advantage, then `yes`/`no` for knockout) and `Ideas!Y{r}:AA{r}` (confidence,
   score_notes, scored_on). Write `killed` to `M{r}` only for knockouts.

7. **Log.** One row to the next empty row of `Runs!A:F`:
   `date, ranking, , <idea_ids scored>, <searches, separated by ; >, <one line on what moved>`.

8. **Verify.** `get_values` on `Ranking!A1:H11` and on the rows you wrote. Every scored idea must
   have a number in X; fix any blank or error before reporting.

9. **Report.**
   - The top 5 from `Ranking` with score, confidence and one line on why each is there.
   - Ideas scored this run with their scores, and any that were knocked out and why.
   - For the #1 idea: the single next validation step for this week, sized for 2-3 evenings.
   - If an idea scores 75 or more with `medium` confidence or better, recommend Daniel shortlist it.
     When he agrees, set its status to `shortlisted`, create
     `ai/entrepreneurship/ideas/<slug>.md` in the format of `b2b-coffee-bogota.md`, and suggest
     `/speckit-specify` to turn it into a launch plan.
