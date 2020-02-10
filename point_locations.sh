#!/bin/bash

# To use, just place in your devil_ray/build/utilities/furnace/
# directory where point_location and point_config.yaml is.
# Usage: ./point_locations.sh START_INDEX END_INDEX /optional/output/dir
set -e

DRAY_OUPUT_PREFIX=${DRAY_LOG_PREFIX:-dray_data}

for ((i=${1:?}; i <= ${2:?}; i++)) 
do
    echo "Build Trial #$i"
    ./point_location point_config.yaml
    mv ${DRAY_OUPUT_PREFIX}_0.yaml ${3}${DRAY_OUPUT_PREFIX}_${i}.yaml
done
