# MetaCell zoo

`ov.single.MetaCell` ships **seven backend partitioners** behind a single API.
Each method has a different algorithmic philosophy and a different trade-off
between speed, scalability, and downstream-task quality.

This zoo gives each backend a dedicated notebook so you can see how its
particular hyperparameters and outputs behave on the same dataset (mouse
pancreas, Bastidas-Ponce et al. 2019), then a final comparison notebook that
runs them all side-by-side and ranks them on purity, mcRigor score, and
runtime.

| Backend | Paper | Capabilities | Tutorial |
|---|---|---|---|
| `seacells`  | Persad 2023 (Nat Biotech)       | soft, latent                                                | [t_metacell_seacells](t_metacell_seacells.ipynb) |
| `metaq`     | Li 2025 (Nat Comms)             | soft, latent, codebook, out_of_sample, multimodal, streaming | [t_metacell_metaq](t_metacell_metaq.ipynb) |
| `supercell` | Bilous 2022 (BMC Bioinformatics)| hierarchical                                                | [t_metacell_supercell](t_metacell_supercell.ipynb) |
| `kmeans`    | (baseline)                      | latent, codebook, out_of_sample                             | [t_metacell_kmeans](t_metacell_kmeans.ipynb) |
| `random`    | (honest baseline)               | —                                                           | [t_metacell_random](t_metacell_random.ipynb) |
| `geosketch` | Hie 2019 (Cell Systems)         | out_of_sample                                               | [t_metacell_geosketch](t_metacell_geosketch.ipynb) |
| `mc2`       | Ben-Kiki 2022 (Genome Biology)  | streaming                                                   | `pip install metacells` + `method='mc2'` |

**Side-by-side comparison** → [t_metacell_compare](t_metacell_compare.ipynb).

Every per-backend notebook runs the same diagnostics (helpers live in
`ov.pl.*` — the notebook cells stay short):

- `ov.pl.metacell_metrics(mc)` — purity / separation / compactness with histograms.
- `mc.check_rigor()` + `ov.pl.rigor_scatter(rep)` — mcRigor validator.
- UMAP with metacell centroids overlaid — `ov.pl.embedding` + a 3-line scatter.
- `ov.pl.metacell_purity_box(mc)` — per-celltype boxplot.
- A **metacell-level UMAP** built via the standard `ov.pp.preprocess` → PCA → UMAP loop on the aggregated AnnData.
- `ov.single.find_markers` + `ov.pl.markers_dotplot` — top markers per celltype.

Plus one backend-specific section per method (`ov.pl.metacell_soft_heatmap`
for SEACells; `ov.pl.metacell_codebook_umap` + `mc.assign_new_cells` for
MetaQ; `mc.fit_multi_gamma` for SuperCell; etc.).

## Which one should I use?

| Task | Recommended |
|---|---|
| UMAP / Leiden / quick visualisation | `kmeans` or `geosketch` (cheap, ~as good) |
| Differential expression / cell–cell communication / GRN inference | `seacells` or `metaq` (proper aggregation) |
| Atlas-style workflow with new samples arriving over time | `metaq` (closed-form out-of-sample via encoder + codebook) |
| Multi-million cell dataset | `metaq` (linear-time) or `mc2` (divide-and-conquer) |
| "Is my metacell pipeline even worth it?" sanity check | `random` (lower bound) |

All seven backends write a unified AnnData schema (`obs['metacell_id']`,
`obs['metacell_conf']`, optional `obsm['X_metacell']` and `obsm['metacell_soft']`,
`uns['metacell']`), so downstream tools (CellPhoneDB, SCENIC, pseudobulk DE)
consume any of them without an `if backend == ...` branch.
