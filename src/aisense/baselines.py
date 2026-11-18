"""Comparison agents sharing the ``reset()`` / ``act(observation, rng)`` interface."""

from collections.abc import Sequence

import numpy as np

from aisense.generative_model import GenerativeModel


class RandomSensorAgent:
    """Queries a random sensor until a fixed budget is spent, then declares its MAP class."""

    def __init__(self, model: GenerativeModel) -> None:
        self.model = model

    def reset(self) -> None:
        """Reset internal state."""
        raise NotImplementedError("AIS-060")

    def act(self, observation: Sequence[int], rng: np.random.Generator) -> int:
        """Return an action index."""
        raise NotImplementedError("AIS-060")


class FixedOrderAgent:
    """Queries sensors in a fixed order, then declares its MAP class."""

    def __init__(self, model: GenerativeModel) -> None:
        self.model = model

    def reset(self) -> None:
        """Reset internal state."""
        raise NotImplementedError("AIS-060")

    def act(self, observation: Sequence[int], rng: np.random.Generator) -> int:
        """Return an action index."""
        raise NotImplementedError("AIS-060")


class PragmaticOnlyAgent:
    """The active inference agent with the epistemic term removed from G (an ablation)."""

    def __init__(self, model: GenerativeModel, horizon: int, gamma: float) -> None:
        self.model = model
        self.horizon = horizon
        self.gamma = gamma

    def reset(self) -> None:
        """Reset beliefs to the prior."""
        raise NotImplementedError("AIS-060")

    def act(self, observation: Sequence[int], rng: np.random.Generator) -> int:
        """Return an action index."""
        raise NotImplementedError("AIS-060")
