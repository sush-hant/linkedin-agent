# Backend (Phase 1-5 baseline)

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

## Run tests
```bash
cd backend
python -m unittest discover -s tests -v
```

## Notes
- Prompt templates are file-based under `app/prompts/` and loaded by `FilePromptProvider`.
- Cron entrypoint is `scripts/run_pipeline.sh`.
