# osg-montecarlo
Repository for code to run xenon1t ROOT monte carlo code

You will need the Xenon1T 3.7A code in order to run this. A tarball with file is included in this repo.
In order to run the monte carlo code:
* checkout this repository
* edit the `xenon.submit` file and change queue 10 to the number of trials to run
* edit the `xenon.submit` file to change the references to `run_Cryostat_neutron.mac` to the macro file that should be used and place that macro in this directory
* submit the `xenon.submit` file using `condor_submit` or `connect submit`
