#!/bin/bash

# untar your Python installation. Make sure you are using the right version!
tar -xzf python39.tar.gz
# (optional) if you have a set of packages (created in Part 1), untar them also
tar -xzf packages.tar.gz

# make sure the script will use your Python installation,
# and the working directory as its home location
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

pid=$1
step=$2 # ranges from 0 to num_jobs
command=$3
echo $params

# run your script
# $step ensures seeding is consistent across experiment batches
python3 -u $command --run-id $pid --seed $step

tar xf results_${pid}.tar.gz results