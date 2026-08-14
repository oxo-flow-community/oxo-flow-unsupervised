#### perform low dimensional embedding of the knn-graph using Uniform Manifold Approximation and Projection (UMAP) ####

#### libraries
# general
import argparse
import os
import pickle
import pandas as pd

# dimensionality reduction
import umap

#### configurations

# inputs/outputs/parameters are passed as CLI arguments in this port
# (upstream: snakemake object)
parser = argparse.ArgumentParser()
parser.add_argument("--data", required=True)
parser.add_argument("--graph", required=True)
parser.add_argument("--out-object", required=True)
parser.add_argument("--out-data", required=True)
parser.add_argument("--out-axes", required=True)
parser.add_argument("--samples-by-features", required=True)
parser.add_argument("--metric", required=True)
parser.add_argument("--n-neighbors", required=True)
parser.add_argument("--min-dist", required=True)
parser.add_argument("--n-components", required=True)
parser.add_argument("--densmap", required=True)
args = parser.parse_args()

data_path = args.data
graph_object_path = args.graph
result_object_path = args.out_object
result_data_path = args.out_data
result_axes_path = args.out_axes

result_dir = os.path.dirname(result_object_path)

samples_by_features = int(args.samples_by_features)
metric = args.metric
n_neighbors = int(args.n_neighbors)
min_dist = float(args.min_dist)
n_components = int(args.n_components)
densmap = True if int(args.densmap) == 1 else False

# make directory if not existing
if not os.path.exists(result_dir):
    os.makedirs(result_dir, exist_ok=True)

### load data

# check data orientation to fit: samples/observations x features
if samples_by_features == 1:
    data = pd.read_csv(data_path, index_col=0)
else:
    data = pd.read_csv(data_path, index_col=0).T

# if less than 11 datapoints there is no pre-computed KNN graph
if data.shape[0] < 11:
    print("no pre-computed KNN graph will be used")
    knn = (None, None, None)
else:
    # load pre-computed KNN graph
    with open(graph_object_path, "rb") as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        knn = pickle.load(f)

### embed data in low dimensions
umap_obj = umap.umap_.UMAP(
    n_neighbors=n_neighbors,
    n_components=n_components,
    metric=metric,
    metric_kwds=None,
    output_metric="euclidean",
    output_metric_kwds=None,
    n_epochs=None,
    learning_rate=1.0,
    init="spectral",
    min_dist=min_dist,
    spread=1.0,
    low_memory=True,
    n_jobs=-1,
    set_op_mix_ratio=1.0,
    local_connectivity=1.0,
    repulsion_strength=1.0,
    negative_sample_rate=5,
    transform_queue_size=4.0,
    a=None,
    b=None,
    random_state=42,
    angular_rp_forest=False,
    target_n_neighbors=-1,
    target_metric="categorical",
    target_metric_kwds=None,
    target_weight=0.5,
    transform_seed=42,
    transform_mode="embedding",
    force_approximation_algorithm=False,
    verbose=False,
    tqdm_kwds=None,
    unique=False,
    densmap=densmap,
    dens_lambda=2.0,
    dens_frac=0.3,
    dens_var_shift=0.1,
    output_dens=False,
    disconnection_distance=None,
    precomputed_knn=knn,
).fit(data)

# data_embedding = umap_obj.fit_transform(data)

data_df = pd.DataFrame(
    umap_obj.embedding_,
    index=data.index,
)
data_df = data_df.rename_axis(("sample_name"))

if densmap:
    data_df.columns = ["densMAP_{}".format(str(idx + 1)) for idx in data_df.columns]
else:
    data_df.columns = ["UMAP_{}".format(str(idx + 1)) for idx in data_df.columns]

### save data

# save umap object
with open(result_object_path, "wb") as f:
    pickle.dump(umap_obj, f, pickle.HIGHEST_PROTOCOL)

# save transformed data
data_df.to_csv(result_data_path)

# save axes information for visualization
axes_info_df = pd.DataFrame(data_df.columns)
axes_info_df.columns = ["label"]
axes_info_df["label"] = [label.replace("_", "") for label in axes_info_df["label"]]
axes_info_df.to_csv(result_axes_path)
