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
python mc_process.py --flavor <G4, NEST, G4p10> --config <MACRO_NAME> --batch-size <JOB_BATCH_SIZE> --events <TOTAL_NUM_EVENTS> --mc-version <MC_VERSION> --pax-version <PAX_VERSION> --grid-type osg
~~~~
where ```MACRO_NAME``` is the string between ```run_``` and ```.mac``` of any of the macros here: https://github.com/XENON1T/mc/tree/master/macros

Instructions for passing a custom macro to come...

8) Check job status with:
~~~~
condor_q
pegasus-status -l /scratch/${USER}/<production_name>/processing/montecarlo/${USER}/pegasus/montecarlo
~~~~

9) Output should appear in:
~~~~
/scratch/${USER}/<production_name>/processing/montecarlo/output/${USER}/pegasus/montecarlo/*/
~~~~


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
    MC_CONFIG: TPC_Kr83m, TPC_Kr85, WholeLXe_Rn220, WholeLXe_Rn222 (more configurations to come soon)
    NUM_EVENTS: Number of events 
    MC_VERSION: MC GitHub release number (https://github.com/XENON1T/mc/releases)
    PAX_VERSION: pax (also fax) GitHub release number (https://github.com/XENON1T/pax/releases)
    SAVE_WAVEFORMS: Flag to save raw waveforms (disk space intensive); 0 - off (default), 1 - on
~~~~

This will create output files in "output" directory.

We advise to run this in the [batch queue or interactive job](https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:analysis:beginnersguide#the_midway_batch_queue)
