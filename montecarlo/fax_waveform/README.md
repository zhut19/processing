# fax waveform simulation
Repository for scripts to run fax waveform simulation code

You will need the Xenon1T code in order to run this (pax, hax).
In order to run the fax code:
- checkout this repository
- edit the `run_fax.sh` file to change run configurations and software paths
- Run: "python MidwayBatch.py (output directory) (number of jobs) (partition: 0 [xenon1t], 1 [public], 2 [kicp])"




### Produce and Merge Datasets with `begin_production.py`
You can use this code to produce fax-only data with Qing's framework in one terminal command (after some editing).

#### Setting Up
- Change the lines containing `username` and `file_header` in `sort_processed_files.sh`. `username` should be your midway username (to check squeue), and `file_header` is where all your produced data will appear (under a subdir defined by `process_name`)

#### Running the Code
- This code imports `setup_production.py`, which creates a dictionary of options to be passed to fax/pax/hax through Qing's production scripts.
- You can hard-code all the options in `setup_production.py`, change the variable `interactive = 0`, then run `python begin_production.py`.
- Or you can just run `python begin_production.py`, and you will be prompted for all the options.

#### Some confusing options:
- `process_name` : this will be the folder name under `file_header` given to your process
- `process_description` : this will be written to a text for your records
- `correlated` : this correlates s1 and s2 in time by adding dt, NOT in area
- `nodetype` : 0 for xenon1t, 1 for public, 2 for kicp
- `use_array_truth` : set to 1 to put truth information in arrays
- `minitree_type` : 0 for basics, 1 for S1S2Properties minitrees, 2 for PeakEfficiency minitrees
