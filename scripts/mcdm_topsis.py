#### load all the internal indices of all clusterings and metadata and apply the MCDM/A method TOPSIS to rank them ####

#### libraries
import argparse
import os
import numpy as np
import pandas as pd
from pymcdm.methods import TOPSIS

#### configurations

# inputs/outputs/parameters are passed as CLI arguments in this port
# (upstream: snakemake object)
parser = argparse.ArgumentParser()
parser.add_argument("--inputs", required=True, nargs="+")
parser.add_argument("--out", required=True)
args = parser.parse_args()

indices_paths = args.inputs
indices_ranked_path = os.path.join(args.out)

# load the internal indices and aggregate
idx_dfs = []
for idx_path in indices_paths:
    idx_dfs.append(pd.read_csv(os.path.join(idx_path), index_col=0))

indices = pd.concat(idx_dfs, axis=1)

# remove rows with NA
indices = indices.dropna()

# perform TOPSIS

# give all scores equal weights as they are supposed to be complementary
weights = np.full(indices.shape[1], 1.0 / indices.shape[1])
# set 1 for benefit (max) and -1 for cost (min) functions (hard coded for internal indices in order)
types = np.array([1, 1, 1, -1, -1, -1])
# create object with defaults
topsis = TOPSIS()
# run TOPSIS
pref = topsis(indices.to_numpy(), weights, types)

# sort by TOPSIS results
indices_ranked = indices.iloc[pref.argsort()[::-1]]

# save ranked indices
indices_ranked.to_csv(indices_ranked_path)
