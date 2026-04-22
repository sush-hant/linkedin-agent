from dataclasses import dataclass
from hashlib import sha256

from app.ports.interfaces import PromptProviderPort
from app.shared.schemas import PostDraft, TrendCandidate


@dataclass
class PostGenerator:
    prompt_provider: PromptProviderPort

    def run(self, trends: list[TrendCandidate], max_topics: int = 3) -> list[PostDraft]:
        _ = self.prompt_provider.get("linkedin_writer")
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
                        content=(
                            f"{trend.title}\n\n"
                            f"Why this matters now: {trend.summary}\n\n"
                            f"Style: {style}. What is your take?"
                        ),
                        hashtags=["#AIAgents", "#GenerativeAI", "#AITrends", "#LinkedIn"],
                        citations=trend.supporting_urls,
                    )
                )
        return drafts
