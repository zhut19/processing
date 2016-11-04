# osg-montecarlo
Repository for scripts to run xenon1t MC code

You will need the Xenon1T code in order to run this (MC, pax, hax).
In order to run the MC code:
* checkout this repository
* edit the `xenon.submit` file and change queue 10 to the number of trials to run
* edit the `run_sim.sh` file to change run configurations
* submit the `xenon.submit` file using `condor_submit` or `connect submit`
