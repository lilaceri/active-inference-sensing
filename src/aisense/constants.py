"""Every tunable number in the project.

Tests import values from here so a setting can change without rewriting tests.
The values below are placeholders: choose them in AIS-020/021/022 and record
the reasoning in an ADR.
"""

from typing import Final

# --- Numerics -------------------------------------------------------------
EPS: Final[float] = 1e-16
"""Floor applied before taking logs (see ``maths.log_stable``)."""

# --- State space labels (AIS-020) -------------------------------------------
OBJECTS: Final[tuple[str, ...]] = ("car", "pedestrian", "cyclist", "background")
CONDITIONS: Final[tuple[str, ...]] = ("clear", "fog")
SENSORS: Final[tuple[str, ...]] = ("camera", "lidar", "radar")

# --- Planning (AIS-052) -------------------------------------------------------
POLICY_HORIZON: Final[int] = 2  # TODO(AIS-052): justify in an ADR
POLICY_PRECISION_GAMMA: Final[float] = 16.0  # TODO(AIS-052)

# --- Episode (AIS-030) ----------------------------------------------------------
MAX_STEPS: Final[int] = 6  # TODO(AIS-030)

# --- Preferences, in nats (AIS-022) ---------------------------------------------
REWARD_CORRECT: Final[float] = 0.0  # TODO(AIS-022)
PENALTY_INCORRECT: Final[float] = 0.0  # TODO(AIS-022)
SENSOR_COST: Final[dict[str, float]] = {  # TODO(AIS-022)
    "camera": 0.0,
    "lidar": 0.0,
    "radar": 0.0,
}

# --- Priors (AIS-022) -------------------------------------------------------------
PRIOR_FOG: Final[float] = 0.5  # TODO(AIS-022): p(condition = fog)
