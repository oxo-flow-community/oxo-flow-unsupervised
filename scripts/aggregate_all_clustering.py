#### aggregate clustering results across methods ####
# Port of the upstream "aggregate_all_clustering_results" run: block.  All
# inputs are the per-method aggregated clustering results.

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

# list to hold the data
agg_clust = []

# read each clustering result and add to data dict
for filename in args.inputs:
    agg_clust.append(pd.read_csv(filename, header=0, index_col=0))

    # convert the dictionary to a DataFrame
agg_clust_df = pd.concat(agg_clust, axis=1)

# Write the DataFrame to a CSV file
agg_clust_df.to_csv(args.out, index=True)
