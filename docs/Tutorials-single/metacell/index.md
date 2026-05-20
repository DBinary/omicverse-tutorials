# MetaCell

Metacells are **small, transcriptionally homogeneous groups of single cells**
that are treated as the unit of analysis instead of individual cells.  They
denoise sparse single-cell counts while preserving cell-state granularity —
unlike Leiden clusters (too coarse for state-level analysis) or single cells
(too sparse for many downstream tools).

This section has three layers:

| Layer | Tutorial | When |
|---|---|---|
| **1. Recommended workflow** | [t_metacell_recommended](t_metacell_recommended.ipynb) | Day-one user.  Run the recommended backend (SEACells, soft membership) end-to-end and drive a downstream pipeline (DEG, pseudobulk, marker dotplot). |
| **2. Multi-sample workflow** | [t_metacell_multisample](t_metacell_multisample.ipynb) | You have ≥2 batches / donors / conditions.  Build per-sample-aware metacells on a Harmony-corrected embedding. |
| **3. Backend zoo** | [zoo/index](zoo/index.md) | You want to compare all 7 backends side-by-side on your own data (`ov.single.compare_metacell_backends`), or read why each method exists. |

## Metacell vs pseudobulk — what's the difference?

Both metacells and pseudobulk produce aggregated count profiles, but they
answer different questions and have different statistical properties.

| | **Pseudobulk** | **Metacell** |
|---|---|---|
| **Granularity** | One profile per *sample × celltype* (or *sample × cluster*) — usually 5–50 profiles total. | One profile per metacell — typically `N // 50` profiles, i.e. **hundreds to thousands**. |
| **Aggregation key** | Pre-existing labels (sample, celltype). | Learned partition based on transcriptional similarity (graph / archetype / VQ-VAE / …). |
| **Within-group purity** | Whatever the labels imply (often messy — "Beta cells from sample 3" still has substate variation). | Optimized to be **transcriptionally homogeneous** — each metacell ≈ one cell state. |
| **Sample / batch awareness** | Native — sample is the aggregation key. | Optional — most backends are sample-agnostic by default; multi-sample workflows need a corrected embedding (see [t_metacell_multisample](t_metacell_multisample.ipynb)). |
| **What it's good for** | **Cohort-level DE** (DESeq2 / edgeR / limma): "does gene X change between healthy and IBD donors *averaged over* T cells?" | **State-level analysis** with denoised counts: cell-cell communication, GRN inference, RNA velocity, marker discovery, trajectory smoothing. |
| **What it's NOT good for** | Within-celltype state granularity, trajectory inference, cell-cell communication. | Cohort-level DE (you'd be testing thousands of "samples", inflating power and breaking the variance model). |
| **Typical N profiles** | ~10s | ~100s–1000s |

**Rule of thumb**: if your statistical model is `expression ~ condition` and
treats samples as the unit of replication, you want **pseudobulk**.  If your
model is "give me per-cell-state expression but with less noise", you want
**metacell**.

The two are also **composable**: you can pseudobulk metacells per sample
(e.g. for cross-sample DE within a metacell type), or compute metacells
within each sample independently and then concatenate.  omicverse's
[t_metacell_multisample](t_metacell_multisample.ipynb) shows the latter.

## Architecture

`ov.single.MetaCell(adata, method=...)` dispatches to seven backends, each
writing a unified AnnData schema:

```
adata.obs['metacell_id']      categorical — universal
adata.obs['metacell_conf']    float       — universal
adata.obsm['X_metacell']      latent      — when backend has 'latent' capability
adata.obsm['metacell_soft']   sparse      — when backend has 'soft' capability
adata.uns['metacell']         metadata    — method, n_metacells, runtime, ...
```

Downstream tools (CellPhoneDB / LIANA / SCENIC / DESeq2) consume any
backend's output via this schema — you never need an `if method == ...`
branch.

The seven backends, with their differentiating capability:

- `seacells` — soft kernel archetypal analysis (Persad 2023, Nat Biotech).  Default recommendation.
- `metaq` — VQ-VAE codebook with **closed-form out-of-sample projection** (Li 2025, Nat Comms).  Use when new samples will arrive after the metacell map is built.
- `supercell` — kNN + walktrap with **graining hierarchy cache** (Bilous 2022, BMC Bioinf).
- `kmeans` — sklearn baseline (fast, codebook, out-of-sample).
- `random` — honest lower bound.
- `geosketch` — density-aware sketching (Hie 2019, Cell Systems).
- `mc2` — divide-and-conquer (Ben-Kiki 2022, Genome Biology).  `pip install metacells`.

See [zoo/index](zoo/index.md) for the full per-backend tour.
