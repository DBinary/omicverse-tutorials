# H&E → spatial transcriptomics prediction (HE-zoo)

Predict spot-level (or sub-spot-level) gene expression directly from
H&E histology images. Every notebook below predicts on the same
10x Visium Breast Cancer Block A Section 1 H&E so the four backends
are directly comparable; HEST-FM / STPath / STFlow additionally
re-run on **Section 2** of the same patient block as a held-out
"never-seen H&E" check.

See [`Tutorials-space/he-zoo/index.md`](../Tutorials-space/he-zoo/index.md)
for the per-backend feature matrix and "which to pick when" guidance.

```{toctree}
:maxdepth: 1

../Tutorials-space/he-zoo/t_histo_hest_fm
../Tutorials-space/he-zoo/t_histo_stpath
../Tutorials-space/he-zoo/t_histo_stflow
../Tutorials-space/he-zoo/t_histo_istar
```
