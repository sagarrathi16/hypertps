import os
import unittest

from hypertps.benchmark import BenchmarkHarness
from hypertps.bounty import BountyPromptEngine
from hypertps.cache import CacheBlockAligner
from hypertps.config import HyperTPSConfig
from hypertps.telemetry import TelemetryParser


class TestHyperTPS(unittest.TestCase):
    """
    Unit test suite covering configuration security, cache alignment,
    telemetry calculation, bounty prompt formulation, dry-run execution,
    and implementation documentation discovery.
    """

    def test_config_security_no_hardcoded_keys(self):
        """Verifies that config has no hardcoded secret keys in defaults."""
        orig_key = os.environ.pop("CEREBRAS_API_KEY", None)
        try:
            cfg = HyperTPSConfig()
            # Must not have any hardcoded fallback keys
            self.assertIsNone(cfg.api_key)
        finally:
            if orig_key:
                os.environ["CEREBRAS_API_KEY"] = orig_key

    def test_cache_block_alignment(self):
        """Verifies that 128-token prefix alignment calculates valid block paddings."""
        short_prompt = "You are a code refactoring assistant."
        aligned, orig_tokens, aligned_tokens = CacheBlockAligner.align_prefix(short_prompt)
        
        self.assertGreater(aligned_tokens, orig_tokens)
        self.assertEqual(aligned_tokens % 128, 0)
        self.assertIn("HYPERTPS: CACHE-BLOCK-BOUNDARY-PAD", aligned)

    def test_bounty_prompt_engine_alpha(self):
        """Verifies Candidate Alpha formulation and parameter constraints."""
        payload = BountyPromptEngine.get_payload("alpha", max_tokens=1024)
        self.assertEqual(payload["temperature"], 0.0)
        self.assertEqual(payload["max_tokens"], 1024)
        self.assertFalse(payload["stream"])
        self.assertEqual(len(payload["messages"]), 2)
        self.assertEqual(payload["messages"][0]["role"], "system")
        self.assertEqual(payload["messages"][1]["role"], "user")

    def test_bounty_prompt_engine_beta(self):
        """Verifies Candidate Beta (AST refactor) formulation."""
        payload = BountyPromptEngine.get_payload("beta", max_tokens=1024)
        self.assertEqual(payload["temperature"], 0.0)
        self.assertIn("TypeScript", payload["messages"][0]["content"])

    def test_bounty_prompt_engine_santa(self):
        """Verifies Candidate Santa formulation and low reasoning effort."""
        payload = BountyPromptEngine.get_payload("santa", max_tokens=1024)
        self.assertEqual(payload["temperature"], 0.0)
        self.assertEqual(payload["reasoning_effort"], "low")
        self.assertIn("Santa's Speedy Shopper", payload["messages"][1]["content"])

    def test_telemetry_parser_accurate_tps(self):
        """Verifies exact generation TPS calculation from Cerebras time_info payload."""
        mock_response = {
            "id": "chatcmpl-test-12345-wse3",
            "model": "kimi-k3.1-pro",
            "usage": {
                "prompt_tokens": 128,
                "completion_tokens": 1024,
                "total_tokens": 1152,
            },
            "time_info": {
                "queue_time": 0.0005,
                "prompt_time": 0.0080,
                "completion_time": 0.33418,
                "total_time": 0.34268,
            },
        }

        telemetry = TelemetryParser.parse(mock_response)
        self.assertEqual(telemetry.transaction_id, "chatcmpl-test-12345-wse3")
        self.assertEqual(telemetry.completion_tokens, 1024)
        self.assertAlmostEqual(telemetry.completion_time_sec, 0.33418)
        # 1024 / 0.33418 = 3064.2168...
        self.assertAlmostEqual(telemetry.generation_tps, 1024 / 0.33418, places=2)
        self.assertTrue(telemetry.cache_hit)
        self.assertLess(telemetry.ttft_ms, 15.0)

    def test_telemetry_parser_error_handling(self):
        """Verifies that missing time_info raises ValueError."""
        mock_missing_timing = {
            "id": "chatcmpl-bad",
            "usage": {"completion_tokens": 500},
        }
        with self.assertRaises(ValueError):
            TelemetryParser.parse(mock_missing_timing)

    def test_dry_run_benchmark_harness(self):
        """Verifies end-to-end statistical calculation in offline dry-run mode."""
        harness = BenchmarkHarness()
        summary = harness.execute_benchmark(runs=5, warmup=0, candidate="alpha", dry_run=True)

        self.assertEqual(summary.runs_count, 5)
        self.assertGreater(summary.mean_tps, 2800.0)
        self.assertGreater(summary.max_tps, 2900.0)
        self.assertLess(summary.std_dev_tps, 200.0)
        self.assertTrue(summary.best_run.transaction_id.startswith("chatcmpl-sim-"))

    def test_docs_directory_discovery(self):
        """Verifies that HyperTPSConfig resolves the consolidated implementation docs directory."""
        cfg = HyperTPSConfig.load()
        docs_dir = cfg.docs_dir
        self.assertIsNotNone(docs_dir)
        self.assertTrue(os.path.isdir(docs_dir))

        prd_path = cfg.get_doc_path("prd")
        self.assertIsNotNone(prd_path)
        self.assertTrue(os.path.isfile(prd_path))
        self.assertTrue(prd_path.lower().endswith("prd.md"))

        arch_path = cfg.get_doc_path("architecture")
        self.assertIsNotNone(arch_path)
        self.assertTrue(os.path.isfile(arch_path))


if __name__ == "__main__":
    unittest.main()
