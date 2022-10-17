# Mujoco on CHTC 

This repo simulates random actions in all environments included in `gym` (no extra environments like atari).
It is small example of MuJoCo working on CHTC.

## Running Locally

```commandline
conda create -n chtc python=3.9
conda activate chtc
git clone git@github.com:Badger-RL/chtc.git
pip install -e chtc
```
To run:
```commandline
python simulate.py
```

## Running on CHTC

See [here](https://chtc.cs.wisc.edu/uw-research-computing/python-jobs.html) for a thorough overview of how to setup jobs with CHTC.

Login to your CHTC submit node, and then:
```commandline
git clone git@github.com:Badger-RL/chtc.git
cd chtc
mkdir output
condor_submit job.sub
```
Output logs (`job.err`, `job.out`, `job.log`) are written to the `output` directory. 
Upon success, `job.out` will contain (modulo randomness):

```commandline
Simulating CartPole-v0...
Average return over 10 episodes: 122.30453232317942 +/- 34.533571653052164

...

Simulating HumanoidStandup-v4...
Average return over 10 episodes: 132.71190201448096 +/- 37.4015262587107

Successfully tested all environments
```
and `job.err` will be empty.

### Getting Dependencies

The dependencies are already included in the `packages.tar.gz` file. 
To obtain this file from scratch:
```commandline
git clone git@github.com:Badger-RL/chtc.git
cd chtc
mkdir output
condor_submit job_packages.sub
```
Upon completion, a `packages.tar.gz` tarball will be outputted.