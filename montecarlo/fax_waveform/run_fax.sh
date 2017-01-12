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
PhotonNumLower=$1
PhotonNumUpper=$2
ElectronNumLower=$3
ElectronNumUpper=$4

RecoilType=ER
IfS1S2Correlation=${10}

echo 'IfS1S2Correlation = ${IfS1S2Correlation}'
# enable s2 after pulse depending on the argument
# 1 for enable
PMTAfterpulseEnableFlag=$5
S2AfterpulseEnableFlag=$6

# Select fax+pax version
PAXVERSION=head

# Specify number of events
NumEvents=$7

# This run number (from command line argument)
SUBRUN=$9

########################################

# Setup the software
CVMFSDIR=/cvmfs/xenon.opensciencegrid.org
#~ export PATH="${CVMFSDIR}/releases/anaconda/2.4/bin:$PATH"
export PATH="/project/lgrandi/anaconda3/bin:$PATH" # changed @ 2016-12-29
source activate pax_${PAXVERSION} &> /dev/null

# Use path of this script for Python scripts below
# (In case user modified them)
#MY_PATH=`dirname \"$0\"`
MY_PATH=$(cd `dirname $0`; pwd)
echo $MY_PATH
RELEASEDIR=`( cd "$MY_PATH" && pwd )`

# Setting up directories
#start_dir=$PWD


OUTDIR=$8/${SUBRUN}
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
HAX_FILENAME=${FILENAME}_hax       # hax reduced data
CustomIniFilename=${RELEASEDIR}/NoS2Afterpulses.ini
NoPMTAfterpulseIniFilename=${RELEASEDIR}/NoPMTAfterpulses.ini
echo ${CustomIniFilename}


# Create the fake input data
python ${RELEASEDIR}/CreateFakeCSV.py ${Detector} ${NumEvents} ${PhotonNumLower} ${PhotonNumUpper} ${ElectronNumLower} ${ElectronNumUpper} ${RecoilType} ${CSV_FILENAME} ${IfS1S2Correlation}

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

# hax stage
HAXPYTHON="import hax; "
HAXPYTHON+="hax.init(main_data_paths=['${OUTDIR}'], minitree_paths=['${OUTDIR}'], pax_version_policy = 'loose'); "
HAXPYTHON+="hax.minitrees.load('${PAX_FILENAME##*/}', ['Basics', 'Fundamentals']);"

(time python -c "${HAXPYTHON}";)  &> ${HAX_FILENAME}.log

# Cleanup
rm -f pax*


#cd $start_dir
#rm -fr $work_dir
