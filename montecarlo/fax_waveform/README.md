# fax waveform simulation
Repository for scripts to run fax waveform simulation code

You will need the Xenon1T code in order to run this (pax, hax).
In order to run the fax code:
* checkout this repository
* edit the `MidwayBatch.py` file to adjust script paths
* edit the `run_sim.sh` file to change run configurations and software paths
* Run: "python MidwayBatch.py <output directory> <number of jobs> <partition: 0 (xenon1t), 1 (public), 2 (kicp)"
