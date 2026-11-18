# Active Inference for Multi-Sensor Active Sensing

<!-- TODO(AIS-083): CI badge -->

An agent built from scratch in NumPy, using **active inference**, that decides *which sensor to look through* before it names an object. It trades off the information a query would give against what the query costs.

> TODO(AIS-080): one-paragraph pitch, and the headline result with numbers.

## The problem

A hidden object (car, pedestrian, cyclist or background) may be in fog. The agent can query a camera, lidar or radar, each with different noise and cost, or it can commit to a label. A good agent has to:

- seek information when it is uncertain (epistemic value)
- stop querying when it is confident (pragmatic value)
- work out that it is foggy, and stop trusting the camera

## Results

> TODO(AIS-070, AIS-071): results table and figures from `results/`.

## What I built

> TODO(AIS-080): map each concept to its file (generative model, state inference, expected free energy, policy selection).

The full maths is in [docs/model.md](docs/model.md).

## How to run

```bash
uv sync --all-groups
uv run pytest
uv run python experiments/run_benchmark.py --episodes 1000 --seed 0
uv run python experiments/visualise_episode.py --seed 0 --fog
```

## How this was built

- Each feature was developed test-first, against tickets tracked as [GitHub issues](https://github.com/lilaceri/active-inference-sensing/issues) (index in [CHECKLIST.md](CHECKLIST.md)).
- Each ticket was graded by an AI judge against explicit acceptance criteria. The verdicts are in [docs/reviews/](docs/reviews/).
- The AI did not write the implementation. Design decisions are logged in [docs/decisions/](docs/decisions/).

## License

MIT
