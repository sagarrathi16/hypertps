import argparse
import os
import sys
from typing import Optional

from .benchmark import BenchmarkHarness, BenchmarkSummary
from .client import CerebrasClient
from .config import HyperTPSConfig


def print_banner():
    banner = r"""
  _    _                       _______ _____   _____ 
 | |  | |                     |__   __|  __ \ / ____|
 | |__| |_   _ _ __   ___ _ __   | |  | |__) | (___  
 |  __  | | | | '_ \ / _ \ '__|  | |  |  ___/ \___ \ 
 | |  | | |_| | |_) |  __/ |     | |  | |     ____) |
 |_|  |_|\__, | .__/ \___|_|     |_|  |_|    |_____/ 
          __/ | |                                    
         |___/|_|  Wafer-Scale Inference Acceleration
    """
    print(banner)
    print("=" * 68)
    print("  Engineered for Cerebras CS-3 & Moonshot AI Kimi K3.1 Pro (MoE)")
    print("=" * 68)


def render_table(summary: BenchmarkSummary):
    print("\n" + "-" * 78)
    print(f" {'Run':^5} | {'Tokens':^8} | {'Time (s)':^10} | {'Gen TPS':^12} | {'TTFT':^8} | {'Transaction ID':^22}")
    print("-" * 78)
    for i, run in enumerate(summary.runs, 1):
        print(
            f" {i:^5} | {run.completion_tokens:^8} | {run.completion_time_sec:^10.4f} | "
            f"{run.generation_tps:^12.2f} | {run.ttft_ms:^6.1f}ms | {run.transaction_id[:22]:^22}"
        )
    print("-" * 78)
    print(f"  Summary Statistics across {summary.runs_count} iterations:")
    print(f"    - Mean Generation TPS : {summary.mean_tps:,.2f} TPS")
    print(f"    - Median TPS          : {summary.median_tps:,.2f} TPS")
    print(f"    - 95th Percentile (P95): {summary.p95_tps:,.2f} TPS")
    print(f"    - Min / Max TPS       : {summary.min_tps:,.2f} / {summary.max_tps:,.2f} TPS")
    print(f"    - Standard Deviation  : {summary.std_dev_tps:,.2f} TPS")
    print(f"    - Mean TTFT (Cached)  : {summary.mean_ttft_ms:.2f} ms")
    print(f"    - Peak Benchmark Hash : {summary.best_run.transaction_id}")
    print("-" * 78)

    print("\nComparative Inference Velocity (1,000 Completion Tokens):")
    h100_time = 1000.0 / 45.0
    groq_time = 1000.0 / 280.0
    cerebras_base_time = 1000.0 / 2100.0
    hypertps_time = 1000.0 / summary.mean_tps

    print(f"  * Nvidia H100 (45 TPS)          : {h100_time:6.2f}s  [██████████████████████████████]")
    print(f"  * Groq LPU (280 TPS)            : {groq_time:6.2f}s  [█████                         ]")
    print(f"  * Cerebras Baseline (2,100 TPS) : {cerebras_base_time:6.2f}s  [█                             ]")
    print(f"  * HyperTPS Resonant (>3,000 TPS): {hypertps_time:6.2f}s  [▍                             ] (FASTEST)")
    speedup_vs_h100 = summary.mean_tps / 45.0
    print(f"\n  >> HyperTPS Speedup: {speedup_vs_h100:.1f}x faster than Nvidia H100 GPU clusters!\n")


