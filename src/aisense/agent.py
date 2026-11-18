"""Active inference: state inference, expected free energy and policy selection.

Notation follows ``docs/model.md``:

- ``qs``: posterior over states, as a list of per-factor vectors
- ``G``: expected free energy per policy
- ``gamma``: policy precision
- ``E``: habit prior over policies
"""

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from aisense.generative_model import GenerativeModel

FloatArray = NDArray[np.float64]
Policy = tuple[int, ...]


@dataclass(frozen=True)
class EFEResult:
    """Expected free energy and its decomposition for one policy.

    Attributes
    ----------
    G : float
        Total expected free energy (lower is better).
    pragmatic : float
        Expected log-preference of predicted outcomes, ``E_q[ln p(o | C)]``.
    epistemic : float
        Expected information gain about hidden states, ``I(o; s)`` under q.
    """

    G: float
    pragmatic: float
    epistemic: float


def infer_states(
    model: GenerativeModel,
    observation: Sequence[int],
    prior: Sequence[FloatArray],
) -> list[FloatArray]:
    """Posterior over hidden states given one multi-modality observation.

    Parameters
    ----------
    model : GenerativeModel
    observation : sequence of int
        One observation index per modality.
    prior : sequence of ndarray
        Per-factor prior, e.g. ``B[f][:, :, u_prev] @ qs_prev[f]``, or ``D`` at t=0.

    Returns
    -------
    list of ndarray
        Normalised per-factor posteriors.
    """
    raise NotImplementedError("AIS-040")


def expected_free_energy(
    model: GenerativeModel,
    qs: Sequence[FloatArray],
    policy: Policy,
) -> EFEResult:
    """Compute the expected free energy of a policy from current beliefs ``qs``.

    Accumulates over every step of ``policy`` using predicted beliefs. The sign
    convention must match ``docs/model.md``.
    """
    raise NotImplementedError("AIS-050")


def enumerate_policies(model: GenerativeModel, horizon: int) -> list[Policy]:
    """Return all valid action sequences of length <= ``horizon``.

    No sequence continues after a ``declare_*`` action.
    """
    raise NotImplementedError("AIS-052")


def infer_policies(
    G: FloatArray,
    gamma: float,
    E: FloatArray | None = None,
) -> FloatArray:
    """Policy posterior ``q(pi) = softmax(-gamma * G + ln E)``.

    Parameters
    ----------
    G : ndarray, shape (num_policies,)
    gamma : float
        Policy precision (> 0).
    E : ndarray, shape (num_policies,), optional
        Habit prior. Uniform if None.

    Returns
    -------
    ndarray, shape (num_policies,)
    """
    raise NotImplementedError("AIS-052")


def sample_action(
    q_pi: FloatArray,
    policies: Sequence[Policy],
    num_actions: int,
    rng: np.random.Generator,
) -> int:
    """Marginalise ``q(pi)`` over first actions and sample one."""
    raise NotImplementedError("AIS-053")


class ActiveInferenceAgent:
    """Perception-action loop wrapping the functions above.

    Interface shared with ``baselines``:

    - ``reset()``
    - ``act(observation, rng) -> int``
    """

    def __init__(self, model: GenerativeModel, horizon: int, gamma: float) -> None:
        self.model = model
        self.horizon = horizon
        self.gamma = gamma

    def reset(self) -> None:
        """Reset beliefs to the prior ``D``."""
        raise NotImplementedError("AIS-053")

    def act(self, observation: Sequence[int], rng: np.random.Generator) -> int:
        """Update beliefs from ``observation``, plan, and return an action index."""
        raise NotImplementedError("AIS-053")
