#!/bin/bash
#SBATCH -J vistest # 8-character name
#SBATCH -o slog # output and error file name (%j expands to jobID)
#SBATCH -e serr
#SBATCH -N 8 # total number of nodes
#SBATCH -n 64 # total number of mpi tasks requested
#SBATCH -p normal # queue (partition) -- normal, development, etc.
#SBATCH -t 02:00:00 # run time (hh:mm:ss)
#SBATCH -A OTH21032 # Project number

#SBATCH --mail-user=atsolovikos@gmail.com
#SBATCH --mail-type=all     # email me when the job finishes

export PYTHONPATH=/home1/05868/atsol/ParaView-5.10.0-egl-MPI-Linux-Python3.9-x86_64/lib/python3.9/site-packages:$PYTHONPATH

ibrun python plot_tbl_main.py --parallel --data 'flat_plate.nek5000' --output 'frames/q_criterion_view_4' --q-criterion --iso-u --animate --view 4
#ibrun python plot_tbl_main.py --parallel --data 'flat_plate.nek5000' --output 'frames/q_criterion_front_view' --animate --view 3 > log
