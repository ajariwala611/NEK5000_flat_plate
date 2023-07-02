#!/bin/bash
#SBATCH -J vistest # 8-character name
#SBATCH -o slog # output and error file name (%j expands to jobID)
#SBATCH -e serr
#SBATCH -N 8 # total number of nodes
#SBATCH -n 83 # total number of mpi tasks requested
#SBATCH -p normal # queue (partition) -- normal, development, etc.
#SBATCH -t 00:05:00 # run time (hh:mm:ss)
#SBATCH -A OTH21032 # Project number

#SBATCH --mail-user=akshit@utexas.edu
#SBATCH --mail-type=end     # email me when the job finishes

export PYTHONPATH=/home1/08302/akshit06/ParaView-5.10.1-osmesa-MPI-Linux-Python3.9-x86_64/lib/python3.9/site-packages:$PYTHONPATH

#ibrun python plot_tbl_main.py --parallel --data 'flat_plate.nek5000' --output 'frames/rpi_t1' --slice1 --slice2 --q-criterion --animate --view 1
#mpirun -np 1 python write_csv.py --data '1910/flat_plate.nek5000' --output '1910/nek_data/slice_Re_1910' --slice1 --timestep 45 --view 1
ibrun python write_csv.py --parallel --data 'flat_plate.nek5000' --output 'slice_6D/slice_Re_6365' --slice1 --animate --view 1
#ibrun python plot_tbl_main.py --parallel --data 'flat_plate.nek5000' --output 'frames/q_criterion_front_view' --animate --view 3 > log
