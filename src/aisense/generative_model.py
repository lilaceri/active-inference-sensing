"""The agent's generative model: what it *believes* about the world.

Array conventions (see AGENTS.md):

- ``A[m]`` has shape ``(num_obs[m], *num_states)`` and normalises over axis 0.
- ``B[f]`` has shape ``(num_states[f], num_states[f], num_actions)``, laid out as
  ``B[next, prev, action]``, and normalises over axis 0.
- ``C[m]`` has shape ``(num_obs[m],)`` and holds log-preferences in nats.
- ``D[f]`` has shape ``(num_states[f],)``.

The concrete factors, modalities and actions are specified in ``docs/model.md`` (AIS-020).
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class SensorSpec:
    """Specification of one sensor's noise and cost.

    Attributes
    ----------
    name : str
        One of ``constants.SENSORS``.
    accuracy_clear : float
        TODO(AIS-021): decide how to parameterise the confusion matrix
        (a single accuracy, a full matrix, per-class accuracies...).
    accuracy_fog : float
        As above, under fog.
    cost : float
        Cost of a query, in nats (enters through ``C``).
    """

    name: str
    accuracy_clear: float
    accuracy_fog: float
    cost: float


@dataclass(frozen=True)
class GenerativeModel:
    """Container for the A, B, C, D arrays and their labels.

    Attributes
    ----------
    A : list of ndarray
        One likelihood tensor per observation modality.
    B : list of ndarray
        One transition tensor per state factor.
    C : list of ndarray
        One log-preference vector per observation modality.
    D : list of ndarray
        One prior vector per state factor.
    action_labels : tuple of str
        Human-readable name of each action index.
    """

    A: list[FloatArray]
    B: list[FloatArray]
    C: list[FloatArray]
    D: list[FloatArray]
    action_labels: tuple[str, ...]

    def validate(self) -> None:
        """Check every shape and normalisation invariant.

        Raises
        ------
        ValueError
            On the first violated invariant, with a message naming the array and index.
        """
        raise NotImplementedError("AIS-023")


def default_sensor_specs() -> tuple[SensorSpec, ...]:
    """Return the camera, lidar and radar specs, built from ``constants``."""
    raise NotImplementedError("AIS-021")


def build_A(sensors: tuple[SensorSpec, ...]) -> list[FloatArray]:
    """Build the likelihood tensors ``p(o_m | s)`` for every modality.

    Returns
    -------
    list of ndarray
        Shapes as documented in ``docs/model.md``.
    """
    raise NotImplementedError("AIS-021")


def build_B() -> list[FloatArray]:
    """Build the transition tensors ``p(s_t+1 | s_t, u)`` for every factor."""
    raise NotImplementedError("AIS-022")


def build_C(sensors: tuple[SensorSpec, ...]) -> list[FloatArray]:
    """Build the log-preferences over outcomes, including sensor costs."""
    raise NotImplementedError("AIS-022")


def build_D() -> list[FloatArray]:
    """Build the prior over initial states for every factor."""
    raise NotImplementedError("AIS-022")


def build_model() -> GenerativeModel:
    """Assemble and validate the default generative model."""
    raise NotImplementedError("AIS-023")
