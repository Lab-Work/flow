# Usage

## To generate random IDM paramters
```bash
python generate_data.py num_of_simulations
```
The above command will generate the num_of_simulations sets of IDM parametrs in the output file called IDMinputParams.csv

## To run multiple sims
```bash
. exec_sim.sh
```
The above command will create all the necessary csv files in the data directory.

## TO DO
- [ ] create reference data file from default paramter set
- [ ] generate 10 sim data files for analysis
- [ ] write script to plot generate macroscopic information from the data and plots necessary graphs
- [ ] write script that attempts to predict initial parameters based on macro results and then generates output statistics regarding accuracy
