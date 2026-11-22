from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CerebrasTelemetry:
    """
    Authoritative microsecond performance telemetry extracted from Cerebras API.
    Calculates exact generation TPS strictly as completion_tokens / completion_time.
    """
    transaction_id: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    queue_time_sec: float
    prompt_time_sec: float
    completion_time_sec: float
    total_time_sec: float
    generation_tps: float
    prompt_tps: float
    cache_hit: bool
    raw_payload: Optional[Dict[str, Any]] = None

    @property
    def ttft_ms(self) -> float:
        """Time to First Token in milliseconds (prompt_time + queue_time)."""
        return (self.prompt_time_sec + self.queue_time_sec) * 1000.0


class TelemetryParser:
    """
    Parses and verifies Cerebras API response payloads for benchmark auditing.
    """

    @staticmethod
    def parse(response_json: Dict[str, Any]) -> CerebrasTelemetry:
        """
        Extracts telemetry from Cerebras API JSON response.
        Raises ValueError if required timing or token fields are missing or invalid.
        """
        if not isinstance(response_json, dict):
            raise ValueError("Invalid response payload: expected JSON object")

        tx_id = response_json.get("id", "unknown-transaction-id")
        model = response_json.get("model", "unknown-model")

        usage = response_json.get("usage", {})
        prompt_tokens = int(usage.get("prompt_tokens", 0))
        completion_tokens = int(usage.get("completion_tokens", 0))
        total_tokens = int(usage.get("total_tokens", prompt_tokens + completion_tokens))

        time_info = response_json.get("time_info")
        if not time_info or not isinstance(time_info, dict):
            raise ValueError(
                "Missing 'time_info' block in Cerebras response. "
                "Cerebras official timing telemetry is required to verify Prompt TPS."
            )

        queue_time = float(time_info.get("queue_time", 0.0))
        prompt_time = float(time_info.get("prompt_time", 0.0))
        completion_time = float(time_info.get("completion_time", 0.0))
        total_time = float(time_info.get("total_time", prompt_time + completion_time))

        if completion_time <= 0.0:
            raise ValueError(f"Invalid completion_time: {completion_time}s must be > 0")

        # Official Cerebras Generation TPS formula
        generation_tps = completion_tokens / completion_time

        prompt_tps = prompt_tokens / prompt_time if prompt_time > 0 else 0.0
        # Cache hit: prompt time below 20ms indicates ephemeral 128-token prefix cache hit
        cache_hit = prompt_time < 0.020

        return CerebrasTelemetry(
            transaction_id=tx_id,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            queue_time_sec=queue_time,
            prompt_time_sec=prompt_time,
            completion_time_sec=completion_time,
            total_time_sec=total_time,
            generation_tps=generation_tps,
            prompt_tps=prompt_tps,
            cache_hit=cache_hit,
            raw_payload=response_json,
        )
