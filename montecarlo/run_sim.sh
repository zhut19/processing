#!/usr/bin/env bash
echo "Start time: " `/bin/date`
echo "Job is running on node: " `/bin/hostname`
echo "Job running as user: " `/usr/bin/id`
echo "Job is running in directory: $PWD"

# Select MC version
MCVERSION=v0.0.5

# Select MC code flavor
# (G4, NEST, G4p10)
MCFLAVOR=NEST

# Select fax+pax version
PAXVERSION=v6.0.2

# Specify number of events
NEVENTS=10

# Specify simulation configuration
# (TPC_Kr83m TPC_Kr85 WholeLXe_Rn220 WholeLXe_Rn222)
CONFIG=TPC_Kr83m

# runPatch argument corresponding to CONFIG variable above
# (83 85 21 31)
PATCHTYPE=83

########################################

# Setup the software
CVMFSDIR=/cvmfs/xenon.opensciencegrid.org
export PATH="${CVMFSDIR}/releases/anaconda/2.4/bin:$PATH"
source activate mc &> /dev/null

if [[ ${MCFLAVOR} == G4p10 ]]; then
    source ${CVMFSDIR}/software/mc_setup.sh
else
    source ${CVMFSDIR}/software/mc_old_setup.sh
fi

RELEASEDIR=${CVMFSDIR}/releases/mc/${MCVERSION}
source ${RELEASEDIR}/setup.sh

# Setting up directories
start_dir=$PWD

OUTDIR=$start_dir/output
mkdir -p  ${OUTDIR}

if [ "$OSG_WN_TMP" == "" ];
then
    OSG_WN_TMP=$PWD
fi
cd $OSG_WN_TMP

work_dir=`mktemp -d --tmpdir=$OSG_WN_TMP`
cd $work_dir

# Filenaming
FILEROOT=Xenon1T_${CONFIG}
SUBRUN=`printf "%06d\n" $1`
FILENUM=${FILEROOT}_${SUBRUN}
FILENAME=${OUTDIR}/${FILENUM}
G4_FILENAME=${FILENAME}_g4mc_${MCFLAVOR}
G4PATCH_FILENAME=${FILENAME}_g4mcpatch
G4NSORT_FILENAME=${FILENAME}_Sort
PAX_FILENAME=${FILENAME}_pax
HAX_FILENAME=${FILENAME}_hax

# Start of simulations #

# Geant4 stage
G4EXEC=${RELEASEDIR}/xenon1t_${MCFLAVOR}
MACROSDIR=${RELEASEDIR}/macros
(time ${G4EXEC} -p ${MACROSDIR}/preinit.mac -f ${MACROSDIR}/run_${CONFIG}.mac -n ${NEVENTS} -o ${G4_FILENAME}.root;) &> ${G4_FILENAME}.log

if [[ ${MCFLAVOR} == NEST ]]; then
    # Patch stage
    PATCHEXEC=${RELEASEDIR}/runPatch
    (time ${PATCHEXEC} -i ${G4_FILENAME}.root -o ${G4PATCH_FILENAME}.root -t ${PATCHTYPE};) &> ${G4PATCH_FILENAME}.log
    PAX_INPUT_FILENAME=${G4PATCH_FILENAME}
else
    # nSort Stage
    NSORTEXEC=${RELEASEDIR}/nSort
    ln -sf ${RELEASEDIR}/data
    (time ${NSORTEXEC} ${G4_FILENAME} 1 1 0 0 0;) &> ${G4NSORT_FILENAME}.log
    PAX_INPUT_FILENAME=${G4NSORT_FILENAME}
fi

# fax+pax stage
source deactivate &> /dev/null
source activate pax_${PAXVERSION} &> /dev/null
(time paxer --input ${PAX_INPUT_FILENAME}.root --config_string "[WaveformSimulator]truth_file_name=\"${FILENAME}_faxtruth.csv\"" --config XENON1T SimulationMCInput --output ${PAX_FILENAME};) &> ${PAX_FILENAME}.log

# hax stage
HAXPYTHON="import hax; "
HAXPYTHON+="hax.init(main_data_paths=['${OUTDIR}'], minitree_paths=['${OUTDIR}'], pax_version_policy = 'loose'); "
HAXPYTHON+="hax.minitrees.load('${FILENUM}_pax', ['Basics', 'Fundamentals']);"

python -c "${HAXPYTHON}"

hadd ${HAX_FILENAME}.root ${PAX_FILENAME}_*


# Cleanup
rm -f pax*


cd $start_dir
rm -fr $work_dir
