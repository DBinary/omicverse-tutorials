# Release Notes

## v 1.0.0
- First public release.

## v 1.1.7
### bulk module:
- Added Deseq2, including `pyDEseq` functions: `deseq2_normalize`, `estimateSizeFactors`, `estimateDispersions`, `Matrix_ID_mapping`.
- Included TCGA with `TCGA`.
- Introduced Enrichment with functions `geneset_enrichment`, `geneset_plot`.

### single module:
- Integrated scdrug with functions `autoResolution`, `writeGEP`, `Drug_Response`.
- Added cpdb with functions `cpdb_network_cal`, `cpdb_plot_network`, `cpdb_plot_interaction`, `cpdb_interaction_filtered`.
- Included scgsea with functions `geneset_aucell`, `pathway_aucell`, `pathway_aucell_enrichment`, `pathway_enrichment`, `pathway_enrichment_plot`.

## v 1.1.8
### single module:
- Addressed errors in cpdb, including import errors and color issues in `cpdb_plot_network`.
- Introduced `cpdb_submeans_exacted` in cpdb for easy sub-network extraction.

## v 1.1.9
### bulk2single module:
- Added the `bulk2single` module.
- Fixed model load error from bulk2space.
- Resolved early stop issues from bulk2space.
- Included more user-friendly input methods and visualizations.
- Added loss history visualization.

### utils module:
- Introduced `pyomic_palette` in the plot module.

## v 1.1.10
- Updated all code references.

### single module:
- Fixed non-valid parameters in `single.mofa.mofa_run` function.
- Added layer raw count addition in `single.scanpy_lazy` function.
- Introduced `utils.plot_boxplot` for plotting box plots with jittered points.
- Added `bulk.pyDEseq.plot_boxplot` for plotting box plots with jittered points for specific genes.

## v 1.2.0
### bulk module:
- Fixed non-valid `cutoff` parameter in `bulk.geneset_enrichment`.
- Added modules: `pyPPI`, `pyGSEA`, `pyWGCNA`, `pyTCGA`, `pyDEG`.

### bulk2single module:
- Introduced `bulk2single.save` for manual model saving.

