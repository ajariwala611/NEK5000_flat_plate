#!/bin/bash
#SBATCH -J vistest # 8-character name
#SBATCH -o slog # output and error file name (%j expands to jobID)
#SBATCH -e serr
#SBATCH -N 1 # total number of nodes
#SBATCH -n 8 # total number of mpi tasks requested
#SBATCH -p normal # queue (partition) -- normal, development, etc.
#SBATCH -t 02:00:00 # run time (hh:mm:ss)
#SBATCH -A OTH21032 # Project number

#SBATCH --mail-user=akshit@utexas.edu
#SBATCH --mail-type=end     # email me when the job finishes

export PYTHONPATH=/home1/08302/akshit06/ParaView-5.10.1-osmesa-MPI-Linux-Python3.9-x86_64/lib/python3.9/site-packages:$PYTHONPATH

ibrun python plot_tbl_main.py --parallel --data 'flat_plate.nek5000' --output 'frames1/test_q' --q-criterion --animate --view 1
#ibrun python plot_tbl_main.py --parallel --data 'flat_plate.nek5000' --output 'frames/q_criterion_front_view' --animate --view 3 > log
