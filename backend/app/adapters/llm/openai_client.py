import json
from dataclasses import dataclass
from time import sleep
from urllib import request

from app.ports.interfaces import LLMClientPort


@dataclass
class OpenAIClient(LLMClientPort):
    api_key: str
    model: str = "gpt-4o-mini"
    timeout_seconds: int = 30
    max_retries: int = 3

    def generate_post(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.5,
        }

        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                req = request.Request(
                    url="https://api.openai.com/v1/chat/completions",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    method="POST",
                )
                with request.urlopen(req, timeout=self.timeout_seconds) as resp:  # noqa: S310
                    body = json.loads(resp.read().decode("utf-8"))
                return body["choices"][0]["message"]["content"].strip()
            except Exception as exc:
                last_error = exc
                if attempt < self.max_retries - 1:
                    sleep(0.7 * (attempt + 1))

        if last_error:
            raise last_error
        raise RuntimeError("OpenAI generation failed")
