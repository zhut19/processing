# fax waveform simulation
Repository for scripts to run fax waveform simulation code

You will need the Xenon1T code in order to run this (pax, hax).
In order to run the fax code:
- checkout this repository
- edit the `run_fax.sh` file to change run configurations and software paths

# This Branch
This branch (hopefully) can be used to run Qing's fax production code in one command (after some editing). There are two main scripts:
- `begin_production.py` just runs each of the production scripts in succession, passing options you can set in a dictionary.
- `tune_config_production.py` allows you to loop over several values of some config parameters, running the production code for each set of values.

## Using this branch

### Setting up
- First, you need to change the `file_header` in `setup_production.py` and `copy_things_around.sh`. This will be where all files will be written (under subfolders for each process).
- Also change username in `setup_production.py` to your midway username.

### To produce and merge datasets without changing the config, use `begin_production.py`
- This code imports `setup_production.py`, which creates a dictionary of options to be passed to fax/pax/hax through Qing's production scripts.
- You can hard-code all the options in `setup_production.py`, change the variable `interactive = 0`, then run `python begin_production.py`.
- Or you can just run `python begin_production.py`, and you will be prompted for all the options.

#### Some confusing options:
- `process_name` : this will be the folder name under `file_header` given to your process
- `process_description` : this will be written to a text for your records
- `correlated` : this correlates s1 and s2 in time by adding dt, NOT in area
- `nodetype` : 0 for xenon1t, 1 for public, 2 for kicp

### To tune some parameters in the config, use `tune_config_production.py`
- This code edits the `config_string` passed to paxer by `run_fax.sh` by directly editing `run_fax.sh`. It allows you to loop over several values of whatever config parameter(s) you are interested in.
- Edit the `pars_to_change` dict so that they keys are the names of the parameters you want to change, and they each key to a list of the values you want that parameter to take.
- Edit the other dictionary options in the loop (these are mostly the same as in `setup_production.py`)

