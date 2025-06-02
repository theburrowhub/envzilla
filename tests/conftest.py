"""Test configuration for envzilla."""

from pathlib import Path
import sys

# Ensure the ``src`` directory is importable during tests
ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(ROOT))

