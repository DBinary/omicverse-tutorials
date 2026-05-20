# Tutorials of Proteomics

`ov.protein` is the AnnData-native downstream framework for **bulk
quantitative proteomics** — label-free LC-MS/MS (MaxQuant, DIA-NN,
FragPipe) and affinity proteomics (Olink NPX). It starts from
search-engine output (a protein- or peptide-level intensity table) and
covers the full downstream workflow: QC, MCAR/MNAR missingness
classification, normalization, peptide→protein summarization, missing-
value imputation, differential expression, and pathway enrichment.

Every stage is a single dispatcher function with a `method=` selector,
the same design as `ov.es` and `ov.metabol`. The statistical engines
are shipped as standalone, R-parity-tested packages that `ov.protein`
wraps:

| Backend package | Ports R package | Role |
|---|---|---|
| `pyimputelcmd` | Bioconductor **imputeLCMD** | left-censored imputation (MinDet / MinProb / QRILC / MLE / KNN / SVD) |
| `pydeqms` | Bioconductor **DEqMS** | peptide-count-aware moderated *t* |
| `pyproda` | Bioconductor **proDA** | MNAR probabilistic differential expression |
| `pymsstats` | Bioconductor **MSstats** | DDA/DIA converters, summarization, group comparison |
| `pyolinkanalyze` | CRAN **OlinkAnalyze** | Olink NPX QC, bridge normalization, LMM |

All five are pure-Python (no `rpy2`), validated bit-for-bit / by Pearson
correlation against the original R packages.

!!! note "Out of scope"
    Single-cell proteomics (SCP) and spatial proteomics (IMC / CODEX)
    are **not** covered by `ov.protein` — use `squidpy` / `SCIMAP` for
    spatial protein imaging.

## Bulk LC-MS/MS workflow

- [Bulk proteomics: QC → impute → differential expression](t_protein_01_intro.ipynb) — the end-to-end label-free pipeline on a simulated MaxQuant-style dataset, comparing DEqMS / limma / proDA / Wilcoxon.

## Peptide-level workflow

- [Peptide → protein summarization](t_protein_02_summarization.ipynb) — collapsing a PSM/peptide-level table to protein level with median / median-sweeping / Tukey-median-polish, then DE.

## Affinity proteomics

- [Olink NPX analysis](t_protein_03_olink.ipynb) — reading NPX, bridge normalization, and differential expression for Olink Explore/Target panels.
