#!/bin/bash

#SBATCH -N 1            # number of nodes
#SBATCH -c 16            # number of cores 
#SBATCH -t 0-01:00:00   # time in d-hh:mm:ss
#SBATCH --mem=128G      # memory for all cores in GB
#SBATCH -q public       # QOS
#SBATCH -o slurm.%j.out # file to save job's STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err # file to save job's STDERR (%j = JobId)
#SBATCH --export=NONE   # Purge the job-submitting shell environment

# Load required modules for job's environment
module load mamba/latest
# Using python, so source activate an appropriate environment
source activate rs23

python /scratch/kdahal3/wetland/process_raster.py $1
