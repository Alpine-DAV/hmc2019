#!/bin/bash

set -e

CONFIGS_DIR=~/testing/configs
TIMING_RESULTS_DIR=~/testing/results/timing
STATS_RESULTS_DIR=~/testing/results/stats
MESH_UTILS_PATH=/g/g12/sobek1/devil_ray/src/dray/GridFunction/mesh_utils.cpp

NUM_TESTS=99

TIMING_FLAGS="-DENABLE_LOGGING=ON -DENABLE_STATS=OFF"
STATS_FLAGS="-DENABLE_LOGGING=ON -DENABLE_STATS=ON"
FIXED_FLAGS="-DENABLE_SUBDIVISIONS_FIXED=ON -DENABLE_SUBDIVISIONS_WANG=OFF \
             -DENABLE_SUBDIVISIONS_REC_SUB=OFF"
WANG_FLAGS="-DENABLE_SUBDIVISIONS_FIXED=OFF -DENABLE_SUBDIVISIONS_WANG=ON \
             -DENABLE_SUBDIVISIONS_REC_SUB=OFF"
REC_SUB_FLAGS="-DENABLE_SUBDIVISIONS_FIXED=OFF -DENABLE_SUBDIVISIONS_WANG=OFF \
             -DENABLE_SUBDIVISIONS_REC_SUB=ON"

CMAKE_CACHE_FLAG_SRC_OPENMP="-C /usr/workspace/wsb/hmc_19/tpls/pascal_openmp/pascal83-toss_3_x86_64_ib-gcc@4.9.3-ascent.cmake ../src"

CMAKE_CACHE_FLAG_SRC_CUDA="-C /usr/workspace/wsb/hmc_19/tpls/pascal_cuda/pascal83-toss_3_x86_64_ib-gcc@4.9.3-ascent.cmake ../src"


echo "TESTING OPENMP TIMING"
cd ~/devil_ray/build

echo "Fixed Timing"
cmake $TIMING_FLAGS $FIXED_FLAGS $CMAKE_CACHE_FLAG_SRC_OPENMP
while read s; do
    DRAY_OUPUT_PREFIX="fixed_${s}"
    echo "${DRAY_OUPUT_PREFIX}"
    # Replace number of splits
    sed -ri "s/(\sconstexpr int splits = )([0-9]+);/\1${s};/" \
            /g/g12/sobek1/devil_ray/src/dray/GridFunction/mesh_utils.cpp
    
    make -j

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml
    mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
    # 100 bvh constructions
    ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml
    for ((i=1; i <= $NUM_TESTS; i++))
    do
        ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml
        mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__${i}.yaml
    done
done < ${CONFIGS_DIR}/fixed_splits.txt


echo "Wang Timing"
cmake $TIMING_FLAGS $WANG_FLAGS $CMAKE_CACHE_FLAG_SRC_OPENMP
make -j
while read t; do
    DRAY_OUPUT_PREFIX="wang_${t}"
    echo "${DRAY_OUPUT_PREFIX}"
    # Replace number of splits

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml ${t}
    mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
    # 100 bvh constructions
    ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml
    for ((i=1; i <= $NUM_TESTS; i++))
    do
        ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml ${t}
        mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__${i}.yaml
    done
done < ${CONFIGS_DIR}/wang_tolerances.txt


echo "Recursive Subdivision Timing"
cmake $TIMING_FLAGS $REC_SUB_FLAGS $CMAKE_CACHE_FLAG_SRC_OPENMP
make -j
while read t; do
    DRAY_OUPUT_PREFIX="rec_sub_${t}"
    echo "${DRAY_OUPUT_PREFIX}"
    # Replace number of splits

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml ${t}
    mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
    # 100 bvh constructions
    ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml
    for ((i=1; i <= $NUM_TESTS; i++))
    do
        ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml ${t}
        mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__${i}.yaml
    done
done < ${CONFIGS_DIR}/rec_sub_tolerances.txt