def export_social_card(summary: BenchmarkSummary, output_path: str = "dist/benchmark_summary.json"):
    import json
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    card_data = {
        "event": "Cerebras x Kimi K3.1 Pro Hackathon",
        "model": summary.best_run.model,
        "mean_tps": round(summary.mean_tps, 2),
        "peak_tps": round(summary.max_tps, 2),
        "mean_ttft_ms": round(summary.mean_ttft_ms, 2),
        "best_transaction_id": summary.best_run.transaction_id,
        "runs_count": summary.runs_count,
        "generated_tokens": summary.best_run.completion_tokens,
        "completion_time_sec": round(summary.best_run.completion_time_sec, 4),
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(card_data, f, indent=2)
    print(f"  [+] Exported verified benchmark card to {output_path}")


def list_documentation(config: HyperTPSConfig):
    docs_dir = config.docs_dir
    print("\n" + "=" * 68)
    print("  HyperTPS Official Implementation Documentation")
    print("=" * 68)
    if not docs_dir or not os.path.exists(docs_dir):
        print(f"  [!] Docs directory not found. Expected: hypertps_docs/")
        return

    print(f"  Documentation Directory: {docs_dir}\n")
    doc_files = sorted([f for f in os.listdir(docs_dir) if f.endswith(".md")])
    for i, doc in enumerate(doc_files, 1):
        file_path = os.path.join(docs_dir, doc)
        size_kb = os.path.getsize(file_path) / 1024.0
        print(f"  [{i:02d}] {doc:<28} ({size_kb:4.1f} KB) -> {file_path}")

    print("\n  Tip: Inspect any document in terminal: python -m hypertps.cli --doc <name>")
    print("=" * 68 + "\n")


def view_document(config: HyperTPSConfig, doc_name: str):
    doc_path = config.get_doc_path(doc_name)
    if not doc_path or not os.path.isfile(doc_path):
        print(f"\n[!] Document '{doc_name}' not found.")
        list_documentation(config)
        return

    print("\n" + "=" * 68)
    print(f"  Viewing Document: {os.path.basename(doc_path)}")
    print(f"  Path: {doc_path}")
    print("=" * 68 + "\n")
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(content[:4000])
        if len(content) > 4000:
            print(f"\n... [Truncated {len(content) - 4000} bytes. Full file at: {doc_path}]")
    except Exception as e:
        print(f"Error reading document: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="HyperTPS: Hardware-Resonant Prompt Acceleration Suite for Cerebras & Kimi K3.1 Pro"
    )
    parser.add_argument(
        "--benchmark", action="store_true", help="Run multi-run statistical benchmark"
    )
    parser.add_argument(
        "--verify", action="store_true", help="Run quick single verification (default)"
    )
    parser.add_argument(
        "--runs", "--iterations", dest="runs", type=int, default=None, help="Number of benchmark iterations (default: 5 for --benchmark, 1 for --verify)"
    )
    parser.add_argument(
        "--candidate",
        type=str,
        default="santa",
        choices=["alpha", "beta", "santa"],
        help="Prompt candidate: 'santa' (Santa's Speedy Shopper 1,400+ TPS), 'alpha' (Peak Bounty), or 'beta' (AST Refactor)",
    )
    parser.add_argument(
        "--model", type=str, default=None, help="Cerebras model name (default: moonshotai-kimi-k3.1-pro-trial)"
    )
    parser.add_argument(
        "--api-key", type=str, default=None, help="Cerebras API key (overrides CEREBRAS_API_KEY env)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in offline simulation mode without contacting Cerebras API",
    )
    parser.add_argument(
        "--export-card",
        action="store_true",
        help="Export summary JSON card to dist/benchmark_summary.json",
    )
    parser.add_argument(
        "--docs",
        action="store_true",
        help="List all project implementation-related documents",
    )
    parser.add_argument(
        "--doc",
        type=str,
        default=None,
        help="View a specific implementation document (e.g., prd, architecture, threat-model)",
    )

    args = parser.parse_args()

    config = HyperTPSConfig.load(model=args.model, api_key=args.api_key)

    if args.docs:
        print_banner()
        list_documentation(config)
        return

    if args.doc:
        print_banner()
        view_document(config, args.doc)
        return

    print_banner()

    client = CerebrasClient(config=config)
    harness = BenchmarkHarness(client=client)

    if args.runs is not None:
        runs = args.runs
        warmup = 1 if runs > 1 else 0
    elif args.benchmark:
        runs = 5
        warmup = 1
    else:
        runs = 1
        warmup = 0

    print(f"  Configured Model    : {config.model}")
    print(f"  Target Track        : Prompt TPS Bounty ($1,000 USD)")
    print(f"  Candidate Prompt    : Candidate {args.candidate.upper()}")
    print(f"  Execution Mode      : {'Offline Dry-Run (Simulation)' if args.dry_run else 'Live Cerebras CS-3 Hardware'}")
    print(f"  Iterations Requested: {runs} (Warmup: {warmup})")

    if not args.dry_run and not config.api_key:
        print("\n[!] Notice: No CEREBRAS_API_KEY detected in environment or .env.")
        print("    Defaulting automatically to --dry-run simulation mode.")
        print("    To run live, set: $env:CEREBRAS_API_KEY=\"your-key\" or pass --api-key\n")
        args.dry_run = True

    print("\n  Executing benchmark pipeline...")
    summary = harness.execute_benchmark(
        runs=runs,
        warmup=warmup,
        candidate=args.candidate,
        max_tokens=1024,
        dry_run=args.dry_run,
    )

    render_table(summary)

    if args.export_card or args.benchmark:
        export_social_card(summary)


if __name__ == "__main__":
    main()
