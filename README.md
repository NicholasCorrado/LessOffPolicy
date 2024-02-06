# CHTC Workflow

This is an example of how I use CHTC to run RL experiments. 
I felt that a minimal working example would not capture some of the relevant details for running large batches of RL experiments,
so I added some bells and whistles to make things more concrete. 

An brief summary of the workflow:

1. Generate a list of commands `commands/mycommands.txt` you want to execute (plus a few other job details).
2. To run 10 seeds of each command, run `./submit.sh mycommands 10`
3. Results are saved to `results/mycommands/`

For example, if we wanted to sweep over different learning rates for the Hopper environment, `commands/mycommands.txt` may look like:
```commandline
1,6,python*-u*train.py*--results-subdir*lr_0.001*--env-id*Hopper-v4*--num-timesteps*10000*--eval-freq*1000*--learning-rate*0.001
1,6,python*-u*train.py*--results-subdir*lr_0.0001*--env-id*Hopper-v4*--num-timesteps*10000*--eval-freq*1000*--learning-rate*0.0001
1,6,python*-u*train.py*--results-subdir*lr_1e-05*--env-id*Hopper-v4*--num-timesteps*10000*--eval-freq*1000*--learning-rate*1e-05
```
Condor doesn't like spaces, so we use asterisks instead.

[//]: # (This workflow has several advantages:)

[//]: # (1. It can be used to submit any kind of job, not just RL jobs.)

[//]: # (2. You can use the same `job.sub` script for any job.)

[//]: # (3. You can easily change what command is executed without modifying condor)

## Running Locally

```commandline
conda create -n chtc python=3.9
conda activate chtc
git clone git@github.com:Badger-RL/chtc.git
pip install -e chtc
```
To train an agent:
```commandline
python train.py --env-id InvertedPendulum-v4 --algo ddpg --num-timesteps 10000 --learning-rate 1e-3
```
See `train.py` for command line arguments. By default, results are saved to 
`results/{env_id}/{algorithm}/run_{run_id}`. 
If `run_id` is not specified, the `run_id` is set such that the current run will not overwrite any existing results.
For instance, if `results/CartPole-v1/ddpg/run_0` already exists, results will be saved to `results/CartPole-v1/ddpg/run_1`.
You can change the save directory and add additional subdirectories using `--results-dir` and `--results-subdir` command line arguments.

## Running on CHTC

See [here](https://chtc.cs.wisc.edu/uw-research-computing/python-jobs.html) for a thorough overview of how to set up jobs with CHTC.

CHTC has different protocols depending on how large your code and dependencies are. RL experiments generally use Pytorch (~1 GB), 
which means you'll need to store your code and dependencies `/staging/` and copy them over at the start of each job. 
If you don't have access to `/staging/`, contact CHTC and they'll set it up for you.  

### Getting Dependencies

```commandline
git clone git@github.com:Badger-RL/chtc.git
cd chtc/chtc/condor
condor_submit job_packages.sub
```
Once the job completes, a `packages.tar.gz` tarball containing dependencies will appear in the `condor` directory.
Move (or copy) this tarball to the `/staging/` directory:
```commandline
mv packages.tar.gz /staging/{your chtc username}
```

Alternatively, you could also start an interactive job, 
copy the contents of `job_packages.sub` into the command line,
and then copy the resulting `packages.tar.gz` back to your submit node:
```commandline
condor_submit job_packages.sub -i

...wait for interactive job to start...

# untar your Python installation. Make sure you are using the right version!
tar -xzf python39.tar.gz

# make sure the script will use your Python installation,
# and the working directory as its home location
export PATH=$PWD/python/bin:$PATH
mkdir packages
export PYTHONPATH=$PWD/packages

python3 -m pip install --target=$PWD/packages git+https://github.com/carlosluis/stable-baselines3@fix_tests mujoco pyyaml seaborn
tar -czf packages.tar.gz packages/
scp packages.tar.gz ncorrado@submit1.chtc.wisc.edu:/home/{your chtc username}/

exit # exit interactive job.
```
The `packages.tar.gz` will now be in your home directory on your submit node. Move it it to `/staging/`:
```commandline
mv packages.tar.gz /staging/{your chtc username}
```

### Training

First, we need to pack the code we want to run and transfer it to `/staging/`.
Login to your CHTC submit node, and then:
```commandline
tar czvf chtc.tar.gz chtc
cp chtc.tar.gz /staging/{your chtc username}/
```
Now, we're going to generate the commands we want to execute. 
```commandline
cd chtc/chtc/condor
python generate_commands.py
```
This generates `commands/train.txt`, which contains a list of python commands we want to execute.
In this example, we want to train agents with DDPG (default algorithm) on several MuJoCo environments using two different learning rates:
```commandline
1,6,python*-u*train.py*--results-subdir*lr_0.001*--env-id*Hopper-v4*--num-timesteps*10000*--eval-freq*1000*--learning-rate*0.001
1,6,python*-u*train.py*--results-subdir*lr_0.0001*--env-id*Hopper-v4*--num-timesteps*10000*--eval-freq*1000*--learning-rate*0.0001
...
1,6,python*-u*train.py*--results-subdir*lr_0.0001*--env-id*InvertedDoublePendulum-v4*--num-timesteps*10000*--eval-freq*1000*--learning-rate*0.0001
```
Condor doesn't place nicely with spaces, so replace spaces with "*" here. 
The 1 and 6 are the amount of memory and disk your job needs, respectively.
Different jobs generally have different requirements, passing having them are job parameters is convenient.
To submit 10 job for each of these commands, run
```commandline
./submit.sh train 10
```
Once the jobs finish, results and logs will be stored in `results/train`. 

More generally, you can run a list of commands stored in `my_commands` by placing them in `commands/my_commands.txt` and then running
```commandline
./submit.sh my_commands 10
```
Once the jobs finish, results and logs will be stored in `results/my_commands`. 

### Saving results

Results are returned as `results_{Process}.tar.gz`, where we append the `Process` Condor variable so that 
each file has a unique name and do not overwrite each other when transferred back to the submit node. 
You must make sure the files inside `results_{Process}.tar.gz` also have unique names 
so that your results aren't overwritten when unpack all of your results. 
In this repo, training results are saved to `results/{env_id}/{algorithm}/lr_{learning_rate}/run_{run_id}` where `run_id=Process`, 
so results all have unique names when you unpack your data.

### Interactive jobs

Interactive jobs will ssh you to a CHTC machine so you can test out your code by hand. 
If you get an error in an interactive job, can debug it right away. 
Maybe you forgot to install a dependency -- no problem. Just `pip install` or `conda install` it.
Maybe there's a bug in your code -- again, no problem. Just fix it and rerun. 
Once you have your code working, 
you can piece together the steps required to install and run your code on CHTC in a job submission script 
(`job.sh` in this repo).
