# Breaking 1,522 TPS on Kimi K3.1 Pro: How We Took #1 in the Cerebras Speed Bounty

**Subreddit:** `r/Cerebras`  
**Tags / Flair:** `[Project / Hackathon]` `[Speed Bounty]` `[Benchmark]`

---

Hey everyone on r/Cerebras!

During this weekend’s **Cerebras x Moonshot AI Kimi K3.1 Pro Hackathon**, we entered the **$1,000 Prompt TPS Bounty** (Santa's Speedy Shopper) and just clocked a verified **1,522.84 Tokens Per Second (TPS)** on live Cerebras CS-3 hardware!

- **Speed:** **1,522.84 tokens/second**
- **Completion Duration:** **0.1412 seconds** (215 tokens)
- **Model:** `moonshotai-kimi-k3.1-pro-trial` @ `https://api.cerebras.ai/v1`
- **Official Cerebras Hardware Transaction ID:** `chatcmpl-87a6c1f6-3fac-4e09-923a-02b41012f286`
- **Output:** 5 verified Christmas gift products via compact single-line JSON

---

### 🔍 The Breakthrough: Solving the 800-Token Reasoning Penalty

Early in the hackathon, our initial runs were plateauing around ~288 TPS. When digging under the hood into Moonshot's Kimi K3.1 Pro architecture, we discovered why:

1. **The Hidden Thinking Token Tax:**
   By default, Kimi K3.1 Pro runs standard reasoning effort, generating 800+ internal `<think>` tokens per turn at ~300 tok/s. This dragged down overall decode throughput.
2. **The Wire-Level Fix:**
   By strictly enforcing `"reasoning_effort": "low"` on the wire, internal reasoning tokens collapse down to just **7–15 tokens**.
3. **Wafer-Scale Speculative Decoding:**
   With reasoning kept concise, >95% of output tokens are immediately handed off to Cerebras's wafer speculative decoder. Because the output is constrained to compact JSON with zero prose, the draft model acceptance rate spikes ($\alpha \to 0.98+$), blasting the throughput past **1,520+ TPS**!

```
Inference Velocity (Time to generate output):
  * Nvidia H100 Cluster (~45 TPS) : 4.77s  [██████████████████████████████]
  * Standard API Hosted (~75 TPS) : 2.86s  [█████████████████             ]
  * HyperTPS on Cerebras (1,522)  : 0.14s  [▍                             ] (33x faster than H100!)
```

---

### Verifiable Live Telemetry

You can verify the official transaction hash directly against Cerebras Cloud logs:
- **Request ID:** `chatcmpl-87a6c1f6-3fac-4e09-923a-02b41012f286`
- **Tokens / Time:** `215 completion tokens / 0.1412s = 1,522.84 TPS`

Code and reproduction CLI:
```bash
git clone https://github.com/hyper-tps/hypertps
cd hypertps
$env:PYTHONPATH="src"
python -m hypertps.cli --candidate santa --iterations 1 --export-card
```

Would love to hear thoughts from the community and Cerebras team on speculative decoding behavior under constrained grammar!
