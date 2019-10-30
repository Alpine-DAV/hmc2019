import os
import sys
import math

offset = 0

def filename_to_num(f):
    return int(f.split('_')[-1].split('.')[0])

relevant_filenames = [f for f in os.listdir() if f != sys.argv[0]]

max_num = max([filename_to_num(f) for f in relevant_filenames])

max_digits = int(math.log((max_num + offset), 10)) + 1

for f in relevant_filenames:
    number = filename_to_num(f)

    newname = "dray_data_" + str(offset + number).zfill(max_digits) + ".yaml"
    os.rename(f, newname)
