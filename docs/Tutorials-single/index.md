# Tutorial of single cell RNA-seq

This page mirrors the `Single` section in `mkdocs.yml`.

## Alignment

- [Alignment of single-cell RNA-seq data](t_alignment_1k.ipynb)
- [Alignment of single-cell RNA-seq data for RNA velocity analysis](t_alignment_velocity.ipynb)

## Preprocessing

- [Preprocessing the data of scRNA-seq [CPU]](t_preprocess_cpu.ipynb)
- [Preprocessing the data of scRNA-seq [GPU]](t_preprocess_gpu.ipynb)
- [Preprocessing the data of scRNA-seq [Rust / out-of-memory]](t_preprocess_rust.ipynb)
- [Clustering space](t_cluster.ipynb)
- [Data integration and batch correction](t_single_batch.ipynb)
- [Consensus Non-negative Matrix factorization (cNMF)](t_cnmf.ipynb)
- [Lazy analysis of scRNA-seq](t_lazy.ipynb)

## Annotation

- [Reference-free automated single-cell cell type annotation](t_anno_noref.ipynb)
- [Reference automated single-cell cell type annotation](t_anno_ref.ipynb)
- [Consensus annotation with CellVote](t_cellvote.ipynb)
- [Mapping Cell Names to the Cell Ontology](t_cellmatch.ipynb)
- [**Individual methods** › SCSA · GPT-cell-type · MetaTiME · scMulan · TOSICA](anno-zoo/index.md)

## Trajectory

- [Prediction of absolute developmental potential using CytoTrace2](t_cytotrace.ipynb)
- [Trajectory Inference with Diffusion Map and PAGA](t_traj_diffusion.ipynb)
- [Trajectory Inference with Slingshot](t_traj_slingshot.ipynb)
- [Trajectory Inference with Palantir](t_traj_palantir.ipynb)
- [Trajectory Inference with scTour](t_traj_sctour.ipynb)
- [Trajectory Inference with Monocle 2](t_traj_monocle2.ipynb)
- [Trajectory Inference with StaVIA](t_traj_stavia.ipynb)
- [Trajectory Inference with VIA and scVelo](t_via_velo.ipynb)
- [Timing-associated genes analysis with TimeFateKernel](t_cellfate_gene.ipynb)
- [Identify the driver regulators of cell fate decisions](t_cellfate.ipynb)

## MetaCell

- [MetaCell overview — metacell vs pseudobulk, decision tree](metacell/index.md)
- [Recommended workflow — SEACells end-to-end + downstream](metacell/t_metacell_recommended.ipynb)
- [Multi-sample metacells with batch correction](metacell/t_metacell_multisample.ipynb)
- [**Backend zoo** › SEACells · MetaQ · SuperCell · k-means · random · GeoSketch · compare](metacell/zoo/index.md)

## Cell Structure

- [Differential expression and celltype analysis [All Cell]](t_deg_single.ipynb)
- [Differential expression analysis [Meta Cell]](t_scdeg.ipynb)
- [Gene Regulatory Network Analysis with SCENIC](t_scenic.ipynb)
- [Drug response predict with scDrug](t_scdrug.ipynb)
- [Batch Correction with SIMBA](t_simba.ipynb)

## Copy-Number Variation

- [Single-cell CNV with CopyKAT](t_copykat.ipynb)
- [Single-cell CNV with inferCNV](t_infercnv.ipynb)

## Enrichment

- [Pathway analysis with AUCell](t_aucell.ipynb)
- [Comparing enrichment-score methods on scRNA-seq](enrichment/t_es_compare.ipynb)

## Cell-Cell Communication

- [Cell-cell communication with CellPhoneDB](t_ccc_cellphonedb.ipynb)
- [Cell-cell communication with LIANA+](t_ccc_liana.ipynb)

## Multi-omics

- [Multi omics analysis by MOFA](t_mofa.ipynb)
- [Multi omics analysis by MOFA and GLUE](t_mofa_glue.ipynb)
- [Celltype annotation transfer in multi-omics](t_anno_trans.ipynb)
