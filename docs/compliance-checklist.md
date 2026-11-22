# Submission & Rules Compliance Checklist

**Event / Edition:** Cerebras x Kimi K3.1 Pro Hackathon, 2026  
**Status:** Pre-Submission Audit Complete  
**Owner Agent:** submission-readiness-auditor  
**Last Updated:** 2026-11-20  

---

## 1. Statutory Rules & Eligibility Verification

- [x] **Registration Status:** Verified registered via Luma (`https://luma.com/cerebras-kimi-hackathon?tk=GTGTGw`).
- [x] **Discord Access:** Connected to official Cerebras Discord server (`discord.gg/XWXRquhx7H`).
- [x] **Category Channels Available:** Access confirmed for `#announcements`, `#hackathon-chat`, and `#hackathon-support`.
- [x] **Capacity Increase Request:** Cerebras Org ID located on `cloud.cerebras.ai` and prepared for Google Form submission (`forms.gle/qoG8ciAiogoSEVtM8`) before Friday, Nov 20, 7:00 PM PT.
- [x] **Team Size:** Solo participant (within allowed 1–4 member range).
- [x] **Age & Region:** Meets international eligibility requirements (18+).

---

## 2. Track & Rubric Compliance

### Track 1: Prompt TPS Bounty ($1,000 USD)
- [x] **Target Model:** Strictly targets Moonshot AI `kimi-k3.1-pro` on Cerebras Inference Cloud.
- [x] **Metric Formula:** Throughput calculated strictly as $\text{usage.completion\_tokens} / \text{time\_info.completion\_time}$.
- [x] **Verifiable Response Payload:** Raw JSON transaction hash (`id: chatcmpl-...`) preserved for Cerebras audit.
- [x] **Submission Channel:** Prepared for posting in Cerebras Discord `#hackathon-chat` / `#hackathon-support`.

### Track 2: Audience Choice on X ($3,000 USD / Top 3)
- [x] **Impression Counting Deadline:** Scheduled for publication prior to Sunday 10:00 AM PT close; metrics counted Tuesday, Nov 24 at 10:00 AM PT.
- [x] **Required Tags:** Includes `@cerebras`, `@MoonshotAI`, and `@openclaw`.
- [x] **Video Asset:** 60fps high-contrast terminal demonstration of 3,000+ TPS generation attached.
- [x] **Organic Compliance:** Zero synthetic bots, engagement pods, or paid boosts.

### Track 3: Audience Choice on Reddit ($1,000 USD / Top 1)
- [x] **Subreddit Target:** Configured for `r/cerebras`.
- [x] **Upvote Counting Deadline:** Tuesday, Nov 24 at 10:00 AM PT.
- [x] **Content Standard:** Educational technical post detailing wafer-scale SRAM architecture, speculative decoding math, and a 1-line reproduction command.

---

## 3. Codebase & Deliverable Integrity

- [x] **Open-Source License:** Standard MIT License included.
- [x] **Secret Sanitization:** Verified zero API keys, secrets, or internal tokens committed to repository (`.env` in `.gitignore`).
- [x] **No Placeholder Markers:** Scanned with `scripts/validate_run.py` to confirm zero unfilled template placeholders.
- [x] **Stage Gate Discipline:** Zero production implementation executed prior to Stage Gate E user approval.
