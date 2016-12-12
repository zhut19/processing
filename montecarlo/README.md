# MC Simulation Production
Repository for scripts to run xenon1t MC code

## Instructions

* Checkout this repository
~~~~
    git clone https://github.com/XENON1T/processing.git
~~~~

### OSG/EGI submission 

Detailed instructions to come...
~~~~
    https://github.com/XENON1T/processing/blob/master/montecarlo/mc_process.py
~~~~

### EGI submission 
~~~~
In order to submit jobs on the EGI sites, you first have the following three steps:
1) get a certificate
2) register at the XENON VO
3) initiate a proxy
Detailed instructions can be found here: https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:sim:grid

~~~~

### Midway local running

You may run locally on Midway with e.g.:
~~~~
    cd processing/montecarlo/
    ./run_sim.sh <Job_Number> <MC_FLAVOR> <MC_CONFIG> <NUM_EVENTS> <MC_VERSION> <PAX_VERSION> <SAVE_WAVEFORMS>
~~~~
where
~~~~
    Job_Number: Unique job identifier that goes into filename
    MC_FLAVOR: NEST, G4 (without NEST), G4p10 (latest Geant4.10 without NEST)
    MC_CONFIG: TPC_Kr83m, TPC_Kr85, WholeLXe_Rn220, WholeLXe_Rn222 (more configurations to come soon)
    NUM_EVENTS: Number of events 
    MC_VERSION: MC GitHub release number (https://github.com/XENON1T/mc/releases)
    PAX_VERSION: pax (also fax) GitHub release number (https://github.com/XENON1T/pax/releases)
    SAVE_WAVEFORMS: Flag to save raw waveforms (disk space intensive); 0 - off (default), 1 - on
~~~~

This will create output files in "output" directory.

We advise to run this in the [batch queue or interactive job](https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:analysis:beginnersguide#the_midway_batch_queue)
