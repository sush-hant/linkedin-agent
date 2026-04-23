# LinkedIn AI Trend Agent — Phase-wise, Decoupled Architecture Plan

## Implementation Status
- ✅ Phase 1 implemented: FastAPI scaffold, contracts, adapters, prompt registry.
- ✅ Phase 2 baseline implemented: static source fetcher, normalize/dedupe, trend ranking.
- ✅ Phase 3 baseline implemented: post draft generation + image draft generation via decoupled modules.
- ✅ Phase 4 backend baseline implemented: draft listing + approval APIs and published artifact storage.
- ✅ Phase 5 backend baseline implemented: feedback capture API + feedback service scoring hook.
- ✅ Next.js review UI baseline implemented: run pipeline, review/edit, approve, feedback submit.
- ✅ RSS source ingestion baseline implemented (with static source fallback).
- ✅ OpenAI-capable generation baseline implemented (with deterministic fallback when key is absent).
- ✅ Chroma adapter baseline implemented (persistent collection, upsert, query, deterministic embeddings).
- ✅ Retrieval-aware generation baseline implemented (related-topic context from vector search is injected into post generation).
- ✅ Retrieval signals are now used in ranking (novelty-aware scoring) and generation context.
- ✅ Multi-source momentum + retrieval-aware novelty ranking are implemented.
- ✅ Evaluation harness summary endpoint is implemented for KPI tracking.
- ✅ Production hardening (auth, retries, richer source coverage) is implemented.
- 🔜 Next step: CI/CD and deployment hardening (non-skipped test pipeline, secrets management, infra rollout).

---

## 1) Objective
Build an agent that continuously finds fresh AI/Agent trends and prepares:
- a high-quality LinkedIn post draft
- a matching image
- a review-ready package for manual publishing

Primary constraints:
- **Simple stack:** FastAPI + Next.js + cron
- **Local-first storage**
- **Decoupled modules** so components can be replaced independently

---

## 2) Final Stack (as requested)
- **Backend API:** FastAPI
- **Frontend:** Next.js
- **Scheduler:** cron
- **LLM + image generation:** OpenAI
- **Vector memory/search:** ChromaDB
- **Observability:** LangSmith
- **Storage:** local filesystem JSON/Markdown + local image folder

---

## 3) Decoupling Principles (Important)

To ensure future changes in one part do not break others:

1. **Contract-first module boundaries**
   - Every module communicates through typed DTOs (Pydantic schemas).
   - Avoid direct DB/file access across modules.

2. **Port/Adapter pattern**
   - Business logic depends on interfaces, not concrete providers.
   - Example: `LLMClient` interface with `OpenAIClient` implementation.

3. **Event-style handoff between stages**
   - Each stage writes output artifacts (`trend_candidates`, `post_drafts`, `image_drafts`).
   - Downstream stage consumes only prior artifact contract.

4. **Independent deploy/test paths**
   - Fetching, ranking, generation, and UI should each have isolated tests.

5. **No cross-module utility leakage**
   - Shared code only in explicit `shared/` package (schemas, constants, logging).

---

## 4) High-Level Architecture

```text
            +------------------+
cron -----> | Pipeline Trigger |
            +---------+--------+
                      |
                      v
            +-------------------+       +----------------+
            | Source Fetcher    | ----> | Raw Store      |
            +-------------------+       +----------------+
                      |
                      v
            +-------------------+       +----------------+
            | Normalize/Dedupe  | ----> | Normalized     |
            +-------------------+       | Store          |
                      |                 +----------------+
                      v
            +-------------------+       +----------------+
            | Trend Ranker      | ----> | Trend Store    |
            +-------------------+       +----------------+
                      |
                      v
            +-------------------+       +----------------+
            | Post Generator    | ----> | Draft Store    |
            | (OpenAI)          |       +----------------+
            +-------------------+
                      |
                      v
            +-------------------+       +----------------+
            | Image Generator   | ----> | Image Store    |
            | (OpenAI)          |       +----------------+
            +-------------------+
                      |
                      v
                 +---------+
                 | FastAPI |
                 +----+----+
                      |
                      v
                 +---------+
                 | Next.js |
                 +---------+
```

LangSmith tracing is attached at fetch, rank, post generation, and image generation steps.

---

## 5) Suggested Repository Structure

