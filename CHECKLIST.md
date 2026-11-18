# Checklist

Tickets are tracked as **GitHub issues**. Each group of tickets (an epic) is a parent issue, and its tickets are sub-issues, so GitHub shows progress per epic. **The acceptance criteria (AC) live in the issue body.** The issue is the single source of truth that the judge grades against. This file is only an index.

## Workflow for each ticket

1. Branch: `git switch -c feat/AIS-0xx-short-name`.
2. RED → GREEN → REFACTOR (see [AGENTS.md](AGENTS.md#strict-test-driven-development)).
3. Update the records.
4. Open a PR with `Closes #N` in the description.
5. Run `/judge AIS-0xx`.
6. Merge on PASS. The issue then closes automatically.

If you find that an acceptance criterion is wrong while you work, edit the issue and say why in the PR.

## Index

| Epic | Ticket | Issue |
|---|---|---|
| [E0: Setup (#1)](https://github.com/lilaceri/active-inference-sensing/issues/1) | AIS-001 Environment and CI green | [#10](https://github.com/lilaceri/active-inference-sensing/issues/10) |
| [E1: Maths utilities (#2)](https://github.com/lilaceri/active-inference-sensing/issues/2) | AIS-010 softmax and log_stable | [#11](https://github.com/lilaceri/active-inference-sensing/issues/11) |
| | AIS-011 entropy and kl_divergence | [#12](https://github.com/lilaceri/active-inference-sensing/issues/12) |
| | AIS-012 Factor dot products | [#13](https://github.com/lilaceri/active-inference-sensing/issues/13) |
| [E2: Generative model (#3)](https://github.com/lilaceri/active-inference-sensing/issues/3) | AIS-020 Specify the model on paper | [#14](https://github.com/lilaceri/active-inference-sensing/issues/14) |
| | AIS-021 SensorSpec and the likelihood A | [#15](https://github.com/lilaceri/active-inference-sensing/issues/15) |
| | AIS-022 B, C, D | [#16](https://github.com/lilaceri/active-inference-sensing/issues/16) |
| | AIS-023 GenerativeModel container and validation | [#17](https://github.com/lilaceri/active-inference-sensing/issues/17) |
| [E3: Environment (#4)](https://github.com/lilaceri/active-inference-sensing/issues/4) | AIS-030 Generative process | [#18](https://github.com/lilaceri/active-inference-sensing/issues/18) |
| | AIS-031 Reproducibility | [#19](https://github.com/lilaceri/active-inference-sensing/issues/19) |
| [E4: State inference (#5)](https://github.com/lilaceri/active-inference-sensing/issues/5) | AIS-040 infer_states | [#20](https://github.com/lilaceri/active-inference-sensing/issues/20) |
| | AIS-041 Inference against an oracle | [#21](https://github.com/lilaceri/active-inference-sensing/issues/21) |
| [E5: Planning (#6)](https://github.com/lilaceri/active-inference-sensing/issues/6) | AIS-050 expected_free_energy | [#22](https://github.com/lilaceri/active-inference-sensing/issues/22) |
| | AIS-051 Epistemic value is information gain | [#23](https://github.com/lilaceri/active-inference-sensing/issues/23) |
| | AIS-052 Policies and the policy posterior | [#24](https://github.com/lilaceri/active-inference-sensing/issues/24) |
| | AIS-053 Action selection and agent loop | [#25](https://github.com/lilaceri/active-inference-sensing/issues/25) |
| [E6: Baselines (#7)](https://github.com/lilaceri/active-inference-sensing/issues/7) | AIS-060 Comparison agents | [#26](https://github.com/lilaceri/active-inference-sensing/issues/26) |
| [E7: Experiments (#8)](https://github.com/lilaceri/active-inference-sensing/issues/8) | AIS-070 Benchmark | [#27](https://github.com/lilaceri/active-inference-sensing/issues/27) |
| | AIS-071 Episode visualisation | [#28](https://github.com/lilaceri/active-inference-sensing/issues/28) |
| | AIS-072 Results committed | [#29](https://github.com/lilaceri/active-inference-sensing/issues/29) |
| [E8: Showcase (#9)](https://github.com/lilaceri/active-inference-sensing/issues/9) | AIS-080 README results | [#30](https://github.com/lilaceri/active-inference-sensing/issues/30) |
| | AIS-081 Maths write-up | [#31](https://github.com/lilaceri/active-inference-sensing/issues/31) |
| | AIS-082 (optional) Walkthrough notebook | [#32](https://github.com/lilaceri/active-inference-sensing/issues/32) |
| | AIS-083 Presentation | [#33](https://github.com/lilaceri/active-inference-sensing/issues/33) |

New tickets: use the **Ticket** issue template, take the next free AIS number in the epic's range, attach the issue as a sub-issue of its epic, and add a row here.
