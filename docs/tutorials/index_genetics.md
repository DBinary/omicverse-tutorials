# Genetics

A systematic, best-practice **GWAS pipeline** built on the
`omicverse.genetics` module — a unified statistical-genetics framework that
threads genotype, expression and complex traits into one analysis.

This chapter is a **two-notebook end-to-end workflow**, not a catalogue of
methods. It runs on a single coherent simulated cohort with a known ground
truth (`ov.genetics.simulate_gwas_study`), so every step can be shown to
recover the planted signal — and each step feeds the next:

1. **From genotypes to loci** — a quality-controlled association study:
   sample QC, variant QC, population-structure correction by genotype PCA,
   naive vs PC-adjusted association, genomic-inflation and Q-Q / Manhattan
   diagnostics, locus definition by LD clumping, and SuSiE statistical
   fine-mapping to 95% credible sets.
2. **From loci to mechanism** — functional follow-up of the GWAS hits:
   cis-eQTL mapping, Bayesian colocalization of the GWAS and eQTL signals,
   transcriptome-wide association (TWAS / PrediXcan), Mendelian
   randomization with MR-Egger pleiotropy sensitivity, SNP-heritability by
   LD score regression, and single-cell disease-relevance scoring (scDRS)
   to pinpoint the disease-relevant cell type.

Every step opens with the rationale — the *why*, the standard thresholds
and how to interpret the result — so the chapter reads as a GWAS protocol.
The statistical engines are the standalone R-parity packages
`pymatrixeqtl`, `pysusie`, `pycoloc`, `pytwosamplemr`, `pyscdrs`, `pyldsc`
and `pytwas`; the GWAS core (QC, association, genomic inflation) needs no
backend.

```{toctree}
:maxdepth: 1

../Tutorials-genetics/t_genetics_01_gwas_pipeline
../Tutorials-genetics/t_genetics_02_functional_followup
```
