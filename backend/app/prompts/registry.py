from pathlib import Path

from app.ports.interfaces import PromptProviderPort


class FilePromptProvider(PromptProviderPort):
    """Decoupled prompt loader: prompt text is kept in versioned files, not hardcoded."""

    def __init__(self, prompt_dir: Path) -> None:
        self.prompt_dir = prompt_dir

    def get(self, prompt_name: str) -> str:
        file_path = self.prompt_dir / f"{prompt_name}.md"
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_name}")
        return file_path.read_text(encoding="utf-8")
