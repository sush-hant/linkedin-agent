import json
from dataclasses import dataclass
from urllib import request

from app.ports.interfaces import LLMClientPort


@dataclass
class OpenAIClient(LLMClientPort):
    api_key: str
    model: str = "gpt-4o-mini"
    timeout_seconds: int = 30

    def generate_post(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.5,
        }
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
