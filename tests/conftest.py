import numpy as np
import pytest

SEED = 20261118


@pytest.fixture
def rng() -> np.random.Generator:
    """Seeded generator. Never use the global NumPy RNG in tests or src."""
    return np.random.default_rng(SEED)


# TODO(AIS-041): add a `tiny_model` fixture (e.g. 2 factors x 2 states, 1 modality)
# for oracle tests against brute-force Bayes.
