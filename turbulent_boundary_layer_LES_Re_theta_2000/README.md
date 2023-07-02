## Setup:
```console
$ makenek flat_plate
```

## Run:
```console
$ sbatch jobcode
```

## Plot:
Use paraview to manually plot or use the `plot_tbl_main.py` script. Example usage:
- To animate all frames serially:
```console
$ python plot_tbl_main.py --data 'flat_plate.nek5000' --output 'frames/q_criterion_view_4' --q-criterion --iso-u --animate --view 4
```
- To animate all frames in parallel
```console
$ sbatch jobcode-render
```
- To plot a single time step
```console
$ python plot_tbl_main.py --data 'flat_plate.nek5000' --output 'frames/q_criterion_view_4' --q-criterion --iso-u --timestep 10 --view 4
```
