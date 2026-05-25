# Trajectory inference

Trajectory inference (TI) orders cells along inferred developmental pathways
and is one of the workhorses of single-cell analysis. omicverse exposes a
single entry point — `ov.single.TrajInfer` — that dispatches to **eleven**
backends spanning the methods compared in the [dynbenchmark
study](https://www.nature.com/articles/s41587-019-0071-9) (Saelens et al.,
2019, *Nat Biotechnol*).

This section has three layers:

| Layer | Tutorial | When |
|---|---|---|
| **1. Recommended workflow** | [t_traj_slingshot](t_traj_slingshot.ipynb) | Day-one user. Slingshot end-to-end on a real branching dataset, with PAGA overlay, branch-aware dynamic heatmaps and lineage-resolved trend plots. |
| **2. Unified downstream — fate** | [t_traj_fate](t_traj_fate.ipynb) | After any pseudotime backend you can run ``ov.single.PseudotimeFate(adata, pseudotime_key=...)`` for **macrostates → terminal states → fate probabilities** in <1 s on 3.7 k cells (≈300× faster than CellRank). Backend-agnostic — same code for Palantir / Slingshot / SCORPIUS / destiny / …. |
| **3. Method zoo** | [zoo/index](zoo/index.md) | You want to compare backends side-by-side, or you need a method that handles a specific topology (linear / multifurcating / cycle / convergence). 15 tutorials, one per backend. |

## Recommendation tree

```
        Do you have a known origin / terminal celltype?
                          │
                ┌─────────┴─────────┐
                yes                 no
                 │                   │
        Branching topology?     CytoTRACE2 (stemness gradient)
            │                   or destiny DPT (data-driven root)
   ┌────────┴────────┐
   bifurc / multi    linear
   │                   │
 Slingshot (recommended)  SCORPIUS / TSCAN / Palantir
   Palantir, VIA, URD
   Monocle3, scTour
```

## The eleven backends

| `method=` | Package | Topology supported | Notes |
|---|---|---|---|
| `'palantir'`    | palantir (vendored)   | tree, branching | Reference implementation. Best on continuous differentiation hierarchies. |
| `'diffusion_map'` | scanpy             | linear, branching | scanpy's `dpt` on the standard diffusion map. |
| `'slingshot'`   | _pyslingshot (vendored) | tree, branching | **Recommended** — outer-level tutorial. Lineage-resolved pseudotime + branch labels. |
| `'sctour'`      | sctour              | any (latent vector field) | Generative; also yields velocity. |
| `'stavia'`      | _stavia (vendored)  | tree, multifurc, cycle | spatial-aware variant. |
| `'scorpius'`    | [pyscorpius](https://pypi.org/project/pyscorpius/) | **linear** | dynbenchmark-style. Returns 1-D ordering only. |
| `'tscan'`       | [pytscan](https://pypi.org/project/pytscan/) | tree, branching | mclust-based clustering on first PCs, then MST traversal. |
| `'destiny'`     | [pydestiny-bio](https://pypi.org/project/pydestiny-bio/) | linear, branching | Python port of R `destiny`. DiffusionMap + DPT, data-driven root via DC1 extremum. |
| `'urd'`         | [pyurd-bio](https://pypi.org/project/pyurd-bio/) | branching | Flood-fill pseudotime on diffusion-map transitions. |
| `'monocle3'`    | [pymonocle3-bio](https://pypi.org/project/pymonocle3-bio/) | tree, branching | UMAP + principal graph; needs explicit root. |
| `'cytotrace'`   | [pycytotrace-bio](https://pypi.org/project/pycytotrace-bio/) | **gradient** | Gene-count correlate of stemness. Single-axis, no branches. |

The first 5 (palantir / diffusion_map / slingshot / sctour / stavia) ship
inside omicverse. The last 6 — the **dynbenchmark zoo** — are
`pip install omicverse[trajectory]` extras.

## Architecture

Every backend writes pseudotime under a unified obs schema:

```
adata.obs['{method}_pseudotime']   float    — universal
adata.obs['{method}_branch']       category — when the backend infers branches
adata.obsm['X_{method}']           latent   — when the backend builds an embedding
```

Downstream tools (PAGA, dynamic_heatmap, branch_streamplot, dynamic_features)
consume any backend's output via this schema — no `if method == ...` branching
in your downstream code.

## Reference

- Saelens W, Cannoodt R, Todorov H, Saeys Y. *A comparison of single-cell trajectory inference methods.* **Nat Biotechnol** 37, 547–554 (2019). [doi:10.1038/s41587-019-0071-9](https://doi.org/10.1038/s41587-019-0071-9)
