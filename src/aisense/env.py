"""The generative process: the *true* world the agent interacts with.

``agent.py`` must never import from this module.
"""

from dataclasses import dataclass

import numpy as np

from aisense.generative_model import SensorSpec


@dataclass
class StepResult:
    """Outcome of one environment step.

    Attributes
    ----------
    observation : list of int
        One observation index per modality, in the model's index space.
    done : bool
        True after a ``declare_*`` action or ``MAX_STEPS``.
    correct : bool or None
        Whether the declaration was correct. None if nothing has been declared yet.
    """

    observation: list[int]
    done: bool
    correct: bool | None


class SensingEnv:
    """Hidden object + condition, observed through noisy sensors."""

    def __init__(self, sensors: tuple[SensorSpec, ...]) -> None:
        self.sensors = sensors

    def reset(self, rng: np.random.Generator) -> list[int]:
        """Sample the true object and condition, and return the initial observation."""
        raise NotImplementedError("AIS-030")

    def step(self, action: int) -> StepResult:
        """Apply an action and return the resulting observation."""
        raise NotImplementedError("AIS-030")
