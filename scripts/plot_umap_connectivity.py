#### generate diagnostic plots for Uniform Manifold Approximation and Projection (UMAP) ####

#### libraries
# general
import argparse
import pickle

# dimensionality reduction
import umap
import umap.plot

#### configurations

# inputs/outputs/parameters are passed as CLI arguments in this port
# (upstream: snakemake object)
parser = argparse.ArgumentParser()
parser.add_argument("--object", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()

object_path = args.object
plot_connectivity_path = args.out

### load data
with open(object_path, "rb") as f:
    umap_obj = pickle.load(f)

### generate & save UMAP connectivity plot

# umap.plot.connectivity(umap_obj, show_points=True)
umap.plot.connectivity(umap_obj, edge_bundling="hammer").figure.savefig(
    plot_connectivity_path
)
