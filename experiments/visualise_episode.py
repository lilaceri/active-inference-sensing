"""Plot belief evolution and the EFE decomposition for one episode (AIS-071).

Usage:
    uv run python experiments/visualise_episode.py --seed 0 [--fog]
"""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--fog", action="store_true", help="force the hidden condition to fog")
    parser.add_argument("--out", type=Path, default=Path("results/episode.png"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise NotImplementedError(f"AIS-071 (args={args})")


if __name__ == "__main__":
    main()
