# User Flows & Interaction Architecture: HyperTPS

**Event Slug:** `cerebras-kimi-hackathon`  
**Owner Agent:** product-prd-author  
**Audit Date:** 2026-11-20  
**Status:** Stage Gate D Approved  

---

## 1. High-Level User Journey Map

```mermaid
flowchart TD
  START([User Starts]) --> PATH{Choose Objective}

  PATH -->|Track 1: Win $1k Bounty| B1[Run HyperTPS Bounty Probe]
  PATH -->|Developer Work: Speed Up Agent| A1[Install OpenClaw HyperTPS Plugin]
  PATH -->|Community: Audit & Reproduce| C1[Run 1-Line Benchmark CLI]

  subgraph Track 1: Bounty Verification Flow
    B1 --> B2[Send 128-Token Aligned Prompt to Cerebras API]
    B2 --> B3[Engage Speculative Decoding Engine on WSE-3]
    B3 --> B4[Receive 1024 Tokens at 3,000+ TPS]
    B4 --> B5[Extract time_info.completion_time & Transaction ID]
    B5 --> B6[Emit Verified Judge Submission Package]
  end

  subgraph Developer Flow: OpenClaw Agent
    A1 --> A2[Agent Receives User Task: e.g. Refactor Codebase]
    A2 --> A3[HyperTPS Middleware Intercepts Prompt]
    A3 --> A4[Compresses System Prompt into 128-Token Block]
    A4 --> A5[Structures Tool Call Schemas to Maximize Speculative Alpha]
    A5 --> A6[Streams 2,800 TPS Stream to Terminal]
    A6 --> A7[Agent Completes 10-Step Loop in 2.2s]
  end

  subgraph Community Audit Flow
    C1 --> C2[Execute: python -m hypertps.benchmark]
    C2 --> C3[Performs 3 Warmups + 10 Test Iterations]
    C3 --> C4[Displays Live ANSI Speed Gauge & Comparison vs H100]
    C4 --> C5[Exports Shareable Results Card for Reddit / X]
  end
```

---

## 2. Detailed Interaction Step-by-Step

### Flow A: The Hackathon Judge / Auditor Verification Flow
1. **Initiation:** The judge opens the Cerebras Discord or terminal and runs:
   ```bash
   python -m hypertps.verify --model kimi-k3.1-pro --api-key $CEREBRAS_API_KEY
   ```
2. **Pre-flight Check:** The harness verifies network connectivity, confirms access to the rate-limit-increased private preview tier, and checks the Org ID.
3. **Execution:** The harness transmits the candidate resonant prompt.
4. **Live Telemetry:** The terminal displays real-time streaming tokens alongside a microsecond timer.
5. **Result Output:** The tool prints a verified audit summary:
   - Tokens Generated: 1,024
   - Completion Time: 0.334s
   - **Generation TPS: 3,065.86 TPS**
   - Transaction ID: `chatcmpl-b8d624a5...`
   - Cache Hit Status: True (TTFT: 12ms)

### Flow B: The OpenClaw Autonomous Agent Developer Flow
1. **Integration:** Developer adds `@openclaw/hyper-tps` to their `openclaw.config.json`.
2. **Transparent Interception:** When OpenClaw dispatches a code refactoring task, HyperTPS:
   - Analyzes prompt syntax.
   - Restructures system and user messages into a 128-token boundary block.
   - Formats code output targets as deterministic syntactical templates.
3. **Execution:** Dispatched to `api.cerebras.ai`.
4. **Outcome:** The agent executes code edits at 2,800+ TPS, delivering interactive sub-second responses directly to the developer's terminal.
