import importlib.util
import tempfile
import unittest

FASTAPI_AVAILABLE = importlib.util.find_spec("fastapi") is not None

if FASTAPI_AVAILABLE:
    from fastapi.testclient import TestClient

    from app.main import create_app
    from app.shared.config import settings


@unittest.skipUnless(FASTAPI_AVAILABLE, "fastapi is required for api tests")
class ApiTests(unittest.TestCase):
    def test_health_and_pipeline_endpoints(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            settings.storage_root = tmp
            app = create_app()
            client = TestClient(app)

            health = client.get("/health")
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json()["status"], "ok")

            run = client.post("/pipeline/run")
            self.assertEqual(run.status_code, 200)
            self.assertEqual(run.json()["status"], "ok")


if __name__ == "__main__":
    unittest.main()
