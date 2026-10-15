# Entrepreneurship & Side Business Research

This folder tracks the exploration of parallel income paths and side business ideas for Daniel Bolivar.

## Goal

Find a sustainable side business or income stream that:
- Leverages Daniel's existing data engineering and analytics expertise
- Can be built part-time alongside a full-time job
- Has real market demand and revenue potential
- Aligns with his interests and lifestyle

## Process

1. **Persona complete** → Fill in `../persona/` files (hobbies, finances, values)
2. **Daily demand mining** → A scheduled run every morning uses `/idea-brainstorm` to listen to one community
   (cyclists, bike trade, divers, LatAm travellers, music, online sellers, Colombian businesses, freelancers,
   data people, outdoors, app reviews, endurance coaches), logs real complaints with links in the `Pains` tab
   of the [`business_ideas`](https://docs.google.com/spreadsheets/d/1N0iOhnKfQDXhDDsYEAGle0jGTp9qMmpRIPL8AglxEIM)
   Sheet, and turns a pain into an idea only when it repeats (3+ sources) or people already pay to fix it
3. **Rank** → `/idea-rank` researches and scores unscored ideas on the weighted rubric; the Sheet's `Ranking` tab sorts them
4. **Shortlist** → Ideas that score 75+ with medium confidence get a file in `ideas/` and `/speckit-specify`
5. **Planning** → Use `/speckit-plan` + `/speckit-tasks` to build execution roadmap
6. **Execute** → Track progress in `ideas/` and `experiments/` folders

## The `business_ideas` Sheet

| Tab | What it holds |
|---|---|
| `Ranking` | Sorted view of scored ideas (formula; killed ideas hidden) |
| `Ideas` | One row per idea: A:M written by the brainstorm, N:W and Y:AA by the ranking, X = score (formula) |
| `Pains` | One row per piece of evidence: a real complaint or request, with quote, link and whether people pay today |
| `Pain clusters` | Pains grouped by label with evidence counts (formula) |
| `Rubric` | The 9 criteria, their weights (blue, editable) and 1/3/5 anchors, plus knockouts |
| `Runs` | Log of every brainstorm and ranking run |

Score = weighted average of the 1-5 criterion scores, scaled to 0-100. Changing a weight on `Rubric`
re-ranks every idea instantly.

## Folders

- `ideas/` — shortlisted business ideas with deeper analysis (the full backlog lives in the Sheet)
- `experiments/` — active experiments / MVPs being tested
- `research/` — market research, competitor analysis, pricing data

## Status

> 🔄 In progress — persona context being built
