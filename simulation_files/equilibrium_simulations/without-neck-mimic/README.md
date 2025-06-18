# Simulation Files

This directory contains the files necessary to run the coarse-grained
molecular dynamics equilibrium simulations:

- gro: contains the structure files for the free and alf3 states
- top: contains the topology and force field files for the corase-grained models
- inp: contains input files for running coarse-grained molecular dynamics simulations in GENESIS

# Usage
To run the simulations, please compile GENESIS v2.0 or greater. Change the seed value
from XXXX to any positive integer number, and then, perform each simulation as follows:

```bash
mpirun -np N /path/to/atdyn /path/to/inp/file
```

where N is the number of MPI processes to use. For 1 MPI, assuming you are inside
the inp directory and atdyn was copied there, you would need to execute:

```bash
mpirun -np 1 ./atdyn ./alf3.inp
mpirun -np 1 ./atdyn ./free.inp
```

### Note
In this work we used seed values from 1 to 100.
