# Metabolism

Tutorials for single-cell metabolism inference via `ov.single.Metabolism`,
which dispatches to three complementary backends, plus
`ov.single.MetaboliteCCC` for metabolite-mediated cell-cell communication:

- **scMetabolism** (`method='scmetabolism'`) — metabolic pathway-activity
  scoring over curated KEGG / REACTOME gene sets (AUCell / VISION / ssGSEA / GSVA).
- **scFEA** (`method='scfea'`) — a graph-neural-network estimate of flux
  through ~168 metabolic modules.
- **Compass** (`method='compass'`) — constraint-based genome-scale
  reaction flux (loaded from a precomputed Compass run).
- **MEBOCOST** (`ov.single.MetaboliteCCC`) — metabolite cell-cell
  communication, reusing the `ov.pl.ccc_*` plots.

The per-cell backends write a unified schema
(`adata.obsm['X_metabolism']`, `adata.uns['metabolism']`) so
`ov.pl.metabolism_heatmap` works with any of them.

```{toctree}
:maxdepth: 1

../Tutorials-single/t_metabolism
../Tutorials-single/t_metabolism_ccc
```
