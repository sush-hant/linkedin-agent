import importlib.util
import tempfile
import unittest
from datetime import datetime, timezone

FASTAPI_AVAILABLE = importlib.util.find_spec("fastapi") is not None
PYDANTIC_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if FASTAPI_AVAILABLE and PYDANTIC_AVAILABLE:
    from fastapi.testclient import TestClient

    from app.main import create_app
    from app.shared.config import settings


@unittest.skipUnless(FASTAPI_AVAILABLE and PYDANTIC_AVAILABLE, "fastapi+pydantic are required for api tests")
class ApiTests(unittest.TestCase):
    def test_endpoints_health_pipeline_review_feedback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            settings.storage_root = tmp
            app = create_app()
            client = TestClient(app)
            headers = {"x-api-key": settings.agent_api_key}

            health = client.get("/health")
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json()["status"], "ok")

            unauthorized = client.post("/pipeline/run")
            self.assertEqual(unauthorized.status_code, 401)

            run = client.post("/pipeline/run", headers=headers)
            self.assertEqual(run.status_code, 200)
            self.assertEqual(run.json()["status"], "ok")

            drafts = client.get("/review/drafts", headers=headers)
            self.assertEqual(drafts.status_code, 200)
            payload = drafts.json()
            self.assertGreater(len(payload), 0)

            images = client.get("/review/images", headers=headers)
            self.assertEqual(images.status_code, 200)
            self.assertGreater(len(images.json()), 0)

            draft_id = payload[0]["draft_id"]
            approve = client.post("/review/approve", json={"draft_id": draft_id}, headers=headers)
            self.assertEqual(approve.status_code, 200)
            published_id = approve.json()["published_id"]

            feedback = client.post(
                "/feedback/record", headers=headers,
                json={
                    "published_id": published_id,
                    "impressions": 100,
                    "comments": 4,
                    "reposts": 1,
                    "saves": 3,
                    "quality": "good",
                    "notes": "Strong engagement on practical tips",
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            self.assertEqual(feedback.status_code, 200)
            self.assertEqual(feedback.json()["status"], "ok")

            summary = client.get("/evaluation/summary", headers=headers)
            self.assertEqual(summary.status_code, 200)
            self.assertIn("avg_engagement_rate", summary.json())


if __name__ == "__main__":
    unittest.main()
