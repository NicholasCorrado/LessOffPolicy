#!/bin/bash

# untar your Python installation. Make sure you are using the right version!
tar -xzf python39.tar.gz

# make sure the script will use your Python installation,
# and the working directory as its home location
export PATH=$PWD/python/bin:$PATH
mkdir packages
export PYTHONPATH=$PWD/packages

python3 -m pip install --target=$PWD/packages mujoco gym
tar -czf packages.tar.gz packages/