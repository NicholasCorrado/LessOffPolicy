commands_file=commands/${1}.txt
results_dir=results/${1}
echo $commands_file
mkdir -p ${results_dir}/logs
condor_submit job.sub \
  results_dir=${results_dir} \
  commands_file=${commands_file} \
  num_jobs=${2:-1}
