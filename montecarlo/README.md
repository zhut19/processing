# MC Simulation Production
Repository for scripts to run xenon1t MC code

## Instructions



### OSG submission 

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
python mc_process.py --flavor <MC_FLAVOR> --config <MC_CONFIG> --batch-size <JOB_BATCH_SIZE=2000> --events <NUM_EVENTS> --mc-version <MC_VERSION> --pax-version <PAX_VERSION> --grid-type osg
~~~~
where 
~~~~
    MC_FLAVOR: NEST, G4 (without NEST), G4p10 (latest Geant4.10 without NEST)
    MC_CONFIG: the string between ```run_``` and ```.mac``` of any of the macros here: https://github.com/XENON1T/mc/tree/master/macros
    JOB_BATCH_SIZE: Number of events per job (default=2000 should be fine for most users running the full chain)
    NUM_EVENTS: Total number of events (summed over all jobs)
    MC_VERSION: MC GitHub release number (https://github.com/XENON1T/mc/releases)
    PAX_VERSION: pax (also fax) GitHub release number (https://github.com/XENON1T/pax/releases)
~~~~
For example:
~~~~
python mc_process.py --flavor G4 --config AmBe_neutronISO --batch-size 2000 --events 1000000 --mc-version v0.1.3 --pax-version v6.2.1 --grid-type osg
~~~~
Instructions for passing a custom macro to come...

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

10) Once everything's complete, copy tarballs to Midway using ```rsync``` or https://globus.rcc.uchicago.edu/globus-app/
~~~~
Source Endpoint: OSG Connect Stash
Destination Endpoint: UChicago RCC Midway
~~~~
More details about using Globus online can be found here: https://rcc.uchicago.edu/docs/data-transfer/index.html#globus-online

The official location will be ```/project/lgrandi/xenon1t/simulations```; please follow the existing directory structure within, e.g.:
~~~~
/project/lgrandi/xenon1t/simulations/mc_v<MC_VERSION>/pax_v<PAX_VERSION>/<MC_FLAVOR>/<MC_CONFIG>
~~~~
and ensure you set the group appropriately
~~~~
chgrp -R pi-lgrandi /project/lgrandi/xenon1t/simulations
~~~~

11) Untar all the files after transferred: 
~~~~
for f in *; do tar xf $f; done
~~~~
(and delete the tarballs after verified to save disk space). And organize them using this script:
~~~~
/project/lgrandi/xenon1t/simulations/organize.sh
~~~~

12) Keep track and share the details of your production here https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:sim:data

### EGI submission 

(Under construction...)

In order to submit jobs on the EGI sites, you first have to:

1) get a certificate

2) register at the XENON VO

3) initiate a proxy
~~~~
Detailed instructions can be found here: https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:sim:grid
~~~~
To submit jobs from xe-grid01:
~~~~
cd processing/montecarlo/
./mc_process.py --flavor <MC_FLAVOR> --config <MC_CONFIG> --events <NUM_EVENTS> --mc-version <MC_VERSION> --pax-version <PAX_VERSION> --grid-type <GRID_TYPE>
with <GRID_TYPE> = egi
~~~~
After the submission, there will be created two folders (if they don't exist yet): 
~~~~
jdl_files: contains the .jdl file for each submitted job
job_id: contains the job_ids.txt file that contains the ID of all the submitted jobs
~~~~
The .jdl and .txt files are automatically generated/updated by the script.

You can check job status with e.g
~~~
glite-wms-job-status -i job_id/job_ids.txt --noint
~~~

If you are not explicitly copying results out at the bottom of run_sim.sh, then you can grab the files with
~~~
glite-wms-job-output --dir output -i job_id/job_ids.txt --noint
~~~

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
    MC_CONFIG: the string between ```run_``` and ```.mac``` of any of the macros here: https://github.com/XENON1T/mc/tree/master/macros
    NUM_EVENTS: Number of events 
    MC_VERSION: MC GitHub release number (https://github.com/XENON1T/mc/releases)
    PAX_VERSION: pax (also fax) GitHub release number (https://github.com/XENON1T/pax/releases)
    SAVE_WAVEFORMS: Flag to save raw waveforms (disk space intensive); 0 - off (default), 1 - on
~~~~

This will create output files in "output" directory.

We advise to run this in the [batch queue or interactive job](https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:analysis:beginnersguide#the_midway_batch_queue)
