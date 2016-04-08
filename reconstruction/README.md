# osg-reconstruction
Code and scripts to do Xenon1T reconstruction on OSG

## pax_process.py
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
 
## generate_run_info.py
The `pax_process` script requires csv files with information about xed files associated with a run and datasets within 
the run. `generate_run_info.py` generates these csv files.  Call it using `generate_run_info.py --run-directory <run_directory>` 
where `<run_directory>` is the location of the directory with the xed files for a given run.  This will put the csv files 
in the current directory.

## run_pax.sh
Job script run on compute nodes to load and run PAX with appropriate arguments and outputs


