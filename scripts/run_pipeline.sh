#!/usr/bin/env bash
set -euo pipefail

cd /workspace/linkedin-agent/backend
python -c 'from app.orchestrator.pipeline import PipelineOrchestrator; print(PipelineOrchestrator().run())'
