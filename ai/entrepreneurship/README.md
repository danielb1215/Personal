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
2. **Daily brainstorm** → A scheduled run every morning uses `/idea-brainstorm` to add 3 ideas to the
   [`business_ideas`](https://docs.google.com/spreadsheets/d/1N0iOhnKfQDXhDDsYEAGle0jGTp9qMmpRIPL8AglxEIM) Sheet,
   rotating through 12 lenses (trends, Colombia as an advantage, cycling and outdoors, water and travel,
   buying a business, physical products, marketplaces, AI-native products, his own problems, demand mining,
   data services, remix). Only one lens produces data services, so the backlog isn't all consulting
3. **Rank** → `/idea-rank` researches and scores unscored ideas on the weighted rubric; the Sheet's `Ranking` tab sorts them
4. **Shortlist** → Ideas that score 75+ with medium confidence get a file in `ideas/` and `/speckit-specify`
5. **Planning** → Use `/speckit-plan` + `/speckit-tasks` to build execution roadmap
6. **Execute** → Track progress in `ideas/` and `experiments/` folders

## The `business_ideas` Sheet

| Tab | What it holds |
|---|---|
| `Ranking` | Sorted view of scored ideas (formula; killed ideas hidden) |
| `Ideas` | One row per idea: A:M written by the brainstorm, N:V and X:Z by the ranking, W = score (formula) |
| `Rubric` | The 8 criteria, their weights (blue, editable) and 1/3/5 anchors, plus knockouts |
| `Runs` | Log of every brainstorm and ranking run |

Score = weighted average of the 1-5 criterion scores, scaled to 0-100. Changing a weight on `Rubric`
re-ranks every idea instantly.

## Folders

- `ideas/` — shortlisted business ideas with deeper analysis (the full backlog lives in the Sheet)
- `experiments/` — active experiments / MVPs being tested
- `research/` — market research, competitor analysis, pricing data

## Status

> 🔄 In progress — persona context being built
