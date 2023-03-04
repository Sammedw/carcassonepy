#!/bin/bash
#
#SBATCH --job-name=carcassonne # Job name for tracking
#SBATCH --partition=cpu-batch  # Partition you wish to use (see above for list)
#SBATCH --cpus-per-task=40     # Number of CPU threads used by your job, set this upto 40 as required.
#SBATCH --mem=6000            # 60GB RAM
#SBATCH --exclusive=mcs        # Exclusive mode, only this job will run
#SBATCH --time=2-00:00:00      # Job time limit set to 2 days (48 hours)
#
#SBATCH --mail-type=END,FAIL,TIME_LIMIT_80 # Events to send email on, remove if you don't want this
#SBATCH --output=joboutput_%j.out # Standard out from your job
#SBATCH --error=joboutput_%j.err  # Standard error from your job

## Initialisation ##
source /etc/profile.d/modules.sh
source /etc/profile.d/conda.sh

## Execute your program(s) ##
# srun python3 -c "print('hello')"
## Other examples:
## A Python program
srun /bin/python3.9 /dcs/20/u2013334/Documents/CS310/carcassonepy/test.py -l config.txt
#
## Excutable program (e.g. with shebang or written in C/C++)
# srun ~/myprogram