# Acceptance Criteria & Verification Matrix: HyperTPS

**Event Slug:** `cerebras-kimi-hackathon`  
**Owner Agent:** product-prd-author  
**Audit Date:** 2026-11-20  
**Status:** Stage Gate D Approved  

---

## 1. Traceability & Acceptance Matrix

Every requirement from `PRD.md` is mapped to concrete, executable acceptance criteria using the Given-When-Then specification format:

---

### AC-001: Peak Generation TPS Verification (REQ-001)
- **Given:** A valid Cerebras Cloud API key with access to Moonshot AI `kimi-k3.1-pro`.
- **When:** The HyperTPS core bounty prompt is dispatched with parameters `temperature=0.0`, `max_tokens=1024`, `stream=False`.
- **Then:**
  1. The API response must return HTTP status 200.
  2. The response payload must contain `usage.completion_tokens >= 1000`.
  3. The calculated throughput $\frac{\text{usage.completion\_tokens}}{\text{time\_info.completion\_time}}$ must exceed **2,800 TPS** on mean, with peak iterations exceeding **3,000 TPS**.

---

### AC-002: Tamper-Proof Telemetry Parsing (REQ-002)
- **Given:** An incoming HTTP response from `https://api.cerebras.ai/v1/chat/completions`.
- **When:** The payload is processed by `HyperTPSMetricsParser`.
- **Then:**
  1. It extracts `time_info.queue_time`, `time_info.prompt_time`, `time_info.completion_time`, and `time_info.total_time`.
  2. It validates that $\text{prompt\_time} + \text{completion\_time} \le \text{total\_time}$.
  3. It prints the raw untouched Cerebras transaction ID (`id`) for third-party auditing.

---

### AC-003: 128-Token Cache Block Alignment (REQ-003)
- **Given:** A prompt payload with arbitrary system instructions.
- **When:** Processed through `CacheBlockAligner.align()`.
- **Then:**
  1. The total token count of the static prefix is exactly divisible by 128 ($N \pmod{128} == 0$).
  2. On repeat requests using the same prefix, the reported `time_info.prompt_time` drops to $< 20$ milliseconds.

---

### AC-004: OpenClaw Agent Middleware Transformation (REQ-004)
- **Given:** An OpenClaw agent instance configured with `@openclaw/hyper-tps`.
- **When:** The agent executes an automated codebase refactoring tool call.
- **Then:**
  1. The tool call payload is converted into a structured low-entropy template.
  2. The generation speed on Cerebras achieves at least a **$35\%$ speedup (TPS increase)** compared to the identical unoptimized prompt.
  3. The refactored code output passes AST syntax validation with zero syntax errors.

---

### AC-005: Multi-Run Statistical Reporting (REQ-005)
- **Given:** The CLI command `python -m hypertps.benchmark --runs 10`.
- **When:** The benchmark suite executes.
- **Then:**
  1. It executes 3 untimed warmup requests followed by 10 timed iterations.
  2. It outputs an ASCII table containing Run #, Completion Tokens, Completion Time, TPS, and Transaction ID.
  3. It computes and displays Mean, Median, Min, Max, and Standard Deviation.

---

### AC-006: Social Proof & Card Generation (REQ-006)
- **Given:** A completed benchmark run.
- **When:** The `--export-card` flag is supplied.
- **Then:**
  1. It generates a markdown summary table formatted for Reddit markdown.
  2. It generates a pre-formatted post copy for X containing `@cerebras`, `@openclaw`, and `@MoonshotAI`.
  3. It exports a high-contrast terminal screenshot / SVG representation.
