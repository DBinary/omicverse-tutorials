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

            The HEST benchmark (Jaume et al., *NeurIPS 2024 Spotlight*) showed that a
            pathology foundation model (UNI, CONCH, Virchow2, GigaPath, CTransPath…)
            followed by a Ridge linear head matches or beats much heavier
            end-to-end neural architectures on spot-level gene-expression
            prediction. `ov.space.histo.predict_expression(method='hest_fm')`
            implements exactly that recipe inside the LazySlide / WSIData pipeline:

            1. tile the H&E into 224 px patches (one per Visium spot's footprint),
            2. embed each tile with a pathology FM,
            3. fit `sklearn.linear_model.Ridge` per gene on the reference Visium spots
               (PCA-compressed FM features → log-expression),
            4. predict on the query tiles.

            This notebook uses the all-public **CTransPath** backbone so it runs
            without any HuggingFace gating. For better accuracy, swap in
            `fm_backbone='uni2'`, `'conch_v1.5'`, or `'gigapath'` once you have
            access.
        """),
        _md("## Environment & demo data"),
        _code("""
            import warnings, os
            warnings.filterwarnings('ignore')

            import omicverse as ov
            import lazyslide as zs
            import scanpy as sc

            ov.utils.ov_plot_set()
            print('omicverse', ov.__version__, '| lazyslide', zs.__version__)
        """),
        _md(
            "`ov.space.histo.load_breast` caches the 10x Visium Breast Cancer Block A "
            "Section 1 sample under `$OV_HISTO_CACHE/he_zoo/visium_breast` (~1.7 GB, "
            "downloaded once)."
        ),
        _code("""
            adata, wsi = ov.space.histo.load_breast()
            adata, wsi
        """),
        _md("## Tile and embed"),
        _code("""
            ov.space.histo.tile(wsi, tile_px=224, mpp=0.5)
            ov.space.histo.embed(wsi, model='ctranspath', batch_size=16, num_workers=0)
            print('tiles:', len(wsi.shapes['tiles']),
                  '| feature table:', list(wsi.tables))
        """),
        _md("## Fit a per-gene Ridge head on the reference, predict on the WSI tiles"),
        _code("""
            genes = ['EPCAM', 'ERBB2', 'CD68', 'ACTA2', 'VIM']
            pred = ov.space.histo.predict_expression(
                wsi, method='hest_fm',
                reference=adata, genes=genes,
                fm_backbone='ctranspath',
                n_components=128, alpha=1.0,
            )
            pred
        """),
        _md("## Visualise predictions on the tissue"),
        _md(
            "The predicted AnnData carries tile-pixel centroids in "
            "`obsm['spatial']`, so any scanpy / `ov.pl` spatial plotter "
            "renders it directly. For high tile counts (3k+) the scanpy "
            "scatter is the fastest path; the heavier `zs.pl.tiles` with "
            "`style='heatmap'` is useful for publication-quality renders."
        ),
        _code("""
            import scanpy as sc
            sc.pl.embedding(pred, basis='spatial',
                            color=['EPCAM', 'ERBB2', 'CD68', 'ACTA2'],
                            cmap='magma', s=12, ncols=2, frameon=False)
        """),
        _md("## Sanity-check against held-out reference spots"),
        _md(
            "Predicting on the same H&E that the Visium reference came from "
            "gives a noisy proxy for accuracy: tile centroids do not coincide "
            "with spot centroids, so the comparison is over the joint spatial "
            "smoothing of both grids. The per-gene Pearson correlation should "
            "be positive across the panel."
        ),
        _code("""
            import numpy as np, pandas as pd
            from scipy.spatial import cKDTree
            from scipy.stats import pearsonr

            # nearest tile per spot
            spot_xy = adata.obsm['spatial']
            tile_xy = pred.obsm['spatial']
            nn = cKDTree(tile_xy).query(spot_xy, k=1)[1]

            ref_X = adata[:, pred.var_names].X
            ref_X = np.log1p(ref_X.toarray() if hasattr(ref_X, 'toarray') else ref_X)
            pred_X = pred.X[nn]
            rows = []
            for i, g in enumerate(pred.var_names):
                r, _ = pearsonr(ref_X[:, i], pred_X[:, i])
                rows.append((g, float(r)))
            corr_df = pd.DataFrame(rows, columns=['gene', 'pearson_r'])
            corr_df.sort_values('pearson_r', ascending=False).reset_index(drop=True)
        """),
        _md(
            "Predicted expression can now feed straight into the rest of "
            "`ov.space`: spatial domains (`ov.space.pySTAGATE`), spatially "
            "variable genes (`ov.space.svg`), deconvolution, or report writing."
        ),
    ]


# ---------------------------------------------------------------------------
# STPath tutorial (zero-shot)
# ---------------------------------------------------------------------------

def stpath_cells() -> list[nbf.NotebookNode]:
    return [
        _md("""
            # STPath — zero-shot generative foundation model

            STPath (Huang et al., *npj Digital Medicine* 2025) is a generative
            foundation model trained on 1,170 paired ST + H&E slides covering
            17 organs and 38,984 genes. The published weights
            (HuggingFace `tlhuang/STPath`) take **only** GigaPath features
            and tile centroids — no reference Visium slide is required.

            STPath currently leads HEST-Bench by +6.9 % Pearson over the next
            best method.

            **HuggingFace access** — both `prov-gigapath/prov-gigapath`
            (used for tile features) and the implicit STPath weights live
            behind HuggingFace gating. Request access on each model card,
            then `huggingface-cli login` once on this machine. The cell that
            calls `predict_expression(method='stpath')` will otherwise raise
            `GatedRepoError`.
        """),
        _md("## Environment & demo data"),
        _code("""
            import warnings, os
            warnings.filterwarnings('ignore')

            import omicverse as ov
            import lazyslide as zs
            ov.utils.ov_plot_set()

            adata, wsi = ov.space.histo.load_breast()
            ov.space.histo.tile(wsi, tile_px=224, mpp=0.5)
        """),
        _md(
            "## Extract GigaPath features (1536-d, gated)\n\n"
            "GigaPath weights live behind HuggingFace gating. Request access "
            "at https://huggingface.co/prov-gigapath/prov-gigapath, then "
            "`huggingface-cli login` on this machine. The cell raises "
            "`GatedRepoError` otherwise."
        ),
        _code("""
            try:
                ov.space.histo.embed(wsi, model='gigapath',
                                     batch_size=16, num_workers=0)
            except Exception as e:
                print(f'gigapath unavailable: {type(e).__name__}: {e}')
                raise
            wsi.tables['gigapath_tiles']
        """),
        _md("## Zero-shot prediction across 17 organs and 38,984 genes"),
        _code("""
            pred = ov.space.histo.predict_expression(
                wsi, method='stpath',
                organ='Breast', tech='Visium',
                genes=['EPCAM', 'ERBB2', 'CD68', 'ACTA2', 'VIM'],
            )
            pred
        """),
        _md("## Visualise"),
        _code("""
            import scanpy as sc
            sc.pl.embedding(pred, basis='spatial',
                            color=['EPCAM', 'ERBB2', 'CD68', 'ACTA2'],
                            cmap='magma', s=12, ncols=2, frameon=False)
        """),
        _md(
            "STPath returns log1p-normalised expression. For "
            "downstream analysis (`ov.space.svg`, `ov.pl.spatial`, …) treat "
            "`wsi.tables['stpath_tiles']` like any other Visium AnnData."
        ),
    ]


# ---------------------------------------------------------------------------
# STFlow tutorial (per-slide fine-tune)
# ---------------------------------------------------------------------------

def stflow_cells() -> list[nbf.NotebookNode]:
    return [
        _md("""
            # STFlow — per-slide flow-matching denoiser

            STFlow (Huang et al., *ICML 2025* Spotlight) models the
            joint distribution of gene expression across the **whole slide**
            with a spatial transformer + flow-matching denoiser. The
            upstream code releases training scripts only; this tutorial
            therefore runs the canonical "fit-on-your-reference,
            predict-on-your-query" workflow on a single GPU in a few minutes.

            Use STFlow when STPath's gene vocabulary doesn't cover your panel,
            when your tissue is far out-of-distribution from the 17 STPath
            organs, or when you want to capture cross-spot coherence in the
            output.
        """),
        _md("## Environment & demo data"),
        _code("""
            import warnings, os
            warnings.filterwarnings('ignore')

            import omicverse as ov
            import lazyslide as zs
            ov.utils.ov_plot_set()

            adata, wsi = ov.space.histo.load_breast()
            ov.space.histo.tile(wsi, tile_px=224, mpp=0.5)
            ov.space.histo.embed(wsi, model='ctranspath',
                                 batch_size=16, num_workers=0)
        """),
        _md(
            "## Fit a flow-matching denoiser on the reference, predict on the query\n\n"
            "Training the per-slide denoiser dominates the runtime. "
            "The cell below uses 80 epochs and a 500-gene HVG panel; "
            "the underlying transformer code is auto-cloned from "
            "`Graph-and-Geometric-Learning/STFlow` on first use."
        ),
        _code("""
            pred = ov.space.histo.predict_expression(
                wsi, method='stflow',
                reference=adata,
                fm_backbone='ctranspath',
                n_epochs=80, n_layers=4,
                n_sample_steps=5,
            )
            pred
        """),
        _md("## Visualise"),
        _code("""
            import scanpy as sc
            sc.pl.embedding(pred, basis='spatial',
                            color=list(pred.var_names[:4]),
                            cmap='magma', s=12, ncols=2, frameon=False)
        """),
    ]


# ---------------------------------------------------------------------------
# iStar tutorial (super-resolution)
# ---------------------------------------------------------------------------

def istar_cells() -> list[nbf.NotebookNode]:
    return [
        _md("""
            # iStar — super-resolve a paired Visium + H&E sample

            iStar (Zhang et al., *Nature Biotechnology* 2024) trains a
            per-slide head on top of HIPT (mahmoodlab) features to imp
            ute sub-spot gene expression at ~8 µm resolution. Unlike the
            spot-level backends (`stpath`, `stflow`, `hest_fm`), iStar's
            output is a much denser grid covering the full tissue
            footprint, suitable for cell-type pixel annotation and
            cluster-level differential analysis.

            `ov.space.histo.super_resolve(method='istar')` wraps iStar's
            shell pipeline behind one Python call: it stages the inputs in
            the format iStar's scripts expect, downloads the HIPT
            checkpoints from the `mahmoodlab/HIPT` GitHub LFS mirror on
            first use, trains a per-slide head, and reads the imputed
            expression back as an `AnnData`.

            **Licence** — iStar's vendored source lives at
            `omicverse.external.istar` and is GPL-3.0. Commercial users
            should contact the authors (see
            `omicverse/external/istar/NOTICE.md`).
        """),
        _md("## Environment & demo data"),
        _code("""
            import warnings, os
            warnings.filterwarnings('ignore')

            import omicverse as ov
            import lazyslide as zs
            ov.utils.ov_plot_set()

            adata, wsi = ov.space.histo.load_breast()
            adata, wsi
        """),
        _md("## Run iStar end-to-end"),
        _md(
            "Training the per-slide head dominates the runtime. The default "
            "`epochs=400` reproduces the paper exactly; lower it to 80 for "
            "this demo notebook."
        ),
        _code("""
            pred = ov.space.histo.super_resolve(
                adata, wsi=wsi, method='istar',
                pixel_size=0.5, n_top_genes=50, epochs=80,
            )
            pred
        """),
        _md("## Visualise sub-spot expression"),
        _md(
            "The output AnnData carries pixel-level coordinates in "
            "`obsm['spatial']`, so existing spatial plotters (scanpy, "
            "`ov.pl.spatial`, …) work out of the box."
        ),
        _code("""
            import scanpy as sc
            sc.pl.embedding(pred, basis='spatial', color=list(pred.var_names[:4]),
                            cmap='magma', s=1, ncols=2, frameon=False)
        """),
        _md(
            "iStar's sub-spot grid is much denser than the 3,798 Visium spots "
            "of the original sample. The output AnnData can feed downstream "
            "spatial-domain detection (`ov.space.pySTAGATE`) and clustering "
            "to surface near-single-cell tissue niches."
        ),
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