```text
/backend
  /app
    /api                 # FastAPI routes only
    /modules
      /fetcher
      /normalizer
      /ranker
      /post_generator
      /image_generator
      /publisher
    /ports               # interfaces (LLMClient, VectorStore, SourceClient)
    /adapters            # OpenAI, ChromaDB, file storage implementations
    /shared              # pydantic schemas, config, logger
    /orchestrator        # pipeline runner triggered by cron
/frontend                # Next.js app (review/edit/approve UI)
/data
  /raw
  /normalized
  /trends
  /drafts
  /images
  /metrics
/chroma                  # ChromaDB persistent directory
/scripts
  run_pipeline.sh        # called by cron
```

This structure keeps frontend, API layer, domain modules, and provider adapters clearly separated.

---

## 6) Core Contracts (Stable Interfaces)

### A) `TrendCandidate`
- `topic_id`
- `title`
- `summary`
- `supporting_urls[]`
- `trend_score`
- `generated_at`

### B) `PostDraft`
- `draft_id`
- `topic_id`
- `style` (educational/contrarian/tactical)
- `content`
- `hashtags[]`
- `citations[]`

### C) `ImageDraft`
- `image_id`
- `draft_id`
- `prompt`
- `file_path`
- `size`

If these contracts stay stable, implementations can change without ripple effects.

---

## 7) Phase-wise Plan

## Phase 1 — Foundation + Contracts (Week 1)
**Goal:** set decoupled skeleton and core data contracts.

Deliverables:
- FastAPI project setup with health/config endpoints.
- Next.js project setup with placeholder review page.
- Shared Pydantic schemas (`TrendCandidate`, `PostDraft`, `ImageDraft`).
- File-based storage adapter + ChromaDB adapter interfaces.
- `run_pipeline.sh` + cron schedule stub.

Success criteria:
- Backend and frontend run independently.
- Contracts validated end-to-end with mock data.

---

## Phase 2 — Ingestion + Ranking (Week 2)
**Goal:** produce reliable trend candidates.

Deliverables:
- Source fetcher module for initial 6 sources.
- Normalizer + deduper module.
- Trend ranker with simple scoring:
  - recency (40%)
  - momentum (35%)
  - audience fit (25%)
- Persist `TrendCandidate` artifacts to `/data/trends`.

Success criteria:
- Cron-triggered run produces top 3–5 trend candidates daily.
- Duplicate rate below agreed threshold.

---

## Phase 3 — Draft + Image Generation (Week 3)
**Goal:** generate complete post package.

Deliverables:
- OpenAI post generator (2–3 draft styles per trend).
- OpenAI image generator (1–2 images per selected draft).
- Citation-aware draft output.
- LangSmith tracing for generation flows.

Success criteria:
- At least one complete post+image package/day.
- Manual review time under ~20 minutes.

---

## Phase 4 — Review UX + Manual Publish (Week 4)
**Goal:** make operator workflow smooth.

Deliverables:
- Next.js review interface:
  - trend selection
  - draft comparison
  - image preview
  - approve/reject/edit
- FastAPI endpoints for listing/approving drafts.
- Manual publish checklist (copy text, upload image, post).

Success criteria:
- Single-page review flow for daily publishing.
- Approved drafts archived in `/data/published`.

---

## Phase 5 — Feedback Loop + Hardening (Week 5)
**Goal:** improve quality and make system maintainable.

Deliverables:
- Feedback capture (manual metrics + qualitative rating).
- Weight/prompt tuning hooks based on past outcomes.
- Module-level tests and API contract tests.
- Error handling + retry policy per module.

Success criteria:
- Observable improvement in draft relevance over 2 weeks.
- Any single module can be swapped with no change to others (validated by interface tests).

---

## 8) Cron and Runtime Plan

Example cron (every 6 hours):

```bash
0 */6 * * * /workspace/linkedin-agent/scripts/run_pipeline.sh
```

Execution rule:
- cron triggers orchestrator
- orchestrator calls modules in sequence
- each module writes versioned artifacts
- failures are isolated and logged; downstream does not run on invalid artifacts

---

## 9) Change Scenarios (Proof of Decoupling)

1. **Switch OpenAI to another model provider**
   - Replace `LLMClient` adapter only.
   - No changes to ranker, API, or UI.

2. **Move from local files to cloud DB/storage**
   - Replace storage adapter only.
   - No changes to business modules.

3. **Replace Next.js with another frontend**
   - Keep FastAPI contracts unchanged.
   - UI can be rebuilt independently.

4. **Change ranking logic**
   - Modify ranker module only as long as `TrendCandidate` contract is preserved.

---

## 10) MVP KPIs
- 1 publish-ready package/day.
- 2x faster workflow than manual process.
- Increasing comment quality and profile visits over 4 weeks.
- <5% pipeline failure rate over rolling 7 days.

This plan keeps the project practical now while remaining flexible for future upgrades.
