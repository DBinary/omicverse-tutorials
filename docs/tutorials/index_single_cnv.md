# Copy-Number Variation

Tutorials for single-cell copy-number variation (CNV) inference via
`ov.single.CNV`, which dispatches to two pure-Python backends:

- **CopyKAT** ([py-CopyKAT](https://github.com/omicverse/py-CopyKAT)) —
  unsupervised aneuploid / diploid classification.
- **inferCNV** ([py-inferCNV](https://github.com/omicverse/py-inferCNV)) —
  reference-anchored CN matrix (needs a normal-cell annotation).

Both backends write a unified schema
(`adata.obsm['X_cnv']`, `adata.uns['cnv']`, `adata.obs['cnv_score']`)
so the plotting helpers (`ov.pl.cnv_heatmap`, `ov.pl.cnv_summary`,
`ov.pl.cnv_umap`) work with either.

```{toctree}
:maxdepth: 1

../Tutorials-single/t_copykat
../Tutorials-single/t_infercnv
```
