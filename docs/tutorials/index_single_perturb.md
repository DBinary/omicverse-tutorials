# In-silico Perturbation

In-silico gene knockout / over-expression with downstream GRN
reconstruction via `ov.single.perturb`. Two backends — scTenifoldKnk
(scRNA only) and CellOracle (RNA + optional ATAC base GRN) — share a
single API and a single `PerturbResult` dataclass.

```{toctree}
:maxdepth: 1

../Tutorials-single/perturb/index
../Tutorials-single/perturb/t_perturb_sctenifoldknk
../Tutorials-single/perturb/t_perturb_celloracle
../Tutorials-single/perturb/t_perturb_unified
```
