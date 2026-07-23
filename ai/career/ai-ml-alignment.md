# AI/ML Career Alignment — Daniel Bolivar

> Analysis date: 2026-07-23 · Based on current AI/ML labor-market data (mid-2026)
> Source profile: `ai/persona/profile.md`, `skills.md`, `hobbies.md`, `finances.md`

## TL;DR

You are **not** starting from scratch. A Senior BI & Data Engineer who is SQL-expert,
dbt/BigQuery-expert, Python-proficient, and *already* shipping with Claude Code, MCP,
the OpenAI API, prompt engineering, and BigQuery ML is sitting on the exact skill base
the 2026 AI market is short on. The market's #1 bottleneck isn't model research — it's
**people who can wire LLMs into real company data and ship them to production**. That is
data engineering with a new surface area.

Your five best-fit fields, ranked by transfer strength × market demand × lifestyle fit:

| Rank | Field | Transfer strength | Market demand | Why it fits *you* |
|------|-------|-------------------|---------------|-------------------|
| 1 | **AI / Applied AI Engineer** (RAG, agents) | High | Very high (#1 fastest-growing US role) | You already use OpenAI API, MCP, prompt eng, Python |
| 2 | **AI Data Engineer** (RAG data pipelines, vector/context infra) | Very high | High & rising | Direct extension of dbt/pipeline work |
| 3 | **LLMOps / MLOps Engineer** | High | High | Your production-pipeline & PR-review discipline maps 1:1 |
| 4 | **AI-Augmented / Conversational Analytics** (text-to-SQL, semantic layers) | Very high | Medium-high | Your LookML/semantic-layer + stakeholder-translation edge |
| 5 | **Forward-Deployed / AI Solutions Engineer** | Medium-high | High (strong LATAM-remote demand) | Build + client-facing; USD-remote-friendly |

The good news: paths 1–4 are **overlapping**, not divergent. The core skill set (RAG,
agents, evals, vector/context pipelines) is shared. You can learn once and position for
whichever role a given company happens to title.

---

## The market backdrop (why now)

A few numbers that frame every recommendation below:

- **AI Engineer was LinkedIn's #1 fastest-growing US job for 2026**, with postings up
  **143% year-over-year**; broader AI/ML postings surged ~163% YoY to 49,000+ open US
  roles.
- The hardest roles to fill are **generative-AI infrastructure, MLOps/LLMOps, and applied
  LLM engineering** — a blend of engineering + production-deployment skill, exactly the
  intersection you live in.
- **RAG is now a default enterprise architecture** — it appears in ~65% of applied-LLM job
  listings and went "from obscure to essential in ~18 months." Prompt-engineering demand
  rose ~136% in a single year.
- Compensation floor for AI/ML roles runs ~$25k above general software engineering; RAG
  engineers average ~$118k with seniors on shipped production systems at $195k–$290k base.
- **The shortage is on the "apply LLMs to *our* data and ship it" side**, not the "train
  foundation models" side. You do not need a PhD or PyTorch-from-scratch to enter — you
  need to prove you can build reliable retrieval + agent systems on real data.

Your personal advantages stack on top of this: you earn **USD, spend COP** (strong
purchasing power), you're already structured as an independent contractor for foreign
income, and you're **remote-native** — and LATAM-remote AI hiring (forward-deployed, AI
app engineers) is actively growing, paid in USD on US business hours.

---

## 1. AI / Applied AI Engineer  — *primary target*

### Why it's growing & relevant now
This is the broadest, hottest title in the market and the #1 fastest-growing US role two
years running. Every company that has data and a chatbot ambition needs someone to turn a
demo into a production system: RAG pipelines, agentic workflows, evals, guardrails, cost/
latency tuning. "Applied AI Engineer" (RAG + evals + agents) is described as *the* most
2026-specific role.

### Specific roles / titles
- AI Engineer / Applied AI Engineer
- GenAI Engineer / LLM Application Engineer
- Agent Developer / Agentic Systems Engineer
- AI Product Engineer

### What you already have that transfers
- **Python** (proficient) — the language of the entire LLM app stack.
- **OpenAI API + prompt engineering + Claude Code / MCP** — you're already *doing* the
  core work; most applicants are learning it from zero.
- **SQL-expert + data modeling** — retrieval quality is a data problem; you understand
  schema, joins, and what "clean, well-modeled context" means better than most app devs.
- **Stakeholder translation** — applied AI is fuzzy-problem → shipped-feature work; your
  exec-communication track record is a differentiator, not a soft extra.

### Gaps to fill
- **Orchestration frameworks**: LangChain / LangGraph, and an agent framework (CrewAI or
  the Agents SDK). You know MCP already — that's a real head start.
