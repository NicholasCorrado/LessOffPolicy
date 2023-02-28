#!/bin/bash

CODENAME=chtc

# untar your Python installation. Make sure you are using the right version!
tar -xzf python39.tar.gz

cp /staging/ncorrado/${CODENAME}.tar.gz .
tar xf ${CODENAME}.tar.gz

# (optional) if you have a set of packages (created in Part 1), untar them also
cd $CODENAME
tar -xzf packages.tar.gz

# Make sure the script will use your Python installation,
# and the working directory as its home location
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

pid=$1
step=$2 #ranges from 0 to num_jobs-1
cmd=$3
echo $cmd $pid $step

# run your script
# $step ensures seeding is constistent across experiment batches
$(python -u $cmd --run-id $pid --seed $step)

# compress results. This file will be transferred to your submit node upon job completion.
tar czvf results_${pid}.tar.gz results
