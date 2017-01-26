#!/usr/bin/env bash

function terminate {

    # tar all files                                                                         
    cd ${OUTDIR}
    tar cvjf ${start_dir}/${JOBID}_output.tar.bz2 *
    
    # copy files on stash                                                                    
    #gfal-copy -p file://${G4_FILENAME}.tgz gsiftp://gridftp.grid.uchicago.edu:2811/cephfs/srm/xenon/xenon1t/simulations/mc_$MCVERSION/pax_$PAXVERSION/$MCFLAVOR/$CONFIG/${JOBID}_output.tar.bz2
    
    # Cleanup
    rm -fr $work_dir
    
    cd $start_dir

    exit 0
}


echo "Start time: " `/bin/date`
echo "Job is running on node: " `/bin/hostname`
echo "Job running as user: " `/usr/bin/id`
echo "Job is running in directory: $PWD"

# used to label output
JOBID=$1

# Select MC code flavor
# (G4, NEST, G4p10)
MCFLAVOR=$2

# Specify simulation configuration
# (TPC_Kr83m TPC_Kr85 WholeLXe_Rn220 WholeLXe_Rn222)
CONFIG=$3

# Specify number of events
NEVENTS=$4

# Select MC version
MCVERSION=$5

# Select fax+pax version
PAXVERSION=$6

# Save raw waveforms (0: no, 1: yes)
SAVE_RAW=0
if [[ "$7" == 1 ]]; then
    SAVE_RAW=$7
fi

# runPatch argument corresponding to CONFIG variable above
if [[ ${CONFIG} == *"Kr83m"* ]]; then
    PATCHTYPE=83
elif [[ ${CONFIG} == *"Kr85"* ]]; then
    PATCHTYPE=85
elif [[ ${CONFIG} == *"Rn220"* ]]; then
    PATCHTYPE=21
elif [[ ${CONFIG} == *"Rn222"* ]]; then
    PATCHTYPE=31
fi
 
# preinit file for Geant4
PREINIT=preinit.mac
if [[ ${CONFIG} == *"Cs137"* ]]; then
    PREINIT=preinit_${CONFIG}.mac
elif [[ ${CONFIG} == *"muon"* || ${CONFIG} == *"MV"* ]]; then
    PREINIT=preinit_MV.mac
fi

# set HOME directory if it's not set
if [[ ${HOME} == "" ]];
then
    HOME=$PWD
fi

########################################

# Set pipe to propagate error codes to $?
set -o pipefail

# Setup the software
CVMFSDIR=/cvmfs/xenon.opensciencegrid.org
export PATH="${CVMFSDIR}/releases/anaconda/2.4/bin:$PATH"
source activate mc
if [ $? -ne 0 ];
then
  exit 1
fi

if [[ ${MCFLAVOR} == G4p10 ]]; then
    source ${CVMFSDIR}/software/mc_setup.sh
else
    source ${CVMFSDIR}/software/mc_old_setup.sh
fi
if [ $? -ne 0 ];
then
  exit 2
fi

RELEASEDIR=${CVMFSDIR}/releases/mc/${MCVERSION}
source ${RELEASEDIR}/setup.sh
if [ $? -ne 0 ];
then
  exit 3
fi

# Setting up directories
start_dir=$PWD

OUTDIR=$start_dir/output
mkdir -p  ${OUTDIR}
if [ $? -ne 0 ];
then
  exit 4
fi

if [ "$OSG_WN_TMP" == "" ];
then
    OSG_WN_TMP=$PWD
fi
cd $OSG_WN_TMP

work_dir=`mktemp -d --tmpdir=$OSG_WN_TMP`
cd $work_dir

# Filenaming
SUBRUN=`printf "%05d\n" $JOBID`
FILEROOT=Xenon1T_${CONFIG}
FILENUM=${FILEROOT}_${SUBRUN}
FILENAME=${OUTDIR}/${FILENUM}
G4_FILENAME=${FILENAME}_g4mc_${MCFLAVOR}
G4PATCH_FILENAME=${G4_FILENAME}_Patch
G4NSORT_FILENAME=${G4_FILENAME}_Sort

# Start of simulations #

# Geant4 stage
G4EXEC=${RELEASEDIR}/xenon1t_${MCFLAVOR}
MACROSDIR=${RELEASEDIR}/macros
ln -sf ${MACROSDIR} # For reading e.g. input spectra from CWD
PREINIT_MACRO=${MACROSDIR}/${PREINIT}
OPTICAL_SETUP=${MACROSDIR}/setup_optical_S1.mac
SOURCE_MACRO=${MACROSDIR}/run_${CONFIG}.mac
(time ${G4EXEC} -p ${PREINIT_MACRO} -s ${OPTICAL_SETUP} -f ${SOURCE_MACRO} -n ${NEVENTS} -o ${G4_FILENAME}.root;) 2>&1 | tee ${G4_FILENAME}.log
if [ $? -ne 0 ];
then
  exit 10
