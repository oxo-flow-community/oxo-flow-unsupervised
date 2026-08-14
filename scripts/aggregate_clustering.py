#### aggregate clustering results per method ####
# Port of the upstream "aggregate_clustering_results" run: block.  The first
# input is the metadata file (unused upstream, mirrored here) and all
# following inputs are the per-parameter clustering results of one method.

#### libraries
import argparse
import pandas as pd

#### configurations

# inputs/outputs are passed as CLI arguments in this port
# (upstream: snakemake run: block)
parser = argparse.ArgumentParser()
parser.add_argument("--inputs", required=True, nargs="+")
parser.add_argument("--out", required=True)
args = parser.parse_args()

#### aggregation (analysis body identical to upstream)

# list to hold the individual clusterings
agg_clust = []

# read each clustering result and add to list
for filename in args.inputs[1:]:
    clust_tmp = pd.read_csv(
        filename, header=0, index_col=0
    )  # .squeeze("columns")
    agg_clust.append(clust_tmp)

    # convert list to dataframe
agg_clust_df = pd.concat(agg_clust, axis=1)

# Write the DataFrame to a CSV file
agg_clust_df.to_csv(args.out, index=True)
