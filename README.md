# oxo-flow-unsupervised — Unsupervised analysis of omics matrices: PCA, UMAP, clustering and validation

[![CI](https://github.com/oxo-flow-community/oxo-flow-unsupervised/actions/workflows/ci.yml/badge.svg)](https://github.com/oxo-flow-community/oxo-flow-unsupervised/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

> ★ Verified · ⇄ Official port of [`epigen/unsupervised_analysis`](https://github.com/epigen/unsupervised_analysis) @ `v4.0.2` — same tools, same versions, same commands. Part of the [oxo-flow-community catalog](https://oxo-flow-community.github.io/).

Point this workflow at one or more omics matrices (each with an optional
metadata table) and it runs the full unsupervised-analysis path: PCA and
UMAP/densMAP embeddings (2D and 3D), distance matrices, hierarchical
clustering heatmaps, Leiden clustering across partition types and
resolutions, clustree analysis, external and internal cluster validation
with TOPSIS ranking, and static plus interactive visualizations. Every
result is written below `results/unsupervised_analysis/{sample}/` for
direct inspection or downstream use.

## Installation

### 1. Install oxo-flow

This workflow requires oxo-flow >= 0.12.0. The `report = "…"` caption
annotations on 28 rules additionally need **>= 0.17.0** (the rule-captions
report section) and are ignored by older engines.

Recommended — release binary (Linux x86_64):

```bash
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
```

Alternatively via conda:

```bash
conda install -c bioconda oxo-flow-cli
```

Note that the conda package may lag behind releases; binaries for other
platforms are on the [releases page](https://github.com/Traitome/oxo-flow/releases).

### 2. Get this workflow

```bash
git clone https://github.com/oxo-flow-community/oxo-flow-unsupervised.git
cd oxo-flow-unsupervised
```

### 3. Requirements

- **Reference data**: no genome, index, or reference files are needed — the
  inputs are the omics matrices themselves. For each sample provide a matrix
  CSV (`{config.data_dir}/{sample}_data.csv`) and, optionally, a labels CSV
  (`{config.data_dir}/{sample}_labels.csv`), and register the sample in
  `config/annotation.csv`. Default inputs are real sklearn `digits` data
  (1797 samples x 64 features) committed under `test/fixtures/`, so the
  workflow runs out of the box.
- **Compute**: up to 2 CPUs and 32 GB RAM per rule (defaults `threads = 2`,
  `mem_mb = 32000`); 7 plotting rules use 8 GB. Lower limits are fine for the
  bundled digits dataset.
- **Tools**: conda environments with pinned versions. 60 of the 61 rules pin
  one of the 7 environments committed under `envs/` (e.g. `scikit-learn=1.3.0`,
  `leidenalg=0.10.1`, `r-ggplot2=3.3.6`); oxo-flow creates these with
  conda/mamba on first run, so a conda (or mamba/micromamba) installation is
  required. The remaining rule (`annot_export`, a file copy) needs no
  environment.

## Usage

```bash
# validate, lint, and dry-run the workflow
./test/run.sh

# run the workflow for sample "digits" (the two plot_dimred_features_*
# rules are when-gated on config.plot_dimred_features, default false)
oxo-flow run main.oxoflow
```

Default inputs are real sklearn `digits` data (1797 samples x 64 features)
committed under `test/fixtures/`. The annotation file `config/annotation.csv`
maps each sample to its matrix and metadata file; the upstream annotation
columns `data`/`metadata` map to the port convention
`{config.data_dir}/{sample}_data.csv` and `{config.data_dir}/{sample}_labels.csv`.

### Configuration

All upstream defaults are set in `[config]` in `main.oxoflow` and can be
overridden with `oxo-flow run main.oxoflow -c key=value` (or a config file):

| Key | Default | Upstream equivalent |
|---|---|---|
| `threads` / `mem_mb` | `2` / `32000` | `threads` / `mem` |
| `project_name` | `digits` | `project_name` |
| `data_dir` | `test/fixtures` | annotation `data`/`metadata` columns |
| `result_path` | `results` | `result_path` (upstream test default `.test/results/`) |
| `samples_by_features` | `1` | annotation `samples_by_features` column |
| `pca_svd_solver` / `pca_n_components` | `auto` / `0.9` | `pca.svd_solver` / `pca.n_components` |
| `umap_metric` / `umap_n_neighbors` / `umap_min_dist` | `euclidean` / `15` / `0.1` | `umap.metrics[0]` / `umap.n_neighbors[0]` / `umap.min_dist[0]` |
| `umap_densmap` / `umap_connectivity` / `umap_diagnostics` | `1` / `1` / `1` | `umap.densmap` / `umap.connectivity` / `umap.diagnostics` |
| `heatmap_hclust_method` / `heatmap_n_observations` / `heatmap_n_features` | `complete` / `1` / `0.5` | `heatmap.hclust_methods[0]` / `heatmap.n_observations` / `heatmap.n_features` |
| `leiden_metric` / `leiden_n_neighbors` / `leiden_n_iterations` | `euclidean` / `15` / `2` | `leiden.metrics[0]` / `leiden.n_neighbors[0]` / `leiden.n_iterations` |
| `clustree_*` | `0` / `0.1` / `tree` / `majority` / `mean` | `clustree.*` |
| `sample_proportion` | `1` | `sample_proportion` |
| `metadata_of_interest` | `["target"]` | `metadata_of_interest` |
| `features_to_plot` | `[]` | `features_to_plot` |
| `plot_dimred_features` | `false` | port switch: upstream gate `len(features_to_plot) > 0` (see porting note 7) |
| `coord_fixed` / `scatterplot2d_size` / `scatterplot2d_alpha` | `0` / `1` / `1` | `coord_fixed` / `scatterplot2d.size` / `scatterplot2d.alpha` |

### Outputs

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
| `envs/` | resolved conda environment snapshots (`conda env export` per env) |

## Source

Ported from **[epigen/unsupervised_analysis](https://github.com/epigen/unsupervised_analysis)**
(Snakemake), version `v4.0.2`, commit
`4da72e9e8792ecdfa474a67c17b3f9b564eb462e`, upstream license MIT. Created
2026-08-15; this workflow may lag behind upstream releases. See `NOTICE.md`
for the full upstream attribution and license.

## Fidelity

Upstream rules and how each is ported (61 ported rules; every analysis step
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
| `plot_dimred_features` | `plot_dimred_features_{pca,umap}` (2) | method fan-out (upstream appends "features" content only for PCA and UMAP); gated on `config.plot_dimred_features` — see porting note 7 |
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
| `env_export` (7) | `env_export_{umap_leiden,clusterCrit,clustree,ComplexHeatmap,ggplot,plotly,pymcdm}` (7) | resolved-env snapshot: oxo-flow runs each rule inside its pinned env via `conda run`, so `conda env export -p "$CONDA_PREFIX"` exports the ANALYSIS env (mamba fallback; mem 1000M like upstream) |
| `config_export` | **not ported** | see "Remaining exclusions" below |
| `report/` generation | **captions ported** | per-rule captions as `report = "…"` annotations; book form not ported — see "Remaining exclusions" below |

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
7. **Boolean gate instead of list gate**: upstream runs `plot_dimred_features`
   only when `len(features_to_plot) > 0`; the oxo-flow `when` evaluator
   compares scalar config values (booleans, numbers, strings), not arrays, so
   the port carries the gate on `config.plot_dimred_features` (default
   `false`, matching the upstream default of an empty `features_to_plot`).
   Enable it together with a non-empty `features_to_plot` — the plotting
   script then uses the requested features, or falls back to the first 10
   columns when the requested features are absent.

### Remaining exclusions (with evidence)

1. **`config_export`** — upstream dumps the effective in-memory Snakemake
   config to `results/configs/{project}_config.yaml`. In oxo-flow the config
   IS the committed `[config]` table of `main.oxoflow` (there is no external
   runtime config object), and the effective config is introspectable at any
   time with `oxo-flow config show` / `oxo-flow config get <key>` (resolved
   values after CLI overrides). A dump rule would have to enumerate every key as a
   `{config.x}` placeholder — duplicating `[config]` while drifting whenever
   a key is added or renamed. The sibling `annot_export` IS ported because
   the annotation CSV is external data, not the workflow's own declaration.
2. **`report/` generation (book form)** — the Snakemake report book is an HTML
   aggregation of rule outputs carrying per-artifact metadata (captions from
   `workflow/report/*.rst`, categories, subcategories, labels) attached
   through `report(...)` output wrappers. The **captions are ported**: the 28
   rules upstream wraps in `report(...)` (dimred/heatmap/clustree/indices
   plots, PCA/UMAP diagnostics and connectivity, 7 `env_export` snapshots,
   `annot_export`) carry a `report = "…"` annotation with the upstream .rst
   caption inlined (rendered by the engine rule-captions report section,
   needs oxo-flow >= 0.17.0; older engines ignore the key). What has no
   oxo-flow equivalent is the **book form**: the self-contained HTML
   aggregation with figures embedded and categories/subcategories/labels
   (static text only — the engine does not interpolate wildcards), the
   workflow-level `report:` directive (`workflow/report/workflow.rst`), and
   `oxo-flow report` itself produces an execution report from the checkpoint
   (rule status, timings, provenance), not an artifact-catalog book. All
   underlying artifact outputs are produced by the ported rules.

## Test

```bash
bash test/run.sh
```

Runs `oxo-flow validate`, `lint`, and `dry-run` (plus a debug check that no
literal wildcards survive expansion) and must exit 0.

## License

Apache-2.0 (this port), upstream MIT — see `NOTICE.md` and `LICENSE.upstream`.
