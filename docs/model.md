# Model Specification

This is the mathematical specification of the agent. The code must match it, and the judge checks that it does. Fill in each section as you reach its ticket.

## 1. Task

An agent must identify a hidden object, possibly in fog. Each step it either queries one sensor (camera, lidar or radar), each with its own reliability and cost, or declares a label.

## 2. Hidden state factors (AIS-020)

| Factor | Index → meaning | Dynamics |
|---|---|---|
| object | TODO | static |
| condition | TODO | static |
| decided | TODO | set by `declare_*` |

## 3. Observation modalities (AIS-020)

| Modality | Index → meaning | Depends on |
|---|---|---|
| sensor reading | TODO | TODO |
| feedback | TODO | TODO |

## 4. Actions (AIS-020)

| Index | Action | Effect |
|---|---|---|
| TODO | | |

## 5. Sensor models (AIS-020, AIS-021)

TODO: the confusion behaviour of each sensor in clear and in fog, with the reasoning.

## 6. Generative model: A, B, C, D (AIS-021, AIS-022)

TODO: LaTeX for $p(o_t \mid s_t)$, $p(s_{t+1} \mid s_t, u_t)$, $\ln p(o \mid C)$, $p(s_1)$.

## 7. State inference (AIS-040, AIS-041)

TODO: the posterior update, and whether mean-field is exact here (and why).

## 8. Expected free energy (AIS-050, AIS-051)

TODO: $G(\pi)$, its risk + ambiguity form, and its pragmatic + epistemic form. State the sign convention.

## 9. Policy selection (AIS-052, AIS-053)

TODO: $q(\pi) = \sigma(-\gamma G + \ln E)$, the horizon, and action marginalisation.

## References

- Friston, K., FitzGerald, T., Rigoli, F., Schwartenbeck, P., & Pezzulo, G. (2017). Active inference: a process theory. *Neural Computation*, 29(1).
- Parr, T., Pezzulo, G., & Friston, K. (2022). *Active Inference: The Free Energy Principle in Mind, Brain, and Behavior*. MIT Press.
- Smith, R., Friston, K., & Whyte, C. (2022). A step-by-step tutorial on active inference and its application to empirical data. *Journal of Mathematical Psychology*, 107.
