import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class HyperTPSConfig:
    """
    Configuration for HyperTPS inference client.
    Strictly follows zero-hardcoded-secret standards: reads API key dynamically
    from environment variable CEREBRAS_API_KEY or an uncommitted local .env file.
    """
    api_key: Optional[str] = None
    base_url: str = "https://api.cerebras.ai/v1"
    model: str = "moonshotai-kimi-k3.1-pro-trial"
    timeout_sec: float = 45.0
    max_retries: int = 6
    retry_delay_sec: float = 3.0

    @classmethod
    def load(cls, model: Optional[str] = None, api_key: Optional[str] = None) -> "HyperTPSConfig":
        """
        Loads configuration safely from environment or .env file.
        Explicitly passed parameters take precedence.
        """
        resolved_key = api_key or os.environ.get("CEREBRAS_API_KEY")

        if not resolved_key:
            # Check for local .env without requiring third-party dotenv library
            env_paths = [
                ".env",
                os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
                os.path.join(os.getcwd(), ".env"),
                os.path.join(os.getcwd(), "hypertps", ".env"),
                os.path.join(os.getcwd(), "hypertaps", ".env"),
                os.path.join(os.getcwd(), "workspace", "hackathons", "cerebras-kimi-hackathon", ".env"),
            ]
            env_model = None
            for env_path in env_paths:
                if os.path.exists(env_path):
                    try:
                        with open(env_path, "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.strip()
                                if line.startswith("CEREBRAS_API_KEY=") and not resolved_key:
                                    resolved_key = line.split("=", 1)[1].strip("'\" ")
                                elif line.startswith("CEREBRAS_MODEL=") and not env_model:
                                    env_model = line.split("=", 1)[1].strip("'\" ")
                    except Exception:
                        pass
                if resolved_key and env_model:
                    break

        resolved_model = (
            model
            or os.environ.get("CEREBRAS_MODEL")
            or env_model
            or "moonshotai-kimi-k3.1-pro-trial"
        )
        # Normalize shorthand alias to exact Cerebras Cloud endpoint model ID
        if resolved_model in ("kimi-k3.1-pro", "kimi-k3.1", "kimi"):
            resolved_model = "moonshotai-kimi-k3.1-pro-trial"
        resolved_base_url = (
            os.environ.get("CEREBRAS_BASE_URL")
            or "https://api.cerebras.ai/v1"
        )

        return cls(
            api_key=resolved_key,
            base_url=resolved_base_url,
            model=resolved_model,
        )

    @property
    def docs_dir(self) -> Optional[str]:
        """
        Locates the consolidated project implementation documentation directory.
        Checks for hypertps_docs and docs directories across package and repo roots.
        """
        candidates = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "hypertps_docs")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs")),
            os.path.abspath(os.path.join(os.getcwd(), "workspace", "hackathons", "cerebras-kimi-hackathon", "hypertps_docs")),
            os.path.abspath(os.path.join(os.getcwd(), "hypertps", "docs")),
            os.path.abspath(os.path.join(os.getcwd(), "hypertps_docs")),
            os.path.abspath(os.path.join(os.getcwd(), "docs")),
        ]
        for c in candidates:
            if os.path.isdir(c):
                return c
        return None

    def get_doc_path(self, doc_name: str) -> Optional[str]:
        """
        Resolves a specific documentation file by stem or filename within the docs folder.
        """
        base = self.docs_dir
        if not base:
            return None
        clean_name = doc_name.lower().strip()
        if not clean_name.endswith(".md"):
            clean_name += ".md"

        target = os.path.join(base, clean_name)
        if os.path.isfile(target):
            return target

        stem = doc_name.lower().replace(".md", "").strip()
        for fname in os.listdir(base):
            if (fname.lower().startswith(stem) or stem in fname.lower()) and fname.endswith(".md"):
                return os.path.join(base, fname)
        return None

    def validate_for_live(self) -> None:
        """
        Validates that an API key is present for live API operations.
        Raises ValueError with clear remediation instructions.
        """
        if not self.api_key or not self.api_key.strip():
            raise ValueError(
                "Missing Cerebras API Key!\n"
                "To execute live inference, set your API key:\n"
                "  PowerShell: $env:CEREBRAS_API_KEY = \"your-api-key\"\n"
                "  Bash:       export CEREBRAS_API_KEY=\"your-api-key\"\n"
                "Or test in offline simulation mode using: --dry-run"
            )