fi

# Skip the rest for optical photons
if [[ ${CONFIG} == *"optPhot"* ]]; then
    terminate
fi

source ${CVMFSDIR}/software/mc_old_setup.sh

if [[ ${MCFLAVOR} == NEST ]]; then
    # Patch stage
    if [[ ${PATCHTYPE} != "" ]]; then
        PATCHEXEC=${RELEASEDIR}/runPatch
        (time ${PATCHEXEC} -i ${G4_FILENAME}.root -o ${G4PATCH_FILENAME}.root -t ${PATCHTYPE};) 2>&1 | tee ${G4PATCH_FILENAME}.log
        if [ $? -ne 0 ];
        then
          exit 11
        fi
        PAX_INPUT_FILENAME=${G4PATCH_FILENAME}

    # Some configurations do not require Patch (or are not yet implemented)
    else
        PAX_INPUT_FILENAME=${G4_FILENAME}
    fi
else
    # nSort Stage
    NSORTEXEC=${RELEASEDIR}/nSort
    ln -sf ${RELEASEDIR}/data
    (time ${NSORTEXEC} -s 2 -i ${G4_FILENAME};) 2>&1 | tee ${G4NSORT_FILENAME}.log
    if [ $? -ne 0 ];
    then
      exit 12
    fi
    PAX_INPUT_FILENAME=${G4NSORT_FILENAME}
fi

RAW_FILENAME=${PAX_INPUT_FILENAME}_raw
PAX_FILENAME=${PAX_INPUT_FILENAME}_pax
HAX_FILENAME=${PAX_INPUT_FILENAME}_hax
FAX_FILENAME=${FILENAME}_faxtruth

# fax+pax stages
source deactivate
source activate pax_${PAXVERSION}

# Do not save raw waveforms
if [[ ${SAVE_RAW} == 0 ]]; then
    (time paxer --input ${PAX_INPUT_FILENAME}.root --config_string "[WaveformSimulator]truth_file_name=\"${FAX_FILENAME}\"" --config XENON1T SimulationMCInput --output ${PAX_FILENAME};) 2>&1 | tee ${PAX_FILENAME}.log

    if [ $? -ne 0 ];
    then
	exit 13
    fi

# Save raw waveforms
else
    (time paxer --input ${PAX_INPUT_FILENAME}.root --config_string "[WaveformSimulator]truth_file_name=\"${FAX_FILENAME}\"" --config XENON1T reduce_raw_data SimulationMCInput --output ${RAW_FILENAME};) 2>&1 | tee ${RAW_FILENAME}.log

    if [ $? -ne 0 ];
    then
	exit 14
    fi

    (time paxer --ignore_rundb --input ${RAW_FILENAME} --config XENON1T --output ${PAX_FILENAME};) 2>&1 | tee ${PAX_FILENAME}.log
    
    if [ $? -ne 0 ];
    then
	exit 15
    fi
fi

# Flatten fax truth info
FAXSORT_FILENAME=${FAX_FILENAME}_sort
MEAN_TOP_FRACTION=0.68 # To be improved: https://github.com/XENON1T/mc/issues/20
FAXSORT_OUTPUT_FORMAT=2 # Pickle + ROOT
(time python ${CVMFSDIR}/releases/processing/montecarlo/fax_waveform/TruthSorting.py ${FAX_FILENAME}.root ${FAXSORT_FILENAME} ${MEAN_TOP_FRACTION} ${FAXSORT_OUTPUT_FORMAT};) 2>&1 | tee ${FAXSORT_FILENAME}.log
if [ $? -ne 0 ];
then
    exit 16
fi

# hax stage
HAX_TREEMAKERS="Basics Fundamentals DoubleScatter LargestPeakProperties TotalProperties"

# ROOT output
(time haxer --main_data_paths ${OUTDIR} --input ${PAX_FILENAME##*/} --pax_version_policy loose --treemakers ${HAX_TREEMAKERS} --force_reload;) 2>&1 | tee ${HAX_FILENAME}.log
if [ $? -ne 0 ];
then
  exit 17
fi

# Pickle output
(time haxer --main_data_paths ${OUTDIR} --input ${PAX_FILENAME##*/} --pax_version_policy loose --treemakers ${HAX_TREEMAKERS} --force_reload --preferred_minitree_format pklz;) 2>&1 | tee -a ${HAX_FILENAME}.log
if [ $? -ne 0 ];
then
  exit 18
fi

# Move hax output
mv *.root *.pklz ${OUTDIR} 

terminate
