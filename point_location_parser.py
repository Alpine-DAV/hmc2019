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

# A dictionary containing dataframes for the following root headers found in the 
# output point location yaml file.
point_data_dataframes = {"mesh_bvh": pd.DataFrame(), "external faces": pd.DataFrame(), "locate": pd.DataFrame()}


# loads the data returned in a point location yaml file into a dataframe
def load_point_file(filename):
    output = None
    with open(filename, 'r') as f:
        output = yaml.load(f.read(), Loader=yaml.FullLoader)
        for header in output.keys():
            if "locate" in header:  # locate headers have the format "locate(_NUM)?"
                point_data_dataframes["locate"] = point_data_dataframes["locate"].append(
                        pd.io.json.json_normalize(data={ "locate" : output[header]}),
                        ignore_index = True)
            else:
                point_data_dataframes[header] = point_data_dataframes[header].append(
                        pd.io.json.json_normalize(data={header : output[header]}),
                        ignore_index = True)


def main():
    # Can take in multiple filnames with pattern matching
    file_count = 0
    for arg in sys.argv[1:]:
        for filename in glob.glob(arg):
            load_point_file(filename)
            file_count += 1
    print("%d file%s loaded into point_data_dataframes dictionary."
            % (file_count, 's' if file_count else ''))
    print("Possible headers are: " + str(point_data_dataframes.keys()))


if __name__ == "__main__":
    main()
