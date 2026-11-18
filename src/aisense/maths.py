"""Pure numerical utilities for discrete active inference.

Every function here is pure and has no side effects. See ``AGENTS.md`` for array conventions.
"""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def log_stable(x: FloatArray) -> FloatArray:
    """Natural log with a floor to avoid ``-inf`` on zero entries.

    Parameters
    ----------
    x : ndarray, any shape
        Non-negative values (typically probabilities).

    Returns
    -------
    ndarray, same shape as ``x``
        ``log(max(x, EPS))`` with ``EPS`` from ``constants``.
    """
    raise NotImplementedError("AIS-010")


def softmax(x: FloatArray) -> FloatArray:
    """Normalised exponential along axis 0, numerically stable.

    Parameters
    ----------
    x : ndarray, shape (n,) or (n, k)
        Unnormalised log-probabilities.

    Returns
    -------
    ndarray, same shape as ``x``
        ``exp(x - max(x)) / sum(exp(x - max(x)))`` along axis 0.
    """
    raise NotImplementedError("AIS-010")


def entropy(p: FloatArray) -> float:
    """Shannon entropy in nats, ``H[p] = -sum_i p_i log p_i``.

    Parameters
    ----------
    p : ndarray, shape (n,)
        A normalised distribution.

    Returns
    -------
    float
        Entropy (>= 0). Zero entries contribute 0.
    """
    raise NotImplementedError("AIS-011")


def kl_divergence(p: FloatArray, q: FloatArray) -> float:
    """Kullback-Leibler divergence ``KL[p || q] = sum_i p_i (log p_i - log q_i)``.

    Parameters
    ----------
    p, q : ndarray, shape (n,)
        Normalised distributions over the same support.

    Returns
    -------
    float
        Divergence in nats (>= 0).
    """
    raise NotImplementedError("AIS-011")


def dot_likelihood(A: FloatArray, qs: Sequence[FloatArray]) -> FloatArray:
    """Contract a likelihood tensor with factorised beliefs over the hidden states.

    Computes ``sum_{s1..sF} A[o, s1, ..., sF] * q1[s1] * ... * qF[sF]``.

    Parameters
    ----------
    A : ndarray, shape (num_obs, num_states_1, ..., num_states_F)
        Likelihood ``p(o | s)``, normalised over axis 0.
    qs : sequence of F ndarrays, shapes (num_states_f,)
        Mean-field beliefs, one per state factor.

    Returns
    -------
    ndarray, shape (num_obs,)
        Predicted observation distribution ``p(o) = E_q[p(o | s)]``.

    Raises
    ------
    ValueError
        If the number or sizes of the factors don't match ``A``.
    """
    raise NotImplementedError("AIS-012")
