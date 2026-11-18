# Checklist

Work through the tickets in order. For each one:

1. Branch.
2. RED → GREEN → REFACTOR (see [AGENTS.md](AGENTS.md#strict-test-driven-development)).
3. Update the records.
4. Run `/judge AIS-0xx`.

A box is ticked **only** after a PASS verdict in `docs/reviews/`.

Acceptance criteria (AC) are what the judge grades. If you find that a criterion is wrong while you work, change it in the same PR and say why in the review.

---

## E0: Setup

- [ ] **AIS-001: Environment and CI green**
    - AC1: `uv sync --all-groups` succeeds on a fresh clone.
    - AC2: `uv run pre-commit install`, then `uv run pre-commit run --all-files` passes.
    - AC3: `uv run pytest` passes (smoke test).
    - AC4: The CI workflow is green on GitHub for the pushed commit.
    - AC5: README "How to run" matches the commands you actually used.

## E1: Maths utilities (`src/aisense/maths.py`, `tests/test_maths.py`)

- [ ] **AIS-010: `softmax` and `log_stable`**
    - AC1: `softmax` output is non-negative and sums to 1 along axis 0. Tested on random inputs, including with `hypothesis`.
    - AC2: `softmax` is invariant to adding a constant: `softmax(x + c) == softmax(x)`.
    - AC3: `softmax` does not overflow on inputs around ±1e3, and returns finite values.
    - AC4: `log_stable(0)` is finite and equals `log(EPS)` (EPS from `constants.py`). For p > EPS it matches `np.log(p)`.
- [ ] **AIS-011: `entropy` and `kl_divergence`**
    - AC1: The entropy of a one-hot distribution is 0, and the entropy of a uniform distribution over n is `log(n)`.
    - AC2: Entropy ≥ 0 for random distributions.
    - AC3: KL(p‖p) = 0, KL(p‖q) ≥ 0, and KL is asymmetric on a hand-checked example.
    - AC4: Zero entries are handled without NaN.
- [ ] **AIS-012: factor dot products (`dot_likelihood`, `spm_dot`-style contraction)**
    - AC1: Contracting `A` of shape `(o, s1, s2)` with beliefs `[q1, q2]` equals an explicit `np.einsum` reference.
    - AC2: Works for 1 and 2 state factors.
    - AC3: Raises `ValueError` on a shape mismatch, and the test asserts that.

## E2: Generative model (`src/aisense/generative_model.py`)

- [ ] **AIS-020: Specify the model on paper**
    - AC1: `docs/model.md` lists these, each with an index → meaning table:
        - state factors (object, condition, decided)
        - observation modalities (sensor reading, feedback, cost signal if used)
        - actions
    - AC2: ADR `0002-model-structure.md` records why these factors and modalities were chosen, and what was rejected.
    - AC3: Each sensor's confusion behaviour is described in clear and in fog.
- [ ] **AIS-021: `SensorSpec` and the likelihood `A`**
    - AC1: `SensorSpec` is a frozen dataclass. Its accuracies and costs come from `constants.py`.
    - AC2: `build_A` returns arrays with the shapes stated in `docs/model.md`.
    - AC3: Every column of every `A[m]` sums to 1 (test over all state combinations).
    - AC4: The camera in fog is less informative than in clear. A test shows this by comparing the mutual information or entropy of the columns.
    - AC5: Radar `A` does not depend on the condition factor.
- [ ] **AIS-022: `B`, `C`, `D`**
    - AC1: `B[f]` columns sum to 1 for every action.
    - AC2: Object and condition are static. A `declare_*` action moves `decided` to true, and it is absorbing.
    - AC3: `C` rewards correct feedback, penalises incorrect feedback, and encodes the per-sensor cost. The values come from `constants.py`.
    - AC4: `D` is a normalised prior per factor.
- [ ] **AIS-023: `GenerativeModel` container and validation**
    - AC1: A single `validate()` checks every normalisation and shape invariant, and raises on violations.
    - AC2: Tests feed it deliberately broken models (an unnormalised column, a wrong shape) and assert that it raises.

## E3: Environment (`src/aisense/env.py`)

- [ ] **AIS-030: Generative process**
    - AC1: `SensingEnv.reset(rng)` samples the true object and condition from the configured priors.
    - AC2: `step(action)` returns observations in the same index space as the model.
    - AC3: The episode ends on `declare_*` or after `MAX_STEPS`.
    - AC4: Over ≥5k seeded samples, the empirical sensor confusion matches the spec within a stated Monte Carlo tolerance.
- [ ] **AIS-031: Reproducibility**
    - AC1: The same seed produces an identical trajectory, and a different seed produces a different one (asserted).
    - AC2: The global NumPy RNG is not used anywhere. A test or grep check enforces this.

## E4: State inference (`src/aisense/agent.py`)

- [ ] **AIS-040: `infer_states`**
    - AC1: It implements the posterior update from `docs/model.md`: prior from `B·qs`, combined with the likelihood of the observations across all modalities.
    - AC2: Output beliefs are normalised per factor.
    - AC3: An uninformative observation leaves the beliefs equal to the prior.
- [ ] **AIS-041: Inference against an oracle**
    - AC1: For random small models and observation sequences, the marginals from `infer_states` match brute-force Bayes over the full joint. The tolerance is justified in a comment (exact if the factors are conditionally independent, otherwise document the mean-field gap).
    - AC2: `docs/model.md` states which case applies, and why.

## E5: Planning

- [ ] **AIS-050: `expected_free_energy`**
    - AC1: Returns `G` together with its separate pragmatic and epistemic parts, as named fields.
    - AC2: `G = -(pragmatic + epistemic)` (or the sign convention documented in `docs/model.md`). The test asserts the identity.
    - AC3: Docstring equations match `docs/model.md`.
- [ ] **AIS-051: Epistemic value is information gain**
    - AC1: The epistemic term equals the mutual information I(o; s), computed independently from the joint p(o, s).
    - AC2: An uninformative sensor has epistemic value 0 (to tolerance).
    - AC3: With a uniform belief over the object, lidar has higher epistemic value than radar.
- [ ] **AIS-052: Policies and the policy posterior**
    - AC1: `enumerate_policies(horizon)` produces every valid action sequence, and none continue after a `declare`.
    - AC2: `G` for a multi-step policy accumulates over the horizon, using predicted beliefs.
    - AC3: `q(π) = softmax(-γ·G + ln E)` sums to 1. As γ → ∞ it becomes one-hot on the argmin of G.
    - AC4: The horizon and γ come from `constants.py`.
- [ ] **AIS-053: Action selection and agent loop**
    - AC1: `sample_action` marginalises q(π) over first actions, and samples with a passed `rng`.
    - AC2: Behavioural test: when the belief is already confident (e.g. p(object) > 0.95), the agent declares rather than queries, in ≥ 90% of seeded trials.
    - AC3: Behavioural test: from a uniform belief, the agent's first action is a sensor query, not a declaration.

## E6: Baselines (`src/aisense/baselines.py`)

- [ ] **AIS-060: Comparison agents**
    - AC1: The baselines share the agent interface:
        - `RandomSensorAgent`
        - `FixedOrderAgent`
        - `PragmaticOnlyAgent` (the active inference agent with the epistemic term removed)
    - AC2: The ablation reuses `expected_free_energy`, and is not a copy-paste.
    - AC3: Each baseline has a seeded behavioural test.

## E7: Experiments (`experiments/`)

- [ ] **AIS-070: Benchmark**
    - AC1: `uv run python experiments/run_benchmark.py --episodes N --seed S` writes `results/benchmark.csv` and `results/benchmark.png`. Columns:
        - accuracy
        - mean queries
        - mean cost
        - reward
        - standard error
    - AC2: A matching experiment record in `docs/experiments/` gives the hypothesis, commit SHA, exact command and seeds, results table, conclusion and limitations.
    - AC3: The README claim matches the record.
- [ ] **AIS-071: Episode visualisation**
    - AC1: `experiments/visualise_episode.py --seed S [--fog]` saves a figure with:
        - belief evolution per factor
        - the per-step pragmatic and epistemic parts of G for each action
        - the chosen action
    - AC2: A fog episode shows the agent preferring a non-camera sensor once its belief in fog is high. This is noted in the experiment record.
- [ ] **AIS-072: Results committed**
    - AC1: The figures are in `results/`, each < 1 MB, and are referenced from the README.

## E8: Showcase

- [ ] **AIS-080: README results**
    - AC1: The README has a one-paragraph pitch, the results table, and both figures.
    - AC2: It states the headline finding with numbers.
    - AC3: It has a "What I built" section that maps concepts to files.
- [ ] **AIS-081: Maths write-up**
    - AC1: `docs/model.md` has LaTeX for:
        - the generative model
        - VFE / the posterior update
        - EFE, with its risk + ambiguity and pragmatic + epistemic decompositions
        - the policy posterior
    - AC2: It has references (Friston et al. 2017; Parr, Pezzulo & Friston 2022; Smith, Friston & Whyte 2022 tutorial).
- [ ] **AIS-082 (optional): Walkthrough notebook**
    - AC1: `notebooks/walkthrough.ipynb` runs top to bottom with `jupyter nbconvert --execute`, and uses only the package API.
- [ ] **AIS-083: Presentation**
    - AC1: The repo description, topics (`active-inference`, `free-energy-principle`, `bayesian-inference`, `numpy`) and pin are set. The CI badge is in the README.
