# HyperTPS Implementation Documentation Index

This directory consolidates all official architecture, product specifications, API schemas, and deployment plans for **HyperTPS**.

---

## 📋 Master Documentation Index

| Document | Category | Purpose | Key Specifications |
|---|---|---|---|
| [`PRD.md`](./PRD.md) | Product | Competition-Grade Product Requirements | JTBD, Personas, REQ-001 through REQ-006, 3,000+ TPS target |
| [`architecture.md`](./architecture.md) | Engineering | System & Wafer Architecture | CS-3 WSE-3 SRAM mapping, speculative decoding pipeline, ADRs |
| [`data-and-api-plan.md`](./data-and-api-plan.md) | Engineering | API Contract & Telemetry Schema | Cerebras `time_info` schema, request JSON, Candidacy payloads |
| [`execution-plan.md`](./execution-plan.md) | Engineering | 24-Hour Hackathon Build Plan | Hour-by-hour workstreams, code freeze, submission gates |
| [`threat-model.md`](./threat-model.md) | Security | STRIDE Threat Matrix & Trust Boundaries | Zero hardcoded keys, TLS 1.3, input sanitization, rate-limit defense |
| [`feasibility-assessment.md`](./feasibility-assessment.md) | Engineering | Technical Feasibility & Latency Budgets | Latency breakdown (sub-400ms end-to-end), API quota handling |
| [`user-flows.md`](./user-flows.md) | Product | Interaction Architecture & Sequence Flows | Bounty verification flow, OpenClaw developer flow, CLI flow |
| [`acceptance-criteria.md`](./acceptance-criteria.md) | Product | Given-When-Then Testable Matrix | AC-001 through AC-006 covering speed, accuracy, and parsing |
| [`final-red-team-review.md`](./final-red-team-review.md) | Adversarial | Red-Team Vulnerability Audit | Resolution of degenerate prompts, queue jitter, and social risks |
| [`demo-readiness.md`](./demo-readiness.md) | QA | Quality Assurance & Test Report | Unit test logs (7/7 passed), live vs dry-run contingency protocol |
| [`demo-script.md`](./demo-script.md) | Go-To-Market | Timed 2-Minute Demo Storyboard | Second-by-second video script, voiceover, on-screen callouts |
| [`pitch-deck-outline.md`](./pitch-deck-outline.md) | Go-To-Market | 10-Slide Competition Pitch Deck | High-contrast visual hooks, latency charts, competitive matrix |
| [`judge-qa.md`](./judge-qa.md) | Go-To-Market | Judge Q&A Defense Guide | Technical responses to speculative decoding & MoE questions |
| [`compliance-checklist.md`](./compliance-checklist.md) | Submission | Pre-Submission Rules Checklist | Rule verification, Org ID deadline, X/Reddit cutoffs |
| [`live-benchmark-results.md`](./live-benchmark-results.md) | Telemetry | Live Hardware Benchmark Ledger | Verified runs, Cerebras CS-3 transaction IDs, peak TPS records |
| [`executive-decision.md`](./executive-decision.md) | Executive | Executive Decision Memo | Summary of selected concept, competitive edge, and approval gate |

---

## 💻 CLI Integration

You can view or inspect these documents directly from the HyperTPS CLI:
```bash
# List all implementation documentation
python -m hypertps.cli --docs

# Inspect a specific document directly in terminal
python -m hypertps.cli --doc prd
python -m hypertps.cli --doc architecture
```