## v 1.2.1-4
### single module:
- Added `pySCSA` module with functions: `cell_anno`, `cell_anno_print`, `cell_auto_anno`, `get_model_tissue`.
- Implemented doublet cell filtering in `single.scanpy_lazy`.
- Added `single.scanpy_cellanno_from_dict` for easier annotation.
- Updated SCSA database from [CellMarker2.0](http://bio-bigdata.hrbmu.edu.cn/CellMarker/).
- Fixed errors in SCSA database keys: `Ensembl_HGNC` and `Ensembl_Mouse`.

## v 1.2.5
### single module:
- Added `pyVIA` module with functions: `run`, `plot_piechart_graph`, `plot_stream`, `plot_trajectory_gams`, `plot_lineage_probability`, `plot_gene_trend`, `plot_gene_trend_heatmap`, `plot_clustergraph`.
- Fixed warning error in `utils.pyomic_plot_set`.
- Updated requirements, including `pybind11`, `hnswlib`, `termcolor`, `pygam`, `pillow`, `gdown`.

## v 1.2.6
### single module:
- Added `pyVIA.get_piechart_dict` and `pyVIA.get_pseudotime`.

## v 1.2.7
### bulk2single module:
- Added `Single2Spatial` module with functions: `load`, `save`, `train`, `spot_assess`.
- Fixed installation errors for packages in pip.

## v 1.2.8
- Fixed pip installation errors.

### bulk2single module:
- Replaced `deep-forest` in `Single2Spatial` with `Neuron Network` for classification tasks.
- Accelerated the entire Single2Spatial inference process using GPU and batch-level estimation by modifying the `predicted_size` setting.

## v 1.2.9
### bulk module:
- Fixed duplicates_index mapping in `Matrix_ID_mapping`.
- Resolved hub genes plot issues in `pyWGCNA.plot_sub_network`.
- Fixed backupgene in `pyGSEA.geneset_enrichment` to support rare species.
- Added matrix plot module in `pyWGCNA.plot_matrix`.

### single module:
- Added `rank_genes_groups` check in `pySCSA`.

### bulk2single module:
- Fixed import error of `deepforest`.

## v 1.2.10
- Renamed the package to `omicverse`.

### single module:
- Fixed argument error in `pySCSA`.

### bulk2single module:
- Updated plot arguments in `bulk2single`.

## v 1.2.11
### bulk module:
- Fixed `wilcoxon` method in `pyDEG.deg_analysis`.
- Added parameter setting for treatment and control group names in `pyDEG.plot_boxplot`.
- Fixed figure display issues in `pyWGCNA.plot_matrix`.
- Fixed category correlation failed by one-hot in `pyWGCNA.analysis_meta_correlation`.
- Fixed network display issues in `pyWGCNA.plot_sub_network` and updated `utils.plot_network` to avoid errors.

## v 1.3.0
### bulk module:
- Added `DEseq2` method to `pyDEG.deg_analysis`.
- Introduced `pyGSEA` module in `bulk`.
- Renamed raw `pyGSEA` to `pyGSE` in `bulk`.
- Added `get_gene_annotation` in `utils` for gene name transformation.

## v 1.3.1
### single module:
- Added `get_celltype_marker` method.

### single module:
- Added `GLUE_pair`, `pyMOFA`, `pyMOFAART` module.
- Added tutorials for `Multi omics analysis by MOFA and GLUE`.
- Updated tutorial for `Multi omics analysis by MOFA`.

## v 1.4.0
### bulk2single module:
- Added `BulkTrajBlend` method.

### single module:
- Fixed errors in `scnocd` model.
- Added `save`, `load`, and `get_pair_dict` in `scnocd` model.

### utils module:
- Added `mde` method.
- Added `gz` format support for `utils.read`.

## v 1.4.1
### preprocess module:
- Added `pp` (preprocess) module with `qc` (quantity control), `hvg` (high variable feature), `pca`.
- Added `data_files` for cell cycle calculation from [Cellula](https://github.com/andrecossa5/Cellula/) and [pegasus](https://github.com/lilab-bcb/pegasus/).

## v 1.4.3
###

 preprocess module:
- Fixed sparse preprocess error in `pp`.
- Fixed trajectory import error in `via`.
- Added gene correlation analysis of trajectory.

## v 1.4.4
### single module:
- Added `panglaodb` database to `pySCSA` module.
- Fixed errors in `pySCSA.cell_auto_anno` when some cell types are not found in clusters.
- Fixed errors in `pySCSA.cell_anno` when `rank_genes_groups` are not consistent with clusters.
- Added `pySIMBA` module in single for batch correction.

### preprocess module:
- Added `store_layers` and `retrieve_layers` in `ov.utils`.
- Added `plot_embedding_celltype` and `plot_cellproportion` in `ov.utils`.

## v 1.4.5
### single module:
- Added `MetaTiME` module to perform cell type annotation automatically in TME.

## v 1.4.12
- Updated `conda install omicverse -c conda-forge`.

### single module:
- Added `pyTOSICA` module to perform cell type migration from reference scRNA-seq in Transformer model.
- Added `atac_concat_get_index`, `atac_concat_inner`, `atac_concat_outer` functions to merge/concatenate scATAC data.
- Fixed `MetaTime.predicted` when Unknown cell type appears.

### preprocess module:
- Added `plot_embedding` in `ov.utils` to plot UMAP in a special color dictionary.

## v 1.4.13
### bulk module:
- Added `mad_filtered` to filter robust genes when calculating the network in `ov.bulk.pyWGCNA` module.
- Fixed `string_interaction` in `ov.bulk.pyPPI` for string-db updates.

### preprocess module:
- Changed `mode` argument of `pp.preprocess` to control preprocessing steps.
- Added `ov.utils.embedding`, `ov.utils.neighbors`, and `ov.utils.stacking_vol`.

## v 1.4.14
### preprocess module:
- Added `batch_key` in `pp.preprocess` and `pp.qc`.

### utils module:
- Added `plot_ConvexHull` to visualize the boundary of clusters.
- Added `weighted_knn_trainer` and `weighted_knn_transfer` for multi-adata integration.

### single module:
- Fixed import errors in `mofa`.

## v 1.4.17
### bulk module:
- Fixed compatibility issues with `pydeseq2` version `0.4.0`.
- Added `bulk.batch_correction` for multi-bulk RNA-seq/microarray samples.

### single module:
- Added `single.batch_correction` for multi-single cell datasets.

### preprocess module:
- Added parameter `layers_add` in `pp.scale`.

## v 1.5.0
### single module:
- Added `cellfategenie` to calculate timing-associated genes/genesets.
- Fixed the name error in `atac_concat_outer`.
- Added more kwargs for `batch_correction`.

### utils module:
- Added `plot_heatmap` to visualize the heatmap of pseudotime.
- Fixed `embedding` when the version of `mpl` is larger than `3.7.0`.
- Added `geneset_wordcloud` to visualize geneset heatmaps of pseudotime.

## v 1.5.1
### single module:
- Added `scLTNN` to infer cell trajectory.

### bulk2single module:
- Updated cell fraction prediction with `TAPE` in bulk2single.
- Fixed group and normalization issues in bulk2single.

### utils module:
- Added `Ro/e` calculation (by: Haihao Zhang).
- Added `cal_paga` and `plot_paga` to visualize the state transfer matrix.
- Fixed the `read` function.

## v 1.5.2
### bulk2single Module:
- Resolved a matrix error occurring when gene symbols are not unique.
- Addressed the `interpolation` issue in `BulkTrajBlend` when target cells do not exist.
- Corrected the `generate` function in `BulkTrajBlend`.
- Rectified the argument for `vae_configure` in `BulkTrajBlend` when `cell_target_num` is set to None.
- Introduced the parameter `max_single_cells` for input in `BulkTrajBlend`.
- Defaulted to using `scaden` for deconvolution in Bulk RNA-seq.

### single Module:
- Fixed an error in `pyVIA` when the root is set to None.
- Added the `TrajInfer` module for inferring cell trajectories.
- Integrated `Palantir` and `Diffusion_map` into the `TrajInfer` module.
- Corrected the parameter error in `batch_correction`.

### utils Module:
- Introduced `plot_pca_variance_ratio` for visualizing the ratio of PCA variance.
- Added the `cluster` and `filtered` module for clustering the cells
- Integrated `MiRA` to calculate the LDA topic

## v 1.5.3
### single Module:
- Added `scVI` and `MIRA` to remove batch effect

### space Module:
- Added `STAGATE` to cluster and denoisy the spatial RNA-seq 

### pp Module:
- Added `doublets` argument of `ov.pp.qc` to control doublets('Default'=True)

## v 1.5.4
### bulk Module:
- Fixed an error in `pyDEG.deg_analysis` when `n_cpus` can not be set in `pyDeseq2(v0.4.3)`

### single Module:
- Fixed an argument error in `single.batch_correction` of combat

### utils Module:
- Added `venn4` plot to visualize
- Fixed the label visualization of `plot_network`
- Added `ondisk` argument of `LDA_topic`

### space Module:
- Added `Tangram` to mapping the scRNA-seq to stRNA-seq

## v 1.5.5
### pp Module:
- Added `max_cells_ratio` and `max_genes_ratio` to control the max threshold in qc of scRNA-seq

### single Module:
- Added `SEACells` model to calculate the metacells from scRNA-seq

### space Module:
- Added `STAligner` to integrate multi stRNA-seq

## v 1.5.6
### pp Module
- Added `mt_startswith` argument to control the `qc` in mouse or other species.

### utils Module
- Added `schist` method to cluster the single cell RNA-seq

### single Module
- Fixed the import error of `palantir` in SEACells
- Added `CEFCON` model to identify the driver regulators of cell fate decisions

### bulk2single Module
- Added `use_rep` and `neighbor_rep` argument to configure the nocd 

### space Module
- Added `SpaceFlow` to identify the pseudo-spatial map

## v 1.5.8

### pp Module
- Added `score_genes_cell_cycle` function to calculate the cell cycle

### bulk Module
- Fixed `dds.plot_volcano` text plot error when the version of `adjustText` larger than `0.9`

### single Module
- Optimised `MetaCell.load` model loading logic
- Fixed an error when loading the model usng `MetaCell.load`
- Added tutorials of `Metacells`

### pl Module

Add `pl` as a unified drawing prefix for the next release, to replace the drawing functionality in the original utils, while retaining the drawing in the original utils.

- Added `embedding` to plot the embedding of scRNA-seq using `ov.pl.embedding`
- Added `optim_palette` to provide a spatially constrained approach that generates discriminate color assignments for visualizing single-cell spatial data in various scenarios
- Added `cellproportion` to plot the proportion of stack bar of scRNA-seq
- Added `embedding_celltype` to plot the figures both celltype proportion and embedding
- Added `ConvexHull` to plot the ConvexHull around the target cells
- Added `embedding_adjust` to adjust the text of celltype legend in embedding
- Added `embedding_density` to plot the category density in the cells
- Added `bardotplot` to plot the bardotplot between different groups.
- Added `add_palue` to plot the p-threshold between different groups.
- Added `embedding_multi` to support the `mudata` object
- Added `purple_color` to visualize the purple palette.
- Added `venn` to plot the venn from set 2 to set 4
- Added `boxplot` to visualize the boxdotplot
- Added `volcano` to visualzize the result of differential expressed genes

## v 1.5.9

### single Module

- Added `slingshot` in `single.TrajInfer`
- Fixed some error of `scLTNN`
- Added `GPU` mode to preprocess the data
- Added `cNMF` to calculate the nmf

### space Module

- Added `Spatrio` to mapping the scRNA-seq to stRNA-seq

## v 1.6.0

Move `CEFCON`,`GNTD`,`mofapy2`,`spaceflow`,`spatrio`,`STAligner`,`tosica` from root to external module.

### space Module

- Added `STT` in `omicverse.space` to calculate the spatial transition tensor.
- Added `scSLAT` in `omicverse.external` to align of different spatial slices.
- Added `PROST` in `omicverse.external` and `svg` in `omicverse.space` to identify the spatially variable genes and domain.

### single Module

- Added `get_results_rfc` in `omicverse.single.cNMF` to predict the precise cluster in complex scRNA-seq/stRNA-seq
- Added `get_results_rfc` in `omicverse.utils.LDA_topic` to predict the precise cluster in complex scRNA-seq/stRNA-seq
- Added `gptcelltype` in `omicverse.single` to annotate celltype using large language model #82.

### pl Module

- Added `plot_spatial` in `omicverse.pl` to visual the spot proportion of cells when deconvolution

## v 1.6.2

Support Raw Windows platform

- Added `mde` in `omicverse.pp` to accerate the umap calculation.

## v 1.6.3

- Added  `ov.setting.cpu_init` to change the environment to CPU.
- Move module `tape`,`SEACells` and `palantir` to `external`

### Single Module
- Added `CytoTrace2` to predict cellular potency categories and absolute developmental potential from single-cell RNA-sequencing data.
- Added `cpdb_exact_target` and `cpdb_exact_source` to exact the means of special ligand/receptor
- Added `gptcelltype_local` to identify the celltype using local LLM #96 #99

### Bulk Module
- Added `MaxBaseMean` columns in dds.result to help people ignore the empty samples.
  
### Space Module
- Added `**kwargs` in `STT.compute_pathway`
- Added `GraphST` to identify the spatial domain

### pl Module
- Added `cpdb_network`, `cpdb_chord`, `cpdb_heatmap`, `cpdb_interacting_network`,`cpdb_interacting_heatmap` and `cpdb_group_heatmap` to visualize the result of CellPhoneDB

### utils Module
- Added `mclust_py` to identify the Gaussian Mixture cluster
- Added `mclust` methdo in `cluster` function

## v 1.6.4

### Bulk Module

- Optimised pyGSEA's `geneset_plot` visualisation of coordinate effects
- Fixed an error of `pyTCGA.survival_analysis` when the matrix is sparse. #62, #68, #95
- Added tqdm to visualize the process of `pyTCGA.survial_analysis_all`
- Fixed an error of `data_drop_duplicates_index` with remove duplicate indexes to retain only the highest expressed genes #45
- Added `geneset_plot_multi` in `ov.bulk` to visualize the multi results of enrichment. #103

### Single Module

- Added `mellon_density` to calculate the cell density. #103

### PP Module
- Fixed an error of `ov.pp.pca` when pcs smaller than 13. #102
- Added `COMPOSITE` in `ov.pp.qc`'s method to predicted doublet cells. #103
- Added `species` argument in `score_genes_cell_cycle` to calculate the cell phase without gene manual input

## v 1.6.6

### Pl Module

- Fixed the 'celltyep_key' error of `ov.pl.cpdb_group_heatmap` #109
- Fixed an error in `ov.utils.roe` when some expected frequencies are less than expected value.
- Added `cellstackarea` to visual the Percent stacked area chart of celltype in samples.

### Single Module
- Fixed the bug of `ov.single.cytotrace2` when adata.X is not sparse data. #115, #116
- Fixed the groupby error in `ov.single.get_obs_value` of SEACells.
- Fixed the error of cNMF #107, #85
- Fixed the plot error when `Pycomplexheatmap` version > 1.7 #136


### Bulk Module

- Fixed an key error in `ov.bulk.Matrix_ID_mapping`
- Added `enrichment_multi_concat` in `ov.bulk` to concat the result of enrichment.
- Fixed the pandas version error in gseapy #137

### Bulk2Single Module

- Added `adata.var_names_make_unique()` to avoid mat shape error if gene not unique. #100

### Space Module

- Fixed an error in `construct_landscape` of `ov.space.STT`
- Fixed an error of `get_image_idx_1D` in `ov.space.svg` #117
- Added `COMMOT` to calculate the cell-cell interaction of spatial RNA-seq.
- Added `starfysh` to deconvolute spatial transcriptomic without scRNA-seq (#108)

### PP Module

- Updated constraint error of ov.pp.mde #129
- Fixed type error of `float128` #134


## v 1.6.7

### Space Module

- Added `n_jobs` argument to adjust thread in `extenel.STT.pl.plot_tensor_single`
- Fixed an error in `extenel.STT.tl.construct_landscape`
- Updated the tutorial of `COMMOT` and `Flowsig`
  

### Pl Module

- Added `legend_awargs` to adjust the legend set in `pl.cellstackarea` and `pl.cellproportion`

### Single Module

- Fixed the error of `get_results` and `get_results_rfc` in `cNMF` module. (#143) (#139)
- Added `sccaf` to obtain the best clusters.
- Fixed the `.str` error in cytotrace2 (#146)

### Bulk Module

- Fixed the import error of `gseapy` in `bulk.geneset_enrichment`
- Optimized code logic for offline enrichment analysis, added background parameter
- Added `pyWGCNA` package replace the raw calculation of pyWGCNA (#162)

### Bulk2Single Module

- Remove `_stat_axis` in `bulk2single_data_prepare` and use `index` instead of it (#160).

### PP Module

- Fixed a return bugs in `pp.regress_and_scale` (#156)
- Fixed a scanpy version error when using `ov.pp.pca` (#154)

## v 1.6.8

### Bulk Module

- Fixed the error of log_init in gsea_obj.enrichment (#184)
- Added `ax` argument to visualize the `geneset_plot`

### Space Module

- Added CAST to integrate multi slice
- Added `crop_space_visium` in `omicverse.tl` to crop the sub area of space data

### Pl Module

- Added `legend` argument to visualize the `cpdb_heatmap`
- Added `text_show` argument to visualize the `cellstackarea`
- Added `ForbiddenCity` color system

## v 1.6.9

### PP Module

- Added `recover_counts` to recover `counts` after `ov.pp.preprocess`
- removed the lognorm layers added in `ov.pp.pca`

### Single Module

- Added `MultiMap` module to integrate multi species
- Added `CellVote` to vote the best cells
- Added `CellANOVA` to integrate samples and correct the batch effect
- Added `StaVia` to calculate the pseudotime and infer trajectory.

### Space Module

- Added `ov.space.cluster` to identify the spatial domain
- Added `Binary` for spatial cluster
- Added `Spateo` to calculate the SVG

## v 1.7.0

Added `cpu-gpu-mixed` to accelerate the analysis of scrna-seq using GPU.
Changed the logo presentation of Omicverse to `ov.plot_set`

### Bulk Module
- Added `limma`, `edgeR` in different expression gene analysis. (#238)
- Fixed the version error of `DEseq2` analysis.

### Single Module
- Added `lazy` function to calculate all function of scrna-seq (#291)
- Added `generate_scRNA_report` and `generate_reference_table` to generate the report and reference (#291) (#292)
- Fixed `geneset_prepare` not being able to read gmt not split by `\t\t` (#235) (#238)
- Added `geneset_aucell_tmp`,`pathway_aucell_tmp`,`pathway_aucell_enrichment_tmp` to test the chunk_size (#238)
- Added data enhancement of `Fate`
- Added `plot_atlas_view_ov` in VIA
- Fixed an error when the matrix is too large in `recover_counts`.
- Added `forceatlas2` to calculate the `X_force_directed`.
- Added `milo` and `scCODA` to analysis different celltype abundance.
- Added `memento` to analysis different gene expression.

### Space Module
- Added `GASTON` to learn a topographic map of a tissue slice from spatially resolved transcriptomics (SRT) data (#238)
- Added super kwargs in `plot_tensor_single` of STT.
- Updated `COMMOT` using GPU-accerlate
  
### Plot Module
- Added `dotplot_doublegroup` to visual the genes in doublegroup.
- Added `transpose` argument of `cpdb_interacting_heatmap` to transpose the figure.
- Added `calculate_gene_density` to plot the gene's density. 


## v 1.7.1

### Single Module
- Fixed some error of `ov.single.lazy`.
- Fixed the format of `ov.single.generate_scRNA_report`
- Updated some functions of `palantir`
- Added `CellOntologyMapper` to map cell name.


## v 1.7.2

### Pl Module
- Optimated the plot effect of `ov.pl.box_plot`
- Optimated the plot effect of `ov.pl.volcano`
Optimated the plot effect of `ov.pl.violin`
- Added beautiful dotplot than scanpy (#318)
- Added the similar visualization function of CellChat. (#313)

### Space Module
- Added 3D cell-cell interaction analysis in `COMMOT` (#315)

### Single Module
- Fixed the error of pathway_enrichment. (#184)
- Added SCENIC module with GPU-accerlate. (#331) 

### utils Module
- Added scICE to calculate the best cluster (#329)

## v 1.7.6

### LLM Module
- Added `GeneFromer`, `scGPT`, `scFoundation`, `UCE`, `CellPLM` to call directly in OmicVerse.

### Pl Module
- Optimized the visualization effect of embedding.
- Added `ov.pl.umap`, `ov.pl.pca`, `ov.pl.mde`, and `ov.pl.tsne` 


## v 1.7.8

Implemented lazy loading system that reduces `import omicverse` time by **40%** (from ~7.8s to ~4.7s).
Added GPU-accelerated PCA support for Apple Silicon (MLX) and CUDA (TorchDR) devices.
Introduced Smart Agent System with natural language processing for 50+ AI models from 8 providers.
Added and fixed the `anndata-rs` to support million size's datasets (#336)

### PP Module
- Added GPU-accelerated PCA in `ov.pp.pca()` with MLX support for Apple Silicon MPS devices
- Added TorchDR-based PCA acceleration in `ov.pp.pca()` for NVIDIA CUDA devices
- Added smart device detection and automatic backend selection in `init_pca()` and `pca()` functions
- Added graceful fallback to CPU implementation when GPU acceleration fails
- Added enhanced verbose output with device selection information and emoji indicators
- Added optimal component determination based on variance contribution thresholds in `init_pca()`
- Added GPU-accelerated SUDE dimensionality reduction in `ov.pp.sude()` with MLX/CUDA support
- Optimize the `ov.pp.qc` and added ribosome and hb-genes to know more information of data quantity.

### Datasets Module
- Complete elimination of scanpy dependencies for faster loading
- Added dynamo-style dataset framework with comprehensive collection
- Added robust download system with progress tracking and caching
- Added enhanced mock data generation with realistic structure
- Added support for h5ad, loom, xlsx, and compressed formats

### Agent Module
- Added multi-provider LLM support (OpenAI, Anthropic, Google, DeepSeek, Qwen, Moonshot, Grok, Zhipu AI)
- Added natural language processing for both English and Chinese
- Added code generation architecture with local execution
- Added function registry system with multi-language aliases
- Added smart API key management and provider-specific configuration

### Bulk Module
- Added `BayesPrime` and `Scaden` to deconvoluted Bulk RNA-seq's celltype proportion.
- Added `alignment` to alignment the fastq to counts.

### Single Module
- Added `ov.single.Annotation` and `ov.single.AnnotationRef` to annotate the cell type automatically.
- Added `ov.alignment.single` to alignment the scRNA-seq to counts directly.

## v 1.7.9

Implemented **smart lazy loading system** that dramatically reduces `import omicverse` time by **85.6x** (from ~16.57s to ~0.19s).
Enhanced RNA-seq alignment workflow with comprehensive toolkit for FASTQ processing and counting.
Optimized dataset management with nested directory creation for better organization.

### Performance Optimization

**Lazy Loading System**:
- Implemented module-level lazy loading using `__getattr__` mechanism for all major modules
- Added attribute-level lazy loading for frequently-used functions (read, palette, Agent, etc.)
- Introduced intelligent caching system to ensure instant access after first load
- Reduced initial import time from **16.57 seconds to 0.19 seconds** (85.6x speedup)
- Maintained full backward compatibility - all existing code works without modification
- Preserved complete IDE support with tab completion via `__dir__()` implementation
- Fixed circular import issues by delaying settings module initialization
- **MkDocs API documentation generation fully compatible** with lazy loading

**Benefits for Users**:
- ⚡ Instant startup for Jupyter notebooks and scripts
- 🎯 Load only what you use - modules imported on first access
- 💾 Reduced memory footprint for simple tasks
- 🔄 Second access is cached and instant (< 0.001s)

### Alignment Module

**New Comprehensive RNA-seq Alignment Toolkit**:

Added complete end-to-end workflow for processing raw sequencing data:

- **`ov.alignment.prefetch`**: Download SRA datasets from NCBI with built-in retry logic
- **`ov.alignment.fqdump`**: Convert SRA to FASTQ format with parallel processing support
- **`ov.alignment.parallel_fastq_dump`**: High-performance parallel FASTQ extraction
- **`ov.alignment.fastp`**: Quality control and adapter trimming for FASTQ files
- **`ov.alignment.STAR`**: RNA-seq alignment using STAR aligner with customizable parameters
- **`ov.alignment.featureCount`**: Gene-level read counting (renamed from `count` to avoid conflicts)
- **`ov.alignment.single`**: One-command scRNA-seq alignment with kb-python (kallisto|bustools)
- **`ov.alignment.ref`**: Build kallisto|bustools reference index for alignment
- **`ov.alignment.count`**: Quantify gene expression from aligned reads

**Key Features**:
- Unified API for both bulk RNA-seq (STAR + featureCount) and scRNA-seq (kb-python) workflows
- Built-in support for RNA velocity analysis with kb-python
- Parallel processing capabilities for faster data conversion
- Automatic handling of paired-end and single-end reads
- Technology-specific filtering for bulk vs single-cell data
- Integration with SRA toolkit for seamless data download

**Example Workflow**:
```python
# Download and process bulk RNA-seq
ov.alignment.prefetch('SRR1234567', output_dir='./data')
ov.alignment.fqdump('SRR1234567', output_dir='./fastq')
ov.alignment.fastp('sample_1.fastq.gz', 'sample_2.fastq.gz', output_prefix='clean')
ov.alignment.STAR(fastq1='clean_1.fastq.gz', fastq2='clean_2.fastq.gz',
                  genome_dir='./genome', output_prefix='aligned')
ov.alignment.featureCount(bam='aligned.bam', annotation='genes.gtf', output='counts.txt')

# Or use one-command scRNA-seq alignment
ov.alignment.single(
    fastq=['read1.fastq.gz', 'read2.fastq.gz'],
    index='./kb_index',
    output_dir='./kb_output',
    technology='10xv3'
)
```

### PP Module
- Fixed an HVG (Highly Variable Genes) selection issue in `ov.pp.preprocess`
- Improved preprocessing pipeline stability and accuracy
- Refactored PCA implementation to utilize `torch_pca` for GPU acceleration (replacing TorchDR)
- Enhanced support for sparse matrices in PCA computation
- Updated PCA embedding basis from `X_pca` to `PCA` for clarity and consistency
- Improved error handling with try-except blocks in PCA computation
- Fixed PCA GPU mode support with sparse matrices to avoid memory errors

### Single Module
- Added `CONCORD` method to `ov.single.batch_correction` for single-cell data integration
- Enhanced batch correction capabilities with state-of-the-art algorithm
- **Fixed critical performance issue in pySCENIC**: Reverted inefficient correlation calculation optimization that caused memory issues and slowdowns in scRNA-seq data
- Removed misleading warnings about dropout genes in SCENIC correlation calculations
- Restored memory-efficient pairwise correlation computation (prevents OOM with >20k genes)
- SCENIC now uses original approach: calculate correlations only for specific TF-target pairs instead of creating full gene×gene matrices
- Added `ov.single.find_markers` for unified marker gene identification supporting five methods: `cosg`, `t-test`, `t-test_overestim_var`, `wilcoxon`, and `logreg`; statistical methods are natively ported from scanpy with no scanpy runtime dependency and numerically consistent results (rtol=1e-4)
- Added `ov.single.get_markers` to extract top marker genes from results as a `DataFrame` or `dict`, with support for single/multiple cluster filtering and optional filtering by `min_logfoldchange`, `min_score`, and `min_pval_adj`; output includes `pct_group` and `pct_rest` columns showing cell expression proportions within and outside each cluster

### Space Module
- Added `FlashDeconv` for fast, GPU-free deconvolution in Visium spatial transcriptomics
- Added `Banksy` clustering method for spatial domain identification
- Updated spatial analysis documentation with new clustering approaches

### Web Module
- Launched `Omicverse-Notebook` for browser-based interactive analysis without local installation
- Launched `Omicverse-Web` for web-based data analysis without coding requirements
- Democratized bioinformatics analysis for researchers without programming background

### Agent Module
- Enhanced `ov.Agent` with improved natural language processing for data analysis
- Expanded LLM provider support and model selection
- Optimized code generation and execution pipeline

### Pl Module
- Enhanced categorical legend handling for scatterplot embeddings
- Added `legend_loc='on data'` option for direct annotation on plots
- Improved visualization clarity for complex datasets
- Added `ov.pl.markers_dotplot` as a cleaner drop-in for `rank_genes_groups_dotplot` with improved defaults (`standard_scale='var'`, `cmap='Spectral_r'`, `dendrogram=False`)
- Fixed `KeyError` in `rank_genes_groups_df` when cluster names are numeric strings (e.g., leiden `'0'`, `'1'`); now correctly handles structured arrays, DataFrames, and plain 2D arrays from all marker methods

### Datasets Module
- Added comprehensive dataset URLs for easier data access
- Expanded data downloading utilities with progress tracking
- **Fixed dataset download to create nested target directories automatically**
- Improved dataset utilities with better error handling
- Refreshed download behaviors for more reliable data fetching

### Docs
- Strengthened data handling documentation in dotplot and DEG analysis tutorials
- Updated the scTour clustering tutorial with latest best practices
- Added comprehensive release notes for v1.7.9
- Enhanced alignment module documentation with end-to-end workflows

### Bug Fixes
- Resolved circular import issues between `_settings` and `utils` modules
- Fixed compatibility issues with latest package versions (zarr, pandas, etc.)
- Improved error handling in parallel processing functions

### Single Module
**Enhanced DEG Analysis with Expression Percentages**: Added cell expression percentage information to differential expression results

- Added `pct_ctrl` column showing percentage of cells expressing each gene in control group (0-100%)
- Added `pct_test` column showing percentage of cells expressing each gene in test group (0-100%)
- Added `pct_diff` column showing the difference in expression percentage (pct_test - pct_ctrl)
- Works with all DEG methods: `wilcoxon`, `t-test`, and `memento-de`
- Enables better marker gene identification by filtering genes based on expression prevalence
- Similar to dotplot circle size information, helps identify genes with widespread vs. sparse expression patterns

**Example Usage**:
```python
deg_obj = ov.single.DEG(adata, condition='condition',
                        ctrl_group='Control', test_group='Treatment')
deg_obj.run(celltype_key='cell_label', celltype_group=['T_cells'])
results = deg_obj.get_results()
# Now includes pct_ctrl, pct_test, pct_diff columns
```

### Compatibility
**NumPy 2.0 Compatibility**: Fixed all NPY201 compatibility issues to ensure seamless support for both NumPy 1.x and 2.x

**Fixed Issues (31 total)**:

1. **`np.in1d` → `np.isin`** (9 instances)
   - `omicverse/bulk/_dynamicTree.py`: 3 instances (lines 697, 741)
   - `omicverse/single/_cosg.py`: 1 instance (line 77)
   - `omicverse/external/GNTD/_preprocessing.py`: 2 instances
   - `omicverse/external/scdiffusion/guided_diffusion/cell_datasets_WOT.py`: 1 instance
   - Other external modules: 2 instances

2. **`np.row_stack` → `np.vstack`** (13 instances)
   - `omicverse/external/CAST/CAST_Projection.py`: 2 instances
   - `omicverse/external/CAST/visualize.py`: 2 instances
   - `omicverse/external/scSLAT/viz/multi_dataset.py`: multiple instances
   - `omicverse/single/_mdic3.py`: 1 instance

3. **`np.product` → `np.prod`** (4 instances)
   - `omicverse/external/umap_pytorch/model.py`: 2 instances
   - `omicverse/external/umap_pytorch/modules.py`: 2 instances

4. **`np.trapz` compatibility wrapper** (2 instances)
   - Added compatibility wrapper in:
     - `omicverse/external/VIA/plotting_via.py`
     - `omicverse/external/VIA/plotting_via_ov.py`
   - Uses `numpy.trapezoid` (NumPy 2.0+) with fallback to `numpy.trapz` (NumPy 1.x)

**Backward Compatibility**:
- ✅ All changes maintain full backward compatibility with NumPy 1.x (1.13+)
- ✅ `np.isin` available since NumPy 1.13
- ✅ `np.vstack` available in all NumPy versions
- ✅ `np.prod` available in all NumPy versions
- ✅ Custom compatibility wrapper handles `trapz`/`trapezoid` transition

## v 1.7.10

### Scope
- This release note summarizes changes from commit `cd3d151` (version set to `1.7.10rc1`) to current `HEAD`.
- Total code delta in this window: `252 files changed`, `+46,992 / -9,752`.

### Agent & Runtime
- Upgraded `ov.Agent` architecture to modern agentic tool-calling workflows with subagent delegation (v4/v5 evolution).
- Improved GPT-5.2 robustness, response parsing, and backend error handling.
- Added harness runtime components for execution contracts, tool catalog, runtime state, tracing, and cleanup policies.
- Strengthened sandbox behavior with restricted import controls for internal modules.
- Added web bridge and session-level execution improvements for agent workflows.

### New Modules
- Added `omicverse.biocontext` for biomedical knowledge queries via BioContext MCP tooling.
- Added `omicverse.fm` (foundation-model adapters, routing, registry, and API).
- Added structured `omicverse.io` namespaces for general/single/bulk/spatial I/O paths.
- Added `omicverse.jarvis` multi-channel bot framework (Feishu/QQ/Telegram) with bridge support.

### Core OmicVerse Improvements
- Continued enhancements across `pp`, `pl`, `single`, `space`, and `utils` modules.
- Fixed circular import between preprocessing utility internals (`_utils.py` and `_scale.py` path).
- Added/updated function-level metadata and documentation quality in key analysis modules (preprocessing, annotation, trajectory, spatial, datasets, bulk).
- Extended dataset utilities with new signature resources and improved loading pathways.

### Registry & Help System
- Improved registry behavior and module import exposure in package entrypoints.
- Enhanced function/class registration metadata coverage for agent discoverability.
- Registry help generation now better aligns with class constructor documentation in class-based tools.

### Web & UI
- Single-cell analysis UI received iterative upgrades:
  - Better code cell management and undo behavior
  - Improved AnnData slot detail retrieval and display
  - Better DataFrame rendering and integration
  - Plot density/point style control refinements
  - i18n and UX polish for analysis panels
- `omicverse_web` service layer expanded with session-oriented agent service support.

### Developer Experience & Testing
- Added FM test suite and multiple harness/ovagent test modules.
- Removed obsolete legacy-priority and complexity-classifier test paths.
- Added workflow and harness documentation pages for runtime contracts and operational guidance.

### Documentation
- Updated and expanded agent architecture and streaming API docs.
- Updated `t_preprocess_cpu.ipynb` to match latest GPU/version detection behavior.
- Added bilingual and deployment-oriented guidance for Jarvis and agent-related workflows.

## v 2.1.x

### Scope
- Summarises every change between `v2.0.0` (tagged 2026-03-18) and the current dev tree (`master` + the in-flight `feat/metabol` and `feat/alignment-16s-amplicon` branches that land in v2.1.x).
- Window stats on `master`: **462 commits**, **429 files changed**, **+98,799 / −17,461 lines**. Plus the two pending feature branches add `ov.metabol` (12 commits) and `ov.micro` + `ov.alignment` (16S amplicon — 5 commits).
- Three top-level themes drove the release:
  1. **New bio modules** — `ov.metabol` (metabolomics), `ov.micro` + `ov.alignment` (16S amplicon → microbiome), `ov.single.Monocle`, `ov.io.read_xenium`, `ov.utils.cluster(method='pymclustR')`, CellSAM, CellCharter, Harmony v0.2, Marsilea heatmaps, CCC plotting, Nanostring spatial, dynamic trajectories, anndataoom OOM Rust backend.
  2. **Spatial-platform support** — Xenium In Situ end-to-end (read + segmentation + viz), Visium HD SpaceRanger v4 round-trip (cellpose + `write_visium_hd_cellseg`), Nanostring CosMx FOV-aware plotting.
  3. **OVAgent / Jarvis runtime overhaul** — ~60 `task-*` commits across PRs #596–#605 (facade slimming, multi-channel migration, P0/P1 security closures, Codex OAuth).

---

### Single-cell trajectory inference

- **`ov.single.Monocle` — pure-Python Monocle 2 reimplementation**: a from-scratch port of the R `monocle2` pipeline (DDRTree, MST, branch-state assignment, BEAM differential expression). No `rpy2`, no R install. Includes:
  - **`method='fast'` DDRTree update** (default): caches `X X.T`, solves in `(K × D)` instead of `(K × N)`, truncates the soft-assignment R to the top-`K/5` entries per row → ~3× faster per iteration with bounded numerical drift. `method='exact'` retained for bitwise R-parity.
  - **Delaunay-based Euclidean MST** in `_project_cells_to_mst` — replaces the O(N²) dense pairwise distance matrix (164 GB for a 143 k-cell atlas in R) with an O(N·d) Delaunay + sparse MST that is provably exact.
  - **Robust HSMM tutorial output** matching the R Monocle 2 reference direction.
  - Pseudotime correlation with R Monocle 2 ≥ 0.99 on every benchmark dataset; 30-100× faster.
  - Also published as a standalone PyPI package (`monocle2-py`) for users who want trajectory inference without the full omicverse stack.
- **Dynamic-trajectory utilities**: new feature-fitting + lineage-aware trend plotting; better Palantir trend visualisation; cleanup of Slingshot debug plots and sctour input stabilisation.

### Spatial omics

#### 10x Xenium In Situ — end-to-end support (PR #629)

- **`ov.io.read_xenium`** — full reader for the standard Xenium `outs/` layout:
  - `cell_feature_matrix.h5` (or `.h5ad`) → `adata.X`
  - `cells.csv.gz` / `cells.parquet` → `adata.obs`, with `x_centroid` / `y_centroid` → `adata.obsm['spatial']`
  - `experiment.xenium` JSON → `adata.uns['spatial'][library_id]['metadata']`
  - Auto-resolves `library_id` from `experiment.xenium` (`region_name` → `run_name`).
  - Exposed as both `ov.io.spatial.read_xenium` and `ov.io.read_xenium`.
  - Verified against the `Xenium_FFPE_Human_Breast_Cancer_Rep1` public sample.
- **`load_boundaries=True`** parameter loads `cell_boundaries.parquet` / `.csv.gz` (Xenium's long-form per-vertex table) into per-cell **WKT POLYGON** strings — sets `uns['omicverse_io']['type'] = 'xenium_seg'` so downstream code (matching `nanostring_seg`) can render cell boundaries directly via `ov.pl.spatialseg`.
- **`cache_file` + smart pyramid-level image loading** — pick the right resolution from the multi-resolution morphology TIFF without loading the full pyramid.
- New tutorial `t_xenium_preprocess.ipynb` showing read → preprocess → spatialseg overlay (verified on KRT7 in the Breast Cancer sample).

#### 10x Atera (WTA Preview) — end-to-end support (PR #700, omicverse-tutorials#30)

- **`ov.io.read_atera`** — reader for the 10x Atera (whole-transcriptome) `outs/` bundle. Atera ships a Xenium-format core (`cell_feature_matrix.h5`, `cells.parquet`, `cell_boundaries.parquet`, `experiment.xenium`) plus four Atera-only additions, all handled by the reader:
  - `nucleus_boundaries.parquet` → `obs['nucleus_geometry']` (WKT POLYGON).
  - `morphology_focus/ch####_<tag>.ome.tif` — content-named multi-stain pyramid TIFFs. Channel selector accepts a semantic tag (`'dapi'` / `'boundary'` / `'rna'` / `'stroma'`), a filename substring (`'cd45'`, `'18s'`), or an integer-as-string index. tifffile's OME multi-file series is bypassed (`is_ome=False`) so each channel's pyramid IFDs are walked standalone.
  - Optional vendor `cell_groups.csv` merge → `obs['cell_group']` and `obs['cell_group_color']`, NaN-preserving for cells absent from the CSV.
  - Optional H&E OME-TIFF + 3×3 affine CSV → `uns['spatial'][lib]['images']['he']` and `scalefactors['he_affine']` / `'he_downsample'`.
  - Verified on the public `WTA_Preview_FFPE_Breast_Cancer` sample (170,057 cells × 18,028 genes after dropping 9,076 control probes/codewords).
- New helpers extracted from the tutorial — `ov.pl.to_rgb_grayscale` (percentile-clipped RGB stack so morphology overlays bypass matplotlib's default viridis colormap), `ov.pl.sync_categorical_palette` (wires a per-cell colour column into `uns[<key>_colors]`), `ov.space.subset_window` (rectangular spatial-window subset preserving `uns`).
- New tutorial `t_atera_preprocess.ipynb` — load the bundle, render the four morphology channels in a 2 × 2 grid, plot the vendor cell-group classifier with `ov.pl.spatial`, render polygon zooms via `ov.pl.spatialseg(img_key=...)` against each of the four channels, run a standard preprocessing → HVG → PCA pipeline, and map canonical breast-cancer markers (KRT8 / PTPRC / COL1A1 / PECAM1).

#### 10x Visium HD — SpaceRanger v4 compat (PRs #620, #622)

- **`ov.io.write_visium_hd_cellseg`** — export cell-level AnnData back to a SpaceRanger v4 directory structure so downstream tools (Loupe Browser, spaceranger-aware pipelines) can consume the cellpose / CellSAM output as if it came straight out of SpaceRanger v4.
- **Cell IDs use the SpaceRanger v4 convention** — `cellid_000000001-1` (zero-padded, suffixed with the slice index) rather than the older spot-id format.
- Image / scalefactors handling simplified; uses existing shapely polygon generation instead of redoing convex hulls.
- Cellpose tutorial rewritten end-to-end with executed outputs (0 errors, 7–16 baked-in figures across iterations) showing both **Cellpose vs CellSAM** segmentation comparison on a 1/16 crop of the HD sample, and the SpaceRanger v4-compatible export round-trip.

#### Nanostring CosMx — FOV-aware plotting

- New `ov.pl.spatial_*` family additions for FOV-aware plotting (multi-FOV layout, per-FOV background image overlay, rasterisation options for very dense slides).
- FOV image processing pipeline picks up cropping / rasterisation hints from `uns`.

#### Cell segmentation backends

- **CellSAM backend** added (alongside the existing Cellpose backend). Uses cropped images for the standard 10x HD flow.
- **`stardist()` → `cellseg()` rename** with backward-compatible alias — clearer name now that there are multiple backends behind it.

#### Other spatial features

- **CellCharter integration**: new `method='cellcharter'` in `ov.utils.cluster` plus enhanced `spatial_neighbors` graph construction. Includes AutoK export, Banksy Jupyter compat, and pickle cross-version loading fixes.
- **`ov.pl.create_custom_colormap`**: generic palette helper, registered for agent discoverability.
- **Spatial-segmentation overlay fixes**: cmap alpha now honoured in `outline_only`; FOV image processing supports rasterization options.
- **Spatial background image scaling**: fixed bug where the H&E background was rendered tiny (coords were not scaled). Affected all `sc.pl.spatial`-style overlays.
- **Starfysh tutorial compatibility** restored against modern numpy/pandas/scipy/pytorch (also pins `s3fs ≥ 2023.1.0` to avoid Python 3.12 build failures).

### Preprocessing & QC

- **`ov.pp.qc(adata, doublets='pydoubletfinder')` — pure-Python DoubletFinder backend** alongside the existing `scrublet` backend. No R install needed; matches the R `DoubletFinder` package within published-tutorial AUC range.
- **Auto-detect mitochondrial gene prefix** in `pp.qc` — no more hand-setting `'mt-'` vs `'MT-'` per species. Explicit override still respected.
- **Harmony upgrade to upstream `harmonypy v0.2.0`** with three backends:
  - **GPU**: existing PyTorch path (unchanged).
  - **CPU NumPy**: pure-NumPy fallback for environments without torch/MLX.
  - **MLX**: native Apple-Silicon (MPS) backend rewritten to use pure MLX operations (no numpy round-trip).
  Restored emoji/colour/tqdm output, `n_init=1` to match upstream, and reproducibility seeds. Multiple review rounds for MLX correctness (lambda double-insert, slice-assignment crash, dead `self._W`).
- **`torch_pca` sparse + `covariance_eigh` fallback** with dynamic memory limits — high-density sparse matrices now convert to dense before CPU PCA (instead of OOM-ing); float64 estimate, OSError handling, and dedup'd memory/threshold constants.
- **`scale()` default**: `to_sparse=False` (no surprise sparse → dense round trips).
- **Removed**: `ov.pp.scrublet` legacy module (use `ov.pp.qc(doublets='scrublet')` or `'pydoubletfinder'`).

### I/O & out-of-memory backend

- **`anndataoom` Rust backend** (optional, opt-in): out-of-memory AnnData reads via Rust. New helper `omicverse.utils.convert_adata_for_rust` and a dedicated `t_preprocess_rust` tutorial. Multiple review rounds (1st through 7th) for stability, lazy-loading semantics, and clear error paths (`no_cc=True` is now refused on the OOM backend; unsorted CSR h5ad gets a precise diagnostic; spatial viz works on lazy AnnData).
- **`ov.io.read_xenium`** added (also covered above under Spatial).
- **`ov.read` docstring** refreshed for the Rust backend's behaviour.

### Plotting

- **Marsilea-based heatmap plotting APIs** (new family): clean, declarative heatmaps with regression coverage in the test suite.
- **Cell-cell communication (CCC) plotting APIs** (`ov.pl.ccc_*`): arrow / sigmoid / flow / scatter / chord-style ligand-receptor plots, with empty-interaction-palette guards and refined flow layouts. Aligned with the CellPhoneDB registry metadata.
- **`ov.pl.create_custom_colormap`** with white-ramp duplicate de-duplication.
- **Half-violin boxplot function** introduced; old equivalent deprecated.
- Subset plotting now drops unused categories so legends are accurate; legendkit `show_at` accepts 0–1 percentiles (not raw data values).
- Iterative refactor of plotting imports (lazy loading, optional torch dependency handling, deprecated old utilities in favour of the new embedding helpers).

### `ov.utils.cluster` — `pymclustR` backend (PR #638)

- New `method='pymclustR'`: pure-Python re-implementation of CRAN `mclust` covering all 14 Banfield-Raftery / Celeux-Govaert covariance parameterisations. Drop-in replacement for the legacy `'mclust_R'` rpy2 backend, which is now removed (calling it raises a `ValueError` pointing at the replacement).
- Validation against CRAN `mclust 6.1.1` across 222 records: 12 of 14 models bitwise-identical, overall mean z-correlation 0.9935.
- Published as `pymclustR` on PyPI.

### Datasets & utilities

- **Gene ID conversion** functions added to `ov.utils` (with conflict-column handling on merge), plus a database-validation helper.
- **Function search** uses a global registry fallback for better discoverability across modules.
- Removed `pymde` dependency; tightened scipy pin and FOV image processing.
- Removed deprecated data files; cleaned up `biocontext` module exports.

### `ov.Agent` / Jarvis / OVAgent runtime

A multi-month decomposition + hardening of the agent runtime stack. ~60 numbered `task-*` commits across PRs **#596 (codex OAuth)**, **#600 (runtime upgrade)**, **#601 (decomposition follow-up)**, **#602 (PR-602 reviewer follow-ups)**, **#603 (security + runtime hardening)**, **#604/#605 (orchestration waves 3 & 4)**.

Highlights:

- **Smart-agent facade slimming**: `smart_agent.py` collapsed; bootstrap, auth, runtime setup, codegen/review/reflection pipeline, session/context/history services, and tool facade extracted into focused modules.
- **OVAgent runtime decomposition**: `analysis_executor.py`, `tool_runtime.py`, `agent_backend.py`, `turn_controller.py` each split into transformer/diagnostic/sandbox/handler helpers.
- **Tool dispatch facade collapse**: the `~45-wrapper` `CodegenToolDispatchFacadeMixin` reduced to 3 concrete delegations.
- **Subagent infrastructure**: configurable subagent profile schema, override plumbing through runtime bootstrap, and end-to-end coverage.
- **Jarvis multi-channel migration onto a single `MessageRuntime`**: Discord, Telegram, QQ, WeChat, Feishu, iMessage all now use the shared runtime / presenter / command / media abstractions. Channel-core session/request abstractions were also extracted (`channel_media`).
- **Tool runtime hardening**: bounded sync bridge, fail-closed bash roots, explicit stdout guard, sandbox runtime enforcement, `pandas.eval` classification, repair-loop retry boundedness, LLM timeout, and dependency-safe parallel tool scheduler.
- **Security closures (P0/P1 from PR #601 review)**: `SafeOsProxy` metadata escape closed via allowlist, `strip_local_paths` ReDoS-hardened, URL substring assertions replaced with parsed-hostname validation (CodeQL clean), CodeQL sensitive-data alerts cleared in real-provider E2E test, session-facade lock-test portability fixed.
- **Backend hardening**: Gemini and OpenAI adapter exception handling, credential resolution + factory consolidation, context budget model-window registry sync, bounded silent-fallback debug logging.
- **Web bridge & sessions**: prior-history retrieval per session, `.h5ad` channel handling, AgentBridge ↔ messaging-channel reply-text plumbing, shared kernel + AnnData support.
- **Codex OAuth** support added to `ov.Agent` (PR #596).
- **CLI / install**: `omicclaw` entrypoint replaces `omicverseweb`; install.sh rewritten as a guided installer with optional package menus (web, Jarvis, full bio suite); MCP startup-timeout troubleshooting documented for Windows.

### Documentation & infrastructure

- **Sphinx + Furo migration** (later switched to **`sphinx_book_theme`**): the docs site moved from MkDocs to Sphinx. Bilingual `docs/` + `docs_zh/` checkouts, `.readthedocs.yaml` config with repo-root-relative paths, deploy-docs CI workflow migrated, gh-pages history accumulation prevented. Pinned `Pygments < 2.20`.
- **Multi-Omics docs reorganisation**: `Tutorials-bulk2single/` folder moved under `Tutorials-Multi-Omics/bulk-single/` with an overview page, in line with how *Multi-Omics* is now framed as a top-level domain alongside Bulk / Single / Spatial.
- **Spatial-clustering tutorials**: original combined `t_cluster_space.ipynb` split into 5 self-contained per-method notebooks under `docs/Tutorials-space/cluster/` (GraphST, BINARY, STAGATE, CAST, BANKSY), all clustered with `method='pymclustR'` (no rpy2). New parent `cluster/index.md` with embedder paper DOIs and a recommendation table.
- **Cellpose tutorial** rewritten with executed CellSAM vs Cellpose comparison and SpaceRanger v4-compatible export.
- **CCC plotting** API docstrings expanded; OmicVerse Agent skill guidance updated for CellPhoneDB.
- **Dependencies**: pinned `s3fs ≥ 2023.1.0` (Python 3.12), updated scipy, removed `pymde`, removed `socksio` from default deps.
- **CI**: dev PRs now run package + MCP workflows; flake8 excludes virtualenvs; lint regressions cleaned up across namespace exports and bootstrap tests.

### `ov.metabol` — new metabolomics module (PR #636, branch `feat/metabol`)

A from-scratch metabolomics analysis namespace mirroring the structure of `ov.bulk` and `ov.single`. Twelve commits, several shipped sub-releases (v0.1 → v0.3).

**v0.1 — base**
- `ov.metabol` namespace registered; LC-MS reader; vendored `gseapy` for environments without it.
- `ID mapping` between HMDB / KEGG / LIPID MAPS / PubChem / ChEBI identifiers.
- Lipidomics class-level summarisation.

**v0.2 — pathway analysis**
- `pyMSEA` (metabolite set enrichment) with KEGG / LION / HMDB pathway sources.
- `pyMummichog` (peak-list-based pathway inference for unannotated LC-MS features).
- `pathway_bar`, `pathway_dot` plots; `volcano` gains `use_pvalue` + `clip_log2fc` options.

**v0.3 — multi-factor + biomarker**
- **SERRF** — QC-RF drift correction for batch / acquisition-order systematic bias.
- **DGCA** — differential gene/metabolite co-correlation analysis.
- **ASCA** + **MixedLM** — multi-factor analysis (e.g. treatment × time, repeated measures).
- **ROC / biomarker panel** — single + multi-feature ROC, AUC bootstrap CIs, panel selection.

**Cross-cutting**
- Every public API registered with `@register_function` so `ov.Agent` can dispatch metabolomics workflows.
- **Lazy-loaded submodules** — top-level `import omicverse` cost cut 3200× by deferring metabol's heavy R-style stats imports until first call.
- **Fetcher-based data migration** — KEGG / LION / HMDB pathway tables fetched on demand instead of shipped (drops 3 data files from the wheel).

### `ov.micro` + `ov.alignment` — microbiome / 16S amplicon (PR #637, branch `feat/alignment-16s-amplicon`)

End-to-end **16S rRNA amplicon → microbiome AnnData** pipeline.

**`ov.alignment` — upstream sequence processing**
- `cutadapt` primer trimming + `vsearch` UNOISE3 ASV calling + `SINTAX` taxonomic classification.
- **Phylogeny step** — multiple sequence alignment via `MAFFT` + tree construction via `FastTree`, attached to the AnnData via `ov.micro.attach_tree(adata, tree_path)`.

**`ov.micro` — downstream microbiome analysis**
- New downstream namespace covering alpha / beta diversity, differential abundance, ordination, taxonomic-level summaries.
- Compatible with `scikit-bio 0.6` (PR #637 round-2 review fix bumps from the deprecated 0.5 API for the phylogenetic metrics).
- Class names follow the no-`py`-prefix convention (e.g. `MicroBiome`, `Diversity`).

### Removed / deprecated

- `ov.pp.scrublet` legacy module.
- `ov.utils.cluster(method='mclust_R')` (rpy2 bridge) — replaced by `'pymclustR'`.
- Old plotting utilities deprecated in favour of new embedding helpers + `half_violin_boxplot`.
- `pymde` runtime dependency.
- `omicverse_web` Git submodule (functionality folded into `omicclaw`).
- Legacy ReadTheDocs MkDocs config.
- Three shipped metabolomics data files (KEGG / LION / HMDB pathway subsets) — now fetched on demand.

## v 2.2.0

### Scope
- Summarises every change between `v2.1.2` and the `v2.2.0` release tip: **208 commits**, **212 files changed**, **+34,878 / −8,888 lines**, ~50 merged PRs (#652 → #727).
- Three top-level themes drove this release:
  1. **New analysis modules** — `ov.es` (vendored decoupler kernels with GPU acceleration), `ov.single.NMF` (Rust-backed), `ov.single.CNV` (copykat / infercnv), Geneformer in-silico perturbation, `ov.pp.champ`, `ov.report` (one-call HTML provenance report), `ov.space.RCTD`, `ov.space.nmf_tissue_zones`.
  2. **GPU-first preprocessing** — pure-PyTorch Leiden (74×), full-GPU parametric UMAP (21×), GPU KNN by default in `pp.neighbors`, native torch t-SNE, plus a ~20-method GPU sweep in `ov.es` (gsva 23–28×, mdt/udt 83–158×, viper 20×, gsea 13–16×, ora 48×).
  3. **Maturation of v2.1.x modules** — Atera (WTA Preview) reader, Xenium V2 / Prime morphology fix, paired microbe↔metabolite + cross-cohort 16S meta-analysis in `ov.micro`, MTBLS1 case study + plot helpers in `ov.metabol`, Seurat-style CCA in `single.batch_correction`, scMulan / MetaTiME / TOSICA in `single.Annotation`, CellVote consensus.

---

### `ov.es` — vendored decoupler kernels with GPU acceleration (PR #722)

A new top-level enrichment-scoring namespace, vendoring the decoupler 1.x algorithms behind a clean `omicverse` API and rewriting every method with an optional torch/GPU kernel.

- **`ov.es.decoupler` unified dispatcher** registered with `@register_function` — single entry point that picks the right backend by method name.
- **GPU kernels for 10 methods**: `aucell`, `ulm`, `zscore`, `mlm`, `waggr` (first wave), then `gsea`, `ora`, `gsva`, `viper`, `mdt`/`udt`. Speedups vs the CPU decoupler reference, on the same matrix:
  - `aucell`: 0.2× → 7.5× after kernel redesign (bit-exact vs CPU).
  - `gsea`: 13–16× via batched cumsum ES.
  - `ora`: 48× via batched hypergeom on torch.
  - `gsva`: 23–28× across the three pipeline stages.
  - `mdt` / `udt`: 83× / 158× via pure-torch GBDT, dropping the xgboost CPU path.
  - `viper`: 20× on aREA, 4× full pipeline.
- **GPU-side sparse densify** (2–3× across the board), math approximations + loop vectorisation, and GPU memory pattern aligned with `ov.pp._pca` (drops per-call cleanup overhead).
- `waggr` GPU dispatcher densifies before CPU fallback to avoid hidden round-trips.
- Method dispatch lifted into each method (no `MethodMeta` facade); decoupler's `_docs` / `_log` infrastructure stripped.
- Legacy `ov.single.aucell` helpers still work but print a migration notice to `ov.es.aucell`.
- pytest smoke coverage for all 11 scoring methods.
- **Tutorial**: [t_es_compare](Tutorials-single/enrichment/t_es_compare.ipynb) — side-by-side comparison of all 11 enrichment methods on the same matrix.

### Single-cell analysis

- **`ov.single.NMF` — Rust-backed fast NMF (PR #717)** via `nmf-rs`. Auto-K selection via stability-drop heuristic and Brunet K-selection with a consensus heatmap; consensus switched from cell-level to spectra-level for stability. Adds per-factor `obs` columns and drops empty categories cleanly. *Tutorial:* uses the cNMF workflow ([t_cnmf](Tutorials-single/t_cnmf.ipynb)) as its reference pipeline.
- **`ov.single.CNV` + `ov.pl.cnv_*` (PR #723)** — single-cell CNV inference covering both copykat and infercnv backends. Plotting uses a **marsilea backend** for `cnv_heatmap` with multi-strip annotations; split between `groupby` (ordering) and `annotations` (overlay) for layering. *Tutorials:* [t_copykat](Tutorials-single/t_copykat.ipynb), [t_infercnv](Tutorials-single/t_infercnv.ipynb).
- **`ov.single.Annotation` — scMulan / MetaTiME / TOSICA backends (PRs #719, #720)**:
  - scMulan added to `Annotation.annotate` (modern transformers compat) — *tutorial:* [t_scmulan](Tutorials-single/anno-zoo/t_scmulan.ipynb).
  - MetaTiME and TOSICA wired into the same dispatcher — *tutorials:* [t_metatime](Tutorials-single/anno-zoo/t_metatime.ipynb), [t_tosica](Tutorials-single/anno-zoo/t_tosica.ipynb).
  - **CellVote consensus score** — confidence-aware multi-annotator consensus (PR #719). *Tutorial:* [t_cellvote](Tutorials-single/t_cellvote.ipynb).
- **`ov.single.batch_correction` — Seurat-style CCA (PR #670, #669)** — drop-in CCA backend alongside the existing methods; 3 review bug-fixes + UX improvements landed in the same PR (PR #670 review feedback). *Tutorial:* [t_single_batch](Tutorials-single/t_single_batch.ipynb).
- **`ov.single.auto_resolution` — null-adjusted (PR #662)**, per Lange et al. 2004. Renamed from `autoResolution`, with a selection-curve plot helper and a new `method='champ'` backend. *Tutorial:* covered in [t_cluster](Tutorials-single/t_cluster.ipynb).
- **`ov.single.cal_grn` fix (#681)** — passes `gene_names` to `grnboost2` / `genie3` so the resulting GRN keeps the real gene labels. *Tutorial:* [t_scenic](Tutorials-single/t_scenic.ipynb).
- **SCLLMManager is now the canonical foundation-model entry (PR #704)** — `ov.fm` namespace dropped entirely; SCLLM is the single FM surface. Defensive HVG warning + actionable RegDiffusion OOM error in `single/SCENIC`. *Tutorials:* [t_scgpt](Tutorials-llm/t_scgpt.ipynb), [t_scfoundation](Tutorials-llm/t_scfoundation.ipynb), [t_cellplm](Tutorials-llm/t_cellplm.ipynb), [t_uce](Tutorials-llm/t_uce.ipynb).

### Geneformer in-silico perturbation (PRs #725, #726)

- **`ov.llm` Geneformer perturbation** — in-silico knockout / knock-in via embedding shifts in the Geneformer foundation model.
- **TF-perturbation per-gene downstream-shift analysis (PR #726)** — quantifies how each downstream gene shifts in embedding space after a TF perturbation.
- New `ov.pl` helpers for the perturbation result tables.
- **Tutorial**: [t_geneformer](Tutorials-llm/t_geneformer.ipynb) — shipped end-to-end with executed outputs.

### Preprocessing & GPU performance

- **Pure-torch GPU Leiden (PR #657)** — `ov.pp.leiden(method='torch')` is **74× faster** than the CPU reference and has **no `torch_sparse` / `torch_scatter` dependency** (one of the most fragile installs in the stack). Pure tensor ops only.
- **Full-GPU parametric UMAP (PR #652)** — pumap path is **21× faster** with bounded VRAM; batch size bumped to 16384 across the board.
- **GPU KNN by default for `method='torch'` (PR #654)** in `ov.pp.neighbors`, with the correct fuzzy simplicial graph (matches the UMAP reference, not an approximation).
- **Native torch t-SNE + louvain auto-redirect (PR #658)** — mixed-mode polish so the GPU path is the default when torch is available.
- **`ov.pp.tsne`** routes directly to sklearn (drops `sc.tl.tsne`) — fixes a stale `n_components` forwarding bug (#683).
- **`ov.pp.qc(doublets=…)` default** is now **`scdblfinder`** for CPU and mixed modes (PR #655).
- **`ov.pp.champ` — Convex Hull of Admissible Modularity Partitions (PR #666)** — new resolution-stability backend with `n_seeds`, `modularity='cpm'`, adaptive refinement, three `width_metric` modes (`log`/`linear`/`relative`), and NaN-safe gamma clamping. Wired into `auto_resolution` as `method='champ'` with a landscape plot. *Tutorial:* [t_cluster](Tutorials-single/t_cluster.ipynb).
- **GPU preprocessing tutorials**: [t_preprocess_gpu](Tutorials-single/t_preprocess_gpu.ipynb) (Leiden / UMAP / KNN GPU path), [t_preprocess_cpu](Tutorials-single/t_preprocess_cpu.ipynb) (CPU baseline with the new defaults).

### Spatial omics

- **`ov.space.RCTD` deconvolution backend (PR #710, issue #682)** — RCTD added alongside the existing spatial deconvolution backends. Full-slide tutorial with executed outputs; reference dataset shipped as `ov.datasets.visium_lymph_node`. *Tutorial:* [t_decov_rctd](Tutorials-space/t_decov_rctd.ipynb).
- **`ov.space.nmf_tissue_zones` (PR #673)** — NMF colocation over spot abundance matrices, with `normalize='rows'` option and DataFrame-column inference. Prefers `uns` factor names and strips shared prefixes for cleaner zone labels. *Tutorial:* [t_decov](Tutorials-space/t_decov.ipynb) Step 6.
- **`ov.io.read_atera` (PR #700)** — full reader for the 10x Atera (WTA Preview) bundle (Xenium-format core + nucleus boundaries + multi-stain morphology + optional H&E + vendor `cell_groups.csv`). See the dedicated section under "I/O" below. *Tutorial:* [t_atera_preprocess](Tutorials-space/t_atera_preprocess.ipynb).
- **`ov.io.read_xenium` V2 / Prime fix (PR #716, issue #708)** — Xenium V2 / Prime data ships `morphology_focus/morphology_focus_NNNN.ome.tif` per stain channel; the OME-XML cross-references between siblings made tifffile's default `_multifile=True` silently merge them and break the pyramid walk, producing `[Xenium] No morphology image loaded`. The fix walks each per-channel pyramid standalone with `_multifile=False` and prioritises the user-requested channel. Verified on Xenium Prime FFPE Human Prostate (5,006 genes / 193K cells) — all four channels now load. *Tutorial:* [t_xenium_preprocess](Tutorials-space/t_xenium_preprocess.ipynb).
- New helpers extracted from the Atera tutorial — `ov.pl.to_rgb_grayscale`, `ov.pl.sync_categorical_palette`, `ov.space.subset_window`.
- **`ov.pl.spatial`** — `frameon=False` now truly hides the frame (matches scanpy).

### Microbiome & Metabolomics

#### `ov.micro` — paired microbe ↔ metabolite + meta-analysis

- **Paired microbe↔metabolite integration (PR #664)** — new `simulate_paired`, `paired_spearman`, `paired_cca`, and **MMvec** for unpaired co-occurrence inference, with companion plotting helpers. *Tutorial:* [t_micro_metabol_paired](Tutorials-Multi-Omics/micro-meta/t_micro_metabol_paired.ipynb).
- **Cross-cohort 16S meta-analysis (PR #663)** — `combine_studies` + `meta_da` for proper between-study differential abundance, handling per-study confounders. *Tutorials:* [t_16s_meta_analysis](Tutorials-microbiome/t_16s_meta_analysis.ipynb), [t_16s_da_comparison](Tutorials-microbiome/t_16s_da_comparison.ipynb).
- **`fetch_franzosa_ibd_2019` (PR #664)** — first built-in real paired multi-omics dataset; the paired tutorial was rewritten end-to-end against it.

#### `ov.metabol` — MTBLS1 case study (PRs #665)

- **MTBLS1 case-study helpers + 4 plot helpers** for the MetaboLights MTBLS1 benchmark.
- **v0.5 perf/usability fixes** discovered during the MTBLS1 smoke-test rollout.
- **Tutorial**: [t_metabol_11_real_data_mtbls1](Tutorials-metabol/t_metabol_11_real_data_mtbls1.ipynb).

### `ov.report` — one-call HTML pipeline report from AnnData provenance (PRs #659, #660)

- **`ov.report` — one-call HTML pipeline report** generated from AnnData provenance.
- **`@tracked` decorator** consolidates timing / nesting / record-call concerns into a single annotation.
- Extends to **`ov.single.batch_correction`, `ov.single.Annotation`, `ov.single.AnnotationRef`** (PR #660) — class-method tracking, not just function tracking.
- **Developer guide**: see the *"Making a dispatcher appear in `ov.report.from_anndata`"* section of [Developer_guild](Developer_guild.md) for how to wire your own dispatcher into the report.

### Plotting

- **`ov.pl.plot1cell` — circular UMAP with concentric metadata tracks (PRs #674, #675, #676, #679)**: new circular embedding plot with `bending.inside` labels, axis ticks, per-track palettes, and **horizontal outer-ring labels with wrap + repel**. Respects `plot_set` background (no hardcoded figure background). Registered in Sphinx toctrees with a 4-scale tutorial slimmed to 2 real datasets. *Tutorial:* [t_plot1cell](Tutorials-plotting/t_plot1cell.ipynb).
- **`ov.pl.embedding` flow layout (PR #719)** — flow layout is now the **default** for multi-panel embedding plots (replaces the grid layout). Multiple polish fixes:
  - Flow layout accounts for default colorbar + title in panel footprint.
  - Colorbar width halved (fraction 0.08 → 0.04); slim inset colorbar default that reclaims unused figure width.
  - `_flow_layout_panels` measures axis & colorbar tightbboxes so layout is colorbar-aware.
  - `inset_axes` colorbar registered so flow layout measures its tightbbox correctly.
- **`ov.pl.ccc_*` — unified communication adapters for LIANA and CellPhoneDB (PR #666 area)** — single adapter layer so `ccc_circle`, `ccc_heatmap`, `ccc_network_plot`, `ccc_stat_plot` work against either source. Empty-interaction palettes guarded. Volcano fix (#712) for non-standard significance column values. *Tutorials:* [t_ccc_cellphonedb](Tutorials-single/t_ccc_cellphonedb.ipynb), [t_ccc_liana](Tutorials-single/t_ccc_liana.ipynb).
- **`ov.pl.trajectory` (PR #707)** — generic trajectory plotting backend with a robust label assertion in tests.
- **`ov.pl.cnv_*`** — see `ov.single.CNV` above for the marsilea backend.
- **Dynamic heatmap fixes** — preserve explicit `feature_labels`; preserve dynamic annotations through layout.
- **WGCNA color assignment refactor (PR #684)** — community contribution from @libmelo.

### I/O

- **`ov.io.read_atera` (PR #700)** — full reader for 10x Atera (WTA Preview) `outs/`. Atera ships a Xenium-format core (`cell_feature_matrix.h5`, `cells.parquet`, `cell_boundaries.parquet`, `experiment.xenium`) plus four Atera-only additions, all handled by the reader:
  - `nucleus_boundaries.parquet` → `obs['nucleus_geometry']` (WKT POLYGON).
  - `morphology_focus/ch####_<tag>.ome.tif` — content-named multi-stain pyramid TIFFs. Channel selector accepts a semantic tag (`'dapi'` / `'boundary'` / `'rna'` / `'stroma'`), a filename substring (`'cd45'`, `'18s'`), or an integer-as-string index. tifffile's OME multi-file series is bypassed (`is_ome=False`) so each channel's pyramid IFDs are walked standalone.
  - Optional vendor `cell_groups.csv` merge → `obs['cell_group']` and `obs['cell_group_color']`, NaN-preserving for cells absent from the CSV.
  - Optional H&E OME-TIFF + 3×3 affine CSV → `uns['spatial'][lib]['images']['he']` and `scalefactors['he_affine']` / `'he_downsample'`.
  - Verified on the public `WTA_Preview_FFPE_Breast_Cancer` sample (170,057 cells × 18,028 genes after dropping 9,076 control probes / codewords).
  - *Tutorial*: [t_atera_preprocess](Tutorials-space/t_atera_preprocess.ipynb).
- **`ov.io.read_csv` (latest)** — now flags pandas's silent duplicate-column rename (`col`, `col.1`, `col.2`, …) instead of letting it pass through unnoticed.
- **`ov.io.read_xenium` V2 / Prime fix** — see Spatial.

### Datasets & utilities

- **`ov.datasets.visium_lymph_node`** loader — first-class reference dataset for the [RCTD tutorial](Tutorials-space/t_decov_rctd.ipynb).
- **`ov.utils.preflight_alignment` (latest)** — sample-metadata alignment pre-flight helper; checks that the `obs` table you're about to merge will actually align with the AnnData index before you do it. Registered with the function registry.
- **`ov.bulk` — `pyWGCNA` / `readWGCNA` registry-discoverable shim (PR #700)** so the WGCNA path is discoverable from `ov.Agent` without importing the heavy backend at top level.

### OVAgent / Jarvis / registry

- **`registry_lookup` improvements (PR #691)**:
  - Shows docstrings + visual dividers in `registry_lookup` output (was a bare table before).
  - `_registry` includes keyword-only args in AST-derived signatures (was previously dropping them).
  - Caches `RegistryScanner` + skill registry across calls (perf win on long agent sessions).
- **`@register_function` backfill on docstring-backfilled APIs (PR #695)** — every metabol / micro / single API whose docstring was filled in from omicverse-skills 0.3.0 grounding is now registry-discoverable.
- **OVAgent resilience + live LLM trace + auto-download (PR #688)** — better recovery on transient backend failures, live trace of the LLM call as it streams, and auto-download of small dependencies on first use.
- **Hardcoded user-specific paths removed (PR #689)** — `possible_paths` fallback lists deleted in favour of explicit configuration.
- **`omicverse-skills` bumped to >=0.3.0 (PR #696)** to pick up the v0.3 docstring corpus.

### Bug fixes

- **#706** — `ov.pp.preprocess(mode='shiftlog|seurat')` no longer raises `UnboundLocalError` (PR #709).
- **#683** — `ov.pp.tsne` no longer forwards `n_components` to the scanpy backend (PR #698).
- **#685** — bulk/single enrichment `logp` now matches the `−log10` colour-bar label (PR #697).
- **#681** — SCENIC `cal_grn` passes `gene_names` to `grnboost2` / `genie3` (PR #699).
- **#708** — Xenium V2 / Prime `morphology_focus_NNNN.ome.tif` channels load correctly (PR #716).
- **#612** — `bulk2single/bayesprism`: `ThetaPost` columns are cell types, not genes (PR #672).
- **#712** — volcano misclassifies significant genes when `sig` column uses non-standard values (community PR).
- **bulk2single TAPE (PR #724)** — high-res mode now exposes signature matrices via `self.signature_matrix`.
- **CCC circle (latest)** — circle aggregation now aligns with significant interactions (community PR #715).
- **MOFA** — raw regex for factor parsing.
- **GPU connectivity device** — lazily resolved (no spurious CUDA imports).

### Removed / deprecated

- **`ov.fm` namespace dropped** — use `SCLLMManager` as the canonical foundation-model entry (PR #704). The `tests/fm/` directory was removed; architecture tests were updated to pin the bulk lazy route through `_wgcna` instead of `_Gene_module`.
- **`xgboost` CPU path for `ov.es.mdt` / `ov.es.udt`** — replaced by the pure-torch GBDT (83× / 158× faster).
- **`possible_paths` hardcoded fallback lists** — removed in favour of explicit configuration.

