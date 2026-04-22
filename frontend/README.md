# Frontend (Next.js)

This is the Phase 4/5 review UI implementation.

## Features
- Run backend pipeline (`POST /pipeline/run`)
- Load latest drafts (`GET /review/drafts`)
- Load latest image draft metadata (`GET /review/images`)
- Edit and approve a draft (`POST /review/approve`)
- Submit post feedback (`POST /feedback/record`)

## Run locally
```bash
cd frontend
npm install
NEXT_PUBLIC_API_BASE=http://localhost:8000 npm run dev
```

Ensure FastAPI backend is running at the same API base URL.
