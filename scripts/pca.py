#### perform Principal Component Analysis (PCA) using sklearn ####

#### libraries
# general
import argparse
import os
import pickle
import pandas as pd

# dimensionality reduction
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

#### configurations

# inputs/outputs/parameters are passed as CLI arguments in this port
# (upstream: snakemake object)
parser = argparse.ArgumentParser()
parser.add_argument("--data", required=True)
parser.add_argument("--out-object", required=True)
parser.add_argument("--out-data", required=True)
parser.add_argument("--out-data-small", required=True)
parser.add_argument("--out-loadings", required=True)
parser.add_argument("--out-loadings-small", required=True)
parser.add_argument("--out-var", required=True)
parser.add_argument("--out-axes", required=True)
parser.add_argument("--samples-by-features", required=True)
parser.add_argument("--n-components", required=True)
parser.add_argument("--svd-solver", required=True)
args = parser.parse_args()

data_path = args.data

result_object_path = args.out_object
result_data_path = args.out_data
result_data_small_path = args.out_data_small
result_loadings_path = args.out_loadings
result_loadings_small_path = args.out_loadings_small
result_var_path = args.out_var
result_axes_path = args.out_axes

samples_by_features = int(args.samples_by_features)
n_components_raw = args.n_components
if n_components_raw.lower() == "mle":
    n_components = "mle"
elif "." in n_components_raw:
    n_components = float(n_components_raw)
else:
    n_components = int(n_components_raw)
svd_solver = args.svd_solver

### load data

# check data orientation to fit: samples/observations x features
if samples_by_features == 1:
    data = pd.read_csv(data_path, index_col=0)
else:
    data = pd.read_csv(data_path, index_col=0).T

### transform data

# unsupervised PCA
pca_obj = PCA(
    n_components=n_components,
    copy=True,
    whiten=False,
    svd_solver=svd_solver,
    tol=0.0,
    iterated_power="auto",
    random_state=42,
)

data_pca = pca_obj.fit_transform(StandardScaler().fit_transform(data))

data_df = pd.DataFrame(
    data_pca,
    index=data.index,
)
data_df = data_df.rename_axis(("sample_name"))
data_df.columns = ["PC_{}".format(str(idx + 1)) for idx in data_df.columns]

### save data

# save pca object
with open(result_object_path, "wb") as f:
    pickle.dump(pca_obj, f, pickle.HIGHEST_PROTOCOL)

# save transformed data
data_df.to_csv(result_data_path)
data_df.iloc[:, : min(10, data_df.shape[1])].to_csv(result_data_small_path)

# save loadings
loadings = pd.DataFrame(
    pca_obj.components_.T, columns=data_df.columns, index=data.columns
)
loadings.to_csv(result_loadings_path)
loadings.iloc[:, : min(10, data_df.shape[1])].to_csv(result_loadings_small_path)

# save explained variance
axes_info_df = pd.DataFrame(pca_obj.explained_variance_ratio_)
axes_info_df.to_csv(result_var_path)

# save axes information for visualization
axes_info_df.columns = ["label"]
axes_info_df["label"] = [
    "PC{} ({}%)".format(idx + 1, round(100 * var, 2))
    for idx, var in axes_info_df["label"].items()
]
axes_info_df.to_csv(result_axes_path)
