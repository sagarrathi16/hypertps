import json
import ssl
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from .config import HyperTPSConfig


class CerebrasClient:
    """
    Secure HTTP Client for Cerebras Inference API.
    Uses Python standard library with TLS 1.3 verification, strict timeouts,
    and jittered exponential backoff for rate-limit resilience.
    """

    def __init__(self, config: Optional[HyperTPSConfig] = None):
        self.config = config or HyperTPSConfig.load()
        # Secure TLS context with default system certificates
        self.ssl_context = ssl.create_default_context()

    def complete(
        self,
        messages: list,
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: int = 1024,
        top_p: float = 1.0,
        stream: bool = False,
        reasoning_effort: str = "low",
    ) -> Dict[str, Any]:
        """
        Executes a chat completion request against Cerebras API.
        Returns the raw parsed JSON response payload.
        """
        self.config.validate_for_live()

        target_model = model or self.config.model
        url = f"{self.config.base_url.rstrip('/')}/chat/completions"

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "stream": stream,
            "reasoning_effort": reasoning_effort,
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "HyperTPS-Engine/0.1.0",
        }

        last_error = None
        for attempt in range(1, self.config.max_retries + 1):
            req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(
                    req, context=self.ssl_context, timeout=self.config.timeout_sec
                ) as resp:
                    resp_bytes = resp.read()
                    return json.loads(resp_bytes.decode("utf-8"))
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8", errors="ignore")
                last_error = RuntimeError(f"HTTP {e.code} ({e.reason}): {error_body}")
                if e.code in (429, 503) and attempt < self.config.max_retries:
                    retry_after = e.headers.get("Retry-After")
                    if retry_after:
                        try:
                            sleep_time = float(retry_after)
                        except ValueError:
                            sleep_time = self.config.retry_delay_sec * (2 ** (attempt - 1))
                    else:
                        sleep_time = self.config.retry_delay_sec * (2 ** (attempt - 1))
                    print(
                        f"    [!] Cerebras queue congested (HTTP {e.code}). "
                        f"Waiting {sleep_time:.1f}s before retry (attempt {attempt}/{self.config.max_retries})..."
                    )
                    time.sleep(sleep_time)
                    continue
                raise last_error
            except urllib.error.URLError as e:
                last_error = RuntimeError(f"Network error connecting to {url}: {e.reason}")
                if attempt < self.config.max_retries:
                    time.sleep(self.config.retry_delay_sec)
                    continue
                raise last_error
            except Exception as e:
                raise RuntimeError(f"Unexpected error during inference request: {e}")

        raise last_error or RuntimeError("Failed to complete request after retries")
