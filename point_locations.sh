#!/bin/bash
DRAY_OUPUT_PREFIX=${DRAY_LOG_PREFIX:-dray_data}

for ((i=1; i <= ${1:?}; i++)) 
do
    echo "Build Trial #$i"
    ./point_location point_config.yaml
    mv ${DRAY_OUPUT_PREFIX}_0.yaml ${DRAY_OUPUT_PREFIX}_${i}.yaml
done