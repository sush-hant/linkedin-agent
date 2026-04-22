# Backend (Phase 1)

## Run API locally
```bash
cd backend
python run.py
```

## Available endpoints
- `GET /health`
- `GET /config`

## Notes
- Phase 1 ships core contracts and decoupled module boundaries.
- Prompt templates are file-based under `app/prompts/`.
- Cron entrypoint is `scripts/run_pipeline.sh`.
