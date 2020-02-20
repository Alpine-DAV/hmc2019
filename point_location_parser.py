#!/usr/bin/env python3
# To run this make sure you have pandas installed (I installed it through anaconda).
# I recommend running this in interactive mode with the -i flag to mess around with the
# dataframes.
# Input: Any number of filenames to load into the dataframes. Can use filename pattern
#        matching.
#
# Example: python -i point_location_parser.py dray_data_*.yaml

import yaml
import sys
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans
from scipy.cluster.vq import vq

# A dictionary containing dataframes for the following root headers found in the 
# output point location yaml file.
dfs = {"locate" : pd.DataFrame()}


# loads the data returned in a point location yaml file into a dataframe
def load_point_file(filename):
    output = None
    run_num = int(filename.split('_')[-1].split('.')[0])
    with open(filename, 'r') as f:
        # depending on what version of the python ymal package you have
        # you might need to delete the ```Loader=yaml.FullLoader``` parameter
        output = yaml.load(f.read(), Loader=yaml.FullLoader)
        for header in output.keys():
            out_dict = {"run" : run_num}
            if "locate" in header:  # locate headers have the format "locate(_NUM)?"
                trial_num = 0 if not '_' in header else int(header.split('_')[-1])
                out_dict["trial"] = trial_num
                out_dict.update(output[header])
                dfs["locate"] = dfs["locate"].append(
                        pd.io.json.json_normalize(data=out_dict),
                        ignore_index = True)
            else:
                if header not in dfs.keys():
                    dfs[header] = pd.DataFrame()
                out_dict.update(output[header])
                dfs[header] = dfs[header].append(
                        pd.io.json.json_normalize(data=out_dict),
                        ignore_index = True)

def plot_anomalies_of(key, column_name, plot_type, clusters=2):
    df = dfs[key]
    plt.style.use('ggplot')
    if (plot_type == "box"):
        df[column_name].plot(kind='box')
        plt.show()
    if (plot_type == "kmeans"):
        raw = df[column_name].values
        raw = raw.reshape(-1, 1)
        raw = raw.astype('float64')
        centroids, avg_distance = kmeans(raw, clusters)
        groups, cdist = vq(raw, centroids)
        plt.scatter(raw, np.arange(0, len(df[column_name].values)), c=groups)
        plt.xlabel('Value')
        plt.ylabel('Trial')
        plt.show()

def save_to_excel(fname='timing.xlsx'):
    # Save the dataframes of data into individual sheets of an excel file
    with pd.ExcelWriter(fname) as writer:  
        for header in dfs.keys():
            dfs[header].to_excel(writer, sheet_name=header)

def main():
    # Can take in multiple filnames with pattern matching
    file_count = 0
    for arg in sys.argv[1:]:
        for filename in glob.glob(arg):
            load_point_file(filename)
            file_count += 1
    print("%d file%s loaded into dfs dictionary."
            % (file_count, 's' if file_count else ''))
    print("Possible headers are: " + str(dfs.keys()))


if __name__ == "__main__":
    main()
