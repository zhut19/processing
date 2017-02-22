#!/usr/bin/env bash
############################################
#
# Usage: Need to modify all parameters and paths below, then:
#           ./run_fax.sh <output directory> <subrun number>
#
############################################

echo "Start time: " `/bin/date`
echo "Job is running on node: " `/bin/hostname`
echo "Job running as user: " `/usr/bin/id`
echo "Job is running in directory: $PWD"

###### General parameters #####
Detector=XENON1T

###### Simulation parameters #####
Input2DBandFile=$1
Nomial_g1=$2
Nomial_g2=$3

RecoilType=ER

PMTAfterpulseEnableFlag=$4
S2AfterpulseEnableFlag=$5

# Select fax+pax version
#~ PAXVERSION=head
PAXVERSION=v6.5.0 # temporary change

# Specify number of events
NumEvents=$6

# This run number (from command line argument)
SUBRUN=$8

########################################

# Setup the software
CVMFSDIR=/cvmfs/xenon.opensciencegrid.org
#export PATH="${CVMFSDIR}/releases/anaconda/2.4/bin:$PATH"
export PATH="/project/lgrandi/anaconda3/bin:$PATH"
source activate pax_${PAXVERSION} &> /dev/null

# Use path of this script for Python scripts below
# (In case user modified them)
#MY_PATH=`dirname \"$0\"`
MY_PATH=$(cd `dirname $0`; pwd)
echo $MY_PATH
RELEASEDIR=`( cd "$MY_PATH" && pwd )`

# Setting up directories
#start_dir=$PWD


OUTDIR=$7/${SUBRUN}
mkdir -p ${OUTDIR}
cd ${OUTDIR}

#if [ "$OSG_WN_TMP" == "" ];
#then
#    OSG_WN_TMP=$PWD
#fi
#cd $OSG_WN_TMP
#
#work_dir=`mktemp -d --tmpdir=$OSG_WN_TMP`
#cd $work_dir

# Filenaming
FILEROOT=FakeWaveform_${Detector}_${SUBRUN}
FILENAME=${OUTDIR}/${FILEROOT}
CSV_FILENAME=${FILENAME}.csv       # Fake input data
FAX_FILENAME=${FILENAME}_truth # fax truth info
PKL_FILENAME=${FILENAME}_truth.pkl # converted fax truth info
RAW_FILENAME=${FILENAME}_raw       # fax simulated raw data
PAX_FILENAME=${FILENAME}_pax       # pax processed data
PAX_FILENAME_WOPATH=${FILEROOT}_pax       # pax processed data without path
MERGEDTRUTH_FILENAME=${FILENAME}_merged_truth
MERGED_FILENAME=${FILENAME}_merged
HAX_FILENAME=${FILENAME}_hax       # hax reduced data
MINITREE_FILENAME=${FILENAME}_pax_S1S2Properties.root
CustomIniFilename=${RELEASEDIR}/NoS2Afterpulses.ini
NoPMTAfterpulseIniFilename=${RELEASEDIR}/NoPMTAfterpulses.ini
echo ${CustomIniFilename}


# Create the fake input data
python ${RELEASEDIR}/CreateFakeCSV_CorrelatedS1S2.py ${Detector} ${Input2DBandFile} ${Nomial_g1} ${Nomial_g2} ${NumEvents} ${RecoilType} ${CSV_FILENAME}

# Start of simulations #

# fax stage
if (($S2AfterpulseEnableFlag==0)); then
	if (($PMTAfterpulseEnableFlag==0)); then
		echo 'Both S2 and PMT afterpulse disabled'
		(time paxer --input ${CSV_FILENAME} --config ${Detector} reduce_raw_data Simulation --config_path ${NoPMTAfterpulseIniFilename} ${CustomIniFilename} --config_string "[WaveformSimulator]truth_file_name=\"${FAX_FILENAME}\"" --output ${RAW_FILENAME};) &> ${RAW_FILENAME}.log
	else
		echo 'Only S2 afterpulse disabled'
		(time paxer --input ${CSV_FILENAME} --config ${Detector} reduce_raw_data Simulation --config_path ${CustomIniFilename} --config_string "[WaveformSimulator]truth_file_name=\"${FAX_FILENAME}\"" --output ${RAW_FILENAME};) &> ${RAW_FILENAME}.log
	fi
else
	if (($PMTAfterpulseEnableFlag==0)); then
		echo 'Only PMT afterpulse disabled'
		(time paxer --input ${CSV_FILENAME} --config ${Detector} reduce_raw_data Simulation --config_path ${NoPMTAfterpulseIniFilename} --config_string "[WaveformSimulator]truth_file_name=\"${FAX_FILENAME}\"" --output ${RAW_FILENAME};) &> ${RAW_FILENAME}.log
	else
		echo 'Both S2 and PMT afterpulse enabled'
		(time paxer --input ${CSV_FILENAME} --config ${Detector} reduce_raw_data Simulation  --config_string "[WaveformSimulator]truth_file_name=\"${FAX_FILENAME}\"" --output ${RAW_FILENAME};) &> ${RAW_FILENAME}.log
	fi
fi

#	(time paxer --input ${CSV_FILENAME} --config ${Detector} reduce_raw_data Simulation --config_string "[WaveformSimulator]truth_file_name=\"${FAX_FILENAME}\"" --output ${RAW_FILENAME};) &> ${RAW_FILENAME}.log


# convert fax truth to pickle
python ${RELEASEDIR}/ConvertFaxTruthToPickle.py ${FAX_FILENAME} ${PKL_FILENAME}

# pax stage
(time paxer --ignore_rundb --input ${RAW_FILENAME} --config ${Detector} --output ${PAX_FILENAME};) &> ${PAX_FILENAME}.log

#~ # hax stage
#~ HAXPYTHON="import hax; "
#~ HAXPYTHON+="hax.init(main_data_paths=['${OUTDIR}'], minitree_paths=['${OUTDIR}'], pax_version_policy = 'loose'); "
#~ HAXPYTHON+="hax.minitrees.load('${PAX_FILENAME##*/}', ['Basics', 'Fundamentals']);"

#~ (time python -c "${HAXPYTHON}";)  &> ${HAX_FILENAME}.log


# custom minitree
(time python ${RELEASEDIR}/ReduceDataNormal.py ${PAX_FILENAME_WOPATH} ${OUTDIR};) &> ${HAX_FILENAME}.log

# merge
(time python ${RELEASEDIR}/TruthSorting.py ${FAX_FILENAME}.root ${MERGEDTRUTH_FILENAME}.pkl;) &> ${MERGEDTRUTH_FILENAME}.log
(time python ${RELEASEDIR}/MergeTruthAndProcessed.py   ${RELEASEDIR}/Configs/QingConfig ${MERGEDTRUTH_FILENAME}.pkl  ${MINITREE_FILENAME} ${MERGED_FILENAME}.pkl;) &> ${MERGED_FILENAME}.log


# Cleanup
rm -f pax*


#cd $start_dir
#rm -fr $work_dir
