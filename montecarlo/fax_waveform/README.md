# fax waveform simulation
Repository for scripts to run fax waveform simulation code

You will need the Xenon1T code in order to run this (pax, hax).
In order to run the fax code:
- checkout this repository
- edit the `run_fax.sh` file to change run configurations and software paths

To Use This Branch:

First, you need to change the file_header in setup_production.py and copy_things_around.sh.
This will be where all files will be written (under subfolders for each process).

Also change username in setup_production.py to your midway username.

To produce and merge datasets without changing the config, use begin_production.py:
either hard-code all the options in setup_production.py, change the variable `interactive = 0`, then run `python begin_production.py`,
or just run `python begin_production.py`, and you will be prompted for all the options.

Some confusing options:
`process_name` : this will be the folder name under file_header given to your process
`process_description` : this will be written to a text for your records
`correlated` : this correlates s1 and s2 in time by adding dt, NOT in area
`nodetype` : 0 for xenon1t, 1 for public, 2 for kicp

To tune some parameters in the config, use tune_config_production.py