- **RAG mechanics**: chunking strategies, embeddings, vector search, re-ranking.
- **Evals**: how to measure LLM output quality systematically (this separates hobbyists
  from hireable engineers). Learn a framework like RAGAS / promptfoo / LangSmith.
- **App plumbing**: FastAPI (you have Flask — close), async, streaming responses,
  websockets.

### Realistic next steps
1. Build **one portfolio RAG app on data you already know** — e.g. a "chat with the dbt
   docs / warehouse metadata" assistant over BigQuery. It plays to your strengths and is
   instantly credible to data-heavy employers.
2. Add an **agentic layer** (a text-to-SQL agent that queries BigQuery and self-checks its
   output against your dbt semantic definitions).
3. Add **evals + a short write-up** of accuracy/latency/cost — this is the artifact that
   gets interviews.
4. Publish on GitHub (`danielb1215`) + a LinkedIn post. Ship in public.

---

## 2. AI Data Engineer  — *your strongest direct transfer*

### Why it's growing & relevant now
RAG and agents are only as good as the data behind them. A new specialization has emerged:
the engineer who builds **retrieval and context pipelines** — ingestion, chunking,
embedding, vector indexing, freshness/CDC for AI systems, and "context engineering." By
2026 building embedding/retrieval pipelines with vector search is standard practice, and
companies with proprietary data all need someone to make that data LLM-ready. This is
literally your job description with `EMBED()` added.

### Specific roles / titles
- AI Data Engineer / GenAI Data Engineer
- RAG / Retrieval Engineer
- Data Platform Engineer (AI)
- Context / Knowledge Engineer

### What you already have that transfers
- **dbt, ELT, CDC (Datastream), staging→marts modeling** — a RAG pipeline is an ELT
  pipeline whose "load" target is a vector index. Freshness, incrementality, and lineage
  are *your* domain.
- **BigQuery expert** — BigQuery now has native vector search + `ML.GENERATE_EMBEDDING`;
  you can build production RAG **without leaving the warehouse you already master**.
- **Cost optimization** (the 67.5% migration win) — embedding/inference cost control is a
  top enterprise pain; you have a headline achievement in exactly this muscle.
- **Cloud Run, Jenkins, Git** — deployment & orchestration already in hand.

### Gaps to fill
- **Vector databases**: pgvector, Pinecone, Weaviate, or Qdrant (plus BigQuery/Snowflake
  native vector search, which you can start with today).
- **Embedding models**: how to choose/evaluate them; chunking & retrieval-quality tuning.
- **Unstructured data**: PDFs, docs, transcripts — parsing and normalizing non-tabular
  sources into retrievable chunks.

### Realistic next steps
1. Do a **BigQuery-native RAG proof** using `ML.GENERATE_EMBEDDING` + `VECTOR_SEARCH` — no
   new platform required, immediate credibility on your résumé.
2. Then rebuild the same pipeline once on **pgvector or Qdrant** to show portability.
3. Reframe your résumé bullets: "20+ dbt pipelines" → also "designed retrieval/embedding
   pipelines feeding LLM applications." Same work, current vocabulary.

> This is the lowest-friction, highest-certainty path: it's an *extension* of your current
> title, not a career change. If you want the safest transition, start here.

---

## 3. LLMOps / MLOps Engineer

### Why it's growing & relevant now
As companies move models from demo to production, demand for the "plumbing of AI" has
skyrocketed: managing compute/latency/cost, deploying models, monitoring drift, running
CI/CD for prompts and pipelines, and building eval harnesses. These roles are among the
*hardest to fill* precisely because they need production-engineering discipline that most
ML researchers lack — and that you already have.

### Specific roles / titles
- LLMOps Engineer / MLOps Engineer
- ML Platform Engineer
- AI Infrastructure Engineer

### What you already have that transfers
- **Production ownership**: 100% on-time delivery of business-critical pipelines, 20+
  production dbt models, data-warehouse standards, **PR review across the team** — this is
  the operational maturity LLMOps is starving for.
- **CI/CD (Jenkins), Git, Cloud Run** — the deployment backbone.
- **Cost/perf optimization** — the core LLMOps value proposition.

### Gaps to fill
- **Model-serving & monitoring stack**: containerization depth (Docker/K8s basics),
  model/prompt versioning, observability (LangSmith / Langfuse / Arize / Weights & Biases).
- **Eval & guardrail pipelines** as first-class CI steps.
- Some **classic MLOps** exposure (feature stores, model registries) if you lean ML vs LLM.

### Realistic next steps
1. Add **monitoring + versioning + a CI eval gate** to the RAG app from Path 1 — that
   single project doubles as an LLMOps portfolio piece.
