# In-silico gene perturbation

`ov.single.perturb` runs a virtual gene perturbation on an `AnnData`
and returns the **post-perturbation expression**, the
**post-perturbation gene regulatory network**, and per-edge / per-gene
Δ-tables. It addresses [issue
omicverse#739](https://github.com/omicverse/omicverse/issues/739)
("Dynamo's virtual KO doesn't analyse downstream GRN").

## When to use

| Use this | Use something else |
|---|---|
| Want to know which TF→target edges change after a KO/OE | Want a cell-fate trajectory shift only → `ov.single.cell_fate_perturbation` (Dynamo) |
| Want a tidy `Δ-expression` + statistical Z / p-value table for downstream genes | Want a foundation-model prediction → Geneformer / scGPT (separate path) |
| Have scRNA-seq alone | Want multi-omics (ATAC + RNA) GRN → SCENIC+ / Pando |

## Three modes, one call

| `mode=` | Effect | Notes |
|---|---|---|
| `'ko'` | Knockout | expression clamped to 0 in the simulated cell state |
| `'kd'` | Knockdown | expression scaled by `1/fold_change` |
| `'oe'` | Over-expression | expression scaled by `fold_change` |

## Backends — pick by what data you have

| Backend | Min data | Strength | Tutorial |
|---|---|---|---|
| **`sctenifoldknk`** ⭐ | scRNA only | Built-in differential-regulation table with `Z`, `FC`, `adjusted p-value` from a PCNet that's identical to what raw scTenifoldKnk produces (parity verified — see end of the tutorial). | [t_perturb_sctenifoldknk](t_perturb_sctenifoldknk.ipynb) |
| **`cell_oracle`** | scRNA + base GRN (motif/ATAC, optional) | Propagates the perturbation through a base GRN for `n_propagation` steps; emits a `trajectory_shift` matrix + a perturbed GRN. Best when you already have an ATAC/motif-derived base GRN or want CellOracle's cell-state-shift heatmap. | [t_perturb_celloracle](t_perturb_celloracle.ipynb) |
| **`auto`** | — | Picks `cell_oracle` if `adata.uns['base_grn']` is present (or you pass `grn_base=`); otherwise falls back to `sctenifoldknk`. | — |

Both backends are **lazy imports** — `omicverse.single` itself doesn't
require either to be installed.

```{toctree}
:maxdepth: 1

t_perturb_sctenifoldknk
t_perturb_celloracle
t_perturb_unified
```

## Unified downstream analyses (Tier A / B / C)

Regardless of backend, every `PerturbResult` exposes the **same**
downstream API. See [t_perturb_unified](t_perturb_unified.ipynb) for an
end-to-end run on the official Paul15 dataset.

| Tier | Method | What it gives |
|---|---|---|
| **A** | `result.delta_X`, `.trajectory_shift` | unified per-cell + cell×cell |
| **A** | `result.add_significance()` | adds `z_score`/`p_value`/`adj_p_value` to delta_expr |
| **B** | `result.perturbation_score(pseudotime=)` | per-cell promote/block score |
| **B** | `result.cluster_transitions()` | source × target cluster matrix |
| **B** | `ov.pl.perturb_sankey/quiver/volcano(...)` | publication-style plots |
| **C** | `result.pathway_enrichment(...)` | GO / KEGG / Reactome enrichment |
| **C** | `result.phenotype_enrichment(...)` | MGI / HPO / DisGeNET enrichment |
| **C** | `result.run_markov(start_cells=...)` | long-run cell fate sampling |
| **C** | `result.validate_against_perturbseq(...)` | predicted-vs-observed correlation + top-K precision |
| **C** | `result.permutation_test(n_perms=...)` | overall robustness Z |

## API at a glance

```python
import omicverse as ov

result = ov.single.perturb(
    adata,
    target='Sox2',          # gene name or list of names
    mode='ko',              # 'ko' | 'kd' | 'oe'
    backend='auto',         # 'auto' | 'sctenifoldknk' | 'cell_oracle'
    fold_change=2.0,        # for OE / KD
    grn_base=None,          # for cell_oracle backend (DataFrame or networkx graph)
    n_propagation=3,        # CellOracle-only
    grn_output=True,
    return_delta=True,
)

# What you get back:
result.adata_perturbed     # AnnData with predicted post-perturbation counts (when supported)
result.grn                 # networkx.DiGraph of the perturbed GRN
result.grn_base            # networkx.DiGraph of the baseline GRN
result.delta_grn           # DataFrame (source, target, weight_base, weight_pert, delta)
result.delta_expr          # DataFrame (gene, delta, Z, log2_fc, p-value, adjusted p-value)
result.trajectory_shift    # CellOracle's transition_prob matrix (or None)
result.summary(top_n=10)   # printable + returned top-affected genes
```

## References

- Osorio, D., Zhong, Y. *et al.* **scTenifoldKnk: an efficient virtual
  knockout tool for gene function predictions via single-cell gene
  regulatory network perturbation.** *Patterns* 3, 100434 (2022).
- Kamimoto, K., Stringa, B., Hoffmann, C.M. *et al.* **Dissecting cell
  identity via network inference and in silico gene perturbation.**
  *Nature* 614, 742–751 (2023). — CellOracle.
- [Issue omicverse#739](https://github.com/omicverse/omicverse/issues/739)
  motivated this module.
