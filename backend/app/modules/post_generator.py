from dataclasses import dataclass
from hashlib import sha256

from app.ports.interfaces import LLMClientPort, PromptProviderPort
from app.shared.schemas import PostDraft, TrendCandidate


@dataclass
class PostGenerator:
    prompt_provider: PromptProviderPort
    llm_client: LLMClientPort | None = None

    def _fallback_content(self, trend: TrendCandidate, style: str) -> str:
        return (
            f"{trend.title}\n\n"
            f"Why this matters now: {trend.summary}\n\n"
            f"Style: {style}. What is your take?"
        )

    def _generate_content(self, trend: TrendCandidate, style: str) -> str:
        system_prompt = self.prompt_provider.get("linkedin_writer")
        user_prompt = (
            f"Create a {style} LinkedIn post using this trend.\\n"
            f"Title: {trend.title}\\n"
            f"Summary: {trend.summary}\\n"
            f"Citations: {', '.join(str(c) for c in trend.supporting_urls)}"
        )

        if not self.llm_client:
            return self._fallback_content(trend, style)

        try:
            return self.llm_client.generate_post(system_prompt, user_prompt)
        except Exception:
            return self._fallback_content(trend, style)

    def run(self, trends: list[TrendCandidate], max_topics: int = 3) -> list[PostDraft]:
        styles = ["educational", "contrarian", "tactical"]
        drafts: list[PostDraft] = []
        for trend in trends[:max_topics]:
            for style in styles:
                draft_id = sha256(f"{trend.topic_id}|{style}".encode()).hexdigest()[:12]
                drafts.append(
                    PostDraft(
                        draft_id=draft_id,
                        topic_id=trend.topic_id,
                        style=style,
                        content=self._generate_content(trend, style),
                        hashtags=["#AIAgents", "#GenerativeAI", "#AITrends", "#LinkedIn"],
                        citations=trend.supporting_urls,
                    )
                )
        return drafts
