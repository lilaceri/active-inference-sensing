"""Benchmark the active inference agent against the baselines (AIS-070).

Usage:
    uv run python experiments/run_benchmark.py --episodes 1000 --seed 0
"""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, default=Path("results"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise NotImplementedError(f"AIS-070 (args={args})")


if __name__ == "__main__":
    main()
