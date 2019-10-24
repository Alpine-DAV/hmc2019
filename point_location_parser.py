#!/usr/bin/env python3
# Input: a YAML file from furnace point_test

import pandas as pd
import yaml
import sys

# This will be a dictionary of dataframes with keys 
# ["mesh_bvh", "external faces", "locate"]
point_data_dataframes = {}
locates = []
output = None

with open(sys.argv[1], 'r') as f:
    output = yaml.load(f.read(), Loader=yaml.FullLoader)
    for header in output.keys():
        if "locate" in header:
            locate_dict = {"locate" : 0 if header == "locate" else int(header[7:])}
            locate_dict.update(output[header])
            locates.append(output)
        else:
            point_data_dataframes[header] = pd.io.json.json_normalize(
            data={header : output[header]})

# locates flattend afterwards to account for multiple 
point_data_dataframes["locate"] = pd.io.json.json_normalize(data=locates)
