"""Build the HE-zoo tutorial notebooks **with executed outputs**.

The cell sources live as plain Python comment blocks in this file. The
builder converts them to `nbformat` notebooks, executes each, and writes
``.ipynb`` files next to it. Tutorial cells therefore never define
functions — all reusable code lives in :mod:`omicverse.space.histo`.

Usage::

    OV_HISTO_CACHE=/scratch/users/steorra/cache/omicverse_histo \\
        python build_notebooks.py [hest_fm|stpath|stflow|istar|all]
"""
from __future__ import annotations

import os
import sys
import textwrap
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

# Allow running the in-process runner without a kernel subprocess.
sys.path.insert(0, str(Path(__file__).parent))
from _runner import run_cells

HERE = Path(__file__).parent


def _md(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(textwrap.dedent(text).strip())


def _code(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(textwrap.dedent(text).strip())


def _build_and_run(name: str, cells: list[nbf.NotebookNode], *, timeout: int = 3600) -> Path:
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata.update({
        "kernelspec": {"display_name": "omicdev", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    })
    out = HERE / f"t_histo_{name}.ipynb"
    no_execute = os.environ.get("OV_HISTO_NB_NO_EXECUTE", "").lower() in {"1", "true", "yes"}
    if no_execute:
        nbf.write(nb, out)
        print(f"[skeleton] wrote {out} (no execution)", flush=True)
        return out
    use_kernel = os.environ.get("OV_HISTO_NB_USE_KERNEL", "").lower() in {"1", "true", "yes"}
    print(f"[build] executing {name}", flush=True)
    if use_kernel:
        kernel_name = os.environ.get("OV_HISTO_NB_KERNEL", "omicdev")
        allow_errors = os.environ.get("OV_HISTO_NB_ALLOW_ERRORS", "").lower() in {"1", "true", "yes"}
        client = NotebookClient(
            nb, timeout=timeout, kernel_name=kernel_name,
            resources={"metadata": {"path": str(HERE)}},
            allow_errors=allow_errors,
        )
        client.execute()
    else:
        nb.cells = run_cells(nb.cells, namespace={"__name__": "__main__"})
    nbf.write(nb, out)
    print(f"[done] wrote {out}", flush=True)
    return out


# ---------------------------------------------------------------------------
# HEST-FM tutorial
# ---------------------------------------------------------------------------

def hest_fm_cells() -> list[nbf.NotebookNode]:
    return [
        _md("""
            # HEST-FM — pathology foundation model + ridge head

            The HEST benchmark (Jaume et al., *NeurIPS 2024 Spotlight*)
            showed that the strongest recipe for predicting spatial
            expression from H&E is also the simplest: take a pretrained
            pathology foundation model (UNI / CONCH / Virchow2 /
            GigaPath / CTransPath / …), extract per-tile features, fit
            one ridge regression per gene on a paired Visium slide, and
            predict on new tiles. With ≥1 paired reference slide this
            beats most end-to-end deep architectures while training in
            seconds.

            `ov.space.histo.predict_expression(method='hest_fm')`
            implements this recipe end-to-end on top of LazySlide /
            WSIData.

            **Why "with paired reference"?** A single Visium slide gives
            you 3–5 k (tile, expression) training pairs, more than
            enough to fit a stable linear head per gene. This is in
            contrast to STPath / STFlow which are pretrained
            cross-cohort and can run zero-shot on a brand-new H&E.

            This notebook uses the **all-public CTransPath** backbone so
            it runs without any HuggingFace gating. For higher accuracy
            swap in `fm_backbone='uni2'`, `'conch_v1.5'`, `'virchow2'`,
            or `'gigapath'` once you have access.
        """),
        _md("## Environment"),
        _code("""
            import warnings
            warnings.filterwarnings('ignore')

            import omicverse as ov
            import lazyslide as zs

            ov.utils.ov_plot_set()
            print('omicverse', ov.__version__, '| lazyslide', zs.__version__)
        """),
        _md("""
            ## How the WSI flows through LazySlide

            `ov.space.histo` does **not** re-implement WSI handling —
            it wraps [LazySlide](https://github.com/RendeiroLab/LazySlide)
            (the scverse-aligned WSI toolkit) and lifts its `WSIData`
            container into the omicverse namespace. Concretely:

            | omicverse call | LazySlide / wsidata under the hood |
            |---|---|
            | `ov.space.histo.open_wsi(path)` | `wsidata.open_wsi(path)` — returns a `WSIData` (a `SpatialData` subclass) wrapping the slide reader (openslide / tiffslide / bioformats) and a thumbnail |
            | `ov.space.histo.tile(wsi, …)` | `zs.pp.find_tissues` + `zs.pp.tile_tissues` — writes tissue contours to `wsi.shapes['tissues']` and a tile grid to `wsi.shapes['tiles']` |
            | `ov.space.histo.embed(wsi, model=…)` | `zs.tl.feature_extraction` — runs the chosen pathology FM on every tile and stores features as `wsi.tables['{model}_tiles']` (an AnnData with one row per tile) |
            | `ov.space.histo.predict_expression(wsi, method=…)` | omicverse-specific: writes another AnnData table `wsi.tables['{method}_tiles']` with predicted gene expression |

            The `WSIData` API surface stays available — drop down to
            `zs.pp.*` / `zs.tl.*` / `zs.pl.*` whenever you need finer
            control than the convenience wrappers expose.
        """),
        _md("""
            ## Inputs HEST-FM expects

            Two objects, both in the *same pixel coordinate frame*:

            - **`reference` — paired Visium AnnData**
              - `reference.X` (n_spots × n_genes) — raw spot counts
              - `reference.obsm['spatial']` (n_spots × 2) — spot pixel
                centroids in the H&E frame
              - `reference.uns['spatial'][lib]['scalefactors']['spot_diameter_fullres']`
                — the spot diameter in full-resolution pixels; HEST-FM
                uses it as the side length of the reference patches it
                cuts out under each spot
            - **`wsi` — `wsidata.WSIData`** wrapping the H&E used in the
              reference, plus optionally any *query* H&E you want to
              predict on. In this tutorial both reference and query are
              the same slide, but you can also tile and embed a
              *different* slide as the query as long as its tile
              features come from the same `fm_backbone`.

            Both objects are returned together by `load_breast()`; the
            next markdown cell shows how to assemble them for your own
            data.
        """),
        _md("""
            ## Model weights & cache layout

            HEST-FM uses **one pretrained foundation-model checkpoint**
            (the patch encoder) and trains a tiny ridge head per gene
            on the user's reference. Everything is auto-downloaded on
            first use; nothing needs manual setup beyond the install.

            | What | From | To | Size | Gated? |
            |---|---|---|---|---|
            | `ctranspath` patch encoder (default) | LazySlide model registry → HF `RendeiroLab/LazySlide-models-gpl` | `$HF_HOME/hub/` (default `~/.cache/huggingface/hub`) | ~100 MB | no |
            | reference spot-patch features (per slide / backbone) | computed once | `$OV_HISTO_CACHE/ref_features/{backbone}_{slide_stem}_n{n_spots}.h5ad` | ~10–50 MB | — |
            | query tile features (per slide / tile-grid / backbone) | computed once | `$OV_HISTO_CACHE/tile_features/{backbone}_{slide_stem}_{tile_key}_n{n_tiles}.h5ad` | ~10–50 MB | — |
            | per-gene Ridge head | trained at predict time | in-memory, not persisted | — | — |

            `$OV_HISTO_CACHE` defaults to `~/.cache/omicverse/histo`.
            Override the location with `OV_HISTO_CACHE=/some/path`
            (recommended on HPC: point it at a scratch filesystem).
            Override the HuggingFace location with `HF_HOME=/some/path`
            (default `~/.cache/huggingface`).

            **Swapping to a more accurate gated backbone** — set
            `fm_backbone='uni2'` (or `'conch_v1.5'`, `'virchow2'`,
            `'gigapath'`, `'h-optimus-1'`) once you have HuggingFace
            access. Request access on the model card, then
            `huggingface-cli login` once on this machine. LazySlide
            handles the gated download for you.
        """),
        _md("## Load the demo dataset"),
        _md(
            "`ov.space.histo.load_breast()` downloads and caches the 10x "
            "Visium Breast Cancer Block A Section 1 sample under "
            "`$OV_HISTO_CACHE/he_zoo/visium_breast` (~1.7 GB on disk; one-time)."
        ),
        _code("""
            adata, wsi = ov.space.histo.load_breast()
            adata
        """),
        _code("""
            wsi
        """),
        _md("""
            ### Loading your own data

            For a real Space Ranger output:

            ```python
            adata, wsi = ov.space.histo.read_visium_with_image(
                visium_path='/path/to/spaceranger/outs',
                image_path='/path/to/full_resolution_HE.tif',
                count_file='filtered_feature_bc_matrix.h5',
            )
            ```

            The helper delegates to scverse-stack readers and `wsidata.open_wsi`
            for you and derives `wsi.properties.mpp` from
            `spot_diameter_fullres` so the downstream backends know the
            physical scale. Predicting on a *different* slide than the
            reference works the same way — just pass that slide's `wsi`
            (after `tile()` + `embed()`) as the first argument while
            keeping `reference=` pointed at the Visium AnnData you
            already have.
        """),
        _md("""
            ## Tile and embed the WSI

            - `tile(wsi, tile_px=224, mpp=0.5)` runs LazySlide's
              `find_tissues` + `tile_tissues`. `tile_px=224` matches
              every pathology FM's input size, and `mpp=0.5` (µm /
              pixel) is the standard "pathology zoom" level — each
              224-pixel patch covers ~112 µm of tissue, roughly twice a
              Visium spot's footprint.
            - `embed(wsi, model='ctranspath', batch_size=16, num_workers=0)`
              extracts per-tile features and writes them as
              `wsi.tables['ctranspath_tiles']` (an AnnData with one row
              per tile and 768 feature columns). The on-disk cache key
              includes slide id, tile key, tile count, and backbone, so
              re-running this cell on the same WSI returns instantly.
        """),
        _code("""
            ov.space.histo.tile(wsi, tile_px=224, mpp=0.5)
            ov.space.histo.embed(wsi, model='ctranspath',
                                 batch_size=16, num_workers=0)
            print('tiles:', len(wsi.shapes['tiles']),
                  '| feature table:', list(wsi.tables))
        """),
        _md("""
            ## Fit a Ridge head on the reference and predict on the query

            `predict_expression(method='hest_fm', …)` does the following
            under the hood:

            1. cut out a 1-tile-per-spot grid on the reference WSI at
               `tile_px = spot_diameter_fullres`,
            2. embed those reference patches with `fm_backbone` (cached
               to `$OV_HISTO_CACHE/ref_features/`),
            3. PCA-project both reference and query embeddings to
               `n_components` dimensions,
            4. fit one `sklearn.linear_model.Ridge` per requested gene on
               the reference, predict on the query tile features,
            5. wrap predictions in an AnnData and store it as
               `wsi.tables['hest_fm_tiles']`.

            ### Key parameters

            - `reference` — paired Visium AnnData (required for
              `hest_fm`).
            - `genes=['EPCAM', …]` — gene panel to predict. Pass
              `None` to predict all of `reference.var_names`.
            - `fm_backbone='ctranspath'` — which pathology FM to extract
              features with. List all options with
              `ov.space.histo.available_backbones()`.
            - `n_components=128` — PCA dimensionality. Smaller =
              faster + more regularised; larger = retain more FM
              signal at the cost of overfitting risk on small
              references.
            - `alpha=1.0` — Ridge regularisation strength. Increase if
              the head overfits (Pearson on held-out spots drops).
            - `head='ridge'` — set to `'mlp'` for a 2-layer GELU MLP
              fitted with AdamW; usually a small gain on dense panels,
              not worth the extra compute on a 5-gene panel.

            ### Pre-staging the patch-encoder weights

            HEST-FM downloads the chosen FM from the LazySlide registry
            on first use. To run **air-gapped** (or to use a checkpoint
            you've validated elsewhere) pass an explicit path:

            ```python
            pred = ov.space.histo.predict_expression(
                wsi, method='hest_fm', reference=adata,
                fm_backbone='ctranspath',
                fm_weight_path='/path/to/ctranspath.pth',  # skips HF download
                hf_token=None,                              # not needed when path is given
                cache_dir='/path/to/scratch/omicverse_histo',
            )
            ```
        """),
        _code("""
            genes = ['EPCAM', 'ERBB2', 'CD68', 'ACTA2', 'VIM']
            pred = ov.space.histo.predict_expression(
                wsi,
                method='hest_fm',
                reference=adata,
                genes=genes,
                fm_backbone='ctranspath',
                n_components=128,
                alpha=1.0,
            )
            pred
        """),
        _md("""
            ## Reading the output

            `pred` is an `AnnData` whose **rows are query tiles** (NOT
            Visium spots) and whose **columns are the requested genes**:

            - `pred.X` (n_tiles × n_genes) — log1p predicted expression,
              `float32`
            - `pred.var_names` — the requested gene symbols
            - `pred.obsm['spatial']` (n_tiles × 2) — tile pixel
              centroids, ready for any spatial plotter
            - `pred.uns['histo']` — run metadata (`method`,
              `fm_backbone`, `n_components`, `alpha`, `head`)
        """),
        _code("""
            print('shape       :', pred.shape)
            print('var_names   :', list(pred.var_names))
            print('coords range:', pred.obsm['spatial'].min(0), '→',
                                   pred.obsm['spatial'].max(0))
            print('metadata    :', pred.uns['histo'])
        """),
        _md("## Visualise predictions on the tissue"),
        _md(
            "Tile-pixel centroids are in `obsm['spatial']`, so any "
            "spatial plotter (`ov.pl.embedding` / `ov.pl.spatial`, "
            "`zs.pl.tiles`) works directly. For high tile counts (3k+) "
            "`ov.pl.embedding` is the fastest path; "
            "`zs.pl.tiles(style='heatmap')` is useful "
            "for publication-quality renders that paint the WSI under "
            "the patches."
        ),
        _code("""
            ov.pl.embedding(pred, basis='spatial',
                            color=['EPCAM', 'ERBB2', 'CD68', 'ACTA2'],
                            cmap='magma', s=12, ncols=2, frameon=False)
        """),
        _md(
            "### Real Visium counts for the same genes\n\n"
            "Render the same four genes from the paired Visium reference "
            "so they can be eyeballed against the predictions above. "
            "The reference is log1p-normalised (`ov.pp.normalize_total` "
            "+ `ov.pp.log1p`) so the colour scale matches the predictor's "
            "output."
        ),
        _code("""
            ref = adata.copy()
            ov.pp.normalize_total(ref, target_sum=1e4)
            ov.pp.log1p(ref)
            ov.pl.embedding(ref, basis='spatial',
                            color=['EPCAM', 'ERBB2', 'CD68', 'ACTA2'],
                            cmap='magma', s=24, ncols=2, frameon=False)
        """),
        _md(
            "### Per-gene scatter on Section 1 (training fit quality)\n\n"
            "The ridge head was trained on Section 1's spots, so this "
            "scatter shows the **best-case fit** — how well the model "
            "can reproduce its own training data. Tile and spot grids "
            "don't coincide, so each Visium spot is matched to its "
            "nearest predicted tile before plotting. Pearson r is "
            "shown in the title; the dashed line is `predicted = true`."
        ),
        _code("""
            import numpy as np, matplotlib.pyplot as plt
            from scipy.spatial import cKDTree
            from scipy.stats import pearsonr

            spot_xy = adata.obsm['spatial']
            tile_xy = pred.obsm['spatial']
            nn = cKDTree(tile_xy).query(spot_xy, k=1)[1]

            ref_X = adata[:, pred.var_names].X
            ref_X = np.log1p(ref_X.toarray() if hasattr(ref_X, 'toarray') else ref_X)
            pred_X = pred.X[nn]

            fig, axes = plt.subplots(1, len(pred.var_names),
                                     figsize=(3 * len(pred.var_names), 3))
            for ax, g, i in zip(axes, pred.var_names, range(len(pred.var_names))):
                ax.scatter(ref_X[:, i], pred_X[:, i], s=4, alpha=0.4)
                r, _ = pearsonr(ref_X[:, i], pred_X[:, i])
                lo = float(min(ref_X[:, i].min(), pred_X[:, i].min()))
                hi = float(max(ref_X[:, i].max(), pred_X[:, i].max()))
                ax.plot([lo, hi], [lo, hi], 'k--', lw=0.8, alpha=0.5)
                ax.set_title(f'{g}: r={r:.2f}')
                ax.set_xlabel('Section 1 real log1p')
                ax.set_ylabel('HEST-FM prediction')
            plt.tight_layout()
        """),
        _md("""
            ## Held-out evaluation on a fresh slide (Section 2)

            The Pearson table above mixes "training data" (the H&E
            patches the ridge head saw) with the comparison spots, so
            it overestimates real-world quality. To get an honest
            number, predict on **Section 2** — the adjacent physical
            section of the same patient block, available from 10x as a
            second Visium dataset. Same anatomy, same staining batch,
            but every H&E pixel is genuinely new to the model.

            `load_breast(section=2)` downloads it (~1.7 GB on first
            use, then cached) and returns the same ``(adata, wsi)``
            shape as Section 1.
        """),
        _code("""
            adata_s2, wsi_s2 = ov.space.histo.load_breast(section=2)
            ov.space.histo.tile(wsi_s2, tile_px=224, mpp=0.5)
            ov.space.histo.embed(wsi_s2, model='ctranspath',
                                 batch_size=16, num_workers=0)
            adata_s2, wsi_s2
        """),
        _md(
            "Predict on Section 2's tiles using the same call shape — "
            "only ``wsi=`` and the reference change."
        ),
        _code("""
            pred_s2 = ov.space.histo.predict_expression(
                wsi_s2,                       # query: Section 2 H&E tiles
                method='hest_fm',
                reference=adata,              # train: Section 1 Visium spots
                genes=genes,                  # same 5-gene panel
                fm_backbone='ctranspath',
                n_components=128, alpha=1.0,
            )
            pred_s2
        """),
        _md(
            "### Spatial visualisation on Section 2 — prediction\n\n"
            "Same `ov.pl.embedding` call as Section 1, just pointed at "
            "the held-out slide's predicted AnnData."
        ),
        _code("""
            ov.pl.embedding(pred_s2, basis='spatial',
                            color=['EPCAM', 'ERBB2', 'CD68', 'ACTA2'],
                            cmap='magma', s=12, ncols=2, frameon=False)
        """),
        _md(
            "### Spatial visualisation on Section 2 — real Visium counts\n\n"
            "Section 2's real Visium expression for the same panel; "
            "compare visually with the predicted maps above. "
            "Log1p-normalised so the colour scale matches the "
            "predictor's output."
        ),
        _code("""
            ref_s2 = adata_s2.copy()
            ov.pp.normalize_total(ref_s2, target_sum=1e4)
            ov.pp.log1p(ref_s2)
            ov.pl.embedding(ref_s2, basis='spatial',
                            color=['EPCAM', 'ERBB2', 'CD68', 'ACTA2'],
                            cmap='magma', s=24, ncols=2, frameon=False)
        """),
        _md(
            "### Per-gene scatter on Section 2 (truly held-out)\n\n"
            "Match each Section 2 Visium spot to its nearest Section 2 "
            "predicted tile, scatter the real log1p expression against "
            "the prediction. Pearson r in the title."
        ),
        _code("""
            import numpy as np, matplotlib.pyplot as plt
            from scipy.spatial import cKDTree
            from scipy.stats import pearsonr

            spot_xy = adata_s2.obsm['spatial']
            tile_xy = pred_s2.obsm['spatial']
            nn = cKDTree(tile_xy).query(spot_xy, k=1)[1]

            ref_X = adata_s2[:, pred_s2.var_names].X
            ref_X = np.log1p(ref_X.toarray() if hasattr(ref_X, 'toarray') else ref_X)
            pred_X = pred_s2.X[nn]

            fig, axes = plt.subplots(1, len(pred_s2.var_names),
                                     figsize=(3 * len(pred_s2.var_names), 3))
            for ax, g, i in zip(axes, pred_s2.var_names, range(len(pred_s2.var_names))):
                ax.scatter(ref_X[:, i], pred_X[:, i], s=4, alpha=0.4)
                r, _ = pearsonr(ref_X[:, i], pred_X[:, i])
                lo = float(min(ref_X[:, i].min(), pred_X[:, i].min()))
                hi = float(max(ref_X[:, i].max(), pred_X[:, i].max()))
                ax.plot([lo, hi], [lo, hi], 'k--', lw=0.8, alpha=0.5)
                ax.set_title(f'{g}: r={r:.2f}')
                ax.set_xlabel('Section 2 real log1p')
                ax.set_ylabel('HEST-FM prediction')
            plt.tight_layout()
        """),
        _md(
            "**Reading the numbers** — per-gene Pearson r ≈ 0.3–0.7 is "
            "typical for the *all-public* CTransPath backbone on a "
            "5-gene panel. Two things noticeably move it up:\n\n"
            "- swap `fm_backbone='uni2'` / `'virchow2'` / "
            "`'gigapath'` (gated, see [model card](https://huggingface.co/MahmoodLab/UNI2-h)) "
            "— typically +5-15% mean r;\n"
            "- bump the panel size (HEST-Bench fits 50 HVG ridges per "
            "slide, which stabilises the alpha pick).\n\n"
            "The dashed diagonal is `predicted = true`; the more the "
            "cloud hugs it, the better."
        ),
        _md("""
            ## Where to go next

            The predicted AnnData is interchangeable with a real Visium
            table, so downstream `ov.space` analyses just work:

            ```python
            ov.space.pySTAGATE(pred, n_domains=8, radius=20)   # spatial domains
            pred = ov.space.svg(pred, mode='prost', n_svgs=200)  # spatially-variable genes
            ov.pl.spatial(pred, color='STAGATE_domain')
            ```

            Compare with the other HE-zoo backends on the same H&E:
            [STPath](t_histo_stpath.ipynb),
            [STFlow](t_histo_stflow.ipynb),
            [iStar](t_histo_istar.ipynb).
        """),
    ]


# ---------------------------------------------------------------------------
# STPath tutorial (zero-shot)
# ---------------------------------------------------------------------------

def stpath_cells() -> list[nbf.NotebookNode]:
    return [
        _md("""
            # STPath — zero-shot generative foundation model

            STPath (Huang et al., *npj Digital Medicine* 2025) is a
            generative foundation model trained on 1,170 paired ST + H&E
            slides covering **17 organs and 38,984 genes**. The published
            weights (HuggingFace [`tlhuang/STPath`](https://huggingface.co/tlhuang/STPath))
            take only GigaPath features and tile centroids as input — no
            reference Visium slide is required, no per-slide
            fine-tuning. On HEST-Bench it leads the next best method by
            **+6.9 % Pearson**.

            This makes STPath the right pick when you have an **H&E-only**
            slide of a tissue covered by its training mixture (any of the
            17 organs × Visium / Visium-HD / Xenium / CosMx) and want
            spot-level expression without doing any per-slide training.
            For organs / panels outside its vocabulary use HEST-FM (with
            a paired reference) or STFlow (per-slide fine-tune).

            **HuggingFace access** — `prov-gigapath/prov-gigapath` (used
            to extract the 1536-d patch features STPath expects) is gated.
            Request access at <https://huggingface.co/prov-gigapath/prov-gigapath>,
            wait for the Microsoft Research approval email, then
            `huggingface-cli login` with a token that includes that
            agreement. Without it the embed cell raises `GatedRepoError`.
        """),
        _md("## Environment"),
        _code("""
            import warnings
            warnings.filterwarnings('ignore')

            import omicverse as ov
            import lazyslide as zs
            ov.utils.ov_plot_set()

            print('omicverse', ov.__version__, '| lazyslide', zs.__version__)
        """),
        _md("""
            ## How the WSI flows through LazySlide

            `ov.space.histo` wraps [LazySlide](https://github.com/RendeiroLab/LazySlide)
            for everything WSI-related. The mapping is:

            | omicverse call | LazySlide / wsidata under the hood |
            |---|---|
            | `ov.space.histo.open_wsi(path)` | `wsidata.open_wsi(path)` → returns `WSIData` (a `SpatialData` subclass) |
            | `ov.space.histo.tile(wsi, …)` | `zs.pp.find_tissues` + `zs.pp.tile_tissues` → `wsi.shapes['tiles']` |
            | `ov.space.histo.embed(wsi, model='gigapath')` | `zs.tl.feature_extraction(model='gigapath')` → `wsi.tables['gigapath_tiles']` (one row per tile, 1536-d features) |
            | `ov.space.histo.predict_expression(wsi, method='stpath')` | omicverse-specific: writes the STPath prediction as `wsi.tables['stpath_tiles']` |

            Drop down to `zs.pp.*` / `zs.tl.*` / `zs.pl.*` whenever you
            need finer control than these convenience wrappers offer.
        """),
        _md("""
            ## Inputs STPath expects

            STPath needs only a tiled WSI; *no Visium reference*. Concretely:

            - **`wsi` — `wsidata.WSIData`** wrapping the H&E.
            - **GigaPath tile features** in `wsi.tables['gigapath_tiles']`
              — produced by `ov.space.histo.embed(wsi, model='gigapath')`.
              GigaPath outputs are 1536-dimensional, matching the
              dimensionality STPath was trained on; substituting other
              backbones is not supported.
            - **organ token** (e.g. `'Breast'`, `'Kidney'`, `'Lung'`,
              `'Colon'`, `'Liver'`, …, one of STPath's 17 organs). Passing
              the wrong organ degrades quality; passing `None` falls back
              to a generic `'Others'` token.
            - **technology token** (`'Visium'`, `'Visium-HD'`, `'Xenium'`,
              `'CosMx'`, …). Defaults to `'Visium'`.

            For a real H&E-only slide:

            ```python
            wsi = ov.space.histo.open_wsi('/path/to/slide.tif')
            ov.space.histo.tile(wsi, tile_px=224, mpp=0.5)
            ov.space.histo.embed(wsi, model='gigapath', batch_size=16)
            ```

            The demo below uses the breast Visium slide for direct
            head-to-head comparison with the other HE-zoo tutorials; the
            Visium counts are not used by STPath, only the H&E.
        """),
        _md("""
            ## Model weights & cache layout

            STPath needs **two pretrained checkpoints + one git
            clone** + the gene vocabulary. Everything below downloads on
            first use; nothing needs manual setup beyond requesting
            GigaPath access on HuggingFace.

            | What | From | To | Size | Gated? |
            |---|---|---|---|---|
            | GigaPath patch encoder (`pytorch_model.bin`) | HF [`prov-gigapath/prov-gigapath`](https://huggingface.co/prov-gigapath/prov-gigapath) | `$HF_HOME/hub/` (default `~/.cache/huggingface/hub`) | ~4 GB | **yes — request access** |
            | STPath model weights (`stfm.pth`) | HF [`tlhuang/STPath`](https://huggingface.co/tlhuang/STPath) | `$OV_HISTO_CACHE/hf/` | ~1 GB | no |
            | STPath python package | git clone `Graph-and-Geometric-Learning/STPath` | `$OV_HISTO_CACHE/STPath/` (added to `sys.path` automatically) | ~100 MB | no |
            | Gene vocabulary (`symbol2ensembl.json`) | shipped inside the STPath clone | `$OV_HISTO_CACHE/STPath/utils_data/` | small | no |
            | tile features (per slide / tile-grid) | computed once | `$OV_HISTO_CACHE/tile_features/gigapath_{slide_stem}_{tile_key}_n{n_tiles}.h5ad` | ~10–50 MB | — |

            `$OV_HISTO_CACHE` defaults to `~/.cache/omicverse/histo`;
            override with `OV_HISTO_CACHE=/some/path` (recommended on
            HPC: point it at scratch). `$HF_HOME` defaults to
            `~/.cache/huggingface`; override with `HF_HOME=/some/path`.

            **Requesting GigaPath access**: visit the model card,
            click "Request access", fill the Microsoft Research data-
            use agreement, wait for approval (usually hours to a few
            days). After approval, on this machine:

            ```bash
            huggingface-cli login   # paste a Read token
            ```

            The `embed(model='gigapath')` call below will then succeed.
            Without access it raises `GatedRepoError`.
        """),
        _md("## Load the demo dataset"),
        _code("""
            adata, wsi = ov.space.histo.load_breast()
            adata
        """),
        _code("""
            wsi
        """),
        _md(
            "Tile the WSI on a 224 px @ 0.5 µm/pixel grid (LazySlide's "
            "`find_tissues` + `tile_tissues` under the hood)."
        ),
        _code("""
            ov.space.histo.tile(wsi, tile_px=224, mpp=0.5)
            print('tiles:', len(wsi.shapes['tiles']))
        """),
        _md("""
            ## Extract GigaPath features (1536-d, gated)

            GigaPath is a 1.1 B-parameter pathology FM (Microsoft Research
            + Providence Health). LazySlide's `feature_extraction` handles
            the gated download and HF auth for us. On first run it
            downloads ~4 GB of weights into `$HF_HOME/hub`; subsequent
            runs use the cache. The resulting features are stored as
            `wsi.tables['gigapath_tiles']` (AnnData with one row per tile
            and 1536 feature columns) and are also cached to
            `$OV_HISTO_CACHE/tile_features/` so notebook re-runs skip
            the embed entirely.
        """),
        _code("""
            ov.space.histo.embed(wsi, model='gigapath',
                                 batch_size=16, num_workers=0)
            wsi.tables['gigapath_tiles']
        """),
        _md("""
            ## Zero-shot prediction

            `predict_expression(method='stpath', …)` does the following
            under the hood:

            1. on first use, auto-clones the upstream STPath repo into
               `$OV_HISTO_CACHE/STPath/` and adds it to `sys.path`,
            2. downloads the model weights (`tlhuang/STPath/stfm.pth`)
               via HuggingFace Hub,
            3. instantiates `STPathInference` (gene vocabulary +
               organ / tech tokenizers + the spatial-transformer
               denoiser),
            4. feeds `(gigapath features, tile centroids, organ id,
               tech id)` through the model in a single forward pass,
            5. wraps the result in an `AnnData` and stores it as
               `wsi.tables['stpath_tiles']`.

            ### Key parameters

            - `organ='Breast'` — STPath's organ-conditioning token. Pick
              one of the 17 organs the model was trained on (`Breast`,
              `Kidney`, `Lung`, `Colon`, `Liver`, …). Wrong organ ⇒
              degraded quality.
            - `tech='Visium'` — sequencing platform token; defaults to
              `'Visium'`. Other choices include `'Visium-HD'`, `'Xenium'`,
              `'CosMx'`.
            - `genes=['EPCAM', 'ERBB2', …]` — gene panel to keep. Passing
              `None` returns all 38,984 genes from STPath's vocabulary
              (`pred.X` becomes a 1426 × 38,984 dense matrix, ~150 MB —
              fine on disk but heavier in memory).
            - `fm_backbone='gigapath'` — must stay `gigapath`; the
              published weights were trained on 1536-d GigaPath features
              specifically.
            - `feature_key=None` — override only if you stored GigaPath
              features under a non-default key.
            - `cache_dir` — override the default
              `$OV_HISTO_CACHE` (where the STPath repo + weights cache).
            - `weight_path` — explicit local path to `stfm.pth` (STPath
              checkpoint). When given, the HuggingFace download of
              `tlhuang/STPath` is skipped.
            - `fm_weight_path` — explicit local path to the GigaPath
              `pytorch_model.bin`. When given, the HuggingFace download
              of `prov-gigapath/prov-gigapath` is skipped (useful when
              the host doesn't have network access to HuggingFace or
              when GigaPath has been pre-staged elsewhere).
            - `hf_token` — explicit HuggingFace token (otherwise reads
              `$HUGGING_FACE_HUB_TOKEN` then
              `~/.cache/huggingface/token`).

            ### Air-gapped run (skip both HuggingFace downloads)

            ```python
            pred = ov.space.histo.predict_expression(
                wsi, method='stpath',
                organ='Breast', tech='Visium',
                genes=['EPCAM', 'ERBB2'],
                fm_weight_path='/scratch/weights/gigapath/pytorch_model.bin',
                weight_path='/scratch/weights/stpath/stfm.pth',
                cache_dir='/scratch/omicverse_histo',
            )
            ```
        """),
        _code("""
            pred = ov.space.histo.predict_expression(
                wsi,
                method='stpath',
                organ='Breast',
                tech='Visium',
                genes=['EPCAM', 'ERBB2', 'CD68', 'ACTA2', 'VIM'],
            )
            pred
        """),
        _md("""
            ## Reading the output

            `pred` is an `AnnData` with:

            - `pred.X` (n_tiles × n_genes) — log1p predicted expression
              (`float32`)
            - `pred.var_names` — the requested gene symbols
            - `pred.obsm['spatial']` (n_tiles × 2) — tile pixel centroids
            - `pred.uns['histo']` — run metadata (`method`,
              `fm_backbone`, `organ`, `tech`)
        """),
        _code("""
            print('shape       :', pred.shape)
            print('var_names   :', list(pred.var_names))
            print('coords range:', pred.obsm['spatial'].min(0), '→',
                                   pred.obsm['spatial'].max(0))
            print('metadata    :', pred.uns['histo'])
        """),
        _md("## Visualise predictions on the tissue"),
        _code("""
            ov.pl.embedding(pred, basis='spatial',
                            color=['EPCAM', 'ERBB2', 'CD68', 'ACTA2'],
                            cmap='magma', s=12, ncols=2, frameon=False)
        """),
        _md(
            "### Real Visium counts for the same genes\n\n"
            "STPath was *not* trained on this slide — it predicts "
            "zero-shot from the H&E. Plotting the real Visium "
            "expression for the same genes gives a qualitative read on "
            "how close the zero-shot output is to ground truth."
        ),
        _code("""
            ref = adata.copy()
            ov.pp.normalize_total(ref, target_sum=1e4)
            ov.pp.log1p(ref)
            ov.pl.embedding(ref, basis='spatial',
                            color=['EPCAM', 'ERBB2', 'CD68', 'ACTA2'],
                            cmap='magma', s=24, ncols=2, frameon=False)
        """),
        _md(
            "### Per-gene scatter on Section 1 (zero-shot quality)\n\n"
            "STPath has never seen this slide during training, so this "
            "scatter already shows held-out generalisation quality. "
            "Match each Visium spot to its nearest predicted tile, "
            "scatter real log1p expression against the prediction, "
            "Pearson r in the title."
        ),
        _code("""
            import numpy as np, matplotlib.pyplot as plt
            from scipy.spatial import cKDTree
            from scipy.stats import pearsonr

            spot_xy = adata.obsm['spatial']
            tile_xy = pred.obsm['spatial']
            nn = cKDTree(tile_xy).query(spot_xy, k=1)[1]

            ref_X = adata[:, pred.var_names].X
            ref_X = np.log1p(ref_X.toarray() if hasattr(ref_X, 'toarray') else ref_X)
            pred_X = pred.X[nn]

            fig, axes = plt.subplots(1, len(pred.var_names),
                                     figsize=(3 * len(pred.var_names), 3))
            for ax, g, i in zip(axes, pred.var_names, range(len(pred.var_names))):
                ax.scatter(ref_X[:, i], pred_X[:, i], s=4, alpha=0.4)
                r, _ = pearsonr(ref_X[:, i], pred_X[:, i])
                lo = float(min(ref_X[:, i].min(), pred_X[:, i].min()))
                hi = float(max(ref_X[:, i].max(), pred_X[:, i].max()))
                ax.plot([lo, hi], [lo, hi], 'k--', lw=0.8, alpha=0.5)
                ax.set_title(f'{g}: r={r:.2f}')
                ax.set_xlabel('Section 1 real log1p')
                ax.set_ylabel('STPath prediction')
            plt.tight_layout()
        """),
        _md("""
            ## Zero-shot prediction on a never-seen slide (Section 2)

            STPath was trained on 1,170 paired slides covering 17
            organs — but **this** slide (and every other Section 1
            we use in HE-zoo) was not in that training set. To
            additionally check generalisation to a brand-new H&E,
            predict on the adjacent **Section 2** of the same patient
            block (separate Visium dataset from 10x).

            `load_breast(section=2)` downloads it on first use
            (~1.7 GB cached) and returns the same `(adata, wsi)`
            shape.
        """),
        _code("""
            adata_s2, wsi_s2 = ov.space.histo.load_breast(section=2)
            ov.space.histo.tile(wsi_s2, tile_px=224, mpp=0.5)
            ov.space.histo.embed(wsi_s2, model='gigapath',
                                 batch_size=16, num_workers=0)
            pred_s2 = ov.space.histo.predict_expression(
                wsi_s2,
                method='stpath',
                organ='Breast', tech='Visium',
                genes=['EPCAM', 'ERBB2', 'CD68', 'ACTA2', 'VIM'],
            )
            pred_s2
        """),
        _md(
            "### Spatial visualisation on Section 2 — prediction\n\n"
            "Same plotter as Section 1, just pointed at the held-out "
            "slide's predicted AnnData."
        ),
        _code("""
            ov.pl.embedding(pred_s2, basis='spatial',
                            color=['EPCAM', 'ERBB2', 'CD68', 'ACTA2'],
                            cmap='magma', s=12, ncols=2, frameon=False)
        """),
        _md(
            "### Spatial visualisation on Section 2 — real Visium counts\n\n"
            "Section 2's real Visium expression for the same panel, "
            "log1p-normalised to match the predictor's output scale."
        ),
        _code("""
            ref_s2 = adata_s2.copy()
            ov.pp.normalize_total(ref_s2, target_sum=1e4)
            ov.pp.log1p(ref_s2)
            ov.pl.embedding(ref_s2, basis='spatial',
                            color=['EPCAM', 'ERBB2', 'CD68', 'ACTA2'],
                            cmap='magma', s=24, ncols=2, frameon=False)
        """),
        _md(
            "### Per-gene scatter on Section 2 (truly zero-shot)\n\n"
            "Match each Section 2 Visium spot to its nearest Section 2 "
            "predicted tile and scatter real log1p expression against "
            "the prediction. Pearson r in the title."
        ),
        _code("""
            import numpy as np, matplotlib.pyplot as plt
            from scipy.spatial import cKDTree
            from scipy.stats import pearsonr

            spot_xy = adata_s2.obsm['spatial']
            tile_xy = pred_s2.obsm['spatial']
            nn = cKDTree(tile_xy).query(spot_xy, k=1)[1]

            ref_X = adata_s2[:, pred_s2.var_names].X
            ref_X = np.log1p(ref_X.toarray() if hasattr(ref_X, 'toarray') else ref_X)
            pred_X = pred_s2.X[nn]

            fig, axes = plt.subplots(1, len(pred_s2.var_names),
                                     figsize=(3 * len(pred_s2.var_names), 3))
            for ax, g, i in zip(axes, pred_s2.var_names, range(len(pred_s2.var_names))):
                ax.scatter(ref_X[:, i], pred_X[:, i], s=4, alpha=0.4)
                r, _ = pearsonr(ref_X[:, i], pred_X[:, i])
                lo = float(min(ref_X[:, i].min(), pred_X[:, i].min()))
                hi = float(max(ref_X[:, i].max(), pred_X[:, i].max()))
                ax.plot([lo, hi], [lo, hi], 'k--', lw=0.8, alpha=0.5)
                ax.set_title(f'{g}: r={r:.2f}')
                ax.set_xlabel('Section 2 real log1p')
                ax.set_ylabel('STPath prediction')
            plt.tight_layout()
        """),
        _md("""
            ## Where to go next

            STPath's output is interchangeable with a real Visium table.
            Feed it straight to `ov.space.pySTAGATE`, `ov.space.svg`, or
            any other spatial analysis. For pixel-level / sub-spot
            resolution on the same H&E, switch to
            [iStar](t_histo_istar.ipynb) (requires the matched Visium
            counts as a reference). For benchmarking against a Ridge
            baseline on the same panel, see
            [HEST-FM](t_histo_hest_fm.ipynb).
        """),
    ]


# ---------------------------------------------------------------------------
# STFlow tutorial (per-slide fine-tune)
# ---------------------------------------------------------------------------

def stflow_cells() -> list[nbf.NotebookNode]:
    return [
        _md("""
            # STFlow — per-slide flow-matching denoiser

            STFlow (Huang et al., *ICML 2025* Spotlight) models the
            **joint distribution** of gene expression across an entire
            slide with a spatial transformer + flow-matching denoiser.
            The training set is the user's own paired Visium reference;
            the trained denoiser then runs reverse-time ODE integration
            on the query tiles' features + coordinates to sample
            cohesive whole-slide expression patterns.

            Upstream ships training scripts only — there is no released
            zero-shot checkpoint. (The same group's productionised
            successor, **STPath**, is the zero-shot path; see the
            [STPath tutorial](t_histo_stpath.ipynb).) This wrapper
            therefore runs the canonical fit-on-your-reference,
            predict-on-your-query workflow on a single GPU in 5–10 min.

            **When to pick STFlow over the alternatives**

            | Goal | Use |
            |---|---|
            | Zero-shot prediction on H&E only | `stpath` |
            | Per-slide fine-tune with paired Visium reference, **joint cross-spot modelling** | `stflow` — this notebook |
            | Per-slide fine-tune with paired Visium reference, fast linear baseline | `hest_fm` |
            | Sub-spot super-resolution on paired Visium+H&E | `istar` |
        """),
        _md("## Environment"),
        _code("""
            import warnings
            warnings.filterwarnings('ignore')

            import omicverse as ov
            import lazyslide as zs
            ov.utils.ov_plot_set()

            print('omicverse', ov.__version__, '| lazyslide', zs.__version__)
        """),
        _md("""
            ## How the WSI flows through LazySlide

            `ov.space.histo` wraps [LazySlide](https://github.com/RendeiroLab/LazySlide)
            for tiling, FM embedding, and the `WSIData` container.
            STFlow only adds the flow-matching denoiser on top:

            | omicverse call | LazySlide / wsidata under the hood |
            |---|---|
            | `ov.space.histo.open_wsi(path)` / `read_visium_with_image` | `wsidata.open_wsi` → `WSIData` (a `SpatialData` subclass) |
            | `ov.space.histo.tile(wsi, …)` | `zs.pp.find_tissues` + `zs.pp.tile_tissues` → `wsi.shapes['tiles']` |
            | `ov.space.histo.embed(wsi, model='ctranspath')` | `zs.tl.feature_extraction(model='ctranspath')` → `wsi.tables['ctranspath_tiles']` |
            | `ov.space.histo.predict_expression(wsi, method='stflow', reference=…)` | omicverse-specific: trains the STFlow denoiser on a tile-grid cut from the reference, runs reverse-time ODE on query tile features, writes `wsi.tables['stflow_tiles']` |
        """),
        _md("""
            ## Inputs STFlow expects

            Same shape as HEST-FM — STFlow trains on the reference
            slide and predicts on the query tiles:

            - **`reference` — paired Visium AnnData** with `.X`,
              `.obsm['spatial']`, and
              `uns['spatial'][lib]['scalefactors']['spot_diameter_fullres']`.
            - **`wsi` — `wsidata.WSIData`** wrapping the H&E. The
              query tiles are whatever you've added via
              `ov.space.histo.tile()`; the reference patches are cut
              out one-per-spot on the same WSI.
            - **FM features** for both reference and query tiles, in
              `wsi.tables['{fm_backbone}_tiles']`. STFlow accepts any
              backbone (768-d CTransPath, 1280-d Virchow2, 1536-d
              GigaPath / UNI2, …) — feature dimensionality is read
              from the table; only consistency between reference and
              query matters.

            For your own data:

            ```python
            adata, wsi = ov.space.histo.read_visium_with_image(
                visium_path='/path/to/spaceranger/outs',
                image_path='/path/to/HE.tif',
            )
            ```
        """),
        _md("""
            ## Model weights & cache layout

            STFlow has **no released pretrained checkpoint** (the
            authors productionised that path as STPath). It is
            trained from scratch on the user's paired reference slide
            every run. The only thing downloaded is the patch encoder.

            | What | From | To | Size | Gated? |
            |---|---|---|---|---|
            | `ctranspath` patch encoder (default) | LazySlide model registry → HF `RendeiroLab/LazySlide-models-gpl` | `$HF_HOME/hub/` (default `~/.cache/huggingface/hub`) | ~100 MB | no |
            | STFlow python package | git clone `Graph-and-Geometric-Learning/STFlow` | `$OV_HISTO_CACHE/STFlow/` (added to `sys.path` automatically) | ~80 MB | no |
            | reference / query tile features | computed once | `$OV_HISTO_CACHE/ref_features/` and `$OV_HISTO_CACHE/tile_features/` | ~10–50 MB each | — |
            | per-slide denoiser weights | trained each run | in-memory, not persisted | — | — |

            `$OV_HISTO_CACHE` defaults to `~/.cache/omicverse/histo`;
            override with `OV_HISTO_CACHE=/some/path` (recommended on
            HPC: point it at scratch). `$HF_HOME` defaults to
            `~/.cache/huggingface`; override with `HF_HOME=/some/path`.

            On first import omicverse also applies a tiny patch to
            upstream `stflow/model/transformer.py` (the upstream
            `GeneUpdate.__init__` doesn't accept a `non_negative=`
            kwarg that the caller passes — a known upstream bug). This
            keeps subsequent re-clones idempotent.

            **Swapping to a gated backbone** — set
            `fm_backbone='uni2'` / `'gigapath'` / `'virchow2'` once
            you have HuggingFace access. Quality usually improves;
            training time is unchanged.
        """),
        _md("## Load the demo dataset and tile / embed"),
        _md(
            "This tutorial uses **CTransPath** (768-d, all-public) so it "
            "runs without HuggingFace gating. Swap in `'gigapath'`, "
            "`'uni2'`, or `'virchow2'` for higher accuracy once you have "
            "access."
        ),
        _code("""
            adata, wsi = ov.space.histo.load_breast()
            adata
        """),
        _code("""
            wsi
        """),
        _md(
            "Tile the WSI and extract per-tile CTransPath features. "
            "Cached on disk under `$OV_HISTO_CACHE/tile_features/` so "
            "re-runs return instantly."
        ),
        _code("""
            ov.space.histo.tile(wsi, tile_px=224, mpp=0.5)
            ov.space.histo.embed(wsi, model='ctranspath',
                                 batch_size=16, num_workers=0)
            print('tiles:', len(wsi.shapes['tiles']),
                  '| feature table:', list(wsi.tables))
        """),
        _md("""
            ## Train STFlow on the reference, predict on the query

            `predict_expression(method='stflow', …)` does the following:

            1. on first use, auto-clones the upstream STFlow repo into
               `$OV_HISTO_CACHE/STFlow/` and adds it to `sys.path`,
            2. picks `n_top_genes` HVGs on the reference (or uses the
               panel you pass via `genes=`),
            3. builds a small spatial-transformer denoiser, sized by
               `n_layers` / `hidden_dim` / `n_neighbors`,
            4. trains it for `n_epochs` iterations with AdamW on the
               reference (one forward pass = the whole slide; very
               cheap per epoch),
            5. runs `n_sample_steps` Euler integration steps of the
               reverse-time ODE on the **query** tiles to draw a sample
               from the conditional distribution `p(expression | image,
               coords)`,
            6. wraps predictions as `wsi.tables['stflow_tiles']`.

            ### Key parameters

            - `reference` — paired Visium AnnData (required).
            - `fm_backbone='ctranspath'` — any registered pathology FM.
            - `genes=None` — explicit panel; defaults to top-500 HVGs.
            - `n_epochs=80` — training iterations. The paper trains for
              thousands of epochs over a multi-slide cohort; 80 is a
              practical demo budget that still gives meaningful
              predictions.
            - `n_layers=4` — depth of the spatial transformer denoiser.
            - `n_neighbors=8` — number of spatial neighbours each tile
              attends to.
            - `n_sample_steps=5` — Euler steps for the reverse-time
              ODE (paper default).
            - `hidden_dim=256`, `batch_size=1` — denoiser sizing.

            **Gene panel size is fixed at 50** — STFlow's upstream
            transformer (`stflow/model/transformer.py:63`) hardcodes a
            `+50` term in the attention-MLP input dim, so the panel
            must be exactly 50 genes. Leave `genes=None` to use the
            top-50 HVGs from the reference, or pass an explicit
            50-gene list.

            ### Pre-staging the patch-encoder weights

            STFlow has no released checkpoint of its own (it trains
            per-slide); the only thing downloaded is the patch encoder
            you choose via `fm_backbone`. To run **air-gapped** or with
            a vetted local checkpoint:

            ```python
            pred = ov.space.histo.predict_expression(
                wsi, method='stflow', reference=adata,
                fm_backbone='ctranspath',
                fm_weight_path='/scratch/weights/ctranspath.pth',
                cache_dir='/scratch/omicverse_histo',
            )
            ```

            **Compute** — at the default settings the cell below takes
            roughly 5–10 min on an H100; most of the time is the
            ctranspath embed of the reference spot grid (cached for
            re-runs).
        """),
        _code("""
            pred = ov.space.histo.predict_expression(
                wsi,
                method='stflow',
                reference=adata,
                fm_backbone='ctranspath',
                n_epochs=80,
                n_layers=4,
                n_neighbors=8,
                n_sample_steps=5,
            )
            pred
        """),
        _md("""
            ## Reading the output

            `pred` is an `AnnData` whose rows are query tiles and whose
            columns are the predicted gene panel:

            - `pred.X` (n_tiles × n_genes) — log1p predicted expression
            - `pred.var_names` — gene symbols (the 500-HVG panel by
              default, or whatever you passed in `genes=`)
            - `pred.obsm['spatial']` — tile pixel centroids
            - `pred.uns['histo']` — run metadata (`method`,
              `fm_backbone`, `n_epochs`, `n_layers`, `n_sample_steps`).
        """),
        _code("""
            print('shape       :', pred.shape)
            print('first 5 vars:', list(pred.var_names[:5]))
            print('coords range:', pred.obsm['spatial'].min(0), '→',
                                   pred.obsm['spatial'].max(0))
            print('metadata    :', pred.uns['histo'])
        """),
        _md("## Visualise"),
        _code("""
            ov.pl.embedding(pred, basis='spatial',
                            color=list(pred.var_names[:4]),
                            cmap='magma', s=12, ncols=2, frameon=False)
        """),
        _md(
            "### Real Visium counts for the same genes\n\n"
            "Plot the same four predicted genes from the paired Visium "
            "reference. The reference is log1p-normalised so the colour "
            "scale lines up with the STFlow output."
        ),
        _code("""
            ref = adata.copy()
            ov.pp.normalize_total(ref, target_sum=1e4)
            ov.pp.log1p(ref)
            ov.pl.embedding(ref, basis='spatial',
                            color=list(pred.var_names[:4]),
                            cmap='magma', s=24, ncols=2, frameon=False)
        """),
        _md(
            "### Per-gene scatter on Section 1 (training fit quality)\n\n"
            "The Denoiser was trained on Section 1's spots, so this "
            "scatter is the best-case fit. Match each Visium spot to "
            "its nearest predicted tile and scatter the real log1p "
            "expression against the prediction. Pearson r in the title."
        ),
        _code("""
            import numpy as np, matplotlib.pyplot as plt
            from scipy.spatial import cKDTree
            from scipy.stats import pearsonr

            spot_xy = adata.obsm['spatial']
            tile_xy = pred.obsm['spatial']
            nn = cKDTree(tile_xy).query(spot_xy, k=1)[1]

            picks = list(pred.var_names[:5])
            ref_X = adata[:, picks].X
            ref_X = np.log1p(ref_X.toarray() if hasattr(ref_X, 'toarray') else ref_X)
            pred_X = pred[:, picks].X[nn]

            fig, axes = plt.subplots(1, len(picks), figsize=(3 * len(picks), 3))
            for ax, g, i in zip(axes, picks, range(len(picks))):
                ax.scatter(ref_X[:, i], pred_X[:, i], s=4, alpha=0.4)
                r, _ = pearsonr(ref_X[:, i], pred_X[:, i])
                lo = float(min(ref_X[:, i].min(), pred_X[:, i].min()))
                hi = float(max(ref_X[:, i].max(), pred_X[:, i].max()))
                ax.plot([lo, hi], [lo, hi], 'k--', lw=0.8, alpha=0.5)
                ax.set_title(f'{g}: r={r:.2f}')
                ax.set_xlabel('Section 1 real log1p')
                ax.set_ylabel('STFlow prediction')
            plt.tight_layout()
        """),
        _md("""
            ## Held-out evaluation on a fresh slide (Section 2)

            The STFlow Denoiser above was trained on Section 1's
            spots and predicts on Section 1's tiles — its training
            and query domains overlap, which inflates apparent
            quality. To get an honest read, predict on **Section 2**:
            the adjacent physical section of the same patient block
            (separate Visium dataset from 10x). Same anatomy and
            staining batch, but every H&E pixel is new to the trained
            head.

            `load_breast(section=2)` downloads it on first use
            (~1.7 GB cached). Note: STFlow's per-slide head has to be
            **re-trained** for the new slide, because the architecture
            references each slide's local spot graph during training —
            we just keep using the same `predict_expression(method=
            'stflow', reference=adata, ...)` call but point `wsi=` at
            Section 2 and `reference=` at Section 1's spots that we
            still want to learn from.
        """),
        _code("""
            adata_s2, wsi_s2 = ov.space.histo.load_breast(section=2)
            ov.space.histo.tile(wsi_s2, tile_px=224, mpp=0.5)
            ov.space.histo.embed(wsi_s2, model='ctranspath',
                                 batch_size=16, num_workers=0)
            pred_s2 = ov.space.histo.predict_expression(
                wsi_s2,                       # query: Section 2 H&E tiles
                method='stflow',
                reference=adata,              # train: Section 1 Visium spots
                fm_backbone='ctranspath',
                n_epochs=80, n_layers=4, n_sample_steps=5,
            )
            pred_s2
        """),
        _md(
            "### Spatial visualisation on Section 2 — prediction\n\n"
            "Same plotter as Section 1, pointed at the held-out slide's "
            "predicted AnnData."
        ),
        _code("""
            ov.pl.embedding(pred_s2, basis='spatial',
                            color=list(pred_s2.var_names[:4]),
                            cmap='magma', s=12, ncols=2, frameon=False)
        """),
        _md(
            "### Spatial visualisation on Section 2 — real Visium counts\n\n"
            "Section 2's real Visium expression for the same panel, "
            "log1p-normalised."
        ),
        _code("""
            ref_s2 = adata_s2.copy()
            ov.pp.normalize_total(ref_s2, target_sum=1e4)
            ov.pp.log1p(ref_s2)
            ov.pl.embedding(ref_s2, basis='spatial',
                            color=list(pred_s2.var_names[:4]),
                            cmap='magma', s=24, ncols=2, frameon=False)
        """),
        _md(
            "### Per-gene scatter on Section 2 (held-out)\n\n"
            "Match each Section 2 Visium spot to its nearest Section 2 "
            "predicted tile and scatter the real log1p expression "
            "against the prediction. Pearson r in the title."
        ),
        _code("""
            import numpy as np, matplotlib.pyplot as plt
            from scipy.spatial import cKDTree
            from scipy.stats import pearsonr

            spot_xy = adata_s2.obsm['spatial']
            tile_xy = pred_s2.obsm['spatial']
            nn = cKDTree(tile_xy).query(spot_xy, k=1)[1]

            picks = list(pred_s2.var_names[:5])
            ref_X = adata_s2[:, picks].X
            ref_X = np.log1p(ref_X.toarray() if hasattr(ref_X, 'toarray') else ref_X)
            pred_X = pred_s2[:, picks].X[nn]

            fig, axes = plt.subplots(1, len(picks), figsize=(3 * len(picks), 3))
            for ax, g, i in zip(axes, picks, range(len(picks))):
                ax.scatter(ref_X[:, i], pred_X[:, i], s=4, alpha=0.4)
                r, _ = pearsonr(ref_X[:, i], pred_X[:, i])
                lo = float(min(ref_X[:, i].min(), pred_X[:, i].min()))
                hi = float(max(ref_X[:, i].max(), pred_X[:, i].max()))
                ax.plot([lo, hi], [lo, hi], 'k--', lw=0.8, alpha=0.5)
                ax.set_title(f'{g}: r={r:.2f}')
                ax.set_xlabel('Section 2 real log1p')
                ax.set_ylabel('STFlow prediction')
            plt.tight_layout()
        """),
        _md("""
            ## Where to go next

            Just like the other HE-zoo backends, the predicted AnnData
            slots straight into `ov.space.pySTAGATE`, `ov.space.svg`,
            and friends. For a head-to-head on the same H&E, see
            [STPath](t_histo_stpath.ipynb),
            [HEST-FM](t_histo_hest_fm.ipynb), and
            [iStar](t_histo_istar.ipynb).
        """),
    ]


# ---------------------------------------------------------------------------
# iStar tutorial (super-resolution)
# ---------------------------------------------------------------------------

def istar_cells() -> list[nbf.NotebookNode]:
    return [
        _md("""
            # iStar — super-resolve a paired Visium + H&E sample

            iStar (Zhang et al., *Nature Biotechnology* 2024) imputes
            gene expression at **near-single-cell** resolution by combining
            the spot-level Visium counts you already have with the full
            morphological detail in the underlying H&E image. The output
            is a dense pixel-level grid (~8 µm/pixel by default) — much
            finer than Visium's 55 µm spots — that you can cluster, cell-
            type, or feed into downstream `ov.space` analysis just like
            any other spatial AnnData.

            **When to reach for iStar vs the spot-level backends**

            | Goal | Use |
            |---|---|
            | Predict expression on a tissue section that has **only H&E** (no Visium) | `predict_expression(method='stpath' / 'stflow' / 'hest_fm')` |
            | You already have **Visium + matched H&E** and want sub-spot resolution | `super_resolve(method='istar')` — this notebook |
            | Same as above but only need spot-level predictions on the same slide | any of the spot-level methods will also work |

            **Conceptually** iStar is a self-supervised refinement: it
            trains a per-slide regression head from HIPT (Hierarchical
            Image Pyramid Transformer, mahmoodlab) features → log1p
            spot expression on *this slide's* paired ST data, then runs
            that head on every sub-spot patch in the tissue mask.
            Re-training on every slide means iStar adapts to staining /
            tissue idiosyncrasies that out-of-the-box zero-shot models
            cannot.

            > **iStar is NOT a zero-shot model.** It cannot predict
            > gene expression from H&E alone — the per-slide regression
            > head trains on the paired Visium counts you pass as
            > `adata`. Super-resolution then extrapolates that fit to
            > sub-spot pixels on the *same* slide. If your slide has
            > **only H&E** (no Visium), use
            > `ov.space.histo.predict_expression(wsi, method='stpath',
            > organ=...)` instead — STPath is a true zero-shot
            > foundation model.

            **Licence** — iStar's vendored source lives at
            `omicverse.external.istar` and is GPL-3.0; commercial users
            should contact the upstream authors (see
            `omicverse/external/istar/NOTICE.md`).
        """),
        _md("## Environment"),
        _code("""
            import warnings
            warnings.filterwarnings('ignore')

            import omicverse as ov
            import lazyslide as zs
            ov.utils.ov_plot_set()

            print('omicverse', ov.__version__, '| lazyslide', zs.__version__)
        """),
        _md("""
            ## Inputs iStar expects

            iStar needs three things bound together: spot counts, spot
            pixel coordinates in the H&E reference frame, and the full-
            resolution H&E image itself. In the omicverse pipeline these
            live in two objects:

            - **`adata` — AnnData (Visium spot counts)**
              - `adata.X` (n_spots × n_genes) — raw counts
              - `adata.obsm['spatial']` (n_spots × 2) — *full-resolution
                pixel* (x, y) of each spot centre, in the same coordinate
                system as the H&E image
              - `adata.uns['spatial'][library_id]['scalefactors']` —
                Space Ranger's JSON, in particular
                `spot_diameter_fullres` (the spot diameter in
                full-resolution pixels) which iStar reads to set the
                physical scale
            - **`wsi` — `wsidata.WSIData` (whole slide image)**
              - `wsi.reader.file` — the underlying `.tif` / `.svs` path
              - `wsi.properties.shape` — (height, width) in pixels at
                level 0
              - `wsi.properties.mpp` — microns per pixel (Visium FFPE
                images typically don't embed this; the omicverse loader
                derives it from `spot_diameter_fullres = 55 µm / mpp`
                and writes it back via `wsi.set_mpp`).

            Both objects are returned together by the convenience loader
            below; the next section shows how to assemble them yourself.
        """),
        _md("""
            ## How the WSI flows through LazySlide

            iStar trains its own per-slide regression head, so it does
            NOT need a pathology FM-embedding pass through LazySlide
            the way the spot-level backends do. What it still uses
            from LazySlide is the WSI container itself:

            | omicverse call | LazySlide / wsidata under the hood |
            |---|---|
            | `ov.space.histo.open_wsi(path)` / `read_visium_with_image` | `wsidata.open_wsi(path)` → returns `WSIData` (a `SpatialData` subclass) wrapping the slide reader (openslide / tiffslide / bioformats) + a thumbnail |
            | `wsi.read_region(x, y, w, h, level=…)` | the iStar wrapper uses this internally to extract patches around each Visium spot before handing them to HIPT |
            | `ov.space.histo.super_resolve(adata, wsi=wsi, method='istar')` | omicverse-specific: stages inputs, trains the iStar head, returns the sub-spot AnnData |

            For iStar specifically there is no `embed(model=…)` step —
            HIPT feature extraction is part of the iStar pipeline and
            uses iStar's own checkpoints, not the LazySlide model
            registry. Tiling (`ov.space.histo.tile(…)`) is also
            optional for the iStar path; the wrapper builds its own
            spot-aligned patch grid from `adata.obsm['spatial']` +
            `spot_diameter_fullres`.
        """),
        _md("""
            ## Model weights & cache layout

            iStar wraps two pretrained HIPT vision-transformer
            checkpoints and trains the regression head from scratch on
            each slide.

            | What | From | To | Size | Gated? |
            |---|---|---|---|---|
            | HIPT-256 (`vit256_small_dino.pth`) | mahmoodlab/HIPT GitHub LFS mirror | `$OV_HISTO_CACHE/istar_checkpoints/` (symlinked into `omicverse/external/istar/checkpoints/`) | ~672 MB | no |
            | HIPT-4K (`vit4k_xs_dino.pth`) | mahmoodlab/HIPT GitHub LFS mirror | `$OV_HISTO_CACHE/istar_checkpoints/` (symlinked) | ~378 MB | no |
            | iStar Python source | vendored in `omicverse/external/istar/` | shipped with omicverse | ~600 KB | — |
            | per-slide super-resolution outputs | written by iStar | `$OV_HISTO_CACHE/istar_runs/{slide_stem}/cnts-super/{gene}.pickle` | ~10 MB / 50 genes | — |
            | per-slide regression head weights | trained each run | `$OV_HISTO_CACHE/istar_runs/{slide_stem}/states/` | ~50 MB | — |

            `$OV_HISTO_CACHE` defaults to `~/.cache/omicverse/histo`;
            override with `OV_HISTO_CACHE=/some/path` (recommended on
            HPC: point it at scratch).

            Subsequent calls with the same `(slide, gene panel)` hit
            the on-disk pickle cache and skip re-training entirely.
        """),
        _md("## Load the demo dataset"),
        _md(
            "`ov.space.histo.load_breast()` downloads and caches the 10x "
            "Visium Breast Cancer Block A Section 1 sample (3,798 spots, "
            "36,601 genes, 1.7 GB H&E) under "
            "`$OV_HISTO_CACHE/he_zoo/visium_breast` and returns the same "
            "`(adata, wsi)` pair you would build by hand on a real dataset."
        ),
        _code("""
            adata, wsi = ov.space.histo.load_breast()
            adata
        """),
        _code("""
            wsi
        """),
        _md("""
            ## Loading your own data

            For your own Space Ranger output, use the lower-level helper
            instead of `load_breast`:

            ```python
            adata, wsi = ov.space.histo.read_visium_with_image(
                visium_path='/path/to/spaceranger/outs',  # contains filtered_feature_bc_matrix.h5 + spatial/
                image_path='/path/to/full_resolution_HE.tif',
                count_file='filtered_feature_bc_matrix.h5',
                library_id=None,           # auto-inferred from spatial/
            )
            ```

            Internally this delegates to scverse readers to get the spot
            counts + spatial metadata, then `wsidata.open_wsi` to wrap
            the H&E. It also auto-derives `wsi.properties.mpp` from
            `spot_diameter_fullres` (Visium spots are 55 µm by design)
            and writes the WSI path into `adata.uns['histo']['wsi_path']`
            so the iStar backend can recover it later without you
            re-passing it.

            For non-Visium spatial transcriptomics (Stereo-seq, Slide-seq,
            Visium HD, …) you can build `(adata, wsi)` manually: any
            AnnData with `.X`, `.obsm['spatial']`, and an
            `uns['spatial'][lib]['scalefactors']['spot_diameter_fullres']`
            entry works as the `adata` argument; the `wsi` is just
            whatever `wsidata.open_wsi('path.tif')` returns. The
            spatial coordinates must be in the same pixel frame as the
            H&E (Space Ranger guarantees this; for other platforms you
            may need an affine registration step first).
        """),
        _md("""
            ## Run iStar end-to-end

            One call performs the entire pipeline:

            1. **stage inputs** into the on-disk format iStar's scripts
               expect (`cnts.tsv`, `locs-raw.tsv`, `he-raw.jpg`,
               `pixel-size-raw.txt`, `radius-raw.txt`),
            2. **rescale** image + locations to `pixel_size` µm/pixel,
            3. **extract HIPT features** (downloads the mahmoodlab/HIPT
               `vit256_small_dino.pth` + `vit4k_xs_dino.pth` checkpoints
               into `$OV_HISTO_CACHE/istar_checkpoints/` on first use),
            4. **detect tissue mask** from those features,
            5. **select genes** to impute (HVGs by default, or whatever
               you pass via `genes=`),
            6. **train** the per-slide regression head for `epochs`
               iterations,
            7. **impute** sub-spot expression and **read it back** as an
               AnnData where rows are in-tissue pixels and columns are
               genes.

            Subsequent calls with the same `(adata, wsi)` and the same
            gene panel hit the on-disk pickle cache and return in seconds.

            ### Key parameters

            - `pixel_size=0.5` — output grid resolution in µm/pixel
              (default `0.5`, matches the paper; halve for finer grids,
              double for coarser/faster).
            - `n_top_genes=50` — number of highly-variable genes to
              impute when `genes=` is not given. The demo uses 50 to
              keep the per-slide training tractable; the paper uses
              `n_top_genes=1000`.
            - `genes=['EPCAM', 'ERBB2', …]` — explicit gene panel; takes
              precedence over `n_top_genes` and is written to
              `gene-names.txt` for iStar.
            - `epochs=80` — training iterations for the per-slide head.
              The paper default is `400`; `80` gives a quick demo with
              already-reasonable quality. Time scales ~linearly with
              `epochs`.
            - `device='cuda'` — defaults to CUDA when available, else CPU.
            - `cache_dir=None` — override the default
              `$OV_HISTO_CACHE/istar_runs/<slide_stem>/` working
              directory.
            - `hipt256_path`, `hipt4k_path` — explicit local paths to the
              HIPT-256 / HIPT-4K weight files. When given, the
              mahmoodlab/HIPT LFS download is skipped (useful when the
              host doesn't have GitHub network access or when the HIPT
              checkpoints have been pre-staged elsewhere).

            ### Air-gapped run (HIPT checkpoints already staged)

            ```python
            pred = ov.space.histo.super_resolve(
                adata, wsi=wsi, method='istar',
                pixel_size=0.5, n_top_genes=50, epochs=80,
                hipt256_path='/scratch/weights/HIPT/vit256_small_dino.pth',
                hipt4k_path='/scratch/weights/HIPT/vit4k_xs_dino.pth',
                cache_dir='/scratch/omicverse_histo',
            )
            ```
        """),
        _code("""
            pred = ov.space.histo.super_resolve(
                adata,
                wsi=wsi,
                method='istar',
                pixel_size=0.5,    # 0.5 µm / pixel ⇒ ~8 µm sub-spot grid
                n_top_genes=50,
                epochs=80,
            )
            pred
        """),
        _md("""
            ## Reading the output

            `pred` is an `AnnData` whose rows are **in-tissue pixels** on
            the super-resolution grid and whose columns are the imputed
            genes:

            - `pred.X` (n_pixels × n_genes) — log1p imputed expression,
              `float32`
            - `pred.obs` carries pixel coordinates as `x` / `y` columns,
              with row names of the form `'px_<y>_<x>'`
            - `pred.var_names` — gene symbols (same order as
              `gene-names.txt`)
            - `pred.obsm['spatial']` (n_pixels × 2) — same `(x, y)` pixel
              positions, ready for any spatial plotter
            - `pred.uns['histo']` — run metadata (`method`, `pixel_size`,
              `factor`, `work_dir`).

            Compared with the input Visium AnnData (3,798 spots) the
            output covers far more locations (here 392,830 sub-spot
            pixels inside the tissue mask), which is what makes
            cell-type pixel annotation and high-resolution clustering
            possible downstream.
        """),
        _code("""
            print('input  Visium :', adata.shape)
            print('output sub-spot:', pred.shape)
            print('coords range  :', pred.obsm['spatial'].min(0), '→',
                                     pred.obsm['spatial'].max(0))
            print('metadata      :', pred.uns['histo'])
        """),
        _md("## Visualise sub-spot expression"),
        _md(
            "Because `pred` carries pixel coordinates in `obsm['spatial']`, "
            "any spatial plotter (`ov.pl.embedding`, `ov.pl.spatial`, "
            "`zs.pl.tiles`) renders it without extra bookkeeping. The "
            "small dot size (`s=1`) is appropriate because the grid is "
            "very dense."
        ),
        _code("""
            ov.pl.embedding(pred, basis='spatial',
                            color=list(pred.var_names[:4]),
                            cmap='magma', s=1, ncols=2, frameon=False)
        """),
        _md(
            "### Real Visium counts for the same genes\n\n"
            "Render the same four imputed genes from the paired Visium "
            "reference so the sub-spot imputation can be eyeballed "
            "against the spot-level ground truth. The reference is "
            "log1p-normalised to match iStar's output scale."
        ),
        _code("""
            ref = adata.copy()
            ov.pp.normalize_total(ref, target_sum=1e4)
            ov.pp.log1p(ref)
            ov.pl.embedding(ref, basis='spatial',
                            color=list(pred.var_names[:4]),
                            cmap='magma', s=24, ncols=2, frameon=False)
        """),
        _md("""
            ## Where to go next

            The output AnnData feeds the rest of `ov.space` directly:

            ```python
            # spatial domain detection on the sub-spot grid
            ov.space.pySTAGATE(pred, n_domains=8, radius=20)

            # spatially-variable genes
            pred = ov.space.svg(pred, mode='prost', n_svgs=200)

            # marker enrichment for cell-type calling
            ov.single.cosg(pred, groupby='STAGATE_domain')
            ```

            For a head-to-head comparison with the spot-level backends
            on the same H&E, see the sibling tutorials
            ([STPath](t_histo_stpath.ipynb),
            [STFlow](t_histo_stflow.ipynb),
            [HEST-FM](t_histo_hest_fm.ipynb)).
        """),
    ]


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    table = {
        "hest_fm": (hest_fm_cells, 7200),
        "stpath":  (stpath_cells, 7200),
        "stflow":  (stflow_cells, 7200),
        "istar":   (istar_cells, 14400),
    }
    if target == "all":
        for name, (fn, t) in table.items():
            _build_and_run(name, fn(), timeout=t)
    elif target in table:
        fn, t = table[target]
        _build_and_run(target, fn(), timeout=t)
    else:
        print(f"unknown target: {target!r}; choose one of {list(table) + ['all']}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