echo "TESTING OPENMP STATS"
echo "Fixed Stats"
cmake $STATS_FLAGS $FIXED_FLAGS $CMAKE_CACHE_FLAG_SRC_OPENMP
while read s; do
    DRAY_OUPUT_PREFIX="fixed_${s}"
    echo "${DRAY_OUPUT_PREFIX}"
    # Replace number of splits
    sed -ri "s/(\sconstexpr int splits = )([0-9]+);/\1${s};/" \
            /g/g12/sobek1/devil_ray/src/dray/GridFunction/mesh_utils.cpp
    
    make -j

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml
    mv dray_data_0.yaml \
            ${STATS_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
done < ${CONFIGS_DIR}/fixed_splits.txt


echo "Wang Stats"
cmake $STATS_FLAGS $WANG_FLAGS $CMAKE_CACHE_FLAG_SRC_OPENMP
make -j
while read t; do
    DRAY_OUPUT_PREFIX="wang_${t}"
    echo "${DRAY_OUPUT_PREFIX}"

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml ${t}
    mv dray_data_0.yaml \
            ${STATS_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
done < ${CONFIGS_DIR}/wang_tolerances.txt


echo "Recursive Subdivision Stats"
cmake $STATS_FLAGS $REC_SUB_FLAGS $CMAKE_CACHE_FLAG_SRC_OPENMP
make -j
while read t; do
    DRAY_OUPUT_PREFIX="rec_sub_${t}"
    echo "${DRAY_OUPUT_PREFIX}"

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml ${t}
    mv dray_data_0.yaml \
            ${STATS_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
done < ${CONFIGS_DIR}/rec_sub_tolerances.txt





# # TESTING CUDA
# echo "TESTING CUDA TIMING"
cd ~/devil_ray/build-cuda
module load cuda

echo "Fixed Timing CUDA"
cmake $TIMING_FLAGS $FIXED_FLAGS $CMAKE_CACHE_FLAG_SRC_CUDA
while read s; do
    DRAY_OUPUT_PREFIX="cuda_fixed_${s}"
    echo "${DRAY_OUPUT_PREFIX}"
    # Replace number of splits
    sed -ri "s/(\sconstexpr int splits = )([0-9]+);/\1${s};/" \
            /g/g12/sobek1/devil_ray/src/dray/GridFunction/mesh_utils.cpp
    
    make -j

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml
    mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
    # 100 bvh constructions
    ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml
    for ((i=1; i <= $NUM_TESTS; i++))
    do
        ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml
        mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__${i}.yaml
    done
done < ${CONFIGS_DIR}/fixed_splits.txt


echo "Wang Timing CUDA"
cmake $TIMING_FLAGS $WANG_FLAGS $CMAKE_CACHE_FLAG_SRC_CUDA
make -j
while read t; do
    DRAY_OUPUT_PREFIX="cuda_wang_${t}"
    echo "${DRAY_OUPUT_PREFIX}"
    # Replace number of splits

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml ${t}
    mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
    # 100 bvh constructions
    ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml
    for ((i=1; i <= $NUM_TESTS; i++))
    do
        ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml ${t}
        mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__${i}.yaml
    done
done < ${CONFIGS_DIR}/wang_tolerances.txt


echo "Recursive Subdivision Timing CUDA"
cmake $TIMING_FLAGS $REC_SUB_FLAGS $CMAKE_CACHE_FLAG_SRC_CUDA
make -j
while read t; do
    DRAY_OUPUT_PREFIX="cuda_rec_sub_${t}"
    echo "${DRAY_OUPUT_PREFIX}"
    # Replace number of splits

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml ${t}
    mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
    # 100 bvh constructions
    ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml
    for ((i=1; i <= $NUM_TESTS; i++))
    do
        ./utilities/furnace/point_location ${CONFIGS_DIR}/bvh_config.yaml ${t}
        mv dray_data_0.yaml \
            ${TIMING_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__${i}.yaml
    done
done < ${CONFIGS_DIR}/rec_sub_tolerances.txt



echo "TESTING CUDA STATS"
echo "Fixed Stats CUDA"
cmake $STATS_FLAGS $FIXED_FLAGS $CMAKE_CACHE_FLAG_SRC_CUDA
while read s; do
    DRAY_OUPUT_PREFIX="cuda_fixed_${s}"
    echo "${DRAY_OUPUT_PREFIX}"
    # Replace number of splits
    sed -ri "s/(\sconstexpr int splits = )([0-9]+);/\1${s};/" \
            /g/g12/sobek1/devil_ray/src/dray/GridFunction/mesh_utils.cpp
    
    make -j

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml
    mv dray_data_0.yaml \
            ${STATS_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
done < ${CONFIGS_DIR}/fixed_splits.txt


echo "Wang Stats CUDA"
cmake $STATS_FLAGS $WANG_FLAGS $CMAKE_CACHE_FLAG_SRC_CUDA
make -j
while read t; do
    DRAY_OUPUT_PREFIX="cuda_wang_${t}"
    echo "${DRAY_OUPUT_PREFIX}"

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml ${t}
    mv dray_data_0.yaml \
            ${STATS_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
done < ${CONFIGS_DIR}/wang_tolerances.txt


echo "Recursive Subdivision Stats CUDA"
cmake $STATS_FLAGS $REC_SUB_FLAGS $CMAKE_CACHE_FLAG_SRC_CUDA
make -j
while read t; do
    DRAY_OUPUT_PREFIX="cuda_rec_sub_${t}"
    echo "${DRAY_OUPUT_PREFIX}"

    # 100 trails of point locations
    ./utilities/furnace/point_location ${CONFIGS_DIR}/point_config.yaml ${t}
    mv dray_data_0.yaml \
            ${STATS_RESULTS_DIR}/${DRAY_OUPUT_PREFIX}__0.yaml
done < ${CONFIGS_DIR}/rec_sub_tolerances.txt

cd -

