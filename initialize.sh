#!/bin/sh

# create a folder where the index and the logs will be stored
mkdir -p data/Rag-Index logs

# install mamba:
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh"
bash Mambaforge-$(uname)-$(uname -m).sh

# set up mamba environment
mamba env create -f environment.yml

# activate the environment
mamba activate eventgpt

# make other script files executable
chmod +x *.sh

# run the pre_start.sh script
bash pre_start.sh