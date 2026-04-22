# Backend (Phase 1-9 baseline)

## Run API locally
```bash
cd backend
python run.py
```

## Available endpoints
- `GET /health`
- `GET /config`
- `POST /pipeline/run`
- `GET /review/drafts`
- `GET /review/images`
- `POST /review/approve`
- `POST /feedback/record`

## Pipeline coverage
- Phase 1: app scaffold + contracts + prompt registry
- Phase 2: source fetching + normalization + ranking
- Phase 3: post draft generation + image draft generation
- Phase 4: review/approval endpoints and published artifact storage
- Phase 5: feedback capture endpoint + scoring hook service
- Phase 6: RSS-based source ingestion (with static fallback for resilience)
- Phase 7: OpenAI-backed post generation adapter (with graceful fallback)
- Phase 8: Chroma adapter with deterministic embedding + query support
- Phase 9: Retrieval-aware generation using vector related-topic context

## Run tests
```bash
cd backend
python -m unittest discover -s tests -v
```

## Notes
- Prompt templates are file-based under `app/prompts/` and loaded by `FilePromptProvider`.
- Cron entrypoint is `scripts/run_pipeline.sh`.


## Source configuration
- RSS feed URLs are configured in `app/shared/config.py` via `settings.rss_feeds`.

## LLM configuration
- Set `OPENAI_API_KEY` (and optional `OPENAI_MODEL`) to enable real post generation.
- Without API key, pipeline uses deterministic fallback post drafting.

- Optional `OPENAI_EMBEDDING_MODEL` controls Chroma embedding calls when API key is available.
