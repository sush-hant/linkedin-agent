# Backend (Phase 1-3 baseline)

## Run API locally
```bash
cd backend
python run.py
```

## Available endpoints
- `GET /health`
- `GET /config`
- `POST /pipeline/run`

## Pipeline coverage
- Phase 1: app scaffold + contracts + prompt registry
- Phase 2: source fetching + normalization + ranking
- Phase 3: post draft generation + image draft generation

## Run tests
```bash
cd backend
python -m unittest discover -s tests -v
```

## Notes
- Prompt templates are file-based under `app/prompts/` and loaded by `FilePromptProvider`.
- Cron entrypoint is `scripts/run_pipeline.sh`.
