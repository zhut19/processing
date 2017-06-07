# MC Simulation Production
Repository for scripts to run xenon1t MC code

## Instructions

### Grid production

1) Get a CI-Connect account (second step after your Midway account):

https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:cmp:computing:midway_cluster:instructions

2) ssh to:
~~~~
login.xenon.ci-connect.net
~~~~
or ```login.ci-connect.uchicago.edu``` to [add your SSH key](https://www.debian.org/devel/passwordlessssh) first, if above fails.

3) Create your scratch space:
~~~~
mkdir /scratch/${USER}
~~~~

4) Create new directory for your production:
~~~~
mkdir /scratch/${USER}/<production_name>
~~~~

5) Checkout this repository
~~~~
cd /scratch/${USER}/<production_name>
git clone https://github.com/XENON1T/processing.git
~~~~

6) Switch to MC directory
~~~~
cd processing/montecarlo
~~~~

7) Submit jobs (this creates one master job (DAG) which then submits the rest):
~~~~
python mc_process.py --flavor <MC_FLAVOR> --config <MC_CONFIG> --batch-size <JOB_BATCH_SIZE> --events <NUM_EVENTS> --mc-version <MC_VERSION> --fax-version <FAX_VERSION> --pax-version <PAX_VERSION> --grid-type <GRID_TYPE> --preinit-macro <PREINIT_MACRO> --preinit-belt <PREINIT_BELT> --preinit-efield <PREINIT_EFIELD> --optical-setup <OPTICAL_SETUP> --source-macro <SOURCE_MACRO>
~~~~
where 
~~~~
    MC_FLAVOR: NEST, G4 (without NEST), G4p10 (latest Geant4.10 without NEST)
    MC_CONFIG: the string between ```run_``` and ```.mac``` of any of the macros here: https://github.com/XENON1T/mc/tree/master/macros
    JOB_BATCH_SIZE: Number of events per job (default=2000 should be fine for most users running the full chain)
    NUM_EVENTS: Total number of events (summed over all jobs)
    MC_VERSION: MC GitHub release number (https://github.com/XENON1T/mc/releases)
    FAX_VERSION: fax GitHub release number (default=PAX_VERSION)
    PAX_VERSION: pax (also fax if not specified above) GitHub release number (https://github.com/XENON1T/pax/releases)
    GRID_TYPE: osg (US grid), egi (EU grid)
    PREINIT_MACRO: (Optional) name of macro to use for Geant4 preinit (defaults to preinit_TPC.mac)
    PREINIT_BELT: (Optional) name of macro for setting up calibration belts (defaults to preinit_B_none.mac or depending on MC_CONFIG)
    PREINIT_EFIELD: (Optional) name of macro for varying e-field in NEST (defaults to preinit_EF_C15kVA4kV.mac)
    OPTICAL_SETUP: (Optional) name of macro to use for Geant4 optical setup (defaults to setup_optical_S1.mac)
    SOURCE_MACRO: (Optional) name of macro to run in Geant4 (defaults to run_<MC_CONFIG>.mac)
~~~~
For example:
~~~~
python mc_process.py --flavor G4 --config AmBe_neutronISO --events 1000000 --mc-version v0.1.7 --pax-version v6.2.1 --grid-type osg
~~~~

8) Check job status with:
~~~~
condor_q
pegasus-status -l /scratch/${USER}/<production_name>/processing/montecarlo/${USER}/pegasus/montecarlo
~~~~

9) Output should eventually appear in:
~~~~
/scratch/${USER}/<production_name>/processing/montecarlo/output/${USER}/pegasus/montecarlo/*
~~~~
and ongoing job logs in:
~~~~
/scratch/${USER}/<production_name>/processing/montecarlo/${USER}/pegasus/montecarlo/*
~~~~

10) Once everything's complete and verified (e.g. checked logs for errors), we will want to keep all the results on Midway for all analysts to access. You may either use:
  a) ```rsync``` to directly copy to Midway, or
  b) copy results to ```/stash/user/${USER}``` then use Globus (https://globus.rcc.uchicago.edu/globus-app)
~~~~
Source Endpoint: OSG Connect Stash
Destination Endpoint: UChicago RCC Midway
~~~~
which can queue several transfers and maximizes the bandwidth usage. More details about using Globus online can be found here: https://rcc.uchicago.edu/docs/data-transfer/index.html#globus-online

The official location will be ```/project2/lgrandi/xenon1t/simulations```; please follow the existing directory structure within, e.g.:
~~~~
/project2/lgrandi/xenon1t/simulations/mc_v<MC_VERSION>/pax_v<PAX_VERSION>/<MC_FLAVOR>/<MC_CONFIG>
~~~~
and ensure you set the group appropriately
~~~~
chgrp -R pi-lgrandi /project2/lgrandi/xenon1t/simulations
~~~~

11) Once you have completed and verified the transfer, clean up your space:
~~~~
rm -rf /scratch/${USER}
~~~~

12) Untar all the files after transferred: 
~~~~
for f in *; do tar xf $f; done
~~~~
(and delete the tarballs after verified to save disk space). And organize them using this script:
~~~~
/project/lgrandi/xenon1t/simulations/organize.sh
~~~~

13) Keep track and share the details of your production here https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:sim:data

### Midway local running

You may run locally on Midway with e.g.:
~~~~
    cd processing/montecarlo/
    ./run_sim.sh <Job_Number> <MC_FLAVOR> <MC_CONFIG> <NUM_EVENTS> <MC_VERSION> <FAX_VERSION> <PAX_VERSION> <SAVE_WAVEFORMS> <PREINIT_MACRO> <PREINIT_BELT> <PREINIT_EFIELD> <OPTICAL_SETUP> <SOURCE_MACRO>
~~~~
where
~~~~
    Job_Number: Unique job identifier that goes into filename
    MC_FLAVOR: NEST, G4 (without NEST), G4p10 (latest Geant4.10 without NEST)
    MC_CONFIG: the string between ```run_``` and ```.mac``` of any of the macros here: https://github.com/XENON1T/mc/tree/master/macros
    NUM_EVENTS: Number of events 
    MC_VERSION: MC GitHub release number (https://github.com/XENON1T/mc/releases)
    FAX_VERSION: fax GitHub release number (default=PAX_VERSION)
    PAX_VERSION: pax (also fax if not specified above) GitHub release number (https://github.com/XENON1T/pax/releases)
    SAVE_WAVEFORMS: Flag to save raw waveforms (disk space intensive); 0 - off (default), 1 - on
    PREINIT_MACRO: (Optional) name of macro to use for Geant4 preinit (defaults to preinit_TPC.mac)
    PREINIT_BELT: (Optional) name of macro for setting up calibration belts (defaults to preinit_B_none.mac or depending on MC_CONFIG)
    PREINIT_EFIELD: (Optional) name of macro for varying e-field in NEST (defaults to preinit_EF_C15kVA4kV.mac)
    OPTICAL_SETUP: (Optional) name of macro to use for Geant4 optical setup (defaults to setup_optical_S1.mac)
    SOURCE_MACRO: (Optional) name of macro to run in Geant4 (defaults to run_<MC_CONFIG>.mac)
~~~~

This will create output files in "output" directory.

We advise to run this in the [batch queue or interactive job](https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:analysis:beginnersguide#the_midway_batch_queue)
