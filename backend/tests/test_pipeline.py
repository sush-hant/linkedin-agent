import importlib.util
import tempfile
import unittest
from pathlib import Path

PYDANTIC_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if PYDANTIC_AVAILABLE:
    from app.orchestrator.pipeline import PipelineOrchestrator
    from app.shared.config import settings


@unittest.skipUnless(PYDANTIC_AVAILABLE, "pydantic is required for pipeline tests")
class PipelineTests(unittest.TestCase):
    def test_pipeline_runs_and_persists_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            settings.storage_root = tmp
            orchestrator = PipelineOrchestrator()
            result = orchestrator.run()

            self.assertEqual(result.status, "ok")
            self.assertGreater(result.raw_count, 0)
            self.assertGreater(result.trend_count, 0)

            expected_dirs = [
                Path(tmp) / "raw",
                Path(tmp) / "normalized",
                Path(tmp) / "trends",
                Path(tmp) / "drafts" / "posts",
                Path(tmp) / "drafts" / "images",
            ]
            for d in expected_dirs:
                self.assertTrue(d.exists())


if __name__ == "__main__":
    unittest.main()
