"""
HyperTPS: Hardware-Resonant Prompt Acceleration Suite
Engineered for Cerebras Wafer-Scale Engine and Moonshot AI Kimi K3.1 Pro.
"""

__version__ = "0.1.0"
__all__ = [
    "HyperTPSConfig",
    "CerebrasClient",
    "CacheBlockAligner",
    "BountyPromptEngine",
    "TelemetryParser",
    "BenchmarkHarness",
]

from .config import HyperTPSConfig
from .client import CerebrasClient
from .cache import CacheBlockAligner
from .bounty import BountyPromptEngine
from .telemetry import TelemetryParser
from .benchmark import BenchmarkHarness