2. Learn one observability tool end-to-end (Langfuse is open-source and quick to stand up).
3. Target job descriptions that say "MLOps/LLMOps + strong data engineering background" —
   you match the *rare* half of that requirement already.

---

## 4. AI-Augmented / Conversational Analytics  — *your unfair advantage*

### Why it's growing & relevant now
"Talk to your data" (text-to-SQL, natural-language BI, AI analysts) is one of the most
funded enterprise AI use cases. The hard part isn't the LLM — it's a **trustworthy
semantic layer** so the model answers correctly. Very few people combine deep LookML/dbt
semantic modeling *and* LLM skills. You are one of them.

### Specific roles / titles
- AI Analytics Engineer
- Conversational / NL-BI Engineer
- Semantic Layer / Metrics Engineer for AI
- AI Solutions Engineer at a BI/data-tooling company (dbt Labs, Looker/Google, Cube,
  Omni, ThoughtSpot, etc.)

### What you already have that transfers
- **LookML + dbt semantic/business-vault modeling** — the exact substrate text-to-SQL
  needs to be reliable. This is genuinely scarce.
- **Self-serve dashboards + exec storytelling** — you understand what a *correct, useful*
  answer looks like for a business user.
- **Attribution/CAC/RFM modeling** — domain analytics depth that makes you credible to
  buyers, not just builders.

### Gaps to fill
- **Text-to-SQL patterns**: schema-linking, grounding on a semantic layer, self-correction
  loops, and evaluating answer correctness.
- LLM app basics (shared with Path 1 — you only learn them once).

### Realistic next steps
1. Build a **text-to-SQL-over-your-dbt-semantic-layer** demo (this is the flagship project
   that unifies Paths 1, 2, and 4).
2. Watch **dbt Labs, Looker/Google, Cube, Omni, ThoughtSpot** careers pages — AI Solutions/
   Applied AI roles there value your exact profile and are remote-friendly.

---

## 5. Forward-Deployed / AI Solutions Engineer  — *fast USD-remote on-ramp*

### Why it's growing & relevant now
Forward-Deployed Engineer postings grew **800%+ in 2025**. AI startups need engineers who
embed with customers, own outcomes from fuzzy problem → shipped agent, and split time
between calls with operators and building/integrating/debugging. **This role is actively
hiring remote across Latin America, paid in USD on US business hours** — a direct fit for
your setup.

### Specific roles / titles
- Forward-Deployed AI Engineer
- AI Solutions Engineer / Applied AI Consultant
- Sales/Solutions Engineer at an AI startup

### What you already have that transfers
- **Translating complex data for technical *and* executive stakeholders** — this is the
  headline requirement of the role, and it's already on your résumé.
- **Python + LLM app skills** (shared with Path 1).
- **End-to-end ownership + "make it work in prod" instinct.**
- **C1 English + native Spanish** — LATAM-remote roles serving US clients value both.

### Gaps to fill
- Same LLM/RAG/agent stack as Path 1.
- Comfort with **customer-facing ambiguity** and rapid iteration (lighter on deep infra).

### Realistic next steps
1. Once the Path 1 portfolio app exists, apply directly — LATAM-remote FDE roles (e.g. via
   Puente Talent Partners, Truelogic, and startup job boards) list this profile.
2. This is also the **best bridge to your side-business mission** (`CLAUDE.md`): FDE/solutions
   consulting is how you'd validate a productized-AI-for-data-teams offer with real clients
   before building it.

---

## What to learn — consolidated gap list

You'll notice the same ~6 skills unlock Paths 1–5. Learn these once:

1. **RAG mechanics** — chunking, embeddings, vector search, re-ranking, evaluation.
2. **An orchestration framework** — LangChain/LangGraph (you already know MCP — leverage it).
3. **An agent pattern** — tool-calling agents, self-correction loops.
4. **Evals** — RAGAS / promptfoo / LangSmith; measuring correctness, not vibes.
5. **Vector storage** — start with BigQuery-native `VECTOR_SEARCH`, then pgvector/Qdrant.
6. **App/serving basics** — FastAPI (≈ your Flask), plus observability (Langfuse/LangSmith).

What you can **de-prioritize**: training foundation models, deep PyTorch/CUDA, distributed
GPU training. That's the research/infra-at-scale lane — high barrier, not where the volume
of hiring or your leverage is.

---

## Suggested 90-day plan (10–15 h/week, fits your schedule)

Your realistic budget is ~10–15 h/week (evenings, minus Tue/Thu rides; partial weekends).

**Weeks 1–3 — Foundations & first RAG**
- Ship a BigQuery-native RAG app over data you know (dbt docs / warehouse metadata).
- Learn embeddings + `VECTOR_SEARCH`; write down accuracy/cost observations.

