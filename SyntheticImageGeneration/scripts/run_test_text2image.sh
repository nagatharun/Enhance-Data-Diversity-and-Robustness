#!/bin/bash

#
if [ ! -d "$TMP/SyntheticImageGeneration/" ]; then
    mkdir $TMP/SyntheticImageGeneration/
fi

if [ ! -d "$TMP/SyntheticImageGeneration/data/" ]; then
    mkdir $TMP/SyntheticImageGeneration/data/
fi

if [ ! -d "$TMP/SyntheticImageGeneration/src/" ]; then
    mkdir $TMP/SyntheticImageGeneration/src/
fi

## Components
if [ ! -d "$TMP/SyntheticImageGeneration/src/components/" ]; then
    tar -C $TMP/ -xvzf $(ws_find data-ssd)/SyntheticImageGeneration/src/components.tgz
fi

## Configs
if [ ! -d "$TMP/SyntheticImageGeneration/configs/" ]; then
    tar -C $TMP/ -xvzf $(ws_find data-ssd)/SyntheticImageGeneration/configs.tgz
fi

## Assets
if [ ! -d "$TMP/SyntheticImageGeneration/src/assets/" ]; then
    tar -C $TMP/ -xvzf $(ws_find data-ssd)/SyntheticImageGeneration/src/assets.tgz
fi

# Extract compressed input data files on local SSD
## Data
if [ ! -d "$TMP/SyntheticImageGeneration/data/Cholec80/" ]; then
    tar -C $TMP/ -xvzf $(ws_find data-ssd)/SyntheticImageGeneration/data/Cholec80.tgz
fi

if [ ! -d "$TMP/SyntheticImageGeneration/data/CholecSeg8k/" ]; then
    tar -C $TMP/ -xvzf $(ws_find data-ssd)/SyntheticImageGeneration/data/CholecSeg8k.tgz
fi

if [ ! -d "$TMP/SyntheticImageGeneration/data/CholecT45/" ]; then
    tar -C $TMP/ -xvzf $(ws_find data-ssd)/SyntheticImageGeneration/data/CholecT45.tgz
fi

## Virtual Environment
if [ ! -d "$TMP/SyntheticImageGeneration/venv/" ]; then
    tar -C $TMP/ -xvzf $(ws_find data-ssd)/SyntheticImageGeneration/venv.tgz
fi

# Create results and scripts directory
mkdir $TMP/SyntheticImageGeneration/scripts
mkdir $TMP/SyntheticImageGeneration/results
cd $TMP/SyntheticImageGeneration/results
mkdir $TMP/SyntheticImageGeneration/results/training

# Activate virtual environment (venv)
cd $TMP/SyntheticImageGeneration/
source ./venv/bin/activate

# Start parameter tuning
./venv/bin/python3 ./src/components/imagen/testing/test_imagen.py --path_data_dir=$TMP/SyntheticImageGeneration/