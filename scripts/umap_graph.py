#### perform knn graph generation from Uniform Manifold Approximation and Projection (UMAP) ####

#### libraries
# general
import argparse
import os
import pickle
import pandas as pd

# dimensionality reduction
from umap.umap_ import nearest_neighbors

#### configurations

# inputs/outputs/parameters are passed as CLI arguments in this port
# (upstream: snakemake object)
parser = argparse.ArgumentParser()
parser.add_argument("--data", required=True)
parser.add_argument("--out", required=True)
parser.add_argument("--samples-by-features", required=True)
parser.add_argument("--metric", required=True)
parser.add_argument("--n-neighbors", required=True)
args = parser.parse_args()

data_path = args.data
result_object_path = args.out

result_dir = os.path.dirname(result_object_path)

samples_by_features = int(args.samples_by_features)
metric = args.metric
n_neighbors = int(args.n_neighbors)

# make directory if not existing
if not os.path.exists(result_dir):
    os.makedirs(result_dir, exist_ok=True)

### load data

# check data orientation to fit: samples/observations x features
if samples_by_features == 1:
    data = pd.read_csv(data_path, index_col=0)
else:
    data = pd.read_csv(data_path, index_col=0).T

# if less than 11 datapoints the KNN graph object can not be serialized (PyNNdescent issue: https://github.com/Teichlab/bbknn/issues/48)
if data.shape[0] < 11:
    from pathlib import Path

    Path(result_object_path).touch()
    import sys

    sys.exit()

### get knn-graph
knn = nearest_neighbors(
    data,
    n_neighbors=n_neighbors,
    metric=metric,
    metric_kwds=None,
    angular=False,
    random_state=42,
    low_memory=True,
    use_pynndescent=True,
    n_jobs=-1,
    verbose=False,
)

## save knn graph object
with open(result_object_path, "wb") as f:
    pickle.dump(knn, f, pickle.HIGHEST_PROTOCOL)
