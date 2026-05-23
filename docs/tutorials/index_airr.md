# Immune Repertoire

Tutorials for the `omicverse.airr` module — a unified analysis framework for
adaptive immune receptor repertoire sequencing (AIRR-seq: TCR / BCR).

`ov.airr` spans four regimes. The **single-cell** side is a clean, AnnData-native
reimplementation of the core of [scirpy](https://scirpy.scverse.org): reading
10x V(D)J / AIRR output, chain QC, exact and distance-based clonotype
definition, clonal expansion, clonotype networks, and repertoire metrics
(diversity, overlap, V(D)J usage, spectratype). The **bulk + B-cell** side
wraps standalone R-parity backend packages behind a registered,
`method=`-dispatch API: bulk repertoire analytics (`pyimmunarch`), the
Immcantation core (`pyalakazam`), somatic hypermutation (`pyshazam`), B-cell
clonal clustering (`pyscoper`), immunoglobulin genotyping (`pytigger`), and
B-cell phylogenetics (`pydowser`). The **TCR-specificity** side adds the
TCRdist metric, GLIPH2 motif grouping (`pygliph`), GIANA / clusTCR clustering,
meta-clonotype discovery and antigen-database annotation (VDJdb / McPAS /
IEDB); and the **TCR + transcriptome** side reimplements the core of
[CoNGA](https://github.com/phbradley/conga) for joint single-cell analysis.

Install the bulk / B-cell / GLIPH2 backends with `pip install omicverse[airr]`;
single-cell, TCRdist and CoNGA-style analysis run on numpy / pandas / anndata
with no extra package.

```{toctree}
:maxdepth: 1

../Tutorials-airr/t_airr_01_singlecell
../Tutorials-airr/t_airr_02_bulk
../Tutorials-airr/t_airr_03_bcr
../Tutorials-airr/t_airr_04_tcr
../Tutorials-airr/t_airr_05_tcr_gex
```