**Weeks 4–6 — Agents + evals**
- Add a text-to-SQL agent grounded on your dbt semantic layer, with a self-check loop.
- Add an eval harness (RAGAS/promptfoo). This is the credibility multiplier.

**Weeks 7–9 — Productionize (LLMOps layer)**
- Add versioning, monitoring (Langfuse), and a CI eval gate. Deploy on Cloud Run.
- Rebuild the retrieval layer once on pgvector/Qdrant to prove portability.

**Weeks 10–12 — Package & go to market**
- Write it up (blog + LinkedIn), push to GitHub, refresh résumé with AI-era vocabulary.
- Start applying: AI Data Engineer / Applied AI Engineer roles + LATAM-remote FDE roles;
  watch dbt Labs / Cube / Omni / ThoughtSpot careers pages.

One portfolio project — **RAG + text-to-SQL agent + evals + monitoring on BigQuery** —
credibly positions you for **all five** paths simultaneously. Build once, aim broadly.

---

## How this ties to your bigger goal

Your stated "why" is financial freedom to travel and explore nature — via a $2–3k/month
parallel income (`finances.md`). These career paths serve that in two ways:

1. **Higher-leverage day job**: moving from BI/Data Engineer to AI Data/Applied AI Engineer
   raises your USD ceiling meaningfully while keeping you remote — more surplus to invest,
   and the exact skills a productized side business would sell.
2. **A validated side-business wedge**: Path 5 (solutions/FDE consulting) is the lowest-risk
   way to test demand for "AI/RAG for data teams" with paying clients before building a
   product — directly feeding `ai/entrepreneurship/`. Consider a `/speckit-specify` on a
   "RAG/AI enablement for small data teams" consulting offer as the next step.

---

## Recommendation

Lead with **Path 2 (AI Data Engineer)** as the safe, near-certain extension of your current
role, while building the **Path 1 portfolio project** that also unlocks Paths 3–5. Keep
**Path 5 (FDE/solutions)** in view as both a fast USD-remote on-ramp and a bridge to the
side-business mission. You are closer to this market than you probably think — the main gap
is *packaging and proof*, not fundamentals.

---

## Sources

- [Machine Learning Engineer Job Outlook 2026 — 365 Data Science](https://365datascience.com/career-advice/machine-learning-engineer-job-outlook/)
- [AI Engineer Job Outlook 2026 — 365 Data Science](https://365datascience.com/career-advice/career-guides/ai-engineer-job-outlook-2025/)
- [AI Engineer Demand 2026: 143% YoY, 3.2:1 Gap — futureproofing.dev](https://www.futureproofing.dev/resources/ai-talent-gap/ai-engineer-demand-2026)
- [AI Engineer vs ML Engineer: Demand, Salaries, and Career Growth — Vettio](https://vettio.com/blog/ai-engineer-vs-ml-engineer/)
- [AI/ML Engineering Jobs in 2026: Analyzing 10,000+ Posts — Axial Search](https://axialsearch.com/insights/ai-ml-engineering-jobs/)
- [The Most In-Demand Machine Learning Roles in 2026 — Acceler8 Talent](https://www.acceler8talent.com/resources/blog/the-most-in-demand-machine-learning-roles-in-2026--managing-the-ai-talent-frontier/)
- [Fastest Growing AI Roles in 2026 — HeroHunt.ai](https://www.herohunt.ai/blog/fastest-growing-ai-roles-in-2026-data-and-rankings/)
- [Top 8 High-Demand AI Roles in 2026 — AI Staffing Ninja](https://www.aistaffingninja.com/blog/high-demand-ai-roles/)
- [How to Hire RAG Engineers in 2026: Salary, Skills & Interview Guide — KORE1](https://www.kore1.com/hire-rag-engineers-2026/)
- [AI Engineer Salary 2026: $145K–$310K — KORE1](https://www.kore1.com/ai-engineer-salary-guide/)
- [RAG Engineer Jobs 2026 — PropelGrad](https://propelgrad.com/ai-jobs/rag-engineer)
- [Forward Deployed AI Engineer (Remote LATAM) — Puente Talent Partners via Get on Board](https://www.getonbrd.com/jobs/machine-learning-ai/forward-deployed-ai-engineer-puente-talent-partners-remote)
- [Forward Deployed Engineer — Truelogic (Latin America Remote)](https://www.remoterocketship.com/company/truelogic-software/jobs/forward-deployed-engineer-technology-latin-america-remote/)
- [Top LATAM Countries to Hire AI Talent in 2026 — Hireslink](https://www.hireslink.com/blog/top-latam-countries-to-hire-ai-talent-in-2026)
