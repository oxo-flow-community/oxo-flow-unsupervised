# oxo-flow-unsupervised

[![CI](https://github.com/oxo-flow-community/oxo-flow-unsupervised/actions/workflows/ci.yml/badge.svg)](https://github.com/oxo-flow-community/oxo-flow-unsupervised/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

Unsupervised analyses of omics matrices: PCA, UMAP/densMAP embeddings,
hierarchical clustering heatmaps, Leiden clustering, clustree analysis,
external/internal cluster validation with TOPSIS ranking, and static and
interactive visualizations. Port of the default execution path of
[epigen/unsupervised_analysis](https://github.com/epigen/unsupervised_analysis)
(Snakemake).

## Source

Ported from **[epigen/unsupervised_analysis](https://github.com/epigen/unsupervised_analysis)**,
version `v4.0.2` (MIT), commit
`4da72e9e8792ecdfa474a67c17b3f9b564eb462e`. This port is maintained
independently and **may lag the upstream** — check the fidelity table below
for the exact ported state.

## Quick start

```bash
# validate, lint, and dry-run the workflow
./test/run.sh

# run everything (all 52 rules for sample "digits")
oxo-flow run main.oxoflow
```

Default inputs are real sklearn `digits` data (1797 samples x 64 features)
committed under `test/fixtures/`. The annotation file `config/annotation.csv`
maps each sample to its matrix and metadata file; the upstream annotation
columns `data`/`metadata` map to the port convention
`{config.data_dir}/{sample}_data.csv` and `{config.data_dir}/{sample}_labels.csv`.

## Configuration

All upstream defaults are set in `[config]` in `main.oxoflow` and can be
overridden with `oxo-flow run main.oxoflow -c key=value` (or a config file):

| Key | Default | Upstream equivalent |
|---|---|---|
| `threads` / `mem_mb` | `2` / `32000` | `threads` / `mem` |
| `project_name` | `digits` | `project_name` |
| `data_dir` | `test/fixtures` | annotation `data`/`metadata` columns |
| `pca_svd_solver` / `pca_n_components` | `auto` / `0.9` | `pca.svd_solver` / `pca.n_components` |
| `umap_metric` / `umap_n_neighbors` / `umap_min_dist` | `euclidean` / `15` / `0.1` | `umap.metrics[0]` / `umap.n_neighbors[0]` / `umap.min_dist[0]` |
| `umap_densmap` / `umap_connectivity` / `umap_diagnostics` | `1` / `1` / `1` | `umap.densmap` / `umap.connectivity` / `umap.diagnostics` |
| `heatmap_hclust_method` / `heatmap_n_observations` / `heatmap_n_features` | `complete` / `1` / `0.5` | `heatmap.hclust_methods[0]` / `heatmap.n_observations` / `heatmap.n_features` |
| `leiden_metric` / `leiden_n_neighbors` / `leiden_n_iterations` | `euclidean` / `15` / `2` | `leiden.metrics[0]` / `leiden.n_neighbors[0]` / `leiden.n_iterations` |
| `clustree_*` | `0` / `0.1` / `tree` / `majority` / `mean` | `clustree.*` |
| `sample_proportion` | `1` | `sample_proportion` |
| `metadata_of_interest` | `["target"]` | `metadata_of_interest` |
| `features_to_plot` | `[]` | `features_to_plot` |
| `coord_fixed` / `scatterplot2d_size` / `scatterplot2d_alpha` | `0` / `1` / `1` | `coord_fixed` / `scatterplot2d.size` / `scatterplot2d.alpha` |

## Outputs

All outputs are written below `results/unsupervised_analysis/{sample}/`:

| Directory | Content |
|---|---|
| `PCA/` | PCA object, transformed data, loadings, variance, axes, diagnostics and metadata/clustering/interactive plots |
| `UMAP/`, `densMAP/` | embedding objects, data, axes, diagnostics, connectivity, metadata/clustering/interactive plots |
| `Heatmap/` | observation/feature distance matrices and heatmap PNGs |
| `Leiden/` | per-parameter clustering CSVs and aggregated `Leiden_clusterings.csv` |
| `clustree/` | clustree PNGs (default, custom) and per-metadata plots |
| `cluster_validation/` | external/internal index CSVs, TOPSIS-ranked internal indices, index heatmaps |
| `metadata_features.csv`, `metadata_clusterings.csv` | aggregated per-sample tables |
| `configs/` | exported annotation file |

## Fidelity

Upstream rules and how each is ported (52 ported rules; every analysis step
of the default-parameter path is executed, none are stubbed):

| Upstream rule | Port | Notes |
|---|---|---|
| `pca` | `pca` | same script; snakemake object replaced by CLI args |
| `umap_graph` | `umap_graph` | knn-graph for the default metric/neighbors |
| `umap_embed` | `umap_embed_2d`, `umap_embed_3d` | parameter-list fan-out (n_components 2/3) becomes explicit rules |
| `densmap_embed` | `densmap_embed_2d`, `densmap_embed_3d` | same fan-out |
| `distance_matrix` | `distance_matrix_{observations,features}_{correlation,cosine}` (4) | wildcard fan-out ({type} x {metric}) becomes explicit rules |
| `prep_feature_plot` | `prep_feature_plot` | runs always (upstream always computes it) |
| `leiden_cluster` | `leiden_RBConfigurationVertexPartition_{0.5,1,1.5,2,4}`, `leiden_ModularityVertexPartition_NA` (6) | partition_types x resolutions fan-out becomes explicit rules; graph always taken from the precomputed UMAP knn-graph |
| `aggregate_clustering_results` | `aggregate_clustering_results` | upstream `run:` block ported to `scripts/aggregate_clustering.py` (input[0] metadata unused upstream, mirrored) |
| `aggregate_all_clustering_results` | `aggregate_all_clustering_results` | `run:` block ported to `scripts/aggregate_all_clustering.py` |
| `plot_dimred_metadata` | `plot_dimred_metadata_{pca,umap,densmap}` (3) | method fan-out; 2D only (upstream default n_components 2) |
| `plot_dimred_clustering` | `plot_dimred_clustering_{pca,umap,densmap}` (3) | same |
| `plot_pca_diagnostics` | `plot_pca_diagnostics` | variance/pairs/loadings/lollipop PNGs, mem 8000M |
| `plot_umap_diagnostics` | `plot_umap_diagnostics_{umap,densmap}` (2) | mem 32000M (upstream) |
| `plot_umap_connectivity` | `plot_umap_connectivity_{umap,densmap}` (2) | mem 16000M (upstream) |
| `plot_dimred_interactive` | `plot_dimred_interactive_{pca,umap,densmap}_{2d,3d}` (6) | n_components fan-out; mem 8000M |
| `plot_heatmap` | `plot_heatmap_{correlation,cosine}` (2) | metric fan-out; hclust method from default list |
| `clustree_analysis` | `clustree_analysis_default`, `clustree_analysis_custom` (2) | content fan-out |
| `clustree_analysis_metadata` | `clustree_analysis_metadata` | directory output of per-metadata PNGs |
| `validation_external` | `validation_external` | all 6 indices (AMI, ARI, FMI, Homogeneity, Completeness, V) in one rule, 6 outputs |
| `validation_internal` | `validation_internal_{Silhouette,Calinski_Harabasz,Dunn,C_index,Davies_Bouldin,BIC}` (6) | index fan-out; mem 2x (upstream) |
| `aggregate_rank_internal` | `aggregate_rank_internal` | TOPSIS ranking of the 6 internal indices |
| `plot_indices` | `plot_indices_external`, `plot_indices_internal` (2) | type fan-out; external = 6 heatmaps, internal = 1 ranked heatmap |
| `annot_export` | `annot_export` | `cp {input} {output}` |
| `env_export` (7) | **not ported** | requires runtime `conda env export`; the pinned envs are committed under `envs/` instead (see README) |
| `config_export` | **not ported** | dumps the in-memory Snakemake config; `[config]` in `main.oxoflow` documents the same values |
| `plot_dimred_features` | **not ported** | upstream default `features_to_plot: []` produces no output on the default path |
| `report/` generation | **not ported** | Snakemake report metadata has no oxo-flow counterpart |

### Porting notes and deviations

1. **Annotation mapping**: the upstream annotation CSV's `data`/`metadata`
   columns become `{config.data_dir}/{sample}_data.csv` and
   `{config.data_dir}/{sample}_labels.csv`; `samples_by_features` is a global
   config key (upstream reads it per sample).
2. **Parameter-list fan-out**: upstream wildcards over parameter lists
   (UMAP/densMAP n_components, distance-matrix metric/type, Leiden
   partition_type/resolution, heatmap metric, clustree content, internal
   index) have no oxo-flow engine equivalent, so each default combination is
   an explicit rule whose name and paths embed the combination. Changing a
   listed parameter (e.g. adding a UMAP metric) requires adding rules.
3. **Snakemake runtime object**: all scripts read their inputs/outputs/params
   as CLI arguments instead of the `snakemake` global; the analysis code is
   unchanged. R scripts share `scripts/args.R` for `--flag value` parsing.
4. **Aggregation rules**: upstream `run:` blocks were ported to Python
   scripts with identical logic.
5. **Memory/threads**: upstream `mem: 32000` / `threads: 2` defaults become
   `[defaults]`; per-rule overrides match upstream (pca diagnostics and
   interactive plots 8000M, internal validation 2x).
6. **Environment**: each rule pins the same conda environment as upstream
   (7 environments, copied verbatim from `workflow/envs/`).

## License

Apache-2.0 (this port), upstream MIT — see `NOTICE.md` and `LICENSE.upstream`.
