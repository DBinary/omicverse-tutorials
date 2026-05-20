# Proteomics

Tutorials for the `omicverse.protein` module — downstream analysis of bulk quantitative
proteomics: label-free LC-MS/MS (MaxQuant, DIA-NN, FragPipe) and affinity proteomics
(Olink NPX). Covers QC, missing-value diagnosis and MCAR/MNAR classification, normalization,
peptide → protein summarization, imputation, differential expression (DEqMS, proDA, MSstats,
limma), and functional enrichment. Every tutorial runs on a real published dataset served
through `ov.datasets`. The statistical engines are the standalone R-parity packages
`pyimputelcmd`, `pydeqms`, `pyproda`, `pymsstats` and `pyolinkanalyze`.

```{toctree}
:maxdepth: 1

../Tutorials-protein/t_protein_01_bulk_pipeline
../Tutorials-protein/t_protein_02_missing_values
../Tutorials-protein/t_protein_03_summarization_dia
../Tutorials-protein/t_protein_04_differential_expression
../Tutorials-protein/t_protein_05_olink
```
