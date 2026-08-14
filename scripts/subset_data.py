#### subset data for usage as metadata in subsequent feature plots ####

#### libraries
# general
import argparse
import pandas as pd

#### configurations

# inputs/outputs/parameters are passed as CLI arguments in this port
# (upstream: snakemake object)
parser = argparse.ArgumentParser()
parser.add_argument("--data", required=True)
parser.add_argument("--out", required=True)
parser.add_argument("--samples-by-features", required=True)
parser.add_argument("--features", default="")
args = parser.parse_args()

data_path = args.data
metadata_features_path = args.out

samples_by_features = int(args.samples_by_features)
# comma separated list (upstream: list from config)
features_to_plot = set(
    [f for f in args.features.split(",") if f != ""] if args.features != "" else []
)

### load data

# check data orientation to fit: samples/observations x features
if samples_by_features == 1:
    data = pd.read_csv(data_path, index_col=0)
else:
    data = pd.read_csv(data_path, index_col=0).T

### check if "ALL" features should be plotted and overlap with columns & subset data
if features_to_plot == {"ALL"}:
    features_to_plot = list(data.columns)
else:
    features_to_plot = list(features_to_plot.intersection(set(data.columns)))

# subset data
if len(features_to_plot) != 0:
    data = data.loc[:, features_to_plot]
else:
    print(
        "requested features to plot are not in the provided data, first 10 features will be plotted instead"
    )
    data = data.iloc[:, :10]

# save data
data.to_csv(metadata_features_path)
