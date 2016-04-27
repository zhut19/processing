# osg-reconstruction
Code and scripts to do Xenon1T reconstruction on OSG

## Pre-requisites

A CI-Connect/OSG account:

 https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:cmp:computing:midway_cluster:instructions

This workflow assumes you have already staged the raw data on Stash (login.ci-connect.uchicago.edu) at /xenon, our SRM endpoint location. Furthermore, this workflow uses GRID transfer protocols for efficient data transfer from this SRM to compute nodes, so you must have a valid GRID certificate obtained following instructions here:

 https://xecluster.lngs.infn.it/dokuwiki/doku.php?id=xenon:xenon1t:sim:grid

and certificate/key files copied to ~/.globus on login.ci-connect.uchicago.edu

## Instructions 
 
Let's work on Stash:
```
ssh login.ci-connect.uchicago.edu # Using your CI-Connect credentials
cd stash
git clone https://github.com/XENON1T/processing.git 
cd processing/reconstruction
```

### XENON100 Processing

First generate the list of runs and sub-files you wish to process from a given directory:
```
./generate_run_info.py --run-directory <Directory containing XENON100 dataset directories, e.g. /xenon/run_14_test>
```
This creates a directory called "info", containing .csv files for each dataset. Each .csv file further contains the list of .xed subruns to process.

Initialize your GRID certificate:
```
voms-proxy-init  -voms xenon.biggrid.nl -valid 168:00 -out user_cert 
```
Note the maximum time of 1 week, so if your jobs stay in queue for longer than that, you should re-run this command well before they start.

Then create the job submission file:
```
./pax_process_XENON100.py --run <Name of last directory in previous command, e.g. run_14_test> --dataset <specific dataset or "all"> --info-directory info --batch-size <number of files per job, def=15> --pax-version 4.9.1 --config <pax config given by 'paxer --help', or custom file ending in .ini>
```
Note, a custom config file must be located in the current working directory with no directory structure given to the argument.

This produces a job submission file called process_run.submit, which you should check for correctness.

Furthermore, to test the workflow, you may reduce the number of datasets/subfiles processed, as well as uncommenting "--stop_after 2" in run_pax.sh.

Submit the jobs:
```
condor_submit process_run.submit
```

Check their status:
```
condor_q
```

Logs and output ROOT files will appear in "log" and "results" directories, respectively.

### XENON1T Processing

Coming soon...


## Script Details

### pax_process.py
script to generate HTCondor submit files to run reconstruction of a run or a dataset within a run

| Arguments | Notes | 
| :-------: | :---: |
| --pax-version | the version of pax to use |
| --info-directory | the path to the directory with information on xed files associated with runs, datasets |
| --batch-size | the number of xed files to process per job (this should be chosen so that jobs will run for about 2-3 hours, the default of 15 should work) |
| --run | the run number to process |
| --dataset | the data set to process, use 'all' as an argument to process all the datasets for a run |

 
 Once the submit file has been generated, you will need to generate a voms proxy using: 
 ``` voms-proxy-init -voms xenon.biggrid.nl -valid 168:00 -out user_cert ```
 
### generate_run_info.py
The `pax_process` script requires csv files with information about xed files associated with a run and datasets within 
the run. `generate_run_info.py` generates these csv files.  Call it using `generate_run_info.py --run-directory <run_directory>` 
where `<run_directory>` is the location of the directory with the xed files for a given run.  This will put the csv files 
in the current directory.

### run_pax.sh
Job script run on compute nodes to load and run PAX with appropriate arguments and outputs


