# Immune Repertoire (AIRR-seq)

Tutorials for the `omicverse.airr` module — a unified analysis framework for
adaptive immune receptor repertoire sequencing (AIRR-seq: TCR / BCR).

`ov.airr` spans two regimes. The **single-cell** side is a clean, AnnData-native
reimplementation of the core of [scirpy](https://scirpy.scverse.org): reading
10x V(D)J / AIRR output, chain QC, exact and distance-based clonotype
definition, clonal expansion, clonotype networks, and repertoire metrics
(diversity, overlap, V(D)J usage, spectratype). The **bulk + B-cell** side
wraps six standalone R-parity backend packages behind a registered,
`method=`-dispatch API: bulk repertoire analytics (`pyimmunarch`), the
Immcantation core (`pyalakazam`), somatic hypermutation (`pyshazam`), B-cell
clonal clustering (`pyscoper`), immunoglobulin genotyping (`pytigger`), and
B-cell phylogenetics (`pydowser`).

Install the bulk / B-cell backends with `pip install omicverse[airr]`; the
single-cell analysis runs on numpy / pandas / anndata with no extra package.

```{toctree}
:maxdepth: 1

../Tutorials-airr/t_airr_01_singlecell
../Tutorials-airr/t_airr_02_bulk
../Tutorials-airr/t_airr_03_bcr
```
