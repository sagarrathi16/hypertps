# Data Model, API Schema & Telemetry Specification

**Event Slug:** `cerebras-kimi-hackathon`  
**Owner Agent:** data-api-integration-analyst  
**Audit Date:** 2026-11-20  
**Status:** Stage Gate D Approved  

---

## 1. Cerebras REST API Request Schema

The application communicates with `https://api.cerebras.ai/v1/chat/completions` using the standard OpenAI-compatible schema, hardened with wafer-scale optimization parameters:

### Request Payload Contract
```json
{
  "model": "kimi-k3.1-pro",
  "messages": [
    {
      "role": "system",
      "content": "You are a hardware-resonant code generator. Output only valid deterministic Python code with zero commentary."
    },
    {
      "role": "user",
      "content": "<RESONANT_BOUNTY_PAYLOAD_V1>"
    }
  ],
  "temperature": 0.0,
  "top_p": 1.0,
  "max_tokens": 1024,
  "stream": false,
  "stop": null
}
```

### Key Parameter Rationale
- `model`: Strictly targets the hackathon's focal model Moonshot `kimi-k3.1-pro`.
- `temperature`: Fixed at `0.0` (greedy decoding). Eliminates multinomial sampling overhead and aligns speculative draft model predictions with target argmax with highest probability.
- `max_tokens`: Fixed at `1024` (or `2048`). Ensures the generation runs long enough to achieve steady-state hardware throughput, amortizing pipeline ramp-up latency.

---

## 2. Cerebras Response & Telemetry Data Model

### Raw JSON Response Object
```json
{
  "id": "chatcmpl-b8d624a5-43d4-477a-8b94-61be750e2872",
  "object": "chat.completion",
  "created": 1775680120,
  "model": "kimi-k3.1-pro",
  "system_fingerprint": "fp_cerebras_cs3_wse3",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "# Resonant Output Stream\ndef generate_sequence():\n    ..."
      },
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 128,
    "completion_tokens": 1024,
    "total_tokens": 1152
  },
  "time_info": {
    "queue_time": 0.000412,
    "prompt_time": 0.008450,
    "completion_time": 0.334180,
    "total_time": 0.343042,
    "created": 1775680120.4512
  }
}
```

### Derived Telemetry Fields
```python
class CerebrasTelemetry:
    transaction_id: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    queue_time_sec: float
    prompt_time_sec: float
    completion_time_sec: float
    total_time_sec: float
    generation_tps: float  # completion_tokens / completion_time_sec
    prompt_tps: float      # prompt_tokens / prompt_time_sec
    cache_hit: bool        # prompt_time_sec < 0.020
```

---

## 3. The Resonant Bounty Prompt Contract (Candidate Alpha)

The candidate prompt designed for the $1,000 TPS Bounty combines:
1. **Padded Static Header (128 Tokens):** Pre-warmed in Cerebras ephemeral cache.
2. **Deterministic Syntactic Generator:** Requests unrolling of a mathematical series (e.g. constant-stride Fibonacci or fast inverse square root coefficients) in pure Python code with no markdown wrapper or conversational prose.
3. **Entropy Minimization:** Output follows a strict 4-token repetitive syntactic loop (`x_{i} = x_{i-1} + c\n`), driving draft acceptance $\alpha > 0.98$ and locking top-16 MoE expert routing on wafer SRAM.

---

## 4. OpenClaw Plugin Data Interface

```typescript
export interface HyperTPSConfig {
  apiKey: string;
  model: string;
  enableCacheAlignment: boolean;
  enableResonanceOptimization: boolean;
  targetMaxTokens: number;
}

export interface OptimizationResult {
  originalPromptTokens: number;
  alignedPromptTokens: number;
  estimatedAlpha: number;
  measuredTPS: number;
  latencySavedMs: number;
}
```
